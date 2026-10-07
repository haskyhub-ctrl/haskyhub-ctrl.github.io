// homepage.js
document.addEventListener('DOMContentLoaded', () => {
    // 1. Intersection Observer for Fade-In-Up Animations
    const observerOptions = {
        root: null,
        rootMargin: '0px 0px -50px 0px',
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const el = entry.target;
                const delay = el.getAttribute('data-delay');
                if (delay) {
                    setTimeout(() => {
                        el.classList.add('visible');
                    }, parseInt(delay));
                } else {
                    el.classList.add('visible');
                }
                observer.unobserve(el);
            }
        });
    }, observerOptions);

    document.querySelectorAll('.fade-in-up, .slide-up').forEach(el => {
        observer.observe(el);
    });

    // 2. Count-Up Animation
    const statsObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const counters = entry.target.querySelectorAll('.count-up');
                counters.forEach(counter => {
                    const targetText = counter.getAttribute('data-target');
                    if (!targetText) return;
                    
                    const target = parseFloat(targetText.replace(/,/g, ''));
                    const duration = 2000; // ms
                    const increment = target / (duration / 16); // 60fps
                    let current = 0;

                    const updateCounter = () => {
                        current += increment;
                        if (current < target) {
                            counter.innerText = Math.ceil(current).toLocaleString('vi-VN');
                            requestAnimationFrame(updateCounter);
                        } else {
                            counter.innerText = target.toLocaleString('vi-VN');
                        }
                    };

                    updateCounter();
                });
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    const statsSection = document.getElementById('stats');
    if (statsSection) {
        statsObserver.observe(statsSection);
    }
    const heroContent = document.querySelector('.hp-hero-content');
    if (heroContent) {
        statsObserver.observe(heroContent);
    }

    // Initialize embedded AI Chatbot on Homepage
    if (document.getElementById('hp-chat-messages')) {
        hpRenderWelcome();
    }
});

// ============================================================
// 3. HOMEPAGE EMBEDDED AI COPILOT (TRỢ LÝ ẢO CHI)
// ============================================================
let hpHistory = [];
let hpIsSending = false;

function hpEscapeHtml(str) {
    const d = document.createElement('div');
    d.textContent = str || '';
    return d.innerHTML;
}

function hpFormatText(text) {
    if (!text) return '';
    // Format bold **text** -> <strong>text</strong>
    let s = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    // Remove standalone markdown hashes
    s = s.replace(/^[ \t]*#{1,6}\s*/gm, '');
    // Links [Title](url) -> <a>
    s = s.replace(/\[([^\]]+)\]\((https?:\/\/[^\s\)]+)\)/g, '<a href="$2" target="_blank" rel="noopener noreferrer">$1</a>');
    return s;
}

function hpRenderWelcome() {
    const container = document.getElementById('hp-chat-messages');
    if (!container) return;

    container.innerHTML = `
        <div class="hp-msg-row ai">
            <div class="hp-msg-avatar">
                <img src="/img/ai_chi_avatar.png" alt="Chi">
            </div>
            <div class="hp-msg-bubble">
                <div class="hp-msg-meta">
                    <span>Trợ lý Ảo Chi • Cảnh sát PCCC</span>
                </div>
                <div class="hp-msg-text">Xin chào quý người dân và chủ cơ sở! Tôi là <strong>Trợ lý ảo Chi</strong>, hỗ trợ trực tuyến 24/7 về công tác Phòng cháy chữa cháy & Cứu nạn cứu hộ.

Tôi có thể hỗ trợ bạn:
• Tra cứu <strong>Luật PCCC số 55/2024/QH15</strong> và các Nghị định mới nhất.
• Quy định trang bị bình chữa cháy, đèn sự cố, hệ thống báo cháy.
• Kỹ năng thoát nạn khẩn cấp, an toàn điện, gas và sạc pin xe điện.
• Khắc phục các vi phạm an toàn PCCC thường gặp.

Bạn có thể bấm vào các gợi ý bên dưới hoặc gửi câu hỏi trực tiếp cho Chi nhé!</div>
                <div class="hp-followup-chips">
                    <button type="button" class="hp-chip-btn" onclick="hpAskChi(this)">🚨 Khi cháy chung cư mini phải làm gì?</button>
                    <button type="button" class="hp-chip-btn" onclick="hpAskChi(this)">📜 Điểm mới Luật PCCC 55/2024?</button>
                    <button type="button" class="hp-chip-btn" onclick="hpAskChi(this)">🧯 Cách kiểm tra hạn dùng bình chữa cháy?</button>
                    <button type="button" class="hp-chip-btn" onclick="hpAskChi(this)">⚡ Hướng dẫn an toàn khi sạc pin xe điện?</button>
                </div>
            </div>
        </div>
    `;
    container.scrollTop = 0;
}

function hpClearChat() {
    hpHistory = [];
    hpRenderWelcome();
    const input = document.getElementById('hp-chat-input');
    if (input) {
        input.value = '';
        input.focus();
    }
}

function hpAskChi(btnOrText) {
    const text = typeof btnOrText === 'string' ? btnOrText : btnOrText.textContent.trim();
    if (!text) return;
    const input = document.getElementById('hp-chat-input');
    if (input) input.value = text;
    hpSubmitQuestion(text);
}

function hpHandleKeydown(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        const input = document.getElementById('hp-chat-input');
        if (input && input.value.trim()) {
            hpSubmitQuestion(input.value.trim());
        }
    }
}

function hpHandleSend(e) {
    e.preventDefault();
    const input = document.getElementById('hp-chat-input');
    if (input && input.value.trim()) {
        hpSubmitQuestion(input.value.trim());
    }
}

