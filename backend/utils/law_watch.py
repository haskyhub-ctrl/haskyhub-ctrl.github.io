"""Theo dõi văn bản mới về PCCC và CNCH: mỗi tuần tự tìm trên mạng, lọc bằng AI, gom vào danh sách chờ cán bộ rà soát.

Quy trình:
  1. Tìm theo các từ khóa (Google News RSS, DuckDuckGo) và đọc chuyên mục PCCC trên cổng thông tin Công an Bắc Ninh.
  2. Bỏ các đường dẫn đã gặp. AI đánh giá từng mục: có phải văn bản hoặc hướng dẫn mới về PCCC, CNCH không, tóm tắt, gợi ý xử lý.
  3. Mục liên quan được ghi vào bảng law_candidates (trạng thái "new") để cán bộ xem ở trang Kho tài liệu AI, mục "Văn bản mới".
  4. Cán bộ bấm "Nạp vào kho" thì hệ thống tải nội dung về và lưu ở dạng NHÁP (chưa dùng để trả lời), rà soát xong mới bật.
Chạy tự động mỗi thứ Hai sau 7 giờ (giờ Việt Nam) và có thể chạy tay. Không tự đưa gì vào dữ liệu trả lời nếu chưa có người duyệt.
"""
import hashlib
import json
import os
import re
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from html import unescape
from urllib.parse import quote

import httpx

from utils import local_rag

VN_TZ = timezone(timedelta(hours=7))
STATE_PATH = os.path.join(os.path.dirname(local_rag.KHO_DIR), "law_watch_state.json")
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"}

QUERIES = [
    "văn bản mới phòng cháy chữa cháy và cứu nạn cứu hộ",
    "nghị định phòng cháy chữa cháy mới ban hành",
    "thông tư Bộ Công an phòng cháy chữa cháy mới",
    "bãi bỏ thủ tục hành chính phòng cháy chữa cháy",
    "quy chuẩn kỹ thuật quốc gia phòng cháy chữa cháy QCVN mới",
    "hướng dẫn cơ sở dữ liệu phòng cháy chữa cháy khai báo cập nhật",
    "Cục Cảnh sát PCCC và CNCH công văn hướng dẫn mới",
    "xử phạt vi phạm hành chính phòng cháy chữa cháy nghị định mới",
]
MAX_AGE_DAYS = 45


