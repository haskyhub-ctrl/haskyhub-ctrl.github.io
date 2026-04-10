import os
import json
from dotenv import load_dotenv

load_dotenv()

from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

CHROMA_DB_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "chroma_db")

def ask_ai_chi(question: str, history_text: str = "", context: str = "") -> dict:
    """
    Nhận câu hỏi từ người dùng, tìm tài liệu ChromaDB, trả về Format JSON cho Router.
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
        if not os.path.exists(CHROMA_DB_DIR):
            doc_context = "(Chưa có cơ sở dữ liệu luật trong ChromaDB. Hệ thống tự suy luận.)"
        else:
            embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-2-preview")
            vectorstore = Chroma(persist_directory=CHROMA_DB_DIR, embedding_function=embeddings)
            
            # Khởi tạo thuật toán tìm kiếm giống nhất (Retrieval)
            docs = vectorstore.similarity_search(question, k=4)
            if not docs:
                doc_context = "(Không tìm thấy đoạn luật nào phù hợp.)"
            else:
                doc_context = "\n\n".join([f"- Nguồn tài liệu:\n{d.page_content}" for d in docs])

        # Generation (LLM)
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.2)
        
        template = """Bạn là Trợ lý ảo AI Chi - chuyên gia tư vấn pháp luật PCCC và an toàn cháy nổ tại Việt Nam (thuộc Công an tỉnh Bắc Ninh).

=== CƠ SỞ DỮ LIỆU PHÁP CHẾ VỪA TÌM ĐƯỢC (Vector DB) ===
{doc_context}
=== HẾT DỮ LIỆU ===

NGỮ CẢNH CƠ SỞ (nếu có):
{context}

LỊCH SỬ HỘI THOẠI:
{history_text}

CÂU HỎI THỰC TẾ CỦA NGƯỜI DÙNG: {question}

NHIỆM VỤ CỦA CHUYÊN GIA:
1. Nếu câu hỏi liên quan đến luật pháp/kỹ thuật PCCC, BẮT BUỘC ưu tiên sử dụng "CƠ SỞ DỮ LIỆU PHÁP CHẾ" ở trên để trả lời. Phải trích dẫn rõ điều/khoản/tên văn bản nếu có trong tài liệu.
2. Nếu "CƠ SỞ DỮ LIỆU PHÁP CHẾ" không có thông tin, hãy dùng kiến thức chung của bạn, nhưng hãy xưng là "Chi" hoặc "Tôi".
3. Trả lời rõ ràng, dễ hiểu, định dạng Markdown (xuống dòng, in đậm).

TRẢ VỀ KẾT QUẢ DƯỚI DẠNG CHỈ CÓ JSON (không dùng ```json), theo Schema sau:
{{
    "reply": "string - câu trả lời",
    "source_type": "docs" (nếu có dùng dữ liệu VectorDB) hoặc "general" (nếu dùng kiến thức chung),
    "suggestions": ["gợi ý 1", "gợi ý 2"],
    "references": ["tên các TCVN, Luật lấy từ cơ sở dữ liệu pháp chế ở trên, nếu không có thì để rỗng"]
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
        print(f"Lỗi RAG: {e}")
        return {
            "reply": f"Hệ thống đang bảo trì phần tử RAG: {e}",
            "source_type": "error",
            "suggestions": [],
            "references": []
        }
