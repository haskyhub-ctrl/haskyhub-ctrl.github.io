/**
 * FRAS Compare JS
 * Compare multiple assessments side by side
 */

let compareState = {
    assessments: [],
    selected: [],
};

async function initCompare() {
    if (!requireAuth()) return;

    showLoading('Đang tải dữ liệu...');
    try {
        compareState.assessments = await api.get('/assessments?status=completed');
        hideLoading();
        renderCompareSelect();
    } catch (error) {
        hideLoading();
        showToast(error.message, 'error');
    }
}

function renderCompareSelect() {
    const container = document.getElementById('compare-list');
    if (!container) return;

    if (compareState.assessments.length < 2) {
        container.innerHTML = `
            <div class="empty-state">
                <div class="empty-icon">📊</div>
                <h3>Chưa đủ dữ liệu so sánh</h3>
                <p>Bạn cần có ít nhất 2 đánh giá hoàn thành để so sánh</p>
                <a href="/survey.html" class="btn btn-primary">Bắt đầu Đánh giá</a>
            </div>
        `;
        return;
    }

    container.innerHTML = `
        <p style="color: var(--text-secondary); margin-bottom: 16px;">Chọn 2-4 đánh giá để so sánh:</p>
        <div class="compare-select">
            ${compareState.assessments.map(a => `
                <div class="compare-card card ${compareState.selected.includes(a.id) ? 'selected' : ''}" 
                     onclick="toggleCompareSelect('${a.id}', this)">
                    <h4>${a.facility_name}</h4>
                    <p style="color:var(--text-muted); font-size:0.82rem;">${formatDate(a.completed_at)}</p>
                    <div style="display:flex; justify-content:space-between; margin-top:8px;">
                        <span style="font-size:0.85rem;">Điểm: ${a.risk_percentage}%</span>
                        ${getRiskBadge(a.risk_level)}
                    </div>
                </div>
            `).join('')}
        </div>
        <div style="text-align:center; margin-top:16px; display:flex; gap:10px; justify-content:center; flex-wrap:wrap;">
            <button class="btn btn-primary" onclick="runCompare()" id="compare-btn" ${compareState.selected.length < 2 ? 'disabled' : ''}>
                📊 So sánh (${compareState.selected.length} đã chọn)
            </button>
            <button class="btn btn-outline" onclick="runAITrend()" id="ai-trend-btn" ${compareState.selected.length < 2 ? 'disabled' : ''}
                style="border-color:#8b5cf6; color:#8b5cf6;">
                🤖 AI Phân tích Xu hướng
            </button>
        </div>
        <div id="ai-trend-result"></div>
        <div id="compare-results"></div>
    `;
}

function toggleCompareSelect(id, el) {
    const idx = compareState.selected.indexOf(id);
    if (idx >= 0) {
        compareState.selected.splice(idx, 1);
        el.classList.remove('selected');
    } else if (compareState.selected.length < 4) {
        compareState.selected.push(id);
        el.classList.add('selected');
    } else {
        showToast('Chỉ có thể chọn tối đa 4 đánh giá', 'warning');
        return;
    }

    const btn = document.getElementById('compare-btn');
    const aiBtn = document.getElementById('ai-trend-btn');
    if (btn) {
        btn.disabled = compareState.selected.length < 2;
        btn.textContent = `📊 So sánh (${compareState.selected.length} đã chọn)`;
    }
    if (aiBtn) {
        aiBtn.disabled = compareState.selected.length < 2;
    }
}

async function runCompare() {
    showLoading('Đang so sánh...');
    try {
        const ids = compareState.selected.join(',');
        const results = await api.get(`/assessments/compare/list?ids=${ids}`);
        hideLoading();
        renderCompareResults(results);
    } catch (error) {
        hideLoading();
        showToast(error.message, 'error');
    }
}

