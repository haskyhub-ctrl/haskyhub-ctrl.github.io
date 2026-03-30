from database import SessionLocal
from models import QuestionCategory, Question, QuestionOption, Recommendation

db = SessionLocal()
try:
    print("Xóa dữ liệu cũ...")
    db.query(Recommendation).delete()
    db.query(QuestionOption).delete()
    db.query(Question).delete()
    db.query(QuestionCategory).delete()
    db.commit()
    print("Đã xóa dữ liệu cũ. Khởi động lại server sẽ tự động nạp (seed) lại câu hỏi mới.")
except Exception as e:
    db.rollback()
    print("Lỗi:", e)
finally:
    db.close()
