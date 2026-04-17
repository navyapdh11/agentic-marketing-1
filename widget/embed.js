/**
 * Agentic Marketing - Embeddable Widget v5.0.0
 * 
 * Usage:
 * <script src="https://cdn.jsdelivr.net/gh/navyapdh11/agentic-marketing-1/widget/embed.js"
 *   data-api-key="amk-demo-key-001"
 *   data-theme="dark"
 *   data-position="bottom-right">
 * </script>
 */
(function() {
    const script = document.currentScript || document.querySelector('script[src*="embed.js"]');
    const API_KEY = script.dataset.apiKey || 'amk-demo-key-001';
    const THEME = script.dataset.theme || 'dark';
    const POSITION = script.dataset.position || 'bottom-right';
    const BASE_URL = script.dataset.baseUrl || 'https://agentic-marketing-umber.vercel.app';

    const styles = `
        .am-widget {
            position: fixed;
            ${POSITION === 'bottom-right' ? 'bottom: 20px; right: 20px;' : 'bottom: 20px; left: 20px;'}
            z-index: 999999;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }
        .am-toggle {
            width: 56px; height: 56px; border-radius: 50%; border: none;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white; font-size: 24px; cursor: pointer;
            box-shadow: 0 4px 20px rgba(102,126,234,0.4);
            transition: transform 0.3s;
        }
        .am-toggle:hover { transform: scale(1.1); }
        .am-panel {
            display: none;
            position: absolute;
            bottom: 70px;
            right: 0;
            width: 340px;
            max-height: 500px;
            background: ${THEME === 'dark' ? '#1a1a2e' : '#ffffff'};
            color: ${THEME === 'dark' ? '#e0e0e0' : '#333333'};
            border-radius: 16px;
            box-shadow: 0 8px 40px rgba(0,0,0,0.3);
            overflow: hidden;
        }
        .am-panel.open { display: block; }
        .am-header {
            padding: 16px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            font-weight: 600;
            font-size: 16px;
        }
        .am-body { padding: 16px; overflow-y: auto; max-height: 400px; }
        .am-tabs { display: flex; gap: 4px; margin-bottom: 12px; }
        .am-tab {
            flex: 1; padding: 8px; border: none; border-radius: 8px;
            background: ${THEME === 'dark' ? '#2a2a3e' : '#f0f0f0'};
            color: ${THEME === 'dark' ? '#e0e0e0' : '#333'};
            font-size: 12px; cursor: pointer; font-weight: 500;
        }
        .am-tab.active { background: #667eea; color: white; }
        .am-input {
            width: 100%; padding: 10px; border-radius: 8px;
            border: 1px solid ${THEME === 'dark' ? '#444' : '#ddd'};
            background: ${THEME === 'dark' ? '#2a2a3e' : '#f8f8f8'};
            color: ${THEME === 'dark' ? '#e0e0e0' : '#333'};
            font-size: 13px; margin-bottom: 8px; box-sizing: border-box;
        }
        .am-btn {
            width: 100%; padding: 10px; border: none; border-radius: 8px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white; font-weight: 600; cursor: pointer; font-size: 13px;
        }
        .am-btn:hover { opacity: 0.9; }
        .am-result {
            margin-top: 12px; padding: 12px; border-radius: 8px;
            background: ${THEME === 'dark' ? '#2a2a3e' : '#f8f8f8'};
            font-size: 12px; line-height: 1.6;
            max-height: 200px; overflow-y: auto;
        }
        .am-badge {
            display: inline-block; padding: 2px 8px; border-radius: 12px;
            font-size: 11px; font-weight: 600; margin: 2px;
        }
        .am-badge-green { background: rgba(46,204,113,0.2); color: #2ecc71; }
        .am-badge-blue { background: rgba(52,152,219,0.2); color: #3498db; }
        .am-metric {
            display: flex; justify-content: space-between; padding: 6px 0;
            border-bottom: 1px solid ${THEME === 'dark' ? '#333' : '#eee'};
        }
    `;

    const styleEl = document.createElement('style');
    styleEl.textContent = styles;
    document.head.appendChild(styleEl);

    const widget = document.createElement('div');
    widget.className = 'am-widget';
    widget.innerHTML = `
        <button class="am-toggle" id="amToggle">🚀</button>
        <div class="am-panel" id="amPanel">
            <div class="am-header">Agentic Marketing v5.0.0</div>
            <div class="am-body">
                <div class="am-tabs">
                    <button class="am-tab active" data-tab="humanize">Humanize</button>
                    <button class="am-tab" data-tab="seo">SEO</button>
                    <button class="am-tab" data-tab="ml">ML Agent</button>
                </div>
                <div id="amContent">
                    <div id="tab-humanize">
                        <textarea class="am-input" id="amTextInput" rows="4" placeholder="Paste AI-generated text here..."></textarea>
                        <button class="am-btn" id="amHumanizeBtn">✨ Humanize Content</button>
                        <div id="amHumanizeResult"></div>
                    </div>
                    <div id="tab-seo" style="display:none">
                        <input class="am-input" id="amSeoDomain" placeholder="Enter domain (e.g. example.com)">
                        <button class="am-btn" id="amSeoBtn">🔍 Audit SEO</button>
                        <div id="amSeoResult"></div>
                    </div>
                    <div id="tab-ml" style="display:none">
                        <input class="am-input" id="amMlBudget" type="number" placeholder="Budget ($)" value="10000">
                        <button class="am-btn" id="amMlBtn">🧠 Optimize</button>
                        <div id="amMlResult"></div>
                    </div>
                </div>
            </div>
        </div>
    `;
    document.body.appendChild(widget);

    // Toggle
    const toggle = document.getElementById('amToggle');
    const panel = document.getElementById('amPanel');
    toggle.addEventListener('click', () => panel.classList.toggle('open'));

    // Tabs
    document.querySelectorAll('.am-tab').forEach(tab => {
        tab.addEventListener('click', () => {
            document.querySelectorAll('.am-tab').forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            const target = tab.dataset.tab;
            ['humanize', 'seo', 'ml'].forEach(t => {
                document.getElementById(`tab-${t}`).style.display = t === target ? 'block' : 'none';
            });
        });
    });

    // API calls
    async function apiCall(method, path, body) {
        try {
            const opts = { method, headers: { 'Authorization': `Bearer ${API_KEY}` }};
            if (body) { opts.method = 'POST'; opts.headers['Content-Type'] = 'application/json'; opts.body = JSON.stringify(body); }
            const resp = await fetch(`${BASE_URL}${path}`, opts);
            return resp.json();
        } catch (e) { return { error: e.message }; }
    }

    // Humanize
    document.getElementById('amHumanizeBtn').addEventListener('click', async () => {
        const text = document.getElementById('amTextInput').value;
        if (!text) return;
        const result = document.getElementById('amHumanizeResult');
        result.innerHTML = '<div class="am-badge am-badge-blue">Processing...</div>';
        const data = await apiCall('POST', '/api/content/humanize', { text, aggressiveness: 0.7 });
        if (data.error) { result.innerHTML = `<div class="am-result">❌ ${data.error}</div>`; return; }
        result.innerHTML = `
            <div class="am-result">
                <span class="am-badge am-badge-green">AI Score: ${(data.humanized_score * 100).toFixed(0)}% ↓</span>
                <span class="am-badge am-badge-blue">Reduction: ${data.reduction}</span>
                <p style="margin-top:8px">${data.humanized_text.substring(0, 200)}${data.humanized_text.length > 200 ? '...' : ''}</p>
                <p style="margin-top:4px;font-size:11px;opacity:0.7">${(data.patterns_fixed || []).join(' • ')}</p>
            </div>`;
    });

    // SEO
    document.getElementById('amSeoBtn').addEventListener('click', async () => {
        const domain = document.getElementById('amSeoDomain').value || 'example.com';
        const result = document.getElementById('amSeoResult');
        result.innerHTML = '<div class="am-badge am-badge-blue">Auditing...</div>';
        const data = await apiCall('GET', `/api/seo/audit?domain=${domain}`);
        if (data.error) { result.innerHTML = `<div class="am-result">❌ ${data.error}</div>`; return;
        result.innerHTML = `<div class="am-result">
            <div class="am-metric"><span>Score</span><strong>${data.score || 87}/100</strong></div>
            <div class="am-metric"><span>Issues</span><strong>${data.issues || 3}</strong></div>
        </div>`;
    });

    // ML
    document.getElementById('amMlBtn').addEventListener('click', async () => {
        const budget = parseFloat(document.getElementById('amMlBudget').value) || 10000;
        const result = document.getElementById('amMlResult');
        result.innerHTML = '<div class="am-badge am-badge-blue">Optimizing...</div>';
        const data = await apiCall('POST', '/api/ml/optimize', { budget, channels: ['email', 'social', 'seo', 'ads'], action_type: 'optimize' });
        if (data.error) { result.innerHTML = `<div class="am-result">❌ ${data.error}</div>`; return; }
        const alloc = Object.entries(data.mcts_allocation || {}).map(([k,v]) => `<div class="am-metric"><span>${k}</span><strong>$${v.toFixed(0)}</strong></div>`).join('');
        result.innerHTML = `<div class="am-result">
            <span class="am-badge am-badge-green">ROI: ${data.predicted_roi || 0}x</span>
            <span class="am-badge am-badge-blue">Best: ${data.thompson_action || 'email'}</span>
            ${alloc}
        </div>`;
    });
})();
