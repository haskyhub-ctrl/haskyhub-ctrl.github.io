/**
 * FRAS Global AI Chatbot
 * Auto-injects chatbot widget on every page when user is logged in.
 * Include this file via <script src="/js/chatbot.js"></script> on any page.
 */

(function () {
    // Only show for logged-in users
    if (!localStorage.getItem('fras_token')) return;

    // Inject CSS
    const style = document.createElement('style');
    style.textContent = `
        .chat-fab{position:fixed;bottom:24px;right:24px;width:56px;height:56px;border-radius:50%;background:linear-gradient(135deg,#8b5cf6,#6366f1);border:none;color:#fff;font-size:1.5rem;cursor:pointer;box-shadow:0 4px 20px rgba(139,92,246,0.4);z-index:9999;transition:transform .2s,box-shadow .2s;}
        .chat-fab:hover{transform:scale(1.1);box-shadow:0 6px 28px rgba(139,92,246,0.6);}
        .chat-fab .notif-dot{position:absolute;top:2px;right:2px;width:12px;height:12px;background:#22c55e;border-radius:50%;border:2px solid #1e293b;}
        .chat-panel{display:none;position:fixed;bottom:90px;right:24px;width:400px;max-height:560px;background:var(--card-bg,#1e293b);border:1px solid var(--border-color,#334155);border-radius:16px;box-shadow:0 20px 60px rgba(0,0,0,0.5);z-index:10000;flex-direction:column;overflow:hidden;}
        .chat-panel.active{display:flex;}
        .chat-header{padding:14px 18px;background:linear-gradient(135deg,#8b5cf6,#6366f1);color:#fff;display:flex;justify-content:space-between;align-items:center;}
        .chat-header h4{margin:0;font-size:0.95rem;}
        .chat-header button{background:none;border:none;color:#fff;font-size:1.2rem;cursor:pointer;padding:0 4px;}
        .chat-messages{flex:1;overflow-y:auto;padding:14px;min-height:280px;max-height:380px;}
        .chat-msg{margin-bottom:10px;display:flex;}
        .chat-msg.user{justify-content:flex-end;}
        .chat-msg .bubble{max-width:85%;padding:10px 14px;border-radius:12px;font-size:0.85rem;line-height:1.6;white-space:pre-wrap;}
        .chat-msg.user .bubble{background:rgba(139,92,246,0.2);color:var(--text-primary,#e2e8f0);border-bottom-right-radius:4px;}
        .chat-msg.ai .bubble{background:rgba(255,255,255,0.05);color:var(--text-secondary,#94a3b8);border-bottom-left-radius:4px;}
        .chat-suggestions{padding:0 14px 8px;display:flex;flex-wrap:wrap;gap:6px;}
        .chat-suggestions button{background:rgba(139,92,246,0.1);color:#a78bfa;border:1px solid rgba(139,92,246,0.3);border-radius:16px;padding:4px 10px;font-size:0.75rem;cursor:pointer;transition:background .2s;}
        .chat-suggestions button:hover{background:rgba(139,92,246,0.25);}
        .chat-input-area{padding:10px 14px;border-top:1px solid var(--border-color,#334155);display:flex;gap:8px;}
        .chat-input-area input{flex:1;background:var(--glass-bg,#0f172a);border:1px solid var(--border-color,#334155);border-radius:8px;padding:8px 12px;color:var(--text-primary,#e2e8f0);font-size:0.85rem;outline:none;}
        .chat-input-area input:focus{border-color:#8b5cf6;}
        .chat-input-area button{background:linear-gradient(135deg,#8b5cf6,#6366f1);border:none;color:#fff;border-radius:8px;padding:8px 14px;cursor:pointer;font-size:0.85rem;font-weight:600;}
        @media(max-width:480px){.chat-panel{width:calc(100vw - 20px);right:10px;bottom:80px;}}
    `;
    document.head.appendChild(style);

    // Inject HTML
    const chatHTML = `
        <button class="chat-fab" id="fras-chat-fab" title="💬 Hỏi AI về PCCC">💬<span class="notif-dot"></span></button>
        <div class="chat-panel" id="fras-chat-panel">
            <div class="chat-header">
                <h4>🤖 AI Tư vấn PCCC</h4>
                <div>
                    <button onclick="frasChatbot.clear()" title="Xóa lịch sử">🗑️</button>
                    <button onclick="frasChatbot.toggle()">✕</button>
                </div>
            </div>
            <div class="chat-messages" id="fras-chat-messages">
                <div class="chat-msg ai"><div class="bubble">Xin chào! Tôi là trợ lý AI tư vấn PCCC. 🔥

Bạn có thể hỏi tôi về:
• Quy định phòng cháy chữa cháy
• Cách sử dụng bình chữa cháy
• Dấu hiệu nguy cơ cháy nổ
• Pháp luật PCCC mới nhất 2024-2025

Hãy đặt câu hỏi!</div></div>
            </div>
            <div class="chat-suggestions" id="fras-chat-suggestions">
                <button onclick="frasChatbot.ask(this)">Dấu hiệu nào cho thấy hệ thống điện sắp gây cháy?</button>
                <button onclick="frasChatbot.ask(this)">Luật PCCC 55/2024 có gì mới?</button>
                <button onclick="frasChatbot.ask(this)">Cách kiểm tra bình chữa cháy?</button>
            </div>
            <div class="chat-input-area">
                <input type="text" id="fras-chat-input" placeholder="Nhập câu hỏi về PCCC..." />
                <button onclick="frasChatbot.send()">Gửi</button>
            </div>
        </div>
    `;

    const container = document.createElement('div');
    container.innerHTML = chatHTML;
    document.body.appendChild(container);

    // Chatbot logic
    window.frasChatbot = {
        history: [],
        toggle() {
            document.getElementById('fras-chat-panel').classList.toggle('active');
        },
        clear() {
            this.history = [];
            document.getElementById('fras-chat-messages').innerHTML = '<div class="chat-msg ai"><div class="bubble">Đã xóa lịch sử. Hãy đặt câu hỏi mới! 🔥</div></div>';
        },
        ask(btn) {
            document.getElementById('fras-chat-input').value = btn.textContent;
            this.send();
        },
        async send() {
            const input = document.getElementById('fras-chat-input');
            const msg = input.value.trim();
            if (!msg) return;
            input.value = '';

            const msgs = document.getElementById('fras-chat-messages');
            msgs.innerHTML += `<div class="chat-msg user"><div class="bubble">${this._esc(msg)}</div></div>`;
            msgs.innerHTML += `<div class="chat-msg ai" id="fras-chat-loading"><div class="bubble">⏳ Đang suy nghĩ...</div></div>`;
            msgs.scrollTop = msgs.scrollHeight;

            this.history.push({ role: 'user', content: msg });

            // Try to get assessment context from URL
            const params = new URLSearchParams(window.location.search);
            const assessmentId = params.get('id') || null;

            try {
                const token = localStorage.getItem('fras_token');
                const baseUrl = localStorage.getItem('fras_api_url') || '';
                const resp = await fetch(`${baseUrl}/api/ai/chat`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify({
                        assessment_id: assessmentId,
                        message: msg,
                        history: this.history.slice(-6)
                    })
                });

                if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
                const result = await resp.json();
                const reply = result.reply || result.raw_text || 'Không thể trả lời lúc này.';
                this.history.push({ role: 'assistant', content: reply });

                document.getElementById('fras-chat-loading')?.remove();
                msgs.innerHTML += `<div class="chat-msg ai"><div class="bubble">${reply}</div></div>`;

                // Update suggestions
                if (result.suggestions?.length) {
                    document.getElementById('fras-chat-suggestions').innerHTML = result.suggestions.map(s =>
                        `<button onclick="frasChatbot.ask(this)">${this._esc(s)}</button>`
                    ).join('');
                }
            } catch (err) {
                document.getElementById('fras-chat-loading')?.remove();
                msgs.innerHTML += `<div class="chat-msg ai"><div class="bubble" style="color:#ef4444;">Lỗi: ${err.message}</div></div>`;
            }
            msgs.scrollTop = msgs.scrollHeight;
        },
        _esc(s) { const d = document.createElement('div'); d.textContent = s; return d.innerHTML; }
    };

    // FAB click handler
    document.getElementById('fras-chat-fab').addEventListener('click', () => frasChatbot.toggle());

    // Enter key handler
    document.getElementById('fras-chat-input').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') frasChatbot.send();
    });

    // Hide notif dot after first open
    document.getElementById('fras-chat-fab').addEventListener('click', function () {
        const dot = this.querySelector('.notif-dot');
        if (dot) dot.style.display = 'none';
    }, { once: true });

})();