async function hpSubmitQuestion(text) {
    if (!text || hpIsSending) return;
    hpIsSending = true;

    const input = document.getElementById('hp-chat-input');
    const sendBtn = document.getElementById('hp-chat-send-btn');
    const messages = document.getElementById('hp-chat-messages');

    if (input) input.value = '';
    if (sendBtn) sendBtn.disabled = true;

    // 1. Render User Message
    const userRow = document.createElement('div');
    userRow.className = 'hp-msg-row user';
    userRow.innerHTML = `
        <div class="hp-msg-avatar user-avatar">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 12c2.7 0 4.8-2.1 4.8-4.8S14.7 2.4 12 2.4 7.2 4.5 7.2 7.2 9.3 12 12 12zm0 2.4c-3.2 0-9.6 1.6-9.6 4.8v2.4h19.2v-2.4c0-3.2-6.4-4.8-9.6-4.8z"/>
            </svg>
        </div>
        <div class="hp-msg-bubble">
            <div class="hp-msg-text">${hpEscapeHtml(text)}</div>
        </div>
    `;
    messages.appendChild(userRow);
    messages.scrollTop = messages.scrollHeight;

    hpHistory.push({ role: 'user', content: text });

    // 2. Render Typing Indicator
    const typingId = 'hp-typing-' + Date.now();
    const typingRow = document.createElement('div');
    typingRow.className = 'hp-msg-row ai';
    typingRow.id = typingId;
    typingRow.innerHTML = `
        <div class="hp-msg-avatar">
            <img src="/img/ai_chi_avatar.png" alt="Chi">
        </div>
        <div class="hp-typing-bubble">
            <div class="hp-typing-dot"></div>
            <div class="hp-typing-dot"></div>
            <div class="hp-typing-dot"></div>
            <span style="font-size:0.78rem;color:#64748B;margin-left:6px;">Chi đang tra cứu dữ liệu pháp luật...</span>
        </div>
    `;
    messages.appendChild(typingRow);
    messages.scrollTop = messages.scrollHeight;

    // 3. API Call
    try {
        let result;
        const payload = {
            assessment_id: null,
            message: text,
            history: hpHistory.slice(-6)
        };

        if (window.api && typeof window.api.post === 'function') {
            result = await window.api.post('/ai/chat', payload);
        } else {
            const token = localStorage.getItem('fras_token');
            const baseUrl = localStorage.getItem('fras_api_url') || window.location.origin;
            const resp = await fetch(`${baseUrl}/api/ai/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    ...(token ? { 'Authorization': `Bearer ${token}` } : {})
                },
                body: JSON.stringify(payload)
            });
            if (!resp.ok) throw new Error(`Lỗi kết nối máy chủ (HTTP ${resp.status})`);
            result = await resp.json();
        }

        document.getElementById(typingId)?.remove();

        const reply = result.reply || result.raw_text || 'Không thể tạo phản hồi lúc này.';
        hpHistory.push({ role: 'assistant', content: reply });

        // Source badge
        let sourceBadge = '';
        if (result.source_type) {
            const labels = {
                docs: '📋 Từ văn bản pháp luật',
                general: '🌐 Kiến thức nghiệp vụ',
                mixed: '📚 Kết hợp quy chuẩn'
            };
            sourceBadge = `<div class="hp-source-tag ${hpEscapeHtml(result.source_type)}">${labels[result.source_type] || ''}</div>`;
        }

        // Legal references
        let refsHtml = '';
        if (result.references && result.references.length) {
            refsHtml = `
                <div class="hp-legal-refs">
                    <strong>📖 Văn bản tham chiếu:</strong>
                    ${result.references.map(r => `<div>• ${hpEscapeHtml(r)}</div>`).join('')}
                </div>
            `;
        }

        // Suggestions
        let suggestionsHtml = '';
        if (result.suggestions && result.suggestions.length) {
            suggestionsHtml = `
                <div class="hp-followup-chips">
                    ${result.suggestions.map(s => `
                        <button type="button" class="hp-chip-btn" onclick="hpAskChi(this)">${hpEscapeHtml(s)}</button>
                    `).join('')}
                </div>
            `;
        }

        const aiRow = document.createElement('div');
        aiRow.className = 'hp-msg-row ai';
        aiRow.innerHTML = `
            <div class="hp-msg-avatar">
                <img src="/img/ai_chi_avatar.png" alt="Chi">
            </div>
            <div class="hp-msg-bubble">
                <div class="hp-msg-meta">
                    <span>Trợ lý Ảo Chi • Cảnh sát PCCC</span>
                </div>
                <div class="hp-msg-text">${hpFormatText(reply)}</div>
                ${sourceBadge}
                ${refsHtml}
                ${suggestionsHtml}
            </div>
        `;
        messages.appendChild(aiRow);
    } catch (err) {
        document.getElementById(typingId)?.remove();
        const errRow = document.createElement('div');
        errRow.className = 'hp-msg-row ai';
        errRow.innerHTML = `
            <div class="hp-msg-avatar">
                <img src="/img/ai_chi_avatar.png" alt="Chi">
            </div>
            <div class="hp-msg-bubble" style="background:#FEF2F2;border-color:#FCA5A5;color:#991B1B;">
                <div class="hp-msg-meta" style="color:#DC2626;">
                    <span>⚠️ Lỗi kết nối trợ lý ảo</span>
                </div>
                <div class="hp-msg-text">
                    ${hpEscapeHtml(err.message || 'Không thể kết nối đến máy chủ AI.')}
                    <br><br>Vui lòng thử lại sau vài giây hoặc kiểm tra kết nối mạng.
                </div>
            </div>
        `;
        messages.appendChild(errRow);
    } finally {
        hpIsSending = false;
        if (sendBtn) sendBtn.disabled = false;
        messages.scrollTop = messages.scrollHeight;
        if (input) input.focus();
    }
}
