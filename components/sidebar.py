# components/sidebar.py
# SAGE AI — Sidebar UI Component

import os
import streamlit as st


def render_sidebar():
    """Render the sidebar and return (api_key, model_choice)."""
    with st.sidebar:
        # Brand
        st.markdown("""
        <div class="sidebar-brand">
            <div class="sidebar-brand-icon">⚡</div>
            <div class="sidebar-brand-name">SAGE AI</div>
            <div class="sidebar-brand-sub">Smart AI Guidance Engine</div>
        </div>
        """, unsafe_allow_html=True)

        # Session Stats
        total_count = st.session_state.total_analyses
        history_count = len(st.session_state.history)

        st.markdown(f"""
        <div class="sidebar-stats">
            <div class="stat-item">
                <div class="stat-value">{total_count}</div>
                <div class="stat-label">Analyses</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">{history_count}</div>
                <div class="stat-label">In History</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Configuration
        st.markdown('<div class="sidebar-label"><span class="sidebar-label-icon">⚙</span> Configuration</div>', unsafe_allow_html=True)

        # Load API key from environment / secrets
        env_key = ""
        try:
            env_key = st.secrets.get("GROQ_API_KEY", "")
        except Exception:
            pass
        if not env_key:
            env_key = os.environ.get("GROQ_API_KEY", os.environ.get("OPENAI_API_KEY", ""))

        api_key = st.text_input(
            "GROQ API KEY",
            value=env_key,
            type="password",
            placeholder="gsk_••••••••••••••••••••",
            help="Free key from console.groq.com — auto-loaded from secrets/env.",
        )

        model_choice = st.selectbox(
            "MODEL",
            options=["meta-llama/llama-4-scout-17b-16e-instruct"],
            index=0,
            help="Groq's active vision model",
        )

        st.markdown("---")

        # Tips
        st.markdown('<div class="sidebar-label"><span class="sidebar-label-icon">💡</span> Quick Tips</div>', unsafe_allow_html=True)
        tips = [
            ("📸", "Clear, high-res screenshots yield best results"),
            ("📁", "Supports PNG, JPG, WEBP, and GIF formats"),
            ("📏", "Max recommended size: 4 MB (auto-resized)"),
            ("🎯", "Best for errors, code, terminals, and UI screens"),
            ("💬", "Ask follow-up questions after analysis"),
        ]
        for icon, tip in tips:
            st.markdown(f'<div class="tip-item"><span class="tip-arrow">{icon}</span>{tip}</div>', unsafe_allow_html=True)

        st.markdown("---")

        # History
        st.markdown('<div class="sidebar-label"><span class="sidebar-label-icon">📋</span> Session History</div>', unsafe_allow_html=True)

        if st.session_state.history:
            for i, entry in enumerate(reversed(st.session_state.history)):
                short_name = (entry["name"][:20] + "…") if len(entry["name"]) > 20 else entry["name"]
                if st.button(f"📄 {short_name}", key=f"history_{i}", use_container_width=True):
                    st.session_state.last_result = entry["result"]
                    st.session_state.last_filename = entry["name"]
                    st.session_state.analysis_time = entry.get("time", None)
                    st.session_state.last_image_bytes = entry.get("image_bytes", None)
                    st.session_state.chat_messages = []
                    st.rerun()
        else:
            st.markdown('<div style="font-family:var(--mono);font-size:0.68rem;color:var(--text-4);text-align:center;padding:12px 0;">No analyses yet</div>', unsafe_allow_html=True)

        st.markdown("---")

        # Footer
        st.markdown("""
        <div class="sidebar-footer">
            POWERED BY GROQ + LLAMA 4 SCOUT<br>
            BUILT WITH STREAMLIT<br>
            <span style="color:var(--accent);opacity:0.6;">■</span> PRODUCTION BUILD
        </div>
        """, unsafe_allow_html=True)

    return api_key, model_choice
