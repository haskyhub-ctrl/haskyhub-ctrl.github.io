"""
RAG Search: Trợ lý Chi
Priority: NotebookLM CLI (1) → ChromaDB (2) → Gemini general knowledge (3)

Luật hiện hành 2024-2025 (cứng):
- Luật PCCC 55/2024/QH15 (thay Luật 2001, 2013)
- Nghị định 105/2025/NĐ-CP (thay NĐ 136/2020)
- QCVN 06:2022/BXD + Sửa đổi 1:2023
- QCVN 10:2025/BCA (thay TCVN 3890:2009)
- QCVN 25:2025/BCT, QCVN 25:2025/BKHCN

NOTE: Dùng httpx REST API trực tiếp thay LangChain để tránh
      lỗi model override (PERMISSION_DENIED với gemini-2.5-flash).
"""
import os
import json
import httpx
import subprocess
import sys
import re
from html import unescape
from urllib.parse import unquote
from dotenv import load_dotenv

env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
if os.path.exists(env_path):
    load_dotenv(dotenv_path=env_path, override=True)
else:
    load_dotenv(override=True)


def _safe_print(msg: str) -> None:
    """In ra console, bỏ qua ký tự không encode được (Windows cp1252)."""
    try:
        print(msg)
    except UnicodeEncodeError:
        print(msg.encode("ascii", errors="replace").decode("ascii"))


