# Tile constants
F,W,FIRE,SMK,EXIT,BCC,TWL,MSK,KEY = 0,1,2,3,4,5,6,7,8
DLCK,TOX,PS,FUR,ELEC,BRKR,GASL,GASV,PHONE = 9,10,11,12,13,14,15,16,17
HDOOR,SDOOR,NPC,BLCK,EXITL = 18,19,20,21,22

def wr(): return [W]*25  # full wall row
def sw(*m): return [W]+list(m)+[W]  # side-walled row (23 middle items)

# We will construct tight corridors where obstacles stretch across the WHOLE playable width,
# forcing the player to interact with them. For 25 tile width, if corridor is 3 tiles wide, 
# it should be 10 W, 3 path, 10 W.

def path_w(w1_count, items, w2_count):
    return [W]*w1_count + items + [W]*w2_count

L1 = {
"nameVi":"Bài học đầu tiên: Bình chữa cháy",
"tip":"Tìm BCC dập lửa chặn đường. Lửa lan nhanh!",
"time":60,"fireSpread":3,"smokeSpread":8,
"map":[
wr(),
path_w(1, [PS,F,BCC,F,W,F,F,F,F,F,F,W,F], 11),
path_w(1, [W,W,F,W,W,F,W,W,W,F,W,F,W], 11),
path_w(1, [F,F,F,F,F,F,F,F,W,F,F,F,W], 11),
path_w(1, [F,W,W,W,W,F,W,F,W,W,W,F,W], 11),
path_w(1, [F,F,F,F,W,F,W,F,F,F,F,F,F], 11),
path_w(1, [F,W,W,F,W,F,W,W,W,W,W,W,W,W,F,W,W,F,W,W,W,F], 1),
path_w(1, [F,F,W,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,W,F,F,F], 1),
path_w(1, [W,F,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,F,W,W,W,W], 1),
path_w(1, [W,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,W,F,F,F,F,F], 1),
path_w(1, [W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,FIRE,W,W,W,W,W,F], 1),
path_w(1, [F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F], 1),
path_w(1, [F,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,F], 1),
path_w(1, [F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F], 1),
path_w(1, [F,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W], 1),
path_w(1, [F,FIRE,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W], 1),
path_w(1, [F,F,W,W,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F], 1),
path_w(1, [W,F,F,F,F,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,EXIT], 1),
wr()]}

L2 = {
"nameVi":"Hành lang khói",
"tip":"Lấy KHĂN ƯỚT qua khói. Khăn chỉ dùng 10s trong khói!",
"time":60,"fireSpread":3,"smokeSpread":6,
"map":[
wr(),
path_w(1, [PS,F,TWL,F], 19),
path_w(1, [F,W,W,W], 19),
path_w(1, [F,F,F,W], 19),
path_w(1, [W,W,F,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W], 1),
path_w(1, [F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F], 1),
path_w(1, [F,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,F], 1),
path_w(1, [F,W,W,W,W,F,F,BCC,F,F,W,W,SMK,SMK,SMK,W,W,F,F,F,W,F], 1),
path_w(1, [F,SMK,SMK,W,W,W,W,W,W,W,W,W,SMK,SMK,SMK,W,W,W,W,F,W,F], 1),
path_w(1, [F,SMK,SMK,W,W,F,F,F,F,F,F,F,SMK,SMK,SMK,W,W,W,W,F,W,F], 1),
path_w(1, [F,SMK,SMK,W,W,F,W,W,W,W,W,W,W,W,W,W,W,W,W,F,W,F], 1),
path_w(1, [F,W,W,W,W,F,W,W,W,W,W,W,W,W,W,W,W,W,W,F,W,F], 1),
path_w(1, [F,F,F,F,W,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,W,F], 1),
path_w(1, [W,W,W,F,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,F], 1),
path_w(1, [W,W,W,F,W,W,W,W,W,W,W,FIRE,FIRE,FIRE,W,W,W,W,W,W,W,F], 1),
path_w(1, [W,W,W,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F], 1),
path_w(1, [W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W], 1),
path_w(1, [W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,EXIT], 1),
wr()]}

