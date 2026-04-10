import re

def update_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Convert texts to Vietnamese
    replacements = [
        ("TAM DUNG", "TẠM DỪNG"),
        ("Game da tam dung. Nhan nut hoac ESC de tiep tuc.", "Game đã tạm dừng. Nhấn nút hoặc ESC để tiếp tục."),
        ("'TIEP TUC'", "'TIẾP TỤC'"),
        ("'CHOI LAI'", "'CHƠI LẠI'"),
        ("'Man '", "'Màn '"),
        ("'BAT DAU'", "'BẮT ĐẦU'"),
        ("Het thoi gian! Ban khong kip thoat ra.", "Hết thời gian! Bạn không kịp thoát ra."),
        ("Lua da lan den vi tri cua ban!", "Lửa đã lan đến vị trí của bạn!"),
        ("Ky luc cao nhat: ", "Kỷ lục cao nhất: "),
        ("Mat mang! (Con ", "Mất mạng! (Còn "),
        ("'THU LAI'", "'THỬ LẠI'"),
        ("Binh chua chay: Keo chot, bop tay cam, huong vao goc lua, quet trai phai.", "Bình chữa cháy: Kéo chốt, bóp tay cầm, hướng vào gốc lửa, quét trái phải."),
        ("Trong khoi: CUI THAP, dung khan uot bit mui, men theo tuong.", "Trong khói: CÚI THẤP, dùng khăn ướt bịt mũi, men theo tường."),
        ("Luon mang chia khoa phong ngua, KHONG khoa cua thoat nan bang khoa ngoai!", "Luôn mang chìa khóa phòng ngừa, KHÔNG khóa cửa thoát nạn bằng khóa ngoài!"),
        ("Day dien ho rat NGUY HIEM! Ngat cau dao truoc khi tiep can.", "Dây điện hở rất NGUY HIỂM! Ngắt cầu dao trước khi tiếp cận."),
        ("Khoa van gas TRUOC KHI dap lua gan nguon gas. Gas + lua = NO!", "Khóa van gas TRƯỚC KHI dập lửa gần nguồn gas. Gas + lửa = NỔ!"),
        ("Khoi lam giam tam nhin cuc ky nguy hiem. Di chuyen cham, cui thap!", "Khói làm giảm tầm nhìn cực kỳ nguy hiểm. Di chuyển chậm, cúi thấp!"),
        ("Goi 114 NGAY khi phat hien chay! Moi giay cham tre = lua lan them.", "Gọi 114 NGAY khi phát hiện cháy! Mỗi giây chậm trễ = lửa lan thêm."),
        ("Kiem tra cua TRUOC KHI mo: dat mu ban tay len cua, neu NONG thi KHONG mo!", "Kiểm tra cửa TRƯỚC KHI mở: đặt mu bàn tay lên cửa, nếu NÓNG thì KHÔNG mở!"),
        ("Khi thoat nan, ho tro nguoi xung quanh. KHONG chan loi thoat!", "Khi thoát nạn, hỗ trợ người xung quanh. KHÔNG chặn lối thoát!"),
        ("Quy trinh chuan: Ngat dien > Khoa gas > Dap lua > Goi 114 > Cuu nguoi > Thoat nan!", "Quy trình chuẩn: Ngắt điện > Khóa gas > Dập lửa > Gọi 114 > Cứu người > Thoát nạn!"),
        (" Bonus cuu nguoi: +200!", " Bonus cứu người: +200!"),
        (" KY LUC MOI! ", " KỶ LỤC MỚI! "),
        ("'CHIEN THANG!'", "'CHIẾN THẮNG!'"),
        ("'Diem: '", "'Điểm: '"),
        ("'THOAT NAN THANH CONG!'", "'THOÁT NẠN THÀNH CÔNG!'"),
        ("'Thuong: +'", "'Thưởng: +'"),
        ("' điểm'", "' điểm'"), # just in case
        ("'MAN TIEP'", "'MÀN TIẾP'"),
        ("Ngat dien!", "Ngắt điện!"),
        ("Luon ngat dien truoc khi tiep can day dien!", "Luôn ngắt điện trước khi tiếp cận dây điện!"),
        ("Khoa gas!", "Khóa gas!"),
        ("Khoa van gas TRUOC KHI dap lua gan nguon gas!", "Khóa van gas TRƯỚC KHI dập lửa gần nguồn gas!"),
        ("Goi 114!", "Gọi 114!"),
        ("Luon goi 114 ngay khi phat hien chay!", "Luôn gọi 114 ngay khi phát hiện cháy!"),
        ("Cua NONG!", "Cửa NÓNG!"),
        ("Cua rat nong, phia sau dang chay! Phai di duong khac.", "Cửa rất nóng, phía sau đang cháy! Phải đi đường khác."),
        ("Cua an toan!", "Cửa an toàn!"),
        ("Don do vat!", "Dọn đồ vật!"),
        ("Luon giu loi thoat thong rong!", "Luôn giữ lối thoát thông rộng!"),
        ("Bi dien giat! Phai ngat cau dao truoc.", "Bị điện giật! Phải ngắt cầu dao trước."),
        ("Khi gas bung chay! Phai khoa van gas truoc.", "Khí gas bùng cháy! Phải khóa van gas trước."),
        ("+50 Dap lua!", "+50 Dập lửa!"),
        ("Di vao dam chay ma khong co binh chua chay!", "Đi vào đám cháy mà không có bình chữa cháy!"),
        ("Hit phai khoi doc! Can khan uot bit mui mieng.", "Hít phải khói độc! Cần khăn ướt bịt mũi miệng."),
        ("Khi doc! Can mat na phong doc.", "Khí độc! Cần mặt nạ phòng độc."),
        ("Mo khoa!", "Mở khóa!"),
        ("Can chia khoa!", "Cần chìa khóa!"),
        ("Phai goi 114!", "Phải gọi 114!"),
        ("Binh chua chay!", "Bình chữa cháy!"),
        ("Khan uot!", "Khăn ướt!"),
        ("Mat na!", "Mặt nạ!"),
        ("Chia khoa!", "Chìa khóa!"),
        ("Cuu nguoi! Di den EXIT!", "Cứu người! Đi đến EXIT!"),
        ("Nhan BAT DAU de choi!", "Nhấn BẮT ĐẦU để chơi!"),
        ("Thoat khoi dam chay", "Thoát khỏi đám cháy"),
        ("Di chuyen: phim mui ten hoac WASD\\nTuong tac: Space hoac Enter\\n\\nThu thap vat pham, giai do va tim loi thoat!", "Di chuyển: phím mũi tên hoặc WASD\\nTương tác: Space hoặc Enter\\n\\nThu thập vật phẩm, giải đố và tìm lối thoát!"),
        ("'BAT DAU CHOI'", "'BẮT ĐẦU CHƠI'"),
        ("'GOI',x+T/2,y+T/2-3", "'GỌI',x+T/2,y+T/2-3"),
        ("'DIEN',x+T/2,y+T-2", "'ĐIỆN',x+T/2,y+T-2"),
        ("'KHOA',x+T/2,y+T-2", "'KHÓA',x+T/2,y+T-2"),
        ("'M.NA',x+T/2,y+T-2", "'M.NẠ',x+T/2,y+T-2"),
        ("'KHAN',x+T/2,y+T-2", "'KHĂN',x+T/2,y+T-2"),
        ("gasOff?'OFF':'MO',x+T/2,y+T-3", "gasOff?'OFF':'MỞ',x+T/2,y+T-3"),
        ("'KIEM',x+T/2,y+T/2-3", "'KIỂM',x+T/2,y+T/2-3"),
        ("'DOI',x+T/2,y+T-2", "'DỜI',x+T/2,y+T-2"),
        ("'NONG!',x+T/2,y+T-2", "'NÓNG!',x+T/2,y+T-2"),
        ("'CUU!',x+T/2,y+T-1", "'CỨU!',x+T/2,y+T-1"),
    ]

    for old_s, new_s in replacements:
        content = content.replace(old_s, new_s)

    # 2. Modify to use Camera
    # Add cam variables
    content = content.replace("tick=0,tInt=null,", "tick=0,tInt=null,\ncamX=0,camY=0,camW=900,camH=684,")
    
    # Remove resizing logic when loading level
    content = content.replace("cv.width=C*T;cv.height=R*T;", "/* cv.width and height are fixed to camW, camH */")
    
    # Update rendering to use Camera
    if "requestAnimationFrame(render);" in content:
        render_function_old = """function render(){
  tick++;cx.clearRect(0,0,cv.width,cv.height);cv.style.transform='translate(0,0)';
  cx.fillStyle='#0d0d1a';cx.fillRect(0,0,cv.width,cv.height);
  if(map){
    if(shakeIntensity>0.5)applyShake();
    var fr=fogRadius||4;
    // FOG OF WAR ALWAYS ACTIVE
    if(fogActive&&fr<20){
      for(var r=0;r<R;r++)for(var c=0;c<C;c++){
        var dist=Math.abs(c-p.x)+Math.abs(r-p.y);
        if(dist<=fr){
          dTile(c,r);
          if(dist>=fr-1){cx.fillStyle='rgba(0,0,0,'+((dist-(fr-1))*0.35)+')';cx.fillRect(c*T,r*T,T,T);}
        }else{
          cx.fillStyle='rgba(0,0,0,0.96)';cx.fillRect(c*T,r*T,T,T);
        }
      }
    }else{
      for(var r=0;r<R;r++)for(var c=0;c<C;c++)dTile(c,r);
    }
    dNPCFollow();dPlayer();
  }else{cx.fillStyle='#fff';cx.font="18px "+FNT;cx.textAlign='center';cx.fillText('Nhấn BẮT ĐẦU để chơi!',cv.width/2,cv.height/2);}
"""
        
        render_function_new = """function render(){
  tick++;cx.clearRect(0,0,cv.width,cv.height);cv.style.transform='translate(0,0)';
  cx.fillStyle='#0d0d1a';cx.fillRect(0,0,cv.width,cv.height);
  if(map){
    if(shakeIntensity>0.5)applyShake();
    
    // Camera logic
    var targetCamX = p.x*T + T/2 - cv.width/2;
    var targetCamY = p.y*T + T/2 - cv.height/2;
    var maxCamX = Math.max(0, C*T - cv.width);
    var maxCamY = Math.max(0, R*T - cv.height);
    targetCamX = Math.max(0, Math.min(maxCamX, targetCamX));
    targetCamY = Math.max(0, Math.min(maxCamY, targetCamY));
    camX += (targetCamX - camX) * 0.15;
    camY += (targetCamY - camY) * 0.15;
    
    cx.save();
    cx.translate(-camX, -camY);

    var fr=fogRadius||4;
    // FOG OF WAR ALWAYS ACTIVE
    if(fogActive&&fr<20){
      for(var r=0;r<R;r++)for(var c=0;c<C;c++){
        // culling
        if(c*T+T < camX || c*T > camX+cv.width || r*T+T < camY || r*T > camY+cv.height) continue;
        
        var dist=Math.abs(c-p.x)+Math.abs(r-p.y);
        if(dist<=fr){
          dTile(c,r);
          if(dist>=fr-1){cx.fillStyle='rgba(0,0,0,'+((dist-(fr-1))*0.35)+')';cx.fillRect(c*T,r*T,T,T);}
        }else{
          cx.fillStyle='rgba(0,0,0,0.96)';cx.fillRect(c*T,r*T,T,T);
        }
      }
    }else{
      for(var r=0;r<R;r++)for(var c=0;c<C;c++){
        if(c*T+T < camX || c*T > camX+cv.width || r*T+T < camY || r*T > camY+cv.height) continue;
        dTile(c,r);
      }
    }
    dNPCFollow();dPlayer();
"""
        content = content.replace(render_function_old, render_function_new)
        
        # We also need to restore `cx.restore()` before drawing particles and messages? 
        # No, particles and messages are world coordinates, so they should be drawn WITHIN the translated context.
        # But wait! HUD or educational messages are absolute coordinates (cv.width/2, cv.height-40). 
        # Let's fix that.
        
        particle_and_msg_old = """  // Particles
  var ap=[];for(var i=0;i<particles.length;i++){var q=particles[i];q.x+=q.vx;q.y+=q.vy;q.life--;q.sz*=.96;
    cx.globalAlpha=Math.max(0,q.life/q.ml);cx.fillStyle=q.col;cx.beginPath();cx.arc(q.x,q.y,q.sz,0,Math.PI*2);cx.fill();
    if(q.life>0)ap.push(q);}particles=ap;cx.globalAlpha=1;
  // Messages
  var am=[];for(var j=0;j<fmsgs.length;j++){var m=fmsgs[j];m.y-=0.25;m.life--;
    if(m.isEduTip){
      cx.globalAlpha=Math.min(1,Math.max(0,m.life/60));
      cx.fillStyle='rgba(0,0,0,0.75)';cx.fillRect(m.x-180,m.y-12,360,22);
      cx.fillStyle='#ffd93d';cx.font="bold 12px "+FNT;cx.textAlign='center';cx.fillText(m.text,m.x,m.y);
    }else{
      cx.globalAlpha=Math.min(1,Math.max(0,m.life/30));
      cx.fillStyle='#ffd93d';cx.font="bold 11px "+FNT;cx.textAlign='center';cx.fillText(m.text,m.x,m.y);
    }
    if(m.life>0)am.push(m);}fmsgs=am;cx.globalAlpha=1;"""
        
        particle_and_msg_new = """  // Particles
  var ap=[];for(var i=0;i<particles.length;i++){var q=particles[i];q.x+=q.vx;q.y+=q.vy;q.life--;q.sz*=.96;
    cx.globalAlpha=Math.max(0,q.life/q.ml);cx.fillStyle=q.col;cx.beginPath();cx.arc(q.x,q.y,q.sz,0,Math.PI*2);cx.fill();
    if(q.life>0)ap.push(q);}particles=ap;cx.globalAlpha=1;
  // Floating Messages (World Space)
  var am=[];var eduTips=[];
  for(var j=0;j<fmsgs.length;j++){
    var m=fmsgs[j];m.y-=0.25;m.life--;
    if(m.isEduTip){
      eduTips.push(m);
    }else{
      cx.globalAlpha=Math.min(1,Math.max(0,m.life/30));
      cx.fillStyle='#ffd93d';cx.font="bold 11px "+FNT;cx.textAlign='center';cx.fillText(m.text,m.x,m.y);
    }
    if(m.life>0)am.push(m);
  }
  fmsgs=am;cx.globalAlpha=1;
  
  cx.restore(); // Restore camera translation
  
  // Educational Tips (Screen Space)
  for(var j=0;j<eduTips.length;j++){
      var m = eduTips[j];
      cx.globalAlpha=Math.min(1,Math.max(0,m.life/60));
      var tx = cv.width/2; var ty = cv.height - 40;
      cx.fillStyle='rgba(0,0,0,0.75)';cx.fillRect(tx-180,ty-12,360,22);
      cx.fillStyle='#ffd93d';cx.font="bold 12px "+FNT;cx.textAlign='center';cx.fillText(m.text,tx,ty);
  }
  cx.globalAlpha=1;
  }else{cx.fillStyle='#fff';cx.font="18px "+FNT;cx.textAlign='center';cx.fillText('Nhấn BẮT ĐẦU để chơi!',cv.width/2,cv.height/2);}
"""
        content = content.replace(particle_and_msg_old + "\n  // MINI-MAP RADAR", particle_and_msg_new + "\n  // MINI-MAP RADAR")

    # 3. Remove MINI-MAP RADAR
    radar_pattern = re.compile(r"  // MINI-MAP RADAR\n  if\(map&&fogActive&&fogRadius<20\)\{.+?RADAR.+?\}\n", re.DOTALL)
    content = radar_pattern.sub("", content)

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

update_file(r"c:\Users\Hasky\.gemini\antigravity\scratch\fras\frontend\js\game-escape.js")
