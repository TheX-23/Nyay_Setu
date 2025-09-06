// Global variables
let currentTab = 'chat';
let chatHistory = [];
let formFields = {};
let authEmailCache = '';
let serverConnected = false;

// API Configuration with resilient auto-detection and fallback
// Prefer injected base, then same-origin if served by backend, else fallback candidates
const API_BASE_URL = (function() {
    const injected = typeof window !== 'undefined' ? window.__API_BASE_URL__ : '';
    if (injected && typeof injected === 'string') return injected.replace(/\/$/, '');
    if (typeof window !== 'undefined') {
        // If we are on the API origin (Flask serving static), use relative paths
        if (window.location.port === '5000') return '';
    }
    return 'http://127.0.0.1:5000';
})();

let ACTIVE_API_BASE_URL = API_BASE_URL;

async function detectApiBaseUrl() {
    const candidates = [];
    // 1) Explicit injection
    if (API_BASE_URL) candidates.push(API_BASE_URL);
    // 2) Same-origin relative
    candidates.push('');
    // 3) Common local dev hosts
    candidates.push('http://127.0.0.1:5000');
    candidates.push('http://localhost:5000');
    // 4) If page served from a LAN host, try same host:5000
    try {
        if (typeof window !== 'undefined' && window.location.hostname && window.location.hostname !== 'localhost') {
            candidates.push(`http://${window.location.hostname}:5000`);
        }
    } catch {}

    for (const base of candidates) {
        try {
            const controller = new AbortController();
            const t = setTimeout(() => controller.abort(), 1500);
            const url = `${base}/health`;
            const res = await fetch(url, { signal: controller.signal, mode: 'cors' });
            clearTimeout(t);
            if (res.ok) {
                ACTIVE_API_BASE_URL = base;
                serverConnected = true;
                updateConnectionStatus('connected');
                if (base && base !== API_BASE_URL) {
                    showNotification(`Connected to API at ${base}`, 'info');
                }
                return base;
            }
        } catch {}
    }
    // Keep whatever we had; UI will surface errors per-request
    serverConnected = false;
    updateConnectionStatus('disconnected');
    return ACTIVE_API_BASE_URL;
}

async function apiFetch(path, options = {}) {
    // Ensure we have a working base (non-blocking: if initial check fails, we still try the call)
    detectApiBaseUrl().catch(() => {});
    const basesToTry = [ACTIVE_API_BASE_URL];
    // Add alternates in case of network failure
    const alternates = ['', 'http://127.0.0.1:5000', 'http://localhost:5000'];
    try {
        if (typeof window !== 'undefined' && window.location.hostname && window.location.hostname !== 'localhost') {
            alternates.push(`http://${window.location.hostname}:5000`);
        }
    } catch {}
    for (const alt of alternates) {
        if (!basesToTry.includes(alt)) basesToTry.push(alt);
    }

    let lastError;
    for (const base of basesToTry) {
        try {
            const url = `${base}${path}`;
            const resp = await fetch(url, { mode: 'cors', ...options });
            if (!resp.ok) return resp; // Non-network error; return it to caller
            // Success; update active base and return
            ACTIVE_API_BASE_URL = base;
            serverConnected = true;
            updateConnectionStatus('connected');
            return resp;
        } catch (e) {
            lastError = e;
            continue; // Try next base on network errors
        }
    }
    // Throw last network error if all bases failed
    serverConnected = false;
    updateConnectionStatus('disconnected');
    throw lastError || new Error('Network error');
}



// Connection Status Management
function updateConnectionStatus(status) {
    const statusElement = document.getElementById('connectionStatus');
    const errorMessage = document.getElementById('serverErrorMessage');
    
    if (!statusElement) return;
    
    statusElement.className = `connection-status ${status}`;
    
    switch (status) {
        case 'connected':
            statusElement.innerHTML = '<i class="fas fa-circle"></i> Connected';
            if (errorMessage) errorMessage.style.display = 'none';
            break;
        case 'disconnected':
            statusElement.innerHTML = '<i class="fas fa-circle"></i> Disconnected';
            if (errorMessage) errorMessage.style.display = 'block';
            break;
        case 'checking':
            statusElement.innerHTML = '<i class="fas fa-circle"></i> Checking connection...';
            if (errorMessage) errorMessage.style.display = 'none';
            break;
    }
}

