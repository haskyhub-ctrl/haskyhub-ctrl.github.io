"""Bước cuối của Trợ lý Chi: kiểm tra lại câu trả lời trước khi gửi cho người dân.

Quy trình:
  1. Rà tự động các nội dung đã hết hiệu lực (luật, nghị định cũ, thủ tục đã bãi bỏ) có xuất hiện trong câu trả lời không.
  2. Nhờ AI "thẩm định" lần hai: từng căn cứ, từng quy định nêu trong câu trả lời còn hiệu lực không,
       - còn hiệu lực: đối chiếu lại với các văn bản hiện hành và tài liệu hướng dẫn trong kho, sửa cho đúng;
       - hết hiệu lực: tra cứu văn bản thay thế rồi viết lại theo văn bản mới;
       - không đủ căn cứ: nói rõ là chưa đủ căn cứ, mời liên hệ cán bộ, và ghi vào hàng chờ câu hỏi khó.
  3. Nếu bước thẩm định lỗi (AI không phản hồi) mà vẫn còn dấu hiệu nội dung hết hiệu lực thì không gửi nguyên bản,
     thay bằng câu trả lời an toàn.
Bật tắt bằng biến môi trường CHAT_VERIFY (mặc định bật).
"""
import json
import os
import re

SAFE_REPLY = (
    ">> Chi chưa đủ căn cứ hiện hành để trả lời chắc chắn câu hỏi này, vì quy định liên quan có thể vừa được sửa đổi hoặc bãi bỏ." + chr(10) * 2 +
    "!! Bạn vui lòng liên hệ cán bộ Cảnh sát PCCC và CNCH đang quản lý cơ sở hoặc địa bàn của bạn để được hướng dẫn đúng quy định mới nhất."
)

# Dấu hiệu nội dung đã hết hiệu lực hoặc thủ tục đã bãi bỏ
_STALE_PATTERNS = [
    r"luật\s+(pccc|phòng cháy)[^.\n]{0,60}(2001|2013)", r"luật[^.\n]{0,40}27/2001",
    r"136/2020", r"50/2024", r"79/2014", r"149/2020", r"66/2014", r"3890\s*:\s*2009",
    r"nộp hồ sơ[^.\n]{0,80}nghiệm thu", r"hồ sơ đề nghị (kiểm tra )?nghiệm thu",
    r"hồ sơ đề nghị phục hồi", r"đơn đề nghị phục hồi", r"quyết định phục hồi hoạt động",
]
_STALE_RE = re.compile("|".join(_STALE_PATTERNS), re.IGNORECASE)


def enabled() -> bool:
    return os.getenv("CHAT_VERIFY", "true").lower() in ("true", "1", "yes")


def stale_hits(text: str) -> list:
    return sorted({m.group(0).strip() for m in _STALE_RE.finditer(text or "")})[:8]


