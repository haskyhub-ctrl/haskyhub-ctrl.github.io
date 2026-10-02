/**
 * FRAS Admin JS
 * Admin dashboard functions
 */

async function initAdminDashboard() {
    if (!requireAuth()) return;
    const user = api.getUser();
    if (user.role !== 'admin' && user.role !== 'superadmin') {
        window.location.href = '/dashboard.html';
        return;
    }

    // Run all 3 independently — one failure won't block the others
    const [statsResult, logsResult, distResult] = await Promise.allSettled([
        api.get('/admin/stats'),
        api.get('/admin/audit-logs?limit=10'),
        api.get('/admin/reports/risk-distribution'),
    ]);

    if (statsResult.status === 'fulfilled') {
        renderAdminStats(statsResult.value);
    } else {
        const c = document.getElementById('admin-stats');
        if (c) c.innerHTML = `<div class="admin-stat-card" style="color:var(--accent-red);grid-column:1/-1;">Không thể tải thống kê: ${statsResult.reason?.message || 'Lỗi server'}</div>`;
    }

    if (logsResult.status === 'fulfilled') {
        renderAuditLogs(logsResult.value);
    } else {
        const c = document.getElementById('audit-log-list');
        if (c) c.innerHTML = `<p style="color:var(--text-muted);text-align:center;padding:20px;">Không thể tải hoạt động: ${logsResult.reason?.message || 'Lỗi server'}</p>`;
    }

    if (distResult.status === 'fulfilled') {
        renderRiskDistribution(distResult.value);
    }
}

function renderAdminStats(stats) {
    const container = document.getElementById('admin-stats');
    if (!container) return;

    container.innerHTML = `
        <div class="admin-stat-card">
            <div class="stat-top">
                <span class="stat-label">Tổng người dùng</span>
                <span class="stat-icon-wrapper" style="background:#EEF4FC; color:#1A3A6B;">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
                </span>
            </div>
            <div class="stat-value">${stats.total_users || 0}</div>
            <div class="stat-subtext" style="color:#64748B; font-size:0.75rem; margin-top:4px; font-weight:500;">Tài khoản cơ sở quản lý</div>
        </div>
        <div class="admin-stat-card">
            <div class="stat-top">
                <span class="stat-label">Tổng lượt đánh giá</span>
                <span class="stat-icon-wrapper" style="background:#EFF6FF; color:#2563EB;">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>
                </span>
            </div>
            <div class="stat-value">${stats.total_assessments || 0}</div>
            <div class="stat-subtext" style="color:#64748B; font-size:0.75rem; margin-top:4px; font-weight:500;">Hồ sơ khảo sát nguy cơ</div>
        </div>
        <div class="admin-stat-card">
            <div class="stat-top">
                <span class="stat-label">Điểm TB an toàn</span>
                <span class="stat-icon-wrapper" style="background:#ECFDF5; color:#10B981;">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
                </span>
            </div>
            <div class="stat-value" style="color:${(stats.avg_risk_score || 0) >= 60 ? '#16A34A' : '#D97706'}">${stats.avg_risk_score || 0}%</div>
            <div class="stat-subtext" style="color:#64748B; font-size:0.75rem; margin-top:4px; font-weight:500;">Chỉ số an toàn tổng hợp</div>
        </div>
        <div class="admin-stat-card">
            <div class="stat-top">
                <span class="stat-label">Nguy cơ cao / rất cao</span>
                <span class="stat-icon-wrapper" style="background:#FEF2F2; color:#C0202A;">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
                </span>
            </div>
            <div class="stat-value" style="color:var(--gov-red)">${stats.high_risk_count || 0}</div>
            <div class="stat-subtext" style="color:#C0202A; font-size:0.75rem; margin-top:4px; font-weight:600;">Cần kiểm tra khắc phục</div>
        </div>
    `;
}

function renderAuditLogs(logs) {
    const container = document.getElementById('audit-log-list');
    if (!container) return;

    if (!logs.length) {
        container.innerHTML = '<p style="color:var(--text-muted); text-align:center; padding:20px;">Chưa có hoạt động nào</p>';
        return;
    }

    container.innerHTML = logs.map(log => `
        <div class="log-item">
            <span class="log-time">${formatDateTime(log.created_at)}</span>
            <span class="log-action">
                <strong>${log.admin_name || 'Admin'}</strong> ${log.action}
                ${log.target_type ? `<span style="color:var(--text-muted);">(${log.target_type})</span>` : ''}
            </span>
        </div>
    `).join('');
}

