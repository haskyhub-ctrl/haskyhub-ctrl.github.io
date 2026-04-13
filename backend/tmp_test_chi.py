#!/usr/bin/env python3
"""Quick test cho Trợ lý Chi — kiểm tra source_type và law references"""
import sys
import os
sys.path.insert(0, '/home/ubuntu/fras/backend')
os.environ.setdefault('GEMINI_API_KEY', 'AIzaSyCQKlo7-oLMPdaFgDYGR6LnvmcZXBthUY4')
os.environ.setdefault('NOTEBOOKLM_PROJECT_ID', '0ef4dd55-b191-43ed-ad6f-66f8a218bf4c')

from utils.rag_search import ask_ai_chi

print("=" * 60)
print("TEST: Trợ lý Chi — Kiểm tra luật mới 2024-2025")
print("=" * 60)

result = ask_ai_chi("Nghị định PCCC mới nhất 2025 là nghị định số mấy?")
print(f"\nsource_type: {result.get('source_type')}")
print(f"references: {result.get('references', [])}")
print(f"\nREPLY (400 chars):\n{result.get('reply', '')[:400]}")
print("\n" + "=" * 60)

# Kiểm tra không còn luật cũ
reply = result.get('reply', '') + str(result.get('references', []))
forbidden = ['136/2020', '149/2020', '79/2014', 'TCVN 3890:2009']
for f in forbidden:
    if f in reply:
        print(f"❌ WARN: Còn sử dụng luật cũ: {f}")
    else:
        print(f"✅ OK: Không có luật cũ: {f}")
