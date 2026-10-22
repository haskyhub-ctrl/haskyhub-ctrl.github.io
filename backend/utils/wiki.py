"""Wiki tri thức PCCC: các trang chủ đề do AI biên soạn từ kho tài liệu, có trích dẫn Điều, cán bộ rà soát rồi mới bật.

Vì sao: tìm trực tiếp trong hàng nghìn đoạn văn bản dễ trượt (một câu hỏi cần ghép ý từ nhiều văn bản). Trang wiki gom sẵn,
ngắn gọn, đã đối chiếu văn bản mới nhất, nên khi bật thì được ưu tiên hơn đoạn thô (hệ số 1,8). Mỗi trang là một tài liệu
trong kho (nhóm "Wiki tri thức"), nên bật, tắt, sửa nội dung đều làm ngay trên trang Kho tài liệu AI.
Trang nháp KHÔNG được dùng để trả lời cho đến khi cán bộ bật.
"""
import os
import re
from datetime import datetime

from utils import local_rag

WIKI_WEIGHT = 1.8
GROUP_DRAFT = "Wiki tri thức"

TOPICS = [
    ("thuoc-dien-quan-ly", "Cơ sở thuộc diện quản lý về PCCC", "cơ sở thuộc diện quản lý về phòng cháy chữa cháy Phụ lục I Nghị định 105/2025 danh mục"),
    ("nguy-hiem-chay-no", "Cơ sở có nguy hiểm về cháy nổ (nhóm 1, nhóm 2)", "cơ sở có nguy hiểm về cháy nổ nhóm 1 nhóm 2 Phụ lục II Nghị định 105/2025"),
    ("tham-dinh-thiet-ke", "Thẩm định thiết kế PCCC: đối tượng, thẩm quyền, thủ tục", "thẩm định thiết kế về phòng cháy chữa cháy danh mục công trình thẩm quyền Phụ lục III Nghị định 347/2026"),
    ("quy-trinh-cong-trinh-moi", "Trình tự PCCC với công trình xây mới, cải tạo: thiết kế, thẩm định, thi công, nghiệm thu, khai báo", "trình tự thiết kế thẩm định thiết kế thi công nghiệm thu khai báo cơ sở dữ liệu đưa vào hoạt động công trình xây mới cải tạo chưa thẩm định"),
    ("nghiem-thu", "Nghiệm thu PCCC theo quy định mới", "nghiệm thu phòng cháy chữa cháy bãi bỏ thủ tục chủ đầu tư tự nghiệm thu khai báo cơ sở dữ liệu"),
    ("phuc-hoi-hoat-dong", "Phục hồi hoạt động sau tạm đình chỉ, đình chỉ", "phục hồi hoạt động tạm đình chỉ đình chỉ hoạt động bãi bỏ thủ tục Nghị quyết 66.18"),
    ("kiem-tra-dinh-ky", "Kiểm tra định kỳ về PCCC: tần suất, nội dung, trình tự", "kiểm tra an toàn về phòng cháy chữa cháy định kỳ đột xuất tần suất nội dung biên bản"),
    ("trach-nhiem-nguoi-dung-dau", "Trách nhiệm của người đứng đầu cơ sở về PCCC", "trách nhiệm người đứng đầu cơ sở phòng cháy chữa cháy"),
    ("doi-pccc-co-so", "Đội PCCC cơ sở, đội PCCC chuyên ngành, lực lượng tình nguyện", "đội phòng cháy chữa cháy cơ sở chuyên ngành thành lập điều kiện lực lượng tình nguyện"),
    ("huan-luyen", "Huấn luyện, bồi dưỡng nghiệp vụ PCCC", "huấn luyện bồi dưỡng nghiệp vụ phòng cháy chữa cháy đối tượng thời hạn giấy chứng nhận"),
    ("phuong-an-chua-chay", "Phương án chữa cháy, CNCH và thực tập phương án", "phương án chữa cháy cứu nạn cứu hộ xây dựng phê duyệt thực tập"),
    ("bao-hiem-chay-no", "Bảo hiểm cháy, nổ bắt buộc", "bảo hiểm cháy nổ bắt buộc đối tượng mua bảo hiểm"),
    ("trang-bi-ban-dau", "Trang bị phương tiện chữa cháy ban đầu (bình chữa cháy...)", "trang bị phương tiện phòng cháy chữa cháy ban đầu bình chữa cháy số lượng bố trí TCVN 3890"),
    ("bao-chay-tu-dong", "Hệ thống báo cháy tự động và thiết bị truyền tin báo cháy", "hệ thống báo cháy tự động thiết bị truyền tin báo cháy kết nối trung tâm thời hạn"),
    ("loi-thoat-nan", "Lối thoát nạn, chiếu sáng sự cố, chỉ dẫn thoát nạn", "lối thoát nạn chiếu sáng sự cố biển chỉ dẫn thoát nạn yêu cầu"),
    ("an-toan-dien", "An toàn điện trong phòng cháy chữa cháy", "an toàn điện phòng cháy chữa cháy ổ cắm dây dẫn aptomat quá tải hệ thống điện"),
    ("nha-o-nha-tro", "Nhà ở riêng lẻ, nhà trọ, nhà ở kết hợp kinh doanh", "nhà ở riêng lẻ nhà trọ nhà ở kết hợp kinh doanh phòng cháy chữa cháy yêu cầu"),
    ("chung-cu-cao-tang", "Chung cư, nhà cao tầng, nhà tập thể", "nhà chung cư nhà tập thể nhà cao tầng phòng cháy chữa cháy yêu cầu"),
    ("co-so-kinh-doanh", "Cơ sở kinh doanh: karaoke, nhà hàng, khách sạn, chợ, trung tâm thương mại", "karaoke vũ trường nhà hàng khách sạn chợ trung tâm thương mại phòng cháy chữa cháy"),
    ("kho-xuong-san-xuat", "Kho hàng, nhà xưởng, cơ sở sản xuất", "kho hàng nhà xưởng cơ sở sản xuất phòng cháy chữa cháy yêu cầu"),
    ("xang-dau-gas", "Cửa hàng xăng dầu, kho xăng dầu, khí đốt hóa lỏng (LPG)", "cửa hàng xăng dầu kho xăng dầu LPG khí đốt hóa lỏng phòng cháy chữa cháy"),
    ("truong-hoc-benh-vien", "Trường học, bệnh viện, cơ sở y tế", "trường học bệnh viện cơ sở y tế phòng cháy chữa cháy yêu cầu"),
    ("phuong-tien-giao-thong", "Phương tiện giao thông cơ giới và giấy phép lưu thông phương tiện PCCC", "phương tiện giao thông cơ giới phòng cháy chữa cháy giấy phép lưu thông phương tiện PCCC CNCH"),
    ("xu-phat", "Xử phạt vi phạm hành chính về PCCC (Nghị định 106/2025)", "xử phạt vi phạm hành chính phòng cháy chữa cháy mức phạt Nghị định 106/2025 hành vi"),
    ("khai-bao-csdl", "Khai báo, cập nhật cơ sở dữ liệu PCCC và kết nối truyền tin báo cháy", "khai báo cập nhật cơ sở dữ liệu phòng cháy chữa cháy thời hạn Phụ lục I truyền tin báo cháy 2027"),
    ("dang-nhap-phan-mem", "Đăng nhập và lập phiếu cơ sở trên phần mềm khai báo CSDL PCCC", "đăng nhập phần mềm khai báo cơ sở dữ liệu PCCC phiếu cơ sở gửi phiếu tài khoản"),
    ("ky-nang-xu-ly-chay", "Kỹ năng xử lý khi xảy ra cháy, thoát nạn, dùng bình chữa cháy", "kỹ năng xử lý khi cháy báo cháy 114 thoát nạn sử dụng bình chữa cháy xách tay"),
    ("hang-hoa-nguy-hiem", "Chất, hàng hóa nguy hiểm về cháy, nổ", "chất hàng hóa nguy hiểm về cháy nổ vận chuyển lưu trữ yêu cầu an toàn"),
    ("uy-ban-cap-xa", "Trách nhiệm của Ủy ban nhân dân cấp xã về PCCC", "trách nhiệm ủy ban nhân dân cấp xã phòng cháy chữa cháy quản lý địa bàn tổ liên gia"),
    ("dieu-kien-an-toan", "Điều kiện bảo đảm an toàn PCCC khi cơ sở hoạt động", "điều kiện bảo đảm an toàn về phòng cháy chữa cháy đối với cơ sở khi hoạt động"),
]
TOPIC_BY_SLUG = {t[0]: t for t in TOPICS}