# ─── Quy định pháp lý cốt lõi năm 2026 (Ưu tiên tuyệt đối) ──────────────
CORE_LEGAL_PRINCIPLES_2026 = """
QUY ĐỊNH PHÁP LUẬT PCCC MỚI NHẤT (NĂM 2026) - ƯU TIÊN ÁP DỤNG TUYỆT ĐỐI:
1. VỀ NGHIỆM THU PCCC (BÃI BỎ THỦ TỤC HÀNH CHÍNH NỘP HỒ SƠ TẠI CƠ QUAN NHÀ NƯỚC):
   - Căn cứ: Nghị quyết số 66.18/2026/NQ-CP ngày 18/5/2026 của Chính phủ (hiệu lực từ 01/07/2026) và Nghị định số 347/2026/NĐ-CP ngày 08/9/2026 của Chính phủ (hiệu lực từ 15/9/2026) sửa đổi, bổ sung Nghị định số 105/2025/NĐ-CP:
   - CHÍNH THỨC BÃI BỎ thủ tục hành chính kiểm tra công tác nghiệm thu về PCCC và bãi bỏ việc cấp văn bản chấp thuận kết quả nghiệm thu của cơ quan Công an và cơ quan chuyên môn về xây dựng.
   - Do đó, chủ đầu tư/chủ sở hữu công trình KHÔNG PHẢI NỘP HỒ SƠ ĐỀ NGHỊ NGHIỆM THU ĐẾN CƠ QUAN CÔNG AN HAY CƠ QUAN XÂY DỰNG NỮA. Mọi quy định cũ trước đây về nộp hồ sơ xin kiểm tra nghiệm thu (như tại Nghị định 105/2025/NĐ-CP cũ và Nghị định 136/2020/NĐ-CP) đều đã bị bãi bỏ.
   - Trình tự thực hiện hiện nay:
     + Chủ đầu tư/chủ sở hữu công trình tự tổ chức nghiệm thu các nội dung về PCCC cùng các nhà thầu (tư vấn thiết kế, thi công, tư vấn giám sát) theo đúng hồ sơ thiết kế đã được thẩm duyệt và tiêu chuẩn, quy chuẩn hiện hành.
     + Chủ đầu tư lập biên bản, hồ sơ nghiệm thu hoàn thành và hoàn toàn tự chịu trách nhiệm trước pháp luật về kết quả nghiệm thu và an toàn PCCC khi đưa công trình vào vận hành.
     + Trước khi đưa công trình, phương tiện vào sử dụng, chủ đầu tư chỉ cần thực hiện KHAI BÁO THÔNG TIN TRÊN HỆ THỐNG CƠ SỞ DỮ LIỆU VỀ PCCC.
     + Cơ quan Công an và UBND chuyển sang cơ chế HẬU KIỂM / KIỂM TRA ĐỊNH KỲ (kiểm tra định kỳ 01 năm/lần đối với nhóm có nguy cơ cao; 02 năm/lần đối với nhóm còn lại; có kế hoạch và thông báo trước 03 ngày làm việc).

1a. TRÌNH TỰ ĐẦY ĐỦ ĐỐI VỚI CÔNG TRÌNH XÂY MỚI HOẶC CẢI TẠO (KHÔNG ĐƯỢC BỎ SÓT KHI TRẢ LỜI VỀ NGHIỆM THU, ĐƯA VÀO HOẠT ĐỘNG):
   - Bãi bỏ thủ tục kiểm tra nghiệm thu KHÔNG có nghĩa là bỏ thẩm định thiết kế. Nghiệm thu chỉ làm được khi trước đó đã có thiết kế đã được thẩm định.
   - Chuỗi bước: (1) Lập thiết kế về PCCC; (2) Xác định công trình có thuộc diện phải thẩm định thiết kế về PCCC không (theo danh mục tại Phụ lục III Nghị định 347/2026/NĐ-CP, căn cứ loại công trình, số tầng, diện tích sàn, khối tích...); (3) nếu thuộc diện: nộp hồ sơ để cơ quan có thẩm quyền THẨM ĐỊNH thiết kế và chỉ thi công khi thiết kế đã được thẩm định; nếu không thuộc diện: chủ đầu tư tự bảo đảm thiết kế đúng quy chuẩn, tiêu chuẩn; (4) Thi công đúng thiết kế; (5) Chủ đầu tư cùng các nhà thầu TỰ NGHIỆM THU, lập biên bản, tự chịu trách nhiệm; (6) Khai báo trên Hệ thống cơ sở dữ liệu về PCCC; (7) Đưa vào hoạt động, chịu kiểm tra định kỳ (hậu kiểm).
   - Nếu người hỏi nói công trình đã xây hoặc chưa được thẩm định thiết kế mà thuộc diện phải thẩm định, phải nói rõ: cần quay lại làm bước thiết kế bổ sung và thẩm định thiết kế theo quy định trước, không thể chỉ tự nghiệm thu rồi đưa vào hoạt động; mời liên hệ cán bộ Cảnh sát PCCC và CNCH để được hướng dẫn xử lý trường hợp cụ thể.

1b. VỀ PHỤC HỒI HOẠT ĐỘNG SAU KHI BỊ TẠM ĐÌNH CHỈ, ĐÌNH CHỈ (ĐÃ BÃI BỎ THỦ TỤC):
   - Theo Nghị quyết số 66.18/2026/NQ-CP, thủ tục hành chính phục hồi hoạt động của cơ sở, phương tiện, hộ gia đình đã bị tạm đình chỉ hoạt động, đình chỉ hoạt động ĐÃ ĐƯỢC BÃI BỎ.
   - Khi người dùng hỏi về thủ tục, hồ sơ, trình tự, thời hạn phục hồi hoạt động: nói rõ ngay thủ tục này đã được bãi bỏ, cơ sở KHÔNG phải làm hồ sơ đề nghị phục hồi hoạt động và KHÔNG có bước nộp hồ sơ hay chờ cơ quan kiểm tra rồi ra quyết định phục hồi.
   - TUYỆT ĐỐI KHÔNG mô tả lại quy trình cũ: không nêu đơn đề nghị phục hồi, không nêu hồ sơ nộp qua bưu chính hay Cổng dịch vụ công, không nêu thời hạn 05 ngày làm việc, không nêu quyết định phục hồi hoạt động. Các nội dung này (từ Điều 18 Nghị định 136/2020/NĐ-CP, Nghị định 50/2024/NĐ-CP hay các tài liệu nội bộ cũ) đã hết hiệu lực.
   - Chỉ nêu những gì có căn cứ trong tài liệu hiện hành. Nếu chưa có hướng dẫn chi tiết về cách thực hiện sau khi bãi bỏ, nói thẳng điều đó và mời người hỏi liên hệ cán bộ Cảnh sát PCCC và CNCH đã ra quyết định hoặc đang quản lý cơ sở để được hướng dẫn. Không tự bịa quy trình thay thế.
   - Lời khuyên chung vẫn đúng: khắc phục triệt để các vi phạm, tồn tại, giữ lại bằng chứng khắc phục (ảnh, biên bản, hóa đơn).

1c. VỀ CHỨNG NHẬN HUẤN LUYỆN PCCC (ĐÃ BÃI BỎ):
   - Chứng nhận huấn luyện nghiệp vụ PCCC và CNCH (thẻ/giấy chứng nhận cấp sau mỗi khóa học) ĐÃ BỊ BÃI BỎ theo Luật PCCC và CNCH số 55/2024/QH15 và Nghị định 105/2025/NĐ-CP. KHÔNG CÒN cấp chứng nhận riêng theo từng khóa và KHÔNG CÒN quy định về thời hạn giá trị của chứng nhận.
   - Cơ chế thay thế hiện hành: Huấn luyện nghiệp vụ phòng cháy, chữa cháy, cứu nạn, cứu hộ được thực hiện định kỳ 05 năm một lần; bồi dưỡng nghiệp vụ phòng cháy, chữa cháy, cứu nạn, cứu hộ được thực hiện định kỳ hằng năm theo Nghị định 105/2025/NĐ-CP.
   - KHI NGƯỜI DÙNG HỎI VỀ THỜI HẠN CỦA CHỨNG NHẬN HUẤN LUYỆN: BẮT BUỘC trả lời rõ ràng: Chứng nhận huấn luyện nghiệp vụ PCCC và CNCH đã được bãi bỏ, không còn cấp chứng nhận hay quy định thời hạn của chứng nhận; thay vào đó, việc huấn luyện nghiệp vụ PCCC và CNCH được thực hiện định kỳ 05 năm một lần, bồi dưỡng nghiệp vụ thực hiện định kỳ hằng năm theo Nghị định 105/2025/NĐ-CP.
   - TUYỆT ĐỐI KHÔNG nói "chứng nhận có thời hạn 05 năm" kiểu cũ (khoản 4 Điều 46 Nghị định 105 cũ trước đây) vì điều đó sai bản chất pháp lý hiện hành.

1d. VỀ THỜI GIAN HUẤN LUYỆN NGHIỆP VỤ PCCC (BẮT BUỘC LIỆT KÊ ĐẦY ĐỦ 6 NHÓM ĐỐI TƯỢNG):
   - Căn cứ: Điều 29 Nghị định số 105/2025/NĐ-CP (được sửa đổi, bổ sung bởi Điều 22 Nghị định số 347/2026/NĐ-CP):
   - KHI HỎI VỀ THỜI GIAN/THỜI LƯỢNG HUẤN LUYỆN PCCC: BẮT BUỘC LIỆT KÊ ĐẦY ĐỦ TẤT CẢ 6 NHÓM ĐỐI TƯỢNG (trình bày dạng bảng hoặc danh sách từng nhóm rõ ràng), TUYỆT ĐỐI KHÔNG ĐƯỢC chỉ chọn 1 nhóm "cá nhân thực hiện nhiều nhiệm vụ" mà bỏ sót các nhóm khác:
     1. Người đứng đầu cơ sở, cơ quan, tổ chức:
        + Huấn luyện lần đầu: Từ 16 giờ đến 24 giờ.
        + Bồi dưỡng định kỳ hằng năm: Từ 08 giờ đến 12 giờ.
     2. Thành viên Đội PCCC và CNCH cơ sở, Đội PCCC và CNCH chuyên ngành:
        + Huấn luyện lần đầu: Từ 32 giờ đến 48 giờ.
        + Bồi dưỡng định kỳ hằng năm: Từ 16 giờ đến 24 giờ.
     3. Người làm việc trong môi trường có nguy hiểm về cháy, nổ hoặc thường xuyên tiếp xúc với chất, hàng hóa nguy hiểm về cháy, nổ:
        + Huấn luyện lần đầu: Từ 16 giờ đến 24 giờ.
        + Bồi dưỡng định kỳ hằng năm: Từ 08 giờ đến 12 giờ.
     4. Trưởng thôn, Tổ trưởng tổ dân phố, Đội trưởng, Đội phó và thành viên Đội dân phòng:
        + Huấn luyện lần đầu: Từ 16 giờ đến 24 giờ.
        + Bồi dưỡng định kỳ hằng năm: Từ 08 giờ đến 12 giờ.
     5. Người điều khiển phương tiện giao thông cơ giới đường bộ vận chuyển chất, hàng nguy hiểm về cháy, nổ:
        + Huấn luyện lần đầu: Từ 16 giờ đến 24 giờ.
        + Bồi dưỡng định kỳ hằng năm: Từ 08 giờ đến 12 giờ.
     6. Cá nhân thực hiện nhiều nhiệm vụ thuộc các đối tượng trên:
        + Huấn luyện lần đầu: Từ 24 giờ đến 32 giờ.
        + Bồi dưỡng định kỳ hằng năm: Từ 08 giờ đến 12 giờ.
2. CÁC VĂN BẢN HIỆN HÀNH CHÍNH:
   - Nghị định số 347/2026/NĐ-CP ngày 08/9/2026 của Chính phủ (hiệu lực 15/9/2026, sửa đổi NĐ 105/2025/NĐ-CP, bãi bỏ văn bản chấp thuận nghiệm thu PCCC)
   - Nghị quyết số 66.18/2026/NQ-CP ngày 18/5/2026 của Chính phủ (hiệu lực 01/07/2026, bãi bỏ thủ tục kiểm tra nghiệm thu PCCC)
   - Luật Phòng cháy, chữa cháy và Cứu nạn, cứu hộ số 55/2024/QH15
   - Nghị định số 105/2025/NĐ-CP (được sửa đổi, bổ sung bởi Nghị định 347/2026/NĐ-CP)
   - Nghị định số 106/2025/NĐ-CP và Nghị định 69/2026/NĐ-CP (xử phạt vi phạm hành chính PCCC)
   - QCVN 06:2022/BXD kèm Sửa đổi 1:2023
   - QCVN 10:2025/BCA (thay thế TCVN 3890:2009)
"""

