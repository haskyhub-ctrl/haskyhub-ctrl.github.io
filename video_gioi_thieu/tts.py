"""Tạo giọng đọc từng cảnh bằng edge-tts, đo thời lượng, sinh timeline và phụ đề (SRT)."""
import asyncio, json, os, re, subprocess, sys
import edge_tts

HERE = os.path.dirname(os.path.abspath(__file__))
AUDIO = os.path.join(HERE, "audio"); os.makedirs(AUDIO, exist_ok=True)
cfg = json.load(open(os.path.join(HERE, "script.json"), encoding="utf-8"))
GAP = 0.55          # giây lặng sau mỗi cảnh
LEAD = 0.5          # giây lặng đầu video


def duration(path):
    out = subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path])
    return float(out.decode().strip())


def chunks(text, limit=62):
    """Chia lời thoại hiển thị thành các dòng phụ đề ngắn, ngắt ở dấu câu."""
    parts = re.split(r"(?<=[,;:.])\s+", text.strip())
    out, cur = [], ""
    for p in parts:
        if cur and len(cur) + 1 + len(p) > limit:
            out.append(cur); cur = p
        else:
            cur = (cur + " " + p).strip()
    if cur:
        out.append(cur)
    return out


def ts(t):
    h, rem = divmod(t, 3600); m, s = divmod(rem, 60)
    return f"{int(h):02d}:{int(m):02d}:{int(s):02d},{int((s - int(s)) * 1000):03d}"


async def main():
    t = LEAD
    scenes, srt, n = [], [], 1
    for sc in cfg["scenes"]:
        path = os.path.join(AUDIO, sc["id"] + ".mp3")
        if "--keep" not in sys.argv or not os.path.exists(path):
            comm = edge_tts.Communicate(sc["spoken"], cfg["voice"], rate=cfg["rate"], pitch=cfg["pitch"])
            await comm.save(path)
        d = duration(path)
        cs = chunks(sc["display"])
        total = sum(len(c) for c in cs)
        cur = t
        subs = []
        for c in cs:
            seg = d * len(c) / total
            subs.append({"start": round(cur, 3), "end": round(cur + seg, 3), "text": c})
            srt.append(f"{n}\n{ts(cur)} --> {ts(cur + seg)}\n{c}\n"); n += 1
            cur += seg
        scenes.append({"id": sc["id"], "start": round(t, 3), "audio": round(d, 3), "end": round(t + d + GAP, 3), "subs": subs})
        t += d + GAP
    timeline = {"duration": round(t, 3), "lead": LEAD, "scenes": scenes}
    json.dump(timeline, open(os.path.join(HERE, "timeline.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    open(os.path.join(HERE, "phude.srt"), "w", encoding="utf-8").write("\n".join(srt))
    print("tổng thời lượng", round(t, 1), "giây;", len(scenes), "cảnh;", n - 1, "dòng phụ đề")

    # Ghép âm thanh: đổi mọi đoạn sang WAV cùng định dạng rồi nối (tránh lỗi nối mp3 với wav)
    def wav(src, dst):
        subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-ar", "44100", "-ac", "1", "-c:a", "pcm_s16le", dst])
    sil = os.path.join(AUDIO, "sil_gap.wav"); lead = os.path.join(AUDIO, "sil_lead.wav")
    for name, dur in ((sil, GAP), (lead, LEAD)):
        subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono", "-t", str(dur), "-c:a", "pcm_s16le", name])
    lst = os.path.join(AUDIO, "list.txt")
    with open(lst, "w", encoding="utf-8") as f:
        NL = chr(10)
        f.write("file '" + lead.replace(chr(92), "/") + "'" + NL)
        for sc in cfg["scenes"]:
            w = os.path.join(AUDIO, sc["id"] + ".wav"); wav(os.path.join(AUDIO, sc["id"] + ".mp3"), w)
            f.write("file '" + w.replace(chr(92), "/") + "'" + NL)
            f.write("file '" + sil.replace(chr(92), "/") + "'" + NL)
    subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst,
                           "-af", "loudnorm=I=-16:TP=-1.5:LRA=9", "-ar", "44100", "-ac", "1", "-b:a", "192k", os.path.join(HERE, "giongdoc.mp3")])
    print("đã ghép giongdoc.mp3")

asyncio.run(main())