function renderRiskDistribution(dist) {
    const canvas = document.getElementById('risk-dist-chart');
    if (!canvas) return;

    const labels = { low: 'Thấp', medium: 'Trung bình', high: 'Cao', critical: 'Rất cao' };
    const colors = { low: '#16A34A', medium: '#C9962C', high: '#E07B39', critical: '#C0202A' };

    new Chart(canvas, {
        type: 'doughnut',
        data: {
            labels: Object.keys(dist).map(k => labels[k] || k),
            datasets: [{
                data: Object.values(dist),
                backgroundColor: Object.keys(dist).map(k => colors[k] || '#94A3B8'),
                borderWidth: 2,
                borderColor: '#FFFFFF',
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: { color: '#1C2A3A', font: { family: 'Source Sans 3, Roboto, sans-serif', size: 12, weight: '600' }, padding: 14 }
                }
            }
        }
    });
}

// Users Management
async function loadAdminUsers(search = '') {
    try {
        const users = await api.get(`/admin/users${search ? '?search=' + encodeURIComponent(search) : ''}`);
        renderUserTable(users);
    } catch (error) {
        showToast(error.message, 'error');
    }
}

function renderUserTable(users) {
    const tbody = document.getElementById('users-tbody');
    if (!tbody) return;

    tbody.innerHTML = users.map(u => `
        <tr>
            <td>${u.full_name}</td>
            <td>${u.email}</td>
            <td>${u.organization || '-'}</td>
            <td><span class="badge badge-info">${u.role}</span></td>
            <td>${u.is_locked ? '<span class="badge badge-critical">Đã khóa</span>' : '<span class="badge badge-safe">Hoạt động</span>'}</td>
            <td>${formatDate(u.created_at)}</td>
            <td>
                <button class="btn-icon" onclick="showResetPasswordModal('${u.id}', '${u.full_name.replace(/'/g, "\\'")}')" title="Reset Mật khẩu">
                    🔑
                </button>
                <button class="btn-icon" onclick="toggleLockUser('${u.id}', ${!u.is_locked})" title="${u.is_locked ? 'Mở khóa' : 'Khóa'}">
                    ${u.is_locked ? '🔓' : '🔒'}
                </button>
            </td>
        </tr>
    `).join('');
}

let targetResetUserId = null;

function showResetPasswordModal(id, name) {
    targetResetUserId = id;
    const span = document.getElementById('reset-target-name');
    if (span) span.textContent = name;
    const input = document.getElementById('reset-new-password');
    if (input) input.value = '';
    
    const m = document.getElementById('reset-password-modal');
    if (m) {
        m.style.display = 'flex';
        setTimeout(() => m.classList.add('active'), 10);
    }
}

function hideResetPasswordModal() {
    targetResetUserId = null;
    const m = document.getElementById('reset-password-modal');
    if (m) {
        m.classList.remove('active');
        setTimeout(() => m.style.display = 'none', 300);
    }
}

async function doResetPassword() {
    if (!targetResetUserId) return;
    const newPassword = document.getElementById('reset-new-password').value;
    if (newPassword.length < 6) {
        showToast('Mật khẩu tối thiểu 6 ký tự', 'error');
        return;
    }
    
    const btn = document.getElementById('btn-do-reset');
    if (btn) btn.disabled = true;
    
    try {
        await api.put(`/admin/users/${targetResetUserId}/reset-password`, { new_password: newPassword });
        showToast('Đặt lại mật khẩu thành công!', 'success');
        hideResetPasswordModal();
    } catch (err) {
        showToast(err.message, 'error');
    } finally {
        if (btn) btn.disabled = false;
    }
}

async function toggleLockUser(userId, lock) {
    try {
        await api.put(`/admin/users/${userId}/lock`, { is_locked: lock });
        showToast(`Đã ${lock ? 'khóa' : 'mở khóa'} tài khoản`);
        loadAdminUsers();
    } catch (error) {
        showToast(error.message, 'error');
    }
}

