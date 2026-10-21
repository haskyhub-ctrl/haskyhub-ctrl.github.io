/**
 * Bảng theo dõi khảo sát theo đội quản lý (admin).
 * TM: trang tổng quan (admin/teams.html). TD: trang danh sách cơ sở của một đội (admin/team.html).
 * Dữ liệu tự làm mới định kỳ nên admin xem được số liệu gần realtime.
 */
(function () {
    const esc = (v) => String(v ?? '').replace(/[&<>"']/g, ch => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[ch]));
    const num = (n) => Number(n || 0).toLocaleString('vi-VN');
    const toDate = (iso) => iso ? new Date(iso.endsWith('Z') || /[+-]\d\d:\d\d$/.test(iso) ? iso : iso + 'Z') : null;
    const fmtDT = (iso) => { const d = toDate(iso); return d ? d.toLocaleString('vi-VN', { hour12: false }) : ''; };
    const fmtTime = (d) => d.toLocaleTimeString('vi-VN', { hour12: false });
    const debounce = (fn, ms) => { let t; return (...a) => { clearTimeout(t); t = setTimeout(() => fn(...a), ms); }; };

    function bar(pct) {
        const p = Math.max(0, Math.min(100, Number(pct) || 0));
        const cls = p >= 60 ? '' : p >= 25 ? 'mid' : 'low';
        return `<div class="tm-bar"><div class="track"><div class="fill ${cls}" style="width:${p}%"></div></div><span class="pct">${p.toFixed(1)}%</span></div>`;
    }
    function kpi(label, value, sub, cls) {
        return `<div class="tm-kpi ${cls || ''}"><div class="lbl">${label}</div><div class="val">${value}</div>${sub ? `<div class="sub">${sub}</div>` : ''}</div>`;
    }
    function guard() {
        if (!requireAuth()) return false;
        const u = api.getUser();
        if (!u || (u.role !== 'admin' && u.role !== 'superadmin')) { window.location.href = '/dashboard.html'; return false; }
        return true;
    }
    function fillWardSelect(sel, wards, keep) {
        const cur = keep ?? sel.value;
        sel.innerHTML = '<option value="">Tất cả xã phường</option>' +
            wards.map(w => `<option value="${esc(w.value)}">${esc(w.ward)} (${num(w.participated)}/${num(w.total)})</option>`).join('');
        sel.value = [...sel.options].some(o => o.value === cur) ? cur : '';
    }

    // ------------------------------------------------------------------ TRANG TỔNG QUAN
    const TM = {
        timer: null, data: null,
        init() {
            if (!guard()) return;
            const p = new URLSearchParams(location.search);
            if (p.get('q')) document.getElementById('tm-q').value = p.get('q');
            this.pendingWard = p.get('ward') || '';
            this.load();
            this.setAuto(true);
        },
        setAuto(on) {
            clearInterval(this.timer);
            if (on) this.timer = setInterval(() => this.load(), 20000);
        },
        params() {
            const q = new URLSearchParams();
            const w = document.getElementById('tm-ward').value;
            const t = document.getElementById('tm-q').value.trim();
            const g = document.getElementById('tm-group').value;
            const tm = document.getElementById('tm-team').value;
            if (w) q.set('ward', w);
            if (t) q.set('q', t);
            if (g) q.set('group', g);
            if (tm) q.set('team', tm);
            q.set('sort', document.getElementById('tm-sort').value);
            return q.toString();
        },
        onFilter() { this.load(true); },
        onFilterDebounced: debounce(function () { TM.load(true); }, 350),
        clear() {
            ['tm-ward', 'tm-q', 'tm-group', 'tm-team'].forEach(id => { document.getElementById(id).value = ''; });
            document.getElementById('tm-sort').value = 'percent';
            this.load(true);
        },
        async exportXlsx() {
            try {
                const res = await fetch(`${window.location.origin}/api/admin/teams/overview/export?${this.params()}`, {
                    headers: { Authorization: 'Bearer ' + (localStorage.getItem('fras_token') || '') },
                });
                if (!res.ok) throw new Error('Không xuất được (mã ' + res.status + ')');
                const a = document.createElement('a');
                a.href = URL.createObjectURL(await res.blob());
                a.download = 'Theo_doi_khao_sat_' + new Date().toISOString().slice(0, 10) + '.xlsx';
                document.body.appendChild(a); a.click(); a.remove();
            } catch (e) { alert(e.message || e); }
        },
        fillTeams(teams) {
            const sel = document.getElementById('tm-team');
            if (sel.value) return;
            const names = teams.map(t => t.team).sort((a, b) => a.localeCompare(b, 'vi'));
            sel.innerHTML = '<option value="">Tất cả các đội</option>' + names.map(n => `<option value="${esc(n)}">${esc(n)}</option>`).join('');
        },
        tab(name) {
            ['teams', 'wards'].forEach(t => {
                document.getElementById('tab-' + t).classList.toggle('active', t === name);
                document.getElementById('tm-wrap-' + t).style.display = t === name ? '' : 'none';
            });
        },
        async load(showSpinner) {
            const upd = document.getElementById('tm-updated');
            try {
                if (this.pendingWard) { document.getElementById('tm-ward').dataset.want = this.pendingWard; }
                const qs = this.params();
                const d = await api.get('/admin/teams/overview' + (qs ? '?' + qs : ''));
                this.data = d;
                const sel = document.getElementById('tm-ward');
                const want = this.pendingWard || sel.value;
                fillWardSelect(sel, d.wards, want);
                if (this.pendingWard) { this.pendingWard = ''; if (sel.value) return this.load(); }
                this.fillTeams(d.teams);
                this.render(d);
                upd.textContent = 'Cập nhật lúc ' + fmtTime(new Date());
            } catch (e) {
                upd.textContent = 'Lỗi tải dữ liệu: ' + (e.message || e);
            }
        },
        render(d) {
            const t = d.totals;
            document.getElementById('tm-kpis').innerHTML =
                kpi('Tổng số cơ sở', num(t.facilities), num(t.teams) + ' đội quản lý') +
                kpi('Đã khảo sát', num(t.participated), 'cơ sở đã hoàn thành ít nhất 1 bài', 'green') +
                kpi('Chưa khảo sát', num(t.remaining), 'cần đôn đốc', 'red') +
                kpi('Tỷ lệ tham gia', t.percent.toFixed(1) + '%', '', 'gold') +
                kpi('Nguy cơ cao, rất cao', num(t.high_risk), 'theo bài khảo sát gần nhất', 'red') +
                kpi('Khảo sát trong 24 giờ qua', num(t.last_24h), 'cơ sở', '');
            const ward = document.getElementById('tm-ward').value;
            const wq = ward ? '&ward=' + encodeURIComponent(ward) : '';
            document.getElementById('tm-teams').innerHTML = d.teams.length ? d.teams.map((x, i) => `
                <tr>
                    <td>${i + 1}</td>
                    <td><a class="tm-link" href="/admin/team.html?team=${encodeURIComponent(x.team)}${wq}">${esc(x.team)}</a></td>
                    <td>${esc(x.group_label)}</td>
                    <td class="tm-num">${num(x.total)}</td>
                    <td class="tm-num"><strong>${num(x.participated)}</strong></td>
                    <td class="tm-num">${num(x.remaining)}</td>
                    <td>${bar(x.percent)}</td>
                    <td class="tm-num">${num(x.high_risk)}</td>
                    <td>${x.last_survey_at ? fmtDT(x.last_survey_at) : '<span style="color:#94a3b8;">Chưa có</span>'}</td>
                    <td><a class="tm-link" href="/admin/team.html?team=${encodeURIComponent(x.team)}${wq}">Xem danh sách →</a></td>
                </tr>`).join('') : '<tr><td colspan="10" class="tm-empty">Không có đội nào khớp bộ lọc.</td></tr>';
            document.getElementById('tm-wards').innerHTML = d.wards.map((w, i) => `
                <tr class="tm-row-click" onclick="TM.pickWard('${esc(w.value).replace(/'/g, '&#39;')}')">
                    <td>${i + 1}</td><td><strong>${esc(w.ward)}</strong></td>
                    <td class="tm-num">${num(w.total)}</td><td class="tm-num"><strong>${num(w.participated)}</strong></td>
                    <td>${bar(w.percent)}</td><td><span class="tm-link">Xem các đội →</span></td>
                </tr>`).join('');
        },
        pickWard(w) {
            document.getElementById('tm-ward').value = w;
            this.tab('teams');
            this.load(true);
        },
    };

    // ------------------------------------------------------------------ TRANG DANH SÁCH CƠ SỞ CỦA ĐỘI
    const TD = {
        timer: null, page: 1, pageSize: 50, team: '', lastTotal: 0,
        init() {
            if (!guard()) return;
            const p = new URLSearchParams(location.search);
            this.team = p.get('team') || '';
            if (!this.team) { window.location.href = '/admin/teams.html'; return; }
            this.pendingWard = p.get('ward') || '';
            document.getElementById('td-title').textContent = this.team;
            document.title = this.team + ' - FRAS Admin';
            this.load();
            this.setAuto(true);
        },
        setAuto(on) {
            clearInterval(this.timer);
            if (on) this.timer = setInterval(() => this.load(), 30000);
        },
        params(extra) {
            const q = new URLSearchParams({ team: this.team });
            const w = document.getElementById('td-ward').value || this.pendingWard;
            const st = document.getElementById('td-status').value;
            const s = document.getElementById('td-q').value.trim();
            if (w) q.set('ward', w);
            q.set('status', st);
            if (s) q.set('q', s);
            Object.entries(extra || {}).forEach(([k, v]) => q.set(k, v));
            return q;
        },
        onFilter() { this.page = 1; this.load(); },
        onFilterDebounced: debounce(function () { TD.page = 1; TD.load(); }, 350),
        goto(p) { this.page = p; this.load(); window.scrollTo({ top: 0, behavior: 'smooth' }); },
        async load() {
            const upd = document.getElementById('td-updated');
            try {
                const d = await api.get('/admin/teams/detail?' + this.params({ page: this.page, page_size: this.pageSize }).toString());
                const sel = document.getElementById('td-ward');
                fillWardSelect(sel, d.wards, sel.value || this.pendingWard);
                this.pendingWard = '';
                this.render(d);
                upd.textContent = 'Cập nhật lúc ' + fmtTime(new Date());
            } catch (e) {
                upd.textContent = 'Lỗi tải dữ liệu: ' + (e.message || e);
            }
        },
        render(d) {
            const s = d.summary;
            document.getElementById('td-kpis').innerHTML =
                kpi('Tổng số cơ sở của đội', num(s.total), document.getElementById('td-ward').value ? 'trong xã phường đang lọc' : '') +
                kpi('Đã khảo sát', num(s.participated), '', 'green') +
                kpi('Chưa khảo sát', num(s.remaining), '', 'red') +
                kpi('Tỷ lệ tham gia', s.percent.toFixed(1) + '%', '', 'gold');
            const start = (d.page - 1) * d.page_size;
            document.getElementById('td-body').innerHTML = d.items.length ? d.items.map((x, i) => `
                <tr>
                    <td>${start + i + 1}</td>
                    <td>${esc(x.code)}</td>
                    <td><strong>${esc(x.name)}</strong></td>
                    <td>${esc(x.ward)}</td>
                    <td>${esc(x.type_label)}</td>
                    <td><span class="tm-badge ${x.participated ? 'done' : 'todo'}">${x.participated ? 'Đã khảo sát' : 'Chưa khảo sát'}</span>${x.surveys > 1 ? ` <small>(${x.surveys} bài)</small>` : ''}</td>
                    <td>${x.participated ? `<span class="tm-badge r-${esc(x.risk_level)}">${esc(x.risk_label)}${x.risk_percentage != null ? ' ' + Number(x.risk_percentage).toFixed(1) + '%' : ''}</span>` : ''}</td>
                    <td>${x.completed_at ? fmtDT(x.completed_at) : ''}</td>
                    <td>${x.assessment_id ? `<a class="tm-link" href="/result.html?id=${esc(x.assessment_id)}" target="_blank">Xem kết quả</a>` : ''}</td>
                </tr>`).join('') : '<tr><td colspan="9" class="tm-empty">Không có cơ sở nào khớp bộ lọc.</td></tr>';
            const pages = Math.max(1, Math.ceil(d.total_items / d.page_size));
            document.getElementById('td-pager').innerHTML = `
                <span>Hiển thị ${d.total_items ? start + 1 : 0} - ${Math.min(start + d.page_size, d.total_items)} / ${num(d.total_items)} cơ sở</span>
                <span class="btns">
                    <button class="btn btn-secondary btn-sm" ${d.page <= 1 ? 'disabled' : ''} onclick="TD.goto(${d.page - 1})">← Trước</button>
                    <span style="align-self:center;">Trang ${d.page} / ${pages}</span>
                    <button class="btn btn-secondary btn-sm" ${d.page >= pages ? 'disabled' : ''} onclick="TD.goto(${d.page + 1})">Sau →</button>
                </span>`;
        },
        async exportCsv() {
            const q = this.params();
            q.delete('q');
            try {
                const res = await fetch(`${window.location.origin}/api/admin/teams/export?${q.toString()}`, {
                    headers: { Authorization: 'Bearer ' + (localStorage.getItem('fras_token') || '') },
                });
                if (!res.ok) throw new Error('Không tải được (mã ' + res.status + ')');
                const blob = await res.blob();
                const a = document.createElement('a');
                a.href = URL.createObjectURL(blob);
                a.download = 'DS_' + this.team.replace(/[^\w\u00C0-\u1EF9]+/g, '_') + '.xlsx';
                document.body.appendChild(a); a.click(); a.remove();
            } catch (e) { alert(e.message || e); }
        },
    };

    window.TM = TM;
    window.TD = TD;
})();
