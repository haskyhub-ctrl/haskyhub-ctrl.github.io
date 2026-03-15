/**
 * FRAS Authentication JS
 * Handles login and register forms
 */

function setupLoginForm() {
    const form = document.getElementById('login-form');
    if (!form) return;

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const email = form.querySelector('#email').value.trim();
        const password = form.querySelector('#password').value;
        const btn = form.querySelector('button[type="submit"]');
        const originalText = btn.textContent;

        if (!email || !password) {
            showToast('Vui lòng nhập đầy đủ thông tin', 'error');
            return;
        }

        btn.disabled = true;
        btn.innerHTML = '<span class="loading-spinner"></span> Đang đăng nhập...';

        try {
            await api.login(email, password);
            showToast('Đăng nhập thành công!');
            const user = api.getUser();
            if (user.role === 'admin' || user.role === 'superadmin') {
                window.location.href = '/admin/';
            } else {
                window.location.href = '/dashboard.html';
            }
        } catch (error) {
            showToast(error.message, 'error');
            btn.disabled = false;
            btn.textContent = originalText;
        }
    });
}

function setupRegisterForm() {
    const form = document.getElementById('register-form');
    if (!form) return;

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const data = {
            full_name: form.querySelector('#full_name').value.trim(),
            email: form.querySelector('#email').value.trim(),
            password: form.querySelector('#password').value,
            organization: form.querySelector('#organization')?.value.trim() || null,
            phone: form.querySelector('#phone')?.value.trim() || null,
        };

        const confirm_password = form.querySelector('#confirm_password').value;

        if (!data.full_name || !data.email || !data.password) {
            showToast('Vui lòng nhập đầy đủ thông tin bắt buộc', 'error');
            return;
        }

        if (data.password.length < 6) {
            showToast('Mật khẩu phải có ít nhất 6 ký tự', 'error');
            return;
        }

        if (data.password !== confirm_password) {
            showToast('Mật khẩu xác nhận không khớp', 'error');
            return;
        }

        const btn = form.querySelector('button[type="submit"]');
        btn.disabled = true;
        btn.innerHTML = '<span class="loading-spinner"></span> Đang đăng ký...';

        try {
            await api.register(data);
            showToast('Đăng ký thành công!');
            window.location.href = '/dashboard.html';
        } catch (error) {
            showToast(error.message, 'error');
            btn.disabled = false;
            btn.textContent = 'Đăng ký';
        }
    });
}
