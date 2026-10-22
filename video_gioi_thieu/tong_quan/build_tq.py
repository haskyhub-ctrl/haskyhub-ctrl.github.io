"""Sinh hf/index.html cho video tổng quan chức năng FRAS-AI (kèm báo cháy 114).
Mốc thời gian lấy từ timeline.json do tts.py tạo."""
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
tl = json.load(open(os.path.join(HERE, "timeline.json"), encoding="utf-8"))
TOTAL = round(tl["duration"], 2)
T = [(s["start"], round(s["start"] + s["audio"], 2)) for s in tl["scenes"]]
scenes = json.load(open(os.path.join(HERE, "script.json"), encoding="utf-8"))["scenes"]
assert len(T) == len(scenes) == 10


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
    merged = []
    for c in out:
        if merged and (len(merged[-1]) < 32 or len(c) < 22) and len(merged[-1]) + len(c) < maxlen + 12:
            merged[-1] += " " + c
        else:
            merged.append(c)
    return merged


def phone(shots, style="left:1400px;top:104px"):
    imgs = "".join(f'<img class="shot" src="assets/shots/{s}">' for s in shots)
    return f'<div class="phone" style="{style}"><div class="screen">{imgs}</div></div>'


def card(icon, title, sub="", style="", cls=""):
    return (f'<div class="card {cls}" data-a style="{style}"><div class="ic">{icon}</div>'
            f'<div class="tx">{title}<small>{sub}</small></div></div>')


def head(eyebrow, title, cls=""):
    return f'<div class="eyebrow {cls}" data-a>{eyebrow}</div><h2 data-a>{title}</h2>'


B = {}

# 1 mở đầu
B[1] = '''
<img class="logo" data-a="fade" src="assets/logo.png" style="left:90px;top:190px;width:200px;height:200px">
<div class="eyebrow" data-a style="left:330px;top:200px">CÔNG AN THÀNH PHỐ BẮC NINH GIỚI THIỆU</div>
<div class="gold" data-a style="left:330px;top:245px;font-size:150px">FRAS-AI</div>
<div class="bigsub" data-a style="left:330px;top:425px;width:960px;font-size:42px">Ứng dụng trí tuệ nhân tạo giúp phòng ngừa cháy, nổ ngay trên điện thoại</div>
<div class="tag" data-a="late" style="left:90px;top:700px">📱 Không cần cài đặt phần mềm · mở trình duyệt là dùng</div>
<div class="url" data-a="later" style="left:90px;top:800px;text-align:left;font-size:84px">fras-ai.com</div>
''' + phone(["home_0.png"])

# 2 năm chức năng
B[2] = head("TỔNG QUAN", "Năm chức năng chính trong một hệ thống") \
    + card("📋", "1. Khảo sát nguy cơ", "từng bước, có kết quả ngay", "left:90px;top:360px;width:610px;height:150px") \
    + card("🚨", "2. Báo cháy 114", "gửi tin báo khẩn cấp trên điện thoại", "left:730px;top:360px;width:610px;height:150px", "alt sos") \
    + card("💬", "3. Trợ lý ảo Chi", "giải đáp pháp luật PCCC 24/7", "left:90px;top:540px;width:610px;height:150px") \
    + card("🎓", "4. Học liệu số", "khóa học trực tuyến", "left:730px;top:540px;width:610px;height:150px") \
    + card("🎮", "5. Trò chơi PCCC", "học mà chơi, chơi mà học", "left:90px;top:720px;width:1250px;height:150px") \
    + phone(["em_home.png"])

# 3 khảo sát
B[3] = head("CHỨC NĂNG 1 · KHẢO SÁT NGUY CƠ", "Chọn loại hình, trả lời từng nhóm câu hỏi") + '''
<div class="grid2 sm" style="left:90px;top:380px">
  <div class="chip2" data-a>🏠 Nhà ở kết hợp kinh doanh</div><div class="chip2" data-a>🍽️ Nhà hàng, khách sạn</div>
  <div class="chip2" data-a>📦 Kho hàng</div><div class="chip2" data-a>🏫 Trường học</div>
  <div class="chip2" data-a>⛽ Cửa hàng xăng dầu</div><div class="chip2" data-a>🏭 Cơ sở sản xuất</div>
</div>
<div class="tag" data-a style="left:90px;top:690px">Mỗi câu chọn 1 trong 4 đáp án, sát với thực tế nhất</div>
<div class="tag red" data-a="late" style="left:90px;top:800px">🏠 Hộ gia đình: khảo sát ngay, không cần tài khoản</div>
''' + phone(["survey_1.png", "survey_q1.png"])