def _page_id(slug: str) -> str:
    return f"wiki_{slug}.txt"


def status() -> list:
    man = local_rag.load_manifest()
    out = []
    for slug, title, _ in TOPICS:
        meta = man.get(_page_id(slug))
        out.append({
            "slug": slug, "title": title, "doc_id": _page_id(slug) if meta else None,
            "state": "none" if not meta else ("active" if meta.get("status") == "active" else "draft"),
            "chars": meta.get("chars", 0) if meta else 0, "updated_at": meta.get("uploaded_at") if meta else None,
        })
    return out


def _prompt(title: str, context: str) -> str:
    from utils.rag_search import CORE_LEGAL_PRINCIPLES_2026, OBSOLETE_TRANSITION_GUIDE
    obsolete = "\n".join(f"- {x}" for x in OBSOLETE_TRANSITION_GUIDE)
    return f"""Bạn là chuyên viên pháp chế PCCC của Công an thành phố Bắc Ninh, đang biên soạn một TRANG WIKI nội bộ để Trợ lý ảo Chi dùng làm căn cứ trả lời người dân.

CHỦ ĐỀ: {title}

QUY ĐỊNH MỚI NHẤT (ƯU TIÊN TUYỆT ĐỐI):
{CORE_LEGAL_PRINCIPLES_2026}

NỘI DUNG ĐÃ HẾT HIỆU LỰC (không dùng):
{obsolete}

TÀI LIỆU TRONG KHO (nguồn duy nhất để biên soạn):
{context}

YÊU CẦU:
- Chỉ dùng thông tin có trong tài liệu ở trên. Không bịa số liệu, ngưỡng, thời hạn, mức phạt, số điều. Chỗ nào tài liệu không nói rõ thì ghi "chưa có căn cứ trong kho".
- Ưu tiên văn bản mới nhất (NĐ 347/2026, NQ 66.18/2026). Quy định cũ đã bãi bỏ chỉ nhắc ngắn trong ngoặc đơn.
- Trang gồm: dòng đầu ">> " tóm tắt 2 đến 3 câu; các mục "## " (ví dụ: Đối tượng áp dụng, Quy định chính, Thủ tục hoặc các bước, Lưu ý); số liệu quan trọng bao bằng **hai dấu sao**; mỗi ý có căn cứ ghi cuối ý dạng {{{{Điều N, tên văn bản}}}}.
- Cuối trang có mục "## Câu hỏi thường gặp" với 3 đến 5 câu hỏi và đáp ngắn.
- Văn phong rõ ràng, mềm mỏng, không quy lỗi, không dùng dấu gạch ngang dài. Dài tối đa khoảng 700 từ.

Trả về DUY NHẤT JSON: {{"content": "toàn bộ nội dung trang wiki"}}"""


