import json
from random import shuffle

hazards = [
    {"img":"img/hazards/hazard1.png","q":"Đâu là nguy cơ cháy nổ trong hình?","a":"Ổ cắm điện quá tải chập cháy","opts":["Bật đèn ngủ quá sáng","Ổ cắm điện quá tải chập cháy","Để giày dép không ngăn nắp","Quét nhà không sạch"]},
    {"img":"img/hazards/hazard2.png","q":"Hành động nào trong hình rất nguy hiểm?","a":"Thắp nến quá gần rèm cửa dễ cháy","opts":["Mở cửa sổ lúc trời tối","Thắp nến quá gần rèm cửa dễ cháy","Trồng cây trong nhà","Sắp xếp phòng lệch phong thủy"]},
    {"img":"img/hazards/hazard3.png","q":"Tình huống trong bếp này do nguyên nhân gì?","a":"Đun nấu để quên làm chảo dầu bốc cháy","opts":["Bếp gas hỏng không đánh lửa","Dao nĩa để lộn xộn","Đun nấu để quên làm chảo dầu bốc cháy","Tràn nước ra bồn rửa"]},
    {"img":"img/hazards/hazard4.png","q":"Điện thoại di động trong hình có nguy cơ gì?","a":"Sạc điện thoại chèn dưới gối ủ nhiệt bốc cháy","opts":["Sạc điện thoại chèn dưới gối ủ nhiệt bốc cháy","Báo thức kêu quá to","Nghe gọi bằng tai nghe có dây","Chỉ là lỗi phần mềm nhẹ"]},
    {"img":"img/hazards/hazard5.png","q":"Sự nguy hiểm lớn nhất từ bình gas này là gì?","a":"Bình gas gỉ sét rò rỉ khí gas ra ngoài","opts":["Bình gas sơn màu kém thẩm mỹ","Bình gas gỉ sét rò rỉ khí gas ra ngoài","Chiếm diện tích bếp","Hết gas khi đang đun nấu"]},
    {"img":"img/hazards/hazard6.png","q":"Đâu là thói quen xấu gây cháy trong hình?","a":"Hút thuốc và làm rơi tàn đỏ xuống sofa vải","opts":["Nằm ngủ sai tư thế","Hút thuốc và làm rơi tàn đỏ xuống sofa vải","Không dọn dẹp phòng khách","Đeo kính khi ngủ"]},
    {"img":"img/hazards/hazard7.png","q":"Lò vi sóng trong hình phát tia lửa vì sao?","a":"Để nĩa/vật dụng kim loại vào lò vi sóng","opts":["Quay thức ăn quá 5 phút","Không đậy nắp hộp nhựa","Máy bị hỏng do ẩm ướt","Để nĩa/vật dụng kim loại vào lò vi sóng"]},
    {"img":"img/hazards/hazard8.png","q":"Tại sao đặt quạt sưởi ở đây rất dễ gây cháy?","a":"Đặt máy sưởi sát quần áo, rèm cửa dễ bắt lửa","opts":["Cắm diện liên tục tốn điện","Máy sưởi bị hỏng mô tơ","Đặt máy sưởi sát quần áo, rèm cửa dễ bắt lửa","Không bật chế độ quay đều"]},
    {"img":"img/hazards/hazard9.png","q":"Hình ảnh này cảnh báo điều gì về an toàn điện?","a":"Dây điện cũ nát, rách vỏ bọc gây chập điện","opts":["Nên cuộn gọn dây điện để tiết kiệm chỗ","Dây điện cũ nát, rách vỏ bọc gây chập điện","Gây mất thẩm mỹ cho căn nhà","Từ trường sẽ làm nhiễu sóng ti vi"]},
    {"img":"img/hazards/hazard10.png","q":"Bạn nhận ra thiết lập nào nguy hiểm trong ảnh?","a":"Thắp nến ngay sát sách vở ngăn kệ bằng gỗ","opts":["Xếp sách không theo bảng giá sách","Thắp nến đèn màu không đẹp","Thắp nến ngay sát sách vở ngăn kệ bằng gỗ","Không lau dọn bụi bặm"]},
    {"img":"img/hazards/hazard11.png","q":"Lỗi nào trong nhà bếp có thể làm lửa lan nhanh?","a":"Để khăn lau bếp vắt ngang gần sát mâm lửa gas","opts":["Không bật máy hút mùi","Quá trình xào nấu quá lửa","Để khăn lau bếp vắt ngang gần sát mâm lửa gas","Bỏ qua gia vị khi nấu"]},
    {"img":"img/hazards/hazard12.png","q":"Việc sử dụng bình xịt cạnh nến sẽ gây ra gì?","a":"Bình xịt khí nén (như gôm tóc/xịt muỗi) phun qua lửa gây nổ","opts":["Hương thơm sẽ đánh bật mùi trong phòng","Bình xịt khí nén (như gôm tóc/xịt muỗi) phun qua lửa gây nổ","Khí xịt sẽ làm tắt nến","Thuốc xịt không có tác dụng"]},
    {"img":"img/hazards/hazard13.png","q":"Trường hợp này sẽ dẫn tới hậu quả gì?","a":"Thiết bị đèn/sưởi bị đổ sấp nung nóng thảm vải bốc khói","opts":["Thiết bị đèn/sưởi bị đổ sấp nung nóng thảm vải bốc khói","Tốn tiền điện khi không sử dụng","Ánh sáng không được tối ưu","Hỏng thiết bị"]},
    {"img":"img/hazards/hazard14.png","q":"Người trong hình đã vi phạm nguyên tắc gì khi là ủi?","a":"Bỏ quên bàn là nóng úp xuống quần áo, gây cháy","opts":["Không rút phích cắm khi đổ nước","Bỏ quên bàn là ngang thay vì úp xuống","Bỏ quên bàn là nóng úp xuống quần áo, gây cháy","Chỉnh nhiệt quá vạch chỉ định"]},
    {"img":"img/hazards/hazard15.png","q":"Trong ảnh hiển thị rủi ro khói lên từ đâu?","a":"Vứt tàn thuốc chưa dập tắt hẳn vào sọt rác toàn giấy","opts":["Vứt tàn thuốc chưa dập tắt hẳn vào sọt rác toàn giấy","Thùng rác dơ dáy không đổ quá lâu","Khói từ món đồ chơi điện tử vô tình rơi vào","Giấy rác tự phân hủy bốc khói"]},
    {"img":"img/hazards/hazard16.png","q":"Bố trí bếp nướng thế này sai lầm ở đâu?","a":"Nướng BBQ trực tiếp dưới kết cấu mái/lan can bằng gỗ bắt lửa","opts":["Thiếu gia vị để ướp đồ nướng","Nướng BBQ trực tiếp dưới kết cấu mái/lan can bằng gỗ bắt lửa","Lò nướng làm bằng sắt dễ han gỉ","Khói làm hỏng quần áo đang phơi"]},
    {"img":"img/hazards/hazard17.png","q":"Tại sao không nên sử dụng thiết bị điện này?","a":"Ổ cắm lỏng lẻo phóng tia lửa điện có thể bắn vào vật dụng xung quanh","opts":["Phích cắm sai tiêu chuẩn quốc gia","Ổ cắm tốn nhiều diện tích phòng","Không đóng chặt các phích cắm làm hỏng lỗ cắm","Ổ cắm lỏng lẻo phóng tia lửa điện có thể bắn vào vật dụng xung quanh"]},
    {"img":"img/hazards/hazard18.png","q":"Hành động vô ý này tiềm tàng nguy cơ gì?","a":"Đèn báo thức/đèn nhiệt bị vải trùm lên không thoát nhiệt gây cháy khăn","opts":["Ánh sáng chói vào mặt gây khó ngủ","Đèn báo thức/đèn nhiệt bị vải trùm lên không thoát nhiệt gây cháy khăn","Phòng sẽ tối và không xem được điện thoại","Mất giá trị thẩm mỹ của đèn ngủ"]},
    {"img":"img/hazards/hazard19.png","q":"Chơi trò này trong nhà sẽ gặp hậu quả gì?","a":"Đốt pháo/bắn tia lửa sát các vật dụng bọc nỉ/da gây cháy nhà","opts":["Khói sẽ bay lên làm đen trần nhà","Tốn tiền mua pháo nhưng không đẹp","Đốt pháo/bắn tia lửa sát các vật dụng bọc nỉ/da gây cháy nhà","Âm thanh lớn làm hàng xóm nhắc nhở"]},
    {"img":"img/hazards/hazard20.png","q":"Cảnh báo PCCC lớn nhất trong hình ảnh này là gì?","a":"Đồ đạc để ngổn ngang chặn kín lối cửa thoát hiểm","opts":["Dọn dẹp không gọn gàng ảnh hưởng mỹ quan","Nhầm lẫn đồ vật của nhau","Đồ đạc để ngổn ngang chặn kín lối cửa thoát hiểm","Gây khó khăn cho việc lau don hằng ngày"]}
]

