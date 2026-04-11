/* ============================================================
   FRAS - Fire Escape Game Levels v5
   10 progressive levels (20x15 grid each)
   
   Tile IDs:
     0 = floor
     1 = wall
     2 = fire
     3 = smoke
     4 = exit (unlocked when objectives met)
     5 = BCC (fire extinguisher)
     6 = towel (wet towel)
     7 = mask (gas mask)
     8 = key
     9 = locked-door
    11 = player-start
    12 = furniture (flammable)
    13 = electric wire (dangerous)
    14 = breaker (circuit breaker)
    15 = gas-leak
    16 = gas-valve
    17 = phone (call 114)

   Design Rules:
   - Every path from PS(11) to EXIT(4) passes through >=1 obstacle
   - All items needed to clear obstacles are reachable
   - EXIT is always surrounded by walls + at least one obstacle type
   ============================================================ */

var _=0,W=1,I=2,S=3,X=4,B=5,T=6,M=7,K=8,D=9,
    P=11,R=12,E=13,BR=14,GL=15,GV=16,PH=17;

window.GAME_LEVELS = [

/* ======================================================
   LEVEL 1 — "Bước đầu tiên" (20x15)
   Objectives: Ngắt điện, Thu BCC, Thu chìa khóa
   Layout: Player top-left, EXIT bottom-right behind locked door
   Obstacles: Electric wire blocks path, fire blocks another path
   ====================================================== */
{
  nameVi: 'Bước đầu tiên',
  time: 150,
  fireSpread: 10,
  tip: 'Ngắt cầu dao điện trước, rồi tìm bình chữa cháy và chìa khóa!',
  desc: 'Tìm cách ngắt điện, lấy bình CC và chìa khóa để mở cửa thoát!',
  mapW: 20, mapH: 15,
  objectives: [
    { type: 'breaker', label: 'Ngắt cầu dao điện' },
    { type: 'collect_bcc', label: 'Thu bình chữa cháy' },
    { type: 'collect_key', label: 'Tìm chìa khóa' }
  ],
  map: [
    [W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W],
    [W,P,_,_,_,_,W,_,_,_,_,_,W,_,_,_,_,_,_,W],
    [W,_,W,W,W,_,W,_,W,W,W,_,W,_,W,W,W,W,_,W],
    [W,_,W,BR,_,_,_,_,W,K,_,_,_,_,W,_,_,_,_,W],
    [W,_,W,W,W,W,W,_,W,W,W,W,W,_,W,_,W,W,W,W],
    [W,_,_,_,_,_,_,_,_,_,_,_,_,_,W,_,_,_,_,W],
    [W,W,W,_,W,W,W,W,W,E,E,W,W,W,W,W,W,W,_,W],
    [W,_,_,_,W,_,_,_,_,_,_,_,_,_,_,_,_,W,_,W],
    [W,_,W,W,W,_,W,W,_,W,W,_,W,W,W,B,_,W,_,W],
    [W,_,_,_,_,_,W,_,_,_,W,_,_,_,W,W,_,_,_,W],
    [W,W,W,W,W,_,W,_,W,_,W,W,W,_,_,_,_,W,W,W],
    [W,_,_,_,_,_,_,_,W,_,_,_,_,_,W,W,_,_,_,W],
    [W,_,W,W,W,W,W,_,W,W,W,I,I,_,W,_,_,W,D,W],
    [W,_,_,_,_,_,_,_,_,_,_,_,_,_,W,_,_,_,X,W],
    [W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W]
  ]
},

/* ======================================================
   LEVEL 2 — "Hành lang khói" (20x15)
   Objectives: Ngắt điện, BCC, Chìa khóa, Khăn ướt
   Smoke corridor blocks path to EXIT area
   ====================================================== */
{
  nameVi: 'Hành lang khói',
  time: 140,
  fireSpread: 8,
  tip: 'Tìm khăn ướt để vượt qua hành lang đầy khói!',
  desc: 'Khói tràn ngập hành lang. Cần khăn ướt và nhiều vật phẩm!',
  mapW: 20, mapH: 15,
  objectives: [
    { type: 'breaker', label: 'Ngắt cầu dao điện' },
    { type: 'collect_bcc', label: 'Thu bình chữa cháy' },
    { type: 'collect_key', label: 'Tìm chìa khóa' },
    { type: 'collect_twl', label: 'Thu khăn ướt' }
  ],
  map: [
    [W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W],
    [W,P,_,_,_,W,_,_,_,_,W,_,_,_,_,_,_,_,_,W],
    [W,_,W,W,_,W,_,W,W,_,W,_,W,W,W,W,_,W,_,W],
    [W,_,W,T,_,_,_,W,BR,_,_,_,W,_,_,_,_,W,_,W],
    [W,_,W,W,W,W,_,W,W,W,W,W,W,_,W,W,W,W,_,W],
    [W,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,W],
    [W,W,W,W,W,_,W,W,S,S,S,S,S,S,W,W,W,W,W,W],
    [W,_,_,_,W,_,_,_,S,_,_,_,_,S,_,_,_,_,_,W],
    [W,_,W,_,W,W,W,_,S,_,W,W,_,S,_,W,W,W,_,W],
    [W,_,W,_,_,_,_,_,S,_,W,K,_,S,_,_,_,_,_,W],
    [W,_,W,W,W,W,W,_,S,S,S,S,S,S,_,W,E,E,W,W],
    [W,_,_,_,_,_,_,_,_,_,_,_,_,_,_,W,_,_,_,W],
    [W,_,W,W,W,_,W,W,W,_,W,W,_,W,W,W,I,I,D,W],
    [W,_,_,_,_,_,_,B,_,_,_,_,_,_,_,_,_,_,X,W],
    [W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W]
  ]
},

/* ======================================================
   LEVEL 3 — "Khu vực nguy hiểm" (20x15)
   Objectives: Ngắt điện, BCC, Chìa khóa, Khăn ướt, Gọi 114
   Phone (114) required - EXIT area locked behind call
   ====================================================== */
{
  nameVi: 'Khu vực nguy hiểm',
  time: 130,
  fireSpread: 7,
  tip: 'Gọi 114 sớm nhất có thể! Tìm điện thoại trong tòa nhà.',
  desc: 'Khu vực nhiều nguy hiểm. Cần gọi 114 để mở lối thoát!',
  mapW: 20, mapH: 15,
  objectives: [
    { type: 'breaker', label: 'Ngắt cầu dao điện' },
    { type: 'collect_bcc', label: 'Thu bình chữa cháy' },
    { type: 'collect_key', label: 'Tìm chìa khóa' },
    { type: 'collect_twl', label: 'Thu khăn ướt' },
    { type: 'call_114', label: 'Gọi 114' }
  ],
  map: [
    [W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W],
    [W,P,_,_,_,_,W,_,_,_,_,_,_,W,_,_,_,_,_,W],
    [W,_,W,W,W,_,W,_,W,W,W,W,_,W,_,W,W,W,_,W],
    [W,_,_,_,W,_,_,_,W,PH,_,_,_,_,_,W,BR,_,_,W],
    [W,W,W,_,W,W,W,W,W,W,W,_,W,W,W,W,W,E,E,W],
    [W,T,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,W],
    [W,W,W,W,W,_,W,S,S,S,S,S,W,_,W,W,W,W,_,W],
    [W,_,_,_,_,_,W,S,_,_,_,S,W,_,_,_,_,_,_,W],
    [W,_,W,W,W,_,W,S,_,K,_,S,W,_,W,W,W,W,W,W],
    [W,_,_,_,_,_,W,S,S,S,S,S,W,_,_,_,_,_,_,W],
    [W,W,W,_,W,W,W,W,W,W,W,W,W,W,W,_,W,W,_,W],
    [W,B,_,_,_,_,_,_,_,_,_,_,_,_,_,_,W,_,_,W],
    [W,W,W,W,W,W,_,W,W,W,I,I,_,W,W,W,W,_,D,W],
    [W,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,X,W],
    [W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W]
  ]
},

/* ======================================================
   LEVEL 4 — "Rò rỉ gas" (20x15)
   Objectives: Ngắt điện, BCC, Chìa khóa, Khăn ướt, Khóa gas, Gọi 114
   Gas leak near fire = deadly combo
   ====================================================== */
{
  nameVi: 'Rò rỉ gas',
  time: 120,
  fireSpread: 6,
  tip: 'Khóa van gas TRƯỚC khi dập lửa gần khu gas!',
  desc: 'Gas rò rỉ! Phải khóa gas trước rồi mới dập lửa an toàn.',
  mapW: 20, mapH: 15,
  objectives: [
    { type: 'breaker', label: 'Ngắt cầu dao điện' },
    { type: 'collect_bcc', label: 'Thu bình chữa cháy' },
    { type: 'collect_key', label: 'Tìm chìa khóa' },
    { type: 'collect_twl', label: 'Thu khăn ướt' },
    { type: 'gas_off', label: 'Khóa van gas' },
    { type: 'call_114', label: 'Gọi 114' }
  ],
  map: [
    [W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W],
    [W,P,_,_,_,W,_,_,_,_,W,_,_,_,_,_,_,_,_,W],
    [W,_,W,W,_,W,_,W,W,_,W,_,W,W,W,W,_,W,_,W],
    [W,_,W,GV,_,_,_,W,_,_,_,_,W,_,PH,_,_,W,_,W],
    [W,_,W,W,W,W,_,W,_,W,W,W,W,_,W,W,W,W,_,W],
    [W,_,_,_,GL,GL,_,_,_,_,_,_,_,_,_,_,_,_,_,W],
    [W,W,W,_,GL,W,W,W,I,I,W,W,W,_,W,E,E,W,W,W],
    [W,T,_,_,_,_,_,_,_,_,_,_,W,_,W,_,_,_,_,W],
    [W,W,W,W,W,_,W,W,_,W,W,_,W,_,W,_,W,W,_,W],
    [W,_,_,_,_,_,W,K,_,_,W,_,_,_,W,_,W,BR,_,W],
    [W,_,W,W,W,_,W,W,W,_,W,W,W,W,W,_,W,W,W,W],
    [W,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,W],
    [W,W,W,_,W,W,W,W,W,S,S,S,_,W,W,W,W,_,D,W],
    [W,B,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,X,W],
    [W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W]
  ]
},

/* ======================================================
   LEVEL 5 — "Nhiệm vụ toàn diện" (20x15)
   Objectives: ALL (Ngắt điện, BCC, Key, TWL, Gas, Mask, 114)
   First level with all objectives
   ====================================================== */
{
  nameVi: 'Nhiệm vụ toàn diện',
  time: 120,
  fireSpread: 5,
  tip: 'Cần tất cả kỹ năng! Hãy lên kế hoạch trước khi hành động.',
  desc: 'Cần thực hiện TẤT CẢ nhiệm vụ để thoát. Lên kế hoạch!',
  mapW: 20, mapH: 15,
  objectives: [
    { type: 'breaker', label: 'Ngắt cầu dao điện' },
    { type: 'collect_bcc', label: 'Thu bình chữa cháy' },
    { type: 'collect_key', label: 'Tìm chìa khóa' },
    { type: 'collect_twl', label: 'Thu khăn ướt' },
    { type: 'gas_off', label: 'Khóa van gas' },
    { type: 'collect_mask', label: 'Thu mặt nạ phòng độc' },
    { type: 'call_114', label: 'Gọi 114' }
  ],
  map: [
    [W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W],
    [W,P,_,_,W,_,_,_,_,_,W,_,_,_,_,W,_,_,_,W],
    [W,_,W,_,W,_,W,W,W,_,W,_,W,W,_,W,_,W,_,W],
    [W,_,W,_,_,_,W,GV,_,_,_,_,W,T,_,_,_,W,_,W],
    [W,_,W,W,W,_,W,W,W,W,W,W,W,W,_,W,W,W,_,W],
    [W,_,_,_,_,_,GL,GL,_,_,_,_,_,_,_,_,_,_,_,W],
    [W,W,W,_,W,W,W,W,_,W,W,E,E,W,W,W,W,_,W,W],
    [W,BR,_,_,_,_,_,_,_,W,_,_,_,_,_,W,M,_,_,W],
    [W,W,W,W,W,_,W,W,_,W,_,W,W,W,_,W,W,W,_,W],
    [W,_,_,_,W,_,W,B,_,_,_,W,_,PH,_,_,_,_,_,W],
    [W,_,W,_,W,_,W,W,W,W,_,W,_,W,W,W,W,W,W,W],
    [W,_,W,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,W],
    [W,_,W,W,W,_,W,W,I,I,_,W,S,S,S,W,W,_,D,W],
    [W,_,_,K,_,_,_,_,_,_,_,_,_,_,_,_,_,_,X,W],
    [W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W]
  ]
},

/* ======================================================
   LEVEL 6 — "Mê cung lửa" (20x15)
   Objectives: ALL - Different layout, more fire
   ====================================================== */
{
  nameVi: 'Mê cung lửa',
  time: 110,
  fireSpread: 5,
  tip: 'Lửa từ nhiều nguồn! Quản lý bình CC cẩn thận.',
  desc: 'Mê cung phức tạp với lửa khắp nơi. Cần tất cả kỹ năng!',
  mapW: 20, mapH: 15,
  objectives: [
    { type: 'breaker', label: 'Ngắt cầu dao điện' },
    { type: 'collect_bcc', label: 'Thu bình chữa cháy' },
    { type: 'collect_key', label: 'Tìm chìa khóa' },
    { type: 'collect_twl', label: 'Thu khăn ướt' },
    { type: 'gas_off', label: 'Khóa van gas' },
    { type: 'collect_mask', label: 'Thu mặt nạ phòng độc' },
    { type: 'call_114', label: 'Gọi 114' }
  ],
  map: [
    [W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W],
    [W,P,_,_,_,_,_,W,_,_,_,_,W,_,_,_,_,_,_,W],
    [W,W,W,_,W,W,_,W,_,W,W,_,W,_,W,W,W,W,_,W],
    [W,M,_,_,W,BR,_,_,_,W,_,_,_,_,_,GV,_,W,_,W],
    [W,W,W,W,W,W,_,W,W,W,_,W,W,W,W,W,_,W,_,W],
    [W,_,_,_,_,_,_,_,_,_,_,GL,GL,_,_,_,_,_,_,W],
    [W,_,W,W,W,_,W,I,I,I,W,W,W,W,_,W,E,E,W,W],
    [W,_,_,_,W,_,_,_,_,_,_,_,_,W,_,W,_,_,_,W],
    [W,W,W,_,W,_,W,W,_,W,W,W,_,W,_,W,_,W,_,W],
    [W,PH,_,_,_,_,W,K,_,_,_,W,_,_,_,_,_,W,_,W],
    [W,W,W,_,W,W,W,W,W,W,_,W,W,_,W,W,W,W,_,W],
    [W,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,W],
    [W,_,W,W,S,S,S,_,W,W,W,I,I,_,W,W,W,_,D,W],
    [W,T,_,_,_,_,_,_,_,B,_,_,_,_,_,_,_,_,X,W],
    [W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W]
  ]
},

/* ======================================================
   LEVEL 7 — "Tòa nhà văn phòng" (20x15)
   Objectives: ALL - Office layout with corridors
   ====================================================== */
{
  nameVi: 'Tòa nhà văn phòng',
  time: 110,
  fireSpread: 4,
  tip: 'Văn phòng rộng! Lên kế hoạch thu thập vật phẩm theo thứ tự.',
  desc: 'Tòa nhà văn phòng phức tạp. Cần hoàn thành mọi nhiệm vụ!',
  mapW: 20, mapH: 15,
  objectives: [
    { type: 'breaker', label: 'Ngắt cầu dao điện' },
    { type: 'collect_bcc', label: 'Thu bình chữa cháy' },
    { type: 'collect_key', label: 'Tìm chìa khóa' },
    { type: 'collect_twl', label: 'Thu khăn ướt' },
    { type: 'gas_off', label: 'Khóa van gas' },
    { type: 'collect_mask', label: 'Thu mặt nạ phòng độc' },
    { type: 'call_114', label: 'Gọi 114' }
  ],
  map: [
    [W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W],
    [W,_,_,_,W,_,_,_,W,_,_,_,W,_,_,_,W,_,P,W],
    [W,_,W,_,W,_,W,_,W,_,W,_,_,_,W,_,W,_,_,W],
    [W,_,W,_,_,_,W,_,_,_,W,_,W,W,W,_,_,_,W,W],
    [W,B,W,W,W,_,W,W,W,_,W,_,W,T,_,_,W,W,_,W],
    [W,_,_,_,_,_,_,_,_,_,_,_,W,W,W,_,_,_,_,W],
    [W,W,W,_,W,E,E,E,W,W,W,_,_,_,_,_,W,W,_,W],
    [W,_,_,_,W,_,_,_,_,_,W,W,W,W,W,_,W,GV,_,W],
    [W,_,W,W,W,_,W,W,W,_,_,_,_,_,_,_,W,W,_,W],
    [W,_,_,PH,_,_,W,K,_,_,W,W,W,W,W,_,GL,GL,_,W],
    [W,W,W,W,W,_,W,W,W,_,W,_,_,BR,_,_,W,W,_,W],
    [W,M,_,_,_,_,_,_,_,_,_,_,W,W,W,_,_,_,_,W],
    [W,W,W,_,W,S,S,S,_,W,I,I,_,W,_,W,W,_,D,W],
    [W,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,X,W],
    [W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W]
  ]
},

/* ======================================================
   LEVEL 8 — "Nhà kho" (20x15)
   Objectives: ALL - Warehouse with tight corridors
   ====================================================== */
{
  nameVi: 'Nhà kho',
  time: 100,
  fireSpread: 4,
  tip: 'Nhà kho chật chội! Cẩn thận khi di chuyển qua hành lang hẹp.',
  desc: 'Nhà kho đầy đồ vật. Lối đi chật, lửa rất nguy hiểm!',
  mapW: 20, mapH: 15,
  objectives: [
    { type: 'breaker', label: 'Ngắt cầu dao điện' },
    { type: 'collect_bcc', label: 'Thu bình chữa cháy' },
    { type: 'collect_key', label: 'Tìm chìa khóa' },
    { type: 'collect_twl', label: 'Thu khăn ướt' },
    { type: 'gas_off', label: 'Khóa van gas' },
    { type: 'collect_mask', label: 'Thu mặt nạ phòng độc' },
    { type: 'call_114', label: 'Gọi 114' }
  ],
  map: [
    [W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W],
    [W,P,_,_,W,_,_,_,W,_,_,_,W,_,_,_,_,_,_,W],
    [W,_,W,_,R,_,W,_,R,_,W,_,R,_,W,W,W,W,_,W],
    [W,_,W,_,W,_,W,_,W,_,W,_,W,_,W,GV,_,_,_,W],
    [W,_,_,_,W,_,_,_,W,_,_,_,W,_,W,W,GL,GL,_,W],
    [W,W,W,_,W,W,W,_,W,W,W,_,_,_,_,_,_,_,_,W],
    [W,T,_,_,_,_,_,_,_,_,_,_,W,I,I,W,E,E,W,W],
    [W,W,W,W,W,W,W,_,W,W,W,_,W,_,_,W,_,_,_,W],
    [W,_,_,_,_,_,W,_,_,_,W,_,W,_,W,W,_,W,_,W],
    [W,_,W,W,W,_,W,W,W,_,W,_,_,_,_,PH,_,W,_,W],
    [W,_,_,BR,_,_,_,_,_,_,W,W,W,W,_,W,W,W,_,W],
    [W,W,W,W,W,_,W,W,W,_,_,_,_,_,_,_,_,_,_,W],
    [W,B,_,_,_,_,W,K,_,_,W,S,S,S,_,W,W,_,D,W],
    [W,W,W,M,_,_,_,_,_,_,_,_,_,_,_,_,_,_,X,W],
    [W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W]
  ]
},

/* ======================================================
   LEVEL 9 — "Tầng hầm" (20x15)
   Objectives: ALL - Harder, faster fire. Basement setting.
   ====================================================== */
{
  nameVi: 'Tầng hầm',
  time: 90,
  fireSpread: 3,
  tip: 'Lửa lan nhanh trong tầng hầm! Mỗi giây đều quan trọng!',
  desc: 'Tầng hầm tối tăm. Lửa lan nhanh, thời gian hạn chế!',
  mapW: 20, mapH: 15,
  objectives: [
    { type: 'breaker', label: 'Ngắt cầu dao điện' },
    { type: 'collect_bcc', label: 'Thu bình chữa cháy' },
    { type: 'collect_key', label: 'Tìm chìa khóa' },
    { type: 'collect_twl', label: 'Thu khăn ướt' },
    { type: 'gas_off', label: 'Khóa van gas' },
    { type: 'collect_mask', label: 'Thu mặt nạ phòng độc' },
    { type: 'call_114', label: 'Gọi 114' }
  ],
  map: [
    [W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W],
    [W,P,_,_,_,_,W,_,_,_,W,_,_,_,_,W,_,_,_,W],
    [W,W,W,_,W,_,W,_,W,_,W,_,W,W,_,W,_,W,_,W],
    [W,_,_,_,W,_,_,_,W,_,_,_,_,W,_,_,_,W,_,W],
    [W,_,W,W,W,W,W,_,W,W,W,W,_,W,W,W,_,W,_,W],
    [W,_,_,BR,_,_,_,_,_,I,I,_,_,_,_,_,_,_,_,W],
    [W,W,W,W,_,W,W,W,W,W,W,W,W,W,_,W,W,W,W,W],
    [W,GV,_,_,_,W,_,_,_,_,_,_,_,W,_,_,_,_,_,W],
    [W,W,GL,GL,_,W,_,W,_,W,W,W,_,W,_,W,W,W,_,W],
    [W,M,_,_,_,_,_,W,K,_,B,W,_,_,_,W,PH,_,_,W],
    [W,W,W,W,W,W,_,W,W,W,W,W,W,W,_,W,W,W,_,W],
    [W,T,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,W],
    [W,W,W,E,E,_,W,W,W,S,S,S,_,W,I,I,W,_,D,W],
    [W,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,X,W],
    [W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W]
  ]
},

/* ======================================================
   LEVEL 10 — "Thử thách cuối cùng" (20x15)
   Objectives: ALL - Hardest. Very fast fire, tight time.
   ====================================================== */
{
  nameVi: 'Thử thách cuối cùng',
  time: 80,
  fireSpread: 3,
  tip: 'Đây là thử thách cuối! Áp dụng MỌI kỹ năng bạn đã học!',
  desc: 'Thử thách cuối! Lửa lan cực nhanh, mọi kỹ năng đều cần!',
  mapW: 20, mapH: 15,
  objectives: [
    { type: 'breaker', label: 'Ngắt cầu dao điện' },
    { type: 'collect_bcc', label: 'Thu bình chữa cháy' },
    { type: 'collect_key', label: 'Tìm chìa khóa' },
    { type: 'collect_twl', label: 'Thu khăn ướt' },
    { type: 'gas_off', label: 'Khóa van gas' },
    { type: 'collect_mask', label: 'Thu mặt nạ phòng độc' },
    { type: 'call_114', label: 'Gọi 114' }
  ],
  map: [
    [W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W],
    [W,P,_,_,W,_,_,_,W,_,_,_,W,_,_,_,_,_,_,W],
    [W,_,W,_,W,_,W,_,_,_,W,_,_,_,W,W,W,W,_,W],
    [W,_,W,_,_,_,W,BR,_,_,W,_,W,_,W,GV,_,_,_,W],
    [W,_,W,W,W,_,W,W,W,_,W,_,W,_,W,W,GL,GL,_,W],
    [W,_,_,_,_,_,_,_,_,_,_,_,W,_,_,_,_,_,_,W],
    [W,W,W,I,I,W,W,W,W,_,W,W,W,W,_,W,E,E,W,W],
    [W,T,_,_,_,_,W,_,_,_,_,_,_,W,_,W,_,_,_,W],
    [W,W,W,W,W,_,W,_,W,W,W,W,_,_,_,W,_,W,_,W],
    [W,_,_,_,_,_,_,_,W,K,_,W,_,W,W,W,_,W,_,W],
    [W,_,W,W,W,W,W,_,W,W,_,_,_,_,PH,_,_,W,_,W],
    [W,_,_,_,_,_,_,_,_,_,_,W,W,W,W,W,_,_,_,W],
    [W,W,W,M,_,W,S,S,S,_,W,W,I,I,_,W,W,_,D,W],
    [W,B,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,X,W],
    [W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W]
  ]
}

]; // end GAME_LEVELS
