
# Tile constants
F,W,FIRE,SMK,EXIT,BCC,TWL,MSK,KEY = 0,1,2,3,4,5,6,7,8
DLCK,TOX,PS,FUR,ELEC,BRKR,GASL,GASV,PHONE = 9,10,11,12,13,14,15,16,17
HDOOR,SDOOR,NPC,BLCK,EXITL = 18,19,20,21,22

def wr(): return [W]*25  # full wall row
def sw(*m): return [W]+list(m)+[W]  # side-walled row (23 middle items)

# ── Palettes for each level ─────────────────────────────
# Each map is 25 wide, 19 tall.

L1 = {
"nameVi":"Bài học đầu tiên: Bình chữa cháy",
"tip":"Tìm BCC dập lửa chặn đường. Lửa lan nhanh!",
"time":60,"fireSpread":3,"smokeSpread":8,
"map":[
wr(),
sw(PS,F,F,F,W,F,F,F,F,F,F,W,F,F,F,F,F,W,F,F,F,F,F,F),
sw(F,W,W,F,W,F,W,W,W,F,W,F,W,W,W,F,W,F,W,W,W,W,F,F),
sw(F,F,W,F,F,F,F,F,W,F,F,F,W,F,F,F,F,F,F,F,F,F,W,F),
sw(W,F,W,W,W,F,W,F,W,W,W,F,W,F,W,W,W,W,W,W,W,F,W,F),
sw(F,F,F,F,W,F,W,F,F,F,F,F,F,F,F,F,F,F,F,F,W,F,F,F),
sw(F,W,W,F,W,F,W,W,W,W,W,W,W,W,W,W,F,W,W,F,W,W,W,F),
sw(F,F,W,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,W,F,F,F,F,F),
sw(W,F,W,W,W,W,W,W,W,F,W,W,W,W,W,F,W,F,W,W,W,W,W,F),
sw(BCC,F,F,F,F,F,F,F,F,F,F,F,F,F,W,F,W,F,F,F,TWL,F,F,F),
sw(W,W,W,W,W,F,W,W,W,W,W,FIRE,FIRE,F,W,F,W,W,W,F,W,W,W,W),
sw(F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F),
sw(F,W,W,W,W,W,W,F,W,W,W,F,W,W,W,W,W,W,W,F,W,W,W,F),
sw(F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,W,F),
sw(W,W,F,W,W,W,W,W,W,W,W,F,W,W,W,W,W,F,W,W,W,F,W,F),
sw(F,F,F,F,F,F,F,FIRE,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F),
sw(F,W,W,W,W,W,W,W,W,W,W,W,W,W,W,F,W,W,W,W,W,F,W,W),
sw(F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,FIRE,F,F,EXIT),
wr()]}

L2 = {
"nameVi":"Hành lang khói",
"tip":"Lấy KHĂN ƯỚT qua khói. Khăn chỉ dùng 10s trong khói!",
"time":60,"fireSpread":3,"smokeSpread":6,
"map":[
wr(),
sw(PS,F,F,F,F,W,F,F,F,F,F,F,W,F,F,F,F,F,F,F,F,F,F,F),
sw(F,W,W,F,W,F,W,W,W,W,F,W,F,W,W,W,W,W,F,W,W,W,F,F),
sw(F,F,W,F,F,F,F,F,F,W,F,F,F,F,F,F,F,F,F,F,F,W,F,F),
sw(W,F,W,W,W,F,W,W,F,W,W,W,W,W,W,W,W,W,W,W,F,W,F,F),
sw(TWL,F,F,F,F,F,F,W,F,F,F,F,F,F,F,F,F,F,F,W,F,F,F,F),
sw(W,W,W,W,W,W,F,W,F,W,W,W,W,W,W,W,W,W,F,W,W,W,W,W),
sw(F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,BCC,F),
sw(F,W,W,W,W,W,W,W,SMK,SMK,SMK,SMK,SMK,SMK,SMK,SMK,SMK,W,F,W,W,W,F,F),
sw(F,F,F,F,F,F,F,W,SMK,SMK,SMK,SMK,SMK,SMK,SMK,SMK,SMK,W,F,F,F,F,F,F),
sw(W,W,F,W,W,W,F,W,SMK,SMK,SMK,SMK,SMK,SMK,SMK,SMK,SMK,W,F,W,W,W,F,F),
sw(F,F,F,F,F,F,F,W,W,W,W,W,F,W,W,W,W,W,F,F,F,F,F,F),
sw(F,W,W,F,W,W,W,F,F,F,F,F,F,F,F,F,F,F,F,W,W,W,W,F),
sw(F,F,F,F,F,W,F,W,W,W,F,W,W,W,F,W,W,W,F,F,F,F,F,F),
sw(W,W,F,W,F,W,F,F,F,F,F,F,F,F,F,F,F,W,W,W,W,W,W,F),
sw(F,F,F,W,F,F,F,W,W,W,W,FIRE,W,W,W,W,F,F,F,F,F,F,F,F),
sw(F,W,W,W,W,W,W,W,F,F,F,F,F,F,F,W,W,W,W,W,W,F,W,W),
sw(F,F,F,F,F,F,F,F,F,W,F,F,F,W,F,F,F,F,F,FIRE,F,F,F,EXIT),
wr()]}

