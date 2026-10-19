/**
 * FRAS Export JS
 * PDF generation using html2pdf.js (supports Vietnamese text)
 * Standard Government Letterhead & Police Assessment Dossier Format
 */

// Danh mục căn cứ pháp lý chuẩn, dùng chung cho trang kết quả và file PDF.
// Giữ đồng bộ với CURRENT_LEGAL_REFERENCES trong backend/utils/ai_prompt.py.
const FRAS_LEGAL_REFERENCES = [
    'Luật Phòng cháy, chữa cháy và Cứu nạn, cứu hộ số 55/2024/QH15',
    'Luật Điện lực số 61/2024/QH15',
    'Nghị quyết số 66.18/2026/NQ-CP ngày 18/5/2026 của Chính phủ',
    'Nghị định số 105/2025/NĐ-CP quy định chi tiết một số điều và biện pháp thi hành Luật Phòng cháy, chữa cháy và Cứu nạn, cứu hộ (sửa đổi, bổ sung bởi Nghị định số 347/2026/NĐ-CP)',
    'QCVN 06:2022/BXD và Sửa đổi 1:2023: Quy chuẩn kỹ thuật quốc gia về An toàn cháy cho nhà và công trình',
    'QCVN 10:2025/BCA: Quy chuẩn kỹ thuật quốc gia về trang bị, bố trí phương tiện phòng cháy, chữa cháy, cứu nạn, cứu hộ cho nhà và công trình',
    'QCVN 01:2021/BXD: Quy chuẩn kỹ thuật quốc gia về Quy hoạch xây dựng',
    'QCVN 13:2018/BXD: Quy chuẩn kỹ thuật quốc gia về Gara ô tô',
    'QCVN 01:2020/BCT: Quy chuẩn kỹ thuật quốc gia về yêu cầu thiết kế cửa hàng xăng dầu',
    'QCVN 25:2025/BCT: Quy chuẩn kỹ thuật quốc gia về An toàn điện',
    'QCVN 25:2025/BKHCN: Quy chuẩn kỹ thuật quốc gia về Thiết bị điện dùng cho lắp đặt điện trong gia đình và hệ thống điện tương tự',
    'TCVN 3890:2023: Phương tiện phòng cháy và chữa cháy cho nhà và công trình, trang bị, bố trí, kiểm tra, bảo dưỡng',
    'TCVN 5738:2021: Phòng cháy chữa cháy, hệ thống báo cháy tự động, yêu cầu kỹ thuật',
    'TCVN 7336:2021: Phòng cháy chữa cháy, hệ thống sprinkler tự động, yêu cầu thiết kế và lắp đặt',
    'TCVN 9385:2012: Chống sét cho công trình xây dựng, hướng dẫn thiết kế, kiểm tra và bảo trì hệ thống',
    'TCVN 6223:2017: Cửa hàng khí dầu mỏ hóa lỏng (LPG), yêu cầu chung về an toàn',
    'TCVN 5307:2009: Kho dầu mỏ và sản phẩm dầu mỏ, yêu cầu thiết kế',
    'Các văn bản quy phạm pháp luật, quy chuẩn, tiêu chuẩn kỹ thuật khác có liên quan',
];

function getAuthToken() {
    return localStorage.getItem('fras_token') || (typeof api !== 'undefined' ? api.token : null);
}

function formatPdfFacilityType(type) {
    if (!type) return 'Chưa phân loại';
    const dict = {
        'hospitality': 'Nhà hàng, khách sạn, dịch vụ lưu trú, ăn uống',
        'commercial': 'Trung tâm thương mại, siêu thị, chợ, cửa hàng',
        'industrial': 'Cơ sở sản xuất công nghiệp, nhà xưởng, kho hàng',
        'residential': 'Nhà ở kết hợp sản xuất kinh doanh, nhà ở nhiều hộ',
        'gas_station': 'Cửa hàng kinh doanh xăng dầu, khí đốt hóa lỏng (LPG)',
        'karaoke': 'Cơ sở kinh doanh dịch vụ karaoke, vũ trường, quán bar',
        'educational': 'Cơ sở giáo dục, trường học, nhà trẻ, mầm non',
        'medical': 'Cơ sở khám chữa bệnh, bệnh viện, phòng khám',
        'office': 'Cơ quan, văn phòng, trụ sở',
        'warehouse': 'Kho hàng, kho vật liệu',
        'mixed_residence': 'Nhà ở hỗn hợp (ở kết hợp kinh doanh)',
        'medical_education': 'Bệnh viện, trường học, cơ sở y tế',
        'fuel_gas': 'Kinh doanh xăng dầu, khí gas, vật liệu nổ',
        'transport': 'Phương tiện giao thông',
        'construction': 'Công trình xây dựng',
        'laboratory': 'Cơ sở nghiên cứu, phòng thí nghiệm',
        'agriculture': 'Nông nghiệp, chế biến nông lâm sản'
    };
    // A survey may carry several types separated by commas
    return type.split(',').map(t => t.trim()).filter(Boolean)
        .map(t => dict[t.toLowerCase()] || t).join('; ');
}

