import os
import json
from database import SessionLocal
from models import Question, QuestionCategory

def extract_for_analysis():
    db = SessionLocal()
    questions = db.query(Question).order_by(Question.category_id, Question.id).all()
    
    output_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'cau_hoi_analysis.json')
    
    data = []
    for q in questions:
        category_name = q.category.name if q.category else 'Khác'
        data.append({
            "id": q.id,
            "category": category_name,
            "text": q.question_text
        })
        
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
            
    db.close()
    print(f"Exported {len(data)} questions to {output_path}")

if __name__ == '__main__':
    extract_for_analysis()