def _verify_prompt(question: str, reply: str, doc_context: str, hits: list) -> str:
    from utils.rag_search import CORE_LEGAL_PRINCIPLES_2026, OBSOLETE_TRANSITION_GUIDE, CURRENT_LEGAL_REFS
    obsolete = "\n".join(f"- {x}" for x in OBSOLETE_TRANSITION_GUIDE)
    current = "\n".join(f"- {x}" for x in CURRENT_LEGAL_REFS)
    flagged = "\n".join(f"- {h}" for h in hits) or "(không có)"
    return f"""Bạn là chuyên viên thẩm định pháp luật PCCC của Công an thành phố Bắc Ninh. Nhiệm vụ: kiểm tra lần cuối một câu trả lời của Trợ lý ảo trước khi gửi cho người dân, nhất là xem nội dung có còn hiệu lực không.

CÂU HỎI CỦA NGƯỜI DÂN:
{question}

CÂU TRẢ LỜI NHÁP CẦN THẨM ĐỊNH:
{reply}

CÁC DẤU HIỆU HẾT HIỆU LỰC MÁY ĐÃ PHÁT HIỆN TRONG CÂU TRẢ LỜI (cần xem xét kỹ):
{flagged}

QUY ĐỊNH MỚI NHẤT (NĂM 2026, ƯU TIÊN TUYỆT ĐỐI):
{CORE_LEGAL_PRINCIPLES_2026}

DANH SÁCH VĂN BẢN HIỆN HÀNH:
{current}

DANH SÁCH NỘI DUNG ĐÃ HẾT HIỆU LỰC HOẶC ĐÃ BỊ BÃI BỎ:
{obsolete}

TÀI LIỆU TRONG KHO LIÊN QUAN (đối chiếu với tài liệu hướng dẫn):
{doc_context[:5000] if doc_context else '(không có)'}

CÁCH THẨM ĐỊNH, thực hiện theo thứ tự:
1. Liệt kê từng văn bản, điều khoản, thủ tục, thời hạn, mức xử phạt mà câu trả lời nêu ra.
2. Với mỗi mục, xác định: CÒN HIỆU LỰC, ĐÃ HẾT HIỆU LỰC hoặc BỊ BÃI BỎ, hay KHÔNG CHẮC. Chỉ coi là còn hiệu lực khi khớp với danh sách văn bản hiện hành hoặc tài liệu trong kho.
3. Mục còn hiệu lực: đối chiếu lại với quy định mới nhất và tài liệu hướng dẫn, sửa nếu sai số liệu, thời hạn, thẩm quyền.
4. Mục hết hiệu lực hoặc bị bãi bỏ: bỏ khỏi câu trả lời, nói rõ thủ tục đã bãi bỏ (nếu có trong quy định mới nhất), không mô tả lại quy trình cũ. Nếu cần biết văn bản thay thế mà chưa có trong tài liệu ở trên, đặt need_newer_search = true và nêu search_query ngắn gọn bằng tiếng Việt.
5. Mục KHÔNG CHẮC: không khẳng định, nói rõ chưa đủ căn cứ và mời liên hệ cán bộ Cảnh sát PCCC và CNCH.

QUY TẮC VIẾT LẠI: giữ nguyên cách trình bày của bản nháp (dòng ">> " là kết luận, "## " là tiêu đề mục, "!! " là lưu ý, số thứ tự cho các bước, **nhấn mạnh**, bảng, và căn cứ trong hai ngoặc nhọn kép); trợ lý tên là Chi, luôn xưng "Chi" và gọi người hỏi là "bạn", không xưng "tôi"; giọng cán bộ hướng dẫn, mềm mỏng, không quy lỗi; không dùng dấu gạch ngang dài; không bịa số hiệu văn bản, điều khoản, thời hạn, mức phạt; chỉ dùng những gì có căn cứ ở trên.

Trả về DUY NHẤT một object JSON hợp lệ:
{{
  "status": "ok" | "fix" | "insufficient",
  "outdated": [{{"item": "nội dung hết hiệu lực", "why": "lý do", "replacement": "văn bản hoặc quy định thay thế nếu biết"}}],
  "need_newer_search": true | false,
  "search_query": "từ khóa tra cứu văn bản mới nếu cần",
  "corrected_reply": "toàn bộ câu trả lời đã sửa cho người dân (để trống nếu status là ok)"
}}
Ý nghĩa status: "ok" là câu trả lời đúng và còn hiệu lực, giữ nguyên; "fix" là đã sửa trong corrected_reply; "insufficient" là chưa đủ căn cứ để trả lời chắc chắn."""


