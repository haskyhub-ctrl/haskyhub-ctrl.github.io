/* ============================================================
   FIRE ESCAPE GAME ENGINE v3 - Full Puzzle Mechanics
   8 mechanics: Electric, Gas, Fire Spread, Call 114,
   Hot Door, NPC Rescue, Blockage, Fog of War
   ============================================================ */
(function(){
'use strict';
var T=40,C=21,R=15,cv=document.getElementById('game-canvas'),cx=cv.getContext('2d');
cv.width=C*T;cv.height=R*T;

// Tile IDs
var F=0,W=1,FIRE=2,SMK=3,EXIT=4,BCC=5,TWL=6,MSK=7,KEY=8,DLCK=9,TOX=10,
PS=11,FUR=12,ELEC=13,BRKR=14,GASL=15,GASV=16,PHONE=17,HDOOR=18,SDOOR=19,
NPC=20,BLCK=21,EXITL=22;

// State
var p={x:1,y:1},inv={bcc:false,twl:false,msk:false,key:false},
lv=0,sc=0,hp=3,tm=90,run=false,tick=0,tInt=null,
breakerOff=false,gasOff=false,called114=false,
npcFollow=false,npcPos=null,npcSaved=false,
fogActive=false,crouching=false,
fireSpreadRate=0,fireSpreadTick=0,
particles=[],fmsgs=[],map=null;

// Levels defined in game-levels.js
var LEVELS=window.GAME_LEVELS||[];

function loadLv(i){
  if(!window.GAME_LEVELS)LEVELS=window.GAME_LEVELS||[];
  if(i>=LEVELS.length){winAll();return;}
  var L=LEVELS[i];lv=i;tm=L.time;
  inv={bcc:false,twl:false,msk:false,key:false};
  breakerOff=false;gasOff=false;called114=false;
  npcFollow=false;npcPos=null;npcSaved=false;
  fogActive=false;crouching=false;
  // Difficulty scaling: increase fire spread rate with level progression
  var baseFireSpread = L.fireSpread||0;
  var levelBonus = Math.floor(lv * 0.5); // Increase by 0.5 per level
  fireSpreadRate = Math.max(1, baseFireSpread + levelBonus);
  fireSpreadTick=0;
  particles=[];fmsgs=[];
  map=[];
  for(var r=0;r<L.map.length;r++){map[r]=[];for(var c=0;c<L.map[r].length;c++)map[r][c]=L.map[r][c];}
  for(var r2=0;r2<R;r2++)for(var c2=0;c2<C;c2++){
    if(map[r2][c2]===PS){p={x:c2,y:r2};map[r2][c2]=F;}
    if(map[r2][c2]===NPC){npcPos={x:c2,y:r2};}
  }
  updHUD();updInv();
  document.getElementById('hud-level').textContent=i+1;
  document.getElementById('level-objective').textContent=L.nameVi;
  showOvl('Màn '+(i+1)+': '+L.nameVi,L.tip,'BẮT ĐẦU',function(){hideOvl();run=true;startTm();});
}

function startTm(){clearInterval(tInt);tInt=setInterval(function(){
  if(!run)return;tm--;
  document.getElementById('hud-timer').textContent=tm;
  if(tm<=10)document.getElementById('hud-timer').style.color='#ff4444';
  if(tm<=0)die('Hết thời gian! Bạn không kịp thoát ra.');
  // Check if player is on fire before spreading
  if(map[p.y]&&map[p.y][p.x]===FIRE)die('Lửa đã lan đến vị trí của bạn!');
  // Fire spread
  if(fireSpreadRate>0){fireSpreadTick++;if(fireSpreadTick>=fireSpreadRate){fireSpreadTick=0;spreadFire();}}
},1000);}

function spreadFire(){
  var newFire=[];
  for(var r=0;r<R;r++)for(var c=0;c<C;c++){
    if(map[r][c]===FIRE){
      var nb=[[c-1,r],[c+1,r],[c,r-1],[c,r+1]];
      for(var n=0;n<nb.length;n++){
        var nx=nb[n][0],ny=nb[n][1];
        if(nx>=0&&nx<C&&ny>=0&&ny<R&&map[ny][nx]===F&&Math.random()<0.3)
          newFire.push([ny,nx]);
      }
    }
  }
  for(var f=0;f<newFire.length;f++)map[newFire[f][0]][newFire[f][1]]=FIRE;
  // Check if player is surrounded
  if(map[p.y]&&map[p.y][p.x]===FIRE)die('Lửa đã lan đến vị trí của bạn!');
}

function updHUD(){
  document.getElementById('hud-score').textContent=sc;
  document.getElementById('hud-timer').textContent=tm;
  document.getElementById('hud-timer').style.color='#ff6b6b';
  document.getElementById('hud-lives').textContent=hp;
}
function updInv(){
  sSlot('inv-extinguisher',inv.bcc,'BCC');
  sSlot('inv-towel',inv.twl,'KƯ');
  sSlot('inv-mask',inv.msk,'MN');
  sSlot('inv-key',inv.key,'CK');
}
function sSlot(id,has,lb){var e=document.getElementById(id);if(!e)return;
  if(has){e.textContent=lb;e.classList.add('active');e.classList.remove('empty');}
  else{e.textContent='';e.classList.remove('active');e.classList.add('empty');}
}

function showOvl(t,tx,bt,fn){
  document.getElementById('msg-icon').textContent='';
  document.getElementById('msg-title').textContent=t;
  document.getElementById('msg-text').textContent=tx;
  document.getElementById('msg-tip').style.display='none';
  var b=document.getElementById('msg-buttons');b.innerHTML='';
  var bn=document.createElement('button');bn.className='game-btn game-btn-primary';
  bn.textContent=bt;bn.onclick=fn;b.appendChild(bn);
  document.getElementById('msg-overlay').classList.add('visible');
}
function showOvlTip(t,tx,tip,bt,fn){
  document.getElementById('msg-icon').textContent='';
  document.getElementById('msg-title').textContent=t;
  document.getElementById('msg-text').textContent=tx;
  var tp=document.getElementById('msg-tip');tp.innerHTML=tip;tp.style.display=tip?'block':'none';
  var b=document.getElementById('msg-buttons');b.innerHTML='';
  var bn=document.createElement('button');bn.className='game-btn game-btn-primary';
  bn.textContent=bt;bn.onclick=fn;b.appendChild(bn);
  document.getElementById('msg-overlay').classList.add('visible');
}
function hideOvl(){document.getElementById('msg-overlay').classList.remove('visible');}

function die(reason){
  run=false;clearInterval(tInt);hp--;updHUD();
  if(hp<=0){showOvlTip('GAME OVER!',reason,'<strong>Bài học:</strong> Luôn bình tĩnh và chuẩn bị trước khi hành động trong đám cháy.','CHƠI LẠI',function(){hp=3;sc=0;hideOvl();loadLv(0);});}
  else{showOvl('Mất mạng! (Còn '+hp+')',reason,'THỬ LẠI',function(){hideOvl();loadLv(lv);});}
}

function winLv(){
  run=false;clearInterval(tInt);
  var bonus=tm*2+(npcSaved?200:0);sc+=bonus;updHUD();
  var tips=['<strong>Bài học:</strong> Tìm bình chữa cháy → Kéo chốt → Hướng vào gốc lửa → Quét trái phải.',
    '<strong>Bài học:</strong> Trong khói: cúi thấp, bịt mũi bằng khăn ướt, men theo tường.',
    '<strong>Bài học:</strong> Ngắt điện và khóa gas TRƯỚC KHI chữa cháy!',
    '<strong>Bài học:</strong> Gọi 114 ngay! Lửa lan rất nhanh, mỗi giây đều quan trọng.',
    '<strong>Bài học:</strong> Tổng hợp: Ngắt điện → Khóa gas → Dùng BCC → Khăn ướt → Gọi 114 → Cứu người → Thoát!'];
  var npcMsg=npcSaved?' Bonus cứu người: +200!':'';
  if(lv+1>=LEVELS.length){
    showOvlTip('CHIẾN THẮNG!','Điểm: '+sc+npcMsg,tips[lv]||tips[0],'CHƠI LẠI',function(){hp=3;sc=0;hideOvl();loadLv(0);});
  }else{
    showOvlTip('THOÁT NẠN THÀNH CÔNG!','Thưởng: +'+bonus+' điểm'+npcMsg,tips[lv]||tips[0],'MÀN TIẾP',function(){hideOvl();loadLv(lv+1);});
  }
}
function winAll(){winLv();}

function spark(gx,gy,col,n){for(var i=0;i<n;i++)particles.push({x:gx*T+T/2,y:gy*T+T/2,vx:(Math.random()-.5)*5,vy:(Math.random()-.5)*5,life:25+Math.random()*20,ml:45,col:col,sz:2+Math.random()*4});}
function fmsg(gx,gy,t){fmsgs.push({x:gx*T+T/2,y:gy*T,text:t,life:50});}

// Show temporary educational tip
function showEduTip(tip){
  // Clear any existing educational tips
  fmsgs = fmsgs.filter(function(msg){return !msg.isEduTip;});
  // Add new educational tip with longer life
  fmsgs.push({x:cv.width/2,y:cv.height-40,text:tip,life:120,isEduTip:true});
}

// ==================== INTERACTION (Space/Enter) ====================
function interact(){
  if(!run||!map)return;
  // Check adjacent tiles for interactable objects
  var dirs=[[0,-1],[0,1],[-1,0],[1,0]];
  for(var i=0;i<dirs.length;i++){
    var nx=p.x+dirs[i][0],ny=p.y+dirs[i][1];
    if(nx<0||nx>=C||ny<0||ny>=R)continue;
    var t=map[ny][nx];
    // Circuit breaker
    if(t===BRKR&&!breakerOff){
      breakerOff=true;sc+=30;
      // Remove all ELEC tiles
      for(var r=0;r<R;r++)for(var c=0;c<C;c++)if(map[r][c]===ELEC)map[r][c]=F;
      spark(nx,ny,'#ffff00',15);fmsg(nx,ny,'Ngat dien!');updHUD();
      showEduTip('<strong>Bài học:</strong> Luôn ngắt điện trước khi tiếp近 dây điện!');
      return;
    }
    // Gas valve
    if(t===GASV&&!gasOff){
      gasOff=true;sc+=30;
      // Remove all GAS_LEAK tiles
      for(var r=0;r<R;r++)for(var c=0;c<C;c++)if(map[r][c]===GASL)map[r][c]=F;
      spark(nx,ny,'#00ffaa',12);fmsg(nx,ny,'Khoa gas!');updHUD();
      showEduTip('<strong>Bài học:</strong> Khóa van gas TRƯỚC KHI dập lửa gần nguồn gas!');
      return;
    }
    // Phone - call 114
    if(t===PHONE&&!called114){
      called114=true;sc+=50;
      // Unlock EXITL tiles
      for(var r=0;r<R;r++)for(var c=0;c<C;c++)if(map[r][c]===EXITL)map[r][c]=EXIT;
      spark(nx,ny,'#4fc3f7',15);fmsg(nx,ny,'Goi 114!');updHUD();
      showEduTip('<strong>Bài học:</strong> Luôn gọi 114 ngay khi phát hiện cháy - mỗi giây đều quan trọng!');
      return;
    }
    // Hot door - check
    if(t===HDOOR){
      fmsg(nx,ny,'Cua NONG! Khong mo!');
      showEduTip('<strong>Bài học:</strong> Luôn kiểm tra nhiệt độ cửa trước khi mở - cửa nóng = đám cháy phía sau!');
      die('Cửa rất nóng — phía sau đang cháy dữ dội! Phải đi đường khác.');return;
    }
    // Safe door - open
    if(t===SDOOR){
      map[ny][nx]=F;sc+=20;spark(nx,ny,'#10b981',8);fmsg(nx,ny,'Cua an toan!');updHUD();return;
    }
    // Blockage - push/remove
    if(t===BLCK){
      map[ny][nx]=F;sc+=20;
      spark(nx,ny,'#a0522d',10);fmsg(nx,ny,'Don do vat!');updHUD();
      showEduTip('<strong>Bài học:</strong> Luôn giữ lối thoát thoáng rộng, không để đồ đạc chặn đường!');
      return;
    }
  }
}

// ==================== MOVEMENT ====================
function move(dx,dy){
  if(!run||!map)return;
  var nx=p.x+dx,ny=p.y+dy;
  if(nx<0||nx>=C||ny<0||ny>=R)return;
  var t=map[ny][nx];
  // Solid blocks
  if(t===W||t===FUR||t===BLCK||t===BRKR||t===GASV||t===PHONE||t===HDOOR||t===SDOOR)return;
  // Electric - needs breaker off
  if(t===ELEC){if(!breakerOff){die('Bị điện giật! Phải tìm và ngắt cầu dao trước.');return;}else{map[ny][nx]=F;}}
  // Gas leak - can walk but fire nearby = explosion
  if(t===GASL){if(!gasOff){die('Khí gas bùng cháy! Phải khóa van gas trước.');return;}}
  // Fire
  if(t===FIRE){
    if(inv.bcc){map[ny][nx]=F;inv.bcc=false;sc+=50;spark(nx,ny,'#87ceeb',15);fmsg(nx,ny,'+50 Dap lua!');updInv();
      showEduTip('<strong>Bài học:</strong> Chỉ dùng bình chữa cháy khi đã tắt điện và khóa gas!');
      return;
    }else{die('Đi vào đám cháy mà không có bình chữa cháy!');}return;
  }
  // Smoke
  if(t===SMK){
    if(inv.twl){p.x=nx;p.y=ny;crouching=true;fogActive=true;sc+=20;updHUD();
      showEduTip('<strong>Bài học:</strong> Trong khói: cúi thấp, dùng khăn ướt bít mũi, theo tường để tìm lối ra!');
      return;
    }else{die('Hít phải khói độc! Cần khăn ướt bịt mũi miệng.');}return;
  }
  // Toxic
  if(t===TOX){
    if(inv.msk){p.x=nx;p.y=ny;sc+=30;updHUD();
      showEduTip('<strong>Bài học:</strong> Khi gặp khí độc, luôn dùng mặt nạ phòng độc!');
      return;
    }else{die('Khí độc! Cần mặt nạ phòng độc.');}return;
  }
  // Locked door
  if(t===DLCK){
    if(inv.key){map[ny][nx]=F;inv.key=false;sc+=40;spark(nx,ny,'#ffd93d',12);fmsg(nx,ny,'Mo khoa!');updInv();
      showEduTip('<strong>Bài học:</strong> Luôn mang theo chìa khóa để mở đường thoát trong trường hợp khẩn cấp!');
      return;
    }else{fmsg(nx,ny,'Can chia khoa!');}return;
  }
  // Locked exit (need 114)
  if(t===EXITL){fmsg(nx,ny,'Phai goi 114 truoc!');return;}
  // Pickups
  if(t===BCC){inv.bcc=true;spark(nx,ny,'#ff6b35',10);fmsg(nx,ny,'Binh chua chay!');sc+=10;map[ny][nx]=F;
    showEduTip('<strong>Bài học:</strong> Bình chữa cháy là thiết bị đầu tiên cần tìm trong trường hợp cháy!');
    return;
  }
  if(t===TWL){inv.twl=true;spark(nx,ny,'#87ceeb',10);fmsg(nx,ny,'Khan uot!');sc+=10;map[ny][nx]=F;
    showEduTip('<strong>Bài học:</strong> Khăn ướt giúp bảo vệ hô hấp khi phải đi qua khu vực khói!');
    return;
  }
  if(t===MSK){inv.msk=true;spark(nx,ny,'#a0a0ff',10);fmsg(nx,ny,'Mat na!');sc+=10;map[ny][nx]=F;
    showEduTip('<strong>Bài học:</strong> Mặt nạ phòng độc bảo vệ khỏi khí độc và khói!');
    return;
  }
  if(t===KEY){inv.key=true;spark(nx,ny,'#ffd93d',10);fmsg(nx,ny,'Chia khoa!');sc+=10;map[ny][nx]=F;
    showEduTip('<strong>Bài học:</strong> Luôn kiểm tra và mang theo chìa khóa khi thoát hiểm!');
    return;
  }
  // NPC
  if(t===NPC){npcFollow=true;map[ny][nx]=F;sc+=50;spark(nx,ny,'#ff69b4',15);fmsg(nx,ny,'Cuu nguoi! Di den EXIT!');updHUD();return;}

  if(t!==SMK){crouching=false;fogActive=false;}
  p.x=nx;p.y=ny;
  // NPC follows
  if(npcFollow&&npcPos){npcPos={x:p.x-dx,y:p.y-dy};}
  updInv();updHUD();
  // Exit
  if(t===EXIT){
    if(npcFollow)npcSaved=true;
    winLv();
  }
}

// Keyboard
document.addEventListener('keydown',function(e){
  switch(e.key){
    case'ArrowUp':case'w':case'W':e.preventDefault();move(0,-1);break;
    case'ArrowDown':case's':case'S':e.preventDefault();move(0,1);break;
    case'ArrowLeft':case'a':case'A':e.preventDefault();move(-1,0);break;
    case'ArrowRight':case'd':case'D':e.preventDefault();move(1,0);break;
    case' ':case'Enter':e.preventDefault();interact();break;
  }
});
// Mobile
var mb=document.querySelectorAll('.ctrl-btn');
for(var i=0;i<mb.length;i++){(function(b){
  var d={up:[0,-1],down:[0,1],left:[-1,0],right:[1,0]},dir=d[b.getAttribute('data-dir')];
  if(dir){b.addEventListener('touchstart',function(e){e.preventDefault();move(dir[0],dir[1]);});
  b.addEventListener('click',function(){move(dir[0],dir[1]);});}
})(mb[i]);}

// ==================== RENDERING ====================
function dFloor(x,y){cx.fillStyle='#2a2d3e';cx.fillRect(x,y,T,T);cx.strokeStyle='#33364a';cx.lineWidth=.5;cx.strokeRect(x,y,T,T);}
function dWall(x,y){cx.fillStyle='#5c5f7a';cx.fillRect(x,y,T,T);cx.fillStyle='#6b6f8a';cx.fillRect(x+1,y+1,T-2,T/2-2);cx.strokeStyle='#44475a';cx.lineWidth=1;cx.strokeRect(x,y,T,T);}
function dFurn(x,y){dFloor(x,y);cx.fillStyle='#8b6914';cx.fillRect(x+5,y+5,T-10,T-10);cx.strokeStyle='#a07d1e';cx.strokeRect(x+5,y+5,T-10,T-10);}

function dFire(x,y){dFloor(x,y);
  var t=tick;cx.fillStyle='rgba(255,80,0,0.3)';cx.fillRect(x+2,y+2,T-4,T-4);
  cx.fillStyle='#ff4400';cx.beginPath();
  cx.moveTo(x+6,y+T-2);cx.quadraticCurveTo(x+4,y+14+Math.sin(t*.15)*4,x+T*.35,y+4+Math.sin(t*.2)*3);
  cx.quadraticCurveTo(x+T/2,y-2+Math.cos(t*.18)*2,x+T*.65,y+4+Math.sin(t*.15+1)*3);
  cx.quadraticCurveTo(x+T-4,y+14+Math.cos(t*.15)*4,x+T-6,y+T-2);cx.closePath();cx.fill();
  cx.fillStyle='#ffcc00';cx.beginPath();
  cx.moveTo(x+12,y+T-4);cx.quadraticCurveTo(x+10,y+20+Math.sin(t*.2)*3,x+T/2,y+10+Math.cos(t*.25)*2);
  cx.quadraticCurveTo(x+T-10,y+20+Math.cos(t*.2)*3,x+T-12,y+T-4);cx.closePath();cx.fill();
  cx.fillStyle='#fff8e0';cx.beginPath();cx.ellipse(x+T/2,y+T*.65,5,8+Math.sin(t*.3)*2,0,0,Math.PI*2);cx.fill();
  cx.fillStyle='#fff';cx.font='bold 8px sans-serif';cx.textAlign='center';cx.fillText('LỬA',x+T/2,y+T-2);
}
function dSmoke(x,y){dFloor(x,y);var t=tick;
  for(var i=0;i<4;i++){var ox=Math.sin(t*.04+i*1.5)*5,oy=Math.cos(t*.03+i*.8)*3;
    cx.fillStyle='rgba(180,180,190,'+(0.25+Math.sin(t*.02+i)*.08)+')';
    cx.beginPath();cx.ellipse(x+8+i*8+ox,y+10+i*6+oy,10+i*2,8+i,0,0,Math.PI*2);cx.fill();}
  cx.fillStyle='rgba(255,255,255,0.5)';cx.font='bold 8px sans-serif';cx.textAlign='center';cx.fillText('KHÓI',x+T/2,y+T-2);
}
function dToxic(x,y){dFloor(x,y);var a=.25+Math.sin(tick*.05)*.1;
  cx.fillStyle='rgba(80,220,0,'+a+')';cx.fillRect(x+2,y+2,T-4,T-4);
  cx.fillStyle='#0f0';cx.beginPath();cx.arc(x+T/2,y+T/2-3,10,0,Math.PI*2);cx.fill();
  cx.fillStyle='#000';cx.fillRect(x+T/2-6,y+T/2-6,4,4);cx.fillRect(x+T/2+2,y+T/2-6,4,4);
  cx.fillStyle='#0f0';cx.font='bold 8px sans-serif';cx.textAlign='center';cx.fillText('ĐỘC',x+T/2,y+T-2);
}
function dExit(x,y){dFloor(x,y);var g=.4+Math.sin(tick*.08)*.2;
  cx.fillStyle='rgba(16,185,129,'+g+')';cx.fillRect(x+2,y+2,T-4,T-4);
  cx.strokeStyle='#10b981';cx.lineWidth=2;cx.strokeRect(x+3,y+3,T-6,T-6);cx.lineWidth=1;
  cx.fillStyle='#10b981';cx.fillRect(x+12,y+6,16,24);cx.fillStyle='#fff';cx.fillRect(x+24,y+18,3,3);
  cx.fillStyle='#fff';cx.font='bold 9px sans-serif';cx.textAlign='center';cx.fillText('EXIT',x+T/2,y+T-4);
}
function dExitL(x,y){dFloor(x,y);
  cx.fillStyle='rgba(255,50,50,0.2)';cx.fillRect(x+2,y+2,T-4,T-4);
  cx.strokeStyle='#ff4444';cx.lineWidth=2;cx.strokeRect(x+3,y+3,T-6,T-6);cx.lineWidth=1;
  cx.fillStyle='#ff4444';cx.font='bold 7px sans-serif';cx.textAlign='center';
  cx.fillText('GỌI',x+T/2,y+T/2-4);cx.fillText('114',x+T/2,y+T/2+6);
}
function dBCC(x,y){dFloor(x,y);var b=Math.sin(tick*.1)*2;
  cx.fillStyle='#e63946';cx.fillRect(x+13,y+10+b,14,20);cx.fillStyle='#333';cx.fillRect(x+16,y+6+b,8,6);
  cx.fillStyle='#ffd93d';cx.font='bold 7px sans-serif';cx.textAlign='center';cx.fillText('BCC',x+T/2,y+T-3);
  cx.fillStyle='rgba(230,57,70,0.12)';cx.beginPath();cx.arc(x+T/2,y+T/2,16,0,Math.PI*2);cx.fill();
}
function dTwl(x,y){dFloor(x,y);var b=Math.sin(tick*.1+1)*2;
  cx.fillStyle='#4fc3f7';cx.fillRect(x+8,y+12+b,24,6);cx.fillRect(x+10,y+18+b,20,8);
  cx.fillStyle='#4fc3f7';cx.font='bold 7px sans-serif';cx.textAlign='center';cx.fillText('KHĂN',x+T/2,y+T-3);
}
function dMask(x,y){dFloor(x,y);var b=Math.sin(tick*.1+2)*2;
  cx.fillStyle='#7e57c2';cx.beginPath();cx.ellipse(x+T/2,y+T/2+b-2,12,10,0,0,Math.PI*2);cx.fill();
  cx.fillStyle='#b39ddb';cx.fillRect(x+13,y+14+b,5,4);cx.fillRect(x+22,y+14+b,5,4);
  cx.fillStyle='#b39ddb';cx.font='bold 7px sans-serif';cx.textAlign='center';cx.fillText('M.NẠ',x+T/2,y+T-3);
}
function dKey(x,y){dFloor(x,y);var b=Math.sin(tick*.12)*2;
  cx.save();cx.translate(x+T/2,y+T/2+b);cx.rotate(Math.sin(tick*.05)*.2);
  cx.strokeStyle='#ffd93d';cx.lineWidth=2;cx.beginPath();cx.arc(-6,-4,6,0,Math.PI*2);cx.stroke();
  cx.fillStyle='#ffd93d';cx.fillRect(-2,-4,16,3);cx.fillRect(10,-1,3,5);cx.fillRect(6,-1,3,4);
  cx.restore();cx.fillStyle='#ffd93d';cx.font='bold 7px sans-serif';cx.textAlign='center';cx.fillText('KHÓA',x+T/2,y+T-3);
}
function dLock(x,y){cx.fillStyle='#5c5f7a';cx.fillRect(x,y,T,T);cx.fillStyle='#8b4513';cx.fillRect(x+4,y+2,T-8,T-4);
  cx.fillStyle='#ffd93d';cx.beginPath();cx.arc(x+T/2,y+T/2-4,6,0,Math.PI*2);cx.fill();
  cx.fillStyle='#333';cx.beginPath();cx.arc(x+T/2,y+T/2-4,3,0,Math.PI*2);cx.fill();
  cx.fillStyle='#ffd93d';cx.fillRect(x+T/2-5,y+T/2,10,10);cx.fillStyle='#333';cx.fillRect(x+T/2-1,y+T/2+3,2,4);
}
// New tile renderers
function dElec(x,y){dFloor(x,y);var t=tick;
  // Sparking wire
  cx.strokeStyle='#333';cx.lineWidth=3;cx.beginPath();cx.moveTo(x+2,y+T/2);cx.lineTo(x+T-2,y+T/2);cx.stroke();
  // Sparks
  if(Math.sin(t*.3)>0){cx.fillStyle='#ffff00';for(var i=0;i<3;i++){
    var sx=x+10+Math.random()*20,sy=y+T/2-5+Math.random()*10;
    cx.fillRect(sx,sy,3,3);}
  cx.fillStyle='rgba(255,255,0,0.15)';cx.fillRect(x,y,T,T);}
  cx.fillStyle='#ffff00';cx.font='bold 7px sans-serif';cx.textAlign='center';cx.fillText('ĐIỆN',x+T/2,y+T-2);
}
function dBrkr(x,y){dFloor(x,y);
  // Enhanced visual indicator for breaker state
  cx.fillStyle=breakerOff?'#2d5a27':'#5a2d2d'; // Dark green when OFF, dark red when ON
  cx.fillRect(x+8,y+4,24,32);
  cx.strokeStyle='#888';cx.strokeRect(x+8,y+4,24,32);

  // Switch lever - more prominent visualization
  cx.fillStyle=breakerOff?'#4caf50':'#f44336'; // Bright green when OFF, bright red when ON
  cx.fillRect(x+14,y+breakerOff?22:10,12,8);

  // Add ON/OFF text with background for better readability
  cx.fillStyle=breakerOff?'#ffffff':'#ffffff';
  cx.fillRect(x+10,y+breakerOff?28:6,8,8);
  cx.fillStyle='#000000';
  cx.font='bold 6px sans-serif';
  cx.textAlign='center';
  cx.fillText(breakerOff?'OFF':'ON',x+14,y+breakerOff?33:11);
}
function dGasL(x,y){dFloor(x,y);var t=tick,a=.2+Math.sin(t*.06)*.1;
  cx.fillStyle='rgba(255,165,0,'+a+')';cx.fillRect(x,y,T,T);
  // Gas bubbles
  for(var i=0;i<3;i++){cx.fillStyle='rgba(255,200,0,'+(0.3+Math.sin(t*.1+i)*.2)+')';
    cx.beginPath();cx.arc(x+8+i*12+Math.sin(t*.05+i)*3,y+12+i*7+Math.cos(t*.04+i)*3,4+i,0,Math.PI*2);cx.fill();}
  cx.fillStyle='#ffa500';cx.font='bold 7px sans-serif';cx.textAlign='center';cx.fillText('GAS',x+T/2,y+T-2);
}
function dGasV(x,y){dFloor(x,y);
  // Enhanced visual indicator for gas valve state
  cx.fillStyle=gasOff?'#2d5a27':'#5a2d2d'; // Dark green when OFF (closed), dark red when ON (open)
  cx.fillRect(x+8,y+4,24,32);
  cx.strokeStyle='#888';cx.strokeRect(x+8,y+4,24,32);

  // Valve handle - more prominent visualization
  cx.fillStyle=gasOff?'#4caf50':'#f44336'; // Bright green when OFF (closed), bright red when ON (open)
  cx.beginPath();
  cx.arc(x+T/2,y+T/2,8,0,Math.PI*2);
  cx.fill();

  // Add OPEN/CLOSED text with background for better readability
  cx.fillStyle=gasOff?'#ffffff':'#ffffff';
  cx.fillRect(x+10,y+28,8,8);
  cx.fillStyle='#000000';
  cx.font='bold 6px sans-serif';
  cx.textAlign='center';
  cx.fillText(gasOff?'ĐÓNG':'MỞ',x+T/2,y+T-3);
}
function dPhone(x,y){dFloor(x,y);var g=called114?'#10b981':'rgba(79,195,247,'+(0.5+Math.sin(tick*.1)*.3)+')';
  cx.fillStyle=g;cx.fillRect(x+12,y+6,16,22);cx.fillStyle='#333';cx.fillRect(x+14,y+8,12,12);
  cx.fillStyle=called114?'#10b981':'#4fc3f7';cx.beginPath();cx.arc(x+T/2,y+24,4,0,Math.PI*2);cx.fill();
  cx.fillStyle=called114?'#10b981':'#fff';cx.font='bold 7px sans-serif';cx.textAlign='center';
  cx.fillText(called114?'OK':'114',x+T/2,y+T-2);
}
function dHDoor(x,y){cx.fillStyle='#8b0000';cx.fillRect(x,y,T,T);cx.fillStyle='#a52a2a';cx.fillRect(x+3,y+2,T-6,T-4);
  // Heat waves
  var t=tick;for(var i=0;i<3;i++){cx.strokeStyle='rgba(255,100,0,'+(0.3+Math.sin(t*.1+i)*.2)+')';cx.lineWidth=1;
    cx.beginPath();cx.moveTo(x+8+i*8,y+5+Math.sin(t*.15+i)*3);cx.quadraticCurveTo(x+12+i*8,y-2+Math.cos(t*.12+i)*3,x+16+i*8,y+5+Math.sin(t*.15+i+1)*3);cx.stroke();}
  cx.fillStyle='#ff6600';cx.font='bold 7px sans-serif';cx.textAlign='center';cx.fillText('NÓNG!',x+T/2,y+T-2);
}
function dSDoor(x,y){cx.fillStyle='#4a6741';cx.fillRect(x,y,T,T);cx.fillStyle='#5a7a50';cx.fillRect(x+3,y+2,T-6,T-4);
  cx.fillStyle='#fff';cx.fillRect(x+T-10,y+T/2-2,4,4);
  cx.fillStyle='#90ee90';cx.font='bold 6px sans-serif';cx.textAlign='center';cx.fillText('KIỂM',x+T/2,y+T/2-4);cx.fillText('TRA',x+T/2,y+T/2+5);
}
function dNPC(x,y){dFloor(x,y);
  cx.fillStyle='#ff69b4';cx.beginPath();cx.arc(x+T/2,y+12,8,0,Math.PI*2);cx.fill();
  cx.fillStyle='#ffb6c1';cx.fillRect(x+12,y+18,16,14);
  cx.fillStyle='#333';cx.fillRect(x+T/2-5,y+10,3,3);cx.fillRect(x+T/2+2,y+10,3,3);
  cx.fillStyle='#ff69b4';cx.font='bold 7px sans-serif';cx.textAlign='center';cx.fillText('CỨU!',x+T/2,y+T-2);
  // Help animation
  if(Math.sin(tick*.15)>0){cx.fillStyle='#ff0';cx.font='bold 9px sans-serif';cx.fillText('!',x+T/2+12,y+8);}
}
function dBlck(x,y){dFloor(x,y);
  cx.fillStyle='#6d4c41';cx.fillRect(x+3,y+3,T-6,T-6);cx.fillStyle='#8d6e63';cx.fillRect(x+3,y+3,T-6,T/2-3);
  cx.fillStyle='#5d4037';cx.fillRect(x+6,y+T/2,T-12,T/2-5);
  cx.strokeStyle='#4e342e';cx.strokeRect(x+3,y+3,T-6,T-6);
  cx.fillStyle='#ffcc80';cx.font='bold 6px sans-serif';cx.textAlign='center';cx.fillText('DỜI',x+T/2,y+T-2);
}

function dTile(c,r){
  if(!map||!map[r])return;var t=map[r][c],x=c*T,y=r*T;
  switch(t){
    case F:dFloor(x,y);break;case W:dWall(x,y);break;case FUR:dFurn(x,y);break;
    case FIRE:dFire(x,y);break;case SMK:dSmoke(x,y);break;case TOX:dToxic(x,y);break;
    case EXIT:dExit(x,y);break;case EXITL:dExitL(x,y);break;
    case BCC:dBCC(x,y);break;case TWL:dTwl(x,y);break;case MSK:dMask(x,y);break;case KEY:dKey(x,y);break;
    case DLCK:dLock(x,y);break;case ELEC:dElec(x,y);break;case BRKR:dBrkr(x,y);break;
    case GASL:dGasL(x,y);break;case GASV:dGasV(x,y);break;case PHONE:dPhone(x,y);break;
    case HDOOR:dHDoor(x,y);break;case SDOOR:dSDoor(x,y);break;
    case NPC:dNPC(x,y);break;case BLCK:dBlck(x,y);break;
    default:dFloor(x,y);
  }
}

function dPlayer(){
  if(!map)return;var x=p.x*T,y=p.y*T;
  cx.fillStyle='rgba(0,0,0,0.3)';cx.beginPath();cx.ellipse(x+T/2,y+T-4,12,4,0,0,Math.PI*2);cx.fill();
  if(crouching){cx.fillStyle='#ffd93d';cx.beginPath();cx.ellipse(x+T/2,y+T*.65,14,9,0,0,Math.PI*2);cx.fill();
    cx.fillStyle='#ffecb3';cx.beginPath();cx.arc(x+T/2-6,y+T*.5,7,0,Math.PI*2);cx.fill();
  }else{cx.fillStyle='#ffd93d';cx.fillRect(x+11,y+16,18,16);
    cx.fillStyle='#ffecb3';cx.beginPath();cx.arc(x+T/2,y+12,9,0,Math.PI*2);cx.fill();
    cx.fillStyle='#333';cx.fillRect(x+16,y+10,3,3);cx.fillRect(x+22,y+10,3,3);
    cx.fillStyle='#1565c0';cx.fillRect(x+13,y+30,6,6);cx.fillRect(x+21,y+30,6,6);}
  cx.fillStyle='rgba(255,215,61,0.08)';cx.beginPath();cx.arc(x+T/2,y+T/2,T*.8,0,Math.PI*2);cx.fill();
}
function dNPCFollow(){
  if(!npcFollow||!npcPos)return;var x=npcPos.x*T,y=npcPos.y*T;
  cx.fillStyle='#ff69b4';cx.beginPath();cx.arc(x+T/2,y+14,7,0,Math.PI*2);cx.fill();
  cx.fillStyle='#ffb6c1';cx.fillRect(x+14,y+19,12,12);
  cx.fillStyle='#ff69b4';cx.font='bold 7px sans-serif';cx.textAlign='center';cx.fillText('♥',x+T/2,y+T-2);
}

function render(){
  tick++;cx.clearRect(0,0,cv.width,cv.height);cx.fillStyle='#1a1a2e';cx.fillRect(0,0,cv.width,cv.height);
  if(map){
    // Fog of war: in smoke, only see nearby tiles
    if(fogActive){
      for(var r=0;r<R;r++)for(var c=0;c<C;c++){
        var dist=Math.abs(c-p.x)+Math.abs(r-p.y);
        if(dist<=3)dTile(c,r);
        else{cx.fillStyle='rgba(100,100,110,0.85)';cx.fillRect(c*T,r*T,T,T);}
      }
    }else{
      for(var r=0;r<R;r++)for(var c=0;c<C;c++)dTile(c,r);
    }
    dNPCFollow();dPlayer();
  }else{cx.fillStyle='#fff';cx.font='18px sans-serif';cx.textAlign='center';cx.fillText('Nhấn BẮT ĐẦU để chơi!',cv.width/2,cv.height/2);}
  // Particles & msgs
  var ap=[];for(var i=0;i<particles.length;i++){var q=particles[i];q.x+=q.vx;q.y+=q.vy;q.life--;q.sz*=.96;
    cx.globalAlpha=Math.max(0,q.life/q.ml);cx.fillStyle=q.col;cx.beginPath();cx.arc(q.x,q.y,q.sz,0,Math.PI*2);cx.fill();
    if(q.life>0)ap.push(q);}particles=ap;cx.globalAlpha=1;
  var am=[];for(var j=0;j<fmsgs.length;j++){var m=fmsgs[j];m.y-=.8;m.life--;
    // Educational tips have different styling
    if(m.isEduTip){
      cx.globalAlpha=Math.max(0,m.life/120);
      cx.fillStyle='#ffff00';
      cx.font='bold 14px sans-serif';
      cx.textAlign='center';
      cx.fillText(m.text,m.x,m.y);
    } else {
      cx.globalAlpha=Math.max(0,m.life/50);
      cx.fillStyle='#ffd93d';
      cx.font='bold 11px sans-serif';
      cx.textAlign='center';
      cx.fillText(m.text,m.x,m.y);
    }
    if(m.life>0)am.push(m);}fmsgs=am;cx.globalAlpha=1;
  requestAnimationFrame(render);
}

window.startGame=function(){hideOvl();loadLv(0);};
// Wait for levels to load
function init(){
  if(window.GAME_LEVELS){LEVELS=window.GAME_LEVELS;
    showOvl('Thoát khỏi đám cháy','Di chuyển: ↑↓←→ hoặc WASD\nTương tác: Space hoặc Enter\n\nThu thập vật phẩm, giải đố và tìm lối thoát!','BẮT ĐẦU CHƠI',function(){hideOvl();loadLv(0);});
  }else{setTimeout(init,100);}
}
init();render();
})();
