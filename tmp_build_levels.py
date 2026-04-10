"""
Build script for Fire Escape Game levels.
25x19 tile grids, validated with state-space BFS.
Uses serpentine horizontal barriers with maze corridors for difficulty.
"""
import json
from collections import deque

CHAR_MAP = {
    '.': 0, '#': 1, 'F': 2, 'S': 3, 'E': 4, 'B': 5, 'T': 6, 'M': 7,
    'K': 8, 'D': 9, 'X': 10, 'P': 11, 'f': 12, 'e': 13, 'b': 14,
    'g': 15, 'V': 16, 'p': 17, 'H': 18, 's': 19, 'N': 20, 'O': 21, 'L': 22,
}
W, H = 25, 19


def parse_map(ascii_str: str) -> list[list[int]]:
    lines = ascii_str.strip().split('\n')
    grid = []
    for i, line in enumerate(lines):
        row = [CHAR_MAP[ch] for ch in line if ch in CHAR_MAP]
        if len(row) != W:
            raise ValueError(f"Row {i}: {len(row)} tiles != {W}")
        grid.append(row)
    if len(grid) != H:
        raise ValueError(f"{len(grid)} rows != {H}")
    return grid


def validate_level(level_data: dict, level_num: int) -> bool:
    m = [row[:] for row in level_data['map']]
    R, C = len(m), len(m[0])
    ps = next(((r,c) for r in range(R) for c in range(C) if m[r][c]==11), None)
    if not ps:
        print(f"  Level {level_num}: NO PLAYER START!")
        return False

    BCC,TWL,MSK,KEY = 1,2,4,8
    BRK,GAS,C114 = 1,2,4
    init = (ps[0],ps[1],0,0,frozenset())
    vis = {init}
    q = deque([init])
    found = False

    while q:
        r,c,inv,wf,cl = q.popleft()
        def ta(rr,cc):
            if (rr,cc) in cl: return 0
            t=m[rr][cc]
            if t==11: return 0
            if t==22 and (wf&C114): return 4
            return t
        def ts(nr,nc,ni,nw,ncl):
            s=(nr,nc,ni,nw,ncl)
            if s not in vis: vis.add(s); q.append(s)

        for dr,dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr,nc = r+dr,c+dc
            if not (0<=nr<R and 0<=nc<C): continue
            t = ta(nr,nc)
            if t==14 and not(wf&BRK):
                ep=frozenset((rr,cc) for rr in range(R) for cc in range(C) if m[rr][cc]==13)
                ts(r,c,inv,wf|BRK,cl|ep)
            elif t==16 and not(wf&GAS):
                gp=frozenset((rr,cc) for rr in range(R) for cc in range(C) if m[rr][cc]==15)
                ts(r,c,inv,wf|GAS,cl|gp)
            elif t==17 and not(wf&C114): ts(r,c,inv,wf|C114,cl)
            elif t==19: ts(r,c,inv,wf,cl|frozenset([(nr,nc)]))
            elif t==21: ts(r,c,inv,wf,cl|frozenset([(nr,nc)]))

        for dr,dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr,nc = r+dr,c+dc
            if not (0<=nr<R and 0<=nc<C): continue
            t = ta(nr,nc)
            ni,nw,ncl = inv,wf,cl
            if t in (1,12,21,14,16,17,18,19): continue
            if t==13:
                if wf&BRK: ncl=cl|frozenset([(nr,nc)])
                else: continue
            if t==15:
                if not(wf&GAS): continue
            if t==2:
                if inv&BCC: ts(r,c,inv&~BCC,nw,cl|frozenset([(nr,nc)]))
                continue
            if t==3:
                if not(inv&TWL): continue
            if t==10:
                if not(inv&MSK): continue
            if t==9:
                if inv&KEY: ts(r,c,inv&~KEY,nw,cl|frozenset([(nr,nc)]))
                continue
            if t==22: continue
            if t==5: ni=inv|BCC; ncl=cl|frozenset([(nr,nc)])
            if t==6: ni=inv|TWL; ncl=cl|frozenset([(nr,nc)])
            if t==7: ni=inv|MSK; ncl=cl|frozenset([(nr,nc)])
            if t==8: ni=inv|KEY; ncl=cl|frozenset([(nr,nc)])
            if t==20: ncl=cl|frozenset([(nr,nc)])
            if t==4: found=True
            ts(nr,nc,ni,nw,ncl)

    s = "SOLVABLE" if found else "*** UNSOLVABLE ***"
    print(f"  Level {level_num}: {s} ({len(vis)} states)")
    return found


# ============================================================
# LEVELS - Each uses horizontal barriers (serpentine pattern)
# with maze corridors, dead-end rooms, and furniture
# ============================================================