L3 = {
"nameVi":"Mê cung chìa khóa",
"tip":"BCC dập lửa, lấy CHÌA KHÓA mở cửa khóa. Khói lan rộng!",
"time":60,"fireSpread":3,"smokeSpread":6,
"map":[
wr(),
path_w(1, [PS,F,TWL,F], 19),
path_w(1, [F,W,W,W], 19),
path_w(1, [F,F,BCC,W], 19),
path_w(1, [W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W], 1),
path_w(1, [F,F,F,F,F,F,F,F,W,F,F,F,F,F,F,F,F,F,F,F,F,F], 1),
path_w(1, [FIRE,W,W,W,W,W,W,F,W,F,W,W,W,W,W,W,W,W,W,W,W,F], 1),
path_w(1, [F,W,W,W,W,W,W,F,W,F,W,W,F,F,F,KEY,F,F,W,W,W,F], 1),
path_w(1, [F,F,F,F,F,F,F,F,W,F,W,W,F,W,W,W,W,W,W,W,W,F], 1),
path_w(1, [W,W,W,W,W,W,W,W,W,F,W,W,F,W,W,W,W,W,W,W,W,F], 1),
path_w(1, [W,F,F,F,F,F,SMK,SMK,F,F,W,W,F,W,W,W,W,W,W,W,W,F], 1),
path_w(1, [W,F,W,W,W,W,W,W,W,W,W,W,F,W,W,W,W,W,W,W,W,F], 1),
path_w(1, [W,F,F,F,F,F,F,F,F,F,F,F,F,W,W,W,W,W,W,W,W,F], 1),
path_w(1, [W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,F], 1),
path_w(1, [W,W,W,W,W,W,W,W,W,W,W,W,FIRE,FIRE,FIRE,W,W,W,W,W,W,F], 1),
path_w(1, [W,W,W,W,W,W,W,W,W,W,W,W,F,F,F,W,W,W,W,W,W,F], 1),
path_w(1, [W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W], 1),
path_w(1, [W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,DLCK,EXIT], 1),
wr()]}

L4 = {
"nameVi":"An toàn điện - Cầu dao ở xa",
"tip":"Dây điện chặn đường! Tìm CẦU DAO tận cuối, bấm SPACE ngắt điện!",
"time":60,"fireSpread":3,"smokeSpread":6,
"map":[
wr(),
path_w(1, [PS,F,TWL,F], 19),
path_w(1, [F,W,W,W], 19),
path_w(1, [F,F,BCC,W], 19),
path_w(1, [W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W], 1),
path_w(1, [F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F], 1),
path_w(1, [F,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W], 1),
path_w(1, [F,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W], 1),
path_w(1, [F,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W], 1),
path_w(1, [ELEC,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W], 1),
path_w(1, [F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F], 1),
path_w(1, [W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,F], 1),
path_w(1, [W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,F], 1),
path_w(1, [W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,F], 1),
path_w(1, [W,W,W,W,W,W,W,W,FIRE,W,W,W,W,W,W,W,W,W,W,W,W,F], 1),
path_w(1, [W,W,W,W,W,W,W,W,F,W,W,W,W,W,W,W,W,W,W,W,W,F], 1),
path_w(1, [W,F,F,F,F,BRKR,W,W,F,W,W,W,W,W,W,W,W,W,W,W,W,F], 1),
path_w(1, [W,W,W,W,W,W,W,W,F,F,F,F,F,F,F,F,F,F,F,F,F,EXIT], 1),
wr()]}

L5 = {
"nameVi":"Rò rỉ gas nguy hiểm",
"tip":"Gas rò! Tìm VAN GAS khóa lại TRƯỚC khi dập lửa!",
"time":60,"fireSpread":3,"smokeSpread":6,
"map":[
wr(),
path_w(1, [PS,F,TWL,F], 19),
path_w(1, [F,W,W,W], 19),
path_w(1, [F,F,BCC,W], 19),
path_w(1, [W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W], 1),
path_w(1, [F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F], 1),
path_w(1, [F,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,F], 1),
path_w(1, [F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,W,W,F], 1),
path_w(1, [W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,F,W,W,F], 1),
path_w(1, [GASL,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,F,W,W,F], 1),
path_w(1, [F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,W,F,W,W,F], 1),
path_w(1, [W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,F,W,F,W,W,F], 1),
path_w(1, [W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,F,W,F,F,F,F], 1),
path_w(1, [W,W,W,W,W,W,W,W,FIRE,FIRE,FIRE,W,W,W,W,W,F,W,W,W,W,W], 1),
path_w(1, [W,W,W,W,W,W,W,W,F,F,F,W,W,W,W,W,F,W,W,W,W,W], 1),
path_w(1, [W,GASV,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F], 1),
path_w(1, [W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,EXIT], 1),
wr()]}

