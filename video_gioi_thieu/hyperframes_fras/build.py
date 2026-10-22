"""Sinh index.html của video giới thiệu FRAS-AI cho HyperFrames.
Chạy: python build.py  ->  fras-video/index.html
Mốc thời gian từng cảnh lấy từ khoảng lặng của file giọng đọc (đã dò bằng ffmpeg silencedetect).
"""
import json
import re

HERE = r"D:\Antigravity\scratch\fras-ai\video_gioi_thieu"
OUT = HERE + r"\hyperframes_fras\fras-video\index.html"
TOTAL = 276.1

# (bắt đầu giọng, kết thúc giọng) của 16 cảnh
T = [(0.0, 10.6), (11.58, 26.57), (27.56, 45.81), (46.79, 63.81), (64.78, 84.77), (85.76, 106.66), (107.66, 123.51),
     (124.5, 134.04), (135.03, 148.64), (149.64, 164.19), (165.18, 180.31), (181.28, 198.94), (199.93, 227.23),
     (228.2, 253.23), (254.2, 265.35), (266.34, 276.1)]

scenes = json.load(open(HERE + r"\full\script.json", encoding="utf-8"))["scenes"]


def clean(s):
    s = re.sub(r"[Tt]ruy cập [Pp]hờ rát gạch [Ââ]y ai chấm com", "Truy cập fras-ai.com", s)
    s = s.replace("Hệ thống Phờ rát, ây ai", "Hệ thống FRAS-AI").replace("Phờ rát, ây ai", "FRAS-AI")
    s = re.sub(r"phờ rát gạch ây ai chấm com", "fras-ai.com", s, flags=re.I)
    return s


def chunks(text, maxlen=92):
    parts = re.split(r"(?<=[.:;?!])\s+", text)
    out = []
    for p in parts:
        p = p.strip()
        while len(p) > maxlen:
            cut = p.rfind(",", 0, maxlen)
            if cut < 30:
                cut = p.rfind(" ", 0, maxlen)
            out.append(p[:cut + 1].strip())
            p = p[cut + 1:].strip()
        if p:
            out.append(p)
    # gộp mảnh quá ngắn
    merged = []
    for c in out:
        if merged and (len(merged[-1]) < 32 or len(c) < 22) and len(merged[-1]) + len(c) < maxlen + 12:
            merged[-1] += " " + c
        else:
            merged.append(c)
    return merged


# ------------------------------------------------------------------ phần dựng từng cảnh
def phone(shots, cls="", style=""):
    """Khung điện thoại; shots: list (ảnh, y_bắt_đầu, y_kết_thúc) đổi ảnh dần theo thời gian của cảnh."""
    imgs = "".join(f'<img class="shot" src="assets/shots/{s}" data-y0="{a}" data-y1="{b}">' for s, a, b in shots)
    return f'<div class="phone {cls}" style="{style}"><div class="notch"></div><div class="screen">{imgs}</div></div>'


def card(icon, title, sub="", style="", cls=""):
    return (f'<div class="card {cls}" data-a style="{style}"><div class="ic">{icon}</div>'
            f'<div class="tx">{title}<small>{sub}</small></div></div>')


def head(eyebrow, title):
    return f'<div class="eyebrow" data-a>{eyebrow}</div><h2 data-a>{title}</h2>'


BODY = {}

# ---- 1 mở đầu
BODY[1] = '''
<div class="night"></div>
<svg class="house" viewBox="0 0 400 300" data-a="fade" style="left:210px;top:380px;width:640px;height:480px">
  <polygon points="40,150 200,40 360,150" fill="#13294f" stroke="#2c4a82" stroke-width="3"/>
  <rect x="70" y="150" width="260" height="130" fill="#10224a" stroke="#2c4a82" stroke-width="3"/>
  <rect x="110" y="185" width="60" height="55" fill="#C9962C" class="win"/>
  <rect x="230" y="185" width="60" height="55" fill="#2a3f6e"/>
  <rect x="180" y="215" width="40" height="65" fill="#0a1530"/>
</svg>
<div class="smoke" style="left:380px;top:150px"></div><div class="smoke s2" style="left:430px;top:190px"></div><div class="smoke s3" style="left:340px;top:230px"></div>
<div class="bigq" data-a style="left:80px;top:150px;width:1220px">Nếu ngay lúc này nhà bạn bốc khói,<br><span style="color:var(--gold)">bạn sẽ làm gì trong những phút đầu tiên?</span></div>
<div class="bigsub" data-a="late" style="left:80px;top:330px;width:1120px">Việc chuẩn bị chỉ cần vài chục phút,<br>ngay trên chiếc điện thoại của bạn.</div>
''' + phone([("home_0.png", 0, 0)], "", "left:1400px;top:104px")

