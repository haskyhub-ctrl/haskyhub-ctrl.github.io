/**
 * FRAS Survey JS
 * Handles the multi-step survey flow
 */

let surveyState = {
    categories: [],
    currentStep: 0, // 0 = facility info, 1..N = categories, N+1 = review
    answers: {},     // { questionId: optionId }
    assessment: null,
    activeAssessmentId: null,
    facilityInfo: {},
    userLocation: null, // { latitude, longitude }
    isSubmitting: false,
    draftBannerDismissed: false,
};

const DRAFT_STORAGE_KEY = 'fras_survey_draft_v1';

function saveSurveyDraft() {
    try {
        const answeredCount = Object.keys(surveyState.answers || {}).length;
        if (!surveyState.facilityInfo?.facility_name && answeredCount === 0) return;
        const draft = {
            facilityInfo: surveyState.facilityInfo || {},
            answers: surveyState.answers || {},
            currentStep: surveyState.currentStep || 0,
            activeAssessmentId: surveyState.activeAssessmentId || null,
            savedAt: new Date().toISOString(),
            answeredCount: answeredCount,
        };
        localStorage.setItem(DRAFT_STORAGE_KEY, JSON.stringify(draft));
    } catch (e) {
        console.warn('Could not save draft to localStorage', e);
    }
}

function getSurveyDraft() {
    try {
        const raw = localStorage.getItem(DRAFT_STORAGE_KEY);
        return raw ? JSON.parse(raw) : null;
    } catch (e) {
        return null;
    }
}

function clearSurveyDraft() {
    try {
        localStorage.removeItem(DRAFT_STORAGE_KEY);
    } catch (e) {}
}

function exportDraftBackup() {
    try {
        const draft = getSurveyDraft() || {
            facilityInfo: surveyState.facilityInfo,
            answers: surveyState.answers,
            activeAssessmentId: surveyState.activeAssessmentId,
            exportedAt: new Date().toISOString(),
        };
        const dataStr = 'data:text/json;charset=utf-8,' + encodeURIComponent(JSON.stringify(draft, null, 2));
        const downloadAnchor = document.createElement('a');
        downloadAnchor.setAttribute('href', dataStr);
        downloadAnchor.setAttribute('download', `fras_backup_khao_sat_${Date.now()}.json`);
        document.body.appendChild(downloadAnchor);
        downloadAnchor.click();
        downloadAnchor.remove();
        showToast('Đã tải xuống bản sao lưu câu trả lời!', 'success');
    } catch (err) {
        showToast('Không thể xuất file: ' + err.message, 'error');
    }
}

function checkDraftBanner() {
    if (surveyState.draftBannerDismissed) return '';
    const draft = getSurveyDraft();
    if (!draft) return '';
    const hasData = (draft.facilityInfo && draft.facilityInfo.facility_name) || (draft.answeredCount && draft.answeredCount > 0);
    if (!hasData) return '';

    return `
        <div id="draft-banner" class="draft-restore-banner">
            <div class="draft-restore-content">
                <span class="draft-restore-icon">💾</span>
                <div class="draft-restore-text">
                    <h4>Phát hiện bài làm chưa hoàn tất</h4>
                    <p>Hệ thống tìm thấy bản nháp cơ sở <strong>${draft.facilityInfo?.facility_name || 'chưa đặt tên'}</strong> (${draft.answeredCount || 0} câu đã làm, lưu lúc ${formatDateTime(draft.savedAt)}).</p>
                </div>
            </div>
            <div class="draft-restore-actions">
                <button type="button" class="btn btn-outline btn-sm" onclick="discardDraft()">Bỏ qua</button>
                <button type="button" class="btn btn-primary btn-sm" onclick="restoreDraft()">Khôi phục bài</button>
            </div>
        </div>
    `;
}

