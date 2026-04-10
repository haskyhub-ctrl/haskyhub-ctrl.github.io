import json

path = r"c:\Users\Hasky\.gemini\antigravity\scratch\fras\frontend\js\game-levels.js"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

json_str = content.replace("window.GAME_LEVELS = ", "").rstrip().rstrip(";")
levels = json.loads(json_str)

for i, lv in enumerate(levels):
    lv["time"] = 60
    lv["fireSpread"] = 5
    if "smokeSpread" not in lv:
        lv["smokeSpread"] = 8

lines = ["window.GAME_LEVELS = ["]
for i, lv in enumerate(levels):
    lines.append("  {")
    lines.append("    nameVi: " + json.dumps(lv["nameVi"], ensure_ascii=False) + ",")
    lines.append("    tip: " + json.dumps(lv["tip"], ensure_ascii=False) + ",")
    lines.append("    time: " + str(lv["time"]) + ", fireSpread: " + str(lv["fireSpread"]) + ", smokeSpread: " + str(lv.get("smokeSpread", 0)) + ",")
    lines.append("    map: [")
    for j, row in enumerate(lv["map"]):
        comma = "," if j < len(lv["map"]) - 1 else ""
        lines.append("      [" + ",".join(str(x) for x in row) + "]" + comma)
    lines.append("    ]")
    comma = "," if i < len(levels) - 1 else ""
    lines.append("  }" + comma)
lines.append("];")

with open(path, "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")

print("Updated " + str(len(levels)) + " levels: time=60, fireSpread=5, smokeSpread=8")