# ---- 2 giới thiệu
BODY[2] = '''
<img class="logo" data-a="fade" src="assets/logo.png" style="left:90px;top:170px;width:200px;height:200px">
<div class="eyebrow" data-a style="left:330px;top:180px">CÔNG AN THÀNH PHỐ BẮC NINH GIỚI THIỆU</div>
<div class="gold" data-a style="left:330px;top:225px;font-size:150px">FRAS-AI</div>
<div class="bigsub" data-a style="left:330px;top:405px;width:1000px;font-size:42px">Ứng dụng trí tuệ nhân tạo trong khảo sát, đánh giá, cảnh báo và tự khắc phục nguy cơ cháy, nổ</div>
''' + card("📋", "1. Khảo sát nguy cơ", "từng bước, ngay trên điện thoại", "left:90px;top:610px;width:600px") \
    + card("💬", "2. Trợ lý ảo", "giải đáp pháp luật PCCC", "left:720px;top:610px;width:600px") \
    + card("🎓", "3. Học liệu số", "khóa học trực tuyến", "left:90px;top:790px;width:600px;height:150px") \
    + card("🎮", "4. Trò chơi PCCC", "học mà chơi, chơi mà học", "left:720px;top:790px;width:600px;height:150px") \
    + phone([("home_0.png", 0, 0), ("home_1.png", 0, 0)], "", "left:1400px;top:104px")

# ---- 3 bước 1
BODY[3] = head("PHẦN 1 · KHẢO SÁT NGUY CƠ", "Bước 1: mở điện thoại, vào fras-ai.com") + '''
<div class="chip" data-a style="left:90px;top:420px;background:#1A3A6B">🏠 Nhà ở</div>
<div class="chip" data-a style="left:420px;top:420px;background:#1A3A6B">🏪 Cửa hàng</div>
<div class="chip" data-a style="left:750px;top:420px;background:#1A3A6B">🏭 Nhà xưởng</div>
<div class="urlbar" data-a style="left:90px;top:560px"><span>🔒</span> fras-ai.com</div>
<div class="btnred" data-a style="left:90px;top:690px">BẮT ĐẦU KHẢO SÁT →</div>
<div class="tag" data-a style="left:90px;top:810px">Không cần cài đặt bất kỳ phần mềm nào</div>
''' + phone([("home_0.png", 0, 0), ("survey_0.png", 0, 0)], "", "left:1400px;top:104px")

# ---- 4 bước 2
BODY[4] = head("BƯỚC 2 · CHỌN ĐỐI TƯỢNG", "Bạn là cơ sở quản lý, hay hộ gia đình?") \
    + card("🏢", "Cơ sở thuộc diện quản lý PCCC", "Nhập mã cơ sở 13 chữ số và mật khẩu do cơ quan Công an cung cấp", "left:90px;top:400px;width:1180px;height:210px") \
    + card("🏠", "Hộ gia đình, nhà ở riêng lẻ, cửa hàng nhỏ", "Vào khảo sát ngay, không cần tạo tài khoản", "left:90px;top:650px;width:1180px;height:210px", "alt") \
    + phone([("home_modal.png", 0, 0)], "", "left:1400px;top:104px")

# ---- 5 bước 3
BODY[5] = head("BƯỚC 3 · KHAI THÔNG TIN CƠ SỞ", "Chọn đúng loại hình hoạt động") + '''
<div class="grid2" style="left:90px;top:410px">
  <div class="chip2" data-a>🏠 Nhà ở kết hợp kinh doanh</div><div class="chip2" data-a>🍽️ Nhà hàng, khách sạn</div>
  <div class="chip2" data-a>📦 Kho hàng</div><div class="chip2" data-a>🏫 Trường học</div>
  <div class="chip2" data-a>⛽ Cửa hàng xăng dầu</div><div class="chip2" data-a>🏭 Cơ sở sản xuất</div>
</div>
<div class="tag" data-a style="left:90px;top:720px">Mỗi loại hình có một bộ câu hỏi riêng · chọn được nhiều loại hình</div>
<div class="map" data-a style="left:90px;top:800px"><span class="pin">📍</span> Lấy vị trí hiện tại, để biết khoảng cách tới trụ nước chữa cháy gần nhất <b>(không bắt buộc)</b></div>
''' + phone([("survey_1.png", 0, 0)], "", "left:1400px;top:104px")

