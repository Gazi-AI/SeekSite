/**
 * SeekSite - AI Website Builder
 * Chat system with localStorage persistence
 */

const STORAGE_KEY = 'seeksite_state';

class SeekSiteApp {
    constructor() {
        // Load state from localStorage
        this.state = this.loadState();
        this.isGenerating = false;
        this.abortController = null;
        this.currentView = 'split';
        this.wordWrap = true;
        this._lastBlobUrl = null;
        this._previewTimer = null;
        this._deleteTargetId = null;
        this.currentLang = localStorage.getItem('seeksite_lang') || 'tr';
        // ... (translations mapping as before) ...
        this.translations = {
            tr: {
                status_ready: "Hazir",
                status_generating: "Uretiliyor...",
                new_chat: "Yeni Sohbet",
                history_title: "Sohbet Gecmisi",
                quick_start: "Hizli Baslangic",
                enhances: "Hizli Iyilestirmeler",
                welcome_title: "SeekSite ile Web Sitesi Olustur",
                welcome_sub: "Yapay zeka destekli website builder. Hayalindeki siteyi tanimla, biz olusturalim.",
                input_placeholder: "Web sitenizi tanimlayin...",
                input_placeholder_edit: "Degisiklik isteyin... (orn: 'Renkleri degistir')",
                toast_copied: "Kod kopyalandi!",
                toast_downloaded: "HTML indirildi!",
                toast_fixed: "Kod otomatik duzeltildi",
                modal_title: "Sohbeti Sil",
                modal_text: "Bu sohbeti ve uretilen websiteyi kalici olarak silmek istediginize emin misiniz?",
                modal_cancel: "Iptal",
                modal_confirm: "Evet, Sil"
            },
            en: {
                status_ready: "Ready",
                status_generating: "Generating...",
                new_chat: "New Chat",
                history_title: "Chat History",
                quick_start: "Quick Start",
                enhances: "Quick Enhancements",
                welcome_title: "Build Website with SeekSite",
                welcome_sub: "AI-powered website builder. Describe your dream site, we build it.",
                input_placeholder: "Describe your website...",
                input_placeholder_edit: "Ask for changes... (e.g. 'Change colors')",
                toast_copied: "Code copied!",
                toast_downloaded: "HTML downloaded!",
                toast_fixed: "Code auto-fixed",
                modal_title: "Delete Chat",
                modal_text: "Are you sure you want to permanently delete this chat and the generated website?",
                modal_cancel: "Cancel",
                modal_confirm: "Yes, Delete"
            }
        };

        this.el = {
            sidebar: document.getElementById('sidebar'),
            sidebarClose: document.getElementById('sidebarClose'),
            menuToggle: document.getElementById('menuToggle'),
            workspace: document.getElementById('workspace'),
            welcomeScreen: document.getElementById('welcomeScreen'),
            codePanel: document.getElementById('codePanel'),
            previewPanel: document.getElementById('previewPanel'),
            resizeHandle: document.getElementById('resizeHandle'),
            codeContent: document.getElementById('codeContent'),
            codeContainer: document.getElementById('codeContainer'),
            lineNumbers: document.getElementById('lineNumbers'),
            previewFrame: document.getElementById('previewFrame'),
            previewContainer: document.getElementById('previewContainer'),
            promptInput: document.getElementById('promptInput'),
            charCount: document.getElementById('charCount'),
            btnSend: document.getElementById('btnSend'),
            btnStop: document.getElementById('btnStop'),
            btnCopyCode: document.getElementById('btnCopyCode'),
            btnDownload: document.getElementById('btnDownload'),
            btnNewChat: document.getElementById('btnNewChat'),
            btnWrapCode: document.getElementById('btnWrapCode'),
            btnRefreshPreview: document.getElementById('btnRefreshPreview'),
            btnOpenExternal: document.getElementById('btnOpenExternal'),
            statusDot: document.getElementById('statusDot'),
            statusText: document.getElementById('statusText'),
            toastContainer: document.getElementById('toastContainer'),
            quickPrompts: document.getElementById('quickPrompts'),
            enhanceButtons: document.getElementById('enhanceButtons'),
            chatHistoryList: document.getElementById('chatHistoryList'),
            deleteModal: document.getElementById('deleteModal'),
            modalCancel: document.getElementById('modalCancel'),
            modalConfirm: document.getElementById('modalConfirm'),
            langBtns: document.querySelectorAll('.lang-btn'),
            modelSelect: document.getElementById('modelSelect'),
        };

        this.init();
        this.updateLangUI();
    }