async function restoreDraft() {
    const draft = getSurveyDraft();
    if (!draft) return;
    surveyState.facilityInfo = draft.facilityInfo || {};
    surveyState.answers = draft.answers || {};
    surveyState.activeAssessmentId = draft.activeAssessmentId || null;
    surveyState.draftBannerDismissed = true;

    if (surveyState.facilityInfo.facility_type) {
        await loadCategoriesForFacilityType(surveyState.facilityInfo.facility_type);
    }
    const maxSteps = getTotalSteps();
    surveyState.currentStep = Math.min(draft.currentStep || 0, maxSteps - 1);
    renderStep();
    showToast('Đã khôi phục bài làm thành công!', 'success');
}

function discardDraft() {
    clearSurveyDraft();
    surveyState.draftBannerDismissed = true;
    renderStep();
    showToast('Đã bắt đầu bài làm mới.');
}

const facilityTypes = [
    { value: 'industrial', label: 'Cơ sở sản xuất công nghiệp', icon: '🏭' },
    { value: 'warehouse', label: 'Kho hàng, kho vật liệu', icon: '🏪' },
    { value: 'mixed_residence', label: 'Nhà ở hỗn hợp (ở + kinh doanh)', icon: '🏠' },
    { value: 'hospitality', label: 'Nhà hàng, khách sạn, chợ, TTTM', icon: '🍽️' },
    { value: 'medical_education', label: 'Bệnh viện, trường học, y tế', icon: '🏥' },
    { value: 'fuel_gas', label: 'Xăng dầu, khí gas, vật liệu nổ', icon: '⛽' },
    { value: 'transport', label: 'Phương tiện giao thông', icon: '🚌' },
    { value: 'residential', label: 'Khu dân cư, nhà ở, nhà trọ', icon: '🏘️' },
    { value: 'construction', label: 'Công trình xây dựng', icon: '🏗️' },
    { value: 'office', label: 'Cơ quan, văn phòng, trụ sở', icon: '🏛️' },
    { value: 'laboratory', label: 'Nghiên cứu, phòng thí nghiệm', icon: '🔬' },
    { value: 'agriculture', label: 'Nông nghiệp, chế biến nông lâm sản', icon: '🌾' },
];

async function initSurvey() {
    if (!requireAuth()) return;

    // Check if user has pre-assigned location (imported accounts)
    const user = api.getUser();
    const isImportedUser = !!(user && user.facility_code);

    if (isImportedUser && user.latitude && user.longitude) {
        // Pre-fill location from user profile (imported account)
        surveyState.userLocation = {
            latitude: user.latitude,
            longitude: user.longitude,
        };
        surveyState.isImportedUser = true;
        console.log('📍 Location pre-set from profile:', surveyState.userLocation);
    } else {
        // Self-registered user: detect GPS
        surveyState.isImportedUser = false;
        detectUserLocation();
    }
    renderStep();
}

function detectUserLocationUI() {
    // Chạy ngầm lập tức để lấy vị trí, không hiển thị giao diện tải
    if ('geolocation' in navigator) {
        navigator.geolocation.getCurrentPosition(
            (pos) => {
                surveyState.userLocation = {
                    latitude: pos.coords.latitude,
                    longitude: pos.coords.longitude,
                };
                console.log('📍 Location detected silently:', surveyState.userLocation);
            },
            (err) => {
                console.log('📍 Location not available silently:', err.message);
            },
            { timeout: 10000, enableHighAccuracy: true }
        );
    }
}

function detectUserLocation() {
    detectUserLocationUI();
}

async function loadCategoriesForFacilityType(facilityType) {
    showLoading('Đang tải câu hỏi phù hợp với loại cơ sở...');
    try {
        const url = facilityType ? `/survey/categories?facility_type=${facilityType}` : '/survey/categories';
        surveyState.categories = await api.get(url);
        hideLoading();
    } catch (error) {
        hideLoading();
        showToast(error.message, 'error');
    }
}