L3 = {
"nameVi":"Mê cung chìa khóa",
"tip":"BCC dập lửa, lấy CHÌA KHÓA mở cửa khóa. Khói lan rộng!",
"time":60,"fireSpread":3,"smokeSpread":6,
"map":[
wr(),
sw(PS,F,F,F,F,W,F,F,F,F,F,F,F,W,F,F,F,F,F,F,F,F,F,F),
sw(F,W,W,F,W,F,W,W,W,W,W,F,W,F,W,W,W,W,W,F,W,W,F,F),
sw(F,F,W,F,F,F,F,F,F,F,W,F,F,F,W,F,TWL,F,F,F,F,F,W,F),
sw(W,F,W,W,W,F,W,W,W,F,W,W,W,W,W,F,W,W,W,W,W,F,W,F),
sw(BCC,F,F,F,F,F,F,F,W,F,F,F,F,F,F,F,F,F,F,F,W,F,F,F),
sw(W,W,W,W,W,W,W,F,W,F,W,W,W,W,W,W,W,W,W,F,W,W,W,W),
sw(F,F,F,F,F,F,F,F,FIRE,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F),
sw(F,W,W,W,W,W,W,W,W,W,W,W,W,F,W,W,W,W,W,W,W,W,W,F),
sw(F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,KEY,F,F,F,F,F,F),
sw(W,W,W,W,W,F,W,W,W,W,W,W,W,W,W,W,W,W,W,F,W,W,W,F),
sw(F,F,F,F,F,F,F,F,W,F,F,F,SMK,SMK,F,F,F,W,F,F,F,F,F,F),
sw(F,W,W,W,W,W,W,F,W,F,W,W,W,W,W,W,W,F,W,W,W,W,W,F),
sw(F,F,F,F,F,F,W,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,W,F),
sw(W,W,W,W,W,F,W,W,W,W,W,F,W,W,W,W,W,W,W,W,W,F,W,F),
sw(F,F,F,F,F,F,F,F,F,F,F,F,FIRE,F,F,F,F,F,F,F,F,F,F,F),
sw(F,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,F,W,W,W,W,W,F),
sw(F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,DLCK,F,EXIT),
wr()]}

L4 = {
"nameVi":"An toàn điện - Cầu dao ở xa",
"tip":"Dây điện chặn đường! Tìm CẦU DAO tận cuối bản đồ, bấm SPACE ngắt điện!",
"time":60,"fireSpread":3,"smokeSpread":6,
"map":[
wr(),
sw(PS,F,F,F,F,F,W,F,F,F,F,F,F,F,W,F,F,F,F,F,F,F,F,F),
sw(F,W,W,W,W,F,W,F,W,W,W,W,W,F,W,F,W,W,W,W,W,W,W,F),
sw(F,F,F,F,W,F,F,F,F,F,TWL,F,W,F,F,F,F,F,F,F,F,W,F,F),
sw(W,W,W,F,W,W,W,W,W,W,W,W,F,W,W,W,W,W,W,W,F,W,F,F),
sw(F,F,F,F,F,F,F,F,F,F,F,W,F,F,F,F,F,F,F,W,F,F,F,F),
sw(F,W,W,W,W,W,F,W,W,F,W,W,W,W,W,W,F,W,W,F,W,W,W,W),
sw(F,F,F,F,F,BCC,F,F,W,F,F,F,F,F,F,F,F,W,F,F,F,F,F,F),
sw(W,W,W,W,W,W,W,F,W,W,W,W,W,W,W,W,F,W,W,W,W,W,W,F),
sw(F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F),
sw(F,W,W,W,F,ELEC,ELEC,ELEC,ELEC,ELEC,ELEC,ELEC,ELEC,ELEC,ELEC,ELEC,ELEC,ELEC,F,W,W,W,W,F),
sw(F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F),
sw(W,W,W,W,W,W,W,F,W,W,W,W,W,W,W,W,F,W,W,W,W,W,W,F),
sw(F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,W,F,F),
sw(F,W,W,W,W,W,F,W,W,W,F,W,W,W,W,W,W,W,W,W,F,W,F,F),
sw(F,F,F,F,F,F,F,F,F,F,F,F,F,FIRE,F,F,F,F,F,F,F,F,F,F),
sw(W,W,F,W,W,W,W,W,W,W,W,W,W,W,W,F,W,W,W,W,W,W,W,F),
sw(F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,BRKR,F,F,F,FIRE,F,EXIT),
wr()]}

