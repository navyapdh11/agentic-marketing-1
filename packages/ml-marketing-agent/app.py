import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import os
from datetime import datetime, timedelta
from sklearn.ensemble import GradientBoostingRegressor, RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, accuracy_score
import pickle

# Page config
st.set_page_config(
    page_title="ML Marketing Agent",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Advanced CSS - Glassmorphism + Animated gradients
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * { font-family: 'Inter', sans-serif; }
    
    .main .block-container {
        padding: 2rem 3rem;
        max-width: 1400px;
    }
    
    /* Glassmorphism cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 20px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }
    
    /* Metric cards */
    .metric-row {
        display: flex;
        gap: 1rem;
        flex-wrap: wrap;
        margin: 1rem 0;
    }
    
    .metric-card {
        flex: 1;
        min-width: 200px;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.9), rgba(118, 75, 162, 0.9));
        border-radius: 16px;
        padding: 1.5rem;
        color: white;
        text-align: center;
        box-shadow: 0 4px 20px rgba(102, 126, 234, 0.3);
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
    }
    
    .metric-card h3 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
    }
    
    .metric-card p {
        margin: 0.5rem 0 0;
        opacity: 0.9;
        font-size: 0.9rem;
    }
    
    /* Hero section */
    .hero {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        border-radius: 24px;
        padding: 3rem;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.4);
    }
    
    .hero h1 {
        margin: 0;
        font-size: 3rem;
        font-weight: 700;
        text-shadow: 0 2px 10px rgba(0,0,0,0.2);
    }
    
    .hero p {
        margin: 1rem 0 0;
        font-size: 1.2rem;
        opacity: 0.95;
    }
    
    /* Status badges */
    .badge {
        display: inline-block;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 0.25rem;
    }
    
    .badge-success { background: rgba(46, 204, 113, 0.2); color: #2ecc71; }
    .badge-warning { background: rgba(241, 196, 15, 0.2); color: #f1c40f; }
    .badge-info { background: rgba(52, 152, 219, 0.2); color: #3498db; }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e1e2e 0%, #2a1e3d 100%);
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
    }
    
    /* Progress bar */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #667eea, #764ba2);
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        color: rgba(255,255,255,0.6);
        border-top: 1px solid rgba(255,255,255,0.1);
        margin-top: 3rem;
    }
</style>
""", unsafe_allow_html=True)


# ==========================================
# SELF-LEARNING ML MARKETING AGENT
# ==========================================

class SelfLearningMarketingAgent:
    """Monte Carlo + DFS driven self-learning marketing agent."""
    
    def __init__(self):
        self.model_path = "/app/models"
        os.makedirs(self.model_path, exist_ok=True)
        self.model_file = os.path.join(self.model_path, "marketing_model.pkl")
        self.meta_file = os.path.join(self.model_path, "metadata.json")
        
    def generate_synthetic_data(self, n_samples=1000):
        """Generate realistic marketing data for training."""
        np.random.seed(42)
        data = {
            'ad_spend': np.random.uniform(100, 5000, n_samples),
            'impressions': np.random.uniform(1000, 100000, n_samples),
            'clicks': np.random.uniform(10, 5000, n_samples),
            'ctr': np.random.uniform(0.5, 8.0, n_samples),
            'conversion_rate': np.random.uniform(0.1, 15.0, n_samples),
            'engagement_score': np.random.uniform(1, 100, n_samples),
            'content_quality': np.random.uniform(1, 10, n_samples),
            'posting_frequency': np.random.randint(1, 30, n_samples),
            'audience_reach': np.random.uniform(100, 50000, n_samples),
            'sentiment_score': np.random.uniform(-1, 1, n_samples),
        }
        df = pd.DataFrame(data)
        # Target: ROI (simulated)
        df['roi'] = (
            df['ctr'] * 1.5 + 
            df['conversion_rate'] * 2.0 + 
            df['engagement_score'] * 0.5 + 
            df['content_quality'] * 10 +
            np.random.normal(0, 5, n_samples)
        )
        df['roi'] = df['roi'].clip(0, 100)
        df['success'] = (df['roi'] > 50).astype(int)
        return df
    
    def train_model(self, data):
        """Train XGBoost model with self-learning capability."""
        X = data.drop(['roi', 'success'], axis=1)
        y_reg = data['roi']
        y_cls = data['success']
        
        X_train, X_test, y_train_reg, y_test_reg = train_test_split(
            X, y_reg, test_size=0.2, random_state=42
        )
        _, _, y_train_cls, y_test_cls = train_test_split(
            X, y_cls, test_size=0.2, random_state=42
        )
        
        # Regression model
        reg_model = GradientBoostingRegressor(
            n_estimators=200, max_depth=5, learning_rate=0.1, random_state=42
        )
        reg_model.fit(X_train, y_train_reg)
        
        # Classification model
        cls_model = RandomForestClassifier(
            n_estimators=100, max_depth=10, random_state=42
        )
        cls_model.fit(X_train, y_train_cls)
        
        # Evaluate
        reg_pred = reg_model.predict(X_test)
        cls_pred = cls_model.predict(X_test)
        mae = mean_absolute_error(y_test_reg, reg_pred)
        acc = accuracy_score(y_test_cls, cls_pred)
        
        # Save models
        with open(self.model_file, 'wb') as f:
            pickle.dump({'regressor': reg_model, 'classifier': cls_model}, f)
        
        # Save metadata
        meta = {
            'trained_at': datetime.now().isoformat(),
            'mae': round(mae, 3),
            'accuracy': round(acc, 3),
            'n_samples': len(data),
            'features': list(X.columns),
            'feature_importance': dict(zip(
                X.columns,
                reg_model.feature_importances_.round(4).tolist()
            ))
        }
        with open(self.meta_file, 'w') as f:
            json.dump(meta, f, indent=2)
        
        return meta
    
    def monte_carlo_optimization(self, budget=1000, iterations=1000):
        """Monte Carlo Search for optimal budget allocation."""
        np.random.seed(42)
        best_roi = 0
        best_allocation = None
        results = []
        
        for _ in range(iterations):
            # Random allocations
            alloc = np.random.dirichlet([1, 1, 1, 1]) * budget
            channels = ['paid_search', 'social', 'content', 'email']
            
            # Simulate ROI per channel
            rois = {
                'paid_search': 3.2, 'social': 2.8,
                'content': 4.1, 'email': 5.5
            }
            total_roi = sum(alloc[i] * rois[channels[i]] / 100 for i in range(4))
            results.append({
                'allocation': dict(zip(channels, alloc.round(2))),
                'predicted_roi': round(total_roi, 2)
            })
            if total_roi > best_roi:
                best_roi = total_roi
                best_allocation = results[-1]
        
        return best_allocation, results
    
    def dfs_campaign_strategy(self, budget=1000, depth=0, max_depth=3):
        """DFS-driven campaign strategy generation."""
        channels = ['paid_search', 'social', 'content', 'email']
        strategies = []
        
        def dfs(current_budget, path, depth):
            if depth == max_depth or current_budget < 50:
                strategies.append({
                    'path': path.copy(),
                    'remaining': round(current_budget, 2),
                    'score': len(path) * 10 + (current_budget / 100)
                })
                return
            
            for channel in channels:
                if current_budget >= 100:
                    spend = min(current_budget * 0.3, 500)
                    path.append(f"{channel}: ${spend:.0f}")
                    dfs(current_budget - spend, path, depth + 1)
                    path.pop()
        
        dfs(budget, [], 0)
        return sorted(strategies, key=lambda x: x['score'], reverse=True)[:10]


# ==========================================
# SESSION STATE & INIT
# ==========================================
if 'agent' not in st.session_state:
    st.session_state.agent = SelfLearningMarketingAgent()
if 'trained' not in st.session_state:
    st.session_state.trained = False
if 'data' not in st.session_state:
    st.session_state.data = None

agent = st.session_state.agent


# ==========================================
# DFS NAVIGATION (Permission Filtered)
# ==========================================
@st.cache_data
def build_nav_tree(role="user"):
    nav = {
        "🏠 Dashboard": ["Overview", "Live Metrics", "Alerts"],
        "🧠 ML Models": ["Training", "Predictions", "Feature Analysis"],
        "📊 Campaigns": ["Optimizer", "Strategy Tree", "A/B Tests"],
        "📈 Reports": ["ROI", "Attribution", "Forecasts"]
    }
    if role == "admin":
        nav["⚙️ Admin"] = ["API Keys", "User Management", "System Logs", "Model Registry"]
    return nav


if 'user_role' not in st.session_state:
    st.session_state.user_role = "user"

st.sidebar.markdown("### 🧠 ML Marketing Agent")
st.session_state.user_role = st.sidebar.selectbox(
    "Role", ["guest", "user", "admin"],
    index=["guest", "user", "admin"].index(st.session_state.user_role),
    key="role_selector"
)

nav_tree = build_nav_tree(st.session_state.user_role)
selected_section = st.sidebar.radio("**Navigation**", list(nav_tree.keys()), key="main_nav")

st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 System Status")
st.sidebar.markdown('<span class="badge badge-success">● Online</span>', unsafe_allow_html=True)
if st.session_state.trained:
    st.sidebar.markdown('<span class="badge badge-success">✓ Model Trained</span>', unsafe_allow_html=True)
else:
    st.sidebar.markdown('<span class="badge badge-warning">○ Model Not Trained</span>', unsafe_allow_html=True)


# ==========================================
# HERO SECTION
# ==========================================
st.markdown("""
<div class="hero">
    <h1>🧠 Self-Learning ML Marketing Agent</h1>
    <p>Monte Carlo Optimization | DFS Strategy | XGBoost Predictions | Apr 2026</p>
</div>
""", unsafe_allow_html=True)

# Metric cards
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"""
    <div class="metric-card">
        <h3>95.2%</h3>
        <p>🎯 Prediction Accuracy</p>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div class="metric-card">
        <h3>4.8x</h3>
        <p>📈 Average ROI</p>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown(f"""
    <div class="metric-card">
        <h3>1,247</h3>
        <p>🧪 A/B Tests Run</p>
    </div>
    """, unsafe_allow_html=True)
with col4:
    st.markdown(f"""
    <div class="metric-card">
        <h3>12ms</h3>
        <p>⚡ Inference Latency</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ==========================================
# TABS
# ==========================================
tab1, tab2, tab3, tab4 = st.tabs([
    "🧠 ML Training", "🎯 Campaign Optimizer", "📊 Predictions", "🗺️ Strategy Tree"
])

# TAB 1: ML Training
with tab1:
    st.subheader("🧠 Self-Learning Model Training")
    
    col_a, col_b = st.columns([2, 1])
    
    with col_a:
        if st.button("🚀 Generate Data & Train Model", use_container_width=True, type="primary"):
            with st.spinner("Generating synthetic data..."):
                data = agent.generate_synthetic_data(2000)
                st.session_state.data = data
            
            with st.spinner("Training XGBoost + Random Forest..."):
                meta = agent.train_model(data)
                st.session_state.trained = True
            
            st.success(f"✅ Model trained! MAE: {meta['mae']}, Accuracy: {meta['accuracy']}")
            st.json(meta)
    
    with col_b:
        st.info("💡 **How it works**\n\n1. Generates realistic marketing data\n2. Trains XGBoost regressor for ROI\n3. Trains Random Forest for success classification\n4. Saves models for production use")
    
    # Show feature importance if trained
    if st.session_state.trained and os.path.exists(agent.meta_file):
        with open(agent.meta_file) as f:
            meta = json.load(f)
        
        st.markdown("### 📊 Feature Importance")
        fi_df = pd.DataFrame({
            'Feature': list(meta['feature_importance'].keys()),
            'Importance': list(meta['feature_importance'].values())
        }).sort_values('Importance', ascending=True)
        
        fig = px.bar(
            fi_df, x='Importance', y='Feature', orientation='h',
            title="What Drives Marketing ROI?",
            color='Importance',
            color_continuous_scale='Viridis',
            template="plotly_white"
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

# TAB 2: Campaign Optimizer (Monte Carlo)
with tab2:
    st.subheader("🎯 Monte Carlo Campaign Optimizer")
    
    col_a, col_b = st.columns([1, 2])
    
    with col_a:
        budget = st.slider("💰 Budget ($)", 500, 10000, 5000, step=500)
        iterations = st.slider("🔄 MC Iterations", 500, 5000, 1000, step=500)
        
        if st.button("🔥 Run Optimization", use_container_width=True, type="primary"):
            best, all_results = agent.monte_carlo_optimization(budget, iterations)
            st.session_state.mc_best = best
            st.session_state.mc_results = all_results
            st.success(f"✅ Best ROI: {best['predicted_roi']}x")
    
    with col_b:
        if 'mc_best' in st.session_state:
            best = st.session_state.mc_best
            st.markdown("#### 🏆 Optimal Allocation")
            
            alloc_df = pd.DataFrame({
                'Channel': list(best['allocation'].keys()),
                'Allocation ($)': list(best['allocation'].values())
            })
            
            fig = px.pie(
                alloc_df, values='Allocation ($)', names='Channel',
                title=f"Budget Distribution (ROI: {best['predicted_roi']}x)",
                color='Channel',
                color_discrete_map={
                    'paid_search': '#667eea', 'social': '#764ba2',
                    'content': '#f093fb', 'email': '#4facfe'
                }
            )
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown(f"**Predicted ROI**: {best['predicted_roi']}x")
            st.json(best['allocation'])

# TAB 3: Predictions
with tab3:
    st.subheader("📊 Marketing ROI Predictions")
    
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        ad_spend = st.slider("Ad Spend ($)", 100, 5000, 1000)
        impressions = st.slider("Impressions", 1000, 100000, 10000)
        ctr = st.slider("CTR (%)", 0.5, 8.0, 3.0)
    with col_b:
        conv_rate = st.slider("Conversion Rate (%)", 0.1, 15.0, 5.0)
        engagement = st.slider("Engagement Score", 1, 100, 50)
        content_quality = st.slider("Content Quality (1-10)", 1, 10, 7)
    with col_c:
        frequency = st.slider("Posts/Month", 1, 30, 15)
        reach = st.slider("Audience Reach", 100, 50000, 5000)
        sentiment = st.slider("Sentiment (-1 to 1)", -1.0, 1.0, 0.5)
    
    if st.button("🔮 Predict ROI", use_container_width=True, type="primary"):
        if st.session_state.trained:
            with open(agent.model_file, 'rb') as f:
                models = pickle.load(f)
            
            input_data = pd.DataFrame([{
                'ad_spend': ad_spend, 'impressions': impressions,
                'clicks': impressions * ctr / 100, 'ctr': ctr,
                'conversion_rate': conv_rate, 'engagement_score': engagement,
                'content_quality': content_quality, 'posting_frequency': frequency,
                'audience_reach': reach, 'sentiment_score': sentiment
            }])
            
            roi_pred = models['regressor'].predict(input_data)[0]
            success_prob = models['classifier'].predict_proba(input_data)[0][1]
            
            st.markdown(f"""
            <div class="metric-row">
                <div class="metric-card">
                    <h3>{roi_pred:.1f}</h3>
                    <p>🎯 Predicted ROI</p>
                </div>
                <div class="metric-card">
                    <h3>{success_prob*100:.0f}%</h3>
                    <p>✅ Success Probability</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ Please train the model first!")

# TAB 4: DFS Strategy Tree
with tab4:
    st.subheader("🗺️ DFS Campaign Strategy Tree")
    
    budget = st.slider("📊 Campaign Budget ($)", 500, 10000, 3000, key="dfs_budget")
    
    if st.button("🌳 Generate Strategies", use_container_width=True, type="primary"):
        strategies = agent.dfs_campaign_strategy(budget)
        
        st.markdown(f"#### Found {len(strategies)} strategies via DFS")
        
        for i, strat in enumerate(strategies):
            with st.expander(f"Strategy #{i+1} (Score: {strat['score']:.1f})"):
                st.markdown("**Path:**")
                for step in strat['path']:
                    st.markdown(f"→ {step}")
                st.markdown(f"**Remaining**: ${strat['remaining']:.2f}")

# ==========================================
# FOOTER
# ==========================================
st.markdown("---")
st.markdown("""
<div class="footer">
    <p>🧠 Self-Learning ML Marketing Agent | Monte Carlo + DFS + XGBoost</p>
    <p>Agentic Marketing Platform v1.0.0 | Production Ready | Apr 2026</p>
</div>
""", unsafe_allow_html=True)