async function checkServerConnection() {
    updateConnectionStatus('checking');
    try {
        await detectApiBaseUrl();
        if (serverConnected) {
            showNotification('Successfully connected to server!', 'success');
        } else {
            showNotification('Failed to connect to server. Please check if the backend is running.', 'error');
        }
    } catch (error) {
        showNotification('Connection check failed: ' + error.message, 'error');
    }
}

// Tab Navigation
function initializeTabs() {
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');
    
    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const targetTab = button.getAttribute('data-tab');
            switchTab(targetTab);
        });
    });
}

function switchTab(tabName) {
    // Update active tab button
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    const tabBtn = document.querySelector(`[data-tab="${tabName}"]`);
    if (tabBtn) tabBtn.classList.add('active');
    
    // Update active tab content
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.remove('active');
    });
    const tabContent = document.getElementById(tabName);
    if (tabContent) tabContent.classList.add('active');
    
    currentTab = tabName;
    
    // Load form fields if switching to forms tab
    if (tabName === 'forms') {
        loadFormFields();
    }
}

// Event Listeners
function setupEventListeners() {
    // Enter key support for chat input
    const questionInput = document.getElementById('question');
    if (questionInput) {
        questionInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                askChatbot();
            }
        });
    }
    
    // Form type change handler
    const formTypeSelect = document.getElementById('formType');
    if (formTypeSelect) {
        formTypeSelect.addEventListener('change', function() {
            loadFormFields();
        });
    }

    const btnRegister = document.getElementById('btnRegister');
    const btnLogin = document.getElementById('btnLogin');
    const btnLogout = document.getElementById('btnLogout');
    const btnGoogle = document.getElementById('btnGoogle');
    const btnDevLogin = document.getElementById('btnDevLogin');
    if (btnRegister) btnRegister.addEventListener('click', registerUser);
    if (btnLogin) btnLogin.addEventListener('click', loginUser);
    if (btnLogout) btnLogout.addEventListener('click', logoutUser);
    if (btnGoogle) btnGoogle.addEventListener('click', () => startOAuth('google'));
    if (btnDevLogin) btnDevLogin.addEventListener('click', devLogin);

    const btnGeneratePdf = document.getElementById('btnGeneratePdf');
    if (btnGeneratePdf) btnGeneratePdf.addEventListener('click', downloadFormPdf);
}