# ---- 6 bước 4
BODY[6] = head("BƯỚC 4 · TRẢ LỜI CÁC CÂU HỎI", "Câu hỏi chia theo từng nhóm") + '''
<div class="grid2 sm" style="left:90px;top:400px">
  <div class="chip2" data-a>⚡ Hệ thống điện</div><div class="chip2" data-a>🔥 Nguồn lửa, nguồn nhiệt</div>
  <div class="chip2" data-a>🚪 Lối thoát nạn, trang bị chữa cháy</div><div class="chip2" data-a>⚙️ Máy móc, thiết bị</div>
  <div class="chip2" data-a>🌦️ Yếu tố tự nhiên</div><div class="chip2" data-a>🚗 Phương tiện giao thông</div>
  <div class="chip2 wide" data-a>🎯 Nhóm câu hỏi đặc thù theo loại hình của bạn</div>
</div>
<div class="tag red" data-a style="left:90px;top:790px">Mỗi câu chọn 1 trong 4 đáp án, từ an toàn đến cần lưu ý</div>
''' + phone([("survey_q1.png", 0, 0)], "", "left:1400px;top:104px")

# ---- 7 ba điều cần nhớ
BODY[7] = head("LƯU Ý KHI TRẢ LỜI", "Ba điều cần nhớ") \
    + card("1", "Trả lời đúng thực tế", "Đây là công cụ giúp chính bạn, không phải bài kiểm tra", "left:90px;top:380px;width:1240px;height:150px", "num") \
    + card("2", "Có thể bấm Quay lại để sửa", "Hệ thống tự lưu nháp, không lo mất dữ liệu khi bị gián đoạn", "left:90px;top:570px;width:1240px;height:150px", "num") \
    + card("3", "Chỉ mất khoảng 10 đến 15 phút", "Ngắn gọn, dễ làm, làm lúc nào cũng được", "left:90px;top:760px;width:1240px;height:150px", "num") \
    + phone([("survey_q1.png", 0, 0)], "", "left:1400px;top:104px")

# ---- 8 gửi
BODY[8] = head("BƯỚC 5 · KIỂM TRA LẠI VÀ GỬI", "Xem lại một lượt, rồi bấm Gửi đánh giá") + '''
<div class="btnred" data-a style="left:90px;top:440px;width:560px;font-size:40px">GỬI ĐÁNH GIÁ</div>
<div class="spin" data-a="late" style="left:700px;top:430px"></div>
<div class="done" data-a="later" style="left:700px;top:430px">✓</div>
<div class="bigsub" data-a="later" style="left:90px;top:620px;width:1100px;font-size:46px">Chỉ sau ít phút, kết quả sẽ hiện ra</div>
''' + phone([("survey_q1.png", 0, 0), ("result_0.png", 0, 0)], "", "left:1400px;top:104px")

# ---- 9 kết quả
BODY[9] = head("TRANG KẾT QUẢ", "Mức nguy cơ hiện ra ngay") + '''
<div class="levels" data-a style="left:90px;top:400px">
  <span style="background:#16A34A">THẤP</span><span style="background:#B45309">TRUNG BÌNH</span><span style="background:#EA580C">CAO</span><span style="background:#DC2626">RẤT CAO</span>
</div>
<div class="tag" data-a style="left:90px;top:520px">Điểm số từng nhóm và biểu đồ trực quan</div>
<div class="tag red" data-a style="left:90px;top:630px">Chỉ một nguy cơ đặc biệt cũng nâng mức chung, để không chủ quan</div>
<div class="tag" data-a style="left:90px;top:740px">📄 Xuất file PDF, in biên bản để lưu hồ sơ</div>
''' + phone([("result_0.png", 0, 0), ("result_1.png", 0, 0), ("result_3.png", 0, 0)], "", "left:1400px;top:104px")

# ---- 10 AI phân tích
BODY[10] = head("TRÍ TUỆ NHÂN TẠO PHÂN TÍCH", "Nhận định cụ thể, bám sát câu trả lời của bạn") \
    + card("✅", "Điểm bạn đang làm tốt", "", "left:90px;top:400px;width:600px;height:130px") \
    + card("⏱️", "Việc cần xử lý trước, kèm thời hạn", "", "left:720px;top:400px;width:620px;height:130px", "alt") \
    + card("📝", "Danh mục tự kiểm tra hằng ngày", "", "left:90px;top:565px;width:1250px;height:130px") + '''
<div class="road" data-a style="left:90px;top:740px"><span>30 ngày</span><i></i><span>60 ngày</span><i></i><span>90 ngày</span><em>Lộ trình khắc phục</em></div>
''' + phone([("result_2.png", 0, 0), ("result_4.png", 0, 0)], "", "left:1400px;top:104px")

