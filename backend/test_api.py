import urllib.request
import json

# Test 1: All categories (no filter)
resp = urllib.request.urlopen('http://localhost:8000/api/survey/categories')
data = json.loads(resp.read())
print(f"=== All categories (no filter): {len(data)} ===")
for c in data:
    print(f"  {c['name']} ({len(c['questions'])} questions)")
total_q = sum(len(c['questions']) for c in data)
print(f"  TOTAL: {total_q} questions")

print()

# Test 2: Filter by industrial
resp2 = urllib.request.urlopen('http://localhost:8000/api/survey/categories?facility_type=industrial')
data2 = json.loads(resp2.read())
print(f"=== Industrial filter: {len(data2)} categories ===")
for c in data2:
    print(f"  {c['name']} ({len(c['questions'])} questions)")
total_q2 = sum(len(c['questions']) for c in data2)
print(f"  TOTAL: {total_q2} questions")

print()

# Test 3: Filter by residential
resp3 = urllib.request.urlopen('http://localhost:8000/api/survey/categories?facility_type=residential')
data3 = json.loads(resp3.read())
print(f"=== Residential filter: {len(data3)} categories ===")
for c in data3:
    print(f"  {c['name']} ({len(c['questions'])} questions)")
total_q3 = sum(len(c['questions']) for c in data3)
print(f"  TOTAL: {total_q3} questions")
