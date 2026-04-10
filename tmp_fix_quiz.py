import os
import re
import json

file_path = os.path.join(os.path.dirname(__file__), "frontend", "game-quiz.html")

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Extract the ALL_QUESTIONS json
match = re.search(r'const ALL_QUESTIONS = (\[.*?\]);', content, re.DOTALL)
if match:
    json_str = match.group(1)
    questions = json.loads(json_str)
    
    new_questions = []
    for q in questions:
        q_text = q['q']
        
        # If it's already in the correct format, leave it, else convert
        if 'opts' in q:
            new_questions.append(q)
            continue
            
        opts = []
        ans_idx = 0
        for i, opt in enumerate(q['options']):
            opts.append(opt['text'])
            if opt.get('isCorrect', False):
                ans_idx = i
                
        new_q = {
            "q": q_text,
            "opts": opts,
            "ans": ans_idx,
            "exp": "Căn cứ theo Luật Phòng cháy chữa cháy và Cứu nạn cứu hộ sửa đổi mới nhất."
        }
        new_questions.append(new_q)
        
    js_array_str = json.dumps(new_questions, ensure_ascii=False, indent=4)
    new_js = f"const ALL_QUESTIONS = {js_array_str};"
    content = content[:match.start()] + new_js + content[match.end():]
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Fixed format!")
else:
    print("Could not find ALL_QUESTIONS")