L5 = {
"nameVi":"Rò rỉ gas nguy hiểm",
"tip":"Gas rò! Tim VAN GAS ở sâu bên trong (cuối map), khóa gas TRƯỚC khi dập lửa!",
"time":60,"fireSpread":3,"smokeSpread":6,
"map":[
wr(),
sw(PS,F,F,F,F,W,F,F,F,F,F,F,W,F,F,F,F,F,W,F,F,F,F,F),
sw(F,W,W,F,W,F,W,W,W,W,F,W,F,W,W,W,F,W,F,W,W,W,F,F),
sw(F,F,W,F,F,F,F,F,F,W,F,F,F,F,F,F,F,F,F,F,F,W,F,F),
sw(W,F,W,W,W,F,W,W,F,W,W,W,W,W,W,W,W,W,W,W,F,W,F,F),
sw(BCC,F,F,F,F,F,F,W,F,F,F,F,F,F,F,F,TWL,F,F,W,F,F,F,F),
sw(W,W,W,W,W,W,F,W,F,W,W,W,W,W,W,W,W,W,F,W,W,W,W,W),
sw(F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F),
sw(F,W,W,W,W,W,W,W,W,W,W,F,W,W,W,W,W,W,W,W,W,W,W,F),
sw(F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F),
sw(W,W,W,W,W,F,W,GASL,GASL,GASL,W,W,F,W,GASL,GASL,GASL,W,W,F,W,W,W,W),
sw(F,F,F,F,F,F,W,GASL,GASL,GASL,F,F,F,W,GASL,GASL,GASL,F,F,F,F,F,F,F),
sw(F,W,W,W,F,F,W,F,FIRE,FIRE,F,W,F,W,F,FIRE,FIRE,F,W,W,W,F,F,F),
sw(F,F,F,W,F,F,F,W,W,W,F,W,F,W,W,W,F,F,F,F,F,F,F,F),
sw(W,W,F,W,W,W,W,W,F,W,W,W,W,W,W,W,F,W,W,W,W,W,W,F),
sw(F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F),
sw(F,W,W,W,W,W,W,W,W,F,W,W,W,W,W,F,W,W,W,W,W,W,W,F),
sw(F,F,F,F,F,F,F,F,F,F,F,F,GASV,F,F,F,F,F,F,F,F,FIRE,F,EXIT),
wr()]}

L6 = {
"nameVi":"Bóng tối trong khói",
"tip":"Khói dày + Lửa chặn EXIT! Lấy khăn ướt qua khói, BCC dập lửa gần EXIT!",
"time":60,"fireSpread":3,"smokeSpread":5,
"map":[
wr(),
sw(PS,F,F,F,F,W,F,F,F,F,TWL,F,W,F,F,F,F,F,F,F,F,F,F,F),
sw(F,W,W,F,W,F,W,W,W,W,W,F,W,F,W,W,W,W,W,W,W,W,W,F),
sw(F,F,W,F,F,F,F,F,F,F,W,F,F,F,F,F,F,F,F,F,F,F,W,F),
sw(W,F,W,W,W,W,W,W,W,F,W,W,W,W,W,F,W,W,W,W,W,F,W,F),
sw(F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,W,F,BCC,F,F,F,F,F),
sw(F,W,W,W,F,W,W,W,W,W,W,W,W,W,W,W,W,F,W,W,W,W,W,W),
sw(F,F,F,W,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F),
sw(W,W,F,W,F,W,SMK,SMK,SMK,SMK,SMK,SMK,SMK,SMK,SMK,SMK,SMK,SMK,W,F,W,W,W,F),
sw(F,F,F,F,F,W,SMK,SMK,SMK,SMK,SMK,SMK,SMK,SMK,SMK,SMK,SMK,SMK,W,F,F,F,F,F),
sw(F,W,W,W,W,W,W,W,W,W,W,W,W,F,W,W,W,W,W,W,W,W,W,F),
sw(F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F),
sw(W,W,F,W,W,W,W,W,W,W,W,F,W,W,W,W,W,F,W,W,W,W,W,F),
sw(F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F),
sw(F,W,W,W,W,W,F,W,W,W,W,W,W,W,W,F,W,W,W,W,W,F,W,W),
sw(F,F,F,F,F,F,F,F,F,F,FIRE,F,F,F,F,F,F,F,F,F,F,F,F,F),
sw(F,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,F,W,W),
sw(F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,FIRE,FIRE,F,F,EXIT),
wr()]}