# ---- 11 theo dõi khắc phục
BODY[11] = head("KHẢO SÁT CHỈ LÀ KHỞI ĐẦU", "Theo dõi khắc phục: làm tới đâu, tích tới đó") + '''
<div class="checks" data-a style="left:90px;top:400px">
  <div><b>☑</b> Thay ổ cắm, dây điện quá tải</div><div><b>☑</b> Dọn lối thoát nạn</div><div><b>☐</b> Bổ sung bình chữa cháy</div>
</div>
<div class="meter" data-a style="left:90px;top:640px"><span>Mức nguy cơ</span><div class="bar"><div class="fill"></div></div><em>tính lại ngay</em></div>
<div class="code" data-a style="left:90px;top:790px">Mã theo dõi: <b>ABCD-EFGH-JK</b><small>Lưu lại để quay về trên bất kỳ thiết bị nào, không cần tài khoản</small></div>
''' + phone([("mit_0.png", 0, 0), ("mit_1.png", 0, 0)], "", "left:1400px;top:104px")

# ---- 12 trợ lý ảo
BODY[12] = head("PHẦN 2 · TRỢ LÝ ẢO", "Người hướng dẫn luôn sẵn sàng 24/7") + '''
<div class="chat" style="left:90px;top:400px">
  <div class="b q" data-a>Cơ sở của tôi cần chuẩn bị hồ sơ gì để được kiểm tra an toàn PCCC?</div>
  <div class="b a" data-a="late">Bạn chuẩn bị theo từng bước sau: hồ sơ pháp lý của cơ sở, phương án chữa cháy, biên bản kiểm tra… <i>(trả lời rõ ràng, từng bước)</i></div>
  <div class="b q" data-a="later">Bao lâu thì có kết quả?</div>
</div>
<div class="tag" data-a style="left:90px;top:790px">Không cần chờ giờ hành chính · không cần đi lại · hỏi bằng ngôn ngữ đời thường</div>
''' + phone([("home_1.png", 0, 0)], "", "left:1400px;top:104px")

# ---- 13 nguồn tri thức
BODY[13] = head("SỨC MẠNH Ở NGUỒN TRI THỨC", "Trả lời theo văn bản hiện hành, nêu rõ căn cứ pháp lý") + '''
<div class="kb" style="left:90px;top:390px">
  <div class="doc" data-a>📚 Luật, nghị định</div><div class="doc" data-a>📐 Quy chuẩn kỹ thuật</div>
  <div class="doc" data-a>🧾 Tài liệu tập huấn</div><div class="doc" data-a>❓ Hàng trăm câu hỏi đáp thực tế</div>
</div>
<div class="flow" data-a style="left:90px;top:590px">▼ đối chiếu · tra cứu thêm khi quy định thay đổi ▼</div>
<div class="card" data-a style="left:90px;top:650px;width:1240px;height:140px"><div class="ic">🤖</div><div class="tx">Trợ lý ảo<small>Nhớ nội dung vừa hỏi · hiểu tình hình cơ sở · gợi ý sẵn câu hỏi tiếp theo</small></div></div>
<div class="bigsub" data-a="late" style="left:90px;top:820px;width:1240px;font-size:32px;color:var(--gold)">Một người hướng dẫn pháp luật PCCC ngay trong túi áo của bạn</div>
''' + phone([("home_1.png", 0, 0)], "", "left:1400px;top:104px")

# ---- 14 học liệu số
BODY[14] = head("PHẦN 3 · HỌC LIỆU SỐ", "Thư viện khóa học PCCC trực tuyến") + '''
<div class="courses" style="left:90px;top:390px">
  <div class="co" data-a><b>Nhóm 1</b>Kiến thức nền tảng và kỹ năng sống còn</div>
  <div class="co" data-a><b>Nhóm 2</b>Kiến thức chuyên sâu và cộng đồng</div>
</div>
<div class="grid2 sm" style="left:90px;top:560px">
  <div class="chip2" data-a>🏘️ Thoát nạn khi cháy nhà ống</div><div class="chip2" data-a>🔌 Sử dụng điện an toàn</div>
  <div class="chip2" data-a>🧯 Dùng bình chữa cháy xách tay</div><div class="chip2" data-a>❤️ Sơ cứu ngừng hô hấp tuần hoàn</div>
  <div class="chip2 wide" data-a>🌊 Phòng ngừa đuối nước</div>
</div>
<div class="btnzalo" data-a style="left:90px;top:800px">Đăng nhập nhanh bằng Zalo</div>
<div class="tag" data-a style="left:520px;top:800px">Phù hợp gia đình, học sinh, tổ liên gia</div>
''' + phone([("home_1.png", 0, 0)], "", "left:1400px;top:104px")