OBSOLETE_TRANSITION_GUIDE = [
    "Nghị quyết 66.18/2026/NQ-CP & Nghị định 347/2026/NĐ-CP: Bãi bỏ thủ tục nộp hồ sơ xin nghiệm thu PCCC tại cơ quan nhà nước; Chủ đầu tư tự tổ chức nghiệm thu với nhà thầu và khai báo CSDL PCCC.",
    "Nghị định 105/2025/NĐ-CP quy định cũ về nộp hồ sơ nghiệm thu tại cơ quan nhà nước → Đã được bãi bỏ, sửa đổi bởi Nghị quyết 66.18 và Nghị định 347.",
    "Thủ tục phục hồi hoạt động sau khi bị tạm đình chỉ, đình chỉ (Điều 18 NĐ 136/2020/NĐ-CP, NĐ 50/2024/NĐ-CP) → Đã bị bãi bỏ theo Nghị quyết 66.18/2026/NQ-CP, không còn hồ sơ đề nghị hay thời hạn giải quyết.",
    "Nghị định 136/2020/NĐ-CP & Nghị định 50/2024/NĐ-CP → Đã hết hiệu lực.",
    "Luật PCCC 2001 & Luật PCCC 2013 → Đã hết hiệu lực, thay bởi Luật 55/2024/QH15.",
    "Thông tư 149/2020/TT-BCA → Đã hết hiệu lực.",
    "TCVN 3890:2009 → Đã thay thế bởi QCVN 10:2025/BCA.",
]

OBSOLETE_LAWS = [
    "Luật PCCC 2001", "Luật PCCC 2013", "Luật sửa đổi PCCC 2013",
    "Nghị định 136/2020/NĐ-CP", "Nghị định 50/2024/NĐ-CP", "Nghị định 79/2014/NĐ-CP",
    "Thông tư 149/2020/TT-BCA", "Thông tư 66/2014/TT-BCA",
    "TCVN 3890:2009",
]

CURRENT_LEGAL_REFS = [
    "Nghị quyết số 66.18/2026/NQ-CP ngày 18/5/2026 của Chính phủ",
    "Nghị định số 347/2026/NĐ-CP ngày 08/9/2026 của Chính phủ",
    "Luật Phòng cháy, chữa cháy và Cứu nạn, cứu hộ số 55/2024/QH15",
    "Nghị định 105/2025/NĐ-CP (sửa đổi bởi NĐ 347/2026/NĐ-CP)",
    "QCVN 06:2022/BXD kèm Sửa đổi 1:2023",
    "QCVN 10:2025/BCA",
]

CHROMA_DB_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "chroma_db")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")


def _get_notebook_ids() -> list[str]:
    """Lấy danh sách các Notebook ID (hỗ trợ nhiều sổ cách nhau bằng dấu phẩy)."""
    raw = os.getenv("NOTEBOOKLM_PROJECT_ID", "")
    if not raw:
        return []
    return [i.strip() for i in raw.split(",") if i.strip()]

# Danh sách model Gemini ổn định theo thứ tự ưu tiên (tự động fallback nếu Google đổi model)
GEMINI_FALLBACK_MODELS = [
    "gemini-3.5-flash",
    "gemini-3.8-flash",
    "gemini-2.5-flash",
    "gemini-3.5-flash-lite",
    "gemini-2.5-flash-lite",
]
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")
GEMINI_EMBED_MODEL = os.getenv("GEMINI_EMBED_MODEL", "models/gemini-embedding-001")


# ════════════════════════════════════════════════════════════════
#  HELPER: Gọi Gemini REST API trực tiếp (hỗ trợ tự động fallback model)
# ════════════════════════════════════════════════════════════════

def _extract_json_block(text: str) -> dict | None:
    """Trích xuất và parse object JSON từ phản hồi của mô hình."""
    if not text:
        return None
    # 1. Thử parse trực tiếp
    try:
        data = json.loads(text.strip())
        if isinstance(data, dict):
            return data
    except Exception:
        pass

    # 2. Markdown fence ```json
    if "```json" in text:
        try:
            raw = text.split("```json")[1].split("```")[0].strip()
            data = json.loads(raw)
            if isinstance(data, dict):
                return data
        except Exception:
            pass

    if "```" in text:
        try:
            raw = text.split("```")[1].split("```")[0].strip()
            data = json.loads(raw)
            if isinstance(data, dict):
                return data
        except Exception:
            pass

    # 3. Tìm khối {...} bao quanh
    start_idx = text.find("{")
    end_idx = text.rfind("}")
    if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
        try:
            candidate = text[start_idx:end_idx + 1]
            data = json.loads(candidate)
            if isinstance(data, dict):
                return data
        except Exception:
            pass

    # 4. Regex trích xuất trường "reply" nếu JSON bị cắt cụt hoặc không đóng ngoặc
    match = re.search(r'"reply"\s*:\s*"((?:[^"\\]|\\.)*)', text)
    if match:
        extracted = match.group(1).replace('\\"', '"').replace('\\n', '\n').replace('\\t', '\t')
        return {
            "reply": extracted,
            "suggestions": [],
            "references": []
        }

    return None


def _call_gemini_sync(prompt: str, temperature: float = 0.15, max_tokens: int = 2048, is_json: bool = False) -> str:
    """
    Gọi Gemini API qua httpx đồng bộ.
    Tự động thử các model dự phòng nếu gặp lỗi 404 (model deprecated), 429 (rate limit), 500, 503.
    """
    api_key = os.getenv("GEMINI_API_KEY") or GEMINI_API_KEY
    if not api_key:
        raise ValueError("GEMINI_API_KEY chưa được cấu hình")

    primary_model = os.getenv("GEMINI_MODEL") or GEMINI_MODEL or "gemini-3.5-flash"
    models_to_try = [primary_model] + [m for m in GEMINI_FALLBACK_MODELS if m != primary_model]

    gen_config = {
        "temperature": temperature,
        "maxOutputTokens": max_tokens,
    }
    if is_json:
        gen_config["responseMimeType"] = "application/json"

    last_error = None
    for model_name in models_to_try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": gen_config,
        }

        try:
            with httpx.Client(timeout=30.0) as client:
                resp = client.post(url, json=payload)

            if resp.status_code == 200:
                data = resp.json()
                try:
                    text = data["candidates"][0]["content"]["parts"][0]["text"]
                    if model_name != primary_model:
                        _safe_print(f"[Gemini REST] Model '{primary_model}' lỗi, đã tự động chuyển sang fallback thành công: '{model_name}'")
                    return text
                except (KeyError, IndexError) as e:
                    raise ValueError(f"Gemini API: cấu trúc phản hồi không hợp lệ: {e}")

            err = resp.text[:200] if resp.text else "No body"
            _safe_print(f"[Gemini REST] ❌ Model {model_name} HTTP {resp.status_code}: {err}")
            last_error = f"HTTP {resp.status_code} ({model_name}): {err}"
            # Thử model tiếp theo nếu gặp lỗi model deprecated / quota / server error
            if resp.status_code in (404, 429, 500, 502, 503):
                continue
            else:
                break
        except httpx.TimeoutException:
            _safe_print(f"[Gemini REST] TIMEOUT với model {model_name}, thử model kế tiếp...")
            last_error = f"Timeout ({model_name})"
            continue
        except Exception as e:
            _safe_print(f"[Gemini REST] Lỗi khi gọi {model_name}: {e}")
            last_error = str(e)
            continue

    raise ValueError(f"Gemini API tất cả model đều lỗi. Lỗi cuối: {last_error}")


