# -*- coding: utf-8 -*-
# app.py
# SAGE AI — Smart AI Guidance Engine
# Main application orchestrator

import os
import time
from datetime import datetime

os.environ.setdefault("PYTHONIOENCODING", "utf-8")

import streamlit as st
from dotenv import load_dotenv

from styles import get_css
from components.sidebar import render_sidebar
from components.upload import render_upload
from components.results import render_results, render_chat
from services.vision import analyze_screenshot

load_dotenv()

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SAGE AI · Smart AI Guidance Engine",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Session state init ───────────────────────────────────────────────────────
defaults = {
    "history": [],
    "last_result": None,
    "last_filename": None,
    "last_image_bytes": None,
    "analysis_time": None,
    "total_analyses": 0,
    "chat_messages": [],
}
for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val

# ── Inject CSS ───────────────────────────────────────────────────────────────
st.markdown(get_css(), unsafe_allow_html=True)

# ── Top bar ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="topbar">
    <div style="display:flex;align-items:center;gap:14px;">
        <div class="topbar-logo">⚡ SAGE<span class="topbar-logo-dim">AI</span></div>
    </div>
    <div class="topbar-status">
        <div class="status-dot"></div>
        GROQ VISION · ONLINE
    </div>
</div>
""", unsafe_allow_html=True)

# ── Sidebar ──────────────────────────────────────────────────────────────────
api_key, model_choice = render_sidebar()

# ── Main layout ──────────────────────────────────────────────────────────────
col_left, col_right = st.columns([1, 1.6], gap="large")

# ── LEFT COLUMN — Upload ─────────────────────────────────────────────────────
with col_left:
    uploaded_file, explain_clicked = render_upload()

# ── RIGHT COLUMN — Analysis + Chat ──────────────────────────────────────────
with col_right:
    # Handle analysis trigger
    if explain_clicked and uploaded_file:
        if not api_key:
            st.error("API key required — enter your Groq key in the sidebar.")
        else:
            processing_placeholder = st.empty()
            processing_placeholder.markdown("""
            <div class="processing-container">
                <div class="processing-orb"></div>
                <div class="processing-title">Analyzing Screenshot</div>
                <div class="processing-step">↳ Encoding image data...</div>
                <div class="processing-step">↳ Sending to Groq Vision API...</div>
                <div class="processing-step">↳ Awaiting AI response...</div>
                <div class="processing-bar"><div class="processing-bar-inner"></div></div>
            </div>
            """, unsafe_allow_html=True)

            try:
                image_bytes = uploaded_file.getvalue()
                start_time = time.time()

                result = analyze_screenshot(
                    image_bytes=image_bytes,
                    file_name=uploaded_file.name,
                    api_key=api_key,
                    model=model_choice,
                )

                elapsed = round(time.time() - start_time, 1)

                # Store results
                st.session_state.last_result = result
                st.session_state.last_filename = uploaded_file.name
                st.session_state.last_image_bytes = image_bytes
                st.session_state.analysis_time = elapsed
                st.session_state.total_analyses += 1
                st.session_state.chat_messages = []

                # Add to history
                st.session_state.history.append({
                    "name": uploaded_file.name,
                    "result": result,
                    "time": elapsed,
                    "timestamp": datetime.now().strftime("%H:%M"),
                    "image_bytes": image_bytes,
                })

                processing_placeholder.empty()
                st.rerun()

            except Exception as e:
                processing_placeholder.empty()
                st.error(f"Analysis failed: {str(e)}")
                with st.expander("Troubleshooting", expanded=True):
                    st.markdown("""
                    | Issue | Solution |
                    |-------|----------|
                    | `AuthenticationError` | Verify your API key starts with `gsk_` |
                    | `Model not found` | The selected model may be temporarily unavailable |
                    | Timeout | Check your internet connection and retry |
                    | Blank output | Try a clearer, higher-resolution screenshot |

                    **Get a free API key:** [console.groq.com](https://console.groq.com)
                    """)

    # Display results
    render_results()

    # Chat with screenshot
    render_chat(api_key, model_choice)