// Chat Functionality
async function askChatbot() {
    const questionInput = document.getElementById('question');
    const languageSelect = document.getElementById('language');
    if (!questionInput || !languageSelect) return;

    const question = questionInput.value.trim();
    const language = languageSelect.value;

    if (!question) {
        showNotification('Please enter a question', 'error');
        return;
    }

    // Check server connection first
    if (!serverConnected) {
        showNotification('Server is not connected. Please check if the backend is running.', 'error');
        updateConnectionStatus('disconnected');
        return;
    }

    const token = getToken();
    if (!token) {
        showNotification('Please login first to use chat', 'warning');
        return;
    }

    // Add user message to chat
    addMessageToChat('user', question);

    // Clear input and disable while loading
    questionInput.value = '';
    questionInput.disabled = true;

    // Show loading
    showLoading(true);

    try {
        const response = await apiFetch(`/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ question, language })
        });

        if (!response.ok) {
            let errorMsg = `HTTP error! status: ${response.status}`;
            try {
                const errData = await response.json();
                if (errData && errData.error) errorMsg = errData.error;
            } catch {}
            throw new Error(errorMsg);
        }

        const data = await response.json();

        if (data.error) {
            throw new Error(data.error);
        }

        // Add bot response to chat
        addMessageToChat('bot', data.answer);

        // Save to chat history
        saveChatToHistory(question, data.answer, language);

    } catch (error) {
        console.error('Error:', error);
        addMessageToChat('bot', `Sorry, I encountered an error: ${error.message}. Please try again or check your connection.`);
    } finally {
        showLoading(false);
        questionInput.disabled = false;
        questionInput.focus();
    }
}

function addMessageToChat(sender, message, pushToHistory = true) {
    const chatMessages = document.getElementById('chatMessages');
    if (!chatMessages) return;

    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;

    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';

    if (sender === 'bot') {
        avatar.innerHTML = '<i class="fas fa-balance-scale"></i>';
    } else {
        avatar.innerHTML = '<i class="fas fa-user"></i>';
    }

    const content = document.createElement('div');
    content.className = 'message-content';
    content.innerHTML = `<p>${escapeHTML(message)}</p>`;

    messageDiv.appendChild(avatar);
    messageDiv.appendChild(content);

    chatMessages.appendChild(messageDiv);

    // Scroll to bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;

    // Add to chat history if needed
    if (pushToHistory) {
        chatHistory.push({ sender, message, timestamp: new Date() });
    }
}

// Escape HTML to prevent XSS
function escapeHTML(str) {
    return str.replace(/[&<>"']/g, function(m) {
        return ({
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#39;'
        })[m];
    });
}

// Form Generation
function initializeFormFields() {
    // Default form fields for different form types
    formFields = {
        'FIR': {
            'complainant_details': {
                'name': 'Full Name',
                'address': 'Complete Address',
                'phone': 'Phone Number',
                'email': 'Email Address',
                'id_proof': 'ID Proof Type and Number'
            },
            'incident_details': {
                'date_time': 'Date and Time of Incident',
                'location': 'Location of Incident',
                'description': 'Detailed Description of Incident',
                'loss_damage': 'Loss or Damage Suffered'
            },
            'accused_details': {
                'name': 'Name of Accused',
                'address': 'Address of Accused',
                'description': 'Description of Accused'
            },
            'witness_details': {
                'witness_names': 'Names of Witnesses',
                'witness_addresses': 'Addresses of Witnesses',
                'witness_phones': 'Phone Numbers of Witnesses'
            },
            'evidence_details': {
                'documents': 'Supporting Documents',
                'physical_evidence': 'Physical Evidence',
                'digital_evidence': 'Digital Evidence'
            }
        },
        'RTI': {
            'applicant_details': {
                'name': 'Full Name',
                'address': 'Complete Address',
                'phone': 'Phone Number',
                'email': 'Email Address',
                'citizenship': 'Citizenship'
            },
            'information_requested': {
                'subject': 'Subject of Information',
                'details': 'Detailed Description of Information Required',
                'period': 'Time Period for Information',
                'format': 'Preferred Format of Information'
            },
            'public_authority': {
                'authority_name': 'Name of Public Authority',
                'officer_name': 'Name of Public Information Officer',
                'address': 'Address of Public Authority'
            },
            'grounds_for_request': {
                'reason': 'Reason for Requesting Information',
                'public_interest': 'Public Interest Justification'
            }
        },
        'COMPLAINT': {
            'complainant_details': {
                'name': 'Full Name',
                'address': 'Complete Address',
                'phone': 'Phone Number',
                'email': 'Email Address',
                'id_proof': 'ID Proof Type and Number'
            },
            'complaint_details': {
                'subject': 'Subject of Complaint',
                'description': 'Detailed Description of Complaint',
                'date_occurred': 'Date When Issue Occurred',
                'previous_actions': 'Previous Actions Taken'
            },
            'relief_sought': {
                'compensation': 'Compensation Sought',
                'action_required': 'Action Required from Authority',
                'timeframe': 'Expected Timeframe for Resolution'
            },
            'supporting_documents': {
                'documents': 'List of Supporting Documents',
                'photographs': 'Photographs (if any)',
                'correspondence': 'Previous Correspondence'
            }
        },
        'APPEAL': {
            'appellant_details': {
                'name': 'Full Name of Appellant',
                'address': 'Complete Address',
                'phone': 'Phone Number',
                'email': 'Email Address',
                'representative': 'Legal Representative (if any)'
            },
            'original_order_details': {
                'order_number': 'Original Order Number',
                'order_date': 'Date of Original Order',
                'issuing_authority': 'Authority that Issued Order',
                'order_summary': 'Summary of Original Order'
            },
            'grounds_for_appeal': {
                'legal_grounds': 'Legal Grounds for Appeal',
                'errors': 'Errors in Original Order',
                'new_evidence': 'New Evidence Available'
            },
            'relief_sought': {
                'compensation': 'Compensation Sought',
                'action_required': 'Action Required from Authority',
                'timeframe': 'Expected Timeframe for Resolution'
            }
        }
    };
}

function loadFormFields() {
    const formTypeSelect = document.getElementById('formType');
    const formFieldsContainer = document.getElementById('formFields');
    if (!formTypeSelect || !formFieldsContainer) return;

    const formType = formTypeSelect.value;

    if (!formFields[formType]) {
        formFieldsContainer.innerHTML = '<p>Form type not supported.</p>';
        return;
    }

    let fieldsHTML = '';

    Object.entries(formFields[formType]).forEach(([section, fields]) => {
        const sectionTitle = section.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
        fieldsHTML += `<h3>${sectionTitle}</h3>`;

        Object.entries(fields).forEach(([fieldKey, fieldLabel]) => {
            // Use textarea for long text fields
            const isTextarea = ['description', 'details', 'grounds_for_request', 'order_summary', 'public_interest', 'previous_actions'].includes(fieldKey);

            if (isTextarea) {
                fieldsHTML += `
                    <div class="form-field">
                        <label for="${fieldKey}">${fieldLabel}:</label>
                        <textarea id="${fieldKey}" placeholder="Enter ${fieldLabel.toLowerCase()}"></textarea>
                    </div>
                `;
            } else {
                fieldsHTML += `
                    <div class="form-field">
                        <label for="${fieldKey}">${fieldLabel}:</label>
                        <input type="text" id="${fieldKey}" placeholder="Enter ${fieldLabel.toLowerCase()}">
                    </div>
                `;
            }
        });
    });

    formFieldsContainer.innerHTML = fieldsHTML;
}

async function generateForm() {
    const formTypeSelect = document.getElementById('formType');
    const formFieldsContainer = document.getElementById('formFields');
    const generatedFormContainer = document.getElementById('generatedForm');
    if (!formTypeSelect || !formFieldsContainer || !generatedFormContainer) return;

    const formType = formTypeSelect.value;

    // Collect form data
    const responses = {};
    const formInputs = formFieldsContainer.querySelectorAll('input, textarea');

    formInputs.forEach(input => {
        if (input.value.trim()) {
            responses[input.id] = input.value.trim();
        }
    });

    if (Object.keys(responses).length === 0) {
        showNotification('Please fill in at least one field', 'warning');
        return;
    }

    // Check server connection first
    if (!serverConnected) {
        showNotification('Server is not connected. Please check if the backend is running.', 'error');
        updateConnectionStatus('disconnected');
        return;
    }

    showLoading(true);

    const token = getToken();
    if (!token) {
        showNotification('Please login first to generate forms', 'warning');
        return;
    }

    try {
        const response = await apiFetch(`/generate_form`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ form_type: formType, responses })
        });

        if (!response.ok) {
            let errorMsg = `HTTP error! status: ${response.status}`;
            try {
                const errData = await response.json();
                if (errData && errData.error) errorMsg = errData.error;
            } catch {}
            throw new Error(errorMsg);
        }

        const data = await response.json();

        if (data.error) {
            throw new Error(data.error);
        }

        // Display generated form
        generatedFormContainer.textContent = data.form;
        generatedFormContainer.style.display = 'block';

        // Scroll to generated form
        generatedFormContainer.scrollIntoView({ behavior: 'smooth' });

        showNotification('Form generated successfully!', 'success');

    } catch (error) {
        console.error('Error:', error);
        showNotification(`Error generating form: ${error.message}`, 'error');
    } finally {
        showLoading(false);
    }
}

// Utility Functions
function showLoading(show) {
    const loadingOverlay = document.getElementById('loadingOverlay');
    if (!loadingOverlay) return;
    loadingOverlay.style.display = show ? 'flex' : 'none';
}

function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <i class="fas fa-${getNotificationIcon(type)}"></i>
        <span>${escapeHTML(message)}</span>
        <button onclick="this.parentElement.remove()" class="notification-close">
            <i class="fas fa-times"></i>
        </button>
    `;

    // Add styles
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${getNotificationColor(type)};
        color: white;
        padding: 15px 20px;
        border-radius: 8px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.15);
        z-index: 1001;
        display: flex;
        align-items: center;
        gap: 10px;
        max-width: 400px;
        animation: slideInRight 0.3s ease-out;
    `;

    // Add to page
    document.body.appendChild(notification);

    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (notification.parentElement) {
            notification.remove();
        }
    }, 5000);
}

function getNotificationIcon(type) {
    const icons = {
        'success': 'check-circle',
        'error': 'exclamation-circle',
        'warning': 'exclamation-triangle',
        'info': 'info-circle'
    };
    return icons[type] || 'info-circle';
}

function getNotificationColor(type) {
    const colors = {
        'success': '#10b981',
        'error': '#ef4444',
        'warning': '#f59e0b',
        'info': '#3b82f6'
    };
    return colors[type] || '#3b82f6';
}

// Chat History Management
function saveChatToHistory(question, answer, language) {
    const chatEntry = {
        question,
        answer,
        language,
        timestamp: new Date().toISOString()
    };

    // Get existing history from localStorage
    let history = JSON.parse(localStorage.getItem('nyaysetu_chat_history') || '[]');

    // Add new entry
    history.push(chatEntry);

    // Keep only last 50 entries
    if (history.length > 50) {
        history = history.slice(-50);
    }

    // Save to localStorage
    localStorage.setItem('nyaysetu_chat_history', JSON.stringify(history));
}

// Display chat history in UI
function displayChatHistory() {
    const chatMessages = document.getElementById('chatMessages');
    if (!chatMessages) return;
    chatMessages.innerHTML = '';
    const history = JSON.parse(localStorage.getItem('nyaysetu_chat_history') || '[]');
    history.forEach(entry => {
        addMessageToChat('user', entry.question, false);
        addMessageToChat('bot', entry.answer, false);
    });
}

// Load chat history on startup
function loadChatHistory() {
    chatHistory = JSON.parse(localStorage.getItem('nyaysetu_chat_history') || '[]');
    displayChatHistory();
}

// Add CSS for notifications
const notificationStyles = document.createElement('style');
notificationStyles.textContent = `
    @keyframes slideInRight {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    .notification-close {
        background: none;
        border: none;
        color: white;
        cursor: pointer;
        padding: 0;
        margin-left: auto;
        opacity: 0.8;
        transition: opacity 0.2s;
    }
    
    .notification-close:hover {
        opacity: 1;
    }
`;
document.head.appendChild(notificationStyles);

// Export functions for global access
window.askChatbot = askChatbot;
window.generateForm = generateForm;
window.switchTab = switchTab;
window.checkServerConnection = checkServerConnection;

// --- Auth Helpers and Actions ---

function getToken() {
    return localStorage.getItem('nyaysetu_token') || '';
}

function setToken(token, email) {
    localStorage.setItem('nyaysetu_token', token);
    if (email) localStorage.setItem('nyaysetu_email', email);
    updateAuthUI();
}

function clearToken() {
    localStorage.removeItem('nyaysetu_token');
    updateAuthUI();
}

function updateAuthUI() {
    const btnLogin = document.getElementById('btnLogin');
    const btnRegister = document.getElementById('btnRegister');
    const btnLogout = document.getElementById('btnLogout');
    const btnGoogle = document.getElementById('btnGoogle');
    const btnFacebook = document.getElementById('btnFacebook');
    const btnDevLogin = document.getElementById('btnDevLogin');
    const authStatus = document.getElementById('authStatus');
    const emailInput = document.getElementById('authEmail');
    const loggedIn = !!getToken();
    if (btnLogin) btnLogin.style.display = loggedIn ? 'none' : 'inline-block';
    if (btnRegister) btnRegister.style.display = loggedIn ? 'none' : 'inline-block';
    if (btnLogout) btnLogout.style.display = loggedIn ? 'inline-block' : 'none';
    if (btnGoogle) btnGoogle.style.display = loggedIn ? 'none' : 'inline-block';
    if (btnFacebook) btnFacebook.style.display = loggedIn ? 'none' : 'inline-block';
    if (btnDevLogin) btnDevLogin.style.display = loggedIn ? 'none' : 'inline-block';
    if (authStatus) {
        const email = localStorage.getItem('nyaysetu_email') || authEmailCache || '';
        authStatus.textContent = loggedIn ? `Logged in${email ? ' as ' + email : ''}` : 'Not logged in';
    }
    if (emailInput && !emailInput.value && localStorage.getItem('nyaysetu_email')) {
        emailInput.value = localStorage.getItem('nyaysetu_email');
    }
}

// --- OAuth ---
function startOAuth(provider) {
    const url = `${API_BASE_URL}/auth/oauth/${provider}/start`;
    const w = 520; const h = 600;
    const left = window.screenX + Math.max(0, (window.outerWidth - w) / 2);
    const top = window.screenY + Math.max(0, (window.outerHeight - h) / 2);
    window.open(url, 'oauth_login', `width=${w},height=${h},left=${left},top=${top}`);
}

window.addEventListener('message', (event) => {
    try {
        const data = event.data || {};
        if (data && data.type === 'oauth_token' && data.token) {
            setToken(data.token, data.email || '');
            if (data.provider) {
                showNotification(`Logged in with ${data.provider}.`, 'success');
            } else {
                showNotification('Logged in successfully.', 'success');
            }
        }
    } catch {}
});

async function downloadFormPdf() {
    const formTypeSelect = document.getElementById('formType');
    const formFieldsContainer = document.getElementById('formFields');
    if (!formTypeSelect || !formFieldsContainer) return;
    const token = getToken();
    if (!token) {
        showNotification('Please login first to generate PDF', 'warning');
        return;
    }
    const formType = formTypeSelect.value;
    const responses = {};
    formFieldsContainer.querySelectorAll('input, textarea').forEach(input => {
        if (input.value.trim()) responses[input.id] = input.value.trim();
    });
    try {
        const res = await apiFetch(`/generate_form_pdf`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ form_type: formType, responses })
        });
        if (!res.ok) {
            let msg = `HTTP ${res.status}`;
            try { const j = await res.json(); if (j.error) msg = j.error; } catch {}
            throw new Error(msg);
        }
        const blob = await res.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${formType}_NyaySetu.pdf`;
        document.body.appendChild(a);
        a.click();
        a.remove();
        window.URL.revokeObjectURL(url);
        showNotification('PDF downloaded.', 'success');
    } catch (e) {
        showNotification(`Failed to download PDF: ${e.message}`, 'error');
    }
}

async function devLogin() {
    try {
        const emailEl = document.getElementById('authEmail');
        const email = (emailEl?.value || `dev_${Date.now()}@example.com`).trim();
        const res = await apiFetch(`/auth/oauth/dev`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email })
        });
        const data = await res.json().catch(() => ({}));
        if (!res.ok) throw new Error(data.error || `HTTP ${res.status}`);
        if (!data.token) throw new Error('No token returned');
        setToken(data.token, email);
        localStorage.setItem('nyaysetu_email', email);
        showNotification('Dev login success.', 'success');
    } catch (e) {
        showNotification(`Dev login failed: ${e.message}`, 'error');
    }
}