# ---- 15 trò chơi
BODY[15] = head("TRÒ CHƠI PHÒNG CHÁY CHỮA CHÁY", "Vừa chơi vừa nhớ kỹ năng cần thiết") \
    + card("🔥", "Thoát khỏi đám cháy", "tìm lối thoát nạn an toàn", "left:90px;top:400px;width:1240px;height:140px") \
    + card("❓", "Đố vui kiến thức PCCC", "thi đua với thời gian, nhớ số 114", "left:90px;top:570px;width:1240px;height:140px", "alt") \
    + card("🔍", "Tìm nguy cơ cháy nổ qua hình ảnh", "ảnh do trí tuệ nhân tạo tạo ra", "left:90px;top:740px;width:1240px;height:140px") \
    + phone([("games_0.png", 0, 0), ("games_1.png", 0, 0)], "", "left:1400px;top:104px")

# ---- 16 kết
BODY[16] = '''
<img class="logo" data-a="fade" src="assets/logo.png" style="left:810px;top:130px;width:300px;height:300px">
<div class="four" data-a style="left:0;right:0;top:470px"><span>📋 Khảo sát để thấy rõ nguy cơ</span><span>💬 Hỏi để làm đúng</span><span>🎓 Học để biết cách ứng phó</span><span>🎮 Chơi để nhớ lâu</span></div>
<div class="gold" data-a style="left:0;right:0;top:600px;text-align:center;font-size:130px">FRAS-AI</div>
<div class="url" data-a="late" style="left:0;right:0;top:770px">fras-ai.com</div>
<div class="bigsub" data-a="later" style="left:0;right:0;top:860px;text-align:center;font-size:36px">Đồng hành cùng người dân và doanh nghiệp, vì một cộng đồng an toàn · Báo cháy 114</div>
'''

CSS = open(HERE + r"\hyperframes_fras\style.css", encoding="utf-8").read()

html = ['''<!doctype html>
<html lang="vi" data-resolution="landscape">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=1920, height=1080"/>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<style>''' + CSS + '''</style></head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="%s" data-width="1920" data-height="1080">
<div id="bg" class="clip" data-start="0" data-duration="%s"><div id="grid"></div></div>
<div id="redbar" class="clip" data-start="0" data-duration="%s"></div>
<div id="brand" class="clip" data-start="0" data-duration="%s"><img src="assets/logo.png"><div><div class="t1">CÔNG AN THÀNH PHỐ BẮC NINH</div><div class="t2">PHÒNG CẢNH SÁT PCCC VÀ CNCH</div></div></div>
<div id="progress" class="clip" data-start="0" data-duration="%s"></div>
''' % (TOTAL, TOTAL, TOTAL, TOTAL, TOTAL)]

caps = []
for i, (a, b) in enumerate(T, 1):
    nxt = T[i][0] if i < len(T) else TOTAL
    html.append(f'<div id="s{i}" class="clip scene" data-start="{a}" data-duration="{round(nxt - a, 2)}">{BODY[i]}</div>')
    text = clean(scenes[i - 1]["display"])
    cs = chunks(text)
    tot = sum(len(c) for c in cs)
    t0 = a
    span = b - a
    for c in cs:
        d = span * len(c) / tot
        caps.append((round(t0, 2), round(t0 + d, 2), c))
        t0 += d

for k, (a, b, c) in enumerate(caps):
    html.append(f'<div class="cap clip" id="cap{k}" data-start="{a}" data-duration="{round(b - a + 0.05, 2)}"><span>{c}</span></div>')

html.append('<audio id="vo" src="assets/am_thanh.m4a" data-start="0" data-duration="%s" data-track-index="9" data-volume="1"></audio>' % TOTAL)
html.append('</div>')
html.append('<script>\nconst T = %s;\nconst TOTAL = %s;\n' % (json.dumps(T), TOTAL) + open(HERE + r"\hyperframes_fras\anim.js", encoding="utf-8").read() + '\n</script></body></html>')
open(OUT, "w", encoding="utf-8").write("\n".join(html))
print("ok", len(caps), "phụ đề")
