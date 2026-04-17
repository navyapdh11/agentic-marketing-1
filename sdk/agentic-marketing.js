/**
 * Agentic Marketing Platform - JavaScript SDK v5.0.0
 * 
 * Usage:
 * <script src="https://cdn.jsdelivr.net/gh/navyapdh11/agentic-marketing-1/sdk/agentic-marketing.js"></script>
 * <script>
 *   const am = new AgenticMarketing('amk-demo-key-001');
 *   const result = await am.humanize('Your AI-generated text here');
 * </script>
 */
class AgenticMarketing {
    constructor(apiKey, baseUrl = 'https://agentic-marketing-umber.vercel.app') {
        this.apiKey = apiKey;
        this.baseUrl = baseUrl.replace(/\/$/, '');
        this.headers = {
            'Authorization': `Bearer ${apiKey}`,
            'Content-Type': 'application/json',
            'X-Client-Version': '5.0.0'
        };
    }

    async _request(method, path, body = null) {
        const opts = { method, headers: this.headers };
        if (body) opts.body = JSON.stringify(body);
        const resp = await fetch(`${this.baseUrl}${path}`, opts);
        if (!resp.ok) throw new Error(`API Error: ${resp.status} ${resp.statusText}`);
        return resp.json();
    }

    // ===== SEO =====
    async seoAudit(domain) {
        return this._request('GET', `/api/seo/audit?domain=${encodeURIComponent(domain)}`);
    }

    async generateSchema(pageType = 'Article') {
        return this._request('GET', `/api/seo/schema?page_type=${pageType}`);
    }

    async rankPrediction(keyword) {
        return this._request('GET', `/api/seo/rank-prediction?keyword=${encodeURIComponent(keyword)}`);
    }

    // ===== Content Humanization =====
    async humanize(text, aggressiveness = 0.7) {
        return this._request('POST', '/api/content/humanize', { text, aggressiveness });
    }

    async analyzeContent(text) {
        return this._request('POST', '/api/content/analyze', { text });
    }

    // ===== ML Marketing =====
    async optimize(budget = 10000, channels = ['email', 'social', 'seo', 'ads']) {
        return this._request('POST', '/api/ml/optimize', { budget, channels, action_type: 'optimize' });
    }

    async predictOutcomes(budget = 5000) {
        return this._request('POST', `/api/ml/predict?budget=${budget}`);
    }

    async getChannelPerformance() {
        return this._request('GET', '/api/ml/channels');
    }

    // ===== Auth =====
    async getToken() {
        return this._request('POST', '/api/auth/token');
    }

    // ===== Health =====
    async health() {
        return this._request('GET', '/api/health');
    }
}

// Auto-init if loaded via script tag
if (typeof window !== 'undefined') {
    window.AgenticMarketing = AgenticMarketing;
    console.log('🚀 Agentic Marketing SDK v5.0.0 loaded');
}

if (typeof module !== 'undefined') {
    module.exports = AgenticMarketing;
}