function getTotalSteps() {
    return surveyState.categories.length + 2; // facility + categories + review
}

function renderProgressBar() {
    const total = getTotalSteps();
    const container = document.getElementById('survey-progress');
    if (!container) return;

    let html = '';
    const stepLabels = ['Thông tin cơ sở', ...surveyState.categories.map(c => c.name), 'Xác nhận'];

    for (let i = 0; i < total; i++) {
        const isActive = i === surveyState.currentStep;
        const isCompleted = i < surveyState.currentStep;
        const indicatorClass = isCompleted ? 'completed' : isActive ? 'active' : '';
        const content = isCompleted ? '✓' : (i + 1);

        html += `<div class="progress-step">
            <div class="step-indicator ${indicatorClass}" title="${stepLabels[i]}">${content}</div>
        </div>`;

        if (i < total - 1) {
            html += `<div class="step-line ${isCompleted ? 'completed' : ''}"></div>`;
        }
    }
    container.innerHTML = html;
}

function renderStep() {
    const container = document.getElementById('survey-body');
    if (!container) return;

    renderProgressBar();

    if (surveyState.currentStep === 0) {
        renderFacilityForm(container);
    } else if (surveyState.currentStep <= surveyState.categories.length) {
        renderCategoryQuestions(container, surveyState.currentStep - 1);
    } else {
        renderReview(container);
    }
}

function renderFacilityForm(container) {
    const info = surveyState.facilityInfo || {};
    const selectedTypes = (info.facility_type || '').split(',').map(s => s.trim());
    const draftBannerHtml = checkDraftBanner();

    container.innerHTML = `
        ${draftBannerHtml}
        <div class="facility-form fade-in">
            <div class="card">
                <h2 style="margin-bottom: 8px;">📋 Thông tin Cơ sở</h2>
                <p style="color: var(--text-secondary); margin-bottom: 24px;">Vui lòng nhập thông tin cơ sở cần đánh giá</p>
                
                <div class="form-group">
                    <label>Tên cơ sở / Công ty *</label>
                    <input type="text" class="form-control" id="f_name" placeholder="VD: Công ty TNHH ABC" value="${info.facility_name || ''}" required>
                </div>
                
                <div class="form-group">
                    <label>Loại hình cơ sở *</label>
                    <div class="facility-type-grid" id="facility-type-grid">
                        ${facilityTypes.map(t => `
                            <div class="facility-type-option ${selectedTypes.includes(t.value) ? 'selected' : ''}" data-value="${t.value}">
                                <span class="type-icon">${t.icon}</span>
                                ${t.label}
                            </div>
                        `).join('')}
                    </div>
                </div>
                
                <div class="form-group">
                    <label>Địa chỉ</label>
                    <input type="text" class="form-control" id="f_address" placeholder="Địa chỉ cơ sở" value="${info.facility_address || ''}">
                    ${!surveyState.isImportedUser ? `
                    <button type="button" class="btn" style="margin-top: 12px; width: 100%; border: 1px dashed var(--border-color); background: transparent; color: var(--text-secondary); display: flex; align-items: center; justify-content: center; gap: 8px;" onclick="openMapPicker()">
                        <span id="map-picker-text">📍 Ấn để chọn vị trí trên bản đồ (Tùy chọn)</span>
                    </button>
                    ` : ''}
                </div>
            </div>
            
            <div class="survey-nav">
                <div></div>
                <button class="btn btn-primary btn-lg" onclick="nextStep()">Bắt đầu Khảo sát →</button>
            </div>
        </div>
    `;

    // Facility type selection — MULTI-SELECT toggle
    document.querySelectorAll('.facility-type-option').forEach(opt => {
        opt.addEventListener('click', () => {
            opt.classList.toggle('selected');
        });
    });
}