# 4 kết quả + AI
B[4] = head("KẾT QUẢ VÀ KHUYẾN NGHỊ CỦA AI", "Biết ngay mức nguy cơ, biết rõ việc cần làm") + '''
<div class="levels" data-a style="left:90px;top:380px">
  <span style="background:#16A34A">THẤP</span><span style="background:#B45309">TRUNG BÌNH</span><span style="background:#EA580C">CAO</span><span style="background:#DC2626">RẤT CAO</span>
</div>
''' + card("⏱️", "Việc cần xử lý trước, kèm thời hạn", "", "left:90px;top:500px;width:1250px;height:120px") + \
    card("📝", "Danh mục tự kiểm tra hằng ngày", "", "left:90px;top:650px;width:1250px;height:120px", "alt") + '''
<div class="road" data-a style="left:90px;top:820px"><span>30 ngày</span><i></i><span>60 ngày</span><i></i><span>90 ngày</span><em>Lộ trình khắc phục</em></div>
''' + phone(["result_0.png", "result_2.png"])

# 5 theo dõi khắc phục
B[5] = head("THEO DÕI KHẮC PHỤC", "Làm tới đâu, tích tới đó") + '''
<div class="checks" data-a style="left:90px;top:380px">
  <div><b>☑</b> Thay ổ cắm, dây điện quá tải</div><div><b>☑</b> Dọn lối thoát nạn</div><div><b>☐</b> Bổ sung bình chữa cháy</div>
</div>
<div class="meter" data-a style="left:90px;top:640px"><span>Mức nguy cơ</span><div class="bar"><div class="fill"></div></div><em>tính lại ngay</em></div>
<div class="code" data-a="late" style="left:90px;top:790px">Mã theo dõi: <b>ABCD-EFGH-JK</b><small>Lưu lại để quay về trên bất kỳ thiết bị nào, không cần tài khoản</small></div>
''' + phone(["mit_0.png", "mit_1.png"])

# 6 báo cháy 114 (A): cách báo
B[6] = head("CHỨC NĂNG 2 · BÁO CHÁY 114", "Nút báo cháy luôn ở đầu trang chủ", "red") + '''
<div class="sos114" data-a style="left:90px;top:330px"><b>114</b><span>BÁO CHÁY<br>KHẨN CẤP</span></div>
<div class="steps" style="left:420px;top:330px">
  <div data-a><i>1</i><span>Nhập địa điểm, bấm <b>định vị GPS</b></span></div>
  <div data-a><i>2</i><span>Chọn loại hình và mức độ cháy</span></div>
  <div data-a><i>3</i><span>Để lại số điện thoại</span></div>
  <div data-a="late"><i>4</i><span>Đính kèm ảnh hiện trường <em>(không bắt buộc)</em></span></div>
</div>
<div class="tag red" data-a="later" style="left:90px;top:790px">🚨 Bấm “BÁO CHÁY NGAY CHO 114” để gửi</div>
''' + phone(["em_home.png", "em_form_0.png", "em_form_1.png"])

# 7 báo cháy 114 (B): sau khi gửi
B[7] = head("CHỨC NĂNG 2 · BÁO CHÁY 114", "Gửi xong, cán bộ trực sẽ gọi lại xác minh", "red") + '''
<div class="flow3" style="left:90px;top:350px">
  <div data-a><b>📱</b>Bạn gửi tin báo<small>kèm vị trí nếu đã định vị</small></div>
  <em data-a>▶</em>
  <div data-a><b>🖥️</b>Lực lượng trực ban nhận tin<small>chuyển tới ngay khi bạn gửi</small></div>
  <em data-a="late">▶</em>
  <div data-a="late"><b>📞</b>Cán bộ gọi lại<small>xác minh thông tin</small></div>
</div>
<div class="btnred" data-a="late" style="left:90px;top:640px;font-size:36px">📞 Hoặc bấm gọi thẳng 114 bất cứ lúc nào</div>
<div class="tag" data-a="later" style="left:90px;top:790px">Chỉ báo khi có cháy thật, để lực lượng đến kịp nơi cần thiết nhất</div>
''' + phone(["em_ok.png"])