    /* =====================
       State Management (localStorage)
       ===================== */
    loadState() {
        try {
            const saved = localStorage.getItem(STORAGE_KEY);
            if (saved) {
                const parsed = JSON.parse(saved);
                // Make sure structure is valid
                if (parsed.sessions && parsed.activeSessionId !== undefined) {
                    return parsed;
                }
            }
        } catch (e) {
            console.warn('Failed to load state:', e);
        }
        return { sessions: [], activeSessionId: null };
    }

    saveState() {
        try {
            localStorage.setItem(STORAGE_KEY, JSON.stringify(this.state));
        } catch (e) {
            console.warn('Failed to save state:', e);
        }
    }

    createSession() {
        const session = {
            id: Date.now().toString() + '-' + Math.floor(Math.random() * 10000),
            title: 'Yeni Sohbet',
            code: '',
            history: [],
            createdAt: Date.now()
        };
        this.state.sessions.unshift(session); // newest first
        this.state.activeSessionId = session.id;
        this.saveState();
        return session;
    }

    getActiveSession() {
        if (!this.state.activeSessionId || this.state.sessions.length === 0) {
            return null;
        }
        return this.state.sessions.find(s => s.id === this.state.activeSessionId) || null;
    }

    switchToSession(sessionId) {
        this.state.activeSessionId = sessionId;
        this.saveState();

        const session = this.getActiveSession();
        if (session && session.code) {
            // Load cached code
            this.el.codeContent.textContent = session.code;
            this.updateLineNumbers();
            this.el.welcomeScreen.classList.add('hidden');
            this.enableActions();

            // Load preview from cached code
            setTimeout(() => {
                this._doPreviewUpdate(session.code);
            }, 100);
        } else {
            // Empty session
            this.el.codeContent.textContent = '';
            this.updateLineNumbers();
            this.el.welcomeScreen.classList.remove('hidden');
            this.el.previewFrame.src = 'about:blank';
            this.disableActions();
        }

        this.renderChatHistory();
        this.el.promptInput.value = '';
        this.updateCharCount();
        this.updatePlaceholder();
        this.closeSidebar();
    }

    deleteSession(sessionId) {
        this.state.sessions = this.state.sessions.filter(s => s.id !== sessionId);

        if (this.state.activeSessionId === sessionId) {
            if (this.state.sessions.length > 0) {
                this.switchToSession(this.state.sessions[0].id);
            } else {
                this.state.activeSessionId = null;
                this.saveState();
                this.el.codeContent.textContent = '';
                this.updateLineNumbers();
                this.el.welcomeScreen.classList.remove('hidden');
                this.el.previewFrame.src = 'about:blank';
                this.disableActions();
                this.renderChatHistory();
            }
        } else {
            this.saveState();
            this.renderChatHistory();
        }
    }

    /* =====================
       Init
       ===================== */
    init() {
        this.setupEventListeners();
        this.setupResizeHandle();
        this.setView('split');
        this.renderChatHistory();
        this.loadModels();

        // Restore active session
        const active = this.getActiveSession();
        if (active && active.code) {
            this.el.codeContent.textContent = active.code;
            this.updateLineNumbers();
            this.el.welcomeScreen.classList.add('hidden');
            this.enableActions();
            setTimeout(() => this._doPreviewUpdate(active.code), 200);
        } else {
            this.updateLineNumbers();
        }
    }