def generate(slug: str) -> dict:
    """Biên soạn (hoặc biên soạn lại) một trang wiki ở dạng NHÁP. Cần AI hoạt động."""
    from utils.rag_search import _call_llm, _extract_json_block
    from utils.chat_format import clean_reply
    topic = TOPIC_BY_SLUG.get(slug)
    if not topic:
        raise ValueError("Chủ đề không tồn tại")
    _, title, query = topic
    hits = local_rag.search_multi([query, title], k=10)
    if not hits:
        raise ValueError("Kho chưa có tài liệu liên quan chủ đề này")
    context = local_rag.format_hits(hits)[:14000]
    raw = _call_llm(_prompt(title, context), temperature=0.1, max_tokens=3500, is_json=True, fast=True, timeout=60.0)
    data = _extract_json_block(raw) or {}
    content = clean_reply(str(data.get("content") or ""))
    if len(content) < 200:
        raise ValueError("AI chưa soạn được nội dung")
    sources = sorted({h[0] for h in hits})[:10]
    stored = _page_id(slug)
    os.makedirs(local_rag.KHO_DIR, exist_ok=True)
    head = f"[Wiki: {title}]\n[Do AI biên soạn từ kho ngày {datetime.utcnow().strftime('%d/%m/%Y')}, cần cán bộ rà soát.]\n\n"
    with open(os.path.join(local_rag.KHO_DIR, stored), "w", encoding="utf-8") as f:
        f.write(head + content)
    man = local_rag.load_manifest()
    old = man.get(stored) or {}
    man[stored] = {
        "title": f"Wiki: {title}", "original_name": f"wiki/{slug}", "tier": 1, "status": "inactive",
        "effective_date": datetime.utcnow().strftime("%d/%m/%Y"),
        "note": "NHÁP do AI biên soạn từ: " + "; ".join(s[:70] for s in sources[:5]) + ". Cần cán bộ rà soát nội dung rồi mới bật.",
        "uploaded_at": datetime.utcnow().isoformat(), "chars": len(content), "chunks": local_rag.count_chunks(content),
        "needs_ocr": False, "from_wiki": True, "group": GROUP_DRAFT, "weight": WIKI_WEIGHT,
        "wiki_slug": slug, "admin_edited": old.get("admin_edited", False),
    }
    local_rag.save_manifest(man)
    local_rag.reindex()
    return {"doc_id": stored, "chars": len(content)}
