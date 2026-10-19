"""Cập nhật các câu hỏi cũ trong CSDL đang chạy sang bản đã làm mềm.

Chạy mỗi lần khởi động backend (xem main.py), TRƯỚC add_enhanced_questions. Câu nào còn nội dung cũ
sẽ được đổi sang nội dung mới (câu hỏi, đáp án, gợi ý, khuyến nghị); câu đã đổi rồi thì bỏ qua.
Không xóa câu hỏi hay câu trả lời nào, nên dữ liệu khảo sát đã có vẫn nguyên vẹn.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import SessionLocal
from models import Question, Recommendation
from seed_data_specific import LEGACY_QUESTIONS
from seed_recommendations import generate_recommendations_for_option
from enhanced_questions_soft import NEW_QUESTIONS_DATA

# Nội dung cũ của 11 câu nâng cao, đúng thứ tự với NEW_QUESTIONS_DATA
LEGACY_ENHANCED_TEXTS = [
    "Khoảng cách xếp đặt hàng hóa trong kho tới trần nhà, đầu phun chữa cháy tự động (sprinkler) và đèn chiếu sáng có đảm bảo tối thiểu 0,5 mét không?",
    "Quy trình kiểm tra và ngắt nguồn điện phụ tải của kho hàng sau giờ làm việc hàng ngày được thực hiện như thế nào?",
    "Lối đi thông gió, thoát nạn và khoảng cách giữa các khối pallet/kệ hàng trong kho có đảm bảo thông thoáng theo quy chuẩn không?",
    "Khu vực để xe máy, xe điện tại tầng 1 (hoặc tầng bán hầm) có được ngăn cách chống cháy, chống khói lan lên cầu thang bộ thoát nạn không?",
    "Quy định và hạ tầng sạc xe máy điện, xe đạp điện tại cơ sở/nhà trọ được bố trí như thế nào?",
    "Lối thoát nạn khẩn cấp thứ hai (qua ban công, lô gia, tầng mái hoặc chuồng cọp) có đảm bảo sẵn sàng mở ra khi có sự cố không?",
    "Vật liệu ốp cách âm, trang trí nội thất trong phòng hát, quầy bar có sử dụng vật liệu chống cháy lan (thử nghiệm theo QCVN 06:2022/BXD) không?",
    "Hệ thống điện và dàn âm thanh, ánh sáng có được liên động tự động ngắt khi hệ thống báo cháy kích hoạt không?",
    "Cửa thoát nạn của phòng dịch vụ và hành lang thoát hiểm mở ra theo chiều nào và có biển chỉ dẫn EXIT phát sáng liên tục không?",
    "Quy trình cách ly và ngắt aptomat tổng các dây chuyền sản xuất cơ khí, may mặc, chế biến gỗ sau ca làm việc được thực hiện ra sao?",
    "Khoảng cách chống cháy lan và đường giao thông cho xe chữa cháy tiếp cận giữa các nhà xưởng liền kề có đảm bảo thông thoáng không?"
]


def _regen_recs(db, option, category_name):
    db.query(Recommendation).filter(Recommendation.question_option_id == option.id).delete()
    if option.score >= 2:
        generate_recommendations_for_option(
            db, option,
            {"score": option.score, "risk": option.risk_level, "text": option.option_text},
            category_name,
        )


def soften_legacy_questions():
    db = SessionLocal()
    updated = 0
    try:
        # 1. Các câu đặc thù gốc (seed_data_specific.py)
        for items in LEGACY_QUESTIONS.values():
            for it in items:
                q = db.query(Question).filter(Question.question_text == it["old_text"]).first()
                if not q:
                    continue
                q.question_text = it["new_text"]
                by_key = {o.option_key: o for o in q.options}
                for key, text in it["options"].items():
                    opt = by_key.get(key)
                    if opt and opt.option_text != text:
                        opt.option_text = text
                        _regen_recs(db, opt, q.category.name if q.category else "")
                updated += 1

        # 2. Các câu nâng cao (add_enhanced_questions.py)
        for old_text, new in zip(LEGACY_ENHANCED_TEXTS, NEW_QUESTIONS_DATA):
            q = db.query(Question).filter(Question.question_text == old_text).first()
            if not q:
                continue
            q.question_text = new["question_text"]
            q.help_text = new.get("help_text")
            q.reference = new.get("reference")
            by_key = {o.option_key: o for o in q.options}
            for od in new["options"]:
                opt = by_key.get(od["key"])
                if not opt:
                    continue
                opt.option_text = od["text"]
                if "rec" in od:
                    rec = db.query(Recommendation).filter(Recommendation.question_option_id == opt.id).first()
                    if rec:
                        rec.recommendation_text = od["rec"]
                        rec.legal_reference = od.get("legal")
            updated += 1

        db.commit()
        print(f"[soften] Đã làm mềm {updated} câu hỏi cũ")
    except Exception as e:
        db.rollback()
        print(f"[soften] Lỗi: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    soften_legacy_questions()