    /* =====================
       Event Listeners
       ===================== */
    setupEventListeners() {
        // Sidebar
        this.el.menuToggle.addEventListener('click', () => this.toggleSidebar());
        this.el.sidebarClose.addEventListener('click', () => this.closeSidebar());

        // Language Switcher
        this.el.langBtns.forEach(btn => {
            btn.addEventListener('click', () => this.setLanguage(btn.dataset.lang));
        });

        // Mobile overlay
        const overlay = document.createElement('div');
        overlay.className = 'sidebar-overlay';
        overlay.id = 'sidebarOverlay';
        document.body.appendChild(overlay);
        overlay.addEventListener('click', () => this.closeSidebar());

        // New chat
        this.el.btnNewChat.addEventListener('click', () => {
            if (this.isGenerating) return;
            this.createSession();
            this.switchToSession(this.state.activeSessionId);
            this.showToast('Yeni sohbet olusturuldu', 'info');
        });

        // Delete modal
        this.el.modalCancel.addEventListener('click', () => {
            this.el.deleteModal.classList.remove('active');
            this._deleteTargetId = null;
        });
        this.el.modalConfirm.addEventListener('click', () => {
            if (this._deleteTargetId) {
                this.deleteSession(this._deleteTargetId);
                this.showToast('Sohbet silindi', 'info');
            }
            this.el.deleteModal.classList.remove('active');
            this._deleteTargetId = null;
        });

        // View Switcher
        document.querySelectorAll('.view-btn').forEach(btn => {
            btn.addEventListener('click', () => this.setView(btn.dataset.view));
        });

        // Device Switcher
        document.querySelectorAll('.device-btn').forEach(btn => {
            btn.addEventListener('click', () => this.setDevice(btn.dataset.device));
        });

        // Quick Prompts
        this.el.quickPrompts.addEventListener('click', (e) => {
            const btn = e.target.closest('.quick-prompt-btn');
            if (btn && !this.isGenerating) {
                const prompt = btn.dataset.prompt;
                // Create new session for quick prompt
                if (!this.getActiveSession()) {
                    this.createSession();
                }
                this.el.promptInput.value = prompt;
                this.updateCharCount();
                this.generateWebsite(prompt);
                this.closeSidebar();
            }
        });

        // Enhance Buttons
        this.el.enhanceButtons.addEventListener('click', (e) => {
            const btn = e.target.closest('.enhance-btn');
            if (btn && !btn.disabled && !this.isGenerating) {
                this.enhanceWebsite(btn.dataset.type);
            }
        });

        // Send / Stop
        this.el.btnSend.addEventListener('click', () => this.handleSend());
        this.el.btnStop.addEventListener('click', () => this.stopGeneration());

        // Input
        this.el.promptInput.addEventListener('input', () => {
            this.updateCharCount();
            this.autoResize();
        });
        this.el.promptInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.handleSend();
            }
        });

        // Top bar buttons
        this.el.btnCopyCode.addEventListener('click', () => this.copyCode());
        this.el.btnDownload.addEventListener('click', () => this.downloadCode());
        this.el.btnWrapCode.addEventListener('click', () => this.toggleWordWrap());
        this.el.btnRefreshPreview.addEventListener('click', () => this.refreshPreview());
        this.el.btnOpenExternal.addEventListener('click', () => this.openExternal());

        // Code editor manual edits
        this.el.codeContent.addEventListener('input', () => {
            const code = this.el.codeContent.textContent;
            this.updateLineNumbers();
            // Save to session
            const session = this.getActiveSession();
            if (session) {
                session.code = code;
                this.saveState();
            }
        });
    }

    /* =====================
       Language & Settings
       ===================== */
    setLanguage(lang) {
        if (!['tr', 'en'].includes(lang)) return;
        this.state.language = lang;
        this.saveState();
        this.updateLangUI();
        this.showToast(lang === 'en' ? 'Language switched to English' : 'Dil Türkçe olarak güncellendi', 'info');
        setTimeout(() => location.reload(), 500);
    }

    updateLangUI() {
        if (!this.state.language) this.state.language = 'tr';
        if (this.el.langBtns) {
            this.el.langBtns.forEach(btn => {
                if (btn.dataset.lang === this.state.language) {
                    btn.classList.add('active');
                } else {
                    btn.classList.remove('active');
                }
            });
        }
    }

    /* =====================
       Ollama Models
       ===================== */
    async loadModels() {
        try {
            const response = await fetch('/api/models');
            const data = await response.json();
            
            if (data.models && data.models.length > 0) {
                this.el.modelSelect.innerHTML = '';
                data.models.forEach(model => {
                    const option = document.createElement('option');
                    option.value = model;
                    option.textContent = model;
                    this.el.modelSelect.appendChild(option);
                });
                
                // Get saved model or use first one
                const savedModel = localStorage.getItem('seeksite_model');
                if (savedModel && data.models.includes(savedModel)) {
                    this.el.modelSelect.value = savedModel;
                }
            } else if (data.error) {
                console.error('Ollama models error:', data.error);
                this.el.modelSelect.innerHTML = '<option value="">Ollama Hata</option>';
            }
        } catch (e) {
            console.error('Failed to load models:', e);
            this.el.modelSelect.innerHTML = '<option value="">Bağlantı Hatası</option>';
        }

        this.el.modelSelect.addEventListener('change', () => {
            localStorage.setItem('seeksite_model', this.el.modelSelect.value);
        });
    }


    /* =====================
       Chat History UI
       ===================== */
    renderChatHistory() {
        const list = this.el.chatHistoryList;
        list.innerHTML = '';

        if (this.state.sessions.length === 0) {
            list.innerHTML = '<div class="chat-history-empty"><i class="fas fa-comments"></i><span>Henuz sohbet yok</span></div>';
            return;
        }

        this.state.sessions.forEach(session => {
            const item = document.createElement('div');
            item.className = `chat-history-item ${session.id === this.state.activeSessionId ? 'active' : ''}`;
            item.innerHTML = `
                <div class="chat-item-content" data-id="${session.id}">
                    <i class="fas fa-globe"></i>
                    <span class="chat-item-title">${this.escapeHtml(session.title)}</span>
                </div>
                <button class="chat-item-delete" data-id="${session.id}" title="Sil">
                    <i class="fas fa-trash-alt"></i>
                </button>
            `;

            // Click to switch
            item.querySelector('.chat-item-content').addEventListener('click', () => {
                if (this.isGenerating) return;
                this.switchToSession(session.id);
            });

            // Click delete - show modal
            item.querySelector('.chat-item-delete').addEventListener('click', (e) => {
                e.stopPropagation();
                if (this.isGenerating) return;
                this._deleteTargetId = session.id;
                this.el.deleteModal.classList.add('active');
            });

            list.appendChild(item);
        });
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    /* =====================
       Sidebar
       ===================== */
    toggleSidebar() {
        this.el.sidebar.classList.toggle('open');
        document.getElementById('sidebarOverlay').classList.toggle('active');
    }

    closeSidebar() {
        this.el.sidebar.classList.remove('open');
        document.getElementById('sidebarOverlay').classList.remove('active');
    }

    /* =====================
       View Management
       ===================== */
    setView(view) {
        this.currentView = view;
        this.el.workspace.className = `workspace view-${view}`;
        document.querySelectorAll('.view-btn').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.view === view);
        });
        const session = this.getActiveSession();
        if ((view === 'preview' || view === 'split') && session && session.code) {
            setTimeout(() => this._doPreviewUpdate(session.code), 50);
        }
    }

    setDevice(device) {
        document.querySelectorAll('.device-btn').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.device === device);
        });
        this.el.previewContainer.className = `preview-container ${device === 'desktop' ? '' : device}`;
    }

    /* =====================
       Code Editor
       ===================== */
    updateLineNumbers() {
        const code = this.el.codeContent.textContent || '';
        const lineCount = code.split('\n').length;
        const numbers = [];
        for (let i = 1; i <= Math.max(lineCount, 1); i++) numbers.push(i);
        this.el.lineNumbers.textContent = numbers.join('\n');
    }

    toggleWordWrap() {
        this.wordWrap = !this.wordWrap;
        this.el.codeContent.classList.toggle('no-wrap', !this.wordWrap);
        this.showToast(this.wordWrap ? 'Word wrap ON' : 'Word wrap OFF', 'info');
    }

    /* =====================
       Preview (Blob URL)
       ===================== */
    updatePreview(immediate = false) {
        const session = this.getActiveSession();
        if (!session || !session.code) return;

        if (immediate) {
            this._doPreviewUpdate(session.code);
            return;
        }
        clearTimeout(this._previewTimer);
        this._previewTimer = setTimeout(() => {
            this._doPreviewUpdate(session.code);
        }, 250);
    }

    _doPreviewUpdate(code) {
        if (!code) return;
        try {
            if (this._lastBlobUrl) URL.revokeObjectURL(this._lastBlobUrl);
            
            // Inject dynamic DNA CSS if generated separately
            let finalCode = code;
            const session = this.getActiveSession();
            if (session && session.dnaCss && !finalCode.includes('/* ===== BASE DNA ===== */')) {
                if (finalCode.includes('</head>')) {
                    finalCode = finalCode.replace('</head>', `\n<style>\n${session.dnaCss}\n</style>\n</head>`);
                } else if (!finalCode.includes('<style')) {
                    finalCode = `\n<style>\n${session.dnaCss}\n</style>\n` + finalCode;
                }
            }

            const blob = new Blob([finalCode], { type: 'text/html;charset=utf-8' });
            this._lastBlobUrl = URL.createObjectURL(blob);
            this.el.previewFrame.src = this._lastBlobUrl;
        } catch (e) {
            try {
                const doc = this.el.previewFrame.contentDocument || this.el.previewFrame.contentWindow.document;
                doc.open(); doc.write(finalCode || code); doc.close();
            } catch (e2) { console.warn('Preview failed:', e2); }
        }
    }

    async preloadImages(code) {
        if (!code) return;
        return new Promise((resolve) => {
            const tempDiv = document.createElement('div');
            tempDiv.innerHTML = code;
            const images = tempDiv.querySelectorAll('img');
            
            if (images.length === 0) return resolve();
            
            let loadedCount = 0;
            // timeout safe release 
            const fallback = setTimeout(() => resolve(), 8000); 

            images.forEach(img => {
                const src = img.getAttribute('src');
                if (!src) {
                    loadedCount++;
                    if (loadedCount === images.length) { clearTimeout(fallback); resolve(); }
                    return;
                }
                const preloader = new Image();
                preloader.onload = preloader.onerror = () => {
                    loadedCount++;
                    if (loadedCount === images.length) { clearTimeout(fallback); resolve(); }
                };
                preloader.src = src;
            });
        });
    }

    refreshPreview() {
        const session = this.getActiveSession();
        if (session && session.code) {
            this._doPreviewUpdate(session.code);
            this.showToast('Onizleme yenilendi', 'info');
        }
    }

    openExternal() {
        const session = this.getActiveSession();
        if (!session || !session.code) return;
        const fullCode = this.getFullCode(session);
        const blob = new Blob([fullCode], { type: 'text/html' });
        window.open(URL.createObjectURL(blob), '_blank');
    }

    /* =====================
       Generation
       ===================== */
    async handleSend() {
        const prompt = this.el.promptInput.value.trim();
        if (!prompt || this.isGenerating) return;

        // Ensure we have a session
        let session = this.getActiveSession();
        if (!session) {
            session = this.createSession();
            this.renderChatHistory();
        }

        if (session.code) {
            this.generateWebsite(prompt, session.code);
        } else {
            this.generateWebsite(prompt);
        }
    }

    async generateWebsite(prompt, existingCode = null) {
        let session = this.getActiveSession();
        if (!session) {
            session = this.createSession();
        }

        this.setGenerating(true);
        this.el.welcomeScreen.classList.add('hidden');

        if (!existingCode) {
            session.code = '';
            this.el.codeContent.textContent = '';
            this.updateLineNumbers();
        }

        let accumulated = '';
        let lastPreviewUpdate = 0;
        let buffer = '';

        try {
            this.abortController = new AbortController();

            const response = await fetch('/api/generate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    prompt: prompt,
                    existing_code: existingCode,
                    history: session.history.length > 0 ? session.history : null,
                    model: this.el.modelSelect.value
                }),
                signal: this.abortController.signal
            });

            if (!response.ok) throw new Error(`HTTP ${response.status}`);

            const reader = response.body.getReader();
            const decoder = new TextDecoder();

            while (true) {
                const { done, value } = await reader.read();
                if (done) break;

                buffer += decoder.decode(value, { stream: true });
                const lines = buffer.split('\n');
                buffer = lines.pop() || '';

                for (const line of lines) {
                    if (!line.startsWith('data: ')) continue;
                    const data = line.slice(6).trim();
                    if (data === '[DONE]') break;

                    try {
                        const parsed = JSON.parse(data);
                        if (parsed.error) { this.showToast(`Hata: ${parsed.error}`, 'error'); continue; }
                        
                        if (parsed.dnaCss) {
                            session.dnaCss = parsed.dnaCss;
                            continue;
                        }
                        
                        // Backend sent a cleaned replacement (ads stripped)
                        if (parsed.replace) {
                            accumulated = parsed.replace;
                            const clean = this.cleanCode(accumulated);
                            session.code = clean;
                            this.el.codeContent.textContent = this.getFullCode(session);
                            this.updateLineNumbers();
                            continue;
                        }
                        
                        if (parsed.content) {
                            accumulated += parsed.content;
                            const clean = this.cleanCode(accumulated);
                            session.code = clean;
                            this.el.codeContent.textContent = this.getFullCode(session);
                            this.updateLineNumbers();
                            this.el.codeContainer.scrollTop = this.el.codeContainer.scrollHeight;
                            
                            // DELIBERATELY NO LIVE PREVIEW HERE.
                            // Live previewing resets <img> tags every second, cancelling Pollinations AI requests
                            // and causing images to be delayed, broken, or never load. 
                        }
                    } catch (e) {}
                }
            }

            // Final - Preparation
            session.code = this.cleanCode(accumulated);
            this.el.codeContent.textContent = this.getFullCode(session);
            this.updateLineNumbers();
            
            // Image Generation Wait Phase
            this.showToast('Gorseller hazirlaniyor, lutfen bekleyin...', 'info', 10000); // 10s toast
            await this.preloadImages(session.code);
            
            this.showToast('Gorseller hazir! Rendeleme tamamlandi.', 'success');
            this._doPreviewUpdate(session.code);  // INSTANT preview with loaded images
            this.enableActions();
            this.saveState();

            // Update history
            session.history.push({ role: 'user', content: prompt });
            session.history.push({ role: 'assistant', content: 'Website updated with your requests.' });
            if (session.history.length > 8) session.history = session.history.slice(-8);

            // Generate title via AI (background)
            this.generateTitle(prompt, session);

            this.showToast('Website olusturuldu!', 'success');
            this.el.promptInput.value = '';
            this.updateCharCount();

            // AUTO-FIX in background (after preview is already shown)
            this.autoFixCode(session).then(() => {
                this._doPreviewUpdate(session.code);
            });

        } catch (error) {
            if (error.name === 'AbortError') {
                this.showToast('Durduruldu', 'warning');
            } else {
                this.showToast(`Hata: ${error.message}`, 'error');
            }

            // Show whatever was generated so far
            const session = this.getActiveSession();
            if (session && accumulated) {
                session.code = this.cleanCode(accumulated);
                this.el.codeContent.textContent = this.getFullCode(session);
                this.updateLineNumbers();
                this._doPreviewUpdate(session.code);
                this.enableActions();
            }
            this.saveState();
        } finally {
            this.setGenerating(false);
            this.abortController = null;
        }
    }

    async enhanceWebsite(type) {
        const session = this.getActiveSession();
        if (!session || !session.code || this.isGenerating) return;

        this.setGenerating(true);
        let accumulated = '';
        let buffer = '';
        let lastPreviewUpdate = 0;

        try {
            this.abortController = new AbortController();

            const response = await fetch('/api/enhance', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    code: session.code, 
                    type, 
                    model: this.el.modelSelect.value 
                }),
                signal: this.abortController.signal
            });

            if (!response.ok) throw new Error(`HTTP ${response.status}`);

            const reader = response.body.getReader();
            const decoder = new TextDecoder();

            while (true) {
                const { done, value } = await reader.read();
                if (done) break;

                buffer += decoder.decode(value, { stream: true });
                const lines = buffer.split('\n');
                buffer = lines.pop() || '';

                for (const line of lines) {
                    if (!line.startsWith('data: ')) continue;
                    const data = line.slice(6).trim();
                    if (data === '[DONE]') break;
                    try {
                        const parsed = JSON.parse(data);
                        if (parsed.content) {
                            accumulated += parsed.content;
                            const clean = this.cleanCode(accumulated);
                            session.code = clean;
                            this.el.codeContent.textContent = this.getFullCode(session);
                            this.updateLineNumbers();
                            this.el.codeContainer.scrollTop = this.el.codeContainer.scrollHeight;
                            
                            // DELIBERATELY NO LIVE PREVIEW DURING STREAM.
                        }
                    } catch (e) {}
                }
            }

            session.code = this.cleanCode(accumulated);
            this.el.codeContent.textContent = this.getFullCode(session);
            this.updateLineNumbers();
            
            this.showToast('Gorseller iyilestiriliyor, lutfen bekleyin...', 'info', 10000);
            await this.preloadImages(session.code);
            
            this._doPreviewUpdate(session.code);
            this.saveState();
            this.showToast('Iyilestirme tamamlandi!', 'success');

            // Auto-fix in background
            this.autoFixCode(session).then(() => {
                this._doPreviewUpdate(session.code);
            });

        } catch (error) {
            if (error.name === 'AbortError') {
                this.showToast('Durduruldu', 'warning');
            } else {
                this.showToast(`Hata: ${error.message}`, 'error');
            }
            const session = this.getActiveSession();
            if (session && accumulated) {
                session.code = this.cleanCode(accumulated);
                this._doPreviewUpdate(session.code);
                this.enableActions();
            }
            this.saveState();
        } finally {
            this.setGenerating(false);
            this.abortController = null;
        }
    }

    async generateTitle(prompt, session) {
        if (session.title !== 'Yeni Sohbet') return;

        try {
            const response = await fetch('/api/generate_title', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    prompt,
                    model: this.el.modelSelect.value 
                })
            });
            const data = await response.json();
            if (data.title) {
                session.title = data.title;
                this.saveState();
                this.renderChatHistory();
            }
        } catch (e) {
            // Fallback: use first 30 chars of prompt
            session.title = prompt.substring(0, 30) + (prompt.length > 30 ? '...' : '');
            this.saveState();
            this.renderChatHistory();
        }
    }

    async autoFixCode(session) {
        if (!session || !session.code) return;
        try {
            const prompt = this.el.promptInput.value.trim() || (session.history.length > 0 ? session.history[0].content : "");
            const response = await fetch('/api/fix', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    code: session.code,
                    prompt: prompt,
                    model: this.el.modelSelect.value
                })
            });
            const data = await response.json();
            if (data.code && data.code !== session.code) {
                session.code = data.code;
                this.el.codeContent.textContent = data.code;
                this.updateLineNumbers();
                this.saveState();

                const issues = data.validation?.issues || [];
                if (issues.length > 0) {
                    console.log('Auto-fix remaining issues:', issues);
                } else {
                    this.showToast('Kod otomatik duzeltildi', 'info');
                }
            }
        } catch (e) {
            console.warn('Auto-fix failed:', e);
        }
    }

    cleanCode(code) {
        let c = code;
        c = c.replace(/^```(?:html?)?\s*\n?/i, '');
        c = c.replace(/\n?```\s*$/i, '');

        // Strip Pollinations AI ads
        c = c.replace(/-{2,}\s*\n?\s*\*{0,2}\s*Support Pollinations\.AI[\s\S]*?keep AI accessible for everyone\.?\s*/gi, '');
        c = c.replace(/🌸[\s\S]*?Ad[\s\S]*?🌸[^\n]*/g, '');
        c = c.replace(/Powered by Pollinations\.AI[\s\S]*?(?:accessible for everyone|pollinations\.ai\/redirect\/kofi\))\.?\s*/gi, '');
        c = c.replace(/\[Support our mission\]\(https?:\/\/pollinations\.ai[^\)]*\)[^\n]*/gi, '');
        c = c.replace(/\*{0,2}Support Pollinations\.AI:?\*{0,2}/gi, '');
        c = c.replace(/\n-{3,}\s*\n-{3,}\s*\n/g, '\n');

        const doctypeIdx = c.indexOf('<!DOCTYPE');
        const doctypeIdxLower = c.indexOf('<!doctype');
        const htmlIdx = c.indexOf('<html');
        const indices = [doctypeIdx, doctypeIdxLower, htmlIdx].filter(i => i !== -1);
        const startIdx = indices.length > 0 ? Math.min(...indices) : -1;

        if (startIdx > 0) c = c.substring(startIdx);
        
        return c.trimEnd();
    }

    stopGeneration() {
        if (this.abortController) {
            this.abortController.abort();
            this.abortController = null;
        }
    }

    /* =====================
       UI State
       ===================== */
    setGenerating(generating) {
        this.isGenerating = generating;
        this.el.btnSend.classList.toggle('hidden', generating);
        this.el.btnStop.classList.toggle('hidden', !generating);
        this.el.statusDot.className = `status-dot ${generating ? 'generating' : ''}`;
        this.el.statusText.textContent = generating ? 'Uretiliyor...' : 'Hazir';
        this.el.promptInput.disabled = generating;
        if (generating) {
            this.el.promptInput.placeholder = 'AI calisiyor...';
        } else {
            this.updatePlaceholder();
        }
    }

    updatePlaceholder() {
        const session = this.getActiveSession();
        this.el.promptInput.placeholder = session && session.code
            ? "Degisiklik isteyin... (orn: 'Renkleri degistir')"
            : "Web sitenizi tanimlayin...";
    }

    enableActions() {
        this.el.btnCopyCode.disabled = false;
        this.el.btnDownload.disabled = false;
        document.querySelectorAll('.enhance-btn').forEach(btn => btn.disabled = false);
    }

    disableActions() {
        this.el.btnCopyCode.disabled = true;
        this.el.btnDownload.disabled = true;
        document.querySelectorAll('.enhance-btn').forEach(btn => btn.disabled = true);
    }

    getFullCode(session) {
        if (!session || !session.code) return '';
        let code = session.code;
        const missingHead = !code.toLowerCase().includes('</head>');

        if (session.dnaCss && !code.includes('/* ===== BASE DNA ===== */')) {
            if (!missingHead) {
                // If it has a head, just inject it there
                code = code.replace(/<\/head>/i, `\n<style>\n${session.dnaCss}\n</style>\n</head>`);
            } else {
                // Completely missing head (only body content), create a full skeleton
                code = `<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>${session.title || 'SeekSite Project'}</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
<style>\n${session.dnaCss}\n</style>
</head>
<body>\n${code}\n</body>\n</html>`;
            }
        } else if (missingHead) {
             // Even if no css to inject, we must ensure charset exists for Blob URLs
             code = `<meta charset="UTF-8">\n` + code;
        }
        
        return code;
    }

    async copyCode() {
        const session = this.getActiveSession();
        if (!session || !session.code) return;
        const fullCode = this.getFullCode(session);
        try {
            await navigator.clipboard.writeText(fullCode);
            this.showToast('Kod kopyalandi!', 'success');
        } catch (e) {
            const ta = document.createElement('textarea');
            ta.value = fullCode;
            document.body.appendChild(ta);
            ta.select();
            document.execCommand('copy');
            document.body.removeChild(ta);
            this.showToast('Kod kopyalandi!', 'success');
        }
    }

    downloadCode() {
        const session = this.getActiveSession();
        if (!session || !session.code) return;
        const fullCode = this.getFullCode(session);
        const blob = new Blob([fullCode], { type: 'text/html' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${session.title.replace(/[^a-zA-Z0-9]/g, '_')}.html`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        this.showToast('HTML indirildi!', 'success');
    }

    /* =====================
       Input Helpers
       ===================== */
    updateCharCount() {
        this.el.charCount.textContent = `${this.el.promptInput.value.length}/2000`;
    }

    autoResize() {
        const ta = this.el.promptInput;
        ta.style.height = 'auto';
        ta.style.height = Math.min(ta.scrollHeight, 100) + 'px';
    }

    /* =====================
       Resize Handle
       ===================== */
    setupResizeHandle() {
        const handle = this.el.resizeHandle;
        let isDragging = false, startX = 0, startWidth = 0;

        handle.addEventListener('mousedown', (e) => {
            isDragging = true;
            startX = e.clientX;
            startWidth = this.el.codePanel.getBoundingClientRect().width;
            handle.classList.add('dragging');
            document.body.style.cursor = 'col-resize';
            document.body.style.userSelect = 'none';
            e.preventDefault();
        });

        document.addEventListener('mousemove', (e) => {
            if (!isDragging) return;
            const ww = this.el.workspace.getBoundingClientRect().width;
            const newWidth = Math.max(200, Math.min(ww - 200, startWidth + (e.clientX - startX)));
            this.el.codePanel.style.flex = `0 0 ${(newWidth / ww) * 100}%`;
            this.el.previewPanel.style.flex = '1';
        });

        document.addEventListener('mouseup', () => {
            if (isDragging) {
                isDragging = false;
                handle.classList.remove('dragging');
                document.body.style.cursor = '';
                document.body.style.userSelect = '';
            }
        });
    }

    /* =====================
       Toast
       ===================== */
    showToast(message, type = 'info', duration = 3000) {
        const icons = { success: 'fa-check-circle', error: 'fa-exclamation-circle', warning: 'fa-exclamation-triangle', info: 'fa-info-circle' };
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.innerHTML = `<i class="fas ${icons[type] || icons.info}"></i><span>${message}</span>`;
        this.el.toastContainer.appendChild(toast);
        setTimeout(() => {
            toast.classList.add('toast-out');
            setTimeout(() => toast.remove(), 300);
        }, duration);
    }
}

// Init
document.addEventListener('DOMContentLoaded', () => {
    window.app = new SeekSiteApp();
});
