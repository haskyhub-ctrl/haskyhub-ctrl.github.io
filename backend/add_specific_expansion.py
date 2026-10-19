"""Nạp bộ câu hỏi đặc thù bổ sung (seed_data_specific_extra*.py) vào CSDL đang chạy.

Chạy tự động mỗi lần khởi động backend (xem main.py). An toàn khi chạy nhiều lần:
câu hỏi đã có (trùng nội dung) sẽ được bỏ qua, nên không làm mất dữ liệu khảo sát cũ.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import SessionLocal
from models import Question, QuestionOption, QuestionCategory
from seed_data_specific import ALL_SPECIFIC_CATEGORIES
from seed_recommendations import generate_recommendations_for_option


def _load_extra():
    from seed_data_specific_extra import EXTRA as e1
    from seed_data_specific_extra2 import EXTRA as e2
    from seed_data_specific_extra3 import EXTRA as e3
    merged = {}
    for part in (e1, e2, e3):
        for letter, questions in part.items():
            merged.setdefault(letter, []).extend(questions)
    return merged


def add_specific_expansion():
    extra = _load_extra()
    name_by_letter = {c["facility_type"]: c["name"] for c in ALL_SPECIFIC_CATEGORIES}

    db = SessionLocal()
    added_q = 0
    try:
        for letter, questions in extra.items():
            cat = db.query(QuestionCategory).filter(QuestionCategory.name == name_by_letter.get(letter)).first()
            if not cat:
                print(f"[expansion] Chưa có nhóm đặc thù {letter}, bỏ qua")
                continue

            order = db.query(Question).filter(Question.category_id == cat.id).count()
            for q_data in questions:
                if db.query(Question).filter(Question.question_text == q_data["text"]).first():
                    continue
                order += 1
                q = Question(
                    category_id=cat.id,
                    question_text=q_data["text"],
                    question_type="single",
                    facility_type=letter,
                    help_text=q_data.get("help"),
                    reference=q_data.get("reference"),
                    order_index=order,
                    is_active=True,
                )
                db.add(q)
                db.flush()
                for i, opt in enumerate(q_data["options"]):
                    db_opt = QuestionOption(
                        question_id=q.id,
                        option_key=opt["key"],
                        option_text=opt["text"],
                        score=opt["score"],
                        risk_level=opt["risk"],
                        order_index=i + 1,
                    )
                    db.add(db_opt)
                    db.flush()
                    if opt["score"] >= 2:
                        generate_recommendations_for_option(db, db_opt, opt, cat.name)
                cat.max_score = (cat.max_score or 0) + 3
                added_q += 1
        db.commit()
        print(f"[expansion] Đã thêm {added_q} câu hỏi đặc thù mới")
    except Exception as e:
        db.rollback()
        print(f"[expansion] Lỗi: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    add_specific_expansion()