# 8 trợ lý ảo
B[8] = head("CHỨC NĂNG 3 · TRỢ LÝ ẢO CHI", "Hỏi đời thường, trả lời từng bước, nêu căn cứ") + '''
<div class="chat" style="left:90px;top:370px">
  <div class="b q" data-a>Cơ sở của tôi cần chuẩn bị hồ sơ gì để được kiểm tra an toàn PCCC?</div>
  <div class="b a" data-a="late">Bạn chuẩn bị theo từng bước sau: hồ sơ pháp lý của cơ sở, phương án chữa cháy, biên bản kiểm tra… <i>(kèm căn cứ pháp lý)</i></div>
</div>
<div class="kb sm" style="left:90px;top:700px">
  <div class="doc" data-a="later">📚 Luật PCCC và CNCH, nghị định</div><div class="doc" data-a="later">📐 Thông tư, quy chuẩn kỹ thuật</div>
</div>
<div class="tag" data-a="later" style="left:90px;top:830px">Hỗ trợ 24/7 · không cần chờ giờ hành chính</div>
''' + phone(["home_1.png"])

# 9 học liệu + trò chơi
B[9] = head("CHỨC NĂNG 4 VÀ 5 · HỌC LIỆU SỐ, TRÒ CHƠI", "Vừa học, vừa chơi, mỗi lượt vài phút") + '''
<div class="grid2 sm" style="left:90px;top:370px">
  <div class="chip2" data-a>🏘️ Thoát nạn khi cháy nhà ống</div><div class="chip2" data-a>🔌 Sử dụng điện an toàn</div>
  <div class="chip2" data-a>🧯 Dùng bình chữa cháy xách tay</div><div class="chip2" data-a>❤️ Sơ cứu ngừng hô hấp tuần hoàn</div>
</div>
''' + card("🔥", "Thoát khỏi đám cháy", "", "left:90px;top:570px;width:1250px;height:100px") \
    + card("❓", "Đố vui kiến thức PCCC", "", "left:90px;top:690px;width:1250px;height:100px", "alt") \
    + card("🔍", "Tìm nguy cơ cháy nổ qua hình ảnh", "", "left:90px;top:810px;width:1250px;height:100px") \
    + phone(["games_0.png", "games_1.png"])

# 10 kết
B[10] = '''
<img class="logo" data-a="fade" src="assets/logo.png" style="left:830px;top:100px;width:260px;height:260px">
<div class="four" data-a style="left:0;right:0;top:390px"><span>📋 Khảo sát để thấy rõ nguy cơ</span><span>💬 Hỏi để làm đúng</span><span>🎓 Học để biết ứng phó</span><span class="hot">🚨 Báo cháy 114 khi cần</span></div>
<div class="gold" data-a style="left:0;right:0;top:520px;text-align:center;font-size:120px">FRAS-AI</div>
<div class="url" data-a="late" style="left:0;right:0;top:660px">fras-ai.com</div>
<div class="bigsub" data-a="later" style="left:0;right:0;top:810px;text-align:center;font-size:36px">Đồng hành cùng người dân và doanh nghiệp, vì một cộng đồng an toàn</div>
'''

CSS = open(os.path.join(HERE, "..", "hyperframes_fras", "style.css"), encoding="utf-8").read()
CSS += """
.eyebrow.red{color:#ff6b6b}
.card.sos{background:rgba(192,32,42,.28);border-color:#ff6b6b}
.kb.sm{grid-template-columns:1fr 1fr;width:1250px}.kb.sm .doc{font-size:26px}
.sos114{display:flex;flex-direction:column;align-items:center;justify-content:center;width:300px;height:380px;background:linear-gradient(160deg,#d62832,#8f1019);box-shadow:0 20px 60px rgba(192,32,42,.55);border:4px solid #ff9a9a}
.sos114 b{font-size:150px;font-weight:900;line-height:1}
.sos114 span{font-size:30px;font-weight:800;letter-spacing:3px;text-align:center;margin-top:10px}
.steps{width:880px;display:flex;flex-direction:column;gap:20px}
.steps>div{display:flex;align-items:center;gap:22px;padding:20px 26px;font-size:34px;font-weight:700;background:rgba(255,255,255,.09);border-left:8px solid var(--red)}
.steps i{font-style:normal;min-width:56px;height:56px;line-height:56px;text-align:center;font-size:34px;font-weight:900;background:var(--red)}
.steps b{color:var(--gold)}.steps em{font-style:normal;font-size:26px;color:#c9d6ee;font-weight:600}
.flow3{display:flex;align-items:stretch;gap:14px;width:1260px}
.flow3>div{flex:1;padding:22px 20px;font-size:32px;font-weight:800;line-height:1.25;background:rgba(255,255,255,.1);border-top:6px solid var(--red);text-align:center}
.flow3>div b{display:block;font-size:64px;margin-bottom:8px}
.flow3 small{display:block;font-size:22px;font-weight:500;color:#c9d6ee;margin-top:8px}
.flow3>em{align-self:center;font-style:normal;font-size:40px;color:var(--gold)}
.four span.hot{background:rgba(192,32,42,.5);border-bottom-color:#ff6b6b}
.four{flex-wrap:wrap;padding:0 60px}
"""