// Assessments Management
async function loadAdminAssessments(riskLevel = '') {
    try {
        const url = '/admin/assessments' + (riskLevel ? `?risk_level=${riskLevel}` : '');
        const assessments = await api.get(url);
        renderAssessmentTable(assessments);
    } catch (error) {
        showToast(error.message, 'error');
    }
}

function renderAssessmentTable(assessments) {
    const tbody = document.getElementById('assessments-tbody');
    if (!tbody) return;

    tbody.innerHTML = assessments.map(a => `
        <tr>
            <td>${a.facility_name}</td>
            <td>${a.user_name}</td>
            <td>${a.organization || '-'}</td>
            <td style="font-weight:700;">${a.risk_percentage}%</td>
            <td>${getRiskBadge(a.risk_level)}</td>
            <td>${a.completed_at ? formatDate(a.completed_at) : '-'}</td>
        </tr>
    `).join('');
}

// Questions Management
async function loadAdminQuestions(categoryId = '') {
    try {
        const url = '/questions' + (categoryId ? `?category_id=${categoryId}` : '');
        const questions = await api.get(url);
        renderQuestionTable(questions);
    } catch (error) {
        showToast(error.message, 'error');
    }
}

function renderQuestionTable(questions) {
    const tbody = document.getElementById('questions-tbody');
    if (!tbody) return;

    tbody.innerHTML = questions.map(q => `
        <tr>
            <td>${q.id}</td>
            <td style="max-width:300px;">${q.question_text.substring(0, 80)}...</td>
            <td>${q.question_type}</td>
            <td>${q.options ? q.options.length : 0}</td>
            <td>${q.is_active ? '<span class="badge badge-safe">Hoạt động</span>' : '<span class="badge badge-critical">Ẩn</span>'}</td>
            <td>
                <button class="btn-icon" onclick="toggleQuestionActive(${q.id}, ${!q.is_active})" title="${q.is_active ? 'Ẩn' : 'Hiện'}">
                    ${q.is_active ? '👁️' : '👁️‍🗨️'}
                </button>
            </td>
        </tr>
    `).join('');
}

async function toggleQuestionActive(qId, active) {
    try {
        await api.put(`/questions/${qId}`, { is_active: active });
        showToast(`Đã ${active ? 'hiện' : 'ẩn'} câu hỏi`);
        loadAdminQuestions();
    } catch (error) {
        showToast(error.message, 'error');
    }
}

// Reports
async function loadAdminReports() {
    try {
        const dist = await api.get('/admin/reports/risk-distribution');
        renderRiskDistribution(dist);

        const trend = await api.get('/admin/reports/monthly-trend');
        renderMonthlyTrend(trend);
    } catch (error) {
        showToast(error.message, 'error');
    }
}