L7 = {
"nameVi":"Gọi cứu hộ 114",
"tip":"EXIT bị KHÓA! Dập lửa, qua khói, tìm điện thoại gọi 114 mở EXIT!",
"time":60,"fireSpread":3,"smokeSpread":6,
"map":[
wr(),
sw(PS,F,F,F,F,W,F,F,F,F,F,F,W,F,F,F,F,F,F,F,F,F,F,F),
sw(F,W,W,F,W,F,W,W,W,W,F,W,F,W,W,W,F,W,W,W,W,W,F,F),
sw(F,F,W,F,F,F,F,BCC,F,W,F,F,F,F,F,W,F,F,TWL,F,F,W,F,F),
sw(W,F,W,W,W,W,W,W,F,W,W,W,W,W,F,W,W,W,W,W,F,W,F,F),
sw(F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,W,F,F,F,F),
sw(F,W,W,W,W,W,F,W,W,W,W,W,W,W,W,W,W,W,F,W,W,W,W,W),
sw(F,F,F,F,F,F,F,W,F,F,F,FIRE,F,SMK,SMK,F,F,W,F,F,F,F,F,F),
sw(W,W,W,W,W,W,F,W,F,W,W,W,W,W,W,W,F,W,W,W,W,W,W,F),
sw(F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F),
sw(F,W,W,W,W,W,W,W,W,W,W,F,W,W,W,F,ELEC,ELEC,ELEC,F,W,W,W,F),
sw(F,F,F,F,F,F,F,F,F,F,PHONE,F,F,F,F,F,F,F,BRKR,F,F,F,F,F),
sw(W,W,F,W,W,W,W,W,W,W,W,W,W,F,W,W,W,W,W,F,W,W,W,F),
sw(F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,W,F),
sw(F,W,W,W,W,W,F,W,W,W,W,W,W,W,W,F,W,W,W,W,W,F,W,F),
sw(F,F,F,F,F,F,F,F,F,F,FIRE,F,F,F,F,F,F,F,F,F,F,F,F,F),
sw(W,W,F,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,F),
sw(F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,EXITL,F),
wr()]}

L8 = {
"nameVi":"Kiểm tra cửa!",
"tip":"2 cửa: 1 NÓNG (chết) 1 AN TOÀN. Bấm SPACE kiểm tra! Có lửa + khói + điện!",
"time":60,"fireSpread":3,"smokeSpread":6,
"map":[
wr(),
sw(PS,F,F,F,F,F,W,F,F,F,F,F,F,W,F,F,F,F,F,F,F,F,F,F),
sw(F,W,W,W,W,F,W,F,W,W,W,W,F,W,F,W,W,W,W,F,W,W,F,F),
sw(F,F,F,F,W,F,F,F,F,TWL,F,W,F,F,F,F,BCC,F,W,F,F,W,F,F),
sw(W,W,W,F,W,W,W,W,W,W,W,W,F,W,W,W,W,W,W,W,F,W,F,F),
sw(F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F),
sw(W,W,W,W,W,HDOOR,W,W,W,W,W,W,W,W,W,W,SDOOR,W,W,W,W,W,W,W),
sw(F,F,F,F,F,F,F,F,F,F,W,F,F,F,F,F,F,F,F,F,F,F,F,F),
sw(F,W,W,W,W,W,W,W,W,F,W,F,W,W,W,W,W,W,W,W,W,W,W,F),
sw(F,F,F,F,F,F,F,F,F,F,W,F,F,F,F,F,F,F,F,F,F,F,F,F),
sw(W,W,W,W,F,W,W,W,W,W,W,W,W,W,W,F,ELEC,ELEC,ELEC,W,W,W,W,F),
sw(F,F,F,F,F,F,F,SMK,SMK,SMK,SMK,SMK,SMK,F,F,F,F,BRKR,F,F,F,F,F,F),
sw(F,W,W,W,W,W,F,W,W,W,F,W,W,W,F,W,W,W,W,W,W,W,W,F),
sw(F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F),
sw(W,W,F,W,W,W,W,W,W,W,F,W,W,W,W,W,W,W,W,F,W,W,W,F),
sw(F,F,F,F,F,F,F,F,F,F,F,F,FIRE,F,F,F,F,F,F,F,F,F,F,F),
sw(F,W,W,W,W,W,W,W,W,F,W,W,W,W,W,W,W,W,W,W,W,W,W,F),
sw(F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,FIRE,F,EXIT),
wr()]}