# Level 1: Fire Extinguisher - Apartment with corridors
LEVEL_1 = {
    "nameVi": "Bài học đầu tiên: Bình chữa cháy",
    "tip": "Tìm BÌNH CHỮA CHÁY (đỏ) rồi dập lửa chặn đường để thoát ra EXIT.",
    "time": 120, "fireSpread": 0,
# Path: P→right→down past wall→left to B→down past wall→right→extinguish F→down→E
    "ascii": """
#########################
#P..f...#...............#
#.......#.......f.......#
#.......#...............#
##.######...............#
#..........f............#
#.......................#
#...............B.......#
#.......................#
######################.##
#.......................#
#...f...................#
#.......................#
##F######################
#.......................#
#.............f.........#
#.......................#
#..................E....#
#########################
"""}

# Level 2: Smoke Corridor - Office building with smoke-filled corridor
LEVEL_2 = {
    "nameVi": "Hành lang khói",
    "tip": "Tìm KHĂN ƯỚT (xanh) bịt mũi miệng rồi đi qua vùng khói dày đặc!",
    "time": 120, "fireSpread": 0,
# Path: P→explore→T→through gaps→cross smoke→E
    "ascii": """
#########################
#P..f.......#...........#
#...........#...........#
#...........#.....T.....#
#...........#...........#
####.########...........#
#............f..........#
#.......................#
######################.##
#SSSSSSSSSSSSSSSSSSSSSSS#
#SSSSSSSSSSSSSSSSSSSSSSS#
#SSSSSSSSSSSSSSSSSSSSSSS#
##.######################
#.......................#
#.......................#
#...f...........f.......#
#.......................#
#..................E....#
#########################
"""}

# Level 3: Key Maze - Multi-room building
LEVEL_3 = {
    "nameVi": "Mê cung chìa khóa",
    "tip": "Tìm CHÌA KHÓA (vàng) rồi mở cửa để thoát! Khám phá nhiều phòng!",
    "time": 140, "fireSpread": 0,
# Path: P→right→down→right to K→backtrack→down through D→E
    "ascii": """
#########################
#P..#...f...#...........#
#...#.......#...........#
#...#.......#...f.......#
#...##.######...........#
#...........#...........#
#.....f.....####.########
#.......................#
#.................K.....#
######################.##
#.......................#
#...f...................#
#.......................#
##D######################
#.......................#
#.............f.........#
#.......................#
#..................E....#
#########################
"""}

# Level 4: Electrical Safety - Industrial building
LEVEL_4 = {
    "nameVi": "An toàn điện",
    "tip": "Tìm CẦU DAO rồi TƯƠNG TÁC (Space/Enter) để ngắt điện trước khi đi qua!",
    "time": 130, "fireSpread": 0,
# Path: P→find b→interact→through eee zone→E
    "ascii": """
#########################
#P..f.......#...........#
#...........#...........#
#...........#.....b.....#
#...........#...........#
####.########...........#
#............f..........#
#.......................#
######################.##
#.......................#
#...f...................#
#.......................#
#.......................#
##eeeee##################
#.......................#
#.............f.........#
#.......................#
#..................E....#
#########################
"""}

# Level 5: Gas Leak - Chemical facility
LEVEL_5 = {
    "nameVi": "Rò rỉ gas cực kỳ nguy hiểm",
    "tip": "KHÓA VAN GAS (V, Space) trước! Lấy bình chữa cháy rồi dập lửa!",
    "time": 150, "fireSpread": 0,
# Path: P→V(interact)→B(pickup)→through cleared gas→extinguish F→E
    "ascii": """
#########################
#P..f...................#
#.......................#
#.......V...............#
#.......................#
######################.##
#.......................#
#...f...........B.......#
#.......................#
##.######################
#.......................#
#..........f............#
#.......................#
##gggggF#################
#.......................#
#.............f.........#
#.......................#
#..................E....#
#########################
"""}

# Level 6: Darkness in Smoke - Dark building with TWL+BCC combo
LEVEL_6 = {
    "nameVi": "Bóng tối trong khói",
    "tip": "Lấy KHĂN ƯỚT qua khói dày, rồi tìm BÌNH CHỮA CHÁY dập lửa thoát nạn!",
    "time": 160, "fireSpread": 0,
# Path: P→T→cross smoke→B→extinguish FF→E
    "ascii": """
#########################
#P..f...................#
#.......................#
#...........T...........#
#.......................#
######################.##
#SSSSSSSSSSSSSSSSSSSSSSS#
#SSSSSSSSSSSSSSSSSSSSSSS#
#SSSSSSSSSSSSSSSSSSSSSSS#
##.######################
#.......................#
#...f...........B.......#
#.......................#
######################.##
#.......................#
#........F..............#
#.......................#
#..................E....#
#########################
"""}

