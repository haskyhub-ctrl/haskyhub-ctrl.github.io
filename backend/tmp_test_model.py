import os
from dotenv import load_dotenv

load_dotenv()
from langchain_google_genai import GoogleGenerativeAIEmbeddings

models_to_test = [
    "models/embedding-001",
    "embedding-001",
    "models/text-embedding-004",
    "text-embedding-004",
    "models/gemini-embedding-2-preview",
    "gemini-embedding-2-preview"
]

print(f"API Key startswith: {os.getenv('GEMINI_API_KEY')[:5]}")

for model_name in models_to_test:
    print(f"Testing model: {model_name}")
    try:
        embeddings = GoogleGenerativeAIEmbeddings(model=model_name)
        res = embeddings.embed_query("test query")
        print(f"✅ Success with {model_name}, dim: {len(res)}")
        break
    except Exception as e:
        print(f"❌ Failed: {e}")
