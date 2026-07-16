import streamlit as st
from datetime import datetime

def render_hero():
    current_time = datetime.now().strftime("%d %b %Y | %I:%M %p")

    st.markdown(f"""
    <div class="hero-card">
        <div class="main-title">🏆 ROBEL TRADERS</div>
        <div class="sub-title">AI Powered Product Research Platform</div>
        <div style="color:#fbbf24;">📅 {current_time}</div>
    </div>
    """, unsafe_allow_html=True)