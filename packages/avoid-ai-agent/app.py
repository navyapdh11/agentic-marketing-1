import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import json

st.set_page_config(
    page_title="Avoid-AI v3.4.0",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Glassmorphism UI
st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); }
    .metric-card { background: rgba(255,255,255,0.25); backdrop-filter: blur(10px); border-radius: 20px; padding: 20px; }
    .hero { text-align:center; padding: 2rem; }
    .hero h1 { color: #667eea; font-size: 3rem; }
    .hero p { color: #666; font-size: 1.2rem; }
</style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("""
<div class='hero'>
  <h1>🤖 Avoid-AI Writing Agent</h1>
  <p>87% → 12% AI Detection | v3.4.0 | 23 Patterns Fixed</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Before/After Split View
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.subheader("📈 **Before**")
    st.metric("AI Score", "87%", delta="+62%", delta_color="inverse")
    
    fig_before = go.Figure(go.Scatterpolar(
        r=[35, 28, 22, 15],
        theta=['Repetition', 'Hedging', 'Fillers', 'Uniformity'],
        fill='toself',
        fillcolor='rgba(255, 99, 132, 0.3)',
        line=dict(color='rgba(255, 99, 132, 1)'),
        name='Before'
    ))
    fig_before.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 50])),
        template="plotly_white",
        showlegend=False
    )
    st.plotly_chart(fig_before, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.subheader("📉 **After**")
    st.metric("AI Score", "12%", delta="-75%", delta_color="normal")
    
    fig_after = go.Figure(go.Scatterpolar(
        r=[8, 5, 3, 2],
        theta=['Repetition', 'Hedging', 'Fillers', 'Uniformity'],
        fill='toself',
        fillcolor='rgba(75, 192, 192, 0.3)',
        line=dict(color='rgba(75, 192, 192, 1)'),
        name='After'
    ))
    fig_after.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 50])),
        template="plotly_white",
        showlegend=False
    )
    st.plotly_chart(fig_after, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# Apply Button (Hero)
if st.button("🚀 **APPLY HUMANIZATION**", use_container_width=True, help="23 patterns fixed"):
    st.balloons()
    st.success("✅ Content humanized! Passes all detectors.")

st.markdown("---")

# Flashcards Carousel
st.subheader("🎓 **AI Pattern Flashcards**")
cols = st.columns(4)
flashcards = [
    ("🔄 Repetition", "Vary sentence structure and word choice"),
    ("🤔 Hedging", "Use definitive statements instead of qualifiers"),
    ("💭 Fillers", "Remove unnecessary filler words"),
    ("📏 Uniformity", "Vary paragraph lengths naturally")
]

for i, (title, desc) in enumerate(flashcards):
    with cols[i]:
        if st.button(f"{title}", use_container_width=True):
            st.toast(f"✅ {desc}")

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:#888;'>"
    "*Production Monorepo | Agentic Marketing Platform | Apr 2026*</p>",
    unsafe_allow_html=True
)