# Randomize options for each hazard
for item in hazards:
    shuffle(item["opts"])

html_template = """<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tìm Nguy Cơ Cháy Nổ (Ảnh AI)</title>
    <!-- Phông chữ hiện đại -->
    <link href="https://fonts.googleapis.com/css2?family=Quicksand:wght@400;600;700&display=swap" rel="stylesheet">
    <!-- Font Awesome -->
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <link rel="stylesheet" href="css/games.css">
    <style>
        .spot-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            width: 100%;
            height: auto;
            position: relative;
        }

        .img-wrapper {
            position: relative;
            width: 80%;
            max-width: 600px;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            margin-bottom: 20px;
            border: 2px solid rgba(255,255,255,0.1);
        }

        .img-wrapper img {
            width: 100%;
            height: auto;
            display: block;
        }

        .question-box {
            background: rgba(0, 0, 0, 0.4);
            padding: 15px 25px;
            border-radius: 8px;
            font-size: 1.4em;
            font-weight: 700;
            color: #ffca28;
            margin-bottom: 20px;
            text-align: center;
            width: 90%;
            max-width: 800px;
        }

        .options-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            width: 90%;
            max-width: 800px;
        }

        .opt-btn {
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            color: #fff;
            padding: 15px;
            border-radius: 10px;
            font-size: 1.1em;
            cursor: pointer;
            transition: all 0.3s;
            text-align: left;
            font-family: 'Quicksand', sans-serif;
            display: flex;
            align-items: center;
        }

        .opt-btn:hover {
            background: rgba(255, 255, 255, 0.2);
            transform: translateY(-2px);
        }

        .opt-btn.correct { background: #4caf50; border-color: #388e3c; }
        .opt-btn.wrong { background: #f44336; border-color: #d32f2f; }

        .game-header {
            display: flex;
            justify-content: space-between;
            width: 90%;
            max-width: 800px;
            margin-bottom: 15px;
            font-size: 1.2em;
        }
        
        #result-modal {
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.8);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 1000;
        }

        .modal-content {
            background: linear-gradient(135deg, rgba(30,30,30,0.9), rgba(10,10,10,0.95));
            border: 1px solid rgba(255,255,255,0.1);
            padding: 40px;
            border-radius: 15px;
            text-align: center;
            color: #fff;
            max-width: 500px;
        }
        .modal-content h2 { margin-top: 0; color: #ffeb3b; }
        .modal-content .score-big { font-size: 3em; margin: 20px 0; font-weight: bold; color: #4caf50; }
        .modal-content button {
            background: #2196f3; color: #fff; border: none; padding: 12px 30px;
            border-radius: 25px; font-size: 1.2em; cursor: pointer; transition: 0.3s;
        }
        .modal-content button:hover { background: #1976d2; }
        
        .timer-text { font-weight: bold; color: #ff5252; }
    </style>
</head>
<body>

    <!-- Nền Particles -->
    <div id="particles-js"></div>

    <div class="glass-panel" style="width: 90%; max-width: 1000px;">
        <div style="display: flex; align-items: center; margin-bottom: 20px; gap: 15px;">
            <button onclick="window.location.href='index.html'" class="btn-primary" style="padding: 10px 20px; font-size: 1rem;"><i class="fas fa-home"></i> Trang chủ</button>
            <h1 style="margin: 0; flex-grow: 1; text-align: center;">TÌM NGUY CƠ CHÁY NỔ QUA ẢNH</h1>
        </div>
        
        <div class="game-header">
            <div><i class="fas fa-image"></i> Hình ảnh: <span id="img-count">1</span> / 20</div>
            <div><i class="fas fa-star" style="color: #ffca28;"></i> Điểm: <span id="score">0</span></div>
        </div>

        <div class="spot-container" id="spot-container">
            <div class="img-wrapper">
                <img id="hazard-img" src="" alt="Nguy cơ cháy nổ">
            </div>
            <div class="question-box" id="question-text">
                Đâu là nguy cơ cháy nổ trong hình?
            </div>
            <div class="options-grid" id="optionsGrid">
                <!-- Options will be pushed here -->
            </div>
        </div>
    </div>

    <!-- Modal Kết quả -->
    <div id="result-modal" style="display: none;">
        <div class="modal-content">
            <h2>Hoàn thành xuất sắc!</h2>
            <div class="score-big" id="final-score">0</div>
            <p>Tuyệt vời! Bạn đã có một kỹ năng nhận biết rủi ro PCCC rất tốt thông qua các hình ảnh chân thực!</p>
            <button onclick="location.reload()">Chơi Lại <i class="fas fa-redo"></i></button>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/particles.js/2.0.0/particles.min.js"></script>
    <script>
        particlesJS.load('particles-js', 'assets/particles.json', function() {
            console.log('particles.js loaded');
        });

        const HAZARDS = """ + json.dumps(hazards, ensure_ascii=False) + """;

        let currentIdx = 0;
        let score = 0;

        const imgEl = document.getElementById('hazard-img');
        const qEl = document.getElementById('question-text');
        const gridEl = document.getElementById('optionsGrid');
        const countSpan = document.getElementById('img-count');
        const scoreSpan = document.getElementById('score');

        function loadQuestion() {
            if(currentIdx >= HAZARDS.length) {
                document.getElementById('result-modal').style.display = 'flex';
                document.getElementById('final-score').innerText = score + " / " + HAZARDS.length;
                return;
            }

            const hz = HAZARDS[currentIdx];
            imgEl.src = hz.img;
            qEl.innerText = hz.q;
            countSpan.innerText = currentIdx + 1;
            
            gridEl.innerHTML = '';
            
            // Render opts
            hz.opts.forEach(opt => {
                const btn = document.createElement('button');
                btn.className = 'opt-btn';
                btn.innerText = opt;
                btn.onclick = () => handleAnswer(opt, hz.a, btn);
                gridEl.appendChild(btn);
            });
        }

        function handleAnswer(selected, correct, btnEl) {
            // disable all
            const btns = gridEl.querySelectorAll('.opt-btn');
            btns.forEach(b => {
                b.disabled = true;
                if(b.innerText === correct) {
                    b.classList.add('correct');
                    b.innerHTML = '<i class="fas fa-check-circle" style="margin-right:8px;"></i> ' + b.innerText;
                }
            });

            if(selected === correct) {
                score++;
                scoreSpan.innerText = score;
                playSfx(1000, 'sine', 0.1); // Ding
            } else {
                btnEl.classList.add('wrong');
                btnEl.innerHTML = '<i class="fas fa-times-circle" style="margin-right:8px;"></i> ' + btnEl.innerText;
                playSfx(150, 'sawtooth', 0.3); // Buzz
            }

            setTimeout(() => {
                currentIdx++;
                loadQuestion();
            }, 1800);
        }

        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        function playSfx(freq, type, dur){
            if(audioCtx.state === 'suspended') audioCtx.resume();
            const osc = audioCtx.createOscillator();
            const gainNode = audioCtx.createGain();
            osc.type = type;
            osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
            if(type === 'sine') {
                osc.frequency.exponentialRampToValueAtTime(freq * 1.5, audioCtx.currentTime + dur);
            } else {
                osc.frequency.exponentialRampToValueAtTime(50, audioCtx.currentTime + dur);
            }
            gainNode.gain.setValueAtTime(0.3, audioCtx.currentTime);
            gainNode.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + dur);
            
            osc.connect(gainNode);
            gainNode.connect(audioCtx.destination);
            osc.start();
            osc.stop(audioCtx.currentTime + dur);
        }

        // Init
        loadQuestion();
    </script>
</body>
</html>"""

with open(r"c:\Users\Hasky\.gemini\antigravity\scratch\fras\frontend\game-spot.html", "w", encoding="utf-8") as f:
    f.write(html_template)

print("Game spot rewritten.")
