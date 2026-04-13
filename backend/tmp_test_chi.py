"""Test ask_ai_chi end-to-end with new API key + model"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dotenv import load_dotenv
load_dotenv()

from utils.rag_search import ask_ai_chi, GEMINI_API_KEY, GEMINI_MODEL, NOTEBOOKLM_NOTEBOOK_ID

print("=" * 60)
print(f"API Key: {GEMINI_API_KEY[:12]}...")
print(f"Model  : {GEMINI_MODEL}")
print(f"NLM ID : {NOTEBOOKLM_NOTEBOOK_ID}")
print("=" * 60)

result = ask_ai_chi("Nghị định PCCC mới nhất 2025 là nghị định số mấy?")
print(f"\nsource_type: {result.get('source_type')}")
print(f"references : {result.get('references', [])[:2]}")
print(f"\nREPLY (first 400 chars):\n{result.get('reply', '')[:400]}")
print("\n" + "=" * 60)

# Kiem tra khong con luat cu
reply = result.get('reply', '') + str(result.get('references', []))
forbidden = ['136/2020', '149/2020', '79/2014', 'TCVN 3890:2009']
for f in forbidden:
    if f in reply:
        print(f"WARN: Con su dung luat cu: {f}")
    else:
        print(f"OK: Khong co luat cu {f}")

if result.get('source_type') != 'error':
    print("\nTEST PASSED - Tro ly Chi hoat dong binh thuong!")
else:
    print("\nTEST FAILED - Co loi!")
