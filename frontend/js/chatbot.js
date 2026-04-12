/**
 * FRAS Global AI Chatbot
 * Auto-injects chatbot widget on every page when user is logged in.
 */
(function () {
    if (!localStorage.getItem('fras_token')) return;

    const style = document.createElement('style');
    style.textContent = `
        /* ===== FAB Button ===== */
        .fras-fab {
            position: fixed; bottom: 24px; right: 24px;
            width: 64px; height: 64px; border-radius: 50%;
            background: #fff; border: 3px solid #C0202A; color: #fff;
            cursor: grab; box-shadow: 0 4px 16px rgba(0,0,0,0.2);
            z-index: 9999; transition: box-shadow .2s;
            display: flex; align-items: center; justify-content: center;
            overflow: hidden; padding: 0;
            background-image: url('/img/ai_chi_avatar.png');
            background-size: cover;
            background-position: center;
            user-select: none;
            touch-action: none;
        }
        .fras-fab:active { cursor: grabbing; box-shadow: 0 2px 8px rgba(0,0,0,0.3); }
        .fras-fab .notif-dot {
            position: absolute; top: 3px; right: 3px;
            width: 12px; height: 12px; background: #22c55e;
            border-radius: 50%; border: 2px solid #fff;
        }

        /* ===== Chat Panel ===== */
        .fras-panel {
            display: none; position: fixed; bottom: 92px; right: 24px;
            width: 420px; max-height: 580px;
            background: #ffffff; border: 1px solid #e2e8f0;
            border-radius: 12px; box-shadow: 0 12px 48px rgba(0,0,0,0.18);
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
        .fras-msg.ai .fras-avatar { background: #C0202A; color: #fff; font-size: 0.65rem; }
        .fras-msg.user .fras-avatar { background: #1A3A6B; color: #fff; }

        .fras-bubble {
            max-width: 82%; padding: 10px 13px;
            border-radius: 14px; font-size: 0.84rem; line-height: 1.65;
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
            border-radius: 22px; padding: 9px 14px; color: #1e293b;
            font-size: 0.84rem; outline: none; transition: border-color .15s;
        }
        .fras-input-area input::placeholder { color: #94a3b8; }
        .fras-input-area input:focus { border-color: #C0202A; background: #fff; }
        .fras-input-area button {
            background: #C0202A; border: none; color: #fff;
            border-radius: 22px; padding: 9px 18px;
            cursor: pointer; font-size: 0.84rem; font-weight: 600;
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
        <button class="fras-fab" id="fras-fab" title="Hỏi AI về PCCC">
            <span class="notif-dot"></span>
        </button>
        <div class="fras-panel" id="fras-panel">
            <div class="fras-resize-handle" id="fras-resize-handle" title="Kéo để thay đổi kích thước"></div>
            <div class="fras-header">
                <div class="fras-header-left">
                    <div class="fras-header-icon">
                        <svg viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2">
                            <path d="M12 2a10 10 0 1 1 0 20A10 10 0 0 1 12 2z"/>
                            <path d="M12 8v4l3 3"/>
                        </svg>
                    </div>
                    <div>
                        <div class="fras-header-title">Trợ lý ảo Chi</div>
                        <div class="fras-header-sub">Phòng Cảnh sát PCCC & CNCH Bắc Ninh</div>
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
                <span>Hệ thống AI đang hoạt động • Hỏi về pháp luật, kỹ thuật PCCC</span>
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
        _appendWelcome() {
            const msgs = document.getElementById('fras-messages');
            this._addBubble('ai',
                'Xin chào! Tôi là trợ lý ảo Chi, chuyên gia tư vấn về Phòng cháy chữa cháy.\n\n' +
                'Tôi có thể tư vấn về:\n' +
                '• Xử lý tình huống khẩn cấp khi có cháy\n' +
                '• Pháp luật PCCC 2024-2025 (Luật 55/2024, NĐ 105...)\n' +
                '• Quy định trang bị thiết bị PCCC\n' +
                '• An toàn điện, gas, lối thoát nạn\n' +
                '• Huấn luyện và diễn tập PCCC\n\n' +
                'Hãy đặt câu hỏi cho Chi nhé!',
                null, null
            );
        },
        ask(btn) {
            document.getElementById('fras-input').value = btn.textContent;
            this.send();
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
                    <div class="fras-avatar">Chi</div>
                    <div class="fras-bubble">
                        <div class="fras-typing-dot"></div>
                        <div class="fras-typing-dot"></div>
                        <div class="fras-typing-dot"></div>
                    </div>
                </div>`;
            msgs.scrollTop = msgs.scrollHeight;

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

                document.getElementById(typingId)?.remove();

                const reply = result.reply || result.raw_text || 'Không thể trả lời lúc này.';
                this.history.push({ role: 'assistant', content: reply });

                this._addBubble('ai', reply, result.source_type, result.references);

                // Update suggestions
                if (result.suggestions?.length) {
                    document.getElementById('fras-suggestions').innerHTML =
                        result.suggestions.map(s =>
                            `<button onclick="frasChatbot.ask(this)">${this._esc(s)}</button>`
                        ).join('');
                }
            } catch (err) {
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
                : `<div class="fras-avatar">Chi</div>`;

            const div = document.createElement('div');
            div.className = `fras-msg ${isUser ? 'user' : 'ai'}`;
            div.innerHTML = `
                ${avatarHtml}
                <div class="fras-bubble" style="${bubbleStyle}">
                    <pre>${this._esc(text)}</pre>
                    ${sourceBadge}
                    ${refsHtml}
                </div>`;
            msgs.appendChild(div);
        },

        _esc(s) {
            const d = document.createElement('div');
            d.textContent = s;
            return d.innerHTML;
        }
    };

    // FAB click & Drag Logic
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
        const rect = fab.getBoundingClientRect();
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
            
            let newX = initialX + dx;
            let newY = initialY + dy;
            
            // Constrain
            newX = Math.max(0, Math.min(window.innerWidth - fab.offsetWidth, newX));
            newY = Math.max(0, Math.min(window.innerHeight - fab.offsetHeight, newY));
            
            fab.style.left = newX + 'px';
            fab.style.top = newY + 'px';
            fab.style.right = 'auto'; 
            fab.style.bottom = 'auto';
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