function renderCompareResults(results) {
    const container = document.getElementById('compare-results');
    if (!container || !results.length) return;

    // Prepare radar data
    const radarDatasets = results.map(r => ({
        label: r.assessment.facility_name + ' (' + formatDate(r.assessment.completed_at) + ')',
        labels: r.category_scores.map(c => c.category_name),
        data: r.category_scores.map(c => c.percentage),
    }));

    container.innerHTML = `
        <div class="dashboard-section mt-4" style="padding:24px;">
            <h3 style="margin-bottom:16px;">📊 Biểu đồ So sánh</h3>
            <div class="chart-container" style="height:400px;">
                <canvas id="compare-radar"></canvas>
            </div>
        </div>
        
        <div class="compare-result mt-3">
            ${results.map(r => `
                <div class="card">
                    <h4>${r.assessment.facility_name}</h4>
                    <p style="color:var(--text-muted); font-size:0.82rem;">${formatDate(r.assessment.completed_at)}</p>
                    <div style="display:flex; gap:16px; margin:16px 0;">
                        <div>
                            <div style="font-size:2rem; font-weight:800; color:${riskColors[r.assessment.risk_level] || '#94a3b8'}">
                                ${r.assessment.risk_percentage}%
                            </div>
                            <div style="font-size:0.8rem; color:var(--text-muted);">Tỷ lệ nguy cơ</div>
                        </div>
                        <div>${getRiskBadge(r.assessment.risk_level)}</div>
                    </div>
                    ${r.category_scores.map(cs => `
                        <div style="display:flex; justify-content:space-between; align-items:center; padding:6px 0; font-size:0.85rem;">
                            <span style="color:var(--text-secondary)">${cs.category_name}</span>
                            <span style="font-weight:600">${cs.percentage}%</span>
                        </div>
                    `).join('')}
                </div>
            `).join('')}
        </div>
    `;

    if (radarDatasets.length > 0) {
        createCompareRadar('compare-radar', radarDatasets);
    }
}

// ========== AI TREND ANALYSIS ==========
async function runAITrend() {
    const container = document.getElementById('ai-trend-result');
    const btn = document.getElementById('ai-trend-btn');
    if (!container || compareState.selected.length < 2) return;

    btn.disabled = true;
    btn.innerHTML = '⏳ AI đang phân tích...';
    container.innerHTML = '<div style="text-align:center; padding:30px;"><div class="loading-spinner"></div><p style="color:var(--text-secondary); margin-top:8px;">🤖 Gemini đang phân tích xu hướng...</p></div>';

    try {
        const result = await api.post('/ai/compare-trend', {
            assessment_ids: compareState.selected,
        });

        const trendIcon = { improving: '📈', declining: '📉', stable: '➡️' };
        const trendColor = { improving: '#22c55e', declining: '#ef4444', stable: '#eab308' };
        const trendText = { improving: 'Đang cải thiện', declining: 'Đang xấu đi', stable: 'Ổn định' };
        const t = result.trend || 'stable';

        container.innerHTML = `
            <div class="dashboard-section mt-3" style="padding:24px; border-left:4px solid ${trendColor[t]};">
                <div style="display:flex; align-items:center; gap:12px; margin-bottom:16px;">
                    <span style="font-size:2.5rem;">${trendIcon[t]}</span>
                    <div>
                        <h3 style="margin:0; color:${trendColor[t]};">${trendText[t]}</h3>
                        <p style="margin:4px 0 0; color:var(--text-secondary); font-size:0.9rem;">${result.summary || ''}</p>
                    </div>
                </div>

                ${result.improved_areas?.length ? `
                    <h5 style="color:#22c55e; margin:12px 0 8px;">✅ Lĩnh vực cải thiện</h5>
                    <ul style="padding-left:20px; color:var(--text-secondary); font-size:0.85rem;">
                        ${result.improved_areas.map(a => `<li style="margin-bottom:4px;">${a}</li>`).join('')}
                    </ul>
                ` : ''}

                ${result.declined_areas?.length ? `
                    <h5 style="color:#ef4444; margin:12px 0 8px;">⚠️ Lĩnh vực xấu đi</h5>
                    <ul style="padding-left:20px; color:var(--text-secondary); font-size:0.85rem;">
                        ${result.declined_areas.map(a => `<li style="margin-bottom:4px;">${a}</li>`).join('')}
                    </ul>
                ` : ''}

                ${result.overall_trend_detail ? `<p style="color:var(--text-muted); font-size:0.85rem; margin-top:12px; line-height:1.6;">${result.overall_trend_detail}</p>` : ''}

                ${result.priority_recommendations?.length ? `
                    <h5 style="color:#f97316; margin:16px 0 8px;">🎯 Đề xuất ưu tiên</h5>
                    <ol style="padding-left:20px; color:var(--text-secondary); font-size:0.85rem;">
                        ${result.priority_recommendations.map(r => `<li style="margin-bottom:4px;">${r}</li>`).join('')}
                    </ol>
                ` : ''}
            </div>
        `;
    } catch (err) {
        container.innerHTML = `<div class="alert alert-danger" style="margin-top:12px;">Lỗi AI: ${err.message}</div>`;
    } finally {
        btn.disabled = false;
        btn.innerHTML = '🤖 AI Phân tích Xu hướng';
    }
}
