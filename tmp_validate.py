import sys, json
sys.path.insert(0, 'backend')
from seed_data import COMMON_CATEGORIES, ALL_COMMON_QUESTIONS, FACILITY_TYPES
from seed_data_specific import ALL_SPECIFIC_CATEGORIES

tc = 0
for idx, qs in ALL_COMMON_QUESTIONS:
    tc += len(qs)
    cat = COMMON_CATEGORIES[idx]
    print(f"  Common [{idx}] {cat['name']}: {len(qs)} qs, icon={cat['icon']}, max={cat['max_score']}")

ts = 0
for sp in ALL_SPECIFIC_CATEGORIES:
    ts += len(sp['questions'])
    print(f"  Specific [{sp['facility_type']}] {sp['name']}: {len(sp['questions'])} qs")

print(f"Total: {tc} common + {ts} specific = {tc+ts}")
print(f"Facility types: {len(FACILITY_TYPES)}")
print("All OK!")
