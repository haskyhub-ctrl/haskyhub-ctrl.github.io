import json, os, shutil, subprocess, sys
from playwright.sync_api import sync_playwright
HERE=os.path.dirname(os.path.abspath(__file__))
FPS=int(os.environ.get("FPS","25")); W,H=1920,1080
tl=json.load(open(os.path.join(HERE,"timeline.json"),encoding="utf-8"))
html=open(os.path.join(HERE,"video.html"),encoding="utf-8").read().replace("/*TIMELINE*/", json.dumps(tl,ensure_ascii=False))
os.makedirs(os.path.join(HERE,"assets"),exist_ok=True)
open(os.path.join(HERE,"build.html"),"w",encoding="utf-8").write(html)
only=os.environ.get("ONLY")           # ví dụ ONLY=12.5,40 chỉ chụp vài khung để xem thử
out=os.path.join(HERE,"frames"); os.makedirs(out,exist_ok=True)
with sync_playwright() as p:
    br=p.chromium.launch(channel="msedge",headless=True)
    pg=br.new_page(viewport={"width":W,"height":H})
    pg.goto("file:///"+os.path.join(HERE,"build.html").replace("\\","/")); pg.wait_for_timeout(1500)
    if only:
        for t in [float(x) for x in only.split(",")]:
            pg.evaluate(f"seek({t})"); pg.wait_for_timeout(150)
            pg.screenshot(path=os.path.join(HERE,f"test_{t:06.2f}.png"))
        print("ok test"); br.close(); sys.exit(0)
    total=int(tl["duration"]*FPS)+1
    ff=subprocess.Popen(["ffmpeg","-y","-loglevel","error","-f","image2pipe","-framerate",str(FPS),"-c:v","mjpeg","-i","-",
        "-i",os.path.join(HERE,"giongdoc.mp3"),"-c:v","libx264","-preset","medium","-crf","18","-pix_fmt","yuv420p","-r",str(FPS),
        "-c:a","aac","-b:a","192k","-shortest","-movflags","+faststart",os.path.join(HERE,"FRAS-AI_gioi_thieu.mp4")],stdin=subprocess.PIPE)
    for i in range(total):
        pg.evaluate(f"seek({i/FPS})")
        ff.stdin.write(pg.screenshot(type="jpeg",quality=92))
        if i%250==0: print(i,"/",total,flush=True)
    ff.stdin.close(); ff.wait(); br.close()
print("xong")
