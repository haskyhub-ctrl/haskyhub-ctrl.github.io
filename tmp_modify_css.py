import re

def update_css(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update .game-container for glassmorphism
    old_game_container = """.game-container {
    max-width: 900px;
    margin: 0 auto;
    padding: 20px;
}"""
    new_game_container = """.game-container {
    max-width: 900px;
    margin: 20px auto;
    padding: 24px;
    background: rgba(26, 26, 46, 0.4);
    border-radius: 24px;
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid rgba(255, 255, 255, 0.08);
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.6);
}"""
    content = content.replace(old_game_container, new_game_container)

    # 2. Add border-radius for .game-card
    old_game_card = """.game-card {
    display: flex;
    flex-direction: column;
    background: #fff;
    border-radius: 0;"""
    new_game_card = """.game-card {
    display: flex;
    flex-direction: column;
    background: #fff;
    border-radius: 16px;"""
    content = content.replace(old_game_card, new_game_card)

    def change_radius(selector, old_val, new_val):
        nonlocal content
        pattern = re.compile(re.escape(selector) + r"(\s*{[^}]+?)border-radius:\s*" + re.escape(old_val) + r";", re.DOTALL)
        content = pattern.sub(selector + r"\1border-radius: " + new_val + ";", content)

    # Convert border-radius: 0 to nice values for UI elements
    change_radius(".game-card-badge", "0", "12px")
    change_radius(".game-card-difficulty", "0", "6px")
    change_radius(".game-skill-tag", "0", "6px")
    change_radius(".game-header", "0", "16px")
    change_radius(".hud-item", "0", "8px")
    change_radius(".hud-action-btn", "0", "8px")
    change_radius(".game-inventory", "0", "16px")
    change_radius(".inventory-slot", "0", "10px")
    change_radius(".game-canvas-wrapper", "0", "16px")
    change_radius(".game-instructions", "0", "16px")
    change_radius(".instruction-item", "0", "12px")
    change_radius(".game-level-info", "0", "12px")
    change_radius(".game-message-tip", "0", "12px")
    change_radius(".game-btn", "0", "24px") # Rounded pill button

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

update_css(r"c:\Users\Hasky\.gemini\antigravity\scratch\fras\frontend\css\games.css")
