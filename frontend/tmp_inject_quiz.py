import json, re

html_path = "game-quiz.html"
with open(html_path, "r", encoding="utf-8") as f:
    html = f.read()

with open("q100.json", "r", encoding="utf-8") as f:
    questions = f.read()

# Replace QUESTIONS array. Let's find: `const QUESTIONS = [` and the closing `];`
# Regular expression to find the QUESTIONS definition
q_pattern = r"(const QUESTIONS = \[).*?(    \];)"
replacement = f"const ALL_QUESTIONS = {questions};\n    let QUESTIONS = [];\n"

# The original code has:
# const QUESTIONS = [ ... \n    ];

new_html = re.sub(r"const QUESTIONS = \[\s*.*?\s*\];", replacement, html, flags=re.DOTALL)

# Now we need to modify the startQuiz function to pick 15 random questions each time
# function startQuiz() {
#         shuffle(QUESTIONS);
startq_pattern = r"function startQuiz\(\) {\s*shuffle\(QUESTIONS\);"
startq_repl = """function startQuiz() {
        QUESTIONS = shuffle([...ALL_QUESTIONS]).slice(0, 15);"""

new_html = new_html.replace("function startQuiz() {\n        shuffle(QUESTIONS);", startq_repl)
# Also just in case the original had spaces
new_html = re.sub(startq_pattern, startq_repl, new_html)

with open("game-quiz.html", "w", encoding="utf-8") as f:
    f.write(new_html)
print("Quiz HTML injected.")
