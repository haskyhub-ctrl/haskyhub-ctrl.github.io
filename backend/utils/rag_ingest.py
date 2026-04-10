import os
from dotenv import load_dotenv

load_dotenv()

from langchain_community.document_loaders import TextLoader, PyPDFLoader, Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma

DOCS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data_docs")
CHROMA_DB_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "chroma_db")

def ingest_docs():
    print(f"Bắt đầu đọc tài liệu từ {DOCS_DIR}...")
    docs = []
    
    if not os.path.exists(DOCS_DIR):
        print(f"Thư mục {DOCS_DIR} không tồn tại!")
        return

    for filename in os.listdir(DOCS_DIR):
        # Bỏ qua các file tạm của Word hoặc file ẩn
        if filename.startswith("~$") or filename.startswith("."):
            continue
            
        file_path = os.path.join(DOCS_DIR, filename)
        try:
            if filename.endswith(".txt"):
                loader = TextLoader(file_path, encoding='utf-8')
                docs.extend(loader.load())
            elif filename.endswith(".pdf"):
                loader = PyPDFLoader(file_path)
                docs.extend(loader.load())
            elif filename.endswith(".docx") or filename.endswith(".doc"):
                loader = Docx2txtLoader(file_path)
                docs.extend(loader.load())
        except Exception as e:
            print(f"Lỗi khi đọc file {filename}: {e}")

    if not docs:
        print("Không tìm thấy dữ liệu để nạp.")
        return

    print(f"Tìm thấy {len(docs)} file. Đang tiến hành Chunking...")
    # Tách đoạn: khoảng 1000 ký tự sẽ được cắt làm 1 chunk, overlap 100 để không đứt nghĩa
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = text_splitter.split_documents(docs)
    
    print(f"Đã tạo ra {len(chunks)} chunks. Tiến hành nhúng (Embedding) vào ChromaDB...")
    
    # Sử dụng Google Gemini Embeddings
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("LỖI: Không tìm thấy GEMINI_API_KEY trong file .env")
        return
        
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-2-preview")
    
    import time
    
    # Khởi tạo Chroma rỗng
    vectorstore = Chroma(
        embedding_function=embeddings, 
        persist_directory=CHROMA_DB_DIR
    )
    
    batch_size = 50  # Số lượng chunk mỗi lần gửi
    total_batches = (len(chunks) + batch_size - 1) // batch_size
    
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i + batch_size]
        print(f"Đang nhúng batch {i // batch_size + 1}/{total_batches}...")
        try:
            vectorstore.add_documents(batch)
            time.sleep(1) # Nghỉ để tránh Rate Limit Quota của Google
        except Exception as e:
            if 'RESOURCE_EXHAUSTED' in str(e):
                print("⚠️ Bị giới hạn API ngắt quãng, tạm nghỉ 30 giây...")
                time.sleep(30)
                vectorstore.add_documents(batch)
            else:
                raise e
                
    vectorstore.persist()
    print(f"✅ Hoàn thành Ingest! Toàn bộ vector đã được lưu tại {CHROMA_DB_DIR}")

if __name__ == "__main__":
    ingest_docs()
