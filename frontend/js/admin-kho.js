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
        init() {
            if (!requireAuth()) return;
            const u = api.getUser();
            if (!u || (u.role !== 'admin' && u.role !== 'superadmin')) { window.location.href = '/dashboard.html'; return; }
            this.loadDocs();
            this.loadQs();
            this.loadWatch();
            this.loadWiki();
        },
        tab(name) {
            ['docs', 'qs', 'wiki', 'watch', 'test'].forEach(t => {
                document.getElementById('kt-' + t).classList.toggle('active', t === name);
                document.getElementById('kp-' + t).style.display = t === name ? '' : 'none';
            });
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