function renderMonthlyTrend(trend) {
    const canvas = document.getElementById('monthly-trend-chart');
    if (!canvas) return;

    new Chart(canvas, {
        type: 'bar',
        data: {
            labels: trend.map(t => t.month),
            datasets: [
                {
                    label: 'Số đánh giá',
                    data: trend.map(t => t.count),
                    backgroundColor: 'rgba(249, 115, 22, 0.6)',
                    borderRadius: 6,
                    yAxisID: 'y',
                },
                {
                    label: 'Điểm TB (%)',
                    data: trend.map(t => t.avg_score),
                    type: 'line',
                    borderColor: '#3b82f6',
                    backgroundColor: 'rgba(59, 130, 246, 0.1)',
                    fill: true,
                    tension: 0.4,
                    yAxisID: 'y1',
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: { ticks: { color: '#94a3b8' }, grid: { display: false } },
                y: {
                    beginAtZero: true,
                    position: 'left',
                    ticks: { color: '#f97316' },
                    grid: { color: 'rgba(255,255,255,0.05)' },
                    title: { display: true, text: 'Số đánh giá', color: '#f97316' }
                },
                y1: {
                    beginAtZero: true,
                    max: 100,
                    position: 'right',
                    ticks: { color: '#3b82f6' },
                    grid: { display: false },
                    title: { display: true, text: 'Điểm TB (%)', color: '#3b82f6' }
                }
            },
            plugins: {
                legend: { labels: { color: '#cbd5e1' } }
            }
        }
    });
}

// ======================== EXCEL IMPORT ========================

let selectedFile = null;

function downloadImportTemplate() {
    const token = localStorage.getItem('fras_token');
    fetch(API_BASE + '/admin/users/import-template', {
        headers: { 'Authorization': `Bearer ${token}` }
    })
        .then(response => {
            if (!response.ok) throw new Error('Không thể tải mẫu');
            return response.blob();
        })
        .then(blob => {
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'fras_import_users_template.xlsx';
            a.click();
            URL.revokeObjectURL(url);
            showToast('Đã tải file mẫu Excel');
        })
        .catch(err => showToast(err.message, 'error'));
}

function showImportModal() {
    console.log("Opening Import Modal");
    const m = document.getElementById('import-modal');
    if (m) {
        m.style.display = 'flex';
        setTimeout(() => m.classList.add('active'), 10);
    }
    clearFileSelection();
    const res = document.getElementById('import-result');
    if (res) res.style.display = 'none';
}

function hideImportModal() {
    const m = document.getElementById('import-modal');
    if (m) {
        m.classList.remove('active');
        setTimeout(() => m.style.display = 'none', 300);
    }
    clearFileSelection();
}

function handleDragOver(e) {
    e.preventDefault();
    e.currentTarget.classList.add('dropzone-active');
}

function handleDragLeave(e) {
    e.currentTarget.classList.remove('dropzone-active');
}

function handleDrop(e) {
    e.preventDefault();
    e.currentTarget.classList.remove('dropzone-active');
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        setSelectedFile(files[0]);
    }
}

function handleFileSelect(e) {
    const files = e.target.files;
    if (files.length > 0) {
        setSelectedFile(files[0]);
    }
}

function setSelectedFile(file) {
    if (!file.name.match(/\.(xlsx|xls)$/i)) {
        showToast('Chỉ hỗ trợ file Excel (.xlsx, .xls)', 'error');
        return;
    }
    selectedFile = file;
    document.getElementById('file-preview').style.display = 'flex';
    document.getElementById('file-name').textContent = `${file.name} (${(file.size / 1024).toFixed(1)} KB)`;
    document.getElementById('btn-do-import').disabled = false;
}

function clearFileSelection() {
    selectedFile = null;
    const preview = document.getElementById('file-preview');
    if (preview) preview.style.display = 'none';
    const btn = document.getElementById('btn-do-import');
    if (btn) btn.disabled = true;
    const input = document.getElementById('excel-file-input');
    if (input) input.value = '';
}

async function importExcelUsers() {
    if (!selectedFile) {
        showToast('Vui lòng chọn file Excel', 'warning');
        return;
    }

    const btn = document.getElementById('btn-do-import');
    btn.disabled = true;
    btn.textContent = '⏳ Đang import...';

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
        const token = localStorage.getItem('fras_token');
        const response = await fetch(API_BASE + '/admin/users/import-excel', {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${token}` },
            body: formData,
        });

        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.detail || 'Lỗi import');
        }

        // Show results
        const resultDiv = document.getElementById('import-result');
        resultDiv.style.display = 'block';
        resultDiv.innerHTML = `
            <div class="import-summary">
                <div class="import-stat import-stat-success">
                    <span class="import-stat-value">${data.created}</span>
                    <span class="import-stat-label">Tạo mới</span>
                </div>
                <div class="import-stat import-stat-warning">
                    <span class="import-stat-value">${data.skipped}</span>
                    <span class="import-stat-label">Bỏ qua</span>
                </div>
                <div class="import-stat import-stat-error">
                    <span class="import-stat-value">${data.errors.length}</span>
                    <span class="import-stat-label">Lỗi</span>
                </div>
            </div>
            <p class="import-message">${data.message}</p>
            ${data.errors.length > 0 ? `
                <div class="import-errors">
                    <strong>Chi tiết lỗi:</strong>
                    <ul>${data.errors.map(e => `<li>${e}</li>`).join('')}</ul>
                </div>
            ` : ''}
        `;

        showToast(data.message);
        clearFileSelection();
        loadAdminUsers(); // Refresh user table
    } catch (err) {
        showToast(err.message, 'error');
    } finally {
        btn.disabled = false;
        btn.textContent = '📥 Import';
    }
}

