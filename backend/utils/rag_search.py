"""
RAG Search — Trợ lý Chi
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
from dotenv import load_dotenv

load_dotenv()


def _safe_print(msg: str) -> None:
    """In ra console, bỏ qua ký tự không encode được (Windows cp1252)."""
    try:
        print(msg)
    except UnicodeEncodeError:
        print(msg.encode("ascii", errors="replace").decode("ascii"))


# ─── Hằng số luật lỗi thời để nhắc Gemini tránh ───────────────────────────
OBSOLETE_LAWS = [
    "Luật PCCC 2001", "Luật PCCC 2013", "Luật sửa đổi PCCC 2013",
    "Nghị định 136/2020/NĐ-CP", "Nghị định 79/2014/NĐ-CP",
    "Thông tư 149/2020/TT-BCA", "Thông tư 66/2014/TT-BCA",
    "TCVN 3890:2009",
]

CURRENT_LEGAL_REFS = [
    "Luật Phòng cháy, chữa cháy và Cứu nạn, cứu hộ số 55/2024/QH15",
    "Nghị định 105/2025/NĐ-CP ngày 15/5/2025",
    "Nghị định 106/2025/NĐ-CP",
    "Nghị định 189/2025/NĐ-CP",
    "Nghị định 190/2025/NĐ-CP",
    "QCVN 06:2022/BXD kèm Sửa đổi 1:2023",
    "QCVN 10:2025/BCA",
    "QCVN 25:2025/BCT",
    "QCVN 25:2025/BKHCN",
]

CHROMA_DB_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "chroma_db")
NOTEBOOKLM_NOTEBOOK_ID = os.getenv("NOTEBOOKLM_PROJECT_ID", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Model được pin cứng — KHÔNG để LangChain tự chọn
# gemini-2.0-flash-lite: model mới nhất hoạt động với API free tier
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash-lite")
GEMINI_EMBED_MODEL = os.getenv("GEMINI_EMBED_MODEL", "models/gemini-embedding-001")

GEMINI_ENDPOINT = (
    f"https://generativelanguage.googleapis.com/v1beta/models/"
    f"{GEMINI_MODEL}:generateContent"
)


# ════════════════════════════════════════════════════════════════
#  HELPER: Gọi Gemini REST API trực tiếp (không dùng LangChain)
# ════════════════════════════════════════════════════════════════

def _call_gemini_sync(prompt: str, temperature: float = 0.15, max_tokens: int = 2048) -> str:
    """
    Gọi Gemini API qua httpx đồng bộ.
    Trả về text nội dung hoặc raise Exception nếu lỗi.
    """
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY chưa được cấu hình")

    url = f"{GEMINI_ENDPOINT}?key={GEMINI_API_KEY}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": temperature,
            "maxOutputTokens": max_tokens,
        },
    }

    with httpx.Client(timeout=30.0) as client:
        resp = client.post(url, json=payload)

    if resp.status_code != 200:
        err = resp.text[:300] if resp.text else "No body"
        print(f"[Gemini REST] ❌ HTTP {resp.status_code}: {err}")
        raise ValueError(f"Gemini API lỗi HTTP {resp.status_code}: {err}")

    data = resp.json()
    try:
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError) as e:
        raise ValueError(f"Gemini API: cấu trúc phản hồi không hợp lệ — {e}")


# ════════════════════════════════════════════════════════════════
#  1. NOTEBOOKLM — qua nlm CLI subprocess
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


def search_notebooklm_api(question: str) -> str:
    """
    Query NotebookLM qua nlm CLI.
    Trả về string kết quả hoặc "" nếu thất bại/không có CLI.
    """
    if not NOTEBOOKLM_NOTEBOOK_ID:
        print("[NotebookLM] NOTEBOOKLM_PROJECT_ID chưa được cấu hình, bỏ qua.")
        return ""

    nlm_cmd = _find_nlm_cmd()
    if not nlm_cmd:
        _safe_print("[NotebookLM] nlm CLI khong tim thay trong PATH, bo qua.")
        return ""

    try:
        # Thiết lập env để nlm dùng UTF-8 trên Windows
        nlm_env = os.environ.copy()
        nlm_env["PYTHONUTF8"] = "1"
        nlm_env["PYTHONIOENCODING"] = "utf-8"

        result = subprocess.run(
            [nlm_cmd, "query", "notebook", NOTEBOOKLM_NOTEBOOK_ID, question],
            capture_output=True,
            text=True,
            timeout=30,
            encoding="utf-8",
            errors="replace",
            env=nlm_env,
        )
        out = result.stdout.strip()
        err = result.stderr.strip()

        # nlm trên Windows có thể exit code 1 do lỗi Unicode trong Rich console
        # nhưng JSON output vẫn hợp lệ trong stdout
        if result.returncode not in (0, 1):
            _safe_print(f"[NotebookLM CLI] FAIL returncode={result.returncode}, stderr={err[:200]}")
            return ""

        # Thử parse JSON từ output của nlm — format: {"value": {"answer": "..."}}
        try:
            data = json.loads(out)
            # nlm trả về {"value": {"answer": "...", "citations": {...}}}
            value = data.get("value", {})
            if isinstance(value, dict):
                answer = value.get("answer", "") or value.get("text", "") or value.get("response", "")
            elif isinstance(value, str):
                answer = value
            else:
                answer = ""

            if answer and len(answer.strip()) > 20:
                # Loại bỏ citation markers như [1], [2]
                import re
                clean_answer = re.sub(r'\[\d+\]', '', answer).strip()
                _safe_print(f"[NotebookLM CLI] OK (JSON) Got {len(clean_answer)} chars")
                return clean_answer
        except (json.JSONDecodeError, AttributeError):
            pass  # Không phải JSON, thử parse text

        # Parse text thô — lọc các dòng metadata/warning của nlm
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

        if clean:
            _safe_print(f"[NotebookLM CLI] OK (text) Got {len(clean)} chars")
            return clean
        else:
            _safe_print(f"[NotebookLM CLI] WARN Empty response. Raw len: {len(out)}")
            return ""

    except subprocess.TimeoutExpired:
        _safe_print("[NotebookLM CLI] TIMEOUT after 30s.")
        return ""
    except Exception as e:
        _safe_print(f"[NotebookLM CLI] ERROR: {e}")
        return ""


# ════════════════════════════════════════════════════════════════
#  2. CHROMADB — Vector similarity search
# ════════════════════════════════════════════════════════════════

def search_chromadb(question: str) -> str:
    """Tìm kiếm ChromaDB local. Trả về context string hoặc ''."""
    if not os.path.exists(CHROMA_DB_DIR):
        _safe_print(f"[ChromaDB] Dir not found: {CHROMA_DB_DIR}")
        return ""

    if not GEMINI_API_KEY:
        return ""

    try:
        # Import lazy để tránh lỗi khi chromadb/langchain chưa cài
        from langchain_community.vectorstores import Chroma
        from langchain_google_genai import GoogleGenerativeAIEmbeddings

        embeddings = GoogleGenerativeAIEmbeddings(
            model=GEMINI_EMBED_MODEL,
            google_api_key=GEMINI_API_KEY,
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
#  3. GEMINI GROUNDED — Fallback dùng kiến thức pháp luật
# ════════════════════════════════════════════════════════════════

def search_notebooklm_gemini_grounded(question: str) -> str:
    """
    Fallback: Dùng Gemini REST API với context pháp luật hiện hành.
    Trả về câu trả lời từ Gemini hoặc '' nếu lỗi.
    """
    if not GEMINI_API_KEY:
        return ""

    legal_context = "\n".join(f"- {ref}" for ref in CURRENT_LEGAL_REFS)
    obsolete_context = "\n".join(f"- {law}" for law in OBSOLETE_LAWS)

    grounding_prompt = f"""Câu hỏi: {question}

