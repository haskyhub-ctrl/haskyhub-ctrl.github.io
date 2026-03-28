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
            <div class="stat-label">Tổng người dùng</div>
            <div class="stat-value">${stats.total_users}</div>
        </div>
        <div class="admin-stat-card">
            <div class="stat-label">Tổng đánh giá</div>
            <div class="stat-value">${stats.total_assessments}</div>
        </div>
        <div class="admin-stat-card">
            <div class="stat-label">Điểm TB an toàn</div>
            <div class="stat-value" style="color:${stats.avg_risk_score >= 60 ? 'var(--accent-green)' : 'var(--accent-orange)'}">${stats.avg_risk_score}%</div>
        </div>
        <div class="admin-stat-card">
            <div class="stat-label">Nguy cơ cao/rất cao</div>
            <div class="stat-value" style="color:var(--accent-red)">${stats.high_risk_count}</div>
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
    const colors = { low: '#22c55e', medium: '#eab308', high: '#f97316', critical: '#ef4444' };

    new Chart(canvas, {
        type: 'doughnut',
        data: {
            labels: Object.keys(dist).map(k => labels[k] || k),
            datasets: [{
                data: Object.values(dist),
                backgroundColor: Object.keys(dist).map(k => colors[k] || '#94a3b8'),
                borderWidth: 0,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: { color: '#cbd5e1', padding: 16 }
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
                <button class="btn-icon" onclick="toggleLockUser('${u.id}', ${!u.is_locked})" title="${u.is_locked ? 'Mở khóa' : 'Khóa'}">
                    ${u.is_locked ? '🔓' : '🔒'}
                </button>
            </td>
        </tr>
    `).join('');
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
        const url = '/questions/' + (categoryId ? `?category_id=${categoryId}` : '');
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

