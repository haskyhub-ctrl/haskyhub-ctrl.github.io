"""Chạy trên máy chủ: biên soạn trang wiki (nháp) và/hoặc chạy một lượt tìm văn bản mới.

Dùng:  python run_wiki.py                 biên soạn các chủ đề wiki còn thiếu
       python run_wiki.py nghiem-thu ...   biên soạn (lại) các chủ đề chỉ định
       python run_wiki.py --watch          chạy một lượt tìm văn bản mới
Trang wiki luôn ở dạng nháp, chưa dùng để trả lời cho đến khi cán bộ bật ở trang Kho tài liệu AI.
"""
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from dotenv import load_dotenv

load_dotenv(os.path.join(HERE, ".env"), override=True)

from database import SessionLocal  # noqa: E402
from utils import kho_seed, wiki  # noqa: E402


def main():
    args = [a for a in sys.argv[1:] if a]
    kho_seed.sync_seed()
    if "--watch" in args:
        from database import Base, engine
        Base.metadata.create_all(bind=engine)
        from utils import law_watch
        db = SessionLocal()
        try:
            print("Kết quả theo dõi:", law_watch.run(db))
        finally:
            db.close()
        args = [a for a in args if a != "--watch"]
        if not args:
            return
    slugs = [a for a in args if a in wiki.TOPIC_BY_SLUG] or [t["slug"] for t in wiki.status() if t["state"] == "none"]
    print(f"Biên soạn {len(slugs)} trang wiki...")
    ok = 0
    for sl in slugs:
        t = time.time()
        try:
            res = wiki.generate(sl)
            ok += 1
            print(f"  OK  {sl}: {res['chars']} ký tự ({time.time() - t:.0f}s)", flush=True)
        except Exception as e:
            print(f"  LỖI {sl}: {str(e)[:160]}", flush=True)
    print(f"Xong: {ok}/{len(slugs)} trang (đang ở dạng nháp).")


if __name__ == "__main__":
    main()