Trả lời dựa trên các văn bản pháp luật PCCC HIỆN HÀNH sau đây (2024-2025):
{legal_context}

TUYỆT ĐỐI KHÔNG trích dẫn các văn bản đã HẾT HIỆU LỰC sau:
{obsolete_context}

Cung cấp câu trả lời ngắn gọn, chính xác (200-400 từ), trích dẫn cụ thể điều khoản."""

    try:
        content = _call_gemini_sync(grounding_prompt, temperature=0.1, max_tokens=1024)
        _safe_print(f"[Gemini Grounded] OK Got {len(content)} chars")
        return content
    except Exception as e:
        _safe_print(f"[Gemini Grounded] ERROR: {e}")
        return ""


# ════════════════════════════════════════════════════════════════
#  4. MAIN FUNCTION — ask_ai_chi
# ════════════════════════════════════════════════════════════════

def ask_ai_chi(question: str, history_text: str = "", context: str = "") -> dict:
    """
    Trợ lý Chi — RAG Pipeline:
    Priority: NotebookLM CLI → ChromaDB → Gemini general (có ràng buộc luật mới)

    Gọi Gemini REST API trực tiếp (httpx) — KHÔNG dùng LangChain ChatGoogleGenerativeAI
    để tránh lỗi model-override PERMISSION_DENIED với gemini-2.5-flash.
    """
    if not GEMINI_API_KEY:
        return {
            "reply": "Xin lỗi, hệ thống AI Chi chưa được cấu hình GEMINI_API_KEY.",
            "source_type": "error",
            "suggestions": [],
            "references": [],
        }

    try:
        source_type = "general"

        # ── Bước 1: NotebookLM (ưu tiên cao nhất) ──────────────────
        notebook_context = ""
        if NOTEBOOKLM_NOTEBOOK_ID:
            notebook_context = search_notebooklm_api(question)
            if notebook_context:
                source_type = "notebooklm"

        # ── Bước 2: ChromaDB ────────────────────────────────────────
        chroma_context = ""
        if not notebook_context:
            chroma_context = search_chromadb(question)
            if chroma_context:
                source_type = "docs"

        # ── Bước 3: Gemini Grounded (nếu cả hai đều rỗng) ──────────
        grounded_context = ""
        if not notebook_context and not chroma_context:
            grounded_context = search_notebooklm_gemini_grounded(question)
            source_type = "general"

        # ── Tổng hợp context ────────────────────────────────────────
        doc_sections = []
        if notebook_context:
            doc_sections.append(f"=== NGUỒN NOTEBOOKLM (ưu tiên) ===\n{notebook_context}")
        if chroma_context:
            doc_sections.append(f"=== NGUỒN TÀI LIỆU NỘI BỘ ===\n{chroma_context}")
        if grounded_context:
            doc_sections.append(f"=== PHÂN TÍCH PHÁP LÝ ===\n{grounded_context}")

        doc_context = "\n\n".join(doc_sections) if doc_sections else (
            "(Không có tài liệu nào phù hợp trong cơ sở dữ liệu. "
            "Trả lời dựa trên kiến thức chuyên môn PCCC 2024-2025.)"
        )

        # ── Build prompt cho Gemini ──────────────────────────────────
        legal_refs_str = "\n".join(f"  ✅ {r}" for r in CURRENT_LEGAL_REFS)
        obsolete_str = "\n".join(f"  ❌ {l}" for l in OBSOLETE_LAWS)

        template = f"""Bạn là Trợ lý ảo AI Chi — chuyên gia tư vấn pháp luật PCCC và an toàn cháy nổ tại Việt Nam (Công an tỉnh Bắc Ninh).