L6 = {
"nameVi":"Bóng tối trong khói",
"tip":"Lửa chặn EXIT! Lấy khăn ướt, dập lửa sát nút!",
"time":60,"fireSpread":3,"smokeSpread":5,
"map":[
wr(),
path_w(1, [PS,F,F,F,W,F,F,F,TWL,W], 13),
path_w(1, [W,W,W,F,W,F,W,W,W,W], 13),
path_w(1, [F,F,F,F,F,F,F,F,F,W], 13),
path_w(1, [F,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W], 1),
path_w(1, [F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,BCC,F], 1),
path_w(1, [W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,F], 1),
path_w(1, [W,SMK,SMK,SMK,SMK,SMK,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,F], 1),
path_w(1, [W,F,F,F,F,F,SMK,W,W,W,W,W,W,W,W,W,W,W,W,W,W,F], 1),
path_w(1, [W,F,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,F], 1),
path_w(1, [W,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F], 1),
path_w(1, [W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W], 1),
path_w(1, [W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W], 1),
path_w(1, [W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W], 1),
path_w(1, [W,W,W,W,W,W,W,W,W,W,W,FIRE,W,W,W,W,W,W,W,W,W,W], 1),
path_w(1, [W,W,W,W,W,W,W,W,W,W,W,F,W,W,W,W,W,W,W,W,W,W], 1),
path_w(1, [W,W,W,W,W,W,W,W,W,W,W,F,F,F,F,F,F,F,F,F,F,EXIT], 1),
wr()]}

L7 = {
"nameVi":"Gọi cứu hộ 114",
"tip":"Gọi 114 bằng ĐIỆN THOẠI để mở EXITL (Cửa khóa tự động)!",
"time":60,"fireSpread":3,"smokeSpread":5,
"map":[
wr(),
path_w(1, [PS,F,TWL,W], 19),
path_w(1, [F,W,W,W], 19),
path_w(1, [F,F,BCC,W], 19),
path_w(1, [W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W], 1),
path_w(1, [W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W], 1),
path_w(1, [FIRE,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W], 1),
path_w(1, [F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,SMK,SMK,F,F], 1),
path_w(1, [W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,F], 1),
path_w(1, [ELEC,F,F,F,BRKR,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,F], 1),
path_w(1, [W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,F], 1),
path_w(1, [W,PHONE,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F], 1),
path_w(1, [W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W], 1),
path_w(1, [W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W], 1),
path_w(1, [W,W,W,W,W,W,W,W,W,W,W,FIRE,W,W,W,W,W,W,W,W,W,W], 1),
path_w(1, [W,W,W,W,W,W,W,W,W,W,W,F,W,W,W,W,W,W,W,W,W,W], 1),
path_w(1, [W,W,W,W,W,W,W,W,W,W,W,F,F,F,F,F,F,F,F,F,F,EXITL], 1),
wr()]}

L8 = {
"nameVi":"Kiểm tra cửa!",
"tip":"2 cửa: 1 NÓNG (chết) 1 AN TOÀN. Kiểm tra khôn ngoan!",
"time":60,"fireSpread":3,"smokeSpread":5,
"map":[
wr(),
path_w(1, [PS,F,TWL,W], 19),
path_w(1, [F,W,W,W], 19),
path_w(1, [F,F,BCC,W], 19),
path_w(1, [W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W], 1),
path_w(1, [W,W,W,W,HDOOR,W,W,W,W,W,W,W,W,SDOOR,W,W,W,W,W,W,W,W], 1),
path_w(1, [W,F,F,F,F,F,W,W,W,W,W,W,W,F,F,F,F,W,W,W,W,W], 1),
path_w(1, [W,ELEC,W,W,W,W,W,W,W,W,W,W,W,W,W,W,F,W,W,W,W,W], 1),
path_w(1, [W,F,F,F,F,F,F,F,F,F,F,BRKR,W,W,W,W,F,W,W,W,W,W], 1),
path_w(1, [W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,F,W,W,W,W,W], 1),
path_w(1, [W,W,W,W,W,W,W,W,FIRE,W,W,W,W,W,W,W,F,W,W,W,W,W], 1),
path_w(1, [W,W,W,W,W,W,W,W,F,F,F,W,W,W,W,W,F,W,W,W,W,W], 1),
path_w(1, [W,W,W,W,W,W,W,W,W,W,F,W,W,W,W,W,F,W,W,W,W,W], 1),
path_w(1, [W,W,W,W,W,W,W,W,W,W,F,W,W,W,W,W,F,W,W,W,W,W], 1),
path_w(1, [W,W,W,W,W,W,W,W,W,W,SMK,SMK,F,F,F,F,F,W,W,W,W,W], 1),
path_w(1, [W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W], 1),
path_w(1, [W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,F,EXIT], 1),
wr()]}

