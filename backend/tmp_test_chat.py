import httpx, json

# Login
r = httpx.post('http://localhost:8000/api/auth/login', json={'email':'admin@fras.vn','password':'admin123'})
token = r.json()['access_token']
print(f"Login OK, token: {token[:20]}...")

# Chat
r2 = httpx.post(
    'http://localhost:8000/api/ai/chat',
    json={'message': 'Nghi dinh 105 quy dinh gi ve PCCC?'},
    headers={'Authorization': f'Bearer {token}'},
    timeout=30
)
print(f"Status: {r2.status_code}")
print(r2.text[:800])
