"""Tạo nhạc nền gốc (không dính bản quyền) cho video giới thiệu FRAS-AI.
Nhạc nền ấm, nghiêm trang, nhịp chậm: dải hợp âm kéo dài, nốt arpeggio mềm, nhịp trống nhẹ ở giữa video.
Chạy: python tao_nhac_nen.py   ->  nhac_nen.wav (stereo 44,1 kHz, dài đúng bằng giọng đọc)
"""
import numpy as np
import wave

SR = 44100
DUR = 276.1 + 3.0           # dài hơn giọng đọc một chút, để mờ dần ở cuối
N = int(SR * DUR)
t = np.arange(N) / SR
rng = np.random.default_rng(7)

BPM = 72
beat = 60 / BPM
bar = beat * 4

# Hợp âm (Hz) lặp theo vòng 4 ô nhịp: Am - F - C - G (cảm giác tin cậy, hy vọng)
CHORDS = [
    [110.00, 164.81, 220.00, 261.63, 329.63],   # Am
    [87.31, 130.81, 174.61, 261.63, 349.23],    # F
    [130.81, 196.00, 261.63, 329.63, 392.00],   # C
    [98.00, 146.83, 196.00, 246.94, 392.00],    # G
]
ARP = [
    [440.00, 523.25, 659.25, 523.25, 440.00, 329.63, 440.00, 523.25],
    [349.23, 440.00, 523.25, 440.00, 349.23, 261.63, 349.23, 440.00],
    [392.00, 523.25, 659.25, 523.25, 392.00, 329.63, 392.00, 523.25],
    [392.00, 493.88, 587.33, 493.88, 392.00, 293.66, 392.00, 493.88],
]


def pad(freqs, n):
    x = np.zeros(n)
    tt = np.arange(n) / SR
    for f in freqs:
        for det in (-0.6, 0.0, 0.6):                      # hơi lệch tần để pad dày hơn
            x += np.sin(2 * np.pi * (f + det) * tt) * 0.5
            x += np.sin(2 * np.pi * (f * 2 + det) * tt) * 0.12
    x /= len(freqs) * 3
    return x


def env(n, a, r):
    e = np.ones(n)
    na, nr = int(a * SR), int(r * SR)
    e[:na] = np.linspace(0, 1, na)
    e[-nr:] = np.linspace(1, 0, nr)
    return e


left = np.zeros(N)
right = np.zeros(N)

# ---- Lớp 1: pad hợp âm
nb = int(bar * SR)
i, k = 0, 0
while i < N:
    n = min(nb, N - i)
    seg = pad(CHORDS[k % 4], nb)[:n] * env(n, 1.6, 1.6)
    left[i:i + n] += seg * 0.55
    right[i:i + n] += seg * 0.55
    i += n
    k += 1

# ---- Lớp 2: arpeggio mềm kiểu chuông (xuất hiện từ giây 12, mềm dần về cuối)
step = beat / 2
n_note = int(step * SR * 2.2)
tt = np.arange(n_note) / SR
bell = np.exp(-tt * 3.2)
pos = int(12 * SR)
idx = 0
while pos + n_note < N:
    bar_i = int((pos / SR) // bar) % 4
    f = ARP[bar_i][idx % 8]
    note = (np.sin(2 * np.pi * f * tt) + 0.35 * np.sin(2 * np.pi * f * 2 * tt)) * bell * 0.13
    pan = 0.35 + 0.3 * ((idx % 4) / 3)
    left[pos:pos + n_note] += note * (1 - pan)
    right[pos:pos + n_note] += note * pan
    pos += int(step * SR)
    idx += 1

# ---- Lớp 3: nhịp nhẹ (bass drum mềm + tiếng nhấn) từ giây 26 đến 255, tạo cảm giác tiến lên
def kick():
    n = int(0.35 * SR)
    tt = np.arange(n) / SR
    f = 55 + 70 * np.exp(-tt * 28)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 9) * 0.55


def tick():
    n = int(0.05 * SR)
    x = rng.standard_normal(n) * np.exp(-np.arange(n) / SR * 90) * 0.05
    return x


kk = kick()
tk = tick()
b = 26.0
while b < 255.0:
    s = int(b * SR)
    left[s:s + len(kk)] += kk
    right[s:s + len(kk)] += kk
    for off in (beat / 2,):
        s2 = int((b + off) * SR)
        left[s2:s2 + len(tk)] += tk * 0.7
        right[s2:s2 + len(tk)] += tk * 1.0
    b += beat

# ---- Mở đầu dịu (giây 0 đến 11 chỉ có pad), kết thúc mờ dần
swell = np.ones(N)
swell[: int(26 * SR)] *= np.linspace(0.75, 1.0, int(26 * SR))
swell[-int(5 * SR):] *= np.linspace(1, 0, int(5 * SR))
swell[: int(2.5 * SR)] *= np.linspace(0, 1, int(2.5 * SR))
left *= swell
right *= swell

# ---- Chuẩn hóa mức (nhạc nền đủ nhỏ, về sau còn hạ nữa khi ghép với giọng)
stereo = np.stack([left, right], axis=1)
stereo /= np.max(np.abs(stereo)) / 0.85
pcm = (stereo * 32767).astype(np.int16)
with wave.open("nhac_nen.wav", "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(pcm.tobytes())
print("xong nhac_nen.wav", round(DUR, 1), "giay")
