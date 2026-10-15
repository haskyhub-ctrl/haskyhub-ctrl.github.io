"""
Update question and option texts in existing database from seed_data.py and seed_data_specific.py
Safe for existing production data (preserves question IDs and foreign keys).
"""
import sys
import os

# Add backend directory to sys.path
backend_dir = os.path.dirname(os.path.abspath(__file__))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from database import SessionLocal
from models import Question, QuestionOption, QuestionCategory
from seed_data import ALL_COMMON_QUESTIONS, COMMON_CATEGORIES
from seed_data_specific import ALL_SPECIFIC_CATEGORIES

def update_questions():
    db = SessionLocal()
    updated_q = 0
    updated_opt = 0
    try:
        # 1. Update Common Questions (facility_type == "all")
        for cat_idx, questions in ALL_COMMON_QUESTIONS:
            cat_meta = COMMON_CATEGORIES[cat_idx]
            cat = db.query(QuestionCategory).filter(QuestionCategory.name == cat_meta["name"]).first()
            if not cat:
                continue
            db_questions = db.query(Question).filter(Question.category_id == cat.id).order_by(Question.order_index, Question.id).all()
            
            for idx, q_data in enumerate(questions):
                if idx < len(db_questions):
                    db_q = db_questions[idx]
                    if db_q.question_text != q_data["text"]:
                        db_q.question_text = q_data["text"]
                        updated_q += 1
                    
                    db_options = db.query(QuestionOption).filter(QuestionOption.question_id == db_q.id).order_by(QuestionOption.order_index, QuestionOption.id).all()
                    for opt_idx, opt_data in enumerate(q_data["options"]):
                        if opt_idx < len(db_options):
                            db_opt = db_options[opt_idx]
                            if db_opt.option_text != opt_data["text"]:
                                db_opt.option_text = opt_data["text"]
                                updated_opt += 1

        # 2. Update Specific Questions
        for spec_cat_data in ALL_SPECIFIC_CATEGORIES:
            ft = spec_cat_data["facility_type"]
            cat = db.query(QuestionCategory).filter(QuestionCategory.name == spec_cat_data["name"]).first()
            if not cat:
                continue
            db_questions = db.query(Question).filter(Question.category_id == cat.id).order_by(Question.order_index, Question.id).all()
            for idx, q_data in enumerate(spec_cat_data["questions"]):
                if idx < len(db_questions):
                    db_q = db_questions[idx]
                    if db_q.question_text != q_data["text"]:
                        db_q.question_text = q_data["text"]
                        updated_q += 1
                    
                    db_options = db.query(QuestionOption).filter(QuestionOption.question_id == db_q.id).order_by(QuestionOption.order_index, QuestionOption.id).all()
                    for opt_idx, opt_data in enumerate(q_data["options"]):
                        if opt_idx < len(db_options):
                            db_opt = db_options[opt_idx]
                            if db_opt.option_text != opt_data["text"]:
                                db_opt.option_text = opt_data["text"]
                                updated_opt += 1

        db.commit()
        print(f"Successfully updated {updated_q} questions and {updated_opt} options in database.")
    except Exception as e:
        db.rollback()
        print(f"Error updating questions: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    update_questions()