ANIM = r"""
window.__timelines = window.__timelines || {};
const tl = gsap.timeline({ paused: true });
tl.fromTo('#progress', { width: '0%' }, { width: '100%', duration: TOTAL, ease: 'none' }, 0);
document.querySelectorAll('.scene').forEach((sc, i) => {
  const a = T[i][0], b = T[i][1];
  const nxt = i < T.length - 1 ? T[i + 1][0] : TOTAL;
  const span = b - a;
  tl.fromTo(sc, { opacity: 0 }, { opacity: 1, duration: 0.5, ease: 'power1.out' }, a);
  if (i < T.length - 1) tl.to(sc, { opacity: 0, duration: 0.45, ease: 'power1.in' }, nxt - 0.5);
  const els = [...sc.querySelectorAll('[data-a]')].filter(e => !e.dataset.a || e.dataset.a === 'fade');
  const step = Math.min(0.7, (span * 0.5) / Math.max(1, els.length));
  els.forEach((el, k) => {
    const fadeOnly = el.dataset.a === 'fade';
    tl.fromTo(el, fadeOnly ? { opacity: 0 } : { opacity: 0, y: 34 },
      fadeOnly ? { opacity: 1, duration: 0.8 } : { opacity: 1, y: 0, duration: 0.6, ease: 'power3.out' }, a + 0.35 + k * step);
  });
  sc.querySelectorAll('[data-a="late"],[data-a="later"]').forEach(el => {
    const at = a + span * (el.dataset.a === 'late' ? 0.4 : 0.62);
    tl.fromTo(el, { opacity: 0, y: 34 }, { opacity: 1, y: 0, duration: 0.6, ease: 'power3.out' }, at);
  });
  sc.querySelectorAll('.phone').forEach(ph => {
    tl.fromTo(ph, { x: 140, opacity: 0 }, { x: 0, opacity: 1, duration: 0.9, ease: 'power3.out' }, a + 0.2);
    const shots = [...ph.querySelectorAll('.shot')];
    shots.forEach((im, j) => {
      if (j === 0) return;
      const at = a + (span + 1.0) * j / shots.length;
      tl.to(shots[j - 1], { opacity: 0, duration: 0.5 }, at);
      tl.to(im, { opacity: 1, duration: 0.5 }, at);
    });
  });
});
document.querySelectorAll('.cap').forEach(c => {
  const s = parseFloat(c.dataset.start), d = parseFloat(c.dataset.duration);
  tl.fromTo(c, { opacity: 0, y: 10 }, { opacity: 1, y: 0, duration: 0.22 }, s);
  tl.to(c, { opacity: 0, duration: 0.15 }, s + d - 0.15);
});
tl.fromTo('#s5 .fill', { width: '92%' }, { width: '28%', duration: 4, ease: 'power2.inOut' }, T[4][0] + 3.0);
tl.fromTo('#s6 .sos114', { scale: 1 }, { scale: 1.06, duration: 0.6, repeat: 5, yoyo: true, ease: 'sine.inOut' }, T[5][0] + 1.2);
window.__timelines['main'] = tl;
tl.seek(0);
"""

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
''' % ((TOTAL,) * 5)]

caps = []
for i, (a, b) in enumerate(T, 1):
    nxt = T[i][0] if i < len(T) else TOTAL
    html.append(f'<div id="s{i}" class="clip scene" data-start="{a}" data-duration="{round(nxt - a, 2)}">{B[i]}</div>')
    cs = chunks(scenes[i - 1]["display"])
    tot = sum(len(c) for c in cs)
    t0 = a
    for c in cs:
        d = (b - a) * len(c) / tot
        caps.append((round(t0, 2), round(t0 + d, 2), c))
        t0 += d
for k, (a, b, c) in enumerate(caps):
    html.append(f'<div class="cap clip" id="cap{k}" data-start="{a}" data-duration="{round(b - a + 0.05, 2)}"><span>{c}</span></div>')
html.append('<audio id="vo" src="assets/am_thanh.m4a" data-start="0" data-duration="%s" data-track-index="9" data-volume="1"></audio>' % TOTAL)
html.append('</div>')
html.append('<script>\nconst T = %s;\nconst TOTAL = %s;\n' % (json.dumps(T), TOTAL) + ANIM + '\n</script></body></html>')
open(os.path.join(HERE, "hf", "index.html"), "w", encoding="utf-8").write("\n".join(html))
print("ok", TOTAL, "giây;", len(caps), "phụ đề")