def _rewrite_prompt(question: str, draft: str, outdated: list, web_ctx: str) -> str:
    od = "\n".join(f"- {o.get('item')}: {o.get('why', '')}" for o in outdated) or "(không có)"
    return f"""Hãy viết lại câu trả lời của Trợ lý ảo PCCC cho đúng văn bản mới nhất, dựa trên thông tin tra cứu bên dưới.

CÂU HỎI: {question}

BẢN NHÁP (có nội dung hết hiệu lực):
{draft}

NỘI DUNG HẾT HIỆU LỰC CẦN BỎ:
{od}

THÔNG TIN TRA CỨU VĂN BẢN MỚI:
{web_ctx}

Quy tắc: chỉ dùng thông tin có trong phần tra cứu và những gì chắc chắn trong bản nháp; nếu phần tra cứu chưa đủ để nêu văn bản thay thế, nói rõ chưa đủ căn cứ và mời liên hệ cán bộ Cảnh sát PCCC và CNCH. Giữ cách trình bày của bản nháp (>>, ##, !!, **, bảng, căn cứ trong ngoặc nhọn kép), xưng "Chi" và gọi người hỏi là "bạn", giọng mềm mỏng, không gạch ngang dài, không bịa số hiệu văn bản.
Trả về DUY NHẤT JSON: {{"reply": "câu trả lời đã viết lại", "sufficient": true | false}}"""


def verify_answer(question: str, result: dict, budget: float = 28.0) -> dict:
    """Thẩm định và sửa câu trả lời. Trả (result, đã_sửa, cần_ghi_câu_hỏi_khó) trong dict kết quả: các khóa 'verified', 'fixed'."""
    from utils.rag_search import _call_llm, _extract_json_block, _clean_chat_formatting, search_internet

    doc_context = result.pop("_doc_context", "") or ""
    reply = result.get("reply") or ""
    if not reply.strip() or not enabled():
        return {"result": result, "fixed": False, "unresolved": False}

    hits = stale_hits(reply)
    verdict = None
    try:
        raw = _call_llm(_verify_prompt(question, reply, doc_context, hits), temperature=0.1, max_tokens=2500, is_json=True, fast=True, timeout=float(budget))
        verdict = _extract_json_block(raw)
    except Exception as e:
        print(f"[answer_check] Lỗi thẩm định: {e}")

    # AI không phản hồi: chỉ chặn khi còn dấu hiệu rõ ràng của nội dung hết hiệu lực
    if not verdict:
        if hits:
            result["reply"] = SAFE_REPLY
            result["suggestions"] = []
            return {"result": result, "fixed": True, "unresolved": True}
        return {"result": result, "fixed": False, "unresolved": False}

    status = verdict.get("status")
    outdated = verdict.get("outdated") if isinstance(verdict.get("outdated"), list) else []
    corrected = (verdict.get("corrected_reply") or "").strip()

    # Hết hiệu lực và chưa biết văn bản thay thế: tra cứu rồi viết lại một lần
    if status == "fix" and verdict.get("need_newer_search") and verdict.get("search_query"):
        try:
            web = search_internet(str(verdict["search_query"])[:150], max_results=3)
            web_ctx = "\n\n".join(f"{w.get('title', '')}: {w.get('snippet', '')} ({w.get('url', '')})" for w in web)
            if web_ctx.strip():
                raw2 = _call_llm(_rewrite_prompt(question, corrected or reply, outdated, web_ctx), temperature=0.1, max_tokens=2000, is_json=True, fast=True, timeout=25.0)
                v2 = _extract_json_block(raw2) or {}
                if v2.get("reply") and v2.get("sufficient"):
                    corrected = v2["reply"].strip()
                elif v2.get("reply") and not v2.get("sufficient"):
                    corrected = v2["reply"].strip()
                    status = "insufficient"
        except Exception as e:
            print(f"[answer_check] Lỗi tra cứu văn bản mới: {e}")

    if status == "ok":
        return {"result": result, "fixed": False, "unresolved": False}
    if status in ("fix", "insufficient") and corrected:
        result["reply"] = _clean_chat_formatting(corrected)
        # Các tham chiếu nêu trong bản nháp có thể đã hết hiệu lực: chỉ giữ danh mục văn bản hiện hành
        try:
            from utils.rag_search import CURRENT_LEGAL_REFS
            result["references"] = list(CURRENT_LEGAL_REFS[:3])
        except Exception:
            pass
        return {"result": result, "fixed": True, "unresolved": status == "insufficient"}
    if status == "insufficient" or hits:
        result["reply"] = SAFE_REPLY
        result["suggestions"] = []
        return {"result": result, "fixed": True, "unresolved": True}
    return {"result": result, "fixed": False, "unresolved": False}