// Improve chat errors
// If unauthorized, prompt login instead of generic network error
const _origAskChatbot = askChatbot;
askChatbot = async function() {
    try { await _origAskChatbot(); }
    catch (e) {
        if ((e.message || '').toLowerCase().includes('unauthorized')) {
            showNotification('Please login to use chat.', 'warning');
        } else {
            showNotification(`Chat failed: ${e.message}`, 'error');
        }
    }
}

async function registerUser() {
    const emailEl = document.getElementById('authEmail');
    const passEl = document.getElementById('authPassword');
    const email = (emailEl?.value || '').trim();
    const password = passEl?.value || '';
    if (!email || !password) {
        showNotification('Enter email and password to register', 'warning');
        return;
    }
    try {
        const res = await apiFetch(`/auth/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });
        const data = await res.json().catch(() => ({}));
        if (!res.ok) throw new Error(data.error || `HTTP ${res.status}`);
        authEmailCache = email;
        localStorage.setItem('nyaysetu_email', email);
        showNotification('Registered successfully. You can now login.', 'success');
    } catch (e) {
        showNotification(`Register failed: ${e.message}`, 'error');
    }
}

async function loginUser() {
    const emailEl = document.getElementById('authEmail');
    const passEl = document.getElementById('authPassword');
    const email = (emailEl?.value || '').trim();
    const password = passEl?.value || '';
    if (!email || !password) {
        showNotification('Enter email and password to login', 'warning');
        return;
    }
    try {
        const res = await apiFetch(`/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });
        const data = await res.json().catch(() => ({}));
        if (!res.ok) throw new Error(data.error || `HTTP ${res.status}`);
        if (!data.token) throw new Error('No token returned');
        setToken(data.token, email);
        localStorage.setItem('nyaysetu_email', email);
        showNotification('Logged in successfully.', 'success');
    } catch (e) {
        showNotification(`Login failed: ${e.message}`, 'error');
    }
}

function logoutUser() {
    clearToken();
    showNotification('Logged out.', 'info');
}

// Export auth for debugging if needed
window.loginUser = loginUser;
window.registerUser = registerUser;
window.logoutUser = logoutUser;

// Initialize UI and event bindings when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    try {
        initializeTabs();
        setupEventListeners();
        initializeFormFields();
        updateAuthUI();
        loadChatHistory();
        switchTab('chat');
        
        // Check server connection on page load
        setTimeout(() => {
            checkServerConnection();
        }, 1000);
    } catch (e) {
        // Surface any init errors to help diagnose missing elements
        showNotification(`Initialization error: ${e.message}`, 'error');
        // Also log to console for deeper debugging
        console.error('Initialization error', e);
    }
});