═══ CƠ SỞ DỮ LIỆU PHÁP CHẾ ═══
{doc_context}
═══ HẾT CƠ SỞ DỮ LIỆU ═══

NGỮ CẢNH CƠ SỞ (nếu có): {context}

LỊCH SỬ HỘI THOẠI: {history_text}

CÂU HỎI: {question}

═══ LUẬT HIỆN HÀNH 2024-2025 (CHỈ ĐƯỢC DÙNG CÁC LUẬT NÀY) ═══
{legal_refs_str}

═══ LUẬT ĐÃ HẾT HIỆU LỰC (TUYỆT ĐỐI KHÔNG TRÍCH DẪN) ═══
{obsolete_str}

NHIỆM VỤ:
1. ĐỌC KỸ CƠ SỞ DỮ LIỆU PHÁP CHẾ — ưu tiên dùng thông tin từ NotebookLM nếu có.
2. CHỈ TRÍCH DẪN các luật HIỆN HÀNH 2024-2025. KHÔNG BAO GIỜ dùng NĐ 136/2020, TT 149/2020, hay luật trước 2024.
3. Nếu tài liệu không có thông tin → dùng kiến thức chuyên môn PCCC 2024-2025 của bạn, KHÔNG nói "tôi không biết".
4. Xưng là "Chi" hoặc "Tôi". Trả lời rõ ràng, định dạng Markdown.
5. Nếu dùng dữ liệu từ CƠ SỞ DỮ LIỆU, trích dẫn [nguồn].

TRẢ VỀ JSON THUẦN (không dùng ```json):
{{
    "reply": "câu trả lời markdown chi tiết",
    "source_type": "{source_type}",
    "suggestions": ["gợi ý câu hỏi liên quan 1", "gợi ý 2", "gợi ý 3"],
    "references": ["văn bản pháp lý trích dẫn HIỆN HÀNH — chỉ 2024-2025"]
}}"""

        # ── Gọi Gemini REST API trực tiếp ───────────────────────────
        _safe_print(f"[ask_ai_chi] Gọi Gemini {GEMINI_MODEL} REST API...")
        content = _call_gemini_sync(template, temperature=0.15, max_tokens=2048)
        _safe_print(f"[ask_ai_chi] OK Got {len(content)} chars")

        # ── Parse JSON từ phản hồi ───────────────────────────────────
        # Loại bỏ markdown fence nếu có
        stripped = content.strip()
        if "```json" in stripped:
            stripped = stripped.split("```json")[1].split("```")[0].strip()
        elif "```" in stripped:
            stripped = stripped.split("```")[1].split("```")[0].strip()

        try:
            result = json.loads(stripped)
            result["source_type"] = source_type  # Đảm bảo source_type đúng
            return result
        except json.JSONDecodeError:
            # Gemini trả về text thô (không JSON) — vẫn hữu ích
            return {
                "reply": stripped,
                "source_type": source_type,
                "suggestions": [],
                "references": list(CURRENT_LEGAL_REFS[:3]),
            }

    except Exception as e:
        err_msg = str(e)
        _safe_print(f"[ask_ai_chi] ERROR: {err_msg}")
        return {
            "reply": (
                f"Hệ thống đang tạm thời gián đoạn (lỗi: {err_msg[:120]}). "
                "Vui lòng thử lại sau."
            ),
            "source_type": "error",
            "suggestions": [],
            "references": [],
        }