L9 = {
"nameVi":"Giải cứu người bị kẹt",
"tip":"Người bị kẹt sau đồ vật! Dọn đồ (SPACE), dập lửa, qua khói, dẫn người đến EXIT!",
"time":60,"fireSpread":3,"smokeSpread":6,
"map":[
wr(),
sw(PS,F,F,F,F,W,F,F,F,F,F,F,W,F,F,F,F,F,W,F,F,NPC,F,F),
sw(F,W,W,F,W,F,W,W,W,W,F,W,F,W,W,W,F,W,F,W,BLCK,BLCK,W,F),
sw(F,F,W,F,F,F,TWL,F,F,F,F,F,F,F,F,W,F,W,BLCK,W,BLCK,W,BLCK,F),
sw(W,F,W,W,W,F,W,W,W,W,W,W,W,W,F,W,F,W,F,BLCK,BLCK,F,BLCK,F),
sw(BCC,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,W,W,W,W),
sw(W,W,W,W,W,W,F,W,W,W,W,W,W,W,W,W,W,W,W,F,F,F,F,F),
sw(F,F,F,F,F,F,F,W,F,F,F,FIRE,SMK,SMK,F,F,F,W,F,W,W,W,F,F),
sw(F,W,W,W,W,W,F,W,F,W,W,W,W,W,W,W,F,W,F,F,F,F,F,F),
sw(F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,W,W,W,W,W),
sw(W,W,F,W,W,W,W,W,W,W,W,F,W,W,W,W,W,W,F,F,F,F,F,F),
sw(F,F,F,F,F,F,F,SMK,SMK,F,F,F,F,F,F,F,F,F,F,W,W,W,F,F),
sw(F,W,W,W,W,W,W,W,F,W,W,W,W,W,W,W,W,F,BLCK,BLCK,F,F,F,F),
sw(F,F,F,F,F,F,F,F,F,F,F,F,F,FIRE,F,F,BLCK,F,BLCK,F,BLCK,F,W,F),
sw(W,W,F,W,W,W,W,W,W,W,W,W,F,W,W,W,W,F,W,BLCK,W,BLCK,W,F),
sw(F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F),
sw(F,W,W,W,W,W,W,W,F,W,W,W,W,W,W,W,W,W,W,W,W,F,W,W),
sw(F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,FIRE,F,F,EXIT),
wr()]}

L10 = {
"nameVi":"Tổng hợp: Thoát nạn hoàn hảo!",
"tip":"TẤT CẢ kỹ năng! Cầu dao ở sâu bên trong. Ngắt điện > Khóa gas > Dập lửa > Gọi 114 > Cứu người!",
"time":60,"fireSpread":3,"smokeSpread":5,
"map":[
wr(),
sw(PS,F,F,F,F,W,F,F,F,W,F,F,F,TWL,F,W,F,F,F,W,F,NPC,F,F),
sw(F,W,W,F,W,F,W,W,F,W,F,W,W,W,F,W,F,W,F,W,F,BLCK,W,F),
sw(F,F,W,F,F,F,ELEC,ELEC,F,F,F,F,F,F,F,F,F,W,F,KEY,F,W,W,F),
sw(W,F,W,W,W,W,W,W,F,W,W,W,W,W,W,W,F,W,W,W,F,F,F,F),
sw(BCC,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,W,W,W,W),
sw(W,W,F,W,W,W,F,W,F,W,F,F,PHONE,F,W,F,F,F,W,F,F,F,F,F),
sw(F,F,F,F,F,F,F,F,F,F,GASL,GASL,F,W,F,F,F,F,F,F,W,W,W,F),
sw(F,W,W,W,W,W,F,W,F,W,GASL,GASL,F,W,F,FIRE,FIRE,W,F,BLCK,F,F,F,F),
sw(F,F,F,F,F,F,F,F,F,W,W,W,GASV,W,W,F,FIRE,W,F,F,W,W,W,W),
sw(W,W,F,W,W,W,W,W,F,F,F,F,F,F,F,F,F,F,W,F,F,F,F,F),
sw(F,F,F,F,F,SMK,SMK,SMK,SMK,F,W,W,W,W,W,W,W,F,W,F,W,W,W,F),
sw(F,W,F,W,SMK,SMK,SMK,SMK,SMK,F,F,F,F,F,F,F,F,F,F,F,F,DLCK,F,F),
sw(F,W,F,W,W,W,W,W,W,W,W,F,W,W,W,W,W,W,W,W,W,W,W,F),
sw(F,W,F,F,F,F,F,F,BRKR,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F),
sw(F,W,W,W,W,W,F,W,W,W,W,W,W,W,W,F,W,W,W,W,W,W,W,F),
sw(F,F,F,F,F,F,F,F,F,MSK,F,F,F,F,F,F,F,F,F,F,F,F,F,F),
sw(F,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,F,W,W,EXITL,F,F),
wr()]}