async function exportPDF(assessmentId) {
    if (typeof showLoading === 'function') showLoading('Đang khởi tạo biên bản PDF chuẩn hóa...');
    try {
        const data = await api.get(`/export/data/${assessmentId}`);
        await generatePDFFromHTML(data);
        if (typeof hideLoading === 'function') hideLoading();
        if (typeof showToast === 'function') showToast('Đã xuất biên bản PDF thành công!');
    } catch (error) {
        if (typeof hideLoading === 'function') hideLoading();
        if (typeof showToast === 'function') showToast(error.message, 'error');
    }
}

async function generatePDFFromHTML(data) {
    const riskLabels = {
        low: 'AN TOÀN / NGUY CƠ THẤP',
        medium: 'TRUNG BÌNH / CẦN CẢI THIỆN',
        high: 'NGUY CƠ CAO',
        critical: 'RẤT CAO / CẤP BÁO'
    };
    const riskColors = {
        low: '#16a34a',
        medium: '#d97706',
        high: '#ea580c',
        critical: '#dc2626'
    };
    const riskColor = riskColors[data.risk_level] || '#0f172a';
    const riskText = riskLabels[data.risk_level] || 'CHƯA XÁC ĐỊNH';

    // Build category scores HTML
    let catHtml = '';
    (data.category_scores || []).forEach((cs, idx) => {
        const barColor = riskColors[cs.risk_level] || '#64748b';
        const statusText = cs.risk_level === 'low' ? 'NGUY CƠ THẤP' : cs.risk_level === 'medium' ? 'CẦN LƯU Ý' : 'NGUY HIỂM';
        // Fixed pixel widths: the PDF renderer ignores % widths on nested bars
        const barFill = Math.round(Math.min(100, Math.max(0, cs.percentage || 0)) * 0.9);
        catHtml += `
            <tr style="page-break-inside: avoid; border-bottom: 1px solid #cbd5e1;">
                <td style="padding: 8px 10px; text-align: center; font-weight: bold; border: 1px solid #cbd5e1;">${idx + 1}</td>
                <td style="padding: 8px 10px; font-weight: bold; color: #0f172a; border: 1px solid #cbd5e1;">${cs.category_name}</td>
                <td style="padding: 8px 10px; text-align: center; font-weight: bold; border: 1px solid #cbd5e1;">${cs.score_obtained}/${cs.max_score} điểm</td>
                <td style="padding: 8px 10px; text-align: center; border: 1px solid #cbd5e1;">
                    <span style="display: inline-block; vertical-align: middle; border: 1px solid #cbd5e1; line-height: 0; white-space: nowrap;"><span style="display: inline-block; height: 10px; width: ${barFill}px; background: ${barColor};"></span><span style="display: inline-block; height: 10px; width: ${90 - barFill}px; background: #e2e8f0;"></span></span>
                    <span style="margin-left: 8px; font-weight: bold; color: ${barColor}; font-size: 12px;">${cs.percentage}%</span>
                </td>
                <td style="padding: 8px 10px; text-align: center; border: 1px solid #cbd5e1;">
                    <span style="display: inline-block; padding: 2px 6px; font-size: 10px; font-weight: bold; color: ${barColor}; border: 1px solid ${barColor}; text-transform: uppercase;">
                        ${statusText}
                    </span>
                </td>
            </tr>`;
    });

    // Parse AI Analysis
    let aiObj = null;
    if (data.ai_analysis) {
        try {
            aiObj = typeof data.ai_analysis === 'string' ? JSON.parse(data.ai_analysis) : data.ai_analysis;
            if (aiObj && aiObj.gemini_38) {
                aiObj = aiObj.gemini_38;
            }
        } catch (e) {
            aiObj = null;
        }
    }

    let aiHtml = '';
    if (aiObj) {
        if (aiObj.overall_assessment) {
            aiHtml += `
            <div class="pdf-avoid-break" style="background: #f8fafc; border: 1px solid #cbd5e1; border-left: 5px solid #0f172a; padding: 12px 14px; margin-bottom: 14px;">
                <div style="font-weight: bold; color: #0f172a; font-size: 13px; text-transform: uppercase; margin-bottom: 4px;">1. NHẬN ĐỊNH TỔNG QUAN</div>
                <div style="font-size: 12px; color: #1e293b; line-height: 1.55;">${aiObj.overall_assessment}</div>
            </div>`;
        }

        if (aiObj.strengths?.length) {
            aiHtml += `
            <div class="pdf-avoid-break" style="margin-bottom: 14px;">
                <div style="font-weight: bold; color: #16a34a; font-size: 13px; text-transform: uppercase; border-bottom: 1.5px solid #16a34a; padding-bottom: 3px; margin-bottom: 6px;">
                    2. ƯU ĐIỂM (${aiObj.strengths.length})
                </div>
                <ul style="font-size: 12px; color: #1e293b; padding-left: 20px; margin: 0; line-height: 1.55;">
                    ${aiObj.strengths.map(s => `<li style="margin-bottom: 4px;">${s}</li>`).join('')}
                </ul>
            </div>`;
        }

        if (aiObj.critical_weaknesses?.length) {
            aiHtml += `
            <div class="pdf-avoid-break" style="margin-bottom: 14px;">
                <div style="font-weight: bold; color: #dc2626; font-size: 13px; text-transform: uppercase; border-bottom: 1.5px solid #dc2626; padding-bottom: 3px; margin-bottom: 6px;">
                    3. TỒN TẠI & NGUY CƠ CHÁY NỔ TIỀM ẨN (${aiObj.critical_weaknesses.length})
                </div>
                <ul style="font-size: 12px; color: #991b1b; padding-left: 20px; margin: 0; line-height: 1.55;">
                    ${aiObj.critical_weaknesses.map(w => `<li style="margin-bottom: 4px; font-weight: bold;">${w}</li>`).join('')}
                </ul>
            </div>`;
        }

        if (aiObj.detailed_recommendations?.length) {
            const priorityLabels = {
                'urgent': 'KHẨN CẤP (TRONG 24H - 48H)',
                'high': 'ƯU TIÊN CAO',
                'medium': 'TRUNG BÌNH',
                'low': 'THẤP'
            };
            aiHtml += `
            <div style="margin-bottom: 14px;">
                <div style="font-weight: bold; color: #ea580c; font-size: 13px; text-transform: uppercase; border-bottom: 1.5px solid #ea580c; padding-bottom: 3px; margin-bottom: 10px;">
                    4. KHUYẾN CÁO & GIẢI PHÁP KỸ THUẬT KHẮC PHỤC (${aiObj.detailed_recommendations.length} HẠNG MỤC)
                </div>`;
            aiObj.detailed_recommendations.forEach((r, i) => {
                const pClass = (r.priority || '').toLowerCase();
                const pLabel = priorityLabels[pClass] || (r.priority || 'ƯU TIÊN').toUpperCase();
                const pColor = pClass === 'urgent' ? '#dc2626' : pClass === 'high' ? '#ea580c' : '#d97706';
                aiHtml += `
                <div class="pdf-avoid-break" style="border: 1px solid #cbd5e1; border-left: 4px solid ${pColor}; padding: 8px 12px; margin-bottom: 8px; background: #ffffff;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                        <span style="font-weight: bold; font-size: 12px; color: #0f172a;">${i + 1}. ${r.title || ''}</span>
                        <span style="font-size: 10px; font-weight: bold; color: ${pColor}; border: 1px solid ${pColor}; padding: 1px 6px;">[${pLabel}]</span>
                    </div>
                    <div style="font-size: 11.5px; color: #334155; line-height: 1.45; margin-bottom: 4px;">${r.description || ''}</div>
                    <div style="font-size: 10.5px; color: #64748b; line-height: 1.4;">
                        <strong>Hạn hoàn thành:</strong> ${r.deadline || (pClass === 'urgent' ? 'Khắc phục ngay trong 24h - 48h' : '30 ngày')}
                        ${r.responsible_party ? ` | <strong>Phụ trách:</strong> ${r.responsible_party}` : ''}
                    </div>
                    ${r.legal_basis ? `<div style="font-size: 10.5px; color: #7c3aed; margin-top: 3px;"><strong>Căn cứ:</strong> ${r.legal_basis}</div>` : ''}
                </div>`;
            });
            aiHtml += `</div>`;
        }

        if (aiObj.daily_checklist?.length) {
            aiHtml += `
            <div class="pdf-avoid-break" style="margin-bottom: 14px;">
                <div style="font-weight: bold; color: #1e3a8a; font-size: 13px; text-transform: uppercase; border-bottom: 1.5px solid #1e3a8a; padding-bottom: 3px; margin-bottom: 6px;">
                    5. DANH MỤC TỰ KIỂM TRA AN TOÀN HÀNG NGÀY
                </div>
                <ul style="font-size: 12px; color: #1e293b; padding-left: 20px; margin: 0; line-height: 1.55;">
                    ${aiObj.daily_checklist.map(item => `<li style="margin-bottom: 4px;"><strong>${item}</strong></li>`).join('')}
                </ul>
            </div>`;
        }

        if (aiObj.improvement_plan) {
            const p = aiObj.improvement_plan;
            const phases = [
                { key: '30_days', label: 'GIAI ĐOẠN 1: KHẮC PHỤC NGAY (24H - 48H) VÀ 30 NGÀY ĐẦU', color: '#dc2626' },
                { key: '60_days', label: 'GIAI ĐOẠN 2: 30 - 60 NGÀY (NÂNG CẤP HẠ TẦNG & TRANG THIẾT BỊ)', color: '#ea580c' },
                { key: '90_days', label: 'GIAI ĐOẠN 3: 60 - 90 NGÀY (HOÀN THIỆN & DUY TRÌ BỀN VỮNG)', color: '#16a34a' }
            ];

            aiHtml += `
            <div style="margin-bottom: 14px;">
                <div style="font-weight: bold; color: #0f172a; font-size: 13px; text-transform: uppercase; border-bottom: 1.5px solid #0f172a; padding-bottom: 3px; margin-bottom: 10px;">
                    6. KẾ HOẠCH HÀNH ĐỘNG KHẮC PHỤC CHI TIẾT (LỘ TRÌNH 90 NGÀY)
                </div>`;
            phases.forEach(phase => {
                const items = p[phase.key];
                if (!items?.length) return;
                aiHtml += `
                <div class="pdf-avoid-break" style="margin-bottom: 10px; border: 1px solid #cbd5e1;">
                    <div style="background: ${phase.color}; color: #ffffff; padding: 6px 10px; font-weight: bold; font-size: 11.5px; text-transform: uppercase;">
                        ${phase.label}
                    </div>
                    <div style="padding: 8px 10px; background: #ffffff;">
                        ${items.map((item, idx) => {
                            if (typeof item === 'string') {
                                return `<div style="font-size: 11px; margin-bottom: 4px;">${idx + 1}. ${item}</div>`;
                            }
                            return `
                            <div style="margin-bottom: 6px; font-size: 11px;">
                                <strong>${idx + 1}. ${item.task || item.title || ''}</strong>
                                ${item.detail || item.description ? `<div style="color: #475569; margin: 2px 0;">${item.detail || item.description}</div>` : ''}
                                <div style="color: #64748b; font-size: 10.5px;">
                                    ${item.responsible ? `Phụ trách: ${item.responsible}` : ''}
                                    ${item.legal_basis ? ` | Căn cứ: ${item.legal_basis}` : ''}
                                </div>
                            </div>`;
                        }).join('')}
                    </div>
                </div>`;
            });
            aiHtml += `</div>`;
        }

        {
            aiHtml += `
            <div class="pdf-avoid-break" style="margin-bottom: 14px;">
                <div style="font-weight: bold; color: #475569; font-size: 12px; text-transform: uppercase; border-bottom: 1.5px solid #cbd5e1; padding-bottom: 3px; margin-bottom: 6px;">
                    7. CĂN CỨ VĂN BẢN QUY PHẠM PHÁP LUẬT & QUY CHUẨN KỸ THUẬT HIỆN HÀNH
                </div>
                <ul style="font-size: 11px; color: #475569; padding-left: 20px; margin: 0; line-height: 1.5;">
                    ${FRAS_LEGAL_REFERENCES.map(r => `<li style="margin-bottom: 3px;">${r}</li>`).join('')}
                </ul>
            </div>`;
        }
    }

    // Without AI recommendations, fall back to the rule-based recommendations stored per answer
    const hasAiRecs = !!(aiObj && aiObj.detailed_recommendations && aiObj.detailed_recommendations.length);
    const ruleRecs = data.recommendations || [];
    if (!hasAiRecs && ruleRecs.length) {
        const pLabels = { urgent: 'KHẨN CẤP', high: 'ƯU TIÊN CAO', medium: 'TRUNG BÌNH', low: 'THẤP' };
        const pColors = { urgent: '#dc2626', high: '#ea580c', medium: '#d97706', low: '#16a34a' };
        aiHtml += `
            <div style="margin-bottom: 14px;">
                <div style="font-weight: bold; color: #ea580c; font-size: 13px; text-transform: uppercase; border-bottom: 1.5px solid #ea580c; padding-bottom: 3px; margin-bottom: 10px;">
                    KHUYẾN CÁO KHẮC PHỤC THEO KẾT QUẢ RÀ SOÁT (${ruleRecs.length} HẠNG MỤC)
                </div>`;
        ruleRecs.forEach((r, i) => {
            const pColor = pColors[r.priority] || '#d97706';
            aiHtml += `
                <div class="pdf-avoid-break" style="border: 1px solid #cbd5e1; border-left: 4px solid ${pColor}; padding: 8px 12px; margin-bottom: 8px; background: #ffffff;">
                    <div style="display: flex; justify-content: space-between; gap: 10px; margin-bottom: 4px;">
                        <span style="font-weight: bold; font-size: 11.5px; color: #475569;">${i + 1}. ${r.category_name || ''}</span>
                        <span style="font-size: 10px; font-weight: bold; color: ${pColor}; border: 1px solid ${pColor}; padding: 1px 6px; white-space: nowrap;">[${pLabels[r.priority] || 'ƯU TIÊN'}]</span>
                    </div>
                    ${r.question_text ? `<div style="font-size: 11px; color: #64748b; font-style: italic; margin-bottom: 3px;">Tồn tại: ${r.question_text}</div>` : ''}
                    <div style="font-size: 11.5px; color: #0f172a; line-height: 1.45; margin-bottom: 3px;">${r.recommendation_text}</div>
                    <div style="font-size: 10.5px; color: #64748b;"><strong>Hạn khắc phục:</strong> ${r.deadline_days ? r.deadline_days + ' ngày' : '30 ngày'}</div>
                    ${r.legal_reference ? `<div style="font-size: 10.5px; color: #7c3aed; margin-top: 3px;"><strong>Căn cứ:</strong> ${r.legal_reference}</div>` : ''}
                </div>`;
        });
        aiHtml += `</div>`;
    }
    const sectionFourTitle = aiObj
        ? 'IV. NHẬN ĐỊNH & KHUYẾN CÁO KHẮC PHỤC TỪ TRÍ TUỆ NHÂN TẠO'
        : 'IV. KHUYẾN CÁO KHẮC PHỤC';

    // Build the complete PDF document HTML
    const formattedDate = data.completed_at ? new Date(data.completed_at).toLocaleDateString('vi-VN') : new Date().toLocaleDateString('vi-VN');
    const docNumber = `FRAS-${(data.id || '').substring(0, 8).toUpperCase()}`;

    const html = `
    <div id="pdf-content" style="font-family: 'Times New Roman', serif; color: #0f172a; padding: 24px; max-width: 820px; margin: 0 auto; background: #ffffff; line-height: 1.45;">
        <style>
            /* The site's dark theme paints table cells white; keep the paper document dark-on-white */
            #pdf-content td { color: #0f172a; }
            #pdf-content tbody tr:hover { background: transparent; }
        </style>
        <!-- POLICE COMMAND HEADER -->
        <div style="border-bottom: 2.5px solid #991b1b; padding-bottom: 14px; margin-bottom: 16px;">
            <table style="width: 100%; border-collapse: collapse; border: none;">
                <tr style="border: none;">
                    <td style="width: 55%; vertical-align: top; text-align: center; border: none; padding: 0;">
                        <div style="font-size: 13px; font-weight: bold; color: #991b1b; text-transform: uppercase; letter-spacing: 0.5px;">CÔNG AN THÀNH PHỐ BẮC NINH</div>
                        <div style="font-size: 11.5px; font-weight: bold; color: #0f172a; text-transform: uppercase; margin-top: 2px;">PHÒNG CẢNH SÁT PCCC VÀ CNCH</div>
                        <div style="font-size: 10.5px; color: #64748b; margin-top: 3px;">Hệ thống Khảo sát & Đánh giá Nguy cơ Cháy nổ FRAS AI</div>
                    </td>
                    <td style="width: 45%; vertical-align: top; text-align: center; border: none; padding: 0;">
                        <div style="font-size: 12px; font-weight: bold; color: #0f172a;">CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM</div>
                        <div style="font-size: 11px; font-style: italic; color: #0f172a;">Độc lập - Tự do - Hạnh phúc</div>
                        <div style="font-size: 10.5px; color: #64748b; margin-top: 4px;">Số hồ sơ: <strong style="color: #0f172a;">${docNumber}</strong></div>
                        <div style="font-size: 9px; color: #475569; font-weight: bold; text-transform: uppercase; margin-top: 2px;">Mã chống làm giả khảo sát: ${docNumber}</div>
                        ${data.id ? `<img src="/api/export/qrcode/${data.id}" alt="QR" style="width: 64px; height: 64px; margin: 4px auto 0; display: block; border: 1px solid #0f172a;">` : ''}
                    </td>
                </tr>
            </table>

            <div style="text-align: center; margin-top: 18px;">
                <h1 style="font-size: 17px; font-weight: bold; color: #991b1b; margin: 0; text-transform: uppercase; letter-spacing: 0.5px;">
                    BIÊN BẢN KẾT QUẢ KHẢO SÁT & KHUYẾN CÁO AN TOÀN PCCC
                </h1>
                <p style="font-size: 11px; color: #64748b; margin: 4px 0 0; font-style: italic;">
                    (Tự động đối soát quy chuẩn kỹ thuật và khuyến cáo bởi Hệ thống FRAS AI - Công an TP Bắc Ninh)
                </p>
            </div>
        </div>

        <!-- I. THÔNG TIN CƠ SỞ -->
        <div class="pdf-avoid-break" style="margin-bottom: 16px;">
            <div style="font-size: 13px; font-weight: bold; color: #0f172a; text-transform: uppercase; background: #f1f5f9; padding: 6px 10px; border-left: 4px solid #991b1b; margin-bottom: 8px;">
                I. THÔNG TIN CƠ SỞ ĐƯỢC KHẢO SÁT
            </div>
            <table style="width: 100%; border-collapse: collapse; font-size: 12px;">
                <tr>
                    <td style="width: 22%; padding: 5px 8px; font-weight: bold; color: #475569; border: 1px solid #e2e8f0;">Tên cơ sở/công trình:</td>
                    <td style="padding: 5px 8px; font-weight: bold; color: #0f172a; border: 1px solid #e2e8f0;" colspan="3">${data.facility_name || 'Khảo sát tự do'}</td>
                </tr>
                <tr>
                    <td style="padding: 5px 8px; font-weight: bold; color: #475569; border: 1px solid #e2e8f0;">Loại hình cơ sở:</td>
                    <td style="padding: 5px 8px; border: 1px solid #e2e8f0;" colspan="3">${formatPdfFacilityType(data.facility_type)}</td>
                </tr>
                <tr>
                    <td style="padding: 5px 8px; font-weight: bold; color: #475569; border: 1px solid #e2e8f0;">Địa chỉ:</td>
                    <td style="padding: 5px 8px; border: 1px solid #e2e8f0;" colspan="3">${data.facility_address || 'TP Bắc Ninh'}</td>
                </tr>
                <tr>
                    <td style="width: 22%; padding: 5px 8px; font-weight: bold; color: #475569; border: 1px solid #e2e8f0;">Diện tích sàn:</td>
                    <td style="width: 28%; padding: 5px 8px; border: 1px solid #e2e8f0;">${data.facility_area ? data.facility_area + ' m²' : 'Chưa khai báo'}</td>
                    <td style="width: 22%; padding: 5px 8px; font-weight: bold; color: #475569; border: 1px solid #e2e8f0;">Số người làm việc:</td>
                    <td style="width: 28%; padding: 5px 8px; border: 1px solid #e2e8f0;">${data.worker_count ? data.worker_count + ' người' : 'Chưa khai báo'}</td>
                </tr>
                <tr>
                    <td style="padding: 5px 8px; font-weight: bold; color: #475569; border: 1px solid #e2e8f0;">Thời gian khảo sát:</td>
                    <td style="padding: 5px 8px; border: 1px solid #e2e8f0;">${formattedDate}</td>
                    <td style="padding: 5px 8px; font-weight: bold; color: #475569; border: 1px solid #e2e8f0;">Người thực hiện:</td>
                    <td style="padding: 5px 8px; border: 1px solid #e2e8f0;">${data.user_name || 'Người đại diện cơ sở'}</td>
                </tr>
            </table>
        </div>

        <!-- II. KẾT QUẢ ĐÁNH GIÁ TỔNG QUAN -->
        <div class="pdf-avoid-break" style="margin-bottom: 16px;">
            <div style="font-size: 13px; font-weight: bold; color: #0f172a; text-transform: uppercase; background: #f1f5f9; padding: 6px 10px; border-left: 4px solid #991b1b; margin-bottom: 8px;">
                II. KẾT QUẢ ĐÁNH GIÁ NGUY CƠ TỔNG QUAN
            </div>
            <table style="width: 100%; border-collapse: collapse; text-align: center; font-size: 12px; margin-bottom: 10px;">
                <tr>
                    <td style="width: 33.3%; padding: 12px; border: 1.5px solid #cbd5e1; background: #f8fafc;">
                        <div style="font-size: 26px; font-weight: 900; color: ${riskColor}; line-height: 1;">${data.risk_percentage}%</div>
                        <div style="font-size: 10.5px; font-weight: bold; color: #64748b; text-transform: uppercase; margin-top: 4px;">TỶ LỆ NGUY CƠ TỔNG HỢP</div>
                    </td>
                    <td style="width: 33.3%; padding: 12px; border: 1.5px solid #cbd5e1; background: #f8fafc;">
                        <div style="font-size: 26px; font-weight: 900; color: #0f172a; line-height: 1;">${data.total_score} <span style="font-size: 14px; font-weight: normal; color: #64748b;">/ ${data.max_possible_score || 100}</span></div>
                        <div style="font-size: 10.5px; font-weight: bold; color: #64748b; text-transform: uppercase; margin-top: 4px;">ĐIỂM NGUY CƠ / ĐIỂM TỐI ĐA</div>
                    </td>
                    <td style="width: 33.3%; padding: 12px; border: 1.5px solid #cbd5e1; background: #f8fafc;">
                        <div style="font-size: 13px; font-weight: bold; color: ${riskColor}; border: 1.5px solid ${riskColor}; display: inline-block; padding: 4px 8px;">
                            ${riskText}
                        </div>
                        <div style="font-size: 10.5px; font-weight: bold; color: #64748b; text-transform: uppercase; margin-top: 6px;">MỨC ĐỘ NGUY CƠ CHÁY NỔ</div>
                    </td>
                </tr>
            </table>
            <div style="font-size: 11px; color: #64748b; font-style: italic; line-height: 1.45; background: #f8fafc; border: 1px solid #e2e8f0; padding: 8px 12px;">
                * <strong>Lưu ý nghiệp vụ:</strong> Tỷ lệ % nguy cơ thể hiện mức độ tích tụ hiểm họa cháy nổ (trong đó sự cố hệ thống điện chiếm hơn 50% nguyên nhân phát sinh cháy; bất cẩn nguồn lửa/nhiệt chiếm 15%... Tồn tại về lối thoát nạn và phương tiện PCCC quyết định khả năng thoát nạn sống còn và hạn chế thiệt hại khi xảy ra cháy).
            </div>
        </div>

        <!-- III. ĐIỂM THEO CÁC NHÓM RÀ SOÁT -->
        <div class="pdf-avoid-break" style="margin-bottom: 16px;">
            <div style="font-size: 13px; font-weight: bold; color: #0f172a; text-transform: uppercase; background: #f1f5f9; padding: 6px 10px; border-left: 4px solid #991b1b; margin-bottom: 8px;">
                III. KẾT QUẢ RÀ SOÁT THEO CÁC NHÓM NGUY CƠ
            </div>
            <table style="width: 100%; border-collapse: collapse; font-size: 11.5px;">
                <thead>
                    <tr style="background: #0f172a; color: #ffffff;">
                        <th style="width: 40px; padding: 8px 6px; text-align: center; border: 1px solid #0f172a;">STT</th>
                        <th style="padding: 8px 10px; text-align: left; border: 1px solid #0f172a;">Nhóm nguy cơ rà soát</th>
                        <th style="width: 110px; padding: 8px 6px; text-align: center; border: 1px solid #0f172a;">Điểm ghi nhận</th>
                        <th style="width: 140px; padding: 8px 6px; text-align: center; border: 1px solid #0f172a;">Tỷ lệ nguy cơ</th>
                        <th style="width: 110px; padding: 8px 6px; text-align: center; border: 1px solid #0f172a;">Đánh giá</th>
                    </tr>
                </thead>
                <tbody>
                    ${catHtml}
                </tbody>
            </table>
        </div>

        <!-- IV. PHÂN TÍCH CHUYÊN SÂU & KHUYẾN CÁO TỪ HỆ THỐNG AI -->
        ${aiHtml ? `
        <div style="margin-bottom: 16px;">
            <div style="font-size: 13px; font-weight: bold; color: #0f172a; text-transform: uppercase; background: #f1f5f9; padding: 6px 10px; border-left: 4px solid #991b1b; margin-bottom: 12px;">
                ${sectionFourTitle}
            </div>
            ${aiHtml}
        </div>
        ` : ''}

        <!-- CHỮ KÝ VÀ ĐỐI SOÁT -->
        <div class="pdf-avoid-break" style="margin-top: 24px; padding-top: 14px; border-top: 2px solid #0f172a;">
            <table style="width: 100%; border: none; font-size: 12px;">
                <tr style="border: none;">
                    <td style="width: 50%; text-align: center; vertical-align: top; border: none; padding: 0;">
                        <div style="font-weight: bold; text-transform: uppercase; color: #0f172a;">ĐẠI DIỆN CƠ SỞ ĐƯỢC KHẢO SÁT</div>
                        <div style="font-size: 11px; font-style: italic; color: #64748b; margin-top: 2px;">(Ký, ghi rõ họ tên và đóng dấu nếu có)</div>
                        <div style="height: 60px;"></div>
                    </td>
                    <td style="width: 50%; text-align: center; vertical-align: top; border: none; padding: 0;">
                        <div style="font-style: italic; font-size: 11px; color: #64748b; margin-bottom: 2px;">Bắc Ninh, ngày ${new Date().getDate()} tháng ${new Date().getMonth() + 1} năm ${new Date().getFullYear()}</div>
                        <div style="font-weight: bold; text-transform: uppercase; color: #0f172a;">HỆ THỐNG FRAS AI - CÔNG AN TP BẮC NINH</div>
                        <div style="font-size: 11px; font-style: italic; color: #64748b; margin-top: 2px;">(Hồ sơ điện tử đối soát tự động)</div>
                        <div style="height: 60px;"></div>
                    </td>
                </tr>
            </table>
            <div style="text-align: center; font-size: 10px; color: #94a3b8; margin-top: 16px; border-top: 1px dashed #cbd5e1; padding-top: 8px;">
                Biên bản này được xuất tự động từ Hệ thống Khảo sát & Đánh giá Nguy cơ Cháy nổ FRAS AI thuộc Công an thành phố Bắc Ninh. Mã hồ sơ: ${docNumber}.
            </div>
        </div>
    </div>`;

    // Create temporary hidden rendering container
    const container = document.createElement('div');
    container.style.position = 'fixed';
    container.style.left = '-9999px';
    container.style.top = '0';
    container.style.width = '820px';
    container.style.background = '#ffffff';
    container.innerHTML = html;
    document.body.appendChild(container);

    const opt = {
        margin: [10, 10, 10, 10],
        filename: `FRAS_${data.facility_name ? data.facility_name.replace(/[^a-zA-Z0-9\u00C0-\u1EF9]/g, '_') : 'BienBan'}_${docNumber}.pdf`,
        image: { type: 'jpeg', quality: 0.98 },
        html2canvas: { scale: 2, useCORS: true, letterRendering: true },
        jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' },
        pagebreak: {
            mode: ['css', 'legacy'],
            avoid: ['.pdf-avoid-break', 'tr', 'table']
        }
    };

    try {
        await html2pdf().set(opt).from(container.querySelector('#pdf-content')).save();
    } finally {
        if (container.parentNode) {
            container.parentNode.removeChild(container);
        }
    }
}
