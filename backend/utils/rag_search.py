import os
import json
import subprocess
from dotenv import load_dotenv

load_dotenv()

from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

CHROMA_DB_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "chroma_db")
NOTEBOOKLM_PROJECT_ID = os.getenv("NOTEBOOKLM_PROJECT_ID", "")

def search_notebooklm(question: str, notebook_id: str) -> str:
    """Truy vấn NotebookLM thông qua CLI."""
    if not notebook_id:
        return ""
    try:
        if os.name == 'nt':
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            result = subprocess.run(
                ["nlm", "query", "notebook", notebook_id, question],
                capture_output=True, text=True, timeout=15, encoding='utf-8',
                startupinfo=startupinfo
            )
        else:
            result = subprocess.run(
                ["nlm", "query", "notebook", notebook_id, question],
                capture_output=True, text=True, timeout=15, encoding='utf-8'
            )
        out = result.stdout.strip()
        lines = [line for line in out.split('\n') if "Warning" not in line and "You are" not in line]
        clean_out = '\n'.join(lines).strip()
        return clean_out if clean_out else ""
    except subprocess.TimeoutExpired:
        print("[NBLM MCP] Request timed out sau 15s.")
        return ""
    except Exception as e:
        print(f"[NBLM MCP] Lỗi: {e}")
        return ""


def ask_ai_chi(question: str, history_text: str = "", context: str = "") -> dict:
    """
    Nhận câu hỏi từ người dùng, tìm tài liệu ChromaDB & NotebookLM, trả về Format JSON cho Router.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return {
            "reply": "Xin lỗi, Hệ thống AI Chi chưa được cấu hình GEMINI_API_KEY.",
            "source_type": "error",
            "suggestions": [],
            "references": []
        }

    try:
        # Search ChromaDB
        chroma_context = ""
        if os.path.exists(CHROMA_DB_DIR):
            embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
            vectorstore = Chroma(persist_directory=CHROMA_DB_DIR, embedding_function=embeddings)
            docs = vectorstore.similarity_search(question, k=4)
            if docs:
                chroma_context = "\n\n".join([f"- Nguồn tài liệu Nội bộ:\n{d.page_content}" for d in docs])

        # Search NotebookLM
        notebook_context = ""
        if NOTEBOOKLM_PROJECT_ID:
            print(f"[NotebookLM] Quering project {NOTEBOOKLM_PROJECT_ID}...")
            nb_out = search_notebooklm(question, NOTEBOOKLM_PROJECT_ID)
            if nb_out:
                notebook_context = f"- Nguồn NotebookLM:\n{nb_out}"
        
        # Merge Contexts
        doc_context = ""
        if chroma_context or notebook_context:
            doc_context = f"{chroma_context}\n\n{notebook_context}".strip()
        else:
            doc_context = "(Hệ thống tìm kiếm RAG cục bộ và NotebookLM đều trả về rỗng. Vui lòng chuyển sang dùng kiến thức tự suy luận/hiểu biết chung.)"

        # Generation (LLM)
        llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.2)
        
        template = """Bạn là Trợ lý ảo AI Chi - chuyên gia tư vấn pháp luật PCCC và an toàn cháy nổ tại Việt Nam (thuộc Công an tỉnh Bắc Ninh).

=== CƠ SỞ DỮ LIỆU PHÁP CHẾ (NotebookLM & ChromaDB) ===
{doc_context}
=== HẾT DỮ LIỆU ===

NGỮ CẢNH CƠ SỞ (nếu có):
{context}

LỊCH SỬ HỘI THOẠI:
{history_text}

CÂU HỎI THỰC TẾ CỦA NGƯỜI DÙNG: {question}

NHIỆM VỤ CỦA CHUYÊN GIA:
1. Đọc và ưu tiên phân tích "CƠ SỞ DỮ LIỆU PHÁP CHẾ" để tìm xem có đáp án/thông tin liên quan đến câu hỏi không.
2. NGUYÊN TẮC DỰ PHÒNG CHÍNH (FALLBACK): Nếu CƠ SỞ DỮ LIỆU PHÁP CHẾ trả về rỗng HOẶC tài liệu không cung cấp được thông tin đáp ứng câu hỏi, BẠN CHI ĐƯỢC CHUYỂN SANG DÙNG KIẾN THỨC CHUNG TỪ API GEMINI ĐỂ TỰ TRẢ LỜI NGAY LẬP TỨC theo chuyên môn (tuyệt đối không nói "Trong tài liệu không có nên tôi không biết".
3. Hãy xưng là "Chi" hoặc "Tôi".
4. Trả lời rõ ràng, dễ hiểu, định dạng Markdown (xuống dòng, in đậm). Phải trích dẫn rõ câu trong tài liệu (VD: [1]) nếu sử dụng dữ liệu từ CƠ SỞ DỮ LIỆU PHÁP CHẾ.

TRẢ VỀ KẾT QUẢ DƯỚI DẠNG CHỈ CÓ JSON (không dùng ```json), theo Schema sau:
{{
    "reply": "string - câu trả lời",
    "source_type": "notebooklm" (nếu có dùng bất kỳ dữ liệu nào từ phần NotebookLM), "docs" (từ nội bộ) hoặc "general" (nếu dùng kiến thức chung của Gemini API),
    "suggestions": ["gợi ý 1", "gợi ý 2"],
    "references": ["tên các TCVN, Luật lấy từ cơ sở dữ liệu pháp chế ở trên hoặc trích dẫn, nếu hoàn toàn không có thì để rỗng"]
}}
"""
        prompt = PromptTemplate(template=template, input_variables=["doc_context", "context", "history_text", "question"])
        
        chain = prompt | llm
        
        response = chain.invoke({
            "doc_context": doc_context,
            "context": context,
            "history_text": history_text,
            "question": question
        })
        
        # Parse JSON
        content = response.content
        if "```json" in content:
            content = content.replace("```json", "").replace("```", "").strip()
        elif "```" in content:
            content = content.replace("```", "").strip()
            
        try:
            return json.loads(content)
        except:
             return {
                "reply": content,
                "source_type": "mixed",
                "suggestions": [],
                "references": []
             }
             
    except Exception as e:
        print(f"Lỗi RAG/NotebookLM: {e}")
        return {
            "reply": f"Hệ thống đang bảo trì phần tử RAG (Lỗi mạng hoặc Timeout): {e}",
            "source_type": "error",
            "suggestions": [],
            "references": []
        }