function renderCategoryQuestions(container, catIndex) {
    const cat = surveyState.categories[catIndex];
    const questions = cat.questions || [];

    let questionsHtml = questions.map((q, qi) => {
        const selectedOptionId = surveyState.answers[q.id];
        return `
            <div class="question-card">
                <div class="question-text">
                    <span class="question-number">${qi + 1}</span>
                    <span>${q.question_text}</span>
                </div>
                ${q.help_text ? `<div class="question-help">💡 ${q.help_text}</div>` : ''}
                ${q.reference ? `<div class="question-ref">📜 ${q.reference}</div>` : ''}
                <div class="options-list">
                    ${(q.options || []).map(opt => `
                        <div class="option-item ${selectedOptionId === opt.id ? 'selected' : ''}" 
                             onclick="selectOption(${q.id}, ${opt.id}, this)">
                            <div class="option-radio"></div>
                            <span class="option-key">${opt.option_key}.</span>
                            <span class="option-text">${opt.option_text}</span>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
    }).join('');

    const answeredCount = questions.filter(q => surveyState.answers[q.id]).length;

    container.innerHTML = `
        <div class="survey-container fade-in">
            <div class="survey-category-header">
                <span class="cat-icon">${cat.icon || '📋'}</span>
                <h2>${cat.name}</h2>
                <p class="cat-desc">${cat.description || ''}</p>
                <p class="cat-progress">${answeredCount}/${questions.length} câu đã trả lời</p>
                <div class="progress-bar mt-2">
                    <div class="progress-fill medium" style="width: ${questions.length > 0 ? (answeredCount / questions.length * 100) : 0}%"></div>
                </div>
            </div>
            
            ${questionsHtml}
            
            <div class="survey-nav">
                <button class="btn btn-secondary" onclick="prevStep()">← Quay lại</button>
                <span class="step-info">Nhóm ${catIndex + 1} / ${surveyState.categories.length}</span>
                <button class="btn btn-primary" onclick="nextStep()">Tiếp theo →</button>
            </div>
        </div>
    `;
}

function selectOption(questionId, optionId, element) {
    surveyState.answers[questionId] = optionId;
    saveSurveyDraft();
    const parent = element.closest('.options-list');
    parent.querySelectorAll('.option-item').forEach(el => el.classList.remove('selected'));
    element.classList.add('selected');

    // Update progress
    const catIndex = surveyState.currentStep - 1;
    const cat = surveyState.categories[catIndex];
    const answered = cat.questions.filter(q => surveyState.answers[q.id]).length;
    const progressText = document.querySelector('.cat-progress');
    if (progressText) progressText.textContent = `${answered}/${cat.questions.length} câu đã trả lời`;
    const progressFill = document.querySelector('.survey-category-header .progress-fill');
    if (progressFill) progressFill.style.width = `${(answered / cat.questions.length) * 100}%`;
}

function renderReview(container) {
    const info = surveyState.facilityInfo || {};
    let categoriesReview = surveyState.categories.map(cat => {
        const questions = cat.questions || [];
        const answered = questions.filter(q => surveyState.answers[q.id]).length;
        const items = questions.map(q => {
            const optId = surveyState.answers[q.id];
            const opt = q.options.find(o => o.id === optId);
            return `<div class="review-item">
                <span class="label">${q.question_text.substring(0, 60)}...</span>
                <span class="value">${opt ? opt.option_key : '—'}</span>
            </div>`;
        }).join('');

        return `<div class="review-section">
            <h4>${cat.icon} ${cat.name} <span style="color: var(--text-muted); font-weight: 400;">(${answered}/${questions.length})</span></h4>
            ${items}
        </div>`;
    }).join('');

    container.innerHTML = `
        <div class="survey-container fade-in">
            <div class="card">
                <h2 style="margin-bottom: 8px;">📝 Xác nhận & Gửi</h2>
                <p style="color: var(--text-secondary); margin-bottom: 24px;">Kiểm tra lại thông tin trước khi gửi đánh giá</p>
                
                <div class="review-section">
                    <h4>📋 Thông tin cơ sở</h4>
                    <div class="review-item"><span class="label">Tên cơ sở:</span><span class="value">${info.facility_name || '—'}</span></div>
                    <div class="review-item"><span class="label">Loại hình:</span><span class="value">${info.facility_type || 'N/A'}</span></div>
                    <div class="review-item"><span class="label">Địa chỉ:</span><span class="value">${info.facility_address || 'N/A'}</span></div>
                </div>
                
                ${categoriesReview}
            </div>
            
            <div class="survey-nav" id="survey-nav-actions">
                <button class="btn btn-secondary" onclick="prevStep()" id="prev-btn">← Quay lại</button>
                <button class="btn btn-primary btn-lg" onclick="submitSurvey()" id="submit-btn">🔥 Gửi Đánh giá</button>
            </div>

            <div id="submission-queue-area" style="display: none;"></div>
        </div>
    `;
}

