W,F,FIRE,SMK,EXIT,BCC,TWL,MSK,KEY,DLCK,TOX,PS,FUR,ELEC,BRKR,GASL,GASV,PHONE,HDOOR,SDOOR,NPC,BLCK,EXITL = 1,0,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22

def row(*items):
    return list(items)

# Helper: 25-wide full-wall row
def wrow(): return [W]*25
# Helper: side walls
def s(*mid): return [W]+list(mid)+[W]

LEVELS = [
  # L1 - BCC only, fire blocks exit
  {
    "nameVi":"Bài học đầu tiên: Bình chữa cháy",
    "tip":"Tìm BCC dập lửa chặn đường. Lửa lan nhanh!",
    "time":60,"fireSpread":3,"smokeSpread":8,
    "map":[
      wrow(),
      s(PS,F,F,F,W,F,F,F,F,F,F,W,F,F,F,F,F,W,F,F,F,F,F,F),
      s(F,W,W,F,W,F,W,W,W,F,W,F,W,W,W,F,W,F,W,W,W,W,F,F),
      s(F,F,W,F,F,F,F,F,W,F,F,F,W,F,F,F,F,F,F,F,F,F,W,F),
      s(W,F,W,W,W,F,W,F,W,W,W,F,W,F,W,W,W,W,W,W,W,F,W,F),
      s(F,F,F,F,W,F,W,F,F,F,F,F,F,F,F,F,F,F,F,F,W,F,F,F),
      s(F,W,W,F,W,F,W,W,W,W,W,W,W,W,W,W,F,W,W,F,W,W,W,F),
      s(F,F,W,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,W,F,F,F,F,F),
      s(W,F,W,W,W,W,W,W,W,F,W,W,W,W,W,F,W,F,W,W,W,W,W,F),
      s(BCC,F,F,F,F,F,F,F,F,F,F,F,F,F,W,F,W,F,F,F,F,TWL,F,F),
      s(W,W,W,W,W,F,W,W,W,W,W,W,FIRE,F,W,F,W,W,W,F,W,W,W,W),
      s(F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F),
      s(F,W,W,W,W,W,W,F,W,W,W,F,W,W,W,W,W,W,W,F,W,W,W,F),
      s(F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,W,F),
      s(W,W,F,W,W,W,W,W,W,W,W,F,W,W,W,W,W,F,W,W,W,F,W,F),
      s(F,F,F,F,F,F,F,FIRE,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F),
      s(F,W,W,W,W,W,W,W,W,W,W,W,W,W,W,F,W,W,W,W,W,F,W,W),
      s(F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,FIRE,F,F,EXIT),
      wrow()])},

  # L2 - Towel+smoke+fire blocks exit
  {
    "nameVi":"Hành lang khói",
    "tip":"Lấy KHĂN ƯỚT qua khói. Khăn chỉ dùng 10s trong khói!",
    "time":60,"fireSpread":3,"smokeSpread":6,
    "map":[
      wrow(),
      s(PS,F,F,F,F,W,F,F,F,F,F,F,W,F,F,F,F,F,F,F,F,F,F,F),
      s(F,W,W,F,W,F,W,W,W,W,F,W,F,W,W,W,W,W,F,W,W,W,F,F),
      s(F,F,W,F,F,F,F,F,F,W,F,F,F,F,F,F,F,F,F,F,F,W,F,F),
      s(W,F,W,W,W,F,W,W,F,W,W,W,W,W,W,W,W,W,W,W,F,W,F,F),
      s(TWL,F,F,F,F,F,F,W,F,F,F,F,F,F,F,F,F,F,F,W,F,F,F,F),
      s(W,W,W,W,W,W,F,W,F,W,W,W,W,W,W,W,W,W,F,W,W,W,W,W),
      s(F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,BCC,F),
      s(F,W,W,W,W,W,W,W,W,SMK,SMK,SMK,SMK,SMK,SMK,SMK,SMK,W,F,W,W,W,F,F),
      s(F,F,F,F,F,F,F,W,SMK,SMK,SMK,SMK,SMK,SMK,SMK,SMK,SMK,W,F,F,F,F,F,F),
      s(W,W,F,W,W,W,F,W,SMK,SMK,SMK,SMK,SMK,SMK,SMK,SMK,SMK,W,F,W,W,W,F,F),
      s(F,F,F,F,F,F,F,W,W,W,W,W,F,W,W,W,W,W,F,F,F,F,F,F),
      s(F,W,W,F,W,W,W,F,F,F,F,F,F,F,F,F,F,F,F,W,W,W,W,F),
      s(F,F,F,F,F,W,F,W,W,W,F,W,W,W,F,W,W,W,F,F,F,F,F,F),
      s(W,W,F,W,F,W,F,F,F,F,F,F,F,F,F,F,F,W,W,W,W,W,W,F),
      s(F,F,F,W,F,F,F,W,W,W,W,FIRE,W,W,W,W,F,F,F,F,F,F,F,F),
      s(F,W,W,W,W,W,W,W,F,F,F,F,F,F,F,W,W,W,W,W,W,F,W,W),
      s(F,F,F,F,F,F,F,F,F,W,F,F,F,W,F,F,F,F,F,F,FIRE,F,F,EXIT),
      wrow()]},

  # L3 - Key+LockedDoor+fire+smoke, EXIT row 17 col 23
  {
    "nameVi":"Mê cung chìa khóa",
    "tip":"BCC dập lửa, lấy CHÌA KHÓA mở cửa khóa. Khói lan rộng!",
    "time":60,"fireSpread":3,"smokeSpread":6,
    "map":[
      wrow(),
      s(PS,F,F,F,F,W,F,F,F,F,F,F,F,W,F,F,F,F,F,F,F,F,F,F),
      s(F,W,W,F,W,F,W,W,W,W,W,F,W,F,W,W,W,W,W,F,W,W,F,F),
      s(F,F,W,F,F,F,F,F,F,F,W,F,F,F,W,F,F,TWL,F,F,F,F,W,F),
      s(W,F,W,W,W,F,W,W,W,F,W,W,W,W,W,F,W,W,W,W,W,F,W,F),
      s(BCC,F,F,F,F,F,F,F,W,F,F,F,F,F,F,F,F,F,F,F,W,F,F,F),
      s(W,W,W,W,W,W,W,F,W,F,W,W,W,W,W,W,W,W,W,F,W,W,W,W),
      s(F,F,F,F,F,F,F,F,FIRE,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F),
      s(F,W,W,W,W,W,W,W,W,W,W,W,W,F,W,W,W,W,W,W,W,W,W,F),
      s(F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,KEY,F,F,F,F,F),
      s(W,W,W,W,W,F,W,W,W,W,W,W,W,W,W,W,W,W,W,F,W,W,W,F),
      s(F,F,F,F,F,F,F,F,W,F,F,F,F,SMK,SMK,F,F,F,W,F,F,F,F),
      s(F,W,W,W,W,W,W,F,W,F,W,W,W,W,W,W,W,F,W,W,W,W,W,F),
      s(F,F,F,F,F,F,W,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,W,F),
      s(W,W,W,W,W,F,W,W,W,W,W,F,W,W,W,W,W,W,W,W,W,F,W,F),
      s(F,F,F,F,F,F,F,F,F,F,F,F,F,FIRE,F,F,F,F,F,F,F,F,F,F),
      s(F,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,F,W,W,W,W,W,F),
      s(F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,DLCK,EXIT),
      wrow()]},

  # L4 - Electric+Breaker far, fire+smoke+towel
  {
    "nameVi":"An toàn điện",
    "tip":"Dây điện chặn đường! Tìm CẦU DAO ở cuối bản đồ, bấm SPACE ngắt điện!",
    "time":60,"fireSpread":3,"smokeSpread":6,
    "map":[
      wrow(),
      s(PS,F,F,F,F,F,W,F,F,F,F,F,F,F,W,F,F,F,F,F,F,F,F,F),
      s(F,W,W,W,W,F,W,F,W,W,W,W,W,F,W,F,W,W,W,W,W,W,W,F),
      s(F,F,F,F,W,F,F,F,F,F,F,TWL,F,W,F,F,F,F,F,F,F,W,F,F),
      s(W,W,W,F,W,W,W,W,W,W,W,W,F,W,W,W,W,W,W,W,F,W,F,F),
      s(F,F,F,F,F,F,F,F,F,F,F,W,F,F,F,F,F,F,F,W,F,F,F,F),
      s(F,W,W,W,W,W,F,W,W,F,W,W,W,W,W,W,F,W,W,F,W,W,W,W),
      s(F,F,F,F,F,BCC,F,F,W,F,F,F,F,F,F,F,F,W,F,F,F,F,F,F),
      s(W,W,W,W,W,W,W,F,W,W,W,W,W,W,W,W,F,W,W,W,W,W,W,F),
      s(F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F),
      s(F,W,W,W,F,ELEC,ELEC,ELEC,ELEC,ELEC,ELEC,ELEC,ELEC,ELEC,ELEC,ELEC,ELEC,ELEC,F,W,W,W,W,F),
      s(F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F),
      s(W,W,W,W,W,W,W,F,W,W,W,W,W,W,W,W,F,W,W,W,W,W,W,F),
      s(F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,W,F,F),
      s(F,W,W,W,W,W,F,W,W,W,F,W,W,W,W,W,W,W,W,W,F,W,F,f),
      s(F,F,F,F,F,F,F,F,F,F,F,F,F,FIRE,F,F,F,F,F,F,F,F,F,F),
      s(W,W,F,W,W,W,W,W,W,W,W,W,W,W,W,F,W,W,W,W,W,W,W,F),
      s(F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,BRKR,F,F,F,F,FIRE,EXIT),
      wrow()]}
]

import json, sys
path = r"c:\Users\Hasky\.gemini\antigravity\scratch\fras\frontend\js\tmp_levels_part1.json"
with open(path,"w",encoding="utf-8") as f:
    json.dump(LEVELS,f,ensure_ascii=False)
print("OK part1, levels:",len(LEVELS))
