/* ============================================================
   FIRE ESCAPE GAME ENGINE v5 — Complete Rewrite
   Features:
   - Objectives system (EXIT locked until all complete)
   - Smooth movement animation
   - Minimap
   - Screen shake
   - Star rating
   - Enhanced particles
   - Larger tiles (44px)
   ============================================================ */
(function () {
  'use strict';

  // --- Constants ---
  var T = 44;            // Tile size px
  var VIEW_COLS = 20;    // Viewport columns
  var VIEW_ROWS = 15;    // Viewport rows
  var CANVAS_W = VIEW_COLS * T; // 880
  var CANVAS_H = VIEW_ROWS * T; // 660

  // Tile IDs
  var F = 0, W = 1, FIRE = 2, SMK = 3, EXIT = 4,
      BCC = 5, TWL = 6, MSK = 7, KEY = 8, DLCK = 9,
      PS = 11, FUR = 12, ELEC = 13, BRKR = 14,
      GASL = 15, GASV = 16, PHONE = 17;

  // --- Canvas ---
  var cv = document.getElementById('game-canvas');
  if (!cv) return;
  cv.width = CANVAS_W;
  cv.height = CANVAS_H;
  var cx = cv.getContext('2d');

  // --- State ---
  var p = { x: 1, y: 1 };          // Player map position (integer)
  var pDir = { dx: 1, dy: 0 };     // Last move direction
  var pAnim = { sx: 0, sy: 0, tx: 0, ty: 0, t: 1, dur: 0.1 }; // Smooth move

  var inv = { bcc: false, twl: false, msk: false, key: false };
  var bccCharges = 0;
  var twlTimeMs = 0;
  var TWL_DURATION = 12000;   // 12 seconds
  var BCC_MAX = 5;

  var lv = 0, sc = 0, hp = 3, tm = 120, run = false;
  var tick = 0, tInt = null, fireInt = null;

  // Camera
  var camTX = 0, camTY = 0;

  // Map
  var mapW = VIEW_COLS, mapH = VIEW_ROWS;
  var map = null;

  // Misc state
  var breakerOff = false, gasOff = false, called114 = false;
  var crouching = false;
  var particles = [], fmsgs = [];
  var shakeTime = 0; // screen shake remaining frames
  var shakeMag = 0;  // shake magnitude

  // Objectives
  var objectives = [];       // Array of {type, label, done}
  var allObjDone = false;
  var fireExtinguished = 0;  // count for 'extinguish' objectives

  // Stars
  var starRating = 0;

  // Input cooldown
  var moveCooldown = 0;
  var MOVE_COOLDOWN_MS = 70;
  var lastMoveTime = 0;

  // Key-held continuous movement
  var heldKeys = {};
  var HELD_INTERVAL_MS = 90;  // ms between moves when holding
  var heldTimer = null;

  // --- Level data ---
  var LEVELS = window.GAME_LEVELS || [];

  // ==================== OBJECTIVES SYSTEM ====================
  function initObjectives(lvData) {
    objectives = [];
    fireExtinguished = 0;
    if (lvData.objectives) {
      for (var i = 0; i < lvData.objectives.length; i++) {
        var o = lvData.objectives[i];
        objectives.push({
          type: o.type,
          label: o.label,
          count: o.count || 0,
          done: false
        });
      }
    }
    allObjDone = objectives.length === 0;
    updateObjectivesUI();
  }

  function completeObjective(type) {
    for (var i = 0; i < objectives.length; i++) {
      if (objectives[i].type === type && !objectives[i].done) {
        objectives[i].done = true;
        break;
      }
    }
    checkAllObjectives();
    updateObjectivesUI();
  }

  function checkExtinguishObj() {
    for (var i = 0; i < objectives.length; i++) {
      if (objectives[i].type === 'extinguish' && !objectives[i].done) {
        if (fireExtinguished >= objectives[i].count) {
          objectives[i].done = true;
        }
      }
    }
    checkAllObjectives();
    updateObjectivesUI();
  }

  function checkAllObjectives() {
    allObjDone = true;
    for (var i = 0; i < objectives.length; i++) {
      if (!objectives[i].done) {
        allObjDone = false;
        break;
      }
    }
  }

  function updateObjectivesUI() {
    var panel = document.getElementById('objectives-list');
    if (!panel) return;
    panel.innerHTML = '';
    for (var i = 0; i < objectives.length; i++) {
      var o = objectives[i];
      var div = document.createElement('div');
      div.className = 'obj-item' + (o.done ? ' obj-done' : '');
      div.innerHTML = '<span class="obj-check">' + (o.done ? '✅' : '⬜') + '</span>' +
                       '<span class="obj-text">' + o.label + '</span>';
      panel.appendChild(div);
    }
    // Update exit status indicator
    var exitStatus = document.getElementById('exit-status');
    if (exitStatus) {
      if (allObjDone) {
        exitStatus.textContent = '🟢 EXIT MỞ';
        exitStatus.className = 'exit-status exit-open';
      } else {
        exitStatus.textContent = '🔴 EXIT KHÓA';
        exitStatus.className = 'exit-status exit-locked';
      }
    }
  }

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
    crouching = false;
    particles = []; fmsgs = [];
    shakeTime = 0; shakeMag = 0;

    // Set map dimensions
    mapW = L.mapW || VIEW_COLS;
    mapH = L.mapH || VIEW_ROWS;

    // Deep-copy map
    map = [];
    for (var r = 0; r < mapH; r++) {
      map[r] = [];
      for (var c = 0; c < mapW; c++) {
        map[r][c] = (L.map[r] && L.map[r][c] !== undefined) ? L.map[r][c] : W;
      }
    }

    // Find player start
    for (var r2 = 0; r2 < mapH; r2++) {
      for (var c2 = 0; c2 < mapW; c2++) {
        if (map[r2][c2] === PS) { p = { x: c2, y: r2 }; map[r2][c2] = F; }
      }
    }

    // Init smooth animation
    pAnim = { sx: p.x, sy: p.y, tx: p.x, ty: p.y, t: 1, dur: 0.1 };

    // Init objectives
    initObjectives(L);

    updateCamera();
    updHUD(); updInv();
    document.getElementById('hud-level').textContent = i + 1;
    var objEl = document.getElementById('level-objective');
    if (objEl) objEl.textContent = L.nameVi || '';

    // Stop old timers
    clearInterval(tInt);
    clearInterval(fireInt);

    showOvlTip(
      'Màn ' + (i + 1) + ': ' + (L.nameVi || ''),
      L.desc || 'Tìm vật phẩm và lối thoát!',
      '<strong>Bài học:</strong> ' + (L.tip || 'Bình tĩnh, suy nghĩ rồi hành động.'),
      'BẮT ĐẦU',
      function () { hideOvl(); run = true; startTimers(L); }
    );
  }

  function startTimers(L) {
    tInt = setInterval(function () {
      if (!run) return;
      tm--;
      document.getElementById('hud-timer').textContent = tm;
      document.getElementById('hud-timer').style.color = tm <= 10 ? '#ff2222' : '#ff6b6b';
      if (tm <= 0) die('Hết thời gian! Bạn không kịp thoát ra.');
    }, 1000);

    var spreadMs = (L.fireSpread || 3) * 1000;
    fireInt = setInterval(function () {
      if (!run) return;
      spreadFire();
      if (map[p.y] && map[p.y][p.x] === FIRE) die('Lửa đã lan đến vị trí của bạn!');
    }, spreadMs);
  }

  function updateCamera() {
    var halfW = Math.floor(VIEW_COLS / 2);
    var halfH = Math.floor(VIEW_ROWS / 2);
    camTX = Math.max(0, Math.min(mapW - VIEW_COLS, p.x - halfW));
    camTY = Math.max(0, Math.min(mapH - VIEW_ROWS, p.y - halfH));
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
              var chance = nt === FUR ? 0.5 : nt === F ? 0.15 : 0;
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

  function showStarOverlay(title, text, tip, stars, btnText, fn, btnText2, fn2) {
    document.getElementById('msg-icon').textContent = '';
    document.getElementById('msg-title').textContent = title;

    // Build star + text content
    var starHtml = '<div class="star-display">';
    for (var i = 0; i < 3; i++) {
      starHtml += '<span class="star-icon ' + (i < stars ? 'star-filled' : 'star-empty') + '">★</span>';
    }
    starHtml += '</div>';
    document.getElementById('msg-text').innerHTML = starHtml + '<p>' + text + '</p>';

    var tp = document.getElementById('msg-tip');
    tp.innerHTML = tip; tp.style.display = tip ? 'block' : 'none';

    var b = document.getElementById('msg-buttons'); b.innerHTML = '';
    var bn = document.createElement('button');
    bn.className = 'game-btn game-btn-primary';
    bn.textContent = btnText; bn.onclick = fn; b.appendChild(bn);
    if (btnText2 && fn2) {
      var bn2 = document.createElement('button');
      bn2.className = 'game-btn game-btn-secondary';
      bn2.textContent = btnText2; bn2.onclick = fn2; b.appendChild(bn2);
    }
    document.getElementById('msg-overlay').classList.add('visible');
  }

  function hideOvl() {
    document.getElementById('msg-overlay').classList.remove('visible');
  }

  // ==================== SCREEN SHAKE ====================
  function triggerShake(duration, magnitude) {
    shakeTime = duration || 15;
    shakeMag = magnitude || 6;
  }

  // ==================== GAME EVENTS ====================
  function die(reason) {
    run = false;
    clearInterval(tInt); clearInterval(fireInt);
    hp--; updHUD();
    triggerShake(20, 8);
    if (hp <= 0) {
      showOvlTip('GAME OVER!', reason,
        '<strong>Bài học:</strong> Luôn bình tĩnh và chuẩn bị trước khi hành động trong đám cháy.',
        'CHƠI LẠI', function () { hp = 3; sc = 0; hideOvl(); loadLv(0); });
    } else {
      showOvl('Mất mạng! (Còn ' + hp + ')', reason, 'THỬ LẠI',
        function () { hideOvl(); loadLv(lv); });
    }
  }

  function calcStars() {
    var maxTime = LEVELS[lv] ? LEVELS[lv].time : 120;
    var timePercent = tm / maxTime;
    var stars = 1;
    if (timePercent >= 0.5 && hp >= 2) stars = 2;
    if (timePercent >= 0.7 && hp >= 3) stars = 3;
    return stars;
  }

  function winLv() {
    run = false;
    clearInterval(tInt); clearInterval(fireInt);
    var bonus = tm * 3;
    sc += bonus; updHUD();
    starRating = calcStars();

    var lessonTips = [
      '<strong>Bài học:</strong> Tìm bình chữa cháy → Kéo chốt → Hướng vào gốc lửa → Quét trái phải.',
      '<strong>Bài học:</strong> Trong khói: cúi thấp, bịt mũi bằng khăn ướt, men theo tường.',
      '<strong>Bài học:</strong> Gọi 114 ngay! Lửa lan rất nhanh, mỗi giây đều quan trọng.',
      '<strong>Bài học:</strong> Ngắt điện và khóa gas TRƯỚC KHI chữa cháy!',
      '<strong>Bài học:</strong> Luôn biết lối thoát hiểm gần nhất trong tòa nhà bạn đang ở.',
      '<strong>Bài học:</strong> Không dùng thang máy khi có cháy. Luôn dùng cầu thang bộ.',
      '<strong>Bài học:</strong> Khói gây chết nhiều hơn lửa. Cúi thấp khi đi qua khói.',
      '<strong>Bài học:</strong> Mặt nạ phòng độc bảo vệ khỏi khí độc. Luôn trang bị mặt nạ.',
      '<strong>Bài học:</strong> Lập kế hoạch thoát hiểm cho gia đình và luyện tập thường xuyên.',
      '<strong>Bài học:</strong> Bạn đã thông thạo PCCC! Hãy áp dụng những kỹ năng này trong thực tế.'
    ];
    var tip = lessonTips[lv] || lessonTips[0];

    if (lv + 1 >= LEVELS.length) {
      showStarOverlay('🏆 CHIẾN THẮNG!',
        'Điểm tổng: ' + sc,
        tip, starRating, 'CHƠI LẠI',
        function () { hp = 3; sc = 0; hideOvl(); loadLv(0); });
    } else {
      showStarOverlay('✅ THOÁT NẠN THÀNH CÔNG!',
        'Thưởng: +' + bonus + ' điểm',
        tip, starRating, 'MÀN TIẾP',
        function () { hideOvl(); loadLv(lv + 1); },
        'CHƠI LẠI MÀN', function () { hideOvl(); loadLv(lv); });
    }
  }

  function winAll() { winLv(); }

  // ==================== PARTICLES & FLOATING MESSAGES ====================
  function spark(gx, gy, col, n) {
    for (var i = 0; i < n; i++) {
      particles.push({
        x: gx * T + T / 2, y: gy * T + T / 2,
        vx: (Math.random() - .5) * 6, vy: (Math.random() - .5) * 6,
        life: 30 + Math.random() * 25, ml: 55, col: col,
        sz: 2 + Math.random() * 5
      });
    }
  }

  function fmsg(gx, gy, text) {
    fmsgs.push({ x: gx * T + T / 2, y: gy * T, text: text, life: 60 });
  }

  function showEduTip(tip) {
    fmsgs = fmsgs.filter(function (m) { return !m.isEduTip; });
    fmsgs.push({ x: cv.width / 2, y: cv.height - 40, text: String(tip).trim(), life: 160, isEduTip: true });
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
        spark(nx, ny, '#ffff00', 15); fmsg(nx, ny, 'Ngắt điện!'); updHUD();
        showEduTip('Bài học: Luôn ngắt điện trước khi tiếp cận dây điện!');
        completeObjective('breaker');
        return;
      }
      if (t === GASV && !gasOff) {
        gasOff = true; sc += 30;
        for (var r = 0; r < mapH; r++) for (var c = 0; c < mapW; c++) if (map[r][c] === GASL) map[r][c] = F;
        spark(nx, ny, '#00ffaa', 12); fmsg(nx, ny, 'Khóa gas!'); updHUD();
        showEduTip('Bài học: Khóa van gas TRƯỚC KHI dập lửa gần nguồn gas!');
        completeObjective('gas_off');
        return;
      }
      if (t === PHONE && !called114) {
        called114 = true; sc += 50;
        spark(nx, ny, '#4fc3f7', 15); fmsg(nx, ny, 'Gọi 114!'); updHUD();
        showEduTip('Bài học: Luôn gọi 114 ngay khi phát hiện cháy!');
        completeObjective('call_114');
        return;
      }
      // Use BCC to extinguish adjacent fire
      if (t === FIRE && inv.bcc) {
        _useBccAt(nx, ny); return;
      }
      // Use KEY on adjacent locked door
      if (t === DLCK && inv.key) {
        map[ny][nx] = F; inv.key = false; sc += 40;
        spark(nx, ny, '#ffd93d', 12); fmsg(nx, ny, 'Mở khóa!'); updInv();
        showEduTip('Bài học: Luôn mang theo chìa khóa khi thoát hiểm!');
        return;
      }
    }
  }

  function _useBccAt(fx, fy) {
    map[fy][fx] = F;
    bccCharges++;
    fireExtinguished++;
    sc += 50; spark(fx, fy, '#87ceeb', 15); fmsg(fx, fy, 'Dập lửa!');
    checkExtinguishObj();
    if (bccCharges >= BCC_MAX) {
      inv.bcc = false; bccCharges = 0;
      showEduTip('Bình chữa cháy hết! Tìm bình mới nếu cần.');
    } else {
      showEduTip('Bình chữa cháy còn ' + (BCC_MAX - bccCharges) + ' lần sử dụng.');
    }
    updInv(); updHUD();
  }

  // ==================== MOVEMENT ====================
  function move(dx, dy) {
    if (!run || !map) return;

    // Cooldown
    var now = Date.now();
    if (now - lastMoveTime < MOVE_COOLDOWN_MS) return;
    lastMoveTime = now;

    var nx = p.x + dx, ny = p.y + dy;
    if (nx < 0 || nx >= mapW || ny < 0 || ny >= mapH) return;
    var t = map[ny][nx];

    pDir = { dx: dx, dy: dy };

    // Hard blocks
    if (t === W || t === FUR) return;

    // Interactive objects — block until activated, then walkable
    if (t === BRKR) {
      if (!breakerOff) { fmsg(nx, ny, 'Nhấn Space!'); return; }
      // already activated → walk through
    }
    if (t === GASV) {
      if (!gasOff) { fmsg(nx, ny, 'Nhấn Space!'); return; }
    }
    if (t === PHONE) {
      if (!called114) { fmsg(nx, ny, 'Nhấn Space!'); return; }
    }

    // Electric tile - needs breaker off
    if (t === ELEC) {
      if (!breakerOff) { die('Bị điện giật! Phải tìm và ngắt cầu dao trước.'); return; }
      else { map[ny][nx] = F; }
    }

    // Gas leak
    if (t === GASL) {
      if (!gasOff) { die('Khí gas bùng cháy! Phải khóa van gas trước.'); return; }
    }

    // Fire — use BCC to extinguish, otherwise DIE
    if (t === FIRE) {
      if (inv.bcc) {
        _useBccAt(nx, ny);
        _doMove(nx, ny, dx, dy);
      } else {
        _doMove(nx, ny, dx, dy);
        triggerShake(15, 6);
        die('Bạn đã bước vào lửa mà không có bình chữa cháy!');
      }
      return;
    }

    // Smoke - blocked unless TWL or MSK
    if (t === SMK) {
      if (inv.twl) {
        twlTimeMs -= 1500;
        if (twlTimeMs <= 0) {
          inv.twl = false; twlTimeMs = 0;
          showEduTip('Khăn ướt hết hiệu lực! Cần tìm chiếc khăn mới.');
        } else {
          showEduTip('Khăn ướt còn ' + Math.ceil(twlTimeMs / 1000) + ' giây hiệu lực.');
        }
        crouching = true;
        _doMove(nx, ny, dx, dy);
        sc += 20; updInv(); updHUD();
        return;
      }
      if (inv.msk) {
        crouching = true;
        _doMove(nx, ny, dx, dy);
        sc += 20; updHUD();
        showEduTip('Mặt nạ bảo vệ khỏi khí độc và khói!');
        return;
      }
      fmsg(nx, ny, 'Cần khăn ướt!');
      showEduTip('Bạn cần khăn ướt (TWL) hoặc mặt nạ (MSK) để đi qua khói!');
      return;
    }

    // Locked door - needs KEY
    if (t === DLCK) {
      if (inv.key) {
        map[ny][nx] = F; inv.key = false; sc += 40;
        spark(nx, ny, '#ffd93d', 12); fmsg(nx, ny, 'Mở khóa!'); updInv();
        showEduTip('Bài học: Luôn mang theo chìa khóa khi thoát hiểm!');
      } else {
        fmsg(nx, ny, 'Cần chìa khóa!');
        showEduTip('Cửa bị khóa! Tìm chìa khóa (KEY) để mở cửa.');
      }
      return;
    }

    // Pickups
    if (t === BCC) {
      inv.bcc = true; bccCharges = 0;
      spark(nx, ny, '#ff6b35', 10); fmsg(nx, ny, 'Bình chữa cháy!');
      sc += 30; map[ny][nx] = F;
      showEduTip('Bài học: Bình chữa cháy: Kéo chốt - Hướng nozzle - Bóp - Quét (PASS)');
      completeObjective('collect_bcc');
      updInv(); updHUD();
      _doMove(nx, ny, dx, dy);
      return;
    }
    if (t === TWL) {
      inv.twl = true; twlTimeMs = TWL_DURATION;
      spark(nx, ny, '#87ceeb', 10); fmsg(nx, ny, 'Khăn ướt!');
      sc += 30; map[ny][nx] = F;
      showEduTip('Bài học: Khăn ướt giúp bảo vệ hô hấp khi phải đi qua khu vực khói!');
      completeObjective('collect_twl');
      updInv(); updHUD();
      _doMove(nx, ny, dx, dy);
      return;
    }
    if (t === MSK) {
      inv.msk = true;
      spark(nx, ny, '#a0a0ff', 10); fmsg(nx, ny, 'Mặt nạ!');
      sc += 30; map[ny][nx] = F;
      showEduTip('Bài học: Mặt nạ phòng độc bảo vệ khỏi khí độc và khói dày!');
      completeObjective('collect_mask');
      updInv(); updHUD();
      _doMove(nx, ny, dx, dy);
      return;
    }
    if (t === KEY) {
      inv.key = true;
      spark(nx, ny, '#ffd93d', 10); fmsg(nx, ny, 'Chìa khóa!');
      sc += 30; map[ny][nx] = F;
      showEduTip('Bài học: Luôn kiểm tra và mang theo chìa khóa khi thoát hiểm!');
      completeObjective('collect_key');
      updInv(); updHUD();
      _doMove(nx, ny, dx, dy);
      return;
    }

    // EXIT check
    if (t === EXIT) {
      if (allObjDone) {
        _doMove(nx, ny, dx, dy);
        winLv();
        return;
      } else {
        fmsg(nx, ny, 'Chưa hoàn thành nhiệm vụ!');
        showEduTip('Hoàn thành TẤT CẢ nhiệm vụ trước khi thoát!');
        triggerShake(8, 3);
        return;
      }
    }

    // Normal floor movement
    crouching = false;
    _doMove(nx, ny, dx, dy);
    updHUD();
  }

  function _doMove(nx, ny, dx, dy) {
    // Start smooth animation
    pAnim = { sx: p.x, sy: p.y, tx: nx, ty: ny, t: 0, dur: 0.12 };
    p.x = nx; p.y = ny;
    updateCamera();
  }

  // ==================== INPUT ====================
  function keyToDir(key) {
    switch (key) {
      case 'ArrowUp': case 'w': case 'W': return [0, -1];
      case 'ArrowDown': case 's': case 'S': return [0, 1];
      case 'ArrowLeft': case 'a': case 'A': return [-1, 0];
      case 'ArrowRight': case 'd': case 'D': return [1, 0];
      default: return null;
    }
  }

  function startHeldMovement() {
    if (heldTimer) return;
    heldTimer = setInterval(function () {
      var keys = Object.keys(heldKeys);
      for (var i = keys.length - 1; i >= 0; i--) {
        var dir = keyToDir(keys[i]);
        if (dir) { move(dir[0], dir[1]); return; }
      }
    }, HELD_INTERVAL_MS);
  }

  function stopHeldMovement() {
    if (Object.keys(heldKeys).length === 0 && heldTimer) {
      clearInterval(heldTimer);
      heldTimer = null;
    }
  }

  document.addEventListener('keydown', function (e) {
    var dir = keyToDir(e.key);
    if (dir) {
      e.preventDefault();
      if (!heldKeys[e.key]) {
        heldKeys[e.key] = true;
        move(dir[0], dir[1]);   // instant first step
        startHeldMovement();
      }
      return;
    }
    if (e.key === ' ' || e.key === 'Enter') { e.preventDefault(); interact(); }
  });

  document.addEventListener('keyup', function (e) {
    delete heldKeys[e.key];
    stopHeldMovement();
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
  function dFloor(sx, sy) {
    cx.fillStyle = '#c2b89a';
    cx.fillRect(sx, sy, T, T);
    cx.strokeStyle = '#a89a7a';
    cx.lineWidth = 1;
    cx.strokeRect(sx + 0.5, sy + 0.5, T - 1, T - 1);
    cx.fillStyle = '#b5a88c';
    cx.fillRect(sx + 3, sy + 3, T / 2 - 4, T / 2 - 4);
    cx.fillRect(sx + T / 2 + 1, sy + T / 2 + 1, T / 2 - 4, T / 2 - 4);
  }

  function dWall(sx, sy) {
    cx.fillStyle = '#0e0f18';
    cx.fillRect(sx, sy, T, T);
    cx.fillStyle = '#181928';
    var bh = Math.floor(T / 3);
    for (var row = 0; row < 3; row++) {
      var offset = (row % 2 === 0) ? 0 : Math.floor(T / 2);
      cx.fillRect(sx + offset + 1, sy + row * bh + 1, Math.floor(T / 2) - 3, bh - 2);
      cx.fillRect(sx + offset + Math.floor(T / 2) + 1, sy + row * bh + 1, Math.floor(T / 2) - 3, bh - 2);
    }
    cx.fillStyle = 'rgba(255,255,255,0.04)';
    cx.fillRect(sx, sy, T, 1);
  }

  function dFurn(sx, sy) {
    dFloor(sx, sy);
    cx.fillStyle = '#7a5618';
    cx.fillRect(sx + 4, sy + 4, T - 8, T - 8);
    cx.fillStyle = '#8f6820';
    cx.fillRect(sx + 4, sy + 4, T - 8, 6);
    cx.strokeStyle = '#4a3208';
    cx.lineWidth = 1.5;
    cx.strokeRect(sx + 4, sy + 4, T - 8, T - 8);
  }

  function dFire(sx, sy) {
    dFloor(sx, sy);
    var t = tick;
    cx.fillStyle = 'rgba(255,80,0,0.25)';
    cx.fillRect(sx, sy, T, T);
    // Base flame
    cx.fillStyle = '#c0200a';
    cx.beginPath();
    cx.moveTo(sx + 5, sy + T - 3);
    cx.quadraticCurveTo(sx + 3, sy + T * 0.5 + Math.sin(t * 0.3) * 5, sx + T * 0.35, sy + T * 0.25 + Math.sin(t * 0.25) * 4);
    cx.quadraticCurveTo(sx + T / 2, sy + 3 + Math.cos(t * 0.2) * 4, sx + T * 0.65, sy + T * 0.25 + Math.sin(t * 0.2) * 4);
    cx.quadraticCurveTo(sx + T - 3, sy + T * 0.5 + Math.cos(t * 0.3) * 5, sx + T - 5, sy + T - 3);
    cx.closePath(); cx.fill();
    // Mid flame
    cx.fillStyle = '#ff6b00';
    cx.beginPath();
    cx.moveTo(sx + 9, sy + T - 4);
    cx.quadraticCurveTo(sx + 7, sy + T * 0.55 + Math.sin(t * 0.35) * 4, sx + T * 0.4, sy + T * 0.35 + Math.sin(t * 0.3) * 3);
    cx.quadraticCurveTo(sx + T / 2, sy + 10 + Math.cos(t * 0.25) * 4, sx + T * 0.6, sy + T * 0.35 + Math.cos(t * 0.3) * 3);
    cx.quadraticCurveTo(sx + T - 9, sy + T * 0.55 + Math.cos(t * 0.35) * 4, sx + T - 9, sy + T - 4);
    cx.closePath(); cx.fill();
    // Inner flame
    cx.fillStyle = '#ffd700';
    cx.beginPath();
    cx.moveTo(sx + 14, sy + T - 5);
    cx.quadraticCurveTo(sx + T / 2, sy + T * 0.3 + Math.sin(t * 0.4) * 5, sx + T - 14, sy + T - 5);
    cx.closePath(); cx.fill();
    // Embers
    if (Math.sin(t * 0.4) > 0.6) {
      cx.fillStyle = '#fff7a0';
      for (var i = 0; i < 3; i++) {
        var ex = sx + 8 + Math.sin(t * 0.3 + i * 2) * 10;
        var ey = sy + 5 + Math.cos(t * 0.5 + i) * 5;
        cx.beginPath(); cx.arc(ex, ey, 2, 0, Math.PI * 2); cx.fill();
      }
    }
    // Label
    cx.fillStyle = '#ffddaa';
    cx.font = 'bold 9px Arial';
    cx.textAlign = 'center';
    cx.fillText('LỬA', sx + T / 2, sy + T - 3);
  }

  function dSmoke(sx, sy) {
    dFloor(sx, sy);
    var t = tick;
    for (var layer = 0; layer < 4; layer++) {
      var alpha = 0.2 + Math.sin(t * 0.08 + layer * 1.1) * 0.07;
      cx.fillStyle = 'rgba(110,115,130,' + alpha + ')';
      for (var i = 0; i < 3; i++) {
        var ox = Math.sin(t * 0.05 + i * 2 + layer) * 5 + layer * 10;
        var oy = Math.cos(t * 0.04 + i * 1.5) * 3;
        cx.beginPath();
        cx.ellipse(sx + 6 + i * 11 + ox, sy + 10 + i * 6 + oy, 9 + i * 2, 6 + i, 0, 0, Math.PI * 2);
        cx.fill();
      }
    }
    for (var j = 0; j < 5; j++) {
      var rise = (t * 0.08 + j * 0.6) % 11;
      cx.fillStyle = 'rgba(160,165,180,' + (0.3 + Math.sin(t * 0.1 + j) * 0.1) + ')';
      cx.beginPath();
      cx.arc(sx + 6 + j * 8 + Math.sin(t * 0.06 + j) * 3, sy + 4 - rise, 2.5, 0, Math.PI * 2);
      cx.fill();
    }
    cx.fillStyle = 'rgba(200,200,210,0.5)';
    cx.font = 'bold 9px Arial';
    cx.textAlign = 'center';
    cx.fillText('KHÓI', sx + T / 2, sy + T - 3);
  }

  function dExit(sx, sy) {
    dFloor(sx, sy);
    if (allObjDone) {
      // Open exit - green glow
      var g = 0.5 + Math.sin(tick * 0.1) * 0.25;
      cx.fillStyle = 'rgba(16,185,129,' + g * 0.5 + ')';
      cx.fillRect(sx, sy, T, T);
      cx.fillStyle = '#065f46';
      cx.fillRect(sx + 3, sy + 3, T - 6, T - 6);
      cx.fillStyle = '#10b981';
      cx.fillRect(sx + 6, sy + 7, T - 12, T - 10);
      cx.fillStyle = '#ffd700';
      cx.beginPath(); cx.arc(sx + T - 12, sy + T / 2, 3.5, 0, Math.PI * 2); cx.fill();
      cx.strokeStyle = 'rgba(52,211,153,' + g + ')';
      cx.lineWidth = 2.5;
      cx.strokeRect(sx + 3, sy + 3, T - 6, T - 6);
      cx.lineWidth = 1;
      cx.fillStyle = '#ffffff';
      cx.font = 'bold 11px Arial';
      cx.textAlign = 'center';
      cx.fillText('EXIT', sx + T / 2, sy + T - 4);
      // Arrow
      cx.fillStyle = '#ffffff';
      cx.beginPath();
      cx.moveTo(sx + T / 2 - 6, sy + 16);
      cx.lineTo(sx + T / 2 + 6, sy + 16);
      cx.lineTo(sx + T / 2, sy + 10);
      cx.closePath(); cx.fill();
    } else {
      // Locked exit - red
      var r = 0.5 + Math.sin(tick * 0.15) * 0.25;
      cx.fillStyle = 'rgba(220,38,38,' + r * 0.3 + ')';
      cx.fillRect(sx, sy, T, T);
      cx.fillStyle = '#3b0000';
      cx.fillRect(sx + 3, sy + 3, T - 6, T - 6);
      cx.fillStyle = '#7f1d1d';
      cx.fillRect(sx + 6, sy + 7, T - 12, T - 10);
      cx.strokeStyle = 'rgba(220,38,38,' + r + ')';
      cx.lineWidth = 2.5;
      cx.strokeRect(sx + 3, sy + 3, T - 6, T - 6);
      cx.lineWidth = 1;
      // Lock icon
      cx.fillStyle = '#ffd700';
      cx.beginPath(); cx.arc(sx + T / 2, sy + T / 2 - 6, 6, 0, Math.PI * 2); cx.fill();
      cx.fillStyle = '#ff8f00';
      cx.fillRect(sx + T / 2 - 5, sy + T / 2 - 1, 10, 10);
      cx.fillStyle = '#3e2723';
      cx.fillRect(sx + T / 2 - 1, sy + T / 2 + 1, 2, 5);
      cx.fillStyle = '#ff4444';
      cx.font = 'bold 8px Arial';
      cx.textAlign = 'center';
      cx.fillText('KHÓA', sx + T / 2, sy + T - 3);
    }
  }

  function dBCC(sx, sy) {
    dFloor(sx, sy);
    var b = Math.sin(tick * 0.12) * 2;
    cx.fillStyle = '#dc2626';
    cx.fillRect(sx + 13, sy + 10 + b, 18, 24);
    cx.fillStyle = '#1c1c1c';
    cx.fillRect(sx + 15, sy + 6 + b, 14, 6);
    cx.fillStyle = '#555';
    cx.fillRect(sx + 16, sy + 4 + b, 12, 5);
    cx.fillStyle = 'rgba(255,255,255,0.3)';
    cx.fillRect(sx + 14, sy + 12 + b, 4, 15);
    cx.fillStyle = '#fff';
    cx.font = 'bold 8px Arial';
    cx.textAlign = 'center';
    cx.fillText('BCC', sx + T / 2, sy + T - 3);
    cx.fillStyle = 'rgba(220,38,38,0.12)';
    cx.beginPath(); cx.arc(sx + T / 2, sy + T / 2, 18, 0, Math.PI * 2); cx.fill();
  }

  function dTwl(sx, sy) {
    dFloor(sx, sy);
    var b = Math.sin(tick * 0.1) * 2;
    cx.fillStyle = '#1d6fa4';
    cx.fillRect(sx + 8, sy + 12 + b, 28, 10);
    cx.fillStyle = '#2196f3';
    cx.fillRect(sx + 10, sy + 20 + b, 24, 9);
    cx.fillStyle = '#87ceeb';
    for (var i = 0; i < 3; i++) {
      var drop = (tick * 0.1 + i) % 8;
      cx.beginPath(); cx.arc(sx + 12 + i * 9, sy + 28 + drop, 2.5, 0, Math.PI * 2); cx.fill();
    }
    cx.fillStyle = '#87ceeb';
    cx.font = 'bold 8px Arial';
    cx.textAlign = 'center';
    cx.fillText('KHĂN', sx + T / 2, sy + T - 2);
  }

  function dMask(sx, sy) {
    dFloor(sx, sy);
    var b = Math.sin(tick * 0.1) * 2;
    cx.fillStyle = '#9e9e9e';
    cx.beginPath();
    cx.ellipse(sx + T / 2, sy + T / 2 + b - 1, 16, 12, 0, 0, Math.PI * 2);
    cx.fill();
    cx.strokeStyle = '#757575'; cx.lineWidth = 2;
    cx.beginPath(); cx.moveTo(sx + T / 2 - 16, sy + T / 2 + b - 1); cx.lineTo(sx + 3, sy + T / 2 + b - 6); cx.stroke();
    cx.beginPath(); cx.moveTo(sx + T / 2 + 16, sy + T / 2 + b - 1); cx.lineTo(sx + T - 3, sy + T / 2 + b - 6); cx.stroke();
    cx.lineWidth = 1;
    cx.fillStyle = '#bdbdbd';
    cx.fillRect(sx + T / 2 - 6, sy + T / 2 + b - 4, 12, 8);
    cx.fillStyle = '#e53935';
    cx.fillRect(sx + T / 2 - 1, sy + T / 2 + b - 5, 2, 10);
    cx.fillRect(sx + T / 2 - 5, sy + T / 2 + b - 1, 10, 2);
    cx.fillStyle = '#bdbdbd';
    cx.font = 'bold 8px Arial';
    cx.textAlign = 'center';
    cx.fillText('MASK', sx + T / 2, sy + T - 2);
  }

  function dKey(sx, sy) {
    dFloor(sx, sy);
    var b = Math.sin(tick * 0.12) * 2;
    cx.save();
    cx.translate(sx + T / 2, sy + T / 2 + b);
    cx.rotate(Math.sin(tick * 0.05) * 0.15);
    cx.strokeStyle = '#f59e0b'; cx.lineWidth = 3;
    cx.beginPath(); cx.arc(-8, -3, 7, 0, Math.PI * 2); cx.stroke();
    cx.fillStyle = '#f59e0b';
    cx.fillRect(-2, -5, 16, 4);
    cx.fillRect(7, -1, 4, 6);
    cx.fillRect(12, -1, 4, 5);
    cx.restore();
    cx.fillStyle = 'rgba(245,158,11,0.15)';
    cx.beginPath(); cx.arc(sx + T / 2, sy + T / 2, 16, 0, Math.PI * 2); cx.fill();
    cx.fillStyle = '#f59e0b';
    cx.font = 'bold 8px Arial';
    cx.textAlign = 'center';
    cx.fillText('KEY', sx + T / 2, sy + T - 2);
  }

  function dLock(sx, sy) {
    cx.fillStyle = '#5c4033';
    cx.fillRect(sx, sy, T, T);
    cx.fillStyle = '#6d4c41';
    cx.fillRect(sx + 4, sy + 3, T - 8, T - 6);
    cx.strokeStyle = '#3e2723'; cx.lineWidth = 1;
    cx.strokeRect(sx + 4, sy + 3, T - 8, T - 6);
    cx.fillStyle = '#ffd700';
    cx.beginPath(); cx.arc(sx + T / 2, sy + T / 2 - 5, 6, 0, Math.PI * 2); cx.fill();
    cx.fillStyle = '#ff8f00';
    cx.fillRect(sx + T / 2 - 5, sy + T / 2, 10, 10);
    cx.fillStyle = '#3e2723';
    cx.fillRect(sx + T / 2 - 1, sy + T / 2 + 2, 2, 5);
    cx.fillStyle = '#ff3d00';
    cx.font = 'bold 8px Arial';
    cx.textAlign = 'center';
    cx.fillText('LOCK', sx + T / 2, sy + T - 2);
  }

  function dElec(sx, sy) {
    dFloor(sx, sy);
    var t = tick;
    cx.strokeStyle = '#212121'; cx.lineWidth = 4;
    cx.beginPath(); cx.moveTo(sx + 3, sy + T / 2); cx.lineTo(sx + T - 3, sy + T / 2); cx.stroke();
    cx.lineWidth = 1;
    if (Math.sin(t * 0.3) > 0) {
      cx.fillStyle = '#ffee58';
      for (var i = 0; i < 5; i++) {
        var sx2 = sx + 8 + Math.random() * 24, sy2 = sy + T / 2 - 8 + Math.random() * 16;
        cx.fillRect(sx2, sy2, 3, 3);
      }
      cx.fillStyle = 'rgba(255,235,59,0.12)';
      cx.fillRect(sx, sy, T, T);
    }
    cx.fillStyle = '#ffee58';
    cx.font = 'bold 8px Arial';
    cx.textAlign = 'center';
    cx.fillText('ĐIỆN', sx + T / 2, sy + T - 3);
  }

  function dBrkr(sx, sy) {
    dFloor(sx, sy);
    cx.fillStyle = breakerOff ? '#1b5e20' : '#b71c1c';
    cx.fillRect(sx + 8, sy + 5, 28, 34);
    cx.strokeStyle = '#777';
    cx.strokeRect(sx + 8, sy + 5, 28, 34);
    cx.fillStyle = breakerOff ? '#4caf50' : '#f44336';
    cx.fillRect(sx + 14, sy + (breakerOff ? 26 : 12), 16, 10);
    cx.fillStyle = '#fff';
    cx.font = 'bold 8px Arial';
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
      cx.arc(sx + 8 + i * 14 + Math.sin(tick * 0.05 + i) * 4, sy + 12 + i * 8 + Math.cos(tick * 0.04 + i) * 4, 5 + i, 0, Math.PI * 2);
      cx.fill();
    }
    cx.fillStyle = '#ffa726';
    cx.font = 'bold 8px Arial';
    cx.textAlign = 'center';
    cx.fillText('GAS', sx + T / 2, sy + T - 2);
  }

  function dGasV(sx, sy) {
    dFloor(sx, sy);
    cx.fillStyle = gasOff ? '#1b5e20' : '#b71c1c';
    cx.fillRect(sx + 8, sy + 5, 28, 34);
    cx.strokeStyle = '#777';
    cx.strokeRect(sx + 8, sy + 5, 28, 34);
    cx.fillStyle = gasOff ? '#4caf50' : '#f44336';
    cx.beginPath(); cx.arc(sx + T / 2, sy + T / 2, 8, 0, Math.PI * 2); cx.fill();
    cx.fillStyle = '#fff';
    cx.font = 'bold 8px Arial';
    cx.textAlign = 'center';
    cx.fillText(gasOff ? 'ĐÓNG' : 'MỞ', sx + T / 2, sy + T - 3);
  }

  function dPhone(sx, sy) {
    dFloor(sx, sy);
    var g = called114 ? '#10b981' : 'rgba(79,195,247,' + (0.5 + Math.sin(tick * 0.1) * 0.3) + ')';
    cx.fillStyle = g;
    cx.fillRect(sx + 13, sy + 6, 18, 28);
    cx.fillStyle = '#1c1c1c';
    cx.fillRect(sx + 15, sy + 9, 14, 16);
    cx.fillStyle = called114 ? '#10b981' : '#4fc3f7';
    cx.beginPath(); cx.arc(sx + T / 2, sy + 29, 5, 0, Math.PI * 2); cx.fill();
    cx.fillStyle = '#fff';
    cx.font = 'bold 9px Arial';
    cx.textAlign = 'center';
    cx.fillText(called114 ? 'OK' : '114', sx + T / 2, sy + T - 2);
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
      case EXIT: dExit(sx, sy); break;
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
      default: dFloor(sx, sy);
    }
  }

  // ==================== PLAYER DRAW ====================
  function dPlayer() {
    if (!map) return;

    // Smooth interpolated position
    var drawX, drawY;
    if (pAnim.t < 1) {
      var ease = pAnim.t * pAnim.t * (3 - 2 * pAnim.t); // smoothstep
      drawX = pAnim.sx + (pAnim.tx - pAnim.sx) * ease;
      drawY = pAnim.sy + (pAnim.ty - pAnim.sy) * ease;
    } else {
      drawX = p.x;
      drawY = p.y;
    }

    var sx = (drawX - camTX) * T;
    var sy = (drawY - camTY) * T;

    // Shadow
    cx.fillStyle = 'rgba(0,0,0,0.45)';
    cx.beginPath();
    cx.ellipse(sx + T / 2 + 2, sy + T - 4, 14, 5, 0, 0, Math.PI * 2);
    cx.fill();

    if (crouching) {
      cx.fillStyle = '#fbbf24';
      cx.beginPath();
      cx.ellipse(sx + T / 2, sy + T * 0.65, 16, 11, 0, 0, Math.PI * 2);
      cx.fill();
      cx.fillStyle = '#fde68a';
      cx.beginPath();
      cx.arc(sx + T / 2 - 6, sy + T * 0.48, 8, 0, Math.PI * 2);
      cx.fill();
      cx.fillStyle = '#1565c0';
      cx.fillRect(sx + T / 2 - 9, sy + T * 0.33, 16, 5);
    } else {
      // Body
      cx.fillStyle = '#fbbf24';
      cx.fillRect(sx + 12, sy + 18, 20, 18);
      if (inv.bcc) {
        cx.fillStyle = '#dc2626';
        cx.fillRect(sx + 12, sy + 18, 4, 18);
        cx.fillRect(sx + 28, sy + 18, 4, 18);
      } else {
        cx.fillStyle = '#1d4ed8';
        cx.fillRect(sx + 12, sy + 30, 8, 6);
        cx.fillRect(sx + 24, sy + 30, 8, 6);
      }
      // Head
      cx.fillStyle = '#fde68a';
      cx.beginPath(); cx.arc(sx + T / 2, sy + 14, 9, 0, Math.PI * 2); cx.fill();
      // Helmet
      cx.fillStyle = '#f59e0b';
      cx.fillRect(sx + T / 2 - 10, sy + 6, 20, 6);
      cx.fillRect(sx + T / 2 - 8, sy + 4, 16, 5);
      // Eyes
      cx.fillStyle = '#1c1c1c';
      cx.beginPath(); cx.arc(sx + T / 2 - 4, sy + 13, 2, 0, Math.PI * 2); cx.fill();
      cx.beginPath(); cx.arc(sx + T / 2 + 4, sy + 13, 2, 0, Math.PI * 2); cx.fill();
      // Item indicators
      if (inv.twl) {
        cx.fillStyle = '#2196f3';
        cx.fillRect(sx + T / 2 - 8, sy + 6, 16, 3);
      }
      if (inv.msk) {
        cx.fillStyle = '#9e9e9e';
        cx.fillRect(sx + T / 2 - 6, sy + 15, 12, 6);
      }
    }
  }

  // ==================== MINIMAP ====================
  function drawMinimap() {
    var mmCanvas = document.getElementById('minimap-canvas');
    if (!mmCanvas || !map) return;
    var mmCx = mmCanvas.getContext('2d');
    var ms = 4; // minimap tile size
    mmCanvas.width = mapW * ms;
    mmCanvas.height = mapH * ms;

    for (var r = 0; r < mapH; r++) {
      for (var c = 0; c < mapW; c++) {
        var t = map[r][c];
        var col = '#111';
        switch (t) {
          case F: col = '#756b55'; break;
          case W: col = '#1a1a2e'; break;
          case FIRE: col = '#ff4400'; break;
          case SMK: col = '#888899'; break;
          case EXIT: col = allObjDone ? '#10b981' : '#ff4444'; break;
          case BCC: col = '#ff6b35'; break;
          case TWL: col = '#2196f3'; break;
          case MSK: col = '#9e9e9e'; break;
          case KEY: col = '#f59e0b'; break;
          case DLCK: col = '#5c4033'; break;
          case ELEC: col = '#ffee58'; break;
          case BRKR: col = breakerOff ? '#4caf50' : '#ff4444'; break;
          case GASL: col = '#ff9800'; break;
          case GASV: col = gasOff ? '#4caf50' : '#ff4444'; break;
          case PHONE: col = '#4fc3f7'; break;
          case FUR: col = '#7a5618'; break;
          default: col = '#756b55';
        }
        mmCx.fillStyle = col;
        mmCx.fillRect(c * ms, r * ms, ms, ms);
      }
    }

    // Player
    mmCx.fillStyle = '#00ff00';
    mmCx.fillRect(p.x * ms - 1, p.y * ms - 1, ms + 2, ms + 2);

    // Viewport box
    mmCx.strokeStyle = 'rgba(255,255,255,0.6)';
    mmCx.lineWidth = 1;
    mmCx.strokeRect(camTX * ms, camTY * ms,
      Math.min(VIEW_COLS, mapW) * ms, Math.min(VIEW_ROWS, mapH) * ms);
  }

  // ==================== MAIN RENDER ====================
  var lastTime = 0;
  var frameTime = 1 / 60;

  function render(timestamp) {
    if (!lastTime) lastTime = timestamp;
    var dt = (timestamp - lastTime) / 1000;
    lastTime = timestamp;
    tick++;

    // Update smooth animation
    if (pAnim.t < 1) {
      pAnim.t += dt / pAnim.dur;
      if (pAnim.t > 1) pAnim.t = 1;
    }

    // Screen shake
    var shakeX = 0, shakeY = 0;
    if (shakeTime > 0) {
      shakeX = (Math.random() - 0.5) * shakeMag;
      shakeY = (Math.random() - 0.5) * shakeMag;
      shakeTime--;
      shakeMag *= 0.95;
    }

    cx.save();
    cx.translate(shakeX, shakeY);

    cx.clearRect(-10, -10, cv.width + 20, cv.height + 20);
    cx.fillStyle = '#111827';
    cx.fillRect(-10, -10, cv.width + 20, cv.height + 20);

    if (map) {
      var visionR = 6;
      if (inv.twl) visionR += 1;
      if (inv.msk) visionR += 1;
      if (inv.bcc) visionR += 1;
      if (inv.key) visionR += 1;
      visionR = Math.min(10, visionR);

      var visRows = Math.min(VIEW_ROWS, mapH);
      var visCols = Math.min(VIEW_COLS, mapW);

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
            cx.fillStyle = '#05060f';
            cx.fillRect(sx, sy, T, T);
          }
        }
      }

      dPlayer();

      // Soft fog edge
      var playerSX = (p.x - camTX) * T + T / 2;
      var playerSY = (p.y - camTY) * T + T / 2;
      var edgeGrad = cx.createRadialGradient(
        playerSX, playerSY, (visionR - 1.5) * T,
        playerSX, playerSY, (visionR + 0.5) * T
      );
      edgeGrad.addColorStop(0, 'rgba(5,6,15,0)');
      edgeGrad.addColorStop(1, 'rgba(5,6,15,1)');
      cx.fillStyle = edgeGrad;
      cx.fillRect(0, 0, cv.width, cv.height);

    } else {
      cx.fillStyle = '#3b82f6';
      cx.font = 'bold 22px Arial';
      cx.textAlign = 'center';
      cx.fillText('Nhấn BẮT ĐẦU để chơi!', cv.width / 2, cv.height / 2);
    }

    // Particles
    var alive = [];
    for (var i = 0; i < particles.length; i++) {
      var q = particles[i];
      q.x += q.vx; q.y += q.vy; q.life--; q.sz *= 0.96;
      cx.globalAlpha = Math.max(0, q.life / q.ml);
      cx.fillStyle = q.col;
      cx.beginPath(); cx.arc(q.x, q.y, q.sz, 0, Math.PI * 2); cx.fill();
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
        cx.save();
        cx.globalAlpha = Math.min(1, Math.max(0, m.life / 100));
        cx.fillStyle = 'rgba(0,0,0,0.75)';
        var tipW = 640;
        if (cv.width < 700) tipW = cv.width - 40;
        cx.fillRect(cv.width / 2 - tipW / 2, cv.height - 55, tipW, 36);
        cx.strokeStyle = 'rgba(251,191,36,0.6)';
        cx.lineWidth = 1;
        cx.strokeRect(cv.width / 2 - tipW / 2, cv.height - 55, tipW, 36);
        cx.fillStyle = '#fde68a';
        cx.font = '13px Arial';
        cx.textAlign = 'center';
        cx.fillText(m.text.replace(/<[^>]+>/g, ''), cv.width / 2, cv.height - 32);
        cx.restore();
      } else {
        cx.globalAlpha = Math.max(0, m.life / 50);
        cx.fillStyle = '#ffd93d';
        cx.font = 'bold 12px Arial';
        cx.textAlign = 'center';
        cx.fillText(m.text, m.x - camTX * T, m.y - camTY * T);
      }
      if (m.life > 0) aliveM.push(m);
    }
    fmsgs = aliveM;
    cx.globalAlpha = 1;

    cx.restore(); // End screen shake

    // Minimap
    if (tick % 10 === 0) drawMinimap();

    requestAnimationFrame(render);
  }

  // ==================== BOOTSTRAP ====================
  window.startGame = function () { hideOvl(); loadLv(0); };

  function init() {
    if (window.GAME_LEVELS) {
      LEVELS = window.GAME_LEVELS;
      showOvl(
        'Thoát khỏi đám cháy',
        'Di chuyển: mũi tên / WASD\nTương tác: Space/Enter\n\nThu thập vật phẩm, hoàn thành nhiệm vụ và tìm lối thoát!',
        'BẮT ĐẦU CHƠI',
        function () { hideOvl(); loadLv(0); }
      );
    } else {
      setTimeout(init, 100);
    }
  }

  init();
  requestAnimationFrame(render);
})();