function prevStep() {
    if (surveyState.currentStep > 0) {
        surveyState.currentStep--;
        saveSurveyDraft();
        renderStep();
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
}

async function nextStep() {
    // Validate current step
    if (surveyState.currentStep === 0) {
        const name = document.getElementById('f_name')?.value.trim();
        if (!name) {
            showToast('Vui lòng nhập tên cơ sở', 'error');
            return;
        }
        const selectedTypes = document.querySelectorAll('.facility-type-option.selected');
        if (selectedTypes.length === 0) {
            showToast('Vui lòng chọn ít nhất một loại hình cơ sở', 'error');
            return;
        }
        const address = document.getElementById('f_address')?.value.trim();
        if (!address || address.length < 5) {
            showToast('Vui lòng nhập địa chỉ cơ sở (tối thiểu 5 ký tự)', 'error');
            document.getElementById('f_address')?.focus();
            return;
        }
        // Collect all selected types as comma-separated
        const typesArray = Array.from(selectedTypes).map(el => el.dataset.value);
        surveyState.facilityInfo = {
            facility_name: name,
            facility_type: typesArray.join(','),
            facility_address: address,
            latitude: surveyState.userLocation?.latitude || null,
            longitude: surveyState.userLocation?.longitude || null,
        };
        saveSurveyDraft();
        // Load categories filtered by ALL selected facility types
        await loadCategoriesForFacilityType(surveyState.facilityInfo.facility_type);
    }

    if (surveyState.currentStep < getTotalSteps() - 1) {
        surveyState.currentStep++;
        saveSurveyDraft();
        renderStep();
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
}

// =================== SUBMISSION QUEUE & AUTO-RETRY ENGINE ===================

function preventTabClose(e) {
    e.preventDefault();
    e.returnValue = 'Bài khảo sát đang được hệ thống gửi và xếp hàng đợi xử lý. Vui lòng không đóng tab!';
    return e.returnValue;
}

function updateQueueStep(stepNum, status) {
    const el = document.getElementById(`q-step-${stepNum}`);
    if (!el) return;
    el.classList.remove('active', 'done');
    if (status === 'active') {
        el.classList.add('active');
        el.querySelector('span:first-child').textContent = '⏳';
    } else if (status === 'done') {
        el.classList.add('done');
        el.querySelector('span:first-child').textContent = '✅';
    } else {
        el.querySelector('span:first-child').textContent = '⚪';
    }
}

function updateQueueAlert(type, icon, message) {
    const box = document.getElementById('queue-alert-box');
    const iconEl = document.getElementById('queue-alert-icon');
    const textEl = document.getElementById('queue-alert-text');
    if (!box || !iconEl || !textEl) return;

    box.className = `queue-live-alert ${type}`;
    iconEl.textContent = icon;
    textEl.innerHTML = message;
}

function updateQueueRetryStatus(text) {
    const el = document.getElementById('queue-retry-status');
    if (el) el.textContent = text;
}

function showQueuePanel() {
    const nav = document.getElementById('survey-nav-actions');
    const queueArea = document.getElementById('submission-queue-area');
    if (nav) nav.style.display = 'none';
    if (!queueArea) return;

    const totalAnswered = Object.keys(surveyState.answers || {}).length;
    queueArea.style.display = 'block';
    queueArea.innerHTML = `
        <div class="queue-status-box" id="queue-box-inner">
            <div class="queue-header">
                <div class="queue-spinner-ring" id="queue-spinner"></div>
                <div class="queue-header-text">
                    <h3 id="queue-title">Đang điều phối gửi phiếu đánh giá...</h3>
                    <p id="queue-desc">Hệ thống đang xếp hàng gửi để bảo vệ dữ liệu không bị nghẽn mạng.</p>
                </div>
            </div>
            
            <div class="queue-steps">
                <div class="queue-step-item active" id="q-step-1">
                    <span>⏳</span> <span>1. Khởi tạo hồ sơ</span>
                </div>
                <div class="queue-step-item" id="q-step-2">
                    <span>⚪</span> <span>2. Nộp câu trả lời</span>
                </div>
                <div class="queue-step-item" id="q-step-3">
                    <span>⚪</span> <span>3. Chấm điểm & Xếp loại</span>
                </div>
            </div>

            <div class="queue-live-alert info" id="queue-alert-box">
                <span id="queue-alert-icon">🚀</span>
                <span id="queue-alert-text">Đang kết nối đến máy chủ an toàn...</span>
            </div>

            <div class="queue-backup-badge">
                <span>🛡️ Đã lưu an toàn trên máy (${totalAnswered} câu trả lời)</span>
                <span id="queue-retry-status" style="font-weight: 600;">Đang gửi lần 1...</span>
            </div>
        </div>
    `;
    queueArea.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function renderQueueExhaustedUI(error) {
    const queueArea = document.getElementById('submission-queue-area');
    if (!queueArea) return;

    const totalAnswered = Object.keys(surveyState.answers || {}).length;
    queueArea.style.display = 'block';
    queueArea.innerHTML = `
        <div class="queue-status-box" style="border-color: var(--accent-red); background: rgba(239, 68, 68, 0.03);">
            <div class="queue-header">
                <div style="font-size: 2.2rem; flex-shrink: 0;">⚠️</div>
                <div class="queue-header-text">
                    <h3 style="color: var(--accent-red);">Chưa thể hoàn tất kết nối tới máy chủ</h3>
                    <p>Lưu lượng truy cập hiện tại đang đạt ngưỡng tối đa hoặc mạng của bạn bị gián đoạn.</p>
                </div>
            </div>
            <div class="queue-live-alert error" style="margin-bottom: 16px;">
                <span>❌</span>
                <span><strong>Nguyên nhân:</strong> ${error.message || 'Hết thời gian chờ phản hồi'}</span>
            </div>
            <p style="font-size: 0.9rem; color: var(--text-secondary); margin-bottom: 20px; line-height: 1.6;">
                🛡️ <strong>Bạn yên tâm:</strong> Toàn bộ <strong>${totalAnswered} câu trả lời</strong> và thông tin cơ sở đã được sao lưu an toàn trong trình duyệt. Dữ liệu của bạn không bị mất!
            </p>
            <div style="display: flex; gap: 12px; flex-wrap: wrap;">
                <button class="btn btn-primary btn-lg" onclick="submitSurvey()">🔄 Thử gửi lại ngay</button>
                <button class="btn btn-outline btn-lg" onclick="exportDraftBackup()">💾 Tải bản sao lưu (.json)</button>
                <button class="btn btn-secondary" onclick="restoreNavFromQueue()">← Xem lại câu trả lời</button>
            </div>
        </div>
    `;
}

function restoreNavFromQueue() {
    const nav = document.getElementById('survey-nav-actions');
    const queueArea = document.getElementById('submission-queue-area');
    if (nav) nav.style.display = 'flex';
    if (queueArea) queueArea.style.display = 'none';
}

async function runWithQueueRetry(stepName, fn, maxRetries = 6) {
    let attempt = 0;
    while (attempt < maxRetries) {
        attempt++;
        try {
            updateQueueRetryStatus(attempt === 1 ? 'Đang gửi...' : `Đang thử lại (Lần ${attempt}/${maxRetries})...`);
            return await fn();
        } catch (error) {
            console.warn(`[Queue Retry] ${stepName} failed attempt ${attempt}/${maxRetries}:`, error);

            // Don't retry on Auth error (401) or Validation error (422)
            if (error.status === 401 || error.status === 422) {
                throw error;
            }

            if (attempt >= maxRetries) {
                throw error;
            }

            // Exponential backoff with random jitter
            const backoffDelays = [0, 3, 5, 8, 12, 18];
            const baseWait = backoffDelays[attempt] || 15;
            const jitter = Math.floor(Math.random() * 2000);
            const totalWaitMs = baseWait * 1000 + jitter;
            const totalWaitSec = Math.round(totalWaitMs / 1000);

            // Countdown timer UI
            for (let sec = totalWaitSec; sec > 0; sec--) {
                updateQueueAlert(
                    'waiting',
                    '⏳',
                    `Máy chủ đang tiếp nhận nhiều phiếu cùng lúc. Bài của bạn đang trong hàng đợi xử lý.<br>Hệ thống tự động gửi lại sau <strong>${sec} giây</strong> (Lần ${attempt + 1}/${maxRetries}). Vui lòng giữ tab này!`
                );
                updateQueueRetryStatus(`Chờ thử lại trong ${sec}s (${attempt}/${maxRetries})`);
                await new Promise(r => setTimeout(r, 1000));
            }

            updateQueueAlert('info', '🔄', `Đang kết nối lại máy chủ (${stepName})...`);
        }
    }
}

async function submitSurvey() {
    if (surveyState.isSubmitting) return;
    surveyState.isSubmitting = true;

    // Persist latest state
    saveSurveyDraft();

    // Prevent accidental reload or close
    window.addEventListener('beforeunload', preventTabClose);

    // Show queue UI
    showQueuePanel();

    try {
        // Step 1: Start assessment session (idempotent, reuse if already obtained)
        updateQueueStep(1, 'active');
        updateQueueAlert('info', '🚀', 'Đang khởi tạo phiên đánh giá trên hệ thống...');
        
        if (!surveyState.activeAssessmentId) {
            const assessment = await runWithQueueRetry('Khởi tạo hồ sơ', async () => {
                return await api.post('/survey/start', surveyState.facilityInfo, { timeoutMs: 25000 });
            });
            surveyState.activeAssessmentId = assessment.id;
            saveSurveyDraft();
        }
        updateQueueStep(1, 'done');

        // Step 2: Submit all answers in bulk
        updateQueueStep(2, 'active');
        updateQueueAlert('info', '📤', 'Đang lưu danh sách câu trả lời vào máy chủ...');
        const answersList = Object.entries(surveyState.answers).map(([qId, optId]) => ({
            assessment_id: surveyState.activeAssessmentId,
            question_id: parseInt(qId),
            selected_option_id: optId,
        }));

        await runWithQueueRetry('Nộp câu trả lời', async () => {
            return await api.post('/survey/submit-all', {
                assessment_id: surveyState.activeAssessmentId,
                answers: answersList,
            }, { timeoutMs: 25000 });
        });
        updateQueueStep(2, 'done');

        // Step 3: Complete assessment and calculate score
        updateQueueStep(3, 'active');
        updateQueueAlert('info', '📊', 'Đang tính toán ma trận nguy cơ và hoàn tất đánh giá...');
        await runWithQueueRetry('Chấm điểm hoàn tất', async () => {
            return await api.post(`/survey/complete/${surveyState.activeAssessmentId}`, {}, { timeoutMs: 25000 });
        });
        updateQueueStep(3, 'done');

        // Step 4: Finished!
        updateQueueAlert('success', '🎉', 'Đã nộp bài thành công! Đang chuyển hướng đến kết quả...');
        updateQueueRetryStatus('Hoàn thành 100%');

        // Async AI trigger
        api.post(`/ai/analyze/${surveyState.activeAssessmentId}`, {}, { timeoutMs: 60000 }).catch(() => {});

        const finalAssessmentId = surveyState.activeAssessmentId;
        clearSurveyDraft();
        window.removeEventListener('beforeunload', preventTabClose);
        surveyState.isSubmitting = false;

        setTimeout(() => {
            window.location.href = `/result.html?id=${finalAssessmentId}`;
        }, 1200);

    } catch (error) {
        console.error('Submission failed after retries:', error);
        window.removeEventListener('beforeunload', preventTabClose);
        surveyState.isSubmitting = false;
        renderQueueExhaustedUI(error);
    }
}

// Map Picker Logic
let pickerMap = null;
let pickerMarker = null;

function openMapPicker() {
    // Create modal dynamically
    const modalHtml = `
    <div id="mapPickerModal" style="position: fixed; inset: 0; z-index: 9999; display: flex; align-items: center; justify-content: center; background: rgba(0,0,0,0.7); padding: 20px;">
        <div style="background: var(--bg-card); width: 100%; max-width: 600px; border-radius: 8px; overflow: hidden; display: flex; flex-direction: column;">
            <div style="padding: 16px; border-bottom: 1px solid var(--border-color); display: flex; justify-content: space-between; align-items: center;">
                <h3 style="margin: 0;">Chọn vị trí cơ sở</h3>
                <button onclick="closeMapPicker()" style="background: transparent; border: none; font-size: 1.5rem; color: var(--text-muted); cursor: pointer;">&times;</button>
            </div>
            <div id="picker-map-container" style="height: 400px; width: 100%;"></div>
            <div style="padding: 16px; text-align: right; background: var(--bg-secondary);">
                <button onclick="closeMapPicker()" class="btn btn-outline" style="margin-right: 8px;">Hủy</button>
                <button onclick="confirmMapPicker()" class="btn btn-primary">Xác nhận chọn</button>
            </div>
        </div>
    </div>`;
    
    document.body.insertAdjacentHTML('beforeend', modalHtml);
    
    // Init map
    setTimeout(() => {
        const center = surveyState.userLocation ? 
             [surveyState.userLocation.latitude, surveyState.userLocation.longitude] : 
             [21.0285, 105.8542]; // Default to Hanoi
             
        pickerMap = L.map('picker-map-container').setView(center, 13);
        L.tileLayer('https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}', {
            attribution: '&copy; Google Maps',
            maxZoom: 20,
            subdomains: ['mt0', 'mt1', 'mt2', 'mt3']
        }).addTo(pickerMap);
        
        pickerMarker = L.marker(center, {draggable: true}).addTo(pickerMap);
        
        pickerMap.on('click', function(e) {
            pickerMarker.setLatLng(e.latlng);
        });
    }, 100);
}

function closeMapPicker() {
    const modal = document.getElementById('mapPickerModal');
    if(modal) {
        modal.remove();
        pickerMap = null;
        pickerMarker = null;
    }
}

function confirmMapPicker() {
    if(pickerMarker) {
        const pos = pickerMarker.getLatLng();
        surveyState.userLocation = {
            latitude: pos.lat,
            longitude: pos.lng
        };
        const textBtn = document.getElementById('map-picker-text');
        if(textBtn) {
            textBtn.innerHTML = `<span style="color:#22c55e">✓ Đã chọn: ${pos.lat.toFixed(4)}, ${pos.lng.toFixed(4)}</span>`;
        }
    }
    closeMapPicker();
}
