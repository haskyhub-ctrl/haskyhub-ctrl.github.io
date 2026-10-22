window.__timelines = window.__timelines || {};
const tl = gsap.timeline({ paused: true });

tl.fromTo('#progress', { width: '0%' }, { width: '100%', duration: TOTAL, ease: 'none' }, 0);

document.querySelectorAll('.scene').forEach((sc, i) => {
  const a = T[i][0], b = T[i][1];
  const nxt = i < T.length - 1 ? T[i + 1][0] : TOTAL;
  const span = b - a;
  tl.fromTo(sc, { opacity: 0 }, { opacity: 1, duration: 0.5, ease: 'power1.out' }, a);
  if (i < T.length - 1) tl.to(sc, { opacity: 0, duration: 0.45, ease: 'power1.in' }, nxt - 0.5);

  // các phần tử hiện lần lượt, rải đều trong nửa đầu cảnh (hoặc theo mốc "late", "later")
  const els = [...sc.querySelectorAll('[data-a]')].filter(e => !e.dataset.a || e.dataset.a === '' || e.dataset.a === 'fade');
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

  // điện thoại trượt vào, đổi ảnh dần theo thời gian của cảnh
  sc.querySelectorAll('.phone').forEach(ph => {
    tl.fromTo(ph, { x: 140, opacity: 0 }, { x: 0, opacity: 1, duration: 0.9, ease: 'power3.out' }, a + 0.2);
    const shots = [...ph.querySelectorAll('.shot')];
    shots.forEach((im, j) => {
      if (j === 0) return;
      const at = a + (span + 1.5) * j / shots.length;
      tl.to(shots[j - 1], { opacity: 0, duration: 0.5 }, at);
      tl.to(im, { opacity: 1, duration: 0.5 }, at);
    });
  });
});

// cảnh 1: khói bốc lên
document.querySelectorAll('#s1 .smoke').forEach((s, k) => {
  tl.fromTo(s, { y: 0, opacity: 0, scale: 0.6 }, { y: -170, opacity: 0.85, scale: 1.8, duration: 3.2, ease: 'power1.out', repeat: 2 }, 0.8 + k * 0.7);
});
tl.fromTo('#s1 .win', { opacity: 0.4 }, { opacity: 1, duration: 1.2, repeat: 4, yoyo: true }, 0.5);
// cảnh 8: vòng xoay rồi dấu tích
tl.fromTo('#s8 .spin', { rotation: 0 }, { rotation: 720, duration: 2.6, ease: 'none' }, T[7][0] + (T[7][1] - T[7][0]) * 0.4);
// cảnh 11: thanh nguy cơ giảm dần khi tích việc đã làm
tl.fromTo('#s11 .fill', { width: '92%' }, { width: '28%', duration: 4, ease: 'power2.inOut' }, T[10][0] + 3.2);

// phụ đề
document.querySelectorAll('.cap').forEach(c => {
  const s = parseFloat(c.dataset.start), d = parseFloat(c.dataset.duration);
  tl.fromTo(c, { opacity: 0, y: 10 }, { opacity: 1, y: 0, duration: 0.22 }, s);
  tl.to(c, { opacity: 0, duration: 0.15 }, s + d - 0.15);
});

window.__timelines['main'] = tl;
tl.seek(0);