def _call_9router(prompt: str, temperature: float = 0.15, max_tokens: int = 2048, is_json: bool = False, fast: bool = False, timeout: float = 45.0) -> str:
    """
    Gọi 9Router OpenAI-compatible endpoint qua tài khoản Google Pro (moonshinemylove@gmail.com).
    """
    base_url = os.getenv("ROUTER_BASE_URL", "http://127.0.0.1:20128/v1").rstrip("/")
    router_url = f"{base_url}/chat/completions"
    router_key = os.getenv("ROUTER_API_KEY", "")
    if not router_key:
        raise ValueError("ROUTER_API_KEY chưa được cấu hình")

    primary_model = os.getenv("ROUTER_MODEL", "ag/gemini-3.8-flash-low")
    fallback_models = [
        primary_model,
        "ag/gemini-3.8-flash-low",
        "ag/gemini-3.8-flash",
        "ag/gemini-3.8-flash-medium",
    ]
    if fast:
        fallback_models = ["ag/gemini-3.8-flash-low", "ag/gemini-3.8-flash"] + fallback_models
    models_to_try = []
    for m in fallback_models:
        if m not in models_to_try:
            models_to_try.append(m)

    headers = {
        "Authorization": f"Bearer {router_key}",
        "Content-Type": "application/json",
    }

    last_error = None
    for model_name in models_to_try:
        payload = {
            "model": model_name,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": False,
        }
        if is_json:
            payload["response_format"] = {"type": "json_object"}

        try:
            with httpx.Client(timeout=timeout) as client:
                resp = client.post(router_url, json=payload, headers=headers)

            if resp.status_code == 200:
                raw_text = resp.text
                if raw_text.startswith("data:") or "text/event-stream" in resp.headers.get("content-type", ""):
                    collected = []
                    for line in raw_text.split("\n"):
                        line = line.strip()
                        if line.startswith("data:"):
                            part = line[5:].strip()
                            if part == "[DONE]":
                                break
                            try:
                                c = json.loads(part)
                                delta = c.get("choices", [{}])[0].get("delta", {})
                                if "content" in delta and delta["content"]:
                                    collected.append(delta["content"])
                            except Exception:
                                pass
                    full = "".join(collected).strip()
                    if full:
                        _safe_print(f"[9Router] OK Thành công với model '{model_name}' (Google Pro SSE)")
                        return full
                data = resp.json()
                text = data["choices"][0]["message"]["content"]
                _safe_print(f"[9Router] OK Thành công với model '{model_name}' (Google Pro)")
                return text

            err = resp.text[:200] if resp.text else "No body"
            _safe_print(f"[9Router] ❌ Model {model_name} HTTP {resp.status_code}: {err}")
            last_error = f"HTTP {resp.status_code} ({model_name}): {err}"
            if resp.status_code in (400, 404, 429, 500, 502, 503):
                continue
            else:
                break
        except httpx.TimeoutException:
            _safe_print(f"[9Router] TIMEOUT với model {model_name}, thử model tiếp theo...")
            last_error = f"Timeout ({model_name})"
            continue
        except Exception as e:
            _safe_print(f"[9Router] Lỗi khi gọi {model_name}: {e}")
            last_error = str(e)
            continue

    raise ValueError(f"9Router tất cả model đều lỗi. Lỗi cuối: {last_error}")


def _call_llm(prompt: str, temperature: float = 0.15, max_tokens: int = 2048, is_json: bool = False, fast: bool = False, timeout: float = 45.0) -> str:
    """
    Hàm gọi LLM hợp nhất:
    1. Ưu tiên 9Router (Google Pro account: moonshinemylove@gmail.com).
    2. Tự động fallback sang Google Gemini REST API trực tiếp nếu 9Router tắt hoặc lỗi.
    """
    use_9router = os.getenv("USE_9ROUTER", "true").lower() in ("true", "1", "yes")
    router_key = os.getenv("ROUTER_API_KEY", "")

    if use_9router and router_key:
        try:
            return _call_9router(prompt, temperature=temperature, max_tokens=max_tokens, is_json=is_json, fast=fast, timeout=timeout)
        except Exception as e:
            _safe_print(f"[LLM Router] 9Router không phản hồi ({e}), tự động chuyển sang Gemini REST API...")

    return _call_gemini_sync(prompt, temperature=temperature, max_tokens=max_tokens, is_json=is_json)


# ════════════════════════════════════════════════════════════════
#  1. NOTEBOOKLM: qua nlm CLI subprocess
# ════════════════════════════════════════════════════════════════

def _find_nlm_cmd() -> str | None:
    """Tìm đường dẫn lệnh nlm. Trả về None nếu không có."""
    candidates = [
        "nlm",
        os.path.expanduser("~/.local/bin/nlm"),
        "/usr/local/bin/nlm",
        os.path.join(sys.prefix, "Scripts", "nlm"),   # Windows venv
        os.path.join(sys.prefix, "bin", "nlm"),        # Unix venv
    ]
    for path in candidates:
        try:
            result = subprocess.run(
                [path, "--version"],
                capture_output=True,
                timeout=5,
            )
            if result.returncode == 0:
                return path
        except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
            continue
    return None


def _query_single_notebook(nlm_cmd: str, nb_id: str, question: str) -> str:
    """Query 1 sổ NotebookLM cụ thể."""
    try:
        nlm_env = os.environ.copy()
        nlm_env["PYTHONUTF8"] = "1"
        nlm_env["PYTHONIOENCODING"] = "utf-8"

        result = subprocess.run(
            [nlm_cmd, "query", "notebook", nb_id, question],
            capture_output=True,
            text=True,
            timeout=30,
            encoding="utf-8",
            errors="replace",
            env=nlm_env,
        )
        out = result.stdout.strip()
        err = result.stderr.strip()

        if result.returncode not in (0, 1):
            _safe_print(f"[NotebookLM CLI] Sổ {nb_id[:8]} FAIL returncode={result.returncode}, stderr={err[:150]}")
            return ""

        try:
            data = json.loads(out)
            value = data.get("value", {})
            if isinstance(value, dict):
                answer = value.get("answer", "") or value.get("text", "") or value.get("response", "")
            elif isinstance(value, str):
                answer = value
            else:
                answer = ""

            if answer and len(answer.strip()) > 20:
                clean_answer = re.sub(r'\[\d+\]', '', answer).strip()
                _safe_print(f"[NotebookLM CLI] Sổ {nb_id[:8]} OK (JSON) Got {len(clean_answer)} chars")
                return clean_answer
        except (json.JSONDecodeError, AttributeError):
            pass

        lines = [
            line for line in out.split("\n")
            if line.strip()
            and "Warning" not in line
            and "You are" not in line
            and "nlm" not in line.lower()
            and not line.strip().startswith("{")
            and not line.strip().startswith("[")
            and "conversation_id" not in line
            and "sources_used" not in line
        ]
        clean = "\n".join(lines).strip()

        auth_error_keywords = ["re-authenticate", "authenticate", "expired", "permission_denied", "not logged in", "login", "error"]
        if any(kw in clean.lower() for kw in auth_error_keywords) or len(clean) < 30:
            _safe_print(f"[NotebookLM CLI] Sổ {nb_id[:8]} Bỏ qua kết quả không hợp lệ/hết phiên: {clean[:60]}")
            return ""

        if clean:
            _safe_print(f"[NotebookLM CLI] Sổ {nb_id[:8]} OK (text) Got {len(clean)} chars")
            return clean
        return ""
    except subprocess.TimeoutExpired:
        _safe_print(f"[NotebookLM CLI] Sổ {nb_id[:8]} TIMEOUT after 30s.")
        return ""
    except Exception as e:
        _safe_print(f"[NotebookLM CLI] Sổ {nb_id[:8]} ERROR: {e}")
        return ""