L9 = {
"nameVi":"Giải cứu người bị kẹt",
"tip":"Dọn đồ (SPACE), dập lửa, qua khói, dẫn người đến EXIT!",
"time":60,"fireSpread":3,"smokeSpread":5,
"map":[
wr(),
path_w(1, [PS,F,TWL,F], 19),
path_w(1, [F,W,W,W], 19),
path_w(1, [F,F,BCC,W], 19),
path_w(1, [W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W], 1),
path_w(1, [F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F], 1),
path_w(1, [W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,F], 1),
path_w(1, [W,NPC,BLCK,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,W,F], 1),
path_w(1, [W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,F,F,F,W,F], 1),
path_w(1, [W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,FIRE,W,W,W,F], 1),
path_w(1, [W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,F,W,W,W,F], 1),
path_w(1, [W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,F,W,W,W,F], 1),
path_w(1, [W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,BLCK,W,W,W,F], 1),
path_w(1, [W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,F,W,W,W,F], 1),
path_w(1, [W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,F,F,F,F,F], 1),
path_w(1, [W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W], 1),
path_w(1, [W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,F,EXIT], 1),
wr()]}

L10 = {
"nameVi":"Tổng hợp 1",
"tip":"Mọi nguy hiểm trộn lẫn!",
"time":60,"fireSpread":3,"smokeSpread":5,
"map":[
wr(),
path_w(1, [PS,F,TWL,W], 19),
path_w(1, [F,W,W,W], 19),
path_w(1, [F,F,BCC,W], 19),
path_w(1, [W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W], 1),
path_w(1, [W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W], 1),
path_w(1, [W,GASL,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W], 1),
path_w(1, [ELEC,F,F,F,BRKR,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W], 1),
path_w(1, [W,GASV,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W], 1),
path_w(1, [W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W], 1),
path_w(1, [W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W], 1),
path_w(1, [W,W,W,W,W,W,W,W,W,W,W,FIRE,W,W,W,W,W,W,W,W,W,W], 1),
path_w(1, [W,W,W,W,W,W,W,W,W,W,W,F,F,BLCK,F,F,W,W,W,W,W,W], 1),
path_w(1, [W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,F,W,W,W,W,W,W], 1),
path_w(1, [W,W,W,W,W,W,W,W,W,W,W,W,W,W,KEY,F,W,W,W,W,W,W], 1),
path_w(1, [W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W], 1),
path_w(1, [W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,DLCK,EXIT], 1),
wr()]}

L11 = {
"nameVi":"Mê cung khói độc",
"tip":"Mặt nạ chống khí độc là chìa khóa! Tìm MẶT NẠ trước khi qua vùng độc.",
"time":60,"fireSpread":3,"smokeSpread":5,
"map":[
wr(),
path_w(1, [PS,F,TWL,W], 19),
path_w(1, [F,W,W,W], 19),
path_w(1, [F,F,BCC,W], 19),
path_w(1, [W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W], 1),
path_w(1, [F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,MSK], 1),
path_w(1, [F,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W], 1),
path_w(1, [F,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W], 1),
path_w(1, [TOX,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W], 1),
path_w(1, [F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F], 1),
path_w(1, [W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,F], 1),
path_w(1, [W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,F], 1),
path_w(1, [W,W,W,W,W,W,W,W,FIRE,W,W,W,W,W,W,W,W,W,W,W,W,F], 1),
path_w(1, [W,W,W,W,W,W,W,W,F,W,W,W,W,W,W,W,W,W,W,W,W,F], 1),
path_w(1, [W,W,W,W,W,W,W,W,F,F,F,F,F,F,F,F,F,F,F,F,F,F], 1),
path_w(1, [W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W], 1),
path_w(1, [W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,F,EXIT], 1),
wr()]}

# Map 12 to 15 logic just duplicate tight halls logic
L12 = L10.copy(); L12["nameVi"] = "Công xưởng nguy hiểm"
L13 = L10.copy(); L13["nameVi"] = "Tòa nhà đang cháy"
L14 = L10.copy(); L14["nameVi"] = "Khu phức hợp nguy cấp"
L15 = L10.copy(); L15["nameVi"] = "Thảm họa tổng lực - Màn cuối!"

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
print("Done! "+str(len(all_levels))+" levels written cleanly.")
