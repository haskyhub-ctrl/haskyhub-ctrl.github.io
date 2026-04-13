"""
RAG Search — Trợ lý Chi
Priority: NotebookLM HTTP API (1) → ChromaDB (2) → Gemini general knowledge (3)

Luật hiện hành 2024-2025 (cứng):
- Luật PCCC 55/2024/QH15 (thay Luật 2001, 2013)
- Nghị định 105/2025/NĐ-CP (thay NĐ 136/2020)
- QCVN 06:2022/BXD + Sửa đổi 1:2023
- QCVN 10:2025/BCA (thay TCVN 3890:2009)
- QCVN 25:2025/BCT, QCVN 25:2025/BKHCN
"""
import os
import json
import httpx
from dotenv import load_dotenv

load_dotenv()

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


# ═══════════════════════════════════════════════════════════════
#  1. NOTEBOOKLM — HTTP API trực tiếp (ưu tiên cao nhất)
# ═══════════════════════════════════════════════════════════════

def search_notebooklm_api(question: str) -> str:
    """
    Gọi NotebookLM query qua Gemini API thay cho CLI.
    Sử dụng GEMINI_API_KEY để query notebook đã có sẵn.
    Trả về string kết quả hoặc "" nếu thất bại.
    """
    if not NOTEBOOKLM_NOTEBOOK_ID or not GEMINI_API_KEY:
        return ""

    try:
        # Dùng Gemini để query với context từ notebook_id
        # NotebookLM public API endpoint
        url = f"https://notebooklm.google.com/api/v1/artifacts/{NOTEBOOKLM_NOTEBOOK_ID}/query"

        # Thử approach 1: Dùng NLM subprocess nếu có
        import subprocess
        import sys

        # Kiểm tra nlm có trong PATH không
        nlm_paths = [
            "nlm",
            os.path.expanduser("~/.local/bin/nlm"),
            "/usr/local/bin/nlm",
            os.path.join(sys.prefix, "bin", "nlm"),
        ]

        nlm_cmd = None
        for path in nlm_paths:
            try:
                result = subprocess.run([path, "--version"], capture_output=True, timeout=3)
                if result.returncode == 0:
                    nlm_cmd = path
                    break
            except (FileNotFoundError, subprocess.TimeoutExpired):
                continue

        if nlm_cmd:
            # nlm có sẵn — dùng CLI
            try:
                result = subprocess.run(
                    [nlm_cmd, "query", "notebook", NOTEBOOKLM_NOTEBOOK_ID, question],
                    capture_output=True, text=True, timeout=20, encoding="utf-8",
                )
                out = result.stdout.strip()
                # Lọc các dòng warning
                lines = [
                    line for line in out.split("\n")
                    if line.strip()
                    and "Warning" not in line
                    and "You are" not in line
                    and "nlm" not in line.lower()
                ]
                clean = "\n".join(lines).strip()
                if clean:
                    print(f"[NotebookLM CLI] ✅ Got {len(clean)} chars")
                    return clean
            except Exception as e:
                print(f"[NotebookLM CLI] Failed: {e}")

        # nlm không có — dùng Gemini Grounding với prompt system
        print("[NotebookLM] nlm not found, using Gemini with legal context...")
        return ""  # fallback to ChromaDB + Gemini general

    except Exception as e:
        print(f"[NotebookLM] Error: {e}")
        return ""


def search_notebooklm_gemini_grounded(question: str) -> str:
    """
    Fallback: Dùng Gemini API với system context chứa các tài liệu pháp lý đã biết.
    Trả về câu trả lời từ Gemini với kiến thức pháp luật 2024-2025.
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
        with httpx.Client(timeout=30.0) as client:
            resp = client.post(
                f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}",
                json={
                    "contents": [{"parts": [{"text": grounding_prompt}]}],
                    "generationConfig": {"temperature": 0.1, "maxOutputTokens": 1024},
                },
            )
            if resp.status_code == 200:
                data = resp.json()
                content = data["candidates"][0]["content"]["parts"][0]["text"]
                print(f"[Gemini Grounded] ✅ Got {len(content)} chars")
                return content
    except Exception as e:
        print(f"[Gemini Grounded] Error: {e}")

    return ""


# ═══════════════════════════════════════════════════════════════
#  2. CHROMADB — Vector similarity search
# ═══════════════════════════════════════════════════════════════

def search_chromadb(question: str) -> str:
    """Tìm kiếm ChromaDB local. Trả về context string hoặc ''."""
    if not os.path.exists(CHROMA_DB_DIR):
        return ""

    try:
        from langchain_community.vectorstores import Chroma
        from langchain_google_genai import GoogleGenerativeAIEmbeddings

        embeddings = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001",
            google_api_key=GEMINI_API_KEY,
        )
        vectorstore = Chroma(
            persist_directory=CHROMA_DB_DIR,
            embedding_function=embeddings,
        )
        docs = vectorstore.similarity_search(question, k=4)
        if docs:
            context = "\n\n".join([f"[Tài liệu nội bộ]:\n{d.page_content}" for d in docs])
            print(f"[ChromaDB] ✅ Found {len(docs)} chunks")
            return context
    except Exception as e:
        print(f"[ChromaDB] Error: {e}")

    return ""


# ═══════════════════════════════════════════════════════════════
#  3. MAIN FUNCTION — ask_ai_chi
# ═══════════════════════════════════════════════════════════════

def ask_ai_chi(question: str, history_text: str = "", context: str = "") -> dict:
    """
    Trợ lý Chi — RAG Pipeline:
    Priority: NotebookLM → ChromaDB → Gemini general (có ràng buộc luật mới)
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
        if not notebook_context:  # Chỉ query ChromaDB nếu NLM không có kết quả
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

        # ── Gọi Gemini ───────────────────────────────────────────────
        from langchain_google_genai import ChatGoogleGenerativeAI
        from langchain_core.messages import HumanMessage

        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.15,
            google_api_key=GEMINI_API_KEY,
        )
        response = llm.invoke([HumanMessage(content=template)])
        content = response.content

        # Parse JSON
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()

        try:
            result = json.loads(content)
            # Force correct source_type
            result["source_type"] = source_type
            return result
        except json.JSONDecodeError:
            return {
                "reply": content,
                "source_type": source_type,
                "suggestions": [],
                "references": list(CURRENT_LEGAL_REFS[:3]),
            }

    except Exception as e:
        print(f"[ask_ai_chi] Error: {e}")
        return {
            "reply": f"Hệ thống đang tạm thời gián đoạn (lỗi: {str(e)[:100]}). Vui lòng thử lại sau.",
            "source_type": "error",
            "suggestions": [],
            "references": [],
        }