def search_notebooklm_api(question: str) -> str:
    """
    Query lần lượt tất cả các NotebookLM đã cấu hình (Sổ 1, Sổ 2...).
    Tổng hợp kết quả từ tất cả các sổ tìm được câu trả lời.
    """
    nb_ids = _get_notebook_ids()
    if not nb_ids:
        return ""

    nlm_cmd = _find_nlm_cmd()
    if not nlm_cmd:
        _safe_print("[NotebookLM] nlm CLI khong tim thay trong PATH, bo qua.")
        return ""

    collected = []
    for idx, nb_id in enumerate(nb_ids, 1):
        ans = _query_single_notebook(nlm_cmd, nb_id, question)
        if ans:
            collected.append(f"=== NGUỒN SỔ NOTEBOOKLM {idx} (ID: {nb_id}) ===\n{ans}")

    if collected:
        return "\n\n".join(collected)
    return ""


# ════════════════════════════════════════════════════════════════
#  1.5. INTERNET SEARCH: Tra cứu thời gian thực kèm link nguồn
# ════════════════════════════════════════════════════════════════

def search_internet(query: str, max_results: int = 3) -> list[dict]:
    """
    Tra cứu thông tin PCCC trên Internet khi dữ liệu gốc (NotebookLM & ChromaDB) không có.
    Trích xuất tiêu đề, tóm tắt và đường dẫn URL chính xác.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    search_q = f"{query} PCCC luật quy định Việt Nam" if "pccc" not in query.lower() else f"{query} quy định"
    try:
        with httpx.Client(timeout=10.0, follow_redirects=True) as client:
            resp = client.post('https://html.duckduckgo.com/html/', data={'q': search_q}, headers=headers)
            if resp.status_code != 200:
                return []

            snippets = re.findall(r'<a class="result__snippet[^"]*"[^>]*>(.*?)</a>', resp.text, re.DOTALL)
            urls = re.findall(r'<a class="result__url"[^>]*href="([^"]*)"', resp.text)
            titles = re.findall(r'<a class="result__title"[^>]*>(.*?)</a>', resp.text, re.DOTALL)

            results = []
            for i in range(min(len(snippets), max_results)):
                raw_snippet = snippets[i] if i < len(snippets) else ""
                clean_snippet = re.sub(r'<[^>]+>', '', raw_snippet).strip()
                raw_url = urls[i] if i < len(urls) else ""
                if "uddg=" in raw_url:
                    actual_url = unquote(raw_url.split("uddg=")[1].split("&")[0])
                else:
                    actual_url = raw_url.strip()

                raw_title = titles[i] if i < len(titles) else ""
                clean_title = re.sub(r'<[^>]+>', '', raw_title).strip()

                if clean_snippet and actual_url and actual_url.startswith("http"):
                    results.append({
                        "title": unescape(clean_title) or "Cổng thông tin pháp luật",
                        "url": actual_url,
                        "snippet": unescape(clean_snippet)
                    })
            if results:
                _safe_print(f"[Internet Search] Tìm thấy {len(results)} kết quả tra cứu web cho: '{query[:40]}'")
            return results
    except Exception as e:
        _safe_print(f"[Internet Search] Lỗi tra cứu web: {e}")
        return []


# ════════════════════════════════════════════════════════════════
#  2. CHROMADB: Vector similarity search
# ════════════════════════════════════════════════════════════════

def _expand_queries(question: str, history_text: str = "") -> list:
    """Nhờ AI viết lại câu hỏi thành vài truy vấn tìm kiếm bằng thuật ngữ pháp lý chính xác (giải quyết cả đại từ theo lịch sử)."""
    prompt = f"""Bạn là chuyên viên tra cứu văn bản pháp luật PCCC. Hãy viết lại câu hỏi của người dân thành tối đa 3 truy vấn tìm kiếm ngắn gọn (5 đến 12 từ), dùng đúng thuật ngữ trong văn bản pháp luật (tên thủ tục, đối tượng, số hiệu nghị định, thông tư nếu biết), mỗi truy vấn nhìn từ một góc khác nhau. Nếu câu hỏi dùng đại từ hay hỏi nối tiếp, hãy thay bằng nội dung cụ thể dựa vào lịch sử.

LỊCH SỬ HỘI THOẠI: {history_text or '(không có)'}
CÂU HỎI: {question}

