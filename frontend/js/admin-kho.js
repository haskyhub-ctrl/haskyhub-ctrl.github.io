/**
 * Kho tài liệu AI (admin): tải tài liệu, phân tầng, bật tắt hiệu lực; hàng chờ câu hỏi khó và đáp án chuẩn.
 */
(function () {
    const esc = (v) => String(v ?? '').replace(/[&<>"']/g, ch => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[ch]));
    const num = (n) => Number(n || 0).toLocaleString('vi-VN');
    const debounce = (fn, ms) => { let t; return (...a) => { clearTimeout(t); t = setTimeout(() => fn(...a), ms); }; };
    const fmtDT = (iso) => iso ? new Date(/[zZ]|[+-]\d\d:\d\d$/.test(iso) ? iso : iso + 'Z').toLocaleString('vi-VN', { hour12: false }) : '';

    function msg(el, text, cls) { el.textContent = text || ''; el.className = 'kho-msg ' + (cls || ''); }
    function token() { return localStorage.getItem('fras_token') || ''; }

    const KHO = {
        logsData: [],
        logsFilter: 'all',
        logsSearch: '',
        activeLogItem: null,
        searchTimer: null,
        showFullContent: true,
        expandedRows: {},

        init() {
            if (!requireAuth()) return;
            const u = api.getUser();
            if (!u || (u.role !== 'admin' && u.role !== 'superadmin')) { window.location.href = '/dashboard.html'; return; }
            this.loadDocs();
            this.loadQs();
            this.loadWatch();
            this.loadFaqAuditStatus();

            const urlParams = new URLSearchParams(window.location.search);
            const initialTab = urlParams.get('tab');
            if (initialTab) {
                this.tab(initialTab);
            }
        },
        tab(name) {
            ['docs', 'qs', 'logs', 'qa', 'watch', 'test'].forEach(t => {
                const elT = document.getElementById('kt-' + t);
                const elP = document.getElementById('kp-' + t);
                if (elT) elT.classList.toggle('active', t === name);
                if (elP) elP.style.display = t === name ? '' : 'none';
            });
            if (name === 'logs') this.loadLogs();
            if (name === 'qa') this.loadQaReports();
        },

        // ------------------------------------------------------------ báo cáo vòng lặp rà soát
        async loadQaReports() {
            const sel = document.getElementById('qa-select');
            try {
                const d = await api.get('/admin/kho/qa-reports');
                if (!d.reports.length) { sel.innerHTML = ''; document.getElementById('qa-report').innerHTML = '<p>Chưa có báo cáo nào.</p>'; return; }
                sel.innerHTML = d.reports.map(r => `<option value="${r.id}">${r.id.slice(6, 8)}/${r.id.slice(4, 6)}/${r.id.slice(0, 4)}</option>`).join('');
                this.loadQaReport(d.reports[0].id);
            } catch (e) { document.getElementById('qa-report').innerHTML = '<p>Không tải được báo cáo.</p>'; }
        },
        async loadQaReport(id) {
            const box = document.getElementById('qa-report');
            try {
                const d = await api.get('/admin/kho/qa-reports/' + id);
                const inline = (t) => esc(t).replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>').replace(/`([^`]+)`/g, '<code>$1</code>');
                let html = '', inList = false;
                for (const line of d.markdown.split(/\r?\n/)) {
                    const li = line.match(/^\s*[-*]\s+(.*)$/);
                    if (li) { if (!inList) { html += '<ul>'; inList = true; } html += '<li>' + inline(li[1]) + '</li>'; continue; }
                    if (inList) { html += '</ul>'; inList = false; }
                    const h = line.match(/^(#{1,3})\s+(.*)$/);
                    if (h) html += h[1].length === 1 ? '<h1>' + inline(h[2]) + '</h1>' : '<h2>' + inline(h[2]) + '</h2>';
                    else if (line.trim()) html += '<p>' + inline(line) + '</p>';
                }
                if (inList) html += '</ul>';
                box.innerHTML = html;
            } catch (e) { box.innerHTML = '<p>Không tải được báo cáo.</p>'; }
        },

        // ------------------------------------------------------------ tài liệu
        async loadDocs() {
            const body = document.getElementById('kd-body');
            try {
                const d = await api.get('/admin/kho/docs');
                const tiers = d.tiers;
                body.innerHTML = d.docs.length ? d.docs.map(x => `
                    <tr>
                        <td><span class="kd-title">${esc(x.title)}</span><span class="kd-sub">${esc(x.original_name || '')} · ${Math.round(x.size / 1024).toLocaleString('vi-VN')} KB · tải lên ${fmtDT(x.uploaded_at)}</span></td>
                        <td><select class="kd-tier" onchange="KHO.setTier('${x.id}', this.value)">
                            ${Object.keys(tiers).map(k => `<option value="${k}" ${String(x.tier) === k ? 'selected' : ''}>Tầng ${k}: ${esc(tiers[k])}</option>`).join('')}
                        </select></td>
                        <td><button class="kd-status ${x.status === 'active' ? 'on' : 'off'}" onclick="KHO.toggle('${x.id}', '${x.status}')">${x.status === 'active' ? 'Đang dùng' : 'Không dùng'}</button></td>
                        <td>${esc(x.effective_date)}</td>
                        <td class="tm-num">${num(x.chunks)}</td>
                        <td>${esc(x.note)}${x.needs_ocr ? ' <b style="color:#B91C1C;">Bản quét, chưa đọc được chữ</b>' : ''}</td>
                        <td>${x.id.endsWith('.txt') ? `<button class="kd-link" onclick="KHO.openDoc('${x.id}')">Xem, sửa</button>` : ''}<button class="kd-del" onclick="KHO.removeDoc('${x.id}')">Xóa</button></td>
                    </tr>`).join('') : '<tr><td colspan="7" class="tm-empty">Chưa có tài liệu nào được tải lên.</td></tr>';
                document.getElementById('kd-builtin').textContent = d.builtin.length
                    ? `Ngoài ra Trợ lý còn dùng ${d.builtin.length} tài liệu có sẵn trong hệ thống (tầng 2): ${d.builtin.join(', ')}`
                    : '';
                document.getElementById('kho-status').textContent = `${d.docs.filter(x => x.status === 'active').length}/${d.docs.length} tài liệu tải lên đang dùng`;
            } catch (e) {
                body.innerHTML = `<tr><td colspan="7" class="tm-empty">Không tải được: ${esc(e.message || e)}</td></tr>`;
            }
        },
        async upload() {
            const out = document.getElementById('kd-msg');
            const f = document.getElementById('kd-file').files[0];
            if (!f) { msg(out, 'Hãy chọn một tệp.', 'err'); return; }
            const fd = new FormData();
            fd.append('file', f);
            fd.append('title', document.getElementById('kd-title').value);
            fd.append('tier', document.getElementById('kd-tier').value);
            fd.append('status', 'active');
            fd.append('effective_date', document.getElementById('kd-date').value);
            fd.append('note', document.getElementById('kd-note').value);
            msg(out, 'Đang tải lên và lập chỉ mục, vui lòng chờ...', '');
            try {
                const res = await fetch(`${window.location.origin}/api/admin/kho/docs`, { method: 'POST', headers: { Authorization: 'Bearer ' + token() }, body: fd });
                const j = await res.json().catch(() => ({}));
                if (!res.ok) throw new Error(j.detail || ('Lỗi mã ' + res.status));
                msg(out, j.warning ? 'Đã tải lên. ' + j.warning : `Đã tải lên và lập chỉ mục (${num(j.doc.chunks)} đoạn).`, j.warning ? 'warn' : 'ok');
                ['kd-file', 'kd-title', 'kd-date', 'kd-note'].forEach(id => { document.getElementById(id).value = ''; });
                this.loadDocs();
            } catch (e) { msg(out, e.message || String(e), 'err'); }
        },
        async setTier(id, tier) {
            try { await this.rawPatch(id, { tier: Number(tier) }); } catch (e) { alert(e.message || e); }
            this.loadDocs();
        },
        async toggle(id, cur) {
            try { await this.rawPatch(id, { status: cur === 'active' ? 'inactive' : 'active' }); } catch (e) { alert(e.message || e); }
            this.loadDocs();
        },
        async rawPatch(id, body) {
            const res = await fetch(`${window.location.origin}/api/admin/kho/docs/${id}`, {
                method: 'PATCH', headers: { Authorization: 'Bearer ' + token(), 'Content-Type': 'application/json' }, body: JSON.stringify(body),
            });
            const j = await res.json().catch(() => ({}));
            if (!res.ok) throw new Error(j.detail || ('Lỗi mã ' + res.status));
            return j;
        },
        async removeDoc(id) {
            if (!confirm('Xóa tài liệu này khỏi kho? Việc này không hoàn tác được.')) return;
            const res = await fetch(`${window.location.origin}/api/admin/kho/docs/${id}`, { method: 'DELETE', headers: { Authorization: 'Bearer ' + token() } });
            if (!res.ok) alert('Không xóa được (mã ' + res.status + ')');
            this.loadDocs();
        },

        // ------------------------------------------------------------ câu hỏi khó
        
        // ------------------------------------------------------------ faq audit 1 tuan/lan
        async loadFaqAuditStatus() {
            const el = document.getElementById('faq-audit-status');
            if (!el) return;
            try {
                const rep = await api.get('/ai/faq/audit');
                if (rep && rep.total_faqs) {
                    el.innerHTML = `Tổng số: <b>${rep.total_faqs}</b> câu chuẩn | Đạt chuẩn: <b style="color:#16a34a;">${rep.valid_count}</b> | Căn cứ cũ: <b style="color:#dc2626;">${rep.outdated_count}</b> | Cần rà soát tuần này: <b>${rep.due_review_count}</b> | Rà soát gần nhất: <em>${rep.timestamp}</em>`;
                } else {
                    el.textContent = 'Chưa có dữ liệu rà soát định kỳ.';
                }
            } catch (e) {
                el.textContent = 'Không tải được trạng thái rà soát.';
            }
        },
        async runFaqAudit() {
            const el = document.getElementById('faq-audit-status');
            if (el) el.textContent = 'Đang quét toàn bộ 200 câu hỏi và kiểm tra hiệu lực căn cứ pháp lý...';
            try {
                const rep = await api.post('/ai/faq/run-audit');
                alert(`Đã rà soát xong ${rep.total_faqs} câu hỏi!\n- Hợp lệ: ${rep.valid_count}\n- Chứa căn cứ cũ cần sửa: ${rep.outdated_count}\n- Quá 7 ngày cần rà soát: ${rep.due_review_count}`);
                this.loadFaqAuditStatus();
                this.loadQs();
            } catch (e) {
                alert('Lỗi rà soát: ' + (e.message || e));
            }
        },
        async seedFaq200() {
            if (!confirm('Bạn có chắc muốn đồng bộ và cập nhật lại 200 câu hỏi - đáp chuẩn PCCC 2026?')) return;
            try {
                const res = await api.post('/ai/faq/seed-200');
                alert(`Đã nạp thành công ${res.added} câu mới và cập nhật ${res.updated} câu chuẩn!`);
                this.loadFaqAuditStatus();
                this.loadQs();
            } catch (e) {
                alert('Lỗi đồng bộ: ' + (e.message || e));
            }
        },

        loadQsDebounced: debounce(function () { KHO.loadQs(); }, 350),
        async loadQs() {
            const st = document.getElementById('kq-status').value;
            const q = document.getElementById('kq-q').value.trim();
            const box = document.getElementById('kq-list');
            try {
                const d = await api.get(`/admin/kho/questions?status=${st}` + (q ? '&q=' + encodeURIComponent(q) : ''));
                document.getElementById('kho-pending').textContent = d.counts.pending;
                box.innerHTML = d.items.length ? d.items.map(r => `
                    <div class="kq-card ${r.status}" id="kq-${r.id}">
                        <div class="kq-q">${esc(r.question)}</div>
                        <div class="kq-meta">Đã được hỏi ${num(r.times_asked)} lần · gần nhất ${fmtDT(r.last_asked_at)} · ${r.source === 'admin' ? 'cán bộ nhập' : (r.source === 'feedback' ? 'người dùng báo chưa hài lòng' : 'bot chưa đủ căn cứ')}${r.status === 'approved' ? ' · đã duyệt' : ''}</div>
                        <textarea rows="4" id="kqa-${r.id}" placeholder="Đáp án chuẩn (theo văn bản hiện hành, ghi rõ căn cứ)...">${esc(r.answer)}</textarea>
                        <div class="kq-actions">
                            <button class="btn btn-primary btn-sm" onclick="KHO.saveQ('${r.id}', 'approved')">✔ Lưu và duyệt</button>
                            <button class="btn btn-secondary btn-sm" onclick="KHO.saveQ('${r.id}', 'rejected')">Bỏ qua</button>
                            <button class="btn btn-secondary btn-sm" onclick="KHO.saveQ('${r.id}', 'pending')">Trả về chờ</button>
                            <button class="kd-del" onclick="KHO.delQ('${r.id}')">Xóa</button>
                        </div>
                    </div>`).join('') : '<p class="tm-empty">Không có câu hỏi nào ở mục này.</p>';
            } catch (e) { box.innerHTML = `<p class="tm-empty">Không tải được: ${esc(e.message || e)}</p>`; }
        },
        async saveQ(id, status) {
            const answer = document.getElementById('kqa-' + id).value;
            try {
                await this.rawJson('PUT', `/admin/kho/questions/${id}`, { answer, status });
            } catch (e) { alert(e.message || e); return; }
            this.loadQs();
        },
        async delQ(id) {
            if (!confirm('Xóa câu hỏi này?')) return;
            await this.rawJson('DELETE', `/admin/kho/questions/${id}`);
            this.loadQs();
        },
        async addQ() {
            const q = document.getElementById('kq-new-q').value.trim();
            const a = document.getElementById('kq-new-a').value.trim();
            if (q.length < 6) { alert('Hãy nhập câu hỏi.'); return; }
            try {
                await this.rawJson('POST', '/admin/kho/questions', { question: q, answer: a });
                document.getElementById('kq-new-q').value = '';
                document.getElementById('kq-new-a').value = '';
                document.getElementById('kq-status').value = a ? 'approved' : 'pending';
                this.loadQs();
            } catch (e) { alert(e.message || e); }
        },
        async rawJson(method, path, body) {
            const res = await fetch(`${window.location.origin}/api${path}`, {
                method, headers: { Authorization: 'Bearer ' + token(), 'Content-Type': 'application/json' }, body: body ? JSON.stringify(body) : undefined,
            });
            const j = await res.json().catch(() => ({}));
            if (!res.ok) throw new Error(j.detail || ('Lỗi mã ' + res.status));
            return j;
        },

        // ------------------------------------------------------------ xem, sửa nội dung một tài liệu
        _openId: null,
        async openDoc(id) {
            try {
                const d = await api.get('/admin/kho/docs/' + id + '/text');
                this._openId = id;
                document.getElementById('kd-modal-title').textContent = d.title || id;
                document.getElementById('kd-modal-text').value = d.text;
                msg(document.getElementById('kd-modal-msg'), d.truncated ? 'Nội dung dài, chỉ hiển thị phần đầu, không nên sửa tài liệu này.' : '', 'warn');
                document.getElementById('kd-modal').style.display = 'flex';
            } catch (e) { alert(e.message || e); }
        },
        closeDoc() { document.getElementById('kd-modal').style.display = 'none'; this._openId = null; },
        async saveDoc(activate) {
            const out = document.getElementById('kd-modal-msg');
            try {
                await this.rawJson('PUT', `/admin/kho/docs/${this._openId}/text`, { text: document.getElementById('kd-modal-text').value });
                if (activate) await this.rawPatch(this._openId, { status: 'active' });
                msg(out, activate ? 'Đã lưu và bật dùng.' : 'Đã lưu.', 'ok');
                this.loadDocs();
                this.loadWiki();
            this.loadFaqAuditStatus();
            } catch (e) { msg(out, e.message || String(e), 'err'); }
        },

        // ------------------------------------------------------------ wiki tri thức
        _wikiTimer: null,
        async loadWiki() {
            const body = document.getElementById('kwi-body');
            try {
                const d = await api.get('/admin/kho/wiki');
                const label = { none: ['Chưa có', 'off'], draft: ['Nháp, chờ rà soát', 'off'], active: ['Đang dùng', 'on'] };
                body.innerHTML = d.topics.map(t => `
                    <tr>
                        <td><strong>${esc(t.title)}</strong></td>
                        <td><span class="kd-status ${label[t.state][1]}">${label[t.state][0]}</span></td>
                        <td class="tm-num">${t.chars ? num(t.chars) : ''}</td>
                        <td>
                            ${t.doc_id ? `<button class="kd-link" onclick="KHO.openDoc('${t.doc_id}')">Xem, sửa</button>
                                <button class="kd-link" onclick="KHO.toggle('${t.doc_id}', '${t.state === 'active' ? 'active' : 'inactive'}').then(() => KHO.loadWiki())">${t.state === 'active' ? 'Tắt' : 'Bật'}</button>` : ''}
                            <button class="kd-link" onclick="KHO.genWiki(['${t.slug}'])">${t.doc_id ? 'Biên soạn lại' : 'Biên soạn'}</button>
                        </td>
                    </tr>`).join('');
                const j = d.job || {};
                const jm = document.getElementById('kwi-job');
                if (j.running) {
                    jm.textContent = `Đang biên soạn ${j.done}/${j.total}: ${j.current}...`;
                    clearTimeout(this._wikiTimer);
                    this._wikiTimer = setTimeout(() => this.loadWiki(), 8000);
                } else {
                    jm.textContent = (j.errors && j.errors.length) ? 'Có lỗi: ' + j.errors.slice(0, 2).join(' | ') : '';
                }
            } catch (e) { body.innerHTML = `<tr><td colspan="4" class="tm-empty">Không tải được: ${esc(e.message || e)}</td></tr>`; }
        },
        async genWiki(slugs) {
            try {
                const r = await this.rawJson('POST', '/admin/kho/wiki/generate', slugs ? { slugs } : {});
                document.getElementById('kwi-job').textContent = r.message;
                setTimeout(() => this.loadWiki(), 4000);
            } catch (e) { alert(e.message || e); }
        },

        // ------------------------------------------------------------ văn bản mới theo dõi hằng tuần
        async loadWatch() {
            const st = document.getElementById('kw-status').value;
            const box = document.getElementById('kw-list');
            try {
                const d = await api.get('/admin/kho/watch?status=' + st);
                document.getElementById('kho-newcount').textContent = d.counts.new;
                const lr = d.last_run || {};
                document.getElementById('kw-last').textContent = lr.last_run ? `Lần tìm gần nhất: ${fmtDT(lr.last_run)} (tìm thấy ${lr.found || 0}, mới ${lr.new || 0}, liên quan ${lr.relevant || 0})` : 'Chưa chạy lần nào. Bấm Tìm ngay hoặc chờ sáng thứ Hai.';
                box.innerHTML = d.items.length ? d.items.map(r => `
                    <div class="kq-card ${r.status === 'new' ? '' : (r.status === 'ingested' ? 'approved' : 'rejected')}">
                        <div class="kq-q"><a href="${esc(r.url)}" target="_blank" rel="noopener" class="tm-link">${esc(r.title)}</a></div>
                        <div class="kq-meta">${esc(r.kind || 'Chưa phân loại')} · ${esc(r.source)}${r.published ? ' · ' + esc(r.published) : ''} · tìm thấy ${fmtDT(r.found_at)}</div>
                        ${r.summary ? `<p style="margin:0 0 6px;font-size:0.9rem;">${esc(r.summary)}</p>` : ''}
                        ${r.hint ? `<p style="margin:0 0 8px;font-size:0.82rem;color:#B45309;">Gợi ý: ${esc(r.hint)}</p>` : ''}
                        <div class="kq-actions">
                            ${r.status === 'new' ? `<button class="btn btn-primary btn-sm" onclick="KHO.watchAct('${r.id}','ingest',this)">📥 Nạp vào kho (nháp)</button>
                            <button class="btn btn-secondary btn-sm" onclick="KHO.watchAct('${r.id}','ignore',this)">Bỏ qua</button>` : ''}
                            ${r.status === 'ingested' ? '<span class="kho-msg ok">Đã nạp thành nháp. Vào mục Tài liệu để rà soát và bật.</span>' : ''}
                        </div>
                    </div>`).join('') : '<p class="tm-empty">Không có mục nào.</p>';
            } catch (e) { box.innerHTML = `<p class="tm-empty">Không tải được: ${esc(e.message || e)}</p>`; }
        },
        async runWatch() {
            try {
                const r = await this.rawJson('POST', '/admin/kho/watch/run');
                document.getElementById('kw-last').textContent = r.message;
                setTimeout(() => this.loadWatch(), 60000);
            } catch (e) { alert(e.message || e); }
        },
        async watchAct(id, act, btn) {
            if (btn) { btn.disabled = true; btn.textContent = 'Đang xử lý...'; }
            try {
                await this.rawJson('POST', `/admin/kho/watch/${id}/${act}`);
                if (act === 'ingest') this.loadDocs();
            } catch (e) { alert(e.message || e); }
            this.loadWatch();
        },

        // ------------------------------------------------------------ thử tra cứu

        // ------------------------------------------------------------ nhat ky hoi dap
        renderMarkdown(md) {
            if (!md) return '';
            const lines = String(md).split(/\r?\n/);
            let out = [];
            let inList = false;
            let listType = null;
            let inTable = false;
            let tableHeadDone = false;

            const inline = (t) => {
                let s = esc(t);
                // Bold: **text**
                s = s.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
                // Code / Cite: {{Điều ...}}
                s = s.replace(/\{\{([^}]+)\}\}/g, '<span style="background:#EEF2FF; color:#4338CA; padding:2px 6px; border-radius:4px; font-size:0.78rem; font-weight:700; border:1px solid #C7D2FE;">$1</span>');
                // Backticks: `code`
                s = s.replace(/`([^`]+)`/g, '<code style="background:#F1F5F9; color:#0F172A; padding:2px 5px; border-radius:4px; font-size:0.82rem; font-family:monospace;">$1</code>');
                // Highlight important notes: !! text
                if (s.startsWith('!! ')) {
                    s = '<div style="background:#FEF2F2; border-left:4px solid #DC2626; padding:8px 12px; margin:6px 0; border-radius:4px; color:#991B1B; font-weight:600;">⚠️ ' + s.slice(3) + '</div>';
                }
                // Highlight conclusions: >> text
                else if (s.startsWith('&gt;&gt; ') || s.startsWith('>> ')) {
                    const txt = s.replace(/^(&gt;&gt;|\>\>)\s*/, '');
                    s = '<div style="background:#EFF6FF; border-left:4px solid #2563EB; padding:8px 12px; margin:6px 0; border-radius:6px; color:#1E3A8A; font-weight:600; line-height:1.5;">💡 ' + txt + '</div>';
                }
                return s;
            };

            for (let i = 0; i < lines.length; i++) {
                const line = lines[i];
                const trimmed = line.trim();

                // Markdown Table detection: | cell | cell |
                if (trimmed.startsWith('|') && trimmed.endsWith('|')) {
                    if (inList) { out.push(listType === 'ol' ? '</ol>' : '</ul>'); inList = false; }
                    if (!inTable) {
                        out.push('<div style="overflow-x:auto; margin:8px 0;"><table style="width:100%; border-collapse:collapse; font-size:0.82rem; background:#fff; border:1px solid #CBD5E1;">');
                        inTable = true;
                        tableHeadDone = false;
                    }
                    if (trimmed.match(/^\|[\s\-:|]+\|$/)) {
                        tableHeadDone = true;
                        continue;
                    }
                    const cells = trimmed.slice(1, -1).split('|').map(c => c.trim());
                    if (!tableHeadDone) {
                        out.push('<tr style="background:#F1F5F9; border-bottom:2px solid #CBD5E1; font-weight:700; color:#0F2347;">' + cells.map(c => `<th style="padding:6px 8px; border:1px solid #CBD5E1; text-align:left;">${inline(c)}</th>`).join('') + '</tr>');
                    } else {
                        out.push('<tr style="border-bottom:1px solid #E2E8F0;">' + cells.map(c => `<td style="padding:6px 8px; border:1px solid #E2E8F0; color:#334155; line-height:1.45;">${inline(c)}</td>`).join('') + '</tr>');
                    }
                    continue;
                } else if (inTable) {
                    out.push('</table></div>');
                    inTable = false;
                }

                // Headings: ## Heading
                const hMatch = trimmed.match(/^(#{1,4})\s+(.*)$/);
                if (hMatch) {
                    if (inList) { out.push(listType === 'ol' ? '</ol>' : '</ul>'); inList = false; }
                    const lvl = hMatch[1].length;
                    const hText = inline(hMatch[2]);
                    if (lvl <= 2) {
                        out.push(`<h4 style="margin:12px 0 4px; color:#0F2347; font-size:0.92rem; font-weight:700; border-bottom:1px solid #E2E8F0; padding-bottom:3px;">${hText}</h4>`);
                    } else {
                        out.push(`<h5 style="margin:8px 0 3px; color:#1E3A8A; font-size:0.86rem; font-weight:700;">${hText}</h5>`);
                    }
                    continue;
                }

                // Bullet list: - or *
                const liMatch = trimmed.match(/^[-*]\s+(.*)$/);
                if (liMatch) {
                    if (!inList || listType !== 'ul') {
                        if (inList) out.push(listType === 'ol' ? '</ol>' : '</ul>');
                        out.push('<ul style="margin:4px 0 6px 18px; padding:0; line-height:1.5;">');
                        inList = true;
                        listType = 'ul';
                    }
                    out.push(`<li style="margin-bottom:3px; color:#334155;">${inline(liMatch[1])}</li>`);
                    continue;
                }

                // Numbered list: 1.
                const numMatch = trimmed.match(/^(\d+)\.\s+(.*)$/);
                if (numMatch) {
                    if (!inList || listType !== 'ol') {
                        if (inList) out.push(listType === 'ol' ? '</ol>' : '</ul>');
                        out.push('<ol style="margin:4px 0 6px 18px; padding:0; line-height:1.5;">');
                        inList = true;
                        listType = 'ol';
                    }
                    out.push(`<li style="margin-bottom:3px; color:#334155;">${inline(numMatch[2])}</li>`);
                    continue;
                }

                if (inList) {
                    out.push(listType === 'ol' ? '</ol>' : '</ul>');
                    inList = false;
                }

                if (!trimmed) {
                    continue;
                }

                // Regular line
                out.push(`<p style="margin:5px 0; color:#1E293B; line-height:1.55;">${inline(trimmed)}</p>`);
            }

            if (inList) out.push(listType === 'ol' ? '</ol>' : '</ul>');
            if (inTable) out.push('</table></div>');

            return out.join('');
        },

        toggleFullContent(checked) {
            this.showFullContent = !!checked;
            this.renderLogsTable();
        },

        toggleRowExpand(logId) {
            this.expandedRows[logId] = !this.expandedRows[logId];
            this.renderLogsTable();
        },

        copyQuestion() {
            if (!this.activeLogItem) return;
            navigator.clipboard.writeText(this.activeLogItem.question || '');
            alert('Đã sao chép toàn văn câu hỏi!');
        },

        insertSnippet(type) {
            const adjEl = document.getElementById('rev-adjusted-reply');
            if (!adjEl) return;
            const snippets = {
                nq66: 'Căn cứ Nghị quyết số 66.18/2026/NQ-CP và Nghị định số 347/2026/NĐ-CP sửa đổi, bổ sung Nghị định số 105/2025/NĐ-CP.\n',
                luat55: 'Căn cứ Luật Phòng cháy, chữa cháy và Cứu nạn, cứu hộ số 55/2024/QH15 (hiệu lực từ ngày 01/7/2025).\n',
                qcvn06: 'Căn cứ Quy chuẩn kỹ thuật quốc gia QCVN 06:2022/BXD (sửa đổi 1:2023) về an toàn cháy cho nhà và công trình.\n',
                nghiemthu: 'Lưu ý theo quy định pháp luật 2026: Đã bãi bỏ hoàn toàn thủ tục nộp hồ sơ xin chấp thuận kết quả nghiệm thu PCCC tại cơ quan Công an. Chủ cơ sở/chủ đầu tư tự tổ chức nghiệm thu, lập biên bản và cập nhật thông tin lên Hệ thống cơ sở dữ liệu PCCC.\n'
            };
            const textToInsert = snippets[type] || '';
            const start = adjEl.selectionStart || adjEl.value.length;
            const end = adjEl.selectionEnd || adjEl.value.length;
            adjEl.value = adjEl.value.substring(0, start) + textToInsert + adjEl.value.substring(end);
            adjEl.focus();
            const radios = document.getElementsByName('rev-status-choice');
            radios.forEach(r => { if (r.value === 'adjusted') r.checked = true; });
        },

        async quickVerify(logId) {
            try {
                await api.post('/ai/chat/history-logs/quick-verify', { log_id: logId });
                const item = this.logsData.find(x => x.id === logId);
                if (item) {
                    item.status = 'verified';
                    item.reviewed_at = new Date().toLocaleString('vi-VN');
                }
                const setC = (id, n) => { const el = document.getElementById(id); if (el) el.textContent = n || 0; };
                setC('count-log-pending', this.logsData.filter(x => !x.status || x.status === 'pending').length);
                setC('count-log-verified', this.logsData.filter(x => x.status === 'verified').length);
                this.renderLogsTable();
            } catch (e) {
                alert('Lỗi xác nhận: ' + (e.message || e));
            }
        },

        async loadLogs() {
            const body = document.getElementById('kl-body');
            body.innerHTML = '<tr><td colspan="7" class="tm-empty"><div class="loading-spinner"></div> Đang tải dữ liệu nhật ký...</td></tr>';
            try {
                const res = await api.get('/ai/chat/history-logs?limit=500&format=envelope');
                if (res && res.items) {
                    this.logsData = res.items;
                    if (res.counts) {
                        const setC = (id, n) => { const el = document.getElementById(id); if (el) el.textContent = n || 0; };
                        setC('count-log-all', res.counts.total);
                        setC('count-log-pending', res.counts.pending);
                        setC('count-log-verified', res.counts.verified);
                        setC('count-log-adjusted', res.counts.adjusted);
                    }
                } else if (Array.isArray(res)) {
                    this.logsData = res;
                    const setC = (id, n) => { const el = document.getElementById(id); if (el) el.textContent = n || 0; };
                    setC('count-log-all', res.length);
                    setC('count-log-pending', res.filter(x => !x.status || x.status === 'pending').length);
                    setC('count-log-verified', res.filter(x => x.status === 'verified').length);
                    setC('count-log-adjusted', res.filter(x => x.status === 'adjusted').length);
                } else {
                    this.logsData = [];
                }
                this.renderLogsTable();
            } catch (e) {
                body.innerHTML = '<tr><td colspan="7" class="tm-empty">Lỗi tải nhật ký hỏi đáp: ' + esc(e.message || e) + '</td></tr>';
            }
        },

        filterLogStatus(st) {
            this.logsFilter = st;
            ['all', 'pending', 'verified', 'adjusted'].forEach(s => {
                const btn = document.getElementById('chip-status-' + s);
                if (btn) btn.classList.toggle('active', s === st);
            });
            this.renderLogsTable();
        },

        searchLogsDebounced() {
            clearTimeout(this.searchTimer);
            this.searchTimer = setTimeout(() => {
                const el = document.getElementById('log-search-input');
                this.logsSearch = el ? el.value.trim().toLowerCase() : '';
                this.renderLogsTable();
            }, 250);
        },

        renderLogsTable() {
            const body = document.getElementById('kl-body');
            if (!this.logsData || !this.logsData.length) {
                body.innerHTML = '<tr><td colspan="7" class="tm-empty">Chưa có lượt hỏi đáp nào được ghi nhận.</td></tr>';
                return;
            }

            let filtered = this.logsData;
            if (this.logsFilter !== 'all') {
                if (this.logsFilter === 'pending') {
                    filtered = filtered.filter(x => !x.status || x.status === 'pending');
                } else {
                    filtered = filtered.filter(x => x.status === this.logsFilter);
                }
            }

            if (this.logsSearch) {
                const sq = this.logsSearch;
                filtered = filtered.filter(x =>
                    (x.question || '').toLowerCase().includes(sq) ||
                    (x.reply || '').toLowerCase().includes(sq) ||
                    (x.adjusted_reply || '').toLowerCase().includes(sq) ||
                    (x.user || '').toLowerCase().includes(sq)
                );
            }

            if (!filtered.length) {
                body.innerHTML = '<tr><td colspan="7" class="tm-empty">Không tìm thấy lượt hỏi đáp nào khớp với bộ lọc.</td></tr>';
                return;
            }

            body.innerHTML = filtered.map(x => {
                const logId = esc(x.id || '');
                const isExpanded = !!this.expandedRows[x.id];
                const isFull = this.showFullContent || isExpanded;

                let statusBadge = '<span style="background:#FEF3C7; color:#B45309; padding:3px 8px; border-radius:12px; font-size:0.72rem; font-weight:700; white-space:nowrap; border:1px solid #FDE68A;">⏳ Chưa rà soát</span>';
                if (x.status === 'verified') {
                    statusBadge = '<span style="background:#DCFCE7; color:#15803D; padding:3px 8px; border-radius:12px; font-size:0.72rem; font-weight:700; white-space:nowrap; border:1px solid #BBF7D0;">✅ Chuẩn 2026</span>';
                } else if (x.status === 'adjusted') {
                    statusBadge = '<span style="background:#DBEAFE; color:#1D4ED8; padding:3px 8px; border-radius:12px; font-size:0.72rem; font-weight:700; white-space:nowrap; border:1px solid #BFDBFE;">✏️ Đã chỉnh</span>';
                }

                const isAdjusted = !!x.adjusted_reply;

                return `
                    <tr style="cursor:pointer;" onclick="KHO.openReviewModal('${logId}')" title="Bấm để mở cửa sổ rà soát chi tiết">
                        <td style="font-size:0.74rem; color:#64748b; white-space:nowrap; vertical-align:top; padding-top:10px;">${esc(x.time)}</td>
                        <td style="font-size:0.75rem; color:#334155; font-weight:500; vertical-align:top; padding-top:10px;">${esc(x.user)}</td>
                        <td style="font-weight:600; color:#0F2347; font-size:0.84rem; vertical-align:top; line-height:1.5; padding-top:10px;">
                            <div style="${isFull ? 'white-space:pre-wrap; word-break:break-word;' : 'max-height:85px; overflow:hidden; text-overflow:ellipsis; display:-webkit-box; -webkit-line-clamp:3; -webkit-box-orient:vertical;'}">
                                ${esc(x.question)}
                            </div>
                            ${!this.showFullContent ? `<button type="button" class="btn btn-link btn-sm" style="padding:0; font-size:0.72rem; color:#2563EB; margin-top:4px;" onclick="event.stopPropagation(); KHO.toggleRowExpand('${logId}')">${isExpanded ? '▲ Thu gọn câu hỏi' : '▼ Xem toàn văn'}</button>` : ''}
                        </td>
                        <td style="font-size:0.83rem; line-height:1.55; vertical-align:top; padding-top:10px;">
                            ${isAdjusted ? `
                                <div style="background:#EFF6FF; border:1px solid #BFDBFE; border-radius:6px; padding:8px 12px; margin-bottom:8px;">
                                    <span style="color:#1D4ED8; font-size:0.72rem; font-weight:700; display:flex; align-items:center; gap:4px; margin-bottom:4px;">
                                        ✏️ CÁN BỘ ĐÃ ĐIỀU CHỈNH CHUẨN XÁC:
                                    </span>
                                    <div style="${isFull ? '' : 'max-height:130px; overflow:hidden;'}">
                                        ${this.renderMarkdown(x.adjusted_reply)}
                                    </div>
                                </div>
                                <details style="font-size:0.76rem; color:#64748B; margin-top:4px;" onclick="event.stopPropagation()">
                                    <summary style="cursor:pointer; font-weight:600; color:#475569;">👁️ Xem câu trả lời gốc của AI</summary>
                                    <div style="margin-top:6px; padding:8px; background:#F8FAFC; border-radius:4px; border:1px solid #E2E8F0;">
                                        ${this.renderMarkdown(x.reply)}
                                    </div>
                                </details>
                            ` : `
                                <div style="${isFull ? '' : 'max-height:120px; overflow:hidden; text-overflow:ellipsis; display:-webkit-box; -webkit-line-clamp:4; -webkit-box-orient:vertical; color:#334155;'}">
                                    ${this.renderMarkdown(x.reply)}
                                </div>
                            `}
                            ${!this.showFullContent && !isAdjusted ? `<button type="button" class="btn btn-link btn-sm" style="padding:0; font-size:0.72rem; color:#2563EB; margin-top:4px;" onclick="event.stopPropagation(); KHO.toggleRowExpand('${logId}')">${isExpanded ? '▲ Thu gọn câu trả lời' : '▼ Xem toàn văn câu trả lời'}</button>` : ''}
                        </td>
                        <td style="text-align:center; vertical-align:top; padding-top:10px;">${statusBadge}</td>
                        <td style="text-align:center; vertical-align:top; padding-top:10px;"><span class="fras-source-badge ${esc(x.source_type)}" style="font-size:0.7rem;">${esc(x.source_type)}</span></td>
                        <td style="text-align:center; vertical-align:top; padding-top:10px;" onclick="event.stopPropagation()">
                            <div style="display:flex; flex-direction:column; gap:5px; align-items:center;">
                                <button class="btn btn-primary btn-sm" style="font-size:0.72rem; padding:4px 8px; width:100%; white-space:nowrap;" onclick="KHO.openReviewModal('${logId}')">🔍 Rà soát & Sửa</button>
                                ${x.status !== 'verified' ? `<button class="btn btn-secondary btn-sm" style="font-size:0.7rem; padding:3px 6px; width:100%; color:#15803D; background:#F0FDF4; border-color:#BBF7D0; font-weight:600;" onclick="KHO.quickVerify('${logId}')" title="Xác nhận câu trả lời đã đúng chuẩn quy định 2026">⚡ Duyệt chuẩn</button>` : ''}
                            </div>
                        </td>
                    </tr>
                `;
            }).join('');
        },

        openReviewModal(logId) {
            const item = this.logsData.find(x => x.id === logId);
            if (!item) return;
            this.activeLogItem = item;

            const setText = (id, txt) => { const el = document.getElementById(id); if (el) el.textContent = txt || '-'; };
            setText('rev-time', item.time);
            setText('rev-user', item.user);
            setText('rev-source', item.source_type || 'docs');
            setText('rev-latency', item.elapsed_seconds ? item.elapsed_seconds + 's' : '-');
            setText('rev-model', item.model || 'openrouter/nvidia/nemotron-3-ultra-550b-a55b:free');

            const qEl = document.getElementById('rev-question');
            if (qEl) qEl.textContent = item.question || '';

            const rEl = document.getElementById('rev-reply');
            if (rEl) rEl.innerHTML = this.renderMarkdown(item.reply || '(Không có nội dung)');

            const radios = document.getElementsByName('rev-status-choice');
            const curStatus = item.status || 'verified';
            radios.forEach(r => { r.checked = (r.value === curStatus); });

            const adjEl = document.getElementById('rev-adjusted-reply');
            if (adjEl) adjEl.value = item.adjusted_reply || (curStatus === 'adjusted' ? item.reply : '');

            const noteEl = document.getElementById('rev-note');
            if (noteEl) noteEl.value = item.review_note || '';

            const msgEl = document.getElementById('rev-save-msg');
            if (msgEl) { msgEl.textContent = ''; msgEl.className = ''; }

            const modal = document.getElementById('modal-review-log');
            if (modal) modal.style.display = 'flex';
        },

        closeReviewModal() {
            const modal = document.getElementById('modal-review-log');
            if (modal) modal.style.display = 'none';
            this.activeLogItem = null;
        },

        copyAiReplyToEditor() {
            if (!this.activeLogItem) return;
            const adjEl = document.getElementById('rev-adjusted-reply');
            if (adjEl) {
                adjEl.value = this.activeLogItem.reply || '';
                adjEl.focus();
            }
            const radios = document.getElementsByName('rev-status-choice');
            radios.forEach(r => { if (r.value === 'adjusted') r.checked = true; });
        },

        onStatusChoiceChange(val) {
            const adjEl = document.getElementById('rev-adjusted-reply');
            if (val === 'adjusted' && adjEl && !adjEl.value.trim() && this.activeLogItem) {
                adjEl.value = this.activeLogItem.reply || '';
            }
        },

        async saveReview() {
            if (!this.activeLogItem) return;
            const logId = this.activeLogItem.id;

            let chosenStatus = 'verified';
            const radios = document.getElementsByName('rev-status-choice');
            radios.forEach(r => { if (r.checked) chosenStatus = r.value; });

            const adjReply = (document.getElementById('rev-adjusted-reply')?.value || '').trim();
            const note = (document.getElementById('rev-note')?.value || '').trim();
            const promoteFaq = !!document.getElementById('rev-promote-faq')?.checked;

            if (chosenStatus === 'adjusted' && !adjReply) {
                alert('Vui lòng nhập nội dung câu trả lời chuẩn sau khi cán bộ điều chỉnh.');
                return;
            }

            const btn = document.getElementById('btn-save-review');
            const msgEl = document.getElementById('rev-save-msg');
            if (btn) btn.disabled = true;
            if (msgEl) { msgEl.textContent = 'Đang lưu đánh giá...'; msgEl.style.color = '#2563EB'; }

            try {
                const res = await api.post('/ai/chat/history-logs/review', {
                    log_id: logId,
                    status: chosenStatus,
                    adjusted_reply: adjReply,
                    review_note: note,
                    promote_to_faq: promoteFaq
                });

                if (msgEl) {
                    msgEl.textContent = '✅ ' + (res.message || 'Đã lưu thành công!');
                    msgEl.style.color = '#15803D';
                }

                // Cập nhật lại bản ghi trong mảng dữ liệu client
                this.activeLogItem.status = chosenStatus;
                this.activeLogItem.adjusted_reply = adjReply;
                this.activeLogItem.review_note = note;
                this.activeLogItem.reviewed_at = new Date().toLocaleString('vi-VN');

                // Cập nhật lại số đếm
                const setC = (id, n) => { const el = document.getElementById(id); if (el) el.textContent = n || 0; };
                setC('count-log-pending', this.logsData.filter(x => !x.status || x.status === 'pending').length);
                setC('count-log-verified', this.logsData.filter(x => x.status === 'verified').length);
                setC('count-log-adjusted', this.logsData.filter(x => x.status === 'adjusted').length);

                this.renderLogsTable();

                setTimeout(() => {
                    this.closeReviewModal();
                }, 1000);
            } catch (err) {
                if (msgEl) {
                    msgEl.textContent = '❌ Lỗi: ' + (err.message || err);
                    msgEl.style.color = '#DC2626';
                }
            } finally {
                if (btn) btn.disabled = false;
            }
        },

        promoteToApproved(encQ, encA) {
            const q = decodeURIComponent(encQ);
            const a = decodeURIComponent(encA);
            this.tab('qs');
            document.getElementById('kq-new-q').value = q;
            document.getElementById('kq-new-a').value = a;
            document.getElementById('kq-new-q').scrollIntoView({ behavior: 'smooth' });
        },

        async test() {
            const q = document.getElementById('kt-q').value.trim();
            const box = document.getElementById('kt-result');
            if (q.length < 2) return;
            box.innerHTML = '<p class="tm-empty">Đang tra cứu...</p>';
            try {
                const hits = await api.get('/admin/kho/test-search?q=' + encodeURIComponent(q));
                box.innerHTML = hits.length ? hits.map(h => `
                    <div class="kt-hit"><small>${esc(h.tier)} · điểm ${h.score}</small><b>${esc(h.source)}</b><br>${esc(h.text)}...</div>`).join('')
                    : '<p class="tm-empty">Không tìm thấy căn cứ nào trong kho cho câu hỏi này. Trợ lý ảo sẽ phải trả lời từ nguồn ngoài, nên nên bổ sung tài liệu hoặc đáp án chuẩn.</p>';
            } catch (e) { box.innerHTML = `<p class="tm-empty">Lỗi: ${esc(e.message || e)}</p>`; }
        },
    };
    window.KHO = KHO;
})();
