/* ============================================================
   FIRE ESCAPE GAME ENGINE v4 - Complete Redesign
   Camera system, proper item mechanics, fog of war
   ============================================================ */
(function () {
  'use strict';

  // --- Constants ---
  var T = 36;            // Tile size px
  var VIEW_COLS = 25;    // Viewport columns (canvas = 900px)
  var VIEW_ROWS = 19;    // Viewport rows   (canvas = 684px)

  // Tile IDs (must match game-levels.js)
  var F = 0, W = 1, FIRE = 2, SMK = 3, EXIT = 4,
      BCC = 5, TWL = 6, MSK = 7, KEY = 8, DLCK = 9,
      TOX = 10, PS = 11, FUR = 12, ELEC = 13, BRKR = 14,
      GASL = 15, GASV = 16, PHONE = 17, HDOOR = 18, SDOOR = 19,
      NPC = 20, BLCK = 21, EXITL = 22;

  // --- Canvas ---
  var cv = document.getElementById('game-canvas');
  var cx = cv.getContext('2d');

  // --- State ---
  var p = { x: 1, y: 1 };          // Player map position
  var pDir = { dx: 1, dy: 0 };     // Last move direction (for BCC aim)
  var inv = { bcc: false, twl: false, msk: false, key: false };
  var bccCharges = 0;               // 0-5
  var twlTimeMs = 0;                // ms remaining for wet towel in smoke
  var TWL_DURATION = 10000;         // 10 seconds
  var BCC_MAX = 5;

  var lv = 0, sc = 0, hp = 3, tm = 90, run = false;
  var tick = 0, tInt = null, fireInt = null;

  // Camera (top-left map tile visible)
  var camTX = 0, camTY = 0;

  // Map dimensions (set per level)
  var mapW = VIEW_COLS, mapH = VIEW_ROWS;
  var map = null;

  // Misc state
  var breakerOff = false, gasOff = false, called114 = false;
  var npcFollow = false, npcPos = null, npcSaved = false;
  var crouching = false;
  var particles = [], fmsgs = [];

  // --- Level data ---
  var LEVELS = window.GAME_LEVELS || [];

  // ==================== LEVEL LOADING ====================
  function loadLv(i) {
    if (!window.GAME_LEVELS) LEVELS = window.GAME_LEVELS || [];
    if (i >= LEVELS.length) { winAll(); return; }
    var L = LEVELS[i]; lv = i;
    tm = L.time || 120;

    // Reset state
    inv = { bcc: false, twl: false, msk: false, key: false };
    bccCharges = 0;
    twlTimeMs = 0;
    breakerOff = false; gasOff = false; called114 = false;
    npcFollow = false; npcPos = null; npcSaved = false;
    crouching = false;
    particles = []; fmsgs = [];

    // Set map dimensions from level data
    mapW = (L.mapW) || VIEW_COLS;
    mapH = (L.mapH) || VIEW_ROWS;

    // Deep-copy map
    map = [];
    for (var r = 0; r < mapH; r++) {
      map[r] = [];
      for (var c = 0; c < mapW; c++) {
        map[r][c] = (L.map[r] && L.map[r][c] !== undefined) ? L.map[r][c] : W;
      }
    }

    // Find player start and NPC
    for (var r2 = 0; r2 < mapH; r2++) {
      for (var c2 = 0; c2 < mapW; c2++) {
        if (map[r2][c2] === PS) { p = { x: c2, y: r2 }; map[r2][c2] = F; }
        if (map[r2][c2] === NPC) { npcPos = { x: c2, y: r2 }; }
      }
    }

    updateCamera();
    updHUD(); updInv();
    document.getElementById('hud-level').textContent = i + 1;
    document.getElementById('level-objective').textContent = L.nameVi || '';

    // Stop old timers
    clearInterval(tInt);
    clearInterval(fireInt);

    showOvlTip(
      'Man ' + (i + 1) + ': ' + (L.nameVi || ''),
      L.desc || 'Tim vat pham va loi thoat!',
      '<strong>Bai hoc:</strong> ' + (L.tip || 'Binh tinh, suy nghi roi hanh dong.'),
      'BAT DAU',
      function () { hideOvl(); run = true; startTimers(L); }
    );
  }

  function startTimers(L) {
    // Countdown timer (1 second)
    tInt = setInterval(function () {
      if (!run) return;
      tm--;
      document.getElementById('hud-timer').textContent = tm;
      document.getElementById('hud-timer').style.color = tm <= 10 ? '#ff2222' : '#ff6b6b';
      if (tm <= 0) die('Het thoi gian! Ban khong kip thoat ra.');
    }, 1000);

    // Fire spread (every 3 seconds)
    var spreadMs = (L.fireSpread || 3) * 1000;
    fireInt = setInterval(function () {
      if (!run) return;
      spreadFire();
      if (map[p.y] && map[p.y][p.x] === FIRE) die('Lua da lan den vi tri cua ban!');
    }, spreadMs);
  }

  function updateCamera() {
    var halfW = Math.floor(VIEW_COLS / 2);
    var halfH = Math.floor(VIEW_ROWS / 2);
    camTX = Math.max(0, Math.min(mapW - VIEW_COLS, p.x - halfW));
    camTY = Math.max(0, Math.min(mapH - VIEW_ROWS, p.y - halfH));
    // If map smaller than viewport, keep at 0
    if (mapW <= VIEW_COLS) camTX = 0;
    if (mapH <= VIEW_ROWS) camTY = 0;
  }

  // ==================== FIRE SPREAD ====================
  function spreadFire() {
    var newFire = [];
    for (var r = 0; r < mapH; r++) {
      for (var c = 0; c < mapW; c++) {
        if (map[r][c] === FIRE) {
          var nb = [[c - 1, r], [c + 1, r], [c, r - 1], [c, r + 1]];
          for (var n = 0; n < nb.length; n++) {
            var nx = nb[n][0], ny = nb[n][1];
            if (nx >= 0 && nx < mapW && ny >= 0 && ny < mapH) {
              var nt = map[ny][nx];
              var chance = nt === FUR ? 0.4 : nt === F ? 0.2 : 0;
              if (chance > 0 && Math.random() < chance) newFire.push([ny, nx]);
            }
          }
        }
      }
    }
    for (var f = 0; f < newFire.length; f++) map[newFire[f][0]][newFire[f][1]] = FIRE;
  }

  // ==================== HUD / INVENTORY ====================
  function updHUD() {
    document.getElementById('hud-score').textContent = sc;
    document.getElementById('hud-timer').textContent = tm;
    document.getElementById('hud-lives').textContent = hp;
  }

  function updInv() {
    slotSet('inv-extinguisher', inv.bcc, inv.bcc ? ('BCC ' + bccCharges + '/' + BCC_MAX) : '');
    slotSet('inv-towel', inv.twl, inv.twl ? ('TWL ' + Math.ceil(twlTimeMs / 1000) + 's') : '');
    slotSet('inv-mask', inv.msk, 'MSK');
    slotSet('inv-key', inv.key, 'KEY');
  }

  function slotSet(id, has, label) {
    var e = document.getElementById(id);
    if (!e) return;
    if (has) {
      e.textContent = label;
      e.classList.add('active');
      e.classList.remove('empty');
    } else {
      e.textContent = '';
      e.classList.remove('active');
      e.classList.add('empty');
    }
  }

  // ==================== OVERLAYS ====================
  function showOvl(title, text, btnText, fn) {
    document.getElementById('msg-icon').textContent = '';
    document.getElementById('msg-title').textContent = title;
    document.getElementById('msg-text').textContent = text;
    var tp = document.getElementById('msg-tip'); tp.style.display = 'none';
    var b = document.getElementById('msg-buttons'); b.innerHTML = '';
    var bn = document.createElement('button');
    bn.className = 'game-btn game-btn-primary';
    bn.textContent = btnText; bn.onclick = fn; b.appendChild(bn);
    document.getElementById('msg-overlay').classList.add('visible');
  }

  function showOvlTip(title, text, tip, btnText, fn) {
    document.getElementById('msg-icon').textContent = '';
    document.getElementById('msg-title').textContent = title;
    document.getElementById('msg-text').textContent = text;
    var tp = document.getElementById('msg-tip');
    tp.innerHTML = tip; tp.style.display = tip ? 'block' : 'none';
    var b = document.getElementById('msg-buttons'); b.innerHTML = '';
    var bn = document.createElement('button');
    bn.className = 'game-btn game-btn-primary';
    bn.textContent = btnText; bn.onclick = fn; b.appendChild(bn);
    document.getElementById('msg-overlay').classList.add('visible');
  }

  function hideOvl() {
    document.getElementById('msg-overlay').classList.remove('visible');
  }

  // ==================== GAME EVENTS ====================
  function die(reason) {
    run = false;
    clearInterval(tInt); clearInterval(fireInt);
    hp--; updHUD();
    if (hp <= 0) {
      showOvlTip('GAME OVER!', reason,
        '<strong>Bai hoc:</strong> Luon binh tinh va chuan bi truoc khi hanh dong trong dam chay.',
        'CHOI LAI', function () { hp = 3; sc = 0; hideOvl(); loadLv(0); });
    } else {
      showOvl('Mat mang! (Con ' + hp + ')', reason, 'THU LAI',
        function () { hideOvl(); loadLv(lv); });
    }
  }

  function winLv() {
    run = false;
    clearInterval(tInt); clearInterval(fireInt);
    var bonus = tm * 2 + (npcSaved ? 200 : 0);
    sc += bonus; updHUD();
    var lessonTips = [
      '<strong>Bai hoc:</strong> Tim binh chua chay -> Keo chot -> Huong vao goc lua -> Quet trai phai.',
      '<strong>Bai hoc:</strong> Trong khoi: cui thap, bit mui bang khan uot, men theo tuong.',
      '<strong>Bai hoc:</strong> Ngat dien va khoa gas TRUOC KHI chua chay!',
      '<strong>Bai hoc:</strong> Goi 114 ngay! Lua lan rat nhanh, moi giay deu quan trong.',
      '<strong>Bai hoc:</strong> Luon biet loi thoat hiem gan nhat trong toa nha ban dang o.',
      '<strong>Bai hoc:</strong> Khong dung thang may khi co chay. Luon dung cau thang bo.',
      '<strong>Bai hoc:</strong> Khoi gay chet nhieu hon lua. Cun thap khi di qua khoi.',
      '<strong>Bai hoc:</strong> Mat na phong doc bao ve khoi khi doc. Luon trang bi mat na.',
      '<strong>Bai hoc:</strong> Khoa cua lai khi thoat hiem de ngan lua lan.',
      '<strong>Bai hoc:</strong> Neu cua nong, khong mo! Tim loi thoat khac hoac chon an.',
      '<strong>Bai hoc:</strong> Lam mat tin hieu cuu tro khi bi ket - vay tai cua so.',
      '<strong>Bai hoc:</strong> Lap ke hoach thoat hiem cho gia dinh va luyen tap thuong xuyen.',
      '<strong>Bai hoc:</strong> Bao cao chay cho hang xom truoc khi thoat - co the cuu song ho.',
      '<strong>Bai hoc:</strong> Dung kem chong chay de bao ve ban than khi qua vung lua.',
      '<strong>Bai hoc:</strong> Ban da thong thao PCCC! Hay ap dung nhung ki nang nay trong thuc te.'
    ];
    var tip = lessonTips[lv] || lessonTips[0];
    var npcMsg = npcSaved ? ' Bonus cuu nguoi: +200!' : '';
    if (lv + 1 >= LEVELS.length) {
      showOvlTip('CHIEN THANG!', 'Diem: ' + sc + npcMsg, tip, 'CHOI LAI',
        function () { hp = 3; sc = 0; hideOvl(); loadLv(0); });
    } else {
      showOvlTip('THOAT NAN THANH CONG!', 'Thuong: +' + bonus + ' diem' + npcMsg, tip,
        'MAN TIEP', function () { hideOvl(); loadLv(lv + 1); });
    }
  }

  function winAll() { winLv(); }

  // ==================== PARTICLES & FLOATING MESSAGES ====================
  function spark(gx, gy, col, n) {
    for (var i = 0; i < n; i++) {
      particles.push({
        x: gx * T + T / 2, y: gy * T + T / 2,
        vx: (Math.random() - .5) * 5, vy: (Math.random() - .5) * 5,
        life: 25 + Math.random() * 20, ml: 45, col: col,
        sz: 2 + Math.random() * 4
      });
    }
  }

  function fmsg(gx, gy, text) {
    fmsgs.push({ x: gx * T + T / 2, y: gy * T, text: text, life: 50 });
  }

  function showEduTip(tip) {
    fmsgs = fmsgs.filter(function (m) { return !m.isEduTip; });
    fmsgs.push({ x: cv.width / 2, y: cv.height - 40, text: String(tip).trim(), life: 140, isEduTip: true });
  }

  // ==================== INTERACTION (Space/Enter) ====================
  function interact() {
    if (!run || !map) return;
    var dirs = [[0, -1], [0, 1], [-1, 0], [1, 0]];
    for (var i = 0; i < dirs.length; i++) {
      var nx = p.x + dirs[i][0], ny = p.y + dirs[i][1];
      if (nx < 0 || nx >= mapW || ny < 0 || ny >= mapH) continue;
      var t = map[ny][nx];

      if (t === BRKR && !breakerOff) {
        breakerOff = true; sc += 30;
        for (var r = 0; r < mapH; r++) for (var c = 0; c < mapW; c++) if (map[r][c] === ELEC) map[r][c] = F;
        spark(nx, ny, '#ffff00', 15); fmsg(nx, ny, 'Ngat dien!'); updHUD();
        showEduTip('Bai hoc: Luon ngat dien truoc khi tiep can day dien!');
        return;
      }
      if (t === GASV && !gasOff) {
        gasOff = true; sc += 30;
        for (var r = 0; r < mapH; r++) for (var c = 0; c < mapW; c++) if (map[r][c] === GASL) map[r][c] = F;
        spark(nx, ny, '#00ffaa', 12); fmsg(nx, ny, 'Khoa gas!'); updHUD();
        showEduTip('Bai hoc: Khoa van gas TRUOC KHI dap lua gan nguon gas!');
        return;
      }
      if (t === PHONE && !called114) {
        called114 = true; sc += 50;
        for (var r = 0; r < mapH; r++) for (var c = 0; c < mapW; c++) if (map[r][c] === EXITL) map[r][c] = EXIT;
        spark(nx, ny, '#4fc3f7', 15); fmsg(nx, ny, 'Goi 114!'); updHUD();
        showEduTip('Bai hoc: Luon goi 114 ngay khi phat hien chay!');
        return;
      }
      if (t === HDOOR) {
        fmsg(nx, ny, 'Cua NONG!');
        showEduTip('Bai hoc: Kiem tra nhiet do cua truoc khi mo - cua nong = dam chay phia sau!');
        die('Cua rat nong - phia sau dang chay du doi! Phai di duong khac.'); return;
      }
      if (t === SDOOR) {
        map[ny][nx] = F; sc += 20; spark(nx, ny, '#10b981', 8); fmsg(nx, ny, 'Cua an toan!'); updHUD(); return;
      }
      if (t === BLCK) {
        map[ny][nx] = F; sc += 20;
        spark(nx, ny, '#a0522d', 10); fmsg(nx, ny, 'Don do vat!'); updHUD();
        showEduTip('Bai hoc: Luon giu loi thoat thoang rong, khong de do dac chan duong!');
        return;
      }
      // Use BCC to extinguish adjacent fire
      if (t === FIRE && inv.bcc) {
        _useBccAt(nx, ny); return;
      }
      // Use KEY on adjacent locked door
      if (t === DLCK && inv.key) {
        map[ny][nx] = F; inv.key = false; sc += 40;
        spark(nx, ny, '#ffd93d', 12); fmsg(nx, ny, 'Mo khoa!'); updInv();
        showEduTip('Bai hoc: Luon mang theo chia khoa khi thoat hiem!');
        return;
      }
    }
  }

  function _useBccAt(fx, fy) {
    map[fy][fx] = F;
    bccCharges++;
    sc += 50; spark(fx, fy, '#87ceeb', 15); fmsg(fx, fy, 'Dap lua!');
    if (bccCharges >= BCC_MAX) {
      inv.bcc = false; bccCharges = 0;
      showEduTip('Binh chua chay het! Tim binh moi neu can.');
    } else {
      showEduTip('Binh chua chay con ' + (BCC_MAX - bccCharges) + ' lan su dung.');
    }
    updInv(); updHUD();
  }

  // ==================== MOVEMENT ====================
  function move(dx, dy) {
    if (!run || !map) return;
    var nx = p.x + dx, ny = p.y + dy;
    if (nx < 0 || nx >= mapW || ny < 0 || ny >= mapH) return;
    var t = map[ny][nx];

    pDir = { dx: dx, dy: dy };

    // Hard blocks
    if (t === W || t === FUR) return;

    // Interactive objects - must use Space/Enter
    if (t === BRKR || t === GASV || t === PHONE || t === HDOOR || t === SDOOR || t === BLCK) {
      fmsg(nx, ny, 'Nhan Space!'); return;
    }

    // Electric tile - needs breaker off
    if (t === ELEC) {
      if (!breakerOff) { die('Bi dien giat! Phai tim va ngat cau dao truoc.'); return; }
      else { map[ny][nx] = F; }
    }

    // Gas leak
    if (t === GASL) {
      if (!gasOff) { die('Khi gas bung chay! Phai khoa van gas truoc.'); return; }
    }

    // Fire - blocked unless player has BCC
    if (t === FIRE) {
      if (inv.bcc) {
        _useBccAt(nx, ny);
        // After extinguishing, allow movement into cleared tile
        p.x = nx; p.y = ny;
        crouching = false;
        updateCamera(); updInv(); updHUD();
        if (map[ny][nx] === EXIT) winLv();
      } else {
        fmsg(nx, ny, 'Can binh chua chay!');
        showEduTip('Ban can binh chua chay (BCC) de di qua lua!');
      }
      return;
    }

    // Smoke - blocked unless TWL or MSK
    if (t === SMK) {
      if (inv.twl) {
        // Towel timer: depletes while in smoke
        twlTimeMs -= 1500; // Cost ~1.5s per tile
        if (twlTimeMs <= 0) {
          inv.twl = false; twlTimeMs = 0;
          showEduTip('Khan uot het hieu luc! Can tim chiec khan moi.');
        } else {
          showEduTip('Khan uot con ' + Math.ceil(twlTimeMs / 1000) + ' giay hieu luc.');
        }
        crouching = true;
        p.x = nx; p.y = ny;
        sc += 20; updInv(); updHUD();
        updateCamera();
        if (map[ny][nx] === EXIT) winLv();
        return;
      }
      if (inv.msk) {
        // Mask: passable, no damage
        crouching = true;
        p.x = nx; p.y = ny;
        sc += 20; updHUD();
        updateCamera();
        showEduTip('Mat na bao ve khoi khi doc va khoi!');
        if (map[ny][nx] === EXIT) winLv();
        return;
      }
      fmsg(nx, ny, 'Can khan uot!');
      showEduTip('Ban can khan uot (TWL) hoac mat na (MSK) de di qua khoi!');
      return;
    }

    // Toxic - blocked unless MSK
    if (t === TOX) {
      if (inv.msk) {
        p.x = nx; p.y = ny; sc += 30; updHUD();
        showEduTip('Mat na phong doc bao ve khoi khi doc!');
        updateCamera();
        return;
      }
      die('Khi doc! Can mat na phong doc.'); return;
    }

    // Locked door - needs KEY (also handles interact)
    if (t === DLCK) {
      if (inv.key) {
        map[ny][nx] = F; inv.key = false; sc += 40;
        spark(nx, ny, '#ffd93d', 12); fmsg(nx, ny, 'Mo khoa!'); updInv();
        showEduTip('Bai hoc: Luon mang theo chia khoa khi thoat hiem!');
      } else {
        fmsg(nx, ny, 'Can chia khoa!');
        showEduTip('Cua bi khoa! Tim chia khoa (KEY) de mo cua.');
      }
      return;
    }

    // Locked exit (need 114)
    if (t === EXITL) { fmsg(nx, ny, 'Phai goi 114 truoc!'); return; }

    // Pickups
    if (t === BCC) {
      inv.bcc = true; bccCharges = 0;
      spark(nx, ny, '#ff6b35', 10); fmsg(nx, ny, 'Binh chua chay!');
      sc += 30; map[ny][nx] = F;
      showEduTip('Bai hoc: Binh chua chay: Keo chot - Huong nozzle - Bop - Quet (PASS)');
      updInv(); updHUD();
      // Move onto tile
      p.x = nx; p.y = ny; crouching = false;
      updateCamera(); return;
    }
    if (t === TWL) {
      inv.twl = true; twlTimeMs = TWL_DURATION;
      spark(nx, ny, '#87ceeb', 10); fmsg(nx, ny, 'Khan uot!');
      sc += 30; map[ny][nx] = F;
      showEduTip('Bai hoc: Khan uot giup bao ve ho hap khi phai di qua khu vuc khoi!');
      updInv(); updHUD();
      p.x = nx; p.y = ny; crouching = false;
      updateCamera(); return;
    }
    if (t === MSK) {
      inv.msk = true;
      spark(nx, ny, '#a0a0ff', 10); fmsg(nx, ny, 'Mat na!');
      sc += 30; map[ny][nx] = F;
      showEduTip('Bai hoc: Mat na phong doc bao ve khoi khi doc va khoi day!');
      updInv(); updHUD();
      p.x = nx; p.y = ny; crouching = false;
      updateCamera(); return;
    }
    if (t === KEY) {
      inv.key = true;
      spark(nx, ny, '#ffd93d', 10); fmsg(nx, ny, 'Chia khoa!');
      sc += 30; map[ny][nx] = F;
      showEduTip('Bai hoc: Luon kiem tra va mang theo chia khoa khi thoat hiem!');
      updInv(); updHUD();
      p.x = nx; p.y = ny; crouching = false;
      updateCamera(); return;
    }

    // NPC rescue
    if (t === NPC) {
      npcFollow = true; map[ny][nx] = F; sc += 50;
      spark(nx, ny, '#ff69b4', 15); fmsg(nx, ny, 'Cuu nguoi! Den EXIT!'); updHUD();
      p.x = nx; p.y = ny;
      updateCamera(); return;
    }

    // Normal floor movement
    crouching = false;
    p.x = nx; p.y = ny;
    if (npcFollow && npcPos) npcPos = { x: p.x - dx, y: p.y - dy };
    updateCamera(); updHUD();

    // EXIT check
    if (t === EXIT) {
      if (npcFollow) npcSaved = true;
      winLv();
    }
  }

  // ==================== INPUT ====================
  document.addEventListener('keydown', function (e) {
    switch (e.key) {
      case 'ArrowUp': case 'w': case 'W': e.preventDefault(); move(0, -1); break;
      case 'ArrowDown': case 's': case 'S': e.preventDefault(); move(0, 1); break;
      case 'ArrowLeft': case 'a': case 'A': e.preventDefault(); move(-1, 0); break;
      case 'ArrowRight': case 'd': case 'D': e.preventDefault(); move(1, 0); break;
      case ' ': case 'Enter': e.preventDefault(); interact(); break;
    }
  });

  var mb = document.querySelectorAll('.ctrl-btn');
  for (var i = 0; i < mb.length; i++) {
    (function (b) {
      var dirMap = { up: [0, -1], down: [0, 1], left: [-1, 0], right: [1, 0] };
      var dir = dirMap[b.getAttribute('data-dir')];
      if (dir) {
        b.addEventListener('touchstart', function (e) { e.preventDefault(); move(dir[0], dir[1]); });
        b.addEventListener('click', function () { move(dir[0], dir[1]); });
      }
    })(mb[i]);
  }

  // ==================== TILE RENDERING ====================
  // All draw functions use screen coordinates (sx, sy) = tile * T offset by camera

  function dFloor(sx, sy) {
    // Warm light floor — clearly visible and walkable
    cx.fillStyle = '#c2b89a';
    cx.fillRect(sx, sy, T, T);
    // Tile grout lines
    cx.strokeStyle = '#a89a7a';
    cx.lineWidth = 1;
    cx.strokeRect(sx + 0.5, sy + 0.5, T - 1, T - 1);
    // Slightly darker center squares for tile pattern
    cx.fillStyle = '#b5a88c';
    cx.fillRect(sx + 2, sy + 2, T / 2 - 3, T / 2 - 3);
    cx.fillRect(sx + T / 2 + 1, sy + T / 2 + 1, T / 2 - 3, T / 2 - 3);
  }

  function dWall(sx, sy) {
    // Dark solid wall — much darker than floor for clear contrast
    cx.fillStyle = '#0e0f18';
    cx.fillRect(sx, sy, T, T);
    // Brick mortar lines (slightly lighter)
    cx.fillStyle = '#181928';
    var bh = Math.floor(T / 3);
    for (var row = 0; row < 3; row++) {
      var offset = (row % 2 === 0) ? 0 : Math.floor(T / 2);
      cx.fillRect(sx + offset + 1, sy + row * bh + 1, Math.floor(T / 2) - 3, bh - 2);
      cx.fillRect(sx + offset + Math.floor(T / 2) + 1, sy + row * bh + 1, Math.floor(T / 2) - 3, bh - 2);
    }
    // Top highlight edge
    cx.fillStyle = 'rgba(255,255,255,0.04)';
    cx.fillRect(sx, sy, T, 1);
  }

  function dFurn(sx, sy) {
    dFloor(sx, sy);
    cx.fillStyle = '#7a5618';
    cx.fillRect(sx + 3, sy + 3, T - 6, T - 6);
    cx.fillStyle = '#8f6820';
    cx.fillRect(sx + 3, sy + 3, T - 6, 5); // top highlight
    cx.strokeStyle = '#4a3208';
    cx.lineWidth = 1.5;
    cx.strokeRect(sx + 3, sy + 3, T - 6, T - 6);
  }

  function dFire(sx, sy) {
    dFloor(sx, sy);
    var t = tick;
    // Warm glow on floor
    cx.fillStyle = 'rgba(255,80,0,0.25)';
    cx.fillRect(sx, sy, T, T);
    // Base flame - dark red
    cx.fillStyle = '#c0200a';
    cx.beginPath();
    cx.moveTo(sx + 4, sy + T - 2);
    cx.quadraticCurveTo(sx + 2, sy + T * 0.5 + Math.sin(t * 0.3) * 4, sx + T * 0.35, sy + T * 0.25 + Math.sin(t * 0.25) * 3);
    cx.quadraticCurveTo(sx + T / 2, sy + 2 + Math.cos(t * 0.2) * 3, sx + T * 0.65, sy + T * 0.25 + Math.sin(t * 0.2) * 3);
    cx.quadraticCurveTo(sx + T - 2, sy + T * 0.5 + Math.cos(t * 0.3) * 4, sx + T - 4, sy + T - 2);
    cx.closePath(); cx.fill();
    // Mid flame - orange
    cx.fillStyle = '#ff6b00';
    cx.beginPath();
    cx.moveTo(sx + 7, sy + T - 3);
    cx.quadraticCurveTo(sx + 5, sy + T * 0.55 + Math.sin(t * 0.35) * 3, sx + T * 0.4, sy + T * 0.35 + Math.sin(t * 0.3) * 2);
    cx.quadraticCurveTo(sx + T / 2, sy + 8 + Math.cos(t * 0.25) * 3, sx + T * 0.6, sy + T * 0.35 + Math.cos(t * 0.3) * 2);
    cx.quadraticCurveTo(sx + T - 7, sy + T * 0.55 + Math.cos(t * 0.35) * 3, sx + T - 7, sy + T - 3);
    cx.closePath(); cx.fill();
    // Inner flame - yellow
    cx.fillStyle = '#ffd700';
    cx.beginPath();
    cx.moveTo(sx + 11, sy + T - 4);
    cx.quadraticCurveTo(sx + T / 2, sy + T * 0.3 + Math.sin(t * 0.4) * 4, sx + T - 11, sy + T - 4);
    cx.closePath(); cx.fill();
    // Ember sparks
    if (Math.sin(t * 0.4) > 0.6) {
      cx.fillStyle = '#fff7a0';
      for (var i = 0; i < 3; i++) {
        var ex = sx + 6 + Math.sin(t * 0.3 + i * 2) * 8;
        var ey = sy + 4 + Math.cos(t * 0.5 + i) * 4;
        cx.beginPath();
        cx.arc(ex, ey, 1.5, 0, Math.PI * 2);
        cx.fill();
      }
    }
  }

  function dSmoke(sx, sy) {
    dFloor(sx, sy);
    var t = tick;
    // Multi-layer drifting clouds
    for (var layer = 0; layer < 4; layer++) {
      var alpha = 0.18 + Math.sin(t * 0.08 + layer * 1.1) * 0.06;
      cx.fillStyle = 'rgba(110,115,130,' + alpha + ')';
      for (var i = 0; i < 3; i++) {
        var ox = Math.sin(t * 0.05 + i * 2 + layer) * 4 + layer * 8;
        var oy = Math.cos(t * 0.04 + i * 1.5) * 2;
        cx.beginPath();
        cx.ellipse(sx + 5 + i * 9 + ox, sy + 8 + i * 5 + oy, 7 + i * 1.5, 5 + i, 0, 0, Math.PI * 2);
        cx.fill();
      }
    }
    // Rising wisps
    for (var j = 0; j < 5; j++) {
      var rise = (t * 0.08 + j * 0.6) % 9;
      cx.fillStyle = 'rgba(160,165,180,' + (0.25 + Math.sin(t * 0.1 + j) * 0.08) + ')';
      cx.beginPath();
      cx.arc(sx + 5 + j * 7 + Math.sin(t * 0.06 + j) * 2, sy + 3 - rise, 2, 0, Math.PI * 2);
      cx.fill();
    }
    cx.fillStyle = 'rgba(200,200,210,0.5)';
    cx.font = 'bold 7px Arial';
    cx.textAlign = 'center';
    cx.fillText('KHOI', sx + T / 2, sy + T - 3);
  }

  function dExit(sx, sy) {
    dFloor(sx, sy);
    var g = 0.5 + Math.sin(tick * 0.1) * 0.25;
    // Green glow
    cx.fillStyle = 'rgba(16,185,129,' + g * 0.5 + ')';
    cx.fillRect(sx, sy, T, T);
    // Door frame
    cx.fillStyle = '#065f46';
    cx.fillRect(sx + 2, sy + 2, T - 4, T - 4);
    // Door panel
    cx.fillStyle = '#10b981';
    cx.fillRect(sx + 5, sy + 6, T - 10, T - 8);
    // Door handle
    cx.fillStyle = '#ffd700';
    cx.beginPath();
    cx.arc(sx + T - 10, sy + T / 2, 3, 0, Math.PI * 2);
    cx.fill();
    // Pulsing border
    cx.strokeStyle = 'rgba(52,211,153,' + g + ')';
    cx.lineWidth = 2;
    cx.strokeRect(sx + 2, sy + 2, T - 4, T - 4);
    cx.lineWidth = 1;
    // EXIT text
    cx.fillStyle = '#ffffff';
    cx.font = 'bold 9px Arial';
    cx.textAlign = 'center';
    cx.fillText('EXIT', sx + T / 2, sy + T - 3);
    // Arrow indicator
    cx.fillStyle = '#ffffff';
    cx.beginPath();
    cx.moveTo(sx + T / 2 - 5, sy + 14);
    cx.lineTo(sx + T / 2 + 5, sy + 14);
    cx.lineTo(sx + T / 2, sy + 9);
    cx.closePath();
    cx.fill();
  }

  function dExitL(sx, sy) {
    dFloor(sx, sy);
    cx.fillStyle = 'rgba(255,50,50,0.2)';
    cx.fillRect(sx + 2, sy + 2, T - 4, T - 4);
    cx.strokeStyle = '#ff4444';
    cx.lineWidth = 2;
    cx.strokeRect(sx + 3, sy + 3, T - 6, T - 6);
    cx.lineWidth = 1;
    cx.fillStyle = '#ff4444';
    cx.font = 'bold 7px Arial';
    cx.textAlign = 'center';
    cx.fillText('GOI', sx + T / 2, sy + T / 2 - 4);
    cx.fillText('114', sx + T / 2, sy + T / 2 + 6);
  }

  function dBCC(sx, sy) {
    dFloor(sx, sy);
    var b = Math.sin(tick * 0.12) * 2;
    // Cylinder body
    cx.fillStyle = '#dc2626';
    cx.fillRect(sx + 11, sy + 8 + b, 14, 20);
    // Top cap
    cx.fillStyle = '#1c1c1c';
    cx.fillRect(sx + 13, sy + 5 + b, 10, 5);
    // Nozzle
    cx.fillStyle = '#555';
    cx.fillRect(sx + 14, sy + 3 + b, 8, 4);
    // Shine
    cx.fillStyle = 'rgba(255,255,255,0.3)';
    cx.fillRect(sx + 12, sy + 10 + b, 3, 12);
    // Label
    cx.fillStyle = '#fff';
    cx.font = 'bold 6px Arial';
    cx.textAlign = 'center';
    cx.fillText('FIRE', sx + T / 2, sy + T - 3);
    // Glow
    cx.fillStyle = 'rgba(220,38,38,0.12)';
    cx.beginPath();
    cx.arc(sx + T / 2, sy + T / 2, 16, 0, Math.PI * 2);
    cx.fill();
  }

  function dTwl(sx, sy) {
    dFloor(sx, sy);
    var b = Math.sin(tick * 0.1) * 2;
    // Folded cloth
    cx.fillStyle = '#1d6fa4';
    cx.fillRect(sx + 7, sy + 10 + b, 22, 8);
    cx.fillStyle = '#2196f3';
    cx.fillRect(sx + 9, sy + 16 + b, 18, 7);
    // Water drops
    cx.fillStyle = '#87ceeb';
    for (var i = 0; i < 3; i++) {
      var drop = (tick * 0.1 + i) % 6;
      cx.beginPath();
      cx.arc(sx + 10 + i * 7, sy + 24 + drop, 2, 0, Math.PI * 2);
      cx.fill();
    }
    cx.fillStyle = '#87ceeb';
    cx.font = 'bold 7px Arial';
    cx.textAlign = 'center';
    cx.fillText('KHAN', sx + T / 2, sy + T - 2);
  }

  function dMask(sx, sy) {
    dFloor(sx, sy);
    var b = Math.sin(tick * 0.1) * 2;
    // Mask body
    cx.fillStyle = '#9e9e9e';
    cx.beginPath();
    cx.ellipse(sx + T / 2, sy + T / 2 + b - 1, 13, 10, 0, 0, Math.PI * 2);
    cx.fill();
    // Straps
    cx.strokeStyle = '#757575';
    cx.lineWidth = 1.5;
    cx.beginPath();
    cx.moveTo(sx + T / 2 - 13, sy + T / 2 + b - 1);
    cx.lineTo(sx + 2, sy + T / 2 + b - 5);
    cx.stroke();
    cx.beginPath();
    cx.moveTo(sx + T / 2 + 13, sy + T / 2 + b - 1);
    cx.lineTo(sx + T - 2, sy + T / 2 + b - 5);
    cx.stroke();
    // Filter
    cx.fillStyle = '#bdbdbd';
    cx.fillRect(sx + T / 2 - 5, sy + T / 2 + b - 3, 10, 6);
    // Medical cross
    cx.fillStyle = '#e53935';
    cx.fillRect(sx + T / 2 - 1, sy + T / 2 + b - 4, 2, 8);
    cx.fillRect(sx + T / 2 - 4, sy + T / 2 + b - 1, 8, 2);
    cx.fillStyle = '#bdbdbd';
    cx.font = 'bold 7px Arial';
    cx.textAlign = 'center';
    cx.fillText('MASK', sx + T / 2, sy + T - 2);
  }

  function dKey(sx, sy) {
    dFloor(sx, sy);
    var b = Math.sin(tick * 0.12) * 2;
    cx.save();
    cx.translate(sx + T / 2, sy + T / 2 + b);
    cx.rotate(Math.sin(tick * 0.05) * 0.15);
    // Key head (ring)
    cx.strokeStyle = '#f59e0b';
    cx.lineWidth = 2.5;
    cx.beginPath();
    cx.arc(-7, -3, 6, 0, Math.PI * 2);
    cx.stroke();
    // Key shaft
    cx.fillStyle = '#f59e0b';
    cx.fillRect(-2, -4, 14, 3);
    // Key teeth
    cx.fillRect(6, -1, 3, 5);
    cx.fillRect(10, -1, 3, 4);
    cx.restore();
    // Glow
    cx.fillStyle = 'rgba(245,158,11,0.15)';
    cx.beginPath();
    cx.arc(sx + T / 2, sy + T / 2, 14, 0, Math.PI * 2);
    cx.fill();
    cx.fillStyle = '#f59e0b';
    cx.font = 'bold 7px Arial';
    cx.textAlign = 'center';
    cx.fillText('KEY', sx + T / 2, sy + T - 2);
  }

  function dLock(sx, sy) {
    // Brown door background
    cx.fillStyle = '#5c4033';
    cx.fillRect(sx, sy, T, T);
    cx.fillStyle = '#6d4c41';
    cx.fillRect(sx + 3, sy + 2, T - 6, T - 4);
    // Door frame
    cx.strokeStyle = '#3e2723';
    cx.lineWidth = 1;
    cx.strokeRect(sx + 3, sy + 2, T - 6, T - 4);
    // Lock mechanism
    cx.fillStyle = '#ffd700';
    cx.beginPath();
    cx.arc(sx + T / 2, sy + T / 2 - 4, 5, 0, Math.PI * 2);
    cx.fill();
    cx.fillStyle = '#ff8f00';
    cx.fillRect(sx + T / 2 - 4, sy + T / 2, 8, 8);
    cx.fillStyle = '#3e2723';
    cx.fillRect(sx + T / 2 - 1, sy + T / 2 + 2, 2, 4);
    cx.fillStyle = '#ff3d00';
    cx.font = 'bold 6px Arial';
    cx.textAlign = 'center';
    cx.fillText('LOCK', sx + T / 2, sy + T - 2);
  }

  function dToxic(sx, sy) {
    dFloor(sx, sy);
    var a = 0.25 + Math.sin(tick * 0.06) * 0.1;
    cx.fillStyle = 'rgba(76,175,80,' + a + ')';
    cx.fillRect(sx + 2, sy + 2, T - 4, T - 4);
    cx.fillStyle = '#66bb6a';
    cx.beginPath();
    cx.arc(sx + T / 2, sy + T / 2 - 2, 10, 0, Math.PI * 2);
    cx.fill();
    cx.fillStyle = '#1b5e20';
    cx.fillRect(sx + T / 2 - 5, sy + T / 2 - 6, 4, 4);
    cx.fillRect(sx + T / 2 + 1, sy + T / 2 - 6, 4, 4);
    cx.fillStyle = '#66bb6a';
    cx.font = 'bold 7px Arial';
    cx.textAlign = 'center';
    cx.fillText('DOC', sx + T / 2, sy + T - 2);
  }

  function dElec(sx, sy) {
    dFloor(sx, sy);
    var t = tick;
    cx.strokeStyle = '#212121';
    cx.lineWidth = 3;
    cx.beginPath();
    cx.moveTo(sx + 2, sy + T / 2);
    cx.lineTo(sx + T - 2, sy + T / 2);
    cx.stroke();
    if (Math.sin(t * 0.3) > 0) {
      cx.fillStyle = '#ffee58';
      for (var i = 0; i < 4; i++) {
        var sx2 = sx + 8 + Math.random() * 20, sy2 = sy + T / 2 - 6 + Math.random() * 12;
        cx.fillRect(sx2, sy2, 3, 3);
      }
      cx.fillStyle = 'rgba(255,235,59,0.12)';
      cx.fillRect(sx, sy, T, T);
    }
    cx.fillStyle = '#ffee58';
    cx.font = 'bold 7px Arial';
    cx.textAlign = 'center';
    cx.fillText('DIEN', sx + T / 2, sy + T - 2);
  }

  function dBrkr(sx, sy) {
    dFloor(sx, sy);
    cx.fillStyle = breakerOff ? '#1b5e20' : '#b71c1c';
    cx.fillRect(sx + 7, sy + 4, 22, 30);
    cx.strokeStyle = '#777';
    cx.strokeRect(sx + 7, sy + 4, 22, 30);
    cx.fillStyle = breakerOff ? '#4caf50' : '#f44336';
    cx.fillRect(sx + 12, sy + (breakerOff ? 22 : 10), 12, 8);
    cx.fillStyle = '#fff';
    cx.font = 'bold 6px Arial';
    cx.textAlign = 'center';
    cx.fillText(breakerOff ? 'OFF' : 'ON', sx + T / 2, sy + T - 3);
  }

  function dGasL(sx, sy) {
    dFloor(sx, sy);
    var a = 0.2 + Math.sin(tick * 0.06) * 0.1;
    cx.fillStyle = 'rgba(255,152,0,' + a + ')';
    cx.fillRect(sx, sy, T, T);
    for (var i = 0; i < 3; i++) {
      cx.fillStyle = 'rgba(255,193,7,' + (0.3 + Math.sin(tick * 0.1 + i) * 0.15) + ')';
      cx.beginPath();
      cx.arc(sx + 7 + i * 11 + Math.sin(tick * 0.05 + i) * 3, sy + 10 + i * 7 + Math.cos(tick * 0.04 + i) * 3, 4 + i, 0, Math.PI * 2);
      cx.fill();
    }
    cx.fillStyle = '#ffa726';
    cx.font = 'bold 7px Arial';
    cx.textAlign = 'center';
    cx.fillText('GAS', sx + T / 2, sy + T - 2);
  }

  function dGasV(sx, sy) {
    dFloor(sx, sy);
    cx.fillStyle = gasOff ? '#1b5e20' : '#b71c1c';
    cx.fillRect(sx + 7, sy + 4, 22, 30);
    cx.strokeStyle = '#777';
    cx.strokeRect(sx + 7, sy + 4, 22, 30);
    cx.fillStyle = gasOff ? '#4caf50' : '#f44336';
    cx.beginPath();
    cx.arc(sx + T / 2, sy + T / 2, 7, 0, Math.PI * 2);
    cx.fill();
    cx.fillStyle = '#fff';
    cx.font = 'bold 6px Arial';
    cx.textAlign = 'center';
    cx.fillText(gasOff ? 'DONG' : 'MO', sx + T / 2, sy + T - 3);
  }

  function dPhone(sx, sy) {
    dFloor(sx, sy);
    var g = called114 ? '#10b981' : 'rgba(79,195,247,' + (0.5 + Math.sin(tick * 0.1) * 0.3) + ')';
    cx.fillStyle = g;
    cx.fillRect(sx + 11, sy + 5, 14, 22);
    cx.fillStyle = '#1c1c1c';
    cx.fillRect(sx + 13, sy + 7, 10, 12);
    cx.fillStyle = called114 ? '#10b981' : '#4fc3f7';
    cx.beginPath();
    cx.arc(sx + T / 2, sy + 23, 4, 0, Math.PI * 2);
    cx.fill();
    cx.fillStyle = called114 ? '#fff' : '#fff';
    cx.font = 'bold 7px Arial';
    cx.textAlign = 'center';
    cx.fillText(called114 ? 'OK' : '114', sx + T / 2, sy + T - 2);
  }

  function dHDoor(sx, sy) {
    cx.fillStyle = '#7f0000';
    cx.fillRect(sx, sy, T, T);
    cx.fillStyle = '#8b0000';
    cx.fillRect(sx + 3, sy + 2, T - 6, T - 4);
    var t = tick;
    for (var i = 0; i < 3; i++) {
      cx.strokeStyle = 'rgba(255,100,0,' + (0.3 + Math.sin(t * 0.1 + i) * 0.2) + ')';
      cx.lineWidth = 1;
      cx.beginPath();
      cx.moveTo(sx + 7 + i * 8, sy + 4 + Math.sin(t * 0.15 + i) * 3);
      cx.quadraticCurveTo(sx + 11 + i * 8, sy - 2 + Math.cos(t * 0.12 + i) * 3, sx + 15 + i * 8, sy + 4 + Math.sin(t * 0.15 + i + 1) * 3);
      cx.stroke();
    }
    cx.fillStyle = '#ff6600';
    cx.font = 'bold 7px Arial';
    cx.textAlign = 'center';
    cx.fillText('NONG!', sx + T / 2, sy + T - 2);
  }

  function dSDoor(sx, sy) {
    cx.fillStyle = '#33691e';
    cx.fillRect(sx, sy, T, T);
    cx.fillStyle = '#558b2f';
    cx.fillRect(sx + 3, sy + 2, T - 6, T - 4);
    cx.fillStyle = '#fff';
    cx.fillRect(sx + T - 10, sy + T / 2 - 2, 4, 4);
    cx.fillStyle = '#aed581';
    cx.font = 'bold 6px Arial';
    cx.textAlign = 'center';
    cx.fillText('KIEM', sx + T / 2, sy + T / 2 - 4);
    cx.fillText('TRA', sx + T / 2, sy + T / 2 + 5);
  }

  function dNPC(sx, sy) {
    dFloor(sx, sy);
    cx.fillStyle = '#f48fb1';
    cx.beginPath();
    cx.arc(sx + T / 2, sy + 11, 8, 0, Math.PI * 2);
    cx.fill();
    cx.fillStyle = '#f06292';
    cx.fillRect(sx + 11, sy + 17, 14, 13);
    cx.fillStyle = '#212121';
    cx.fillRect(sx + T / 2 - 5, sy + 9, 3, 3);
    cx.fillRect(sx + T / 2 + 2, sy + 9, 3, 3);
    cx.fillStyle = '#f48fb1';
    cx.font = 'bold 7px Arial';
    cx.textAlign = 'center';
    cx.fillText('CUU!', sx + T / 2, sy + T - 2);
    if (Math.sin(tick * 0.15) > 0) {
      cx.fillStyle = '#fff176';
      cx.font = 'bold 9px Arial';
      cx.fillText('!', sx + T / 2 + 12, sy + 7);
    }
  }

  function dBlck(sx, sy) {
    dFloor(sx, sy);
    cx.fillStyle = '#5d4037';
    cx.fillRect(sx + 3, sy + 3, T - 6, T - 6);
    cx.fillStyle = '#795548';
    cx.fillRect(sx + 3, sy + 3, T - 6, T / 2 - 3);
    cx.strokeStyle = '#3e2723';
    cx.lineWidth = 1;
    cx.strokeRect(sx + 3, sy + 3, T - 6, T - 6);
    cx.fillStyle = '#ffcc80';
    cx.font = 'bold 6px Arial';
    cx.textAlign = 'center';
    cx.fillText('DOI', sx + T / 2, sy + T - 2);
  }

  // ==================== DISPATCH TILE DRAW ====================
  function dTile(mc, mr, sc_col, sc_row) {
    if (!map || !map[mr] || map[mr][mc] === undefined) return;
    var t = map[mr][mc];
    var sx = sc_col * T, sy = sc_row * T;
    switch (t) {
      case F: dFloor(sx, sy); break;
      case W: dWall(sx, sy); break;
      case FUR: dFurn(sx, sy); break;
      case FIRE: dFire(sx, sy); break;
      case SMK: dSmoke(sx, sy); break;
      case TOX: dToxic(sx, sy); break;
      case EXIT: dExit(sx, sy); break;
      case EXITL: dExitL(sx, sy); break;
      case BCC: dBCC(sx, sy); break;
      case TWL: dTwl(sx, sy); break;
      case MSK: dMask(sx, sy); break;
      case KEY: dKey(sx, sy); break;
      case DLCK: dLock(sx, sy); break;
      case ELEC: dElec(sx, sy); break;
      case BRKR: dBrkr(sx, sy); break;
      case GASL: dGasL(sx, sy); break;
      case GASV: dGasV(sx, sy); break;
      case PHONE: dPhone(sx, sy); break;
      case HDOOR: dHDoor(sx, sy); break;
      case SDOOR: dSDoor(sx, sy); break;
      case NPC: dNPC(sx, sy); break;
      case BLCK: dBlck(sx, sy); break;
      default: dFloor(sx, sy);
    }
  }

  // ==================== PLAYER DRAW ====================
  function dPlayer() {
    if (!map) return;
    var sx = (p.x - camTX) * T;
    var sy = (p.y - camTY) * T;

    // Shadow
    cx.fillStyle = 'rgba(0,0,0,0.45)';
    cx.beginPath();
    cx.ellipse(sx + T / 2 + 2, sy + T - 3, 12, 4, 0, 0, Math.PI * 2);
    cx.fill();

    if (crouching) {
      // Crouching pose
      cx.fillStyle = '#fbbf24';
      cx.beginPath();
      cx.ellipse(sx + T / 2, sy + T * 0.65, 14, 9, 0, 0, Math.PI * 2);
      cx.fill();
      cx.fillStyle = '#fde68a';
      cx.beginPath();
      cx.arc(sx + T / 2 - 5, sy + T * 0.48, 7, 0, Math.PI * 2);
      cx.fill();
      // Helmet
      cx.fillStyle = '#1565c0';
      cx.fillRect(sx + T / 2 - 8, sy + T * 0.33, 14, 4);
    } else {
      // Standing - body
      cx.fillStyle = '#fbbf24';
      cx.fillRect(sx + 10, sy + 15, 16, 15);
      // Vest stripes
      if (inv.bcc) {
        cx.fillStyle = '#dc2626';
        cx.fillRect(sx + 10, sy + 15, 3, 15);
        cx.fillRect(sx + 23, sy + 15, 3, 15);
      } else {
        cx.fillStyle = '#1d4ed8';
        cx.fillRect(sx + 10, sy + 26, 6, 4);
        cx.fillRect(sx + 20, sy + 26, 6, 4);
      }
      // Head
      cx.fillStyle = '#fde68a';
      cx.beginPath();
      cx.arc(sx + T / 2, sy + 11, 8, 0, Math.PI * 2);
      cx.fill();
      // Helmet
      cx.fillStyle = '#f59e0b';
      cx.fillRect(sx + T / 2 - 9, sy + 5, 18, 5);
      cx.fillRect(sx + T / 2 - 7, sy + 3, 14, 4);
      // Eyes
      cx.fillStyle = '#1c1c1c';
      cx.beginPath();
      cx.arc(sx + T / 2 - 3, sy + 10, 1.5, 0, Math.PI * 2);
      cx.fill();
      cx.beginPath();
      cx.arc(sx + T / 2 + 3, sy + 10, 1.5, 0, Math.PI * 2);
      cx.fill();
      // Item indicators on character
      if (inv.twl) {
        // Blue head wrap
        cx.fillStyle = '#2196f3';
        cx.fillRect(sx + T / 2 - 7, sy + 5, 14, 3);
      }
      if (inv.msk) {
        // Gray mask
        cx.fillStyle = '#9e9e9e';
        cx.fillRect(sx + T / 2 - 5, sy + 12, 10, 5);
      }
    }
  }

  function dNPCFollow() {
    if (!npcFollow || !npcPos) return;
    var sx = (npcPos.x - camTX) * T, sy = (npcPos.y - camTY) * T;
    cx.fillStyle = '#f48fb1';
    cx.beginPath();
    cx.arc(sx + T / 2, sy + 13, 7, 0, Math.PI * 2);
    cx.fill();
    cx.fillStyle = '#f06292';
    cx.fillRect(sx + 13, sy + 18, 10, 11);
    cx.fillStyle = '#f48fb1';
    cx.font = 'bold 7px Arial';
    cx.textAlign = 'center';
    cx.fillText('♥', sx + T / 2, sy + T - 2);
  }

  // ==================== MAIN RENDER ====================
  function render() {
    tick++;
    cx.clearRect(0, 0, cv.width, cv.height);
    cx.fillStyle = '#111827';
    cx.fillRect(0, 0, cv.width, cv.height);

    if (map) {
      // Calculate vision radius (in tiles) — base 6 is enough to see clearly
      var visionR = 6;
      if (inv.twl) visionR += 1;
      if (inv.msk) visionR += 1;
      if (inv.bcc) visionR += 1;
      if (inv.key) visionR += 1;
      visionR = Math.min(10, visionR);

      var visRows = Math.min(VIEW_ROWS, mapH);
      var visCols = Math.min(VIEW_COLS, mapW);

      // Draw tiles: visible ones normally, hidden ones as solid dark
      for (var r = 0; r < visRows; r++) {
        for (var c = 0; c < visCols; c++) {
          var mr = r + camTY, mc = c + camTX;
          if (mr < 0 || mr >= mapH || mc < 0 || mc >= mapW) continue;
          var dx = mc - p.x, dy = mr - p.y;
          var dist = Math.sqrt(dx * dx + dy * dy);
          var sx = c * T, sy = r * T;
          if (dist <= visionR) {
            dTile(mc, mr, c, r);
          } else {
            // Hidden tile — draw as near-black
            cx.fillStyle = '#05060f';
            cx.fillRect(sx, sy, T, T);
          }
        }
      }

      dNPCFollow();
      dPlayer();

      // Soft fog edge gradient (purely cosmetic, on top of tiles)
      var playerSX = (p.x - camTX) * T + T / 2;
      var playerSY = (p.y - camTY) * T + T / 2;

      // Feather the edge of visible area — smooth gradient ring
      var edgeGrad = cx.createRadialGradient(
        playerSX, playerSY, (visionR - 1.5) * T,
        playerSX, playerSY, (visionR + 0.5) * T
      );
      edgeGrad.addColorStop(0, 'rgba(5,6,15,0)');
      edgeGrad.addColorStop(1, 'rgba(5,6,15,1)');
      cx.fillStyle = edgeGrad;
      cx.fillRect(0, 0, cv.width, cv.height);

      // Restore dark corners outside gradient circle using compositing
      // (already handled by per-tile pass above — gradient just softens edge)

    } else {
      cx.fillStyle = '#3b82f6';
      cx.font = 'bold 22px Arial';
      cx.textAlign = 'center';
      cx.fillText('Nhan BAT DAU de choi!', cv.width / 2, cv.height / 2);
    }

    // Particles
    var alive = [];
    for (var i = 0; i < particles.length; i++) {
      var q = particles[i];
      q.x += q.vx; q.y += q.vy; q.life--; q.sz *= 0.96;
      cx.globalAlpha = Math.max(0, q.life / q.ml);
      cx.fillStyle = q.col;
      cx.beginPath();
      cx.arc(q.x, q.y, q.sz, 0, Math.PI * 2);
      cx.fill();
      if (q.life > 0) alive.push(q);
    }
    particles = alive;
    cx.globalAlpha = 1;

    // Floating messages
    var aliveM = [];
    for (var j = 0; j < fmsgs.length; j++) {
      var m = fmsgs[j];
      m.y -= 0.7; m.life--;
      if (m.isEduTip) {
        // Educational tip - bottom panel style
        cx.save();
        cx.globalAlpha = Math.min(1, Math.max(0, m.life / 100));
        cx.fillStyle = 'rgba(0,0,0,0.75)';
        cx.fillRect(cv.width / 2 - 320, cv.height - 55, 640, 36);
        cx.strokeStyle = 'rgba(251,191,36,0.6)';
        cx.lineWidth = 1;
        cx.strokeRect(cv.width / 2 - 320, cv.height - 55, 640, 36);
        cx.fillStyle = '#fde68a';
        cx.font = '13px Arial';
        cx.textAlign = 'center';
        cx.fillText(m.text.replace(/<[^>]+>/g, ''), cv.width / 2, cv.height - 32);
        cx.restore();
      } else {
        cx.globalAlpha = Math.max(0, m.life / 50);
        cx.fillStyle = '#ffd93d';
        cx.font = 'bold 11px Arial';
        cx.textAlign = 'center';
        // Offset by camera for world-space messages
        cx.fillText(m.text, m.x - camTX * T, m.y - camTY * T);
      }
      if (m.life > 0) aliveM.push(m);
    }
    fmsgs = aliveM;
    cx.globalAlpha = 1;

    requestAnimationFrame(render);
  }

  // ==================== BOOTSTRAP ====================
  window.startGame = function () { hideOvl(); loadLv(0); };

  function init() {
    if (window.GAME_LEVELS) {
      LEVELS = window.GAME_LEVELS;
      showOvl(
        'Thoat khoi dam chay',
        'Di chuyen: mui ten / WASD\nTuong tac: Space/Enter\n\nThu thap vat pham, giai do va tim loi thoat!',
        'BAT DAU CHOI',
        function () { hideOvl(); loadLv(0); }
      );
    } else {
      setTimeout(init, 100);
    }
  }

  init();
  render();
})();
