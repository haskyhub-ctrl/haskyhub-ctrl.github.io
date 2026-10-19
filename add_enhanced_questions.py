import os
import sys

# Ensure backend imports work
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from database import SessionLocal
from models import Question, QuestionOption, QuestionCategory, Recommendation

from enhanced_questions_soft import NEW_QUESTIONS_DATA  # bản làm mềm; câu cũ được cập nhật bởi soften_legacy_questions.py

def add_enhanced_questions():
    db = SessionLocal()
    added_questions = 0
    added_options = 0
    added_recs = 0

    try:
        for q_data in NEW_QUESTIONS_DATA:
            # Check if question already exists to prevent duplication
            existing_q = db.query(Question).filter(
                Question.question_text == q_data["question_text"]
            ).first()

            if existing_q:
                print(f"Skipping existing: {q_data['question_text'][:50]}...")
                continue

            # Determine order_index in category
            max_order = db.query(Question).filter(
                Question.category_id == q_data["category_id"]
            ).count()

            new_q = Question(
                category_id=q_data["category_id"],
                question_text=q_data["question_text"],
                question_type="single",
                facility_type=q_data["facility_type"],
                help_text=q_data.get("help_text"),
                reference=q_data.get("reference"),
                order_index=max_order + 1,
                is_active=True
            )
            db.add(new_q)
            db.flush()
            added_questions += 1

            for idx, opt_data in enumerate(q_data["options"]):
                new_opt = QuestionOption(
                    question_id=new_q.id,
                    option_key=opt_data["key"],
                    option_text=opt_data["text"],
                    score=opt_data["score"],
                    risk_level=opt_data["risk"],
                    order_index=idx + 1
                )
                db.add(new_opt)
                db.flush()
                added_options += 1

                # If recommendation exists for risky option
                if "rec" in opt_data:
                    priority = "urgent" if opt_data["score"] == 3 else "high"
                    deadline_days = 2 if opt_data["score"] == 3 else 30
                    new_rec = Recommendation(
                        question_option_id=new_opt.id,
                        recommendation_text=opt_data["rec"],
                        priority=priority,
                        deadline_days=deadline_days,
                        legal_reference=opt_data.get("legal"),
                        is_active=True
                    )
                    db.add(new_rec)
                    added_recs += 1

        db.commit()
        print(f"SUCCESS: Added {added_questions} questions, {added_options} options, {added_recs} recommendations!")

    except Exception as e:
        db.rollback()
        print(f"ERROR: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    add_enhanced_questions()