# Level 7: Call 114 - Emergency scenario with locked exit
LEVEL_7 = {
    "nameVi": "Gọi cứu hộ 114",
    "tip": "Dập lửa chặn đường, tìm ĐIỆN THOẠI gọi 114 để mở cửa thoát hiểm!",
    "time": 150, "fireSpread": 0,
# Path: P→B→extinguish F→find p→call 114→L becomes E
    "ascii": """
#########################
#P..f...................#
#.......................#
#...........B...........#
#.......................#
######################.##
#.......................#
#...f...................#
#.......................#
##F######################
#.......................#
#..........f............#
#.......................#
##.######################
#.......................#
#.....p.........f.......#
#.......................#
#..................L....#
#########################
"""}

# Level 8: Check Doors - Smoke + Hot/Safe doors
LEVEL_8 = {
    "nameVi": "Kiểm tra cửa!",
    "tip": "Kiểm tra cửa trước khi mở! Cửa NÓNG = nguy hiểm. Cửa an toàn → đi tiếp!",
    "time": 140, "fireSpread": 0,
# Path: P→T→cross smoke→try doors (H kills, s opens)→E
    "ascii": """
#########################
#P..f...................#
#.......................#
#...........T...........#
#.......................#
######################.##
#.......................#
#...f...................#
#SSSSSSSSSSSSSSSSSSSSSSS#
#SSSSSSSSSSSSSSSSSSSSSSS#
#.......................#
####H########s###########
#.......#...............#
#..f....#...............#
#.......#.......f.......#
#.......#...............#
#.......#...............#
#.......#..........E....#
#########################
"""}

# Level 9: Rescue NPC - Building with trapped person
LEVEL_9 = {
    "nameVi": "Giải cứu người bị kẹt",
    "tip": "Dọn chướng ngại vật (Space), cứu người bị kẹt (N), dập lửa rồi thoát!",
    "time": 160, "fireSpread": 0,
# Path: P→right to O(interact)→N(rescue)→back→B→extinguish FF→E
    "ascii": """
#########################
#P..f...........#...N...#
#...............#.......#
#...............#.O.....#
#...............#.......#
####.############.......#
#............f..........#
#.......................#
#...........B...........#
#.......................#
######################.##
#.......................#
#..........f............#
#.......................#
##FF#####################
#.......................#
#.............f.........#
#..................E....#
#########################
"""}

# Level 10: Final Test - ALL mechanics, fire spreads!
LEVEL_10 = {
    "nameVi": "Tổng hợp: Thoát nạn hoàn hảo!",
    "tip": "Ngắt điện → Khóa gas → Dập lửa → Qua khói → Gọi 114 → Thoát!",
    "time": 200, "fireSpread": 12,
# Path: b(interact)→eee cleared→V(interact)→B→ggg cleared→extinguish FF→
#       T→cross smoke→p(call 114)→L becomes E
    "ascii": """
#########################
#P..f...................#
#.......................#
#...b...........T.......#
#.......................#
######################.##
#...eee.................#
#...eee.................#
##.######################
#.......................#
#...V...........B.......#
#.......................#
######################.##
#...ggg.................#
#...gggFF...............#
##.######################
#SSSSSSSSSSSSS..........#
#.....p.......#....L....#
#########################
"""}


def main():
    levels = [LEVEL_1,LEVEL_2,LEVEL_3,LEVEL_4,LEVEL_5,
              LEVEL_6,LEVEL_7,LEVEL_8,LEVEL_9,LEVEL_10]
    output, ok = [], True
    print("Validating levels...")
    for i,lv in enumerate(levels):
        try:
            grid = parse_map(lv["ascii"])
        except ValueError as e:
            print(f"  Level {i+1}: PARSE ERROR - {e}")
            ok = False; continue
        ld = {"nameVi":lv["nameVi"],"tip":lv["tip"],
              "time":lv["time"],"fireSpread":lv["fireSpread"],"map":grid}
        if not validate_level(ld,i+1): ok = False
        output.append(ld)

    print("\nAll levels validated!" if ok else "\n*** ISSUES FOUND ***")
    js = "window.GAME_LEVELS = " + json.dumps(output,indent=2,ensure_ascii=False) + ";\n"
    with open("frontend/js/game-levels.js","w",encoding="utf-8") as f: f.write(js)
    print(f"Wrote {len(output)} levels to frontend/js/game-levels.js")

if __name__=="__main__": main()