L11 = {
"nameVi":"Mê cung khói độc",
"tip":"Mặt nạ chống khí độc là chìa khóa! Tìm MẶT NẠ trước khi qua vùng độc.",
"time":60,"fireSpread":3,"smokeSpread":5,
"map":[
wr(),
sw(PS,F,F,F,F,W,F,F,F,F,F,F,W,F,F,F,F,F,F,F,F,F,F,F),
sw(F,W,W,F,W,F,W,W,W,F,W,F,W,W,W,F,W,W,W,W,W,W,F,F),
sw(F,F,W,F,F,F,F,F,W,F,F,F,W,F,BCC,F,F,F,F,F,F,W,F,F),
sw(W,F,W,W,W,F,W,F,W,W,W,W,W,F,W,W,W,W,W,W,F,W,F,F),
sw(F,F,F,F,W,F,W,F,F,F,F,F,F,F,F,F,TWL,F,F,W,F,F,F,F),
sw(F,W,W,F,W,W,W,W,W,W,W,W,W,W,W,W,W,W,F,W,W,W,W,W),
sw(F,F,W,F,F,F,F,F,F,F,F,FIRE,F,SMK,SMK,F,F,F,F,F,F,F,F,F),
sw(W,F,W,W,W,W,W,W,W,F,W,W,W,W,W,W,W,F,W,W,W,W,W,F),
sw(F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,MSK,F,F),
sw(W,W,W,W,W,F,W,W,W,W,W,W,W,W,W,F,TOX,TOX,TOX,F,W,W,W,F),
sw(F,F,F,F,F,F,F,F,W,F,F,F,F,F,F,F,TOX,TOX,TOX,F,F,F,F,F),
sw(F,W,W,W,W,W,W,F,W,F,W,W,W,W,W,W,W,F,W,W,W,W,W,F),
sw(F,F,F,F,F,F,W,F,F,F,F,F,FIRE,F,F,F,F,F,F,F,F,F,W,F),
sw(W,W,W,W,W,F,W,W,W,W,W,F,W,W,W,W,W,W,W,W,W,F,W,F),
sw(F,F,F,F,F,F,F,F,F,F,F,F,F,F,ELEC,ELEC,ELEC,F,F,F,F,F,F,F),
sw(W,W,F,W,W,W,W,W,W,W,W,W,W,W,W,F,W,W,W,W,W,W,W,F),
sw(F,F,F,F,F,F,F,F,F,F,F,BRKR,F,F,F,F,F,F,FIRE,F,F,F,FIRE,EXIT),
wr()]}

L12 = {
"nameVi":"Công xưởng nguy hiểm",
"tip":"Gas + Điện + Khói + Lửa cùng lúc! Ưu tiên: Ngắt điện > Khóa gas > Dập lửa.",
"time":60,"fireSpread":3,"smokeSpread":5,
"map":[
wr(),
sw(PS,F,F,F,W,F,F,F,F,F,F,W,F,F,F,F,F,W,F,F,F,F,F,F),
sw(F,W,W,F,W,F,W,W,W,W,F,W,F,W,W,W,F,W,F,W,W,W,F,F),
sw(F,F,W,F,F,F,F,F,F,W,F,F,F,F,BCC,F,F,F,TWL,F,F,W,F,F),
sw(W,F,W,W,W,F,W,W,F,W,W,W,W,W,W,W,W,W,W,W,F,W,F,F),
sw(F,F,F,F,W,F,W,F,F,F,F,F,F,F,F,F,F,F,F,W,F,F,F,F),
sw(F,W,W,F,W,W,W,F,ELEC,ELEC,ELEC,ELEC,ELEC,W,W,F,W,W,F,W,W,W,W,W),
sw(F,F,W,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F),
sw(W,F,W,W,W,W,W,W,W,F,W,W,W,W,W,W,W,F,W,W,W,W,W,F),
sw(F,F,F,F,F,F,F,F,F,F,F,F,F,BRKR,F,F,F,F,F,F,F,F,F),
sw(W,W,W,W,W,F,W,GASL,GASL,GASL,W,W,F,W,GASL,GASL,GASL,W,W,F,W,W,W,W),
sw(F,F,F,F,F,F,W,GASL,GASL,GASL,F,F,F,W,GASL,GASL,GASL,F,F,F,F,F,F,F),
sw(F,W,W,W,F,F,W,F,FIRE,FIRE,F,W,F,W,F,FIRE,FIRE,F,W,W,W,F,F,F),
sw(F,F,F,W,F,F,F,W,W,W,F,W,F,W,W,W,F,F,F,F,SMK,SMK,F,F),
sw(W,W,F,W,W,W,W,W,F,W,W,W,W,W,W,W,GASV,W,W,W,SMK,SMK,W,F),
sw(F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F),
sw(F,W,W,W,W,W,W,W,W,F,W,W,W,W,W,F,W,W,W,W,W,W,W,F),
sw(F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,KEY,F,F,F,FIRE,DLCK,F,EXIT),
wr()]}