Trả về DUY NHẤT JSON: {{"queries": ["truy vấn 1", "truy vấn 2", "truy vấn 3"]}}"""
    try:
        raw = _call_llm(prompt, temperature=0.1, max_tokens=300, is_json=True, fast=True, timeout=14.0)
        data = _extract_json_block(raw) or {}
        qs = [q.strip() for q in (data.get("queries") or []) if isinstance(q, str) and q.strip()]
        return qs[:3]
    except Exception as e:
        _safe_print(f"[expand_queries] {e}")
        return []


def search_kho(question: str, history_text: str = "") -> str:
    """Tra cứu kho tài liệu: câu hỏi gốc cộng các cách diễn đạt do AI mở rộng, gộp kết quả, lấy tối đa 6 đoạn."""
    from utils import local_rag
    try:
        first = local_rag.search_multi([question], k=6)
        raw_top = local_rag.search(question, k=1)
        weak = (not raw_top) or raw_top[0][2] < 22 or bool(history_text.strip())
        queries = [question] + (_expand_queries(question, history_text) if weak else [])
        hits = local_rag.search_multi(queries, k=6) if len(queries) > 1 else first
        if hits:
            _safe_print(f"[RAG cục bộ] {len(queries)} truy vấn, {len(hits)} đoạn")
            return local_rag.format_hits(hits)
    except Exception as e:
        _safe_print(f"[search_kho] {e}")
    return search_chromadb(question)


def search_chromadb(question: str) -> str:
    """Tra cứu kho tài liệu nội bộ (RAG). Trả về context string hoặc ''.

    Ưu tiên tra cứu cục bộ BM25 trên thư mục data_docs (utils/local_rag.py): không cần khóa Gemini, không gọi dịch vụ ngoài.
    Chỉ khi không tìm được gì và có khóa Gemini mới thử thêm vector ChromaDB như trước.
    """
    from utils.local_rag import search_context
    local_ctx = search_context(question, k=4)
    if local_ctx:
        _safe_print("[RAG cục bộ] OK tìm thấy tài liệu liên quan trong kho")
        return local_ctx

    if not os.path.exists(CHROMA_DB_DIR):
        _safe_print(f"[ChromaDB] Dir not found: {CHROMA_DB_DIR}")
        return ""

    api_key = os.getenv("GEMINI_API_KEY") or GEMINI_API_KEY
    if not api_key:
        return ""

    try:
        # Import lazy để tránh lỗi khi chromadb/langchain chưa cài
        from langchain_community.vectorstores import Chroma
        from langchain_google_genai import GoogleGenerativeAIEmbeddings

        embeddings = GoogleGenerativeAIEmbeddings(
            model=os.getenv("GEMINI_EMBED_MODEL", GEMINI_EMBED_MODEL),
            google_api_key=api_key,
        )
        vectorstore = Chroma(
            persist_directory=CHROMA_DB_DIR,
            embedding_function=embeddings,
        )
        docs = vectorstore.similarity_search(question, k=4)
        if docs:
            context = "\n\n".join([f"[Tai lieu noi bo]:\n{d.page_content}" for d in docs])
            _safe_print(f"[ChromaDB] OK Found {len(docs)} chunks")
            return context
    except Exception as e:
        _safe_print(f"[ChromaDB] ERROR: {e}")

    return ""


# ════════════════════════════════════════════════════════════════
#  1.6. CLEAN FORMATTING: Loại bỏ ký tự markdown thừa (###, **, ---)
# ════════════════════════════════════════════════════════════════

def _clean_chat_formatting(text: str) -> str:
    """Chuẩn hóa câu trả lời: giữ các ký hiệu trình bày (>>, ##, !!, **, bảng, {{căn cứ}}), bỏ ký tự thừa, thống nhất xưng hô Chi."""
    from utils.chat_format import clean_reply
    return clean_reply(text)


# ════════════════════════════════════════════════════════════════
#  3. GEMINI GROUNDED: Fallback dùng kiến thức pháp luật
# ════════════════════════════════════════════════════════════════

def search_notebooklm_gemini_grounded(question: str) -> str:
    """
    Fallback: Dùng Gemini REST API với context pháp luật hiện hành.
    Trả về câu trả lời từ Gemini hoặc '' nếu lỗi.
    """
    if not (os.getenv("ROUTER_API_KEY") or os.getenv("GEMINI_API_KEY") or GEMINI_API_KEY):
        return ""

    legal_context = "\n".join(f"- {ref}" for ref in CURRENT_LEGAL_REFS)

    grounding_prompt = f"""Câu hỏi: {question}

Trả lời dựa trên các văn bản pháp luật PCCC HIỆN HÀNH sau đây (2024-2026):
{CORE_LEGAL_PRINCIPLES_2026}
{legal_context}

QUY TẮC BẮT BUỘC:
- Đi thẳng vào quy định mới nhất hiện hành (Nghị quyết 66.18/2026/NQ-CP, Nghị định 347/2026/NĐ-CP, Luật 55/2024/QH15).
- Nghiệm thu PCCC: ĐÃ BÃI BỎ thủ tục nộp hồ sơ xin nghiệm thu tại cơ quan nhà nước; chủ đầu tư tự tổ chức nghiệm thu với nhà thầu và khai báo CSDL PCCC.
- Không đưa quy định cũ lan man, chỉ đưa tên văn bản gần nhất trong ngoặc đơn nếu thật sự cần thiết.
- TUYỆT ĐỐI KHÔNG dùng ký tự markdown gây rối mắt: KHÔNG dùng ###, KHÔNG dùng **.
- Cung cấp câu trả lời ngắn gọn, rành mạch (200-350 từ)."""

    try:
        content = _call_llm(grounding_prompt, temperature=0.1, max_tokens=1024)
        _safe_print(f"[Gemini Grounded] OK Got {len(content)} chars")
        return _clean_chat_formatting(content)
    except Exception as e:
        _safe_print(f"[Gemini Grounded] ERROR: {e}")
        return ""


# ════════════════════════════════════════════════════════════════
#  4. MAIN FUNCTION: ask_ai_chi
# ════════════════════════════════════════════════════════════════



def ask_ai_chi(question: str, history_text: str = "", context: str = "") -> dict:
    """
    Trợ lý Chi: RAG Pipeline 2 lớp (tối ưu tốc độ < 20s):
    Lớp 1: Kho tài liệu nội bộ BM25 (local_rag) → ưu tiên cao nhất
    Lớp 2: Tra cứu Internet thời gian thực (khi kho không có hoặc hỏi về văn bản mới)
    Gọi LLM 1 lần duy nhất (không thẩm định lần 2 riêng biệt).
    """
    try:
        source_type = "general"
        use_router = os.getenv("USE_9ROUTER", "true").lower() in ("true", "1", "yes")
        router_key = os.getenv("ROUTER_API_KEY", "")

        # ── Lớp 1: Kho tài liệu nội bộ BM25 ─────────────────────────
        docs_context = ""
        docs_context = search_kho(question, history_text)
        if docs_context:
            source_type = "docs"

        # ── Lớp 2: Tra cứu Internet ──────────────────────────────────
        # Kích hoạt khi: kho không có kết quả, HOẶC câu hỏi về văn bản/thủ tục mới
        internet_context = ""
        internet_refs = []
        need_web_search = False

        if not docs_context:
            need_web_search = True
        else:
            combined = docs_context.lower()
            doc_codes = re.findall(r'\b(?:\d{2,3}(?:[/\.]\d+)?)\b', question)
            for code in doc_codes:
                if code not in ("2024", "2025", "2026") and code.lower() not in combined:
                    need_web_search = True
                    break
            reform_keywords = ["66.18", "347", "nghiệm thu", "bãi bỏ", "cải cách", "nộp ở đâu"]
            if any(kw in question.lower() for kw in reform_keywords) and "66.18" not in combined:
                need_web_search = True

        if need_web_search:
            _safe_print(f"[ask_ai_chi] Tra Internet cho: '{question[:40]}'")
            web_results = search_internet(question, max_results=3)
            if web_results:
                if not docs_context:
                    source_type = "web"
                web_blocks = []
                for item in web_results:
                    web_blocks.append(f"• Tiêu đề: {item['title']}\n  Đường dẫn: {item['url']}\n  Nội dung: {item['snippet']}")
                    internet_refs.append(f"{item['title']} ({item['url']})")
                internet_context = "\n\n".join(web_blocks)

        # ── Tổng hợp context ─────────────────────────────────────────
        doc_sections = []
        if docs_context:
            doc_sections.append(f"=== TÀI LIỆU NỘI BỘ (ưu tiên cao nhất) ===\n{docs_context}")
        if internet_context:
            doc_sections.append(f"=== TRA CỨU INTERNET (trích dẫn rõ nguồn và link) ===\n{internet_context}")

        doc_context = "\n\n".join(doc_sections) if doc_sections else (
            "(Không tìm thấy văn bản liên quan trực tiếp. Trả lời dựa trên kiến thức pháp luật PCCC 2024-2026.)"
        )

        # Lọc tài liệu cũ về phục hồi hoạt động (đã bãi bỏ theo NQ 66.18/2026)
        if re.search(r"phục hồi|phuc hoi", question, re.I):
            kept = [p for p in re.split(r"\n{2,}|\n(?=\s*[-•]|\d+[.)]\s)", doc_context)
                    if not re.search(r"phục hồi hoạt động|136/2020|50/2024", p, re.I)]
            doc_context = "\n\n".join(kept)

        # ── Build prompt ─────────────────────────────────────────────
        legal_refs_str = "\n".join(f"  - {r}" for r in CURRENT_LEGAL_REFS)

        template = f"""Bạn là Trợ lý ảo hỗ trợ giải đáp pháp luật và thủ tục hành chính (TTHC) về PCCC, chuyên gia tư vấn pháp luật PCCC và an toàn cháy nổ tại Việt Nam (Công an thành phố Bắc Ninh).

═══ CƠ SỞ PHÁP LÝ QUAN TRỌNG NĂM 2026 (ƯU TIÊN CAO NHẤT, VƯỢT TRÊN MỌI TÀI LIỆU CŨ) ═══
{CORE_LEGAL_PRINCIPLES_2026}

═══ TÀI LIỆU NỘI BỘ VÀ DỮ LIỆU TRA CỨU BỔ TRỢ ═══
{doc_context}
═══ HẾT TÀI LIỆU ═══

NGỮ CẢNH CƠ SỞ (nếu có): {context}

LỊCH SỬ HỘI THOẠI: {history_text}

CÂU HỎI CỦA NGƯỜI DÙNG: {question}

═══ CÁC VĂN BẢN HIỆN HÀNH ═══
{legal_refs_str}

═══ CÁC QUY TẮC BẮT BUỘC KHI TRẢ LỜI CỦA TRỢ LÝ ẢO (TUÂN THỦ 100%) ═══
0. CHUẨN MỰC HÀNH VĂN NGƯỜI THẬT (0% AI HUMAN WRITING):
   - Tuyệt đối CẤM sử dụng dấu gạch ngang dài (em dash). Luôn dùng dấu phẩy, dấu chấm, dấu hai chấm hoặc ngoặc đơn.
   - CẤM sáo ngữ robot: "Trong bối cảnh...", "Không thể phủ nhận rằng...", "Đóng vai trò vô cùng quan trọng...", "Mang lại lợi ích đáng kể...", "Tối ưu hóa", "Đột phá".
   - CẤM các câu mở đầu hoặc kết bài xã giao kiểu chatbot ("Hy vọng câu trả lời này hữu ích với bạn", "Nếu bạn cần thêm thông tin..."). Đi thẳng vào nội dung chuyên môn.
   - Trộn câu ngắn dài tự nhiên, hành văn dứt khoát, chuẩn xác của chuyên gia luật PCCC.

00. PHẠM VI TRẢ LỜI: Trợ lý ảo chỉ trả lời các câu hỏi thuộc lĩnh vực phòng cháy, chữa cháy, cứu nạn cứu hộ, an toàn cháy nổ và cách dùng Hệ thống FRAS-AI. Nếu câu hỏi không thuộc các lĩnh vực này (kể cả khi có nhắc từ khóa liên quan nhưng nội dung là chuyện khác), KHÔNG trả lời nội dung đó. Chỉ đáp ngắn gọn, nhã nhặn: câu hỏi nằm ngoài lĩnh vực Trợ lý ảo phụ trách, và mời người dùng đặt câu hỏi về PCCC. Không giải thích dài, không phê bình người hỏi.

1. ĐI THẲNG VÀO NỘI DUNG MỚI NHẤT HIỆN HÀNH (NĂM 2026):
   - Luôn hướng dẫn theo quy định mới nhất hiện hành (Nghị quyết số 66.18/2026/NQ-CP, Nghị định số 347/2026/NĐ-CP, Luật 55/2024/QH15...).
   - ĐẶC BIỆT VỀ NGHIỆM THU PCCC:
     + Nêu rõ ngay: Thủ tục hành chính nộp hồ sơ xin kiểm tra nghiệm thu tại cơ quan Công an hoặc cơ quan Xây dựng ĐÃ ĐƯỢC CHÍNH THỨC BÃI BỎ.
     + Chủ đầu tư KHÔNG PHẢI NỘP HỒ SƠ ĐỀ NGHỊ NGHIỆM THU ĐẾN CƠ QUAN NÀO NỮA.
     + Chủ đầu tư tự tổ chức nghiệm thu cùng các nhà thầu (tư vấn thiết kế, thi công, tư vấn giám sát) theo đúng hồ sơ thiết kế đã thẩm duyệt.
     + Chủ đầu tư lập hồ sơ nghiệm thu, tự chịu trách nhiệm pháp lý và thực hiện khai báo thông tin trên Hệ thống cơ sở dữ liệu về PCCC trước khi đưa công trình vào vận hành.
     + Cơ quan Công an chuyển sang kiểm tra định kỳ (hậu kiểm: 1 năm/lần với cơ sở rủi ro cao, 2 năm/lần với cơ sở còn lại).
   - ĐẶC BIỆT VỀ CHỨNG NHẬN HUẤN LUYỆN PCCC: Chứng nhận huấn luyện nghiệp vụ PCCC và CNCH (thẻ chứng nhận, giấy chứng nhận cấp sau mỗi khóa) ĐÃ BÃI BỎ theo Luật PCCC và CNCH số 55/2024/QH15 và Nghị định 105/2025/NĐ-CP. Không còn cấp giấy chứng nhận riêng theo từng khóa hay quy định thời hạn của chứng nhận. Khi người hỏi hỏi về thời hạn giá trị chứng nhận huấn luyện PCCC, PHẢI khẳng định ngay: Chứng nhận huấn luyện đã bãi bỏ; thay vào đó: "Huấn luyện nghiệp vụ phòng cháy, chữa cháy, cứu nạn, cứu hộ được thực hiện định kỳ 05 năm một lần; bồi dưỡng nghiệp vụ phòng cháy, chữa cháy, cứu nạn, cứu hộ được thực hiện định kỳ hằng năm theo Nghị định 105/2025/NĐ-CP".
   - ĐẶC BIỆT VỀ THỜI GIAN HUẤN LUYỆN PCCC: Khi người hỏi hỏi về thời gian huấn luyện PCCC là bao lâu, BẮT BUỘC liệt kê ĐẦY ĐỦ cả 6 nhóm đối tượng (Người đứng đầu cơ sở: 16-24h/8-12h; Đội PCCC cơ sở/chuyên ngành: 32-48h/16-24h; Người làm việc môi trường nguy hiểm: 16-24h/8-12h; Đội dân phòng, trưởng thôn: 16-24h/8-12h; Lái xe vận chuyển chất, hàng nguy hiểm: 16-24h/8-12h; Cá nhân làm nhiều nhiệm vụ: 24-32h/8-12h). TUYỆT ĐỐI KHÔNG được chỉ trả lời mỗi một nhóm "cá nhân làm nhiều nhiệm vụ" mà bỏ sót các nhóm còn lại.

2. TUYỆT ĐỐI KHÔNG ĐƯA QUY ĐỊNH CŨ LAN MAN:
   - KHÔNG lập riêng mục "Đối chiếu quy định cũ - mới".
   - KHÔNG liệt kê các luật cũ, nghị định cũ xa xưa (Luật 2001, Luật 2013, Nghị định 136/2020, Nghị định 50/2024...).
   - Quy định cũ chỉ được đưa ra văn bản gần nhất (nếu thật sự cần thiết để người hỏi không nhầm lẫn) và PHẢI ĐẶT TRONG DẤU NGOẶC ĐƠN THẬT NGẮN GỌN.

3. CÁCH TRÌNH BÀY (bộ hiển thị của hệ thống sẽ tô màu, kẻ khung theo các ký hiệu dưới đây, hãy dùng đúng):
   - Dòng bắt đầu bằng ">> " là KẾT LUẬN: 1 đến 2 câu trả lời thẳng vào câu hỏi, luôn đặt ở dòng đầu tiên.
   - Dòng bắt đầu bằng "## " là TIÊU ĐỀ MỤC (ví dụ: ## Việc cần làm, ## Điều kiện áp dụng, ## Lưu ý). Chỉ dùng 2 đến 4 mục, tên mục ngắn.
   - Dòng bắt đầu bằng "!! " là LƯU Ý QUAN TRỌNG hoặc CẢNH BÁO (rủi ro, hạn chót, điều dễ nhầm). Tối đa 2 dòng.
   - Các bước làm tuần tự: đánh số "1. ", "2. ", mỗi bước một dòng, bắt đầu bằng động từ.
   - Ý liệt kê ngang hàng: gạch đầu dòng "- ".
   - Từ khóa quan trọng (số liệu, thời hạn, tên thủ tục): bao bằng **hai dấu sao**. Chỉ bôi đậm những cụm thật cần chú ý, không bôi tràn lan.
   - So sánh nhiều phương án hoặc nhiều loại hình: dùng bảng với dòng tiêu đề, ví dụ "| Loại hình | Yêu cầu |" rồi "|---|---|" rồi các dòng "| ... | ... |".
   - Căn cứ pháp lý: viết trong hai dấu ngoặc nhọn kép, ví dụ {{{{Điều 5 Nghị định 105/2025/NĐ-CP}}}}, đặt ngay sau ý được căn cứ. CHỈ trích điều, khoản, văn bản có thật trong phần tài liệu ở trên; không bịa số điều.
   - Không dùng đường kẻ ngang (---) ngoài bảng, không dùng dấu gạch ngang dài, không dùng ### hay # ngoài tiêu đề "## ".
   - Câu hỏi đơn giản: trả lời gọn trong khoảng 80 đến 150 từ. Câu hỏi về thủ tục, quy trình: đủ bước nhưng không quá 500 từ.

3a. DIỄN GIẢI ĐẦY ĐỦ NỘI DUNG, KHÔNG CẮT BỎ:
   - Liệt kê ĐẦY ĐỦ tất cả các đối tượng, nhóm đối tượng, trường hợp có trong tài liệu.
   - Với câu hỏi về huấn luyện PCCC: liệt kê ĐẦY ĐỦ từng nhóm đối tượng và thời lượng tương ứng (không được bỏ nhóm nào).
   - Mỗi bước trong danh sách đánh số phải viết thành 2 đến 4 câu hoặc có các ý nhỏ, nêu rõ: AI làm, LÀM GÌ cụ thể, THỜI HẠN nếu có, và căn cứ.
   - TUYỆT ĐỐI KHÔNG rút gọn hoặc bỏ bớt đối tượng, thời lượng, bước nào có trong tài liệu.

3b. KHI THIẾU THÔNG TIN: nếu đáp án phụ thuộc loại hình, quy mô mà người hỏi chưa nói, hãy trả lời trước cho trường hợp phổ biến, rồi cuối bài thêm một dòng "!! Để có thể tư vấn chính xác hơn, bạn cho biết thêm: ..." (tối đa 2 ý cần hỏi lại).

3c. TỰ KIỂM TRA TRƯỚC KHI TRẢ LỜI: mọi con số, thời hạn, điều khoản phải có trong tài liệu ở trên hoặc trong phần CƠ SỞ PHÁP LÝ 2026. Nếu không chắc, nói rõ chưa có căn cứ trong tài liệu và mời liên hệ cán bộ Cảnh sát PCCC và CNCH.

4. PHONG CÁCH VÀ XƯNG HÔ:
   - Trợ lý ảo PCCC của Công an thành phố Bắc Ninh. Xưng là "Tôi" hoặc "Trợ lý ảo", gọi người hỏi là "bạn". TUYỆT ĐỐI KHÔNG tự xưng là "Chi" hay bất kỳ tên riêng nào khác.
   - Giọng ân cần, mềm mỏng, rành mạch của người cán bộ hướng dẫn. Không quy lỗi, không dạy đời.
   - Không mở đầu kiểu xã giao ("Chào bạn", "Cảm ơn bạn đã hỏi"), đi thẳng vào kết luận.

TRẢ VỀ JSON THUẦN (không dùng ```json):
{{{{
    "reply": "câu trả lời theo đúng cách trình bày ở mục 3, xưng Tôi hoặc Trợ lý ảo (tuyệt đối không xưng Chi), tập trung quy định mới 2026, ĐẦY ĐỦ nội dung không cắt bỏ",
    "source_type": "{source_type}",
    "suggestions": ["gợi ý câu hỏi tiếp theo 1", "gợi ý 2", "gợi ý 3"],
    "references": ["văn bản pháp lý hiện hành hoặc link nguồn internet"]
}}}}"""

        # ── Gọi LLM (9Router Google Pro hoặc Gemini REST API) ───────
        router_model = os.getenv("ROUTER_MODEL", "ag/gemini-3.8-flash-high")
        current_model = router_model if use_router and router_key else os.getenv("GEMINI_MODEL", "gemini-3.5-flash")
        _safe_print(f"[ask_ai_chi] Gọi LLM (ưu tiên {current_model})...")
        # Dùng mô hình nhanh (không phải bản "high" suy nghĩ chậm) để đảm bảo < 20s
        content = _call_llm(template, temperature=0.15, max_tokens=3000, is_json=True, fast=True, timeout=30.0)
        _safe_print(f"[ask_ai_chi] OK Got {len(content)} chars")

        # ── Parse JSON từ phản hồi ───────────────────────────────────
        result = _extract_json_block(content)
        if result and isinstance(result, dict) and "reply" in result:
            result["reply"] = _clean_chat_formatting(result["reply"])
            result["source_type"] = source_type
            if not isinstance(result.get("suggestions"), list):
                result["suggestions"] = []
            if not isinstance(result.get("references"), list):
                result["references"] = list(CURRENT_LEGAL_REFS[:3])
            if internet_refs:
                for ref in internet_refs:
                    if ref not in result["references"]:
                        result["references"].append(ref)
            result["_doc_context"] = doc_context
            return result

        # Fallback nếu JSON parse lỗi
        fallback_refs = list(CURRENT_LEGAL_REFS[:3])
        if internet_refs:
            fallback_refs.extend(internet_refs)

        raw_reply = content.strip()
        if raw_reply.startswith("{") and '"reply"' in raw_reply:
            m = re.search(r'"reply"\s*:\s*"((?:[^"\\]|\\.)*)', raw_reply)
            if m:
                raw_reply = m.group(1).replace('\\"', '"').replace('\\n', '\n')

        return {
            "reply": _clean_chat_formatting(raw_reply),
            "source_type": source_type,
            "suggestions": ["Quy định về nghiệm thu PCCC mới nhất?", "Khai báo cơ sở dữ liệu PCCC thế nào?", "Trách nhiệm của chủ đầu tư về PCCC?"],
            "references": fallback_refs,
        }

    except Exception as e:
        err_msg = str(e)
        _safe_print(f"[ask_ai_chi] ERROR: {err_msg}")

        # Khong dump tho context khi LLM loi de tranh vo format va vo loi font
        pass

        try:
            from routers.ai_analysis import _chat_fallback
            fb = _chat_fallback(question)
            if isinstance(fb, dict) and "reply" in fb:
                fb["reply"] = _clean_chat_formatting(fb["reply"])
            return fb
        except Exception:
            return {
                "reply": "Hệ thống đang tạm thời gián đoạn kết nối AI. Vui lòng thử lại sau giây lát hoặc liên hệ cán bộ quản lý PCCC.",
                "source_type": "error",
                "suggestions": [],
                "references": [],
            }
