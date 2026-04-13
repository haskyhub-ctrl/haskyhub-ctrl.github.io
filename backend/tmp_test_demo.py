import asyncio
import os
import sys
from fastapi.testclient import TestClient

sys.path.append(os.path.join(os.path.dirname(__file__), "backend"))

from main import app
from database import SessionLocal
from models import User, Assessment, AdminAuditLog
from middleware.auth_middleware import create_access_token

# Get an admin user
db = SessionLocal()
admin = db.query(User).filter(User.role == "superadmin").first()
if not admin:
    print("No superadmin found!")
    sys.exit(1)

# Generate token
token = create_access_token({"sub": admin.id})
print(f"Token: {token}")

client = TestClient(app)
headers = {"Authorization": f"Bearer {token}"}

# Test POST /api/admin/assessments/generate
req_data = {
    "count": 5,
    "risk_distribution": "random",
    "province": "Hà Nội"
}
print("Testing Generate...")
res = client.post("/api/admin/assessments/generate", json=req_data, headers=headers)
print(f"Status: {res.status_code}")
print(f"Response: {res.text}")

print("Testing Delete Demo...")
res_delete = client.delete("/api/admin/assessments/demo", headers=headers)
print(f"Status: {res_delete.status_code}")
print(f"Response: {res_delete.text}")

db.close()