L13 = {
"nameVi":"Tòa nhà đang cháy",
"tip":"Lửa lan nhanh từ nhiều phía! Dập lửa + Cứu 114 + qua khói + Cứu người.",
"time":60,"fireSpread":3,"smokeSpread":4,
"map":[
wr(),
sw(PS,F,F,F,W,F,F,F,F,F,F,W,F,F,F,F,F,W,F,F,F,NPC,F,F),
sw(F,W,W,F,W,F,W,W,W,W,F,W,F,W,W,W,F,W,F,BLCK,BLCK,BLCK,W,F),
sw(F,F,W,F,F,F,TWL,F,F,W,F,F,F,BCC,F,F,F,F,BLCK,W,BLCK,W,BLCK,F),
sw(W,F,W,W,W,F,W,W,F,W,W,W,W,W,W,W,W,F,F,BLCK,F,BLCK,F,F),
sw(F,F,F,F,W,F,F,F,F,F,ELEC,ELEC,ELEC,F,F,F,W,F,F,F,W,W,W,W),
sw(F,W,W,F,W,W,W,F,W,W,W,W,W,W,W,W,F,W,W,F,F,F,F,W),
sw(F,F,W,F,F,F,F,F,F,FIRE,F,SMK,SMK,SMK,F,FIRE,F,F,F,F,PHONE,F,F,F),
sw(W,F,W,W,W,W,W,W,F,W,W,W,W,W,W,W,F,W,W,W,W,W,W,F),
sw(F,F,F,F,F,F,F,F,F,F,F,F,F,BRKR,F,F,F,F,F,F,F,F,F,F),
sw(W,W,W,W,F,W,GASL,GASL,GASL,W,W,F,W,GASL,GASL,GASL,W,W,F,W,W,W,W,F),
sw(F,F,F,F,F,W,GASL,GASL,GASL,F,F,F,W,GASL,GASL,GASL,F,F,F,F,F,F,F,F),
sw(F,W,W,W,F,W,F,FIRE,FIRE,F,W,F,W,F,FIRE,FIRE,F,W,W,W,F,GASV,F,F),
sw(F,F,F,W,F,F,W,W,W,F,W,F,W,W,W,F,F,F,F,F,F,F,F,F),
sw(W,W,F,W,W,W,W,F,W,W,W,W,W,W,W,F,W,W,W,W,W,W,W,F),
sw(F,F,F,F,F,F,F,F,F,F,FIRE,F,F,F,F,F,ELEC,ELEC,ELEC,F,F,F,F,F),
sw(F,W,W,W,W,W,W,W,W,F,W,W,W,W,W,F,W,BRKR,W,W,W,W,W,F),
sw(F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,FIRE,EXITL,F,F),
wr()]}

L14 = {
"nameVi":"Khu phức hợp nguy cấp",
"tip":"Hai tầng nguy hiểm! Ngắt điện tầng trên, khóa gas tầng dưới, gọi 114 mở EXIT.",
"time":60,"fireSpread":3,"smokeSpread":4,
"map":[
wr(),
sw(PS,F,F,F,W,F,F,F,F,W,F,F,F,TWL,F,W,F,F,F,W,F,F,F,F),
sw(F,W,W,F,W,F,W,W,F,W,F,W,W,W,F,W,F,W,F,W,F,W,W,F),
sw(F,F,W,F,F,ELEC,ELEC,ELEC,F,F,BCC,F,F,F,F,F,F,W,F,KEY,F,F,W,F),
sw(W,F,W,W,W,W,W,W,F,W,W,W,W,W,W,W,F,W,W,W,F,F,F,F),
sw(F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,BRKR,F,F,F,F,W,W,W,W),
sw(W,W,F,W,W,W,F,W,F,W,F,FIRE,SMK,SMK,W,F,PHONE,F,W,F,F,NPC,F,W),
sw(F,F,F,F,F,F,F,F,F,F,FIRE,F,SMK,SMK,F,F,F,F,F,F,BLCK,BLCK,F,F),
sw(F,W,W,W,W,W,F,W,F,W,W,W,W,W,W,W,F,W,W,BLCK,W,BLCK,W,F),
sw(F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,BLCK,F,BLCK,F,BLCK,F),
sw(W,W,W,W,F,W,GASL,GASL,GASL,W,W,F,W,GASL,GASL,GASL,W,W,F,W,W,W,W,F),
sw(F,F,F,F,F,W,GASL,GASL,GASL,F,F,F,W,GASL,GASL,GASL,F,F,F,F,F,F,F,F),
sw(F,W,W,W,F,W,F,FIRE,FIRE,F,W,F,W,F,FIRE,FIRE,F,W,W,F,GASV,F,F,F),
sw(F,F,F,W,F,F,W,W,W,F,W,F,W,W,W,F,F,F,F,F,F,F,F,F),
sw(W,W,F,W,W,W,W,F,W,W,W,W,W,W,W,F,W,W,W,W,W,W,W,F),
sw(F,F,F,F,F,F,F,F,F,FIRE,F,F,F,F,ELEC,ELEC,ELEC,F,F,F,F,F,F,F),
sw(F,W,W,W,W,W,W,W,W,F,W,W,W,W,W,F,W,BRKR,W,W,W,W,W,F),
sw(F,F,F,F,F,F,F,F,F,F,F,DLCK,F,F,F,F,F,F,F,F,FIRE,EXITL,MSK,F),
wr()]}

