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
                    raise ValueError(f"Gemini API: cấu trúc phản hồi không hợp lệ — {e}")

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

        # Loại bỏ các thông báo lỗi xác thực hoặc chuỗi quá ngắn
        auth_error_keywords = ["re-authenticate", "authenticate", "expired", "permission_denied", "not logged in", "login", "error"]
        if any(kw in clean.lower() for kw in auth_error_keywords) or len(clean) < 30:
            _safe_print(f"[NotebookLM CLI] Bỏ qua kết quả không hợp lệ hoặc lỗi phiên: {clean[:60]}")
            return ""

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
#  3. GEMINI GROUNDED — Fallback dùng kiến thức pháp luật
# ════════════════════════════════════════════════════════════════

def search_notebooklm_gemini_grounded(question: str) -> str:
    """
    Fallback: Dùng Gemini REST API với context pháp luật hiện hành.
    Trả về câu trả lời từ Gemini hoặc '' nếu lỗi.
    """
    api_key = os.getenv("GEMINI_API_KEY") or GEMINI_API_KEY
    if not api_key:
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
    để tránh lỗi model-override PERMISSION_DENIED.
    """
    try:
        source_type = "general"
        api_key = os.getenv("GEMINI_API_KEY") or GEMINI_API_KEY

        # ── Bước 1: NotebookLM (ưu tiên cao nhất nếu có CLI cấu hình) ──
        notebook_context = ""
        if NOTEBOOKLM_NOTEBOOK_ID:
            notebook_context = search_notebooklm_api(question)
            if notebook_context and len(notebook_context) > 30 and "authenticate" not in notebook_context.lower():
                source_type = "notebooklm"
            else:
                notebook_context = ""

        # ── Bước 2: ChromaDB ────────────────────────────────────────
        chroma_context = ""
        if not notebook_context:
            chroma_context = search_chromadb(question)
            if chroma_context:
                source_type = "docs"

        # Nếu không có API Key Gemini, ưu tiên dữ liệu nội bộ/NotebookLM
        if not api_key:
            if notebook_context:
                return {
                    "reply": f"{notebook_context}\n\n*(Hệ thống đang hiển thị thông tin trực tiếp từ NotebookLM)*",
                    "source_type": "notebooklm",
                    "suggestions": ["Quy định về bình chữa cháy?", "Khi xảy ra cháy cần làm gì?"],
                    "references": list(CURRENT_LEGAL_REFS[:2])
                }
            if chroma_context:
                return {
                    "reply": f"Thông tin quy chuẩn PCCC trích xuất:\n\n{chroma_context[:1000]}",
                    "source_type": "docs",
                    "suggestions": ["Quy định về bình chữa cháy?", "Khi xảy ra cháy cần làm gì?"],
                    "references": list(CURRENT_LEGAL_REFS[:2])
                }
            from routers.ai_analysis import _chat_fallback
            return _chat_fallback(question)

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
        current_model = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")
        _safe_print(f"[ask_ai_chi] Gọi Gemini API (ưu tiên {current_model})...")
        content = _call_gemini_sync(template, temperature=0.15, max_tokens=2048, is_json=True)
        _safe_print(f"[ask_ai_chi] OK Got {len(content)} chars")

        # ── Parse JSON từ phản hồi ───────────────────────────────────
        result = _extract_json_block(content)
        if result and isinstance(result, dict) and "reply" in result:
            result["source_type"] = source_type
            if not isinstance(result.get("suggestions"), list):
                result["suggestions"] = []
            if not isinstance(result.get("references"), list):
                result["references"] = list(CURRENT_LEGAL_REFS[:3])
            return result

        # Fallback nếu kết quả text không parse được dạng JSON hoàn chỉnh
        return {
            "reply": content.strip(),
            "source_type": source_type,
            "suggestions": ["Quy định về bình chữa cháy?", "Khi xảy ra cháy cần làm gì?", "Luật PCCC 55/2024 có gì mới?"],
            "references": list(CURRENT_LEGAL_REFS[:3]),
        }

    except Exception as e:
        err_msg = str(e)
        _safe_print(f"[ask_ai_chi] ERROR: {err_msg}")

        # Nếu có dữ liệu NotebookLM hợp lệ thì trả về
        if 'notebook_context' in locals() and notebook_context and len(notebook_context) > 30 and "authenticate" not in notebook_context.lower():
            return {
                "reply": f"{notebook_context}\n\n*(Lưu ý: Hệ thống đang trích xuất câu trả lời trực tiếp từ NotebookLM)*",
                "source_type": "notebooklm_direct",
                "suggestions": [],
                "references": list(CURRENT_LEGAL_REFS[:2])
            }

        # Nếu có ChromaDB context thì phản hồi từ dữ liệu pháp lý nội bộ
        if 'chroma_context' in locals() and chroma_context and len(chroma_context) > 30:
            return {
                "reply": f"Dựa trên cơ sở dữ liệu pháp luật PCCC đã đối soát:\n\n{chroma_context[:1200]}\n\n*(Lưu ý: Hệ thống đang phản hồi từ kho văn bản quy chuẩn nội bộ)*",
                "source_type": "docs",
                "suggestions": ["Quy định về bình chữa cháy?", "Khi xảy ra cháy cần làm gì?", "Luật PCCC 55/2024 có gì mới?"],
                "references": list(CURRENT_LEGAL_REFS[:2])
            }

        # Fallback về bộ kịch bản kiến thức PCCC tiêu chuẩn
        try:
            from routers.ai_analysis import _chat_fallback
            fb = _chat_fallback(question)
            return fb
        except Exception:
            return {
                "reply": (
                    "Hệ thống đang tạm thời gián đoạn kết nối AI. Vui lòng thử lại sau giây lát hoặc liên hệ cán bộ quản lý PCCC."
                ),
                "source_type": "error",
                "suggestions": [],
                "references": [],
            }
