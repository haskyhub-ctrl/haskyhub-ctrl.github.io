/**
 * FRAS Global AI Chatbot
 * Auto-injects chatbot widget on every page when user is logged in.
 */
(function () {
    const style = document.createElement('style');
    style.textContent = `
        /* ===== FAB Wrap & Speech Badge ===== */
        .fras-fab-wrap {
            position: fixed; bottom: 24px; right: 24px;
            z-index: 9999; display: flex; align-items: center; gap: 10px;
            user-select: none;
        }

        .fras-fab-badge {
            background: #ffffff; color: #C0202A;
            padding: 8px 18px; border-radius: 999px;
            box-shadow: 0 6px 20px rgba(192, 32, 42, 0.28), 0 2px 6px rgba(0,0,0,0.08);
            border: 2px solid #C0202A;
            font-weight: 800; font-size: 0.92rem;
            cursor: pointer; display: flex; align-items: center; gap: 7px;
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
            animation: fras-badge-float 3.5s infinite ease-in-out;
            white-space: nowrap; position: relative;
        }
        .fras-fab-badge::after {
            content: ''; position: absolute; right: -7px; top: 50%;
            transform: translateY(-50%);
            border-width: 5px 0 5px 7px; border-style: solid;
            border-color: transparent transparent transparent #C0202A;
        }
        .fras-fab-badge:hover {
            transform: translateY(-3px) scale(1.04);
            box-shadow: 0 8px 26px rgba(192, 32, 42, 0.4);
            background: #fef2f2;
        }
        .fras-fab-badge .badge-icon { font-size: 1.1rem; line-height: 1; }
        .fras-fab-badge .badge-pulse-dot {
            width: 8px; height: 8px; background: #22c55e;
            border-radius: 50%; display: inline-block;
            animation: fras-dot-pulse 1.8s infinite;
        }

        @keyframes fras-badge-float {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-4px); }
        }
        @keyframes fras-dot-pulse {
            0% { box-shadow: 0 0 0 0 rgba(34, 197, 94, 0.7); }
            70% { box-shadow: 0 0 0 6px rgba(34, 197, 94, 0); }
            100% { box-shadow: 0 0 0 0 rgba(34, 197, 94, 0); }
        }

        /* ===== FAB Avatar Button ===== */
        .fras-fab {
            width: 58px; height: 58px; border-radius: 0 !important;
            background: #ffffff; border: 2.5px solid #C0202A; color: #fff;
            cursor: pointer; box-shadow: 0 4px 16px rgba(0,0,0,0.22);
            transition: transform .2s, box-shadow .2s;
            display: flex; align-items: center; justify-content: center;
            overflow: hidden; padding: 4px;
            background-image: url('/img/ai_chi_avatar_256.png');
            background-size: 100% 100%; background-repeat: no-repeat; background-position: center;
            flex-shrink: 0; position: relative;
        }
        .fras-fab:hover { transform: scale(1.05); box-shadow: 0 6px 20px rgba(192,32,42,0.4); }
        .fras-fab:active { transform: scale(0.96); }
        .fras-fab .notif-dot {
            position: absolute; top: 2px; right: 2px;
            width: 10px; height: 10px; background: #22c55e;
            border-radius: 0; border: 1.5px solid #fff;
        }

        /* ===== Chat Panel ===== */
        .fras-panel {
            display: none; position: fixed; bottom: 88px; right: 24px;
            width: 420px; max-height: 580px;
            background: #ffffff; border: 2px solid #C0202A;
            border-radius: 0 !important; box-shadow: 0 16px 54px rgba(0,0,0,0.28);
            z-index: 10000; flex-direction: column; overflow: hidden;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            min-width: 320px; min-height: 360px;
            max-width: 90vw; max-height: 85vh;
        }
        .fras-panel.open { display: flex; }

        /* Resize handle - top left corner */
        .fras-resize-handle {
            position: absolute; top: 0; left: 0;
            width: 20px; height: 20px;
            cursor: nw-resize; z-index: 10001;
            background: transparent;
        }
        .fras-resize-handle::after {
            content: '';
            position: absolute; top: 4px; left: 4px;
            width: 8px; height: 8px;
            border-top: 2px solid #cbd5e1;
            border-left: 2px solid #cbd5e1;
            border-radius: 2px 0 0 0;
            transition: border-color .2s;
        }
        .fras-resize-handle:hover::after {
            border-color: #C0202A;
        }

        /* ===== Header ===== */
        .fras-header {
            background: #C0202A; padding: 0 16px;
            height: 52px; display: flex; align-items: center;
            justify-content: space-between; flex-shrink: 0;
        }
        .fras-header-left { display: flex; align-items: center; gap: 10px; }
        .fras-header-icon {
            width: 32px; height: 32px; background: rgba(255,255,255,0.2);
            border-radius: 50%; display: flex; align-items: center; justify-content: center;
        }
        .fras-header-icon svg { width: 18px; height: 18px; }
        .fras-header-title { color: #fff; font-weight: 700; font-size: 0.9rem; line-height: 1.2; }
        .fras-header-sub { color: rgba(255,255,255,0.75); font-size: 0.72rem; }
        .fras-header-actions { display: flex; gap: 4px; }
        .fras-header-actions button {
            background: rgba(255,255,255,0.15); border: none; color: #fff;
            width: 30px; height: 30px; border-radius: 6px; cursor: pointer;
            display: flex; align-items: center; justify-content: center;
            font-size: 0.85rem; transition: background .15s;
        }
        .fras-header-actions button:hover { background: rgba(255,255,255,0.3); }

        /* ===== Status bar ===== */
        .fras-status {
            background: #f8fafc; border-bottom: 1px solid #e2e8f0;
            padding: 5px 14px; display: flex; align-items: center; gap: 6px;
            font-size: 0.72rem; color: #64748b; flex-shrink: 0;
        }
        .fras-status-dot {
            width: 7px; height: 7px; border-radius: 50%;
            background: #22c55e; animation: fras-pulse 2s infinite;
        }
        @keyframes fras-pulse {
            0%, 100% { opacity: 1; } 50% { opacity: 0.4; }
        }

        /* ===== Messages ===== */
        .fras-messages {
            flex: 1; overflow-y: auto; padding: 16px 14px;
            display: flex; flex-direction: column; gap: 12px;
            background: #f8fafc; min-height: 260px;
            scrollbar-width: thin; scrollbar-color: #cbd5e1 transparent;
        }
        .fras-messages::-webkit-scrollbar { width: 4px; }
        .fras-messages::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 4px; }

        /* Message bubbles */
        .fras-msg { display: flex; align-items: flex-end; gap: 8px; }
        .fras-msg.user { flex-direction: row-reverse; }

        .fras-avatar {
            width: 28px; height: 28px; border-radius: 50%;
            flex-shrink: 0; display: flex; align-items: center; justify-content: center;
            font-size: 0.8rem; font-weight: 700;
        }
        .fras-msg.ai .fras-avatar { background: #fff; overflow: hidden; border: 1.5px solid #C0202A; }
        .fras-msg.ai .fras-avatar img { width: 100%; height: 100%; object-fit: cover; display: block; }
        .fras-msg.user .fras-avatar { background: #1A3A6B; color: #fff; }

        .fras-bubble {
            max-width: 82%; padding: 10px 13px;
            border-radius: 14px; font-size: 0.78rem; line-height: 1.6;
        }
        .fras-msg.user .fras-bubble {
            background: #1A3A6B; color: #ffffff;
            border-bottom-right-radius: 4px;
        }
        .fras-msg.ai .fras-bubble {
            background: #ffffff; color: #1e293b;
            border: 1px solid #e2e8f0; border-bottom-left-radius: 4px;
            box-shadow: 0 1px 4px rgba(0,0,0,0.06);
        }
        .fras-bubble pre {
            white-space: pre-wrap; word-break: break-word;
            margin: 0; font-family: inherit; font-size: 0.84rem;
        }

        /* ===== Câu trả lời có cấu trúc ===== */
        .fras-msg.ai .fras-bubble { max-width: 92%; }
        .fras-rich { font-size: 0.73rem; line-height: 1.52; color: #1e293b; word-break: break-word; }
        .fras-rich p { margin: 0 0 8px; }
        .fras-rich strong { color: #0F2347; font-weight: 800; }
        .fras-rich mark { background: #FFF1B8; color: inherit; padding: 0 2px; }
        .fras-answer { background: #EEF4FC; border-left: 4px solid #1A3A6B; padding: 9px 12px; margin: 0 0 10px; font-weight: 600; color: #0F2347; }
        .fras-h { margin: 10px 0 5px; padding-bottom: 3px; border-bottom: 2px solid #C0202A; color: #C0202A; font-weight: 800; font-size: 0.70rem; letter-spacing: .4px; text-transform: uppercase; }
        .fras-warn { background: #FFF7E6; border-left: 4px solid #C9962C; padding: 8px 12px; margin: 8px 0; color: #7a4b00; font-weight: 600; }
        .fras-steps { list-style: none; counter-reset: step; margin: 4px 0 8px; padding: 0; }
        .fras-steps li { counter-increment: step; position: relative; padding: 5px 0 5px 34px; margin: 0 0 4px; }
        .fras-steps li::before { content: counter(step); position: absolute; left: 0; top: 4px; width: 24px; height: 24px; background: #1A3A6B; color: #fff; font-weight: 800; font-size: 0.78rem; text-align: center; line-height: 24px; }
        .fras-rich ul { margin: 4px 0 8px; padding-left: 20px; }
        .fras-rich ul li { margin: 0 0 3px; }
        .fras-rich ul li::marker { color: #C0202A; }
        .fras-cite { display: inline-block; font-size: 0.68rem; font-weight: 600; color: #1A3A6B; background: #E8EEF8; border: 1px solid #C5D3EA; padding: 0 6px; margin: 0 1px; white-space: normal; }
        .fras-table { width: 100%; border-collapse: collapse; margin: 6px 0 10px; font-size: 0.70rem; }
        .fras-table th { background: #1A3A6B; color: #fff; padding: 5px 8px; text-align: left; font-weight: 700; }
        .fras-table td { padding: 5px 8px; border: 1px solid #D8DCE6; vertical-align: top; }
        .fras-table tr:nth-child(even) td { background: #F6F8FC; }
        .fras-foot { margin-top: 8px; font-size: 0.72rem; font-style: italic; color: #64748b; }
        .fras-feedback { display: flex; gap: 6px; align-items: center; margin-top: 8px; font-size: 0.72rem; color: #64748b; }
        .fras-feedback button { background: #fff; border: 1px solid #cbd5e1; padding: 2px 8px; cursor: pointer; font-size: 0.75rem; }
        .fras-feedback button:hover { border-color: #C0202A; }
        .fras-status-text { margin-left: 8px; font-size: 0.75rem; color: #64748b; }

        /* Source badge */
        .fras-source-badge {
            display: inline-block; font-size: 0.68rem; font-weight: 600;
            padding: 1px 6px; border-radius: 4px; margin-top: 6px;
        }
        .fras-source-badge.docs { background: #dbeafe; color: #1d4ed8; }
        .fras-source-badge.general { background: #fef3c7; color: #92400e; }
        .fras-source-badge.mixed { background: #f0fdf4; color: #166534; }

        /* References */
        .fras-refs {
            margin-top: 8px; padding-top: 8px;
            border-top: 1px solid #e2e8f0; font-size: 0.75rem; color: #64748b;
        }
        .fras-refs strong { color: #475569; }

        /* Typing indicator */
        .fras-typing .fras-bubble {
            display: flex; align-items: center; gap: 5px; padding: 12px 16px;
        }
        .fras-typing-dot {
            width: 7px; height: 7px; border-radius: 50%; background: #94a3b8;
            animation: fras-typing 1.2s infinite ease-in-out;
        }
        .fras-typing-dot:nth-child(2) { animation-delay: .2s; }
        .fras-typing-dot:nth-child(3) { animation-delay: .4s; }
        @keyframes fras-typing {
            0%, 80%, 100% { transform: scale(0.7); opacity: .5; }
            40% { transform: scale(1); opacity: 1; }
        }

        /* ===== Suggestions ===== */
        .fras-suggestions {
            padding: 6px 14px 10px; display: flex;
            flex-wrap: wrap; gap: 6px; background: #f8fafc;
            border-top: 1px solid #e2e8f0; flex-shrink: 0;
        }
        .fras-suggestions button {
            background: #fff; color: #C0202A;
            border: 1px solid #fca5a5; border-radius: 20px;
            padding: 4px 10px; font-size: 0.75rem; cursor: pointer;
            transition: background .15s, border-color .15s; line-height: 1.4;
        }
        .fras-suggestions button:hover { background: #fef2f2; border-color: #C0202A; }

        /* ===== Input area ===== */
        .fras-input-area {
            padding: 10px 14px; border-top: 1px solid #e2e8f0;
            display: flex; gap: 8px; background: #fff; flex-shrink: 0;
        }
        .fras-input-area input {
            flex: 1; background: #f1f5f9; border: 1px solid #e2e8f0;
            border-radius: 22px; padding: 8px 14px; color: #1e293b;
            font-size: 0.80rem; outline: none; transition: border-color .15s;
        }
        .fras-input-area input::placeholder { color: #94a3b8; }
        .fras-input-area input:focus { border-color: #C0202A; background: #fff; }
        .fras-input-area button {
            background: #C0202A; border: none; color: #fff;
            border-radius: 22px; padding: 8px 16px;
            cursor: pointer; font-size: 0.80rem; font-weight: 600;
            transition: background .15s; white-space: nowrap; flex-shrink: 0;
        }
        .fras-input-area button:hover { background: #8B0000; }
        .fras-input-area button:disabled { background: #94a3b8; cursor: not-allowed; }

        /* ===== Responsive ===== */
        @media (max-width: 480px) {
            .fras-panel { width: calc(100vw - 16px); right: 8px; bottom: 82px; max-height: 70vh; }
        }
    `;
    document.head.appendChild(style);

    // HTML structure
    const wrap = document.createElement('div');
    wrap.innerHTML = `
        <div class="fras-fab-wrap" id="fras-fab-wrap">
            <div class="fras-fab-badge" id="fras-fab-badge" onclick="frasChatbot.toggle()" title="Hỏi Trợ lý ảo về pháp luật, TTHC PCCC">
                <span class="badge-icon">💬</span>
                <span>Hãy đặt câu hỏi</span>
                <span class="badge-pulse-dot"></span>
            </div>
            <button class="fras-fab" id="fras-fab" title="Trợ lý ảo hỗ trợ giải đáp pháp luật và TTHC về PCCC">
                <span class="notif-dot"></span>
            </button>
        </div>
        <div class="fras-panel" id="fras-panel">
            <div class="fras-resize-handle" id="fras-resize-handle" title="Kéo để thay đổi kích thước"></div>
            <div class="fras-header">
                <div class="fras-header-left">
                    <div class="fras-header-icon" style="background:#fff; overflow:hidden; width:36px; height:36px; flex-shrink:0;">
                        <img src="/img/ai_chi_avatar_256.png" alt="Trợ lý ảo" width="36" height="36" style="object-fit:cover; display:block;">
                    </div>
                    <div>
                        <div class="fras-header-title">Trợ lý ảo hỗ trợ giải đáp pháp luật và TTHC về PCCC</div>
                        <div class="fras-header-sub">Công an thành phố Bắc Ninh • PCCC & CNCH</div>
                    </div>
                </div>
                <div class="fras-header-actions">
                    <button onclick="frasChatbot.clear()" title="Xóa hội thoại">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                            <polyline points="3 6 5 6 21 6"/><path d="M19 6l-1 14H6L5 6"/><path d="M10 11v6M14 11v6"/>
                        </svg>
                    </button>
                    <button onclick="frasChatbot.close()" title="Đóng">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                            <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
                        </svg>
                    </button>
                </div>
            </div>
            <div class="fras-status">
                <span class="fras-status-dot"></span>
                <span>Trực tuyến 24/7 • Hỏi đáp pháp luật, thủ tục hành chính, quy chuẩn PCCC</span>
            </div>
            <div class="fras-messages" id="fras-messages"></div>
            <div class="fras-suggestions" id="fras-suggestions">
                <button onclick="frasChatbot.ask(this)">Khi cháy phải làm gì?</button>
                <button onclick="frasChatbot.ask(this)">Luật PCCC 55/2024 có gì mới?</button>
                <button onclick="frasChatbot.ask(this)">Quy định bình chữa cháy?</button>
            </div>
            <div class="fras-input-area">
                <input type="text" id="fras-input" placeholder="Nhập câu hỏi về PCCC..." autocomplete="off" />
                <button id="fras-send-btn" onclick="frasChatbot.send()">Gửi</button>
            </div>
        </div>
    `;
    document.body.appendChild(wrap);

    // Chatbot logic
    window.frasChatbot = {
        history: [],
        isOpen: false,
        suggestionPool: [
            "Khi cháy phải làm gì?",
            "Luật PCCC 55/2024 có gì mới?",
            "Quy định bình chữa cháy?",
            "Lối thoát nạn an toàn?",
            "Kiểm tra hệ thống điện",
            "Sơ cứu người bị ngạt khói",
            "Quy định PCCC nhà trọ",
            "Phân loại bình chữa cháy",
            "Mức phạt vi phạm PCCC"
        ],

        toggle() {
            this.isOpen ? this.close() : this.open();
        },
        open() {
            this.isOpen = true;
            document.getElementById('fras-panel').classList.add('open');
            document.getElementById('fras-input').focus();
            const dot = document.querySelector('.fras-fab .notif-dot');
            if (dot) dot.style.display = 'none';
            const badge = document.getElementById('fras-fab-badge');
            if (badge) badge.style.display = 'none';
            // Show welcome message if empty
            const msgs = document.getElementById('fras-messages');
            if (!msgs.children.length) {
                this._appendWelcome();
                this._randomizeSuggestions();
            }
        },
        close() {
            this.isOpen = false;
            document.getElementById('fras-panel').classList.remove('open');
            const badge = document.getElementById('fras-fab-badge');
            if (badge) badge.style.display = 'flex';
        },
        clear() {
            this.history = [];
            const msgs = document.getElementById('fras-messages');
            msgs.innerHTML = '';
            this._appendWelcome();
            this._randomizeSuggestions();
        },
        _randomizeSuggestions() {
            const shuffled = [...this.suggestionPool].sort(() => 0.5 - Math.random());
            const selected = shuffled.slice(0, 3);
            const container = document.getElementById('fras-suggestions');
            container.innerHTML = selected.map(s => 
                `<button onclick="frasChatbot.ask(this)">${this._esc(s)}</button>`
            ).join('');
        },
        askText(text) {
            if (!text) return;
            if (!this.isOpen) this.open();
            document.getElementById('fras-input').value = text;
            this.send();
        },
        ask(btn) {
            this.askText(btn.textContent.trim());
        },
        _appendWelcome() {
            const msgs = document.getElementById('fras-messages');
            this._addBubble('ai',
                '>> Chào bạn, tôi là Trợ lý ảo hỗ trợ giải đáp pháp luật và thủ tục hành chính về Phòng cháy chữa cháy và Cứu nạn cứu hộ của Công an thành phố Bắc Ninh.\n\n' +
                '## Tôi có thể giúp bạn\n' +
                '• Quy định pháp luật: Luật PCCC và CNCH số 55/2024/QH15, các Nghị định, Thông tư hướng dẫn\n' +
                '• Thủ tục hành chính: thẩm duyệt thiết kế, nghiệm thu, kiểm tra, cấp giấy chứng nhận, thời hạn giải quyết\n' +
                '• Điều kiện an toàn PCCC theo từng loại hình cơ sở: nhà ở, chung cư, cơ sở kinh doanh, sản xuất, kho, trường học, bệnh viện...\n' +
                '• Trang thiết bị: bình chữa cháy, báo cháy tự động, chữa cháy tự động, chiếu sáng sự cố, biển chỉ dẫn\n' +
                '• Lối thoát nạn, an toàn điện, khí gas, chất cháy nổ, phương tiện giao thông\n' +
                '• Tổ chức lực lượng: đội PCCC cơ sở, huấn luyện, phương án chữa cháy và CNCH\n' +
                '• Kỹ năng xử lý khi xảy ra cháy, thoát hiểm, sơ cứu\n' +
                '• Khắc phục tồn tại, nguy cơ mất an toàn và cách hạ mức nguy cơ trên hệ thống\n\n' +
                '\n!! Bạn chọn câu hỏi gợi ý hoặc nhập nội dung cần giải đáp ở bên dưới nhé.',
                null, null
            );
        },
        async send() {
            const input = document.getElementById('fras-input');
            const btn = document.getElementById('fras-send-btn');
            const msg = input.value.trim();
            if (!msg) return;

            if (!this.isOpen) this.open();
            input.value = '';
            btn.disabled = true;

            const msgs = document.getElementById('fras-messages');

            // Add user message
            this._addBubble('user', msg, null, null);
            msgs.scrollTop = msgs.scrollHeight;

            // Add typing indicator
            const typingId = 'fras-typing-' + Date.now();
            msgs.innerHTML += `
                <div class="fras-msg ai fras-typing" id="${typingId}">
                    <div class="fras-avatar"><img src="/img/ai_chi_avatar_256.png" alt="Trợ lý ảo"></div>
                    <div class="fras-bubble">
                        <div class="fras-typing-dot"></div>
                        <div class="fras-typing-dot"></div>
                        <div class="fras-typing-dot"></div>
                        <span class="fras-status-text" id="${typingId}-t">Chi đang tra cứu văn bản...</span>
                    </div>
                </div>`;
            msgs.scrollTop = msgs.scrollHeight;
            const stages = [[5000, 'Chi đang đối chiếu các quy định...'], [12000, 'Chi đang kiểm tra hiệu lực của căn cứ...'], [22000, 'Sắp xong rồi, Chi đang hoàn thiện câu trả lời...']];
            const timers = stages.map(([ms, txt]) => setTimeout(() => { const el = document.getElementById(typingId + '-t'); if (el) el.textContent = txt; }, ms));

            this.history.push({ role: 'user', content: msg });

            const params = new URLSearchParams(window.location.search);
            const assessmentId = params.get('id') || null;

            try {
                let result;
                if (window.api) {
                    result = await window.api.post('/ai/chat', {
                        assessment_id: assessmentId,
                        message: msg,
                        history: this.history.slice(-6)
                    });
                } else {
                    const token = localStorage.getItem('fras_token');
                    const baseUrl = localStorage.getItem('fras_api_url') || window.location.origin;
                    const resp = await fetch(`${baseUrl}/api/ai/chat`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            ...(token ? { 'Authorization': `Bearer ${token}` } : {})
                        },
                        body: JSON.stringify({
                            assessment_id: assessmentId,
                            message: msg,
                            history: this.history.slice(-6)
                        })
                    });
                    if (!resp.ok) throw new Error(`Lỗi kết nối (HTTP ${resp.status})`);
                    result = await resp.json();
                }

                timers.forEach(clearTimeout);
                document.getElementById(typingId)?.remove();

                const reply = result.reply || result.raw_text || 'Không thể trả lời lúc này.';
                this.history.push({ role: 'assistant', content: reply });

                this._addBubble('ai', reply, result.source_type, result.references);
                this._addFeedback(msg, reply);

                // Update suggestions
                if (result.suggestions?.length) {
                    document.getElementById('fras-suggestions').innerHTML =
                        result.suggestions.map(s =>
                            `<button onclick="frasChatbot.ask(this)">${this._esc(s)}</button>`
                        ).join('');
                }
            } catch (err) {
                timers.forEach(clearTimeout);
                document.getElementById(typingId)?.remove();
                this._addBubble('ai-error', `Không thể kết nối AI: ${err.message}\n\nVui lòng thử lại hoặc liên hệ quản trị viên.`, null, null);
            }

            msgs.scrollTop = msgs.scrollHeight;
            btn.disabled = false;
            input.focus();
        },

        _addBubble(role, text, sourceType, refs) {
            const msgs = document.getElementById('fras-messages');
            const isUser = role === 'user';
            const isError = role === 'ai-error';

            let sourceBadge = '';
            if (!isUser && sourceType) {
                const labels = { docs: '📋 Từ văn bản pháp lý', general: '🌐 Kiến thức chung', mixed: '📚 Kết hợp' };
                sourceBadge = `<div class="fras-source-badge ${sourceType}">${labels[sourceType] || ''}</div>`;
            }

            let refsHtml = '';
            if (refs && refs.length) {
                refsHtml = `<div class="fras-refs"><strong>Văn bản tham chiếu:</strong><br>${refs.map(r => `• ${this._esc(r)}`).join('<br>')}</div>`;
            }

            const bubbleStyle = isError ? 'background:#fef2f2;color:#991b1b;border-color:#fca5a5;' : '';
            const avatarHtml = isUser
                ? `<div class="fras-avatar">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor">
                            <path d="M12 12c2.7 0 4.8-2.1 4.8-4.8S14.7 2.4 12 2.4 7.2 4.5 7.2 7.2 9.3 12 12 12zm0 2.4c-3.2 0-9.6 1.6-9.6 4.8v2.4h19.2v-2.4c0-3.2-6.4-4.8-9.6-4.8z"/>
                        </svg>
                   </div>`
                : `<div class="fras-avatar"><img src="/img/ai_chi_avatar_256.png" alt="Trợ lý ảo"></div>`;

            const bubbleContent = isUser
                ? `<pre>${this._esc(text)}</pre>`
                : `<div class="fras-rich">${this._renderRich(text)}</div>`;

            const div = document.createElement('div');
            div.className = `fras-msg ${isUser ? 'user' : 'ai'}`;
            div.innerHTML = `
                ${avatarHtml}
                <div class="fras-bubble" style="${bubbleStyle}">
                    ${bubbleContent}
                    ${sourceBadge}
                    ${refsHtml}
                </div>`;
            msgs.appendChild(div);
        },

        // Hiển thị câu trả lời có cấu trúc: >> kết luận, ## tiêu đề, !! lưu ý, ~~ chú thích, bước đánh số, gạch đầu dòng, bảng, **đậm**, ==nổi==, {{căn cứ}}
        _renderRich(raw) {
            if (!raw) return '';
            const link = (m, a, b) => `<a href="${b || a}" target="_blank" rel="noopener noreferrer" style="color:#2563eb;text-decoration:underline;">${a}</a>`;
            const inline = (t) => {
                let h = this._esc(t);
                h = h.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
                h = h.replace(/==([^=]+)==/g, '<mark>$1</mark>');
                h = h.replace(/\{\{([^}]+)\}\}/g, '<span class="fras-cite">$1</span>');
                h = h.replace(/\[([^\]]+)\]\((https?:\/\/[^\s)]+)\)/g, (m, a, b) => link(m, a, b));
                h = h.replace(/(^|[^">])(https?:\/\/[^\s<]+)/g, (m, pre, url) => pre + link(m, url, url));
                return h;
            };
            const lines = String(raw).replace(/\r/g, '').split('\n');
            const out = [];
            let list = null;                       // 'ol' hoặc 'ul' đang mở
            const closeList = () => { if (list) { out.push(`</${list}>`); list = null; } };
            for (let i = 0; i < lines.length; i++) {
                const line = lines[i];
                if (!line.trim()) { closeList(); continue; }
                let m;
                if ((m = line.match(/^\s*>>\s+(.*)$/))) { closeList(); out.push(`<div class="fras-answer">${inline(m[1])}</div>`); continue; }
                if ((m = line.match(/^\s*##\s+(.*)$/))) { closeList(); out.push(`<div class="fras-h">${inline(m[1])}</div>`); continue; }
                if ((m = line.match(/^\s*!!\s+(.*)$/))) { closeList(); out.push(`<div class="fras-warn">⚠ ${inline(m[1])}</div>`); continue; }
                if ((m = line.match(/^\s*~~\s+(.*)$/))) { closeList(); out.push(`<div class="fras-foot">${inline(m[1])}</div>`); continue; }
                if (/^\s*\|/.test(line) && i + 1 < lines.length && /^\s*\|?[\s:|-]+\|[\s:|-]*$/.test(lines[i + 1]) && /-/.test(lines[i + 1])) {
                    closeList();
                    const cells = (l) => l.trim().replace(/^\||\|$/g, '').split('|').map(c => c.trim());
                    const head = cells(line);
                    let j = i + 2;
                    const rows = [];
                    while (j < lines.length && /^\s*\|/.test(lines[j])) { rows.push(cells(lines[j])); j++; }
                    out.push('<table class="fras-table"><thead><tr>' + head.map(c => `<th>${inline(c)}</th>`).join('') + '</tr></thead><tbody>' +
                        rows.map(r => '<tr>' + r.map(c => `<td>${inline(c)}</td>`).join('') + '</tr>').join('') + '</tbody></table>');
                    i = j - 1;
                    continue;
                }
                if ((m = line.match(/^\s*(\d+)[.)]\s+(.*)$/))) {
                    if (list !== 'ol') { closeList(); out.push('<ol class="fras-steps">'); list = 'ol'; }
                    out.push(`<li>${inline(m[2])}</li>`);
                    continue;
                }
                if ((m = line.match(/^\s*[-*•]\s+(.*)$/))) {
                    if (list !== 'ul') { closeList(); out.push('<ul>'); list = 'ul'; }
                    out.push(`<li>${inline(m[1])}</li>`);
                    continue;
                }
                closeList();
                out.push(`<p>${inline(line)}</p>`);
            }
            closeList();
            return out.join('');
        },

        // Nút phản hồi: câu trả lời chưa tốt sẽ được gửi vào hàng chờ câu hỏi khó để cán bộ bổ sung đáp án chuẩn
        _addFeedback(question, reply) {
            const msgs = document.getElementById('fras-messages');
            const last = msgs.lastElementChild;
            const bubble = last && last.querySelector('.fras-bubble');
            if (!bubble) return;
            const box = document.createElement('div');
            box.className = 'fras-feedback';
            box.innerHTML = 'Câu trả lời này có giúp được bạn không? <button data-v="1">👍 Có</button> <button data-v="0">👎 Chưa</button>';
            box.querySelectorAll('button').forEach(b => b.addEventListener('click', async () => {
                const helpful = b.dataset.v === '1';
                box.textContent = helpful ? 'Cảm ơn bạn đã phản hồi.' : 'Cảm ơn bạn. Chi đã ghi lại để cán bộ bổ sung câu trả lời chuẩn.';
                try {
                    const baseUrl = localStorage.getItem('fras_api_url') || window.location.origin;
                    await fetch(`${baseUrl}/api/ai/chat/feedback`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ message: question, reply: reply.slice(0, 1500), helpful }) });
                } catch (e) { /* bỏ qua */ }
            }));
            bubble.appendChild(box);
        },

        _formatText(text) {
            if (!text) return '';
            // Xóa triệt để các ký tự markdown thừa nếu có (###, **, ---)
            let s = text.replace(/^[ \t]*#{1,6}\s*/gm, '').replace(/\*\*/g, '').replace(/^[ \t]*[-=_]{3,}[ \t]*$/gm, '');
            s = this._esc(s);
            // Hỗ trợ chuyển link markdown [Tên](url) thành thẻ <a>
            s = s.replace(/\[([^\]]+)\]\((https?:\/\/[^\s\)]+)\)/g, '<a href="$2" target="_blank" rel="noopener noreferrer" style="color:#2563eb;text-decoration:underline;">$1</a>');
            // Hỗ trợ chuyển link url thuần thành thẻ <a>
            s = s.replace(/(^|[^">])(https?:\/\/[^\s<]+)/g, '$1<a href="$2" target="_blank" rel="noopener noreferrer" style="color:#2563eb;text-decoration:underline;">$2</a>');
            return s;
        },

        _esc(s) {
            const d = document.createElement('div');
            d.textContent = s;
            return d.innerHTML;
        }
    };

    // FAB click & Drag Logic
    const fabWrap = document.getElementById('fras-fab-wrap');
    const fab = document.getElementById('fras-fab');
    let isDragging = false;
    let startX, startY, initialX, initialY;
    
    function startDrag(e) {
        if (e.type === 'touchstart') {
            startX = e.touches[0].clientX;
            startY = e.touches[0].clientY;
        } else {
            startX = e.clientX;
            startY = e.clientY;
        }
        
        isDragging = false;
        const targetEl = fabWrap || fab;
        const rect = targetEl.getBoundingClientRect();
        initialX = rect.left;
        initialY = rect.top;
        
        document.addEventListener('mousemove', onDrag);
        document.addEventListener('mouseup', stopDrag);
        document.addEventListener('touchmove', onDrag, {passive: false});
        document.addEventListener('touchend', stopDrag);
    }
    
    function onDrag(e) {
        let clientX, clientY;
        if (e.type === 'touchmove') {
            clientX = e.touches[0].clientX;
            clientY = e.touches[0].clientY;
        } else {
            clientX = e.clientX;
            clientY = e.clientY;
            e.preventDefault();
        }
        
        const dx = clientX - startX;
        const dy = clientY - startY;
        
        if (Math.abs(dx) > 3 || Math.abs(dy) > 3) {
            isDragging = true;
            if (e.type === 'touchmove') e.preventDefault(); // prevent scroll
            
            const targetEl = fabWrap || fab;
            let newX = initialX + dx;
            let newY = initialY + dy;
            
            // Constrain
            newX = Math.max(0, Math.min(window.innerWidth - targetEl.offsetWidth, newX));
            newY = Math.max(0, Math.min(window.innerHeight - targetEl.offsetHeight, newY));
            
            targetEl.style.left = newX + 'px';
            targetEl.style.top = newY + 'px';
            targetEl.style.right = 'auto'; 
            targetEl.style.bottom = 'auto';
        }
    }
    
    function stopDrag() {
        document.removeEventListener('mousemove', onDrag);
        document.removeEventListener('mouseup', stopDrag);
        document.removeEventListener('touchmove', onDrag);
        document.removeEventListener('touchend', stopDrag);
    }
    
    fab.addEventListener('mousedown', startDrag);
    fab.addEventListener('touchstart', startDrag, {passive: false});
    
    fab.addEventListener('click', (e) => {
        if (isDragging) {
            e.preventDefault();
            e.stopPropagation();
        } else {
            frasChatbot.toggle();
        }
    });

    // Enter key
    document.getElementById('fras-input').addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) frasChatbot.send();
    });

    // ==================== RESIZE LOGIC ====================
    const resizeHandle = document.getElementById('fras-resize-handle');
    const panel = document.getElementById('fras-panel');
    let isResizing = false;
    let resizeStartX, resizeStartY, startWidth, startHeight, startBottom, startRight;

    function startResize(e) {
        isResizing = true;
        e.preventDefault();
        e.stopPropagation();
        
        const touch = e.type === 'touchstart' ? e.touches[0] : e;
        resizeStartX = touch.clientX;
        resizeStartY = touch.clientY;
        
        const rect = panel.getBoundingClientRect();
        startWidth = rect.width;
        startHeight = rect.height;
        startBottom = window.innerHeight - rect.bottom;
        startRight = window.innerWidth - rect.right;
        
        panel.style.transition = 'none';
        
        document.addEventListener('mousemove', onResize);
        document.addEventListener('mouseup', stopResize);
        document.addEventListener('touchmove', onResize, { passive: false });
        document.addEventListener('touchend', stopResize);
    }
    
    function onResize(e) {
        if (!isResizing) return;
        e.preventDefault();
        
        const touch = e.type === 'touchmove' ? e.touches[0] : e;
        const dx = resizeStartX - touch.clientX;  // moving left = increase width
        const dy = resizeStartY - touch.clientY;  // moving up = increase height
        
        let newW = Math.max(320, Math.min(startWidth + dx, window.innerWidth * 0.9));
        let newH = Math.max(360, Math.min(startHeight + dy, window.innerHeight * 0.85));
        
        panel.style.width = newW + 'px';
        panel.style.maxHeight = newH + 'px';
        panel.style.height = newH + 'px';
    }
    
    function stopResize() {
        isResizing = false;
        panel.style.transition = '';
        document.removeEventListener('mousemove', onResize);
        document.removeEventListener('mouseup', stopResize);
        document.removeEventListener('touchmove', onResize);
        document.removeEventListener('touchend', stopResize);
    }
    
    resizeHandle.addEventListener('mousedown', startResize);
    resizeHandle.addEventListener('touchstart', startResize, { passive: false });

})();
