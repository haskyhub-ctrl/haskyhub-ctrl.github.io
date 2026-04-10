/**
 * FRAS Survey JS
 * Handles the multi-step survey flow
 */

let surveyState = {
    categories: [],
    currentStep: 0, // 0 = facility info, 1..N = categories, N+1 = review
    answers: {},     // { questionId: optionId }
    assessment: null,
    facilityInfo: {},
    userLocation: null, // { latitude, longitude }
};

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
            },
            (err) => {
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
    const info = surveyState.facilityInfo;
    container.innerHTML = `
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
                            <div class="facility-type-option ${info.facility_type === t.value ? 'selected' : ''}" data-value="${t.value}">
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
    const info = surveyState.facilityInfo;
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
                    <div class="review-item"><span class="label">Tên cơ sở:</span><span class="value">${info.facility_name}</span></div>
                    <div class="review-item"><span class="label">Loại hình:</span><span class="value">${info.facility_type || 'N/A'}</span></div>
                    <div class="review-item"><span class="label">Địa chỉ:</span><span class="value">${info.facility_address || 'N/A'}</span></div>
                </div>
                
                ${categoriesReview}
            </div>
            
            <div class="survey-nav">
                <button class="btn btn-secondary" onclick="prevStep()">← Quay lại</button>
                <button class="btn btn-primary btn-lg" onclick="submitSurvey()" id="submit-btn">🔥 Gửi Đánh giá</button>
            </div>
        </div>
    `;
}

function prevStep() {
    if (surveyState.currentStep > 0) {
        surveyState.currentStep--;
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
        // Load categories filtered by ALL selected facility types
        await loadCategoriesForFacilityType(surveyState.facilityInfo.facility_type);
    }

    if (surveyState.currentStep < getTotalSteps() - 1) {
        surveyState.currentStep++;
        renderStep();
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
}

async function submitSurvey() {
    const btn = document.getElementById('submit-btn');
    btn.disabled = true;
    btn.innerHTML = '<span class="loading-spinner"></span> Đang xử lý...';

    try {
        // 1. Start assessment
        const assessment = await api.post('/survey/start', surveyState.facilityInfo);

        // 2. Submit all answers
        const answersList = Object.entries(surveyState.answers).map(([qId, optId]) => ({
            assessment_id: assessment.id,
            question_id: parseInt(qId),
            selected_option_id: optId,
        }));

        await api.post('/survey/submit-all', {
            assessment_id: assessment.id,
            answers: answersList,
        });

        // 3. Complete assessment
        const result = await api.post(`/survey/complete/${assessment.id}`, {});

        // 4. Trigger AI analysis (async, don't wait)
        api.post(`/ai/analyze/${assessment.id}`, {}).catch(() => { });

        showToast('Đánh giá hoàn thành!');
        window.location.href = `/result.html?id=${assessment.id}`;

    } catch (error) {
        showToast(error.message, 'error');
        btn.disabled = false;
        btn.textContent = '🔥 Gửi Đánh giá';
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
        L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
            attribution: '&copy; CARTO'
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
