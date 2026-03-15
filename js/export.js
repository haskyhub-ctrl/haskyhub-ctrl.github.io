/**
 * FRAS Export JS
 * PDF generation using html2pdf.js (supports Vietnamese text)
 */

function getAuthToken() {
    return localStorage.getItem('fras_token') || (typeof api !== 'undefined' ? api.token : null);
}

async function exportPDF(assessmentId) {
    showLoading('Đang tạo PDF...');
    try {
        const data = await api.get(`/export/data/${assessmentId}`);
        generatePDFFromHTML(data);
        hideLoading();
        showToast('Đã tạo PDF thành công!');
    } catch (error) {
        hideLoading();
        showToast(error.message, 'error');
    }
}

function generatePDFFromHTML(data) {
    const riskLabels = { low: 'Thấp', medium: 'Trung bình', high: 'Cao', critical: 'Rất cao' };
    const riskColors = { low: '#22c55e', medium: '#eab308', high: '#f97316', critical: '#ef4444' };
    const riskColor = riskColors[data.risk_level] || '#94a3b8';

    // Build category scores HTML
    let catHtml = '';
    (data.category_scores || []).forEach(cs => {
        const barColor = riskColors[cs.risk_level] || '#94a3b8';
        catHtml += `
            <tr>
                <td style="padding:8px 12px; border-bottom:1px solid #e2e8f0;">${cs.icon || ''} ${cs.category_name}</td>
                <td style="padding:8px 12px; border-bottom:1px solid #e2e8f0; text-align:center;">${cs.score_obtained}/${cs.max_score}</td>
                <td style="padding:8px 12px; border-bottom:1px solid #e2e8f0; text-align:center;">
                    <div style="background:#e2e8f0; border-radius:2px; height:8px; width:100px; display:inline-block; vertical-align:middle;">
                        <div style="background:${barColor}; height:100%; width:${cs.percentage}%; border-radius:2px;"></div>
                    </div>
                    <span style="margin-left:6px; font-weight:600; color:${barColor};">${cs.percentage}%</span>
                </td>
            </tr>`;
    });

    // Build AI analysis HTML
    let aiHtml = '';
    if (data.ai_analysis) {
        const ai = typeof data.ai_analysis === 'string' ? JSON.parse(data.ai_analysis) : data.ai_analysis;
        if (ai.overall_assessment) {
            aiHtml += `<div style="background:#f0f9ff; border-left:3px solid #3b82f6; padding:10px 14px; margin-bottom:12px; font-size:11px;">${ai.overall_assessment}</div>`;
        }
        if (ai.strengths?.length) {
            aiHtml += `<h4 style="color:#16a34a; font-size:12px; margin:10px 0 6px;">✅ Ưu điểm</h4><ul style="font-size:11px; padding-left:18px; margin:0;">`;
            ai.strengths.forEach(s => { aiHtml += `<li style="margin-bottom:3px;">${s}</li>`; });
            aiHtml += '</ul>';
        }
        if (ai.critical_weaknesses?.length) {
            aiHtml += `<h4 style="color:#dc2626; font-size:12px; margin:10px 0 6px;">⚠️ Tồn tại, nguy cơ cháy, nổ</h4><ul style="font-size:11px; padding-left:18px; margin:0;">`;
            ai.critical_weaknesses.forEach(s => { aiHtml += `<li style="margin-bottom:3px;">${s}</li>`; });
            aiHtml += '</ul>';
        }
        if (ai.detailed_recommendations?.length) {
            aiHtml += `<h4 style="color:#ea580c; font-size:12px; margin:10px 0 6px;">🔧 Khuyến cáo chi tiết</h4>`;
            ai.detailed_recommendations.forEach((r, i) => {
                aiHtml += `<div style="border-left:3px solid ${riskColors[r.priority] || '#94a3b8'}; padding:6px 10px; margin-bottom:6px; background:#fafafa; font-size:11px;">
                    <strong>${i + 1}. ${r.title || ''}</strong> <span style="color:${riskColors[r.priority] || '#666'}; font-size:10px; font-weight:600;">[${(r.priority || '').toUpperCase()}]</span>
                    <div style="color:#555; margin-top:3px;">${r.description || ''}</div>
                    <div style="color:#888; font-size:10px; margin-top:2px;">⏰ ${r.deadline || ''} ${r.legal_basis ? '| 📜 ' + r.legal_basis : ''}</div>
                </div>`;
            });
        }
        if (ai.legal_references?.length) {
            aiHtml += `<h4 style="color:#7c3aed; font-size:12px; margin:10px 0 6px;">📜 Tham chiếu pháp lý</h4><ul style="font-size:10px; padding-left:18px; margin:0; color:#555;">`;
            ai.legal_references.forEach(r => { aiHtml += `<li style="margin-bottom:2px;">${r}</li>`; });
            aiHtml += '</ul>';
        }
    }

    // Build full HTML document for PDF
    const html = `
    <div id="pdf-content" style="font-family: 'Times New Roman', serif; color:#1a1a1a; padding:20px; max-width:800px; margin:0 auto;">
        <div style="text-align:center; border-bottom:2px solid #1e3a5f; padding-bottom:16px; margin-bottom:16px;">
            <h1 style="font-size:18px; color:#1e3a5f; margin:0;">BÁO CÁO ĐÁNH GIÁ NGUY CƠ CHÁY NỔ</h1>
            <p style="font-size:11px; color:#666; margin:4px 0 0;">Hệ thống FRAS — Fire Risk Assessment System</p>
        </div>

        <h3 style="font-size:13px; color:#1e3a5f; border-bottom:1px solid #cbd5e1; padding-bottom:4px;">I. THÔNG TIN CƠ SỞ</h3>
        <table style="width:100%; font-size:11px; margin-bottom:16px;">
            <tr><td style="width:140px; padding:4px 0; font-weight:bold;">Tên cơ sở:</td><td>${data.facility_name || 'N/A'}</td></tr>
            <tr><td style="padding:4px 0; font-weight:bold;">Loại hình:</td><td>${data.facility_type || 'N/A'}</td></tr>
            <tr><td style="padding:4px 0; font-weight:bold;">Địa chỉ:</td><td>${data.facility_address || 'N/A'}</td></tr>
            <tr><td style="padding:4px 0; font-weight:bold;">Diện tích:</td><td>${data.facility_area || 'N/A'} m²</td></tr>
            <tr><td style="padding:4px 0; font-weight:bold;">Số người làm việc:</td><td>${data.worker_count || 'N/A'}</td></tr>
            <tr><td style="padding:4px 0; font-weight:bold;">Người đánh giá:</td><td>${data.user_name || 'N/A'}</td></tr>
            <tr><td style="padding:4px 0; font-weight:bold;">Ngày đánh giá:</td><td>${data.completed_at ? new Date(data.completed_at).toLocaleDateString('vi-VN') : 'N/A'}</td></tr>
        </table>

        <h3 style="font-size:13px; color:#1e3a5f; border-bottom:1px solid #cbd5e1; padding-bottom:4px;">II. KẾT QUẢ TỔNG QUAN</h3>
        <div style="display:flex; gap:20px; margin-bottom:16px;">
            <div style="flex:1; text-align:center; background:#f8fafc; border:1px solid #e2e8f0; padding:12px;">
                <div style="font-size:22px; font-weight:800; color:${riskColor};">${data.risk_percentage}%</div>
                <div style="font-size:10px; color:#64748b; text-transform:uppercase;">Tỷ lệ nguy cơ</div>
            </div>
            <div style="flex:1; text-align:center; background:#f8fafc; border:1px solid #e2e8f0; padding:12px;">
                <div style="font-size:22px; font-weight:800;">${data.total_score}/${data.max_possible_score}</div>
                <div style="font-size:10px; color:#64748b; text-transform:uppercase;">Tổng điểm</div>
            </div>
            <div style="flex:1; text-align:center; background:#f8fafc; border:1px solid #e2e8f0; padding:12px;">
                <div style="font-size:14px; font-weight:700; color:${riskColor}; padding:4px 12px; border:2px solid ${riskColor}; display:inline-block;">${riskLabels[data.risk_level] || data.risk_level}</div>
                <div style="font-size:10px; color:#64748b; text-transform:uppercase; margin-top:4px;">Mức nguy cơ</div>
            </div>
        </div>

        <h3 style="font-size:13px; color:#1e3a5f; border-bottom:1px solid #cbd5e1; padding-bottom:4px;">III. ĐIỂM THEO NHÓM NGUYÊN NHÂN</h3>
        <table style="width:100%; border-collapse:collapse; font-size:11px; margin-bottom:16px;">
            <tr style="background:#1e3a5f; color:white;">
                <th style="padding:8px 12px; text-align:left;">Nhóm nguyên nhân</th>
                <th style="padding:8px 12px; text-align:center;">Điểm</th>
                <th style="padding:8px 12px; text-align:center;">Tỷ lệ nguy cơ</th>
            </tr>
            ${catHtml}
        </table>

        ${aiHtml ? `
        <h3 style="font-size:13px; color:#1e3a5f; border-bottom:1px solid #cbd5e1; padding-bottom:4px;">IV. PHÂN TÍCH VÀ KHUYẾN CÁO</h3>
        ${aiHtml}
        ` : ''}

        <div style="text-align:center; margin-top:24px; padding-top:12px; border-top:1px solid #cbd5e1; font-size:10px; color:#94a3b8;">
            FRAS — Hệ thống Đánh giá Nguy cơ Cháy Nổ | Xuất ngày ${new Date().toLocaleDateString('vi-VN')}
        </div>
    </div>`;

    // Create temp container 
    const container = document.createElement('div');
    container.style.position = 'fixed';
    container.style.left = '-9999px';
    container.style.top = '0';
    container.style.width = '800px';
    container.style.background = 'white';
    container.innerHTML = html;
    document.body.appendChild(container);

    const opt = {
        margin: [10, 10, 10, 10],
        filename: `FRAS_${data.facility_name || 'Report'}_${new Date().toISOString().slice(0, 10)}.pdf`,
        image: { type: 'jpeg', quality: 0.98 },
        html2canvas: { scale: 2, useCORS: true, letterRendering: true },
        jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' },
        pagebreak: { mode: ['avoid-all', 'css', 'legacy'] }
    };

    html2pdf().set(opt).from(container.querySelector('#pdf-content')).save().then(() => {
        document.body.removeChild(container);
    }).catch(err => {
        document.body.removeChild(container);
        showToast('Lỗi tạo PDF: ' + err.message, 'error');
    });
}
