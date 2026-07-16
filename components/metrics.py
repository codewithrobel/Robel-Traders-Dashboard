import streamlit as st

def render_metrics():
    c1, c2, c3, c4 = st.columns(4)

    c1.metric("📦 Products", "LIVE")
    c2.metric("🤖 AI Engine", "ACTIVE")
    c3.metric("💾 Backup", "ENABLED")
    c4.metric("🟢 Status", "ONLINE")