L15 = {
"nameVi":"Thảm họa tổng lực - Màn cuối!",
"tip":"Màn cuối khó nhất! Tất cả mọi nguy hiểm đồng thời. Bình tĩnh, lên kế hoạch!",
"time":60,"fireSpread":2,"smokeSpread":3,
"map":[
wr(),
sw(PS,F,F,F,W,F,F,F,W,F,F,F,TWL,F,W,F,F,F,W,F,NPC,F,F,F),
sw(F,W,W,F,W,F,W,W,F,W,F,W,W,F,W,F,W,W,F,W,BLCK,W,BLCK,F),
sw(F,F,W,F,F,ELEC,ELEC,F,F,BCC,F,F,F,F,F,F,W,F,KEY,F,BLCK,F,BLCK,F),
sw(W,F,W,W,W,W,W,F,W,W,W,W,W,W,W,F,W,W,W,F,BLCK,BLCK,F,F),
sw(F,F,F,F,W,F,F,F,F,F,F,F,F,F,BRKR,F,F,F,F,W,W,W,W,F),
sw(W,W,F,W,W,W,F,W,F,W,F,FIRE,SMK,SMK,W,F,PHONE,F,W,F,F,F,F,W),
sw(F,F,F,F,F,F,F,F,F,FIRE,FIRE,F,SMK,SMK,F,F,F,F,F,F,W,W,W,F),
sw(F,W,W,W,W,W,F,W,F,W,W,W,W,W,W,W,F,W,W,F,F,F,F,F),
sw(F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,W,W,W,W,W),
sw(W,W,W,W,F,GASL,GASL,GASL,W,W,F,W,GASL,GASL,GASL,W,W,F,W,F,F,F,F,F),
sw(F,F,F,F,F,GASL,GASL,GASL,F,F,F,W,GASL,GASL,GASL,F,F,F,W,F,W,W,W,F),
sw(F,W,W,W,F,F,FIRE,FIRE,F,W,F,W,F,FIRE,FIRE,F,W,W,F,F,GASV,F,F,F),
sw(F,F,F,W,F,F,W,W,F,W,F,W,W,W,F,F,F,F,F,F,F,F,F,F),
sw(W,W,F,W,W,W,W,F,W,W,W,W,W,W,W,F,TOX,TOX,F,W,W,W,W,F),
sw(F,F,F,F,F,F,F,FIRE,F,F,F,F,F,ELEC,ELEC,F,TOX,TOX,F,F,F,F,F,F),
sw(F,W,W,W,W,W,W,W,W,F,W,W,W,W,W,F,W,BRKR,W,W,W,W,W,F),
sw(F,F,F,F,F,F,F,F,F,F,F,DLCK,F,F,F,F,F,F,F,FIRE,FIRE,EXITL,MSK,F),
wr()]}

import json
all_levels = [L1,L2,L3,L4,L5,L6,L7,L8,L9,L10,L11,L12,L13,L14,L15]
out = "window.GAME_LEVELS = [\n"
for i,lv in enumerate(all_levels):
    rows = []
    for row in lv["map"]:
        rows.append("      ["+",".join(str(x) for x in row)+"]")
    out += "  {\n"
    out += "    nameVi: "+json.dumps(lv["nameVi"],ensure_ascii=False)+",\n"
    out += "    tip: "+json.dumps(lv["tip"],ensure_ascii=False)+",\n"
    out += "    time: "+str(lv["time"])+", fireSpread: "+str(lv["fireSpread"])+", smokeSpread: "+str(lv.get("smokeSpread",0))+",\n"
    out += "    map: [\n"
    out += ",\n".join(rows)+"\n"
    out += "    ]\n"
    out += "  }"
    if i < len(all_levels)-1: out += ","
    out += "\n"
out += "];\n"

path = r"c:\Users\Hasky\.gemini\antigravity\scratch\fras\frontend\js\game-levels.js"
with open(path,"w",encoding="utf-8") as f:
    f.write(out)
print("Done! "+str(len(all_levels))+" levels written.")
