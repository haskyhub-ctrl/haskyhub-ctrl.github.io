import sys
import os
import csv
from database import SessionLocal
from models import Question, QuestionOption, Recommendation, QuestionCategory

def export_to_csv():
    db = SessionLocal()
    questions = db.query(Question).order_by(Question.category_id, Question.id).all()
    
    output_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'danh_sach_210_cau_hoi.csv')
    
    with open(output_path, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            'TT', 'Lĩnh vực', 'Câu hỏi', 'Loại', 'Các đáp án lựa chọn (Điểm - Rủi ro)', 'Các khuyến nghị xử lý'
        ])
        
        count = 1
        for q in questions:
            category_name = q.category.name if q.category else 'Khác'
            options_text = []
            recommendations_text = []
            
            for opt in q.options:
                opt_str = f"{opt.option_key}) {opt.option_text} [Điểm: {opt.score}, Rủi ro: {opt.risk_level}]"
                options_text.append(opt_str)
                
                for rec in opt.recommendations:
                    rec_str = f"- Nếu chọn ({opt.option_key}): {rec.recommendation_text}"
                    recommendations_text.append(rec_str)
            
            writer.writerow([
                count,
                category_name,
                q.question_text,
                q.question_type,
                "\n".join(options_text),
                "\n".join(recommendations_text)
            ])
            count += 1
            
    db.close()
    print(f"Da xuat {count-1} cau hoi ra file: {output_path}")

if __name__ == '__main__':
    export_to_csv()