def _state() -> dict:
    try:
        with open(STATE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def _save_state(d: dict) -> None:
    os.makedirs(os.path.dirname(STATE_PATH), exist_ok=True)
    with open(STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False)


def last_run() -> dict:
    return _state()


def due(now=None) -> bool:
    """Đến hạn chạy hằng tuần: thứ Hai từ 7 giờ sáng (giờ Việt Nam), và lần chạy trước đã hơn 5 ngày."""
    now = now or datetime.now(VN_TZ)
    st = _state()
    try:
        last = datetime.fromisoformat(st["last_run"])
        if (now - last).total_seconds() < 5 * 86400:
            return False
    except Exception:
        pass
    return now.weekday() == 0 and now.hour >= 7


# ------------------------------------------------------------------ thu thập
def _rss(query: str) -> list:
    url = f"https://news.google.com/rss/search?q={quote(query + ' when:30d')}&hl=vi&gl=VN&ceid=VN:vi"
    out = []
    try:
        r = httpx.get(url, headers=UA, timeout=20, follow_redirects=True)
        if r.status_code != 200:
            return []
        root = ET.fromstring(r.content)
        for it in root.iter("item"):
            title = (it.findtext("title") or "").strip()
            link = (it.findtext("link") or "").strip()
            pub = it.findtext("pubDate") or ""
            src = (it.findtext("source") or "").strip()
            try:
                dt = parsedate_to_datetime(pub)
            except Exception:
                dt = None
            if dt and (datetime.now(timezone.utc) - dt.astimezone(timezone.utc)).days > MAX_AGE_DAYS:
                continue
            if title and link:
                out.append({"title": unescape(title), "url": link, "snippet": "", "published": dt.strftime("%d/%m/%Y") if dt else "", "source": src or "Google News"})
    except Exception as e:
        print(f"[law_watch] RSS lỗi '{query[:30]}': {e}")
    return out


def _ddg(query: str) -> list:
    try:
        from utils.rag_search import search_internet
        return [{"title": x["title"], "url": x["url"], "snippet": x.get("snippet", ""), "published": "", "source": "Tìm kiếm web"} for x in search_internet(query, max_results=5)]
    except Exception as e:
        print(f"[law_watch] Tìm web lỗi: {e}")
        return []


def _portal() -> list:
    """Chuyên mục PCCC trên cổng thông tin Công an Bắc Ninh."""
    out = []
    try:
        r = httpx.get("https://congan.bacninh.gov.vn/pages/category/1259/Phong-chay-chua-chay-va-cuu-nan-cuu-ho.html", headers=UA, timeout=25, follow_redirects=True)
        for m in re.finditer(r'<a[^>]+href="(/pages/news/\d+/[^"]+)"[^>]*>(.*?)</a>', r.text, re.S):
            title = re.sub(r"\s+", " ", unescape(re.sub(r"<[^>]+>", "", m.group(2)))).strip()
            if len(title) > 25:
                out.append({"title": title, "url": "https://congan.bacninh.gov.vn" + m.group(1), "snippet": "", "published": "", "source": "Công an Bắc Ninh"})
    except Exception as e:
        print(f"[law_watch] Cổng Công an Bắc Ninh lỗi: {e}")
    seen, uniq = set(), []
    for x in out:
        if x["url"] not in seen:
            seen.add(x["url"])
            uniq.append(x)
    return uniq[:25]


_LAW_HINT = re.compile(r"(nghị định|thông tư|nghị quyết|quy định|văn bản|hướng dẫn|bãi bỏ|quy chuẩn|qcvn|tcvn|công văn|cơ sở dữ liệu|thủ tục|luật|sửa đổi|bổ sung|hiệu lực|xử phạt|truyền tin báo cháy)", re.I)


def collect() -> list:
    items = []
    for q in QUERIES:
        items += _rss(q)
        if len(items) < 5:
            items += _ddg(q)
    items += _portal()
    seen, uniq = set(), []
    for x in items:
        key = x["url"].split("#")[0]
        # Lọc sơ bộ theo từ khóa để giảm số mục AI phải đánh giá (bỏ tin hoạt động, hội thi, diễn tập...)
        if key not in seen and _LAW_HINT.search(x["title"] + " " + x.get("snippet", "")):
            seen.add(key)
            uniq.append(x)
    return uniq


# ------------------------------------------------------------------ AI đánh giá
def _classify(batch: list) -> list:
    from utils.rag_search import _call_llm, _extract_json_block
    lines = "\n".join(f"{i}. {b['title']} | {b.get('snippet','')[:200]} | nguồn: {b.get('source','')} | ngày: {b.get('published','')}" for i, b in enumerate(batch))
    prompt = f"""Bạn giúp Công an thành phố Bắc Ninh theo dõi văn bản mới về phòng cháy chữa cháy (PCCC) và cứu nạn cứu hộ (CNCH). Dưới đây là các tin, bài tìm được. Với mỗi mục, đánh giá:
- relevant: true nếu là văn bản quy phạm pháp luật, công văn, hướng dẫn nghiệp vụ, quy chuẩn, hoặc tin NÓI RÕ về quy định mới, sửa đổi, bãi bỏ liên quan PCCC, CNCH, cơ sở dữ liệu PCCC. false nếu chỉ là tin hoạt động, vụ cháy, tuyên truyền chung, quảng cáo.
- kind: "Văn bản quy phạm" | "Công văn, hướng dẫn" | "Tin về quy định mới" | "Khác"
- summary: 1 đến 2 câu nêu văn bản nào, thay đổi gì (chỉ dùng thông tin có trong mục, không suy đoán)
- hint: gợi ý cho cán bộ, ví dụ "nên nạp vào kho", "cần rà văn bản cũ bị thay thế", "chỉ là tin tức, bỏ qua"

DANH SÁCH:
{lines}

Trả về DUY NHẤT JSON: {{"items": [{{"i": 0, "relevant": true, "kind": "...", "summary": "...", "hint": "..."}}]}}"""
    try:
        raw = _call_llm(prompt, temperature=0.1, max_tokens=2500, is_json=True, fast=True, timeout=45.0)
        data = _extract_json_block(raw) or {}
        return data.get("items") or []
    except Exception as e:
        print(f"[law_watch] AI đánh giá lỗi: {e}")
        return []


def run(db) -> dict:
    """Chạy một lượt theo dõi. Trả {found, new, relevant}."""
    from models import LawCandidate
    items = collect()
    known = {u for (u,) in db.query(LawCandidate.url).all()}
    fresh = [x for x in items if x["url"].split("#")[0] not in known]
    new_rows = []
    for x in fresh:
        row = LawCandidate(url=x["url"].split("#")[0], title=x["title"][:500], snippet=(x.get("snippet") or "")[:600],
                           source=(x.get("source") or "")[:120], published=x.get("published") or "", status="new")
        db.add(row)
        new_rows.append(row)
    db.commit()
    relevant = 0
    for i in range(0, len(new_rows), 8):
        batch = new_rows[i:i + 8]
        verdicts = _classify([{"title": r.title, "snippet": r.snippet, "source": r.source, "published": r.published} for r in batch])
        by_i = {int(v.get("i", -1)): v for v in verdicts if isinstance(v, dict)}
        for j, row in enumerate(batch):
            v = by_i.get(j)
            if v is None:          # AI không phản hồi: giữ lại để cán bộ tự xem
                row.relevant = True
                row.summary = ""
                relevant += 1
                continue
            row.relevant = bool(v.get("relevant"))
            row.kind = str(v.get("kind") or "")[:60]
            row.summary = str(v.get("summary") or "")[:600]
            row.hint = str(v.get("hint") or "")[:300]
            if not row.relevant:
                row.status = "ignored"
            else:
                relevant += 1
    db.commit()
    result = {"found": len(items), "new": len(new_rows), "relevant": relevant, "at": datetime.now(VN_TZ).isoformat()}
    _save_state({"last_run": result["at"], **{k: v for k, v in result.items() if k != "at"}})
    _notify(db, result)
    return result


def _notify(db, result: dict) -> None:
    """Gửi bản tóm tắt qua Telegram nếu có đặt LAW_WATCH_TELEGRAM_CHAT_ID (nhóm riêng, không dùng nhóm báo cháy 114)."""
    chat = os.getenv("LAW_WATCH_TELEGRAM_CHAT_ID", "").strip()
    token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    if not chat or not token or not result.get("relevant"):
        return
    from models import LawCandidate
    rows = db.query(LawCandidate).filter(LawCandidate.status == "new", LawCandidate.relevant.is_(True)).order_by(LawCandidate.found_at.desc()).limit(10).all()
    lines = [f"📚 <b>Văn bản mới về PCCC, CNCH cần rà soát</b> ({len(rows)} mục)"]
    for r in rows:
        lines.append(f"• {r.title[:140]}" + (f"\n  <i>{r.summary[:160]}</i>" if r.summary else ""))
    lines.append("\nMở trang Kho tài liệu AI, mục Văn bản mới để xem và duyệt.")
    try:
        httpx.post(f"https://api.telegram.org/bot{token}/sendMessage", json={"chat_id": chat, "text": "\n".join(lines)[:3800], "parse_mode": "HTML", "disable_web_page_preview": True}, timeout=10)
    except Exception as e:
        print(f"[law_watch] Telegram lỗi: {e}")


# ------------------------------------------------------------------ nạp nội dung về kho (dạng nháp)
def _html_to_text(html: str) -> str:
    html = re.sub(r"(?is)<(script|style|nav|header|footer|aside|form)[^>]*>.*?</\1>", " ", html)
    m = re.search(r'(?is)<(article|div)[^>]+(class|id)="[^"]*(content|detail|article|post|noidung|news)[^"]*"[^>]*>(.*)', html)
    body = m.group(4) if m else html
    body = re.sub(r"(?i)</(p|div|li|h\d|tr)>", "\n", body)
    body = re.sub(r"(?i)<br\s*/?>", "\n", body)
    text = unescape(re.sub(r"<[^>]+>", " ", body))
    text = re.sub(r"[ \t\r\f\v]+", " ", text)
    text = re.sub(r"\n\s*\n+", "\n\n", text)
    return text.strip()


def resolve_google_news(url: str) -> str:
    """Đường dẫn trong Google News RSS là đường dẫn chuyển tiếp; giải ra đường dẫn bài viết gốc. Không giải được thì trả lại nguyên đường dẫn."""
    import base64
    if "news.google.com" not in url:
        return url
    m = re.search(r"/articles/([^?/]+)", url)
    if not m:
        return url
    gid = m.group(1)
    try:
        raw = base64.urlsafe_b64decode(gid + "=" * (-len(gid) % 4))
        if raw.startswith(b"\x08\x13\x22"):                      # dạng cũ: chứa sẵn đường dẫn
            ln = raw[3]
            off = 4
            if ln >= 0x80:
                ln = (ln & 0x7F) | (raw[4] << 7)
                off = 5
            cand = raw[off:off + ln].decode("utf-8", "ignore")
            if cand.startswith("http"):
                return cand
    except Exception:
        pass
    try:
        page = httpx.get(f"https://news.google.com/articles/{gid}", headers=UA, timeout=20, follow_redirects=True).text
        sg = re.search(r'data-n-a-sg="([^"]+)"', page)
        ts = re.search(r'data-n-a-ts="([^"]+)"', page)
        if not sg or not ts:
            return url
        inner = json.dumps(["garturlreq", [["X", "X", ["X", "X"], None, None, 1, 1, "US:en", None, 1, None, None, None, None, None, 0, 1], "X", "X", 1, [1, 1, 1], 1, 1, None, 0, 0, None, 0], gid, int(ts.group(1)), sg.group(1)])
        freq = json.dumps([[["Fbv4je", inner, None, "generic"]]])
        r = httpx.post("https://news.google.com/_/DotsSplashUi/data/batchexecute", data={"f.req": freq},
                       headers={**UA, "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"}, timeout=20)
        bs = chr(92)
        mm = re.search('garturlres' + re.escape(bs + chr(34)) + ',' + re.escape(bs + chr(34)) + '(https?:[^' + re.escape(chr(34) + bs) + ']+)', r.text)
        if mm:
            return mm.group(1).replace(bs + 'u003d', '=').replace(bs + 'u0026', '&')
    except Exception as e:
        print(f"[law_watch] Không giải được đường dẫn Google News: {e}")
    return url


def ingest_url(url: str, title: str = "") -> dict:
    """Tải nội dung từ đường dẫn và lưu thành tài liệu NHÁP trong kho (chưa dùng để trả lời). Trả {id, chars}."""
    import tempfile
    url = resolve_google_news(url)
    r = httpx.get(url, headers=UA, timeout=60, follow_redirects=True)
    r.raise_for_status()
    ctype = (r.headers.get("content-type") or "").lower()
    if "pdf" in ctype or url.lower().split("?")[0].endswith(".pdf"):
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
            f.write(r.content)
            tmp = f.name
        try:
            text = local_rag.read_text(tmp)
        finally:
            os.remove(tmp)
    else:
        text = _html_to_text(r.text)
    text = text.strip()
    if len(text) < 300:
        raise ValueError("Nội dung tải về quá ngắn hoặc không đọc được chữ (có thể là bản quét hoặc trang cần đăng nhập).")
    sid = "web_" + hashlib.sha1(url.encode("utf-8")).hexdigest()[:12]
    stored = f"{sid}.txt"
    os.makedirs(local_rag.KHO_DIR, exist_ok=True)
    head = f"[{title or url}]\n[Nguồn: {url}. Nạp ngày {datetime.now(VN_TZ).strftime('%d/%m/%Y')}. Trạng thái: NHÁP, chờ cán bộ rà soát.]\n\n"
    with open(os.path.join(local_rag.KHO_DIR, stored), "w", encoding="utf-8") as f:
        f.write(head + text)
    man = local_rag.load_manifest()
    man[stored] = {
        "title": (title or url)[:200], "original_name": url, "tier": 2, "status": "inactive", "effective_date": "",
        "note": f"NHÁP: tải từ {url}. Cần cán bộ rà soát nội dung, ngày hiệu lực, văn bản bị thay thế rồi mới bật.",
        "uploaded_at": datetime.utcnow().isoformat(), "chars": len(text), "chunks": local_rag.count_chunks(text),
        "needs_ocr": False, "from_web": True, "group": "Văn bản mới (chờ duyệt)", "weight": 1.0,
    }
    local_rag.save_manifest(man)
    local_rag.reindex()
    return {"id": stored, "chars": len(text)}


async def weekly_loop():
    """Vòng lặp nền: mỗi giờ kiểm tra đã đến hạn chạy hằng tuần chưa."""
    import asyncio
    from database import SessionLocal
    await asyncio.sleep(90)
    while True:
        try:
            if due():
                db = SessionLocal()
                try:
                    res = await asyncio.to_thread(run, db)
                    print(f"[law_watch] Đã chạy theo dõi hằng tuần: {res}")
                finally:
                    db.close()
        except asyncio.CancelledError:
            break
        except Exception as e:
            print(f"[law_watch] Lỗi vòng lặp: {e}")
        await asyncio.sleep(3600)
