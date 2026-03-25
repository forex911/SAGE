# -*- coding: utf-8 -*-
# app.py
# ScreenSight AI -- Production-Grade UI

import os
import time
from datetime import datetime

# Fix Windows console encoding
os.environ.setdefault('PYTHONIOENCODING', 'utf-8')

import streamlit as st
from dotenv import load_dotenv
from vision import analyze_screenshot
from utils import save_uploaded_image, format_file_size

# Load .env file if present (auto-fills API key)
load_dotenv()

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ScreenSight AI · Intelligent Screenshot Analysis",
    page_icon="zap",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Session state init ────────────────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []
if "last_result" not in st.session_state:
    st.session_state.last_result = None
if "last_filename" not in st.session_state:
    st.session_state.last_filename = None
if "analysis_time" not in st.session_state:
    st.session_state.analysis_time = None
if "total_analyses" not in st.session_state:
    st.session_state.total_analyses = 0
if "theme" not in st.session_state:
    st.session_state.theme = "midnight"

# ── CSS Design System ─────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600;700;800;900&display=swap');

/* ═══════════════ DESIGN TOKENS ═══════════════ */
:root {
    --bg-primary:    #faf8f5;
    --bg-secondary:  #f5f2ed;
    --bg-tertiary:   #efe9e1;
    --surface:       #ffffff;
    --surface-2:     #f9f7f4;
    --surface-3:     #f0ece6;
    --glass:         rgba(255, 255, 255, 0.85);
    --glass-border:  rgba(0, 0, 0, 0.06);
    --border:        rgba(0, 0, 0, 0.08);
    --border-2:      rgba(0, 0, 0, 0.12);
    --border-glow:   rgba(13, 148, 136, 0.08);

    --accent:        #0d9488;
    --accent-dim:    #0f766e;
    --accent-glow:   rgba(13, 148, 136, 0.1);
    --green:         #059669;
    --green-dim:     #047857;
    --green-glow:    rgba(5, 150, 105, 0.1);
    --amber:         #d97706;
    --red:           #dc2626;
    --purple:        #7c3aed;
    --pink:          #db2777;

    --text:          #1a1a1a;
    --text-2:        #4a4a4a;
    --text-3:        #737373;
    --text-4:        #a3a3a3;

    --mono:          'JetBrains Mono', monospace;
    --sans:          'Inter', -apple-system, system-ui, sans-serif;

    --radius:        14px;
    --radius-sm:     10px;
    --radius-lg:     18px;

    --shadow-sm:     0 1px 3px rgba(0,0,0,0.04), 0 1px 2px rgba(0,0,0,0.06);
    --shadow-md:     0 4px 16px rgba(0,0,0,0.06), 0 2px 4px rgba(0,0,0,0.04);
    --shadow-lg:     0 12px 40px rgba(0,0,0,0.08), 0 4px 12px rgba(0,0,0,0.04);
    --shadow-glow:   0 0 20px rgba(13, 148, 136, 0.05);
}

*, *::before, *::after {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

html, body, [class*="css"] {
    font-family: var(--sans) !important;
    background: var(--bg-primary) !important;
    color: var(--text) !important;
}

.stApp {
    background: var(--bg-primary) !important;
}

/* ═══════════════ AMBIENT BACKGROUND ═══════════════ */
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background:
        radial-gradient(ellipse 70% 50% at 10% 0%, rgba(13,148,136,0.03) 0%, transparent 55%),
        radial-gradient(ellipse 55% 45% at 90% 100%, rgba(217,119,6,0.02) 0%, transparent 50%);
    pointer-events: none;
    z-index: 0;
}

/* ═══════════════ HIDE STREAMLIT DEFAULTS ═══════════════ */
#MainMenu, footer, header { visibility: hidden !important; }
.stDeployButton { display: none !important; }
[data-testid="stToolbar"] { display: none !important; }
[data-testid="stDecoration"] { display: none !important; }

/* ═══════════════ SIDEBAR ═══════════════ */
section[data-testid="stSidebar"] {
    background: var(--bg-secondary) !important;
    border-right: 1px solid var(--border) !important;
    width: 310px !important;
}
section[data-testid="stSidebar"] > div {
    padding: 1.2rem 1.4rem 1rem 1.4rem !important;
}

/* ═══════════════ INPUTS ═══════════════ */
.stTextInput > div > div > input {
    background: var(--surface) !important;
    border: 1px solid var(--border-2) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text) !important;
    font-family: var(--mono) !important;
    font-size: 0.8rem !important;
    caret-color: var(--accent);
    padding: 0.75rem 1rem !important;
    transition: all 0.25s cubic-bezier(0.4,0,0.2,1) !important;
    height: 44px !important;
}
.stTextInput > div > div > input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px var(--accent-glow), var(--shadow-glow) !important;
}
.stTextInput label {
    color: var(--text-3) !important;
    font-family: var(--mono) !important;
    font-size: 0.66rem !important;
    letter-spacing: 0.14em !important;
    text-transform: uppercase !important;
    margin-bottom: 4px !important;
}

.stSelectbox > div > div {
    background: var(--surface) !important;
    border: 1px solid var(--border-2) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text) !important;
    font-size: 0.82rem !important;
    transition: all 0.25s cubic-bezier(0.4,0,0.2,1) !important;
}
.stSelectbox > div > div:hover {
    border-color: var(--accent-dim) !important;
}
.stSelectbox label {
    color: var(--text-3) !important;
    font-family: var(--mono) !important;
    font-size: 0.66rem !important;
    letter-spacing: 0.14em !important;
    text-transform: uppercase !important;
    margin-bottom: 4px !important;
}

/* ═══════════════ PRIMARY BUTTON ═══════════════ */
.stButton > button {
    background: linear-gradient(135deg, var(--accent-dim) 0%, var(--accent) 100%) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: var(--radius-sm) !important;
    font-family: var(--mono) !important;
    font-size: 0.78rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.1em !important;
    padding: 0.8rem 1.6rem !important;
    transition: all 0.3s cubic-bezier(0.4,0,0.2,1) !important;
    box-shadow: var(--shadow-md) !important;
    text-transform: uppercase !important;
    position: relative !important;
    overflow: hidden !important;
    height: 46px !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: var(--shadow-lg) !important;
    color: #ffffff !important;
    background: linear-gradient(135deg, var(--accent) 0%, #2dd4bf 100%) !important;
}
.stButton > button:active {
    transform: translateY(0px) !important;
    box-shadow: var(--shadow-sm) !important;
}

/* ═══════════════ DOWNLOAD BUTTON ═══════════════ */
.stDownloadButton > button {
    background: var(--surface-2) !important;
    color: var(--text-2) !important;
    border: 1px solid var(--border-2) !important;
    border-radius: var(--radius-sm) !important;
    font-family: var(--mono) !important;
    font-size: 0.72rem !important;
    font-weight: 500 !important;
    padding: 0.6rem 1rem !important;
    transition: all 0.25s cubic-bezier(0.4,0,0.2,1) !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    height: 40px !important;
}
.stDownloadButton > button:hover {
    border-color: var(--accent) !important;
    color: var(--accent) !important;
    background: rgba(13,148,136,0.06) !important;
    box-shadow: var(--shadow-md) !important;
}

/* ═══════════════ FILE UPLOADER ═══════════════ */
[data-testid="stFileUploader"] {
    background: var(--surface) !important;
    border: 2px dashed var(--border-2) !important;
    border-radius: var(--radius) !important;
    transition: all 0.35s cubic-bezier(0.4,0,0.2,1) !important;
    position: relative !important;
    padding: 1.2rem !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: var(--accent) !important;
    box-shadow: var(--shadow-md) !important;
    background: rgba(13,148,136,0.02) !important;
}

/* ═══════════════ IMAGE ═══════════════ */
[data-testid="stImage"] img {
    border-radius: var(--radius) !important;
    border: 1px solid var(--border) !important;
    box-shadow: var(--shadow-md) !important;
    transition: all 0.3s ease !important;
}
[data-testid="stImage"] img:hover {
    box-shadow: var(--shadow-lg) !important;
    border-color: var(--border-2) !important;
}

/* ═══════════════ ALERTS ═══════════════ */
.stAlert {
    border-radius: var(--radius-sm) !important;
    font-family: var(--mono) !important;
    font-size: 0.82rem !important;
    backdrop-filter: blur(12px) !important;
}

/* ═══════════════ EXPANDER ═══════════════ */
.streamlit-expanderHeader {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
    font-family: var(--mono) !important;
    font-size: 0.78rem !important;
    color: var(--text-2) !important;
}
.streamlit-expanderContent {
    background: var(--surface-2) !important;
    border: 1px solid var(--border) !important;
    border-top: none !important;
    border-radius: 0 0 var(--radius-sm) var(--radius-sm) !important;
}

/* ═══════════════ TABS ═══════════════ */
.stTabs [data-baseweb="tab-list"] {
    gap: 2px !important;
    background: var(--surface) !important;
    border-radius: var(--radius-sm) !important;
    padding: 5px !important;
    border: 1px solid var(--border) !important;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 7px !important;
    font-family: var(--mono) !important;
    font-size: 0.7rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    color: var(--text-3) !important;
    padding: 9px 20px !important;
    transition: all 0.25s cubic-bezier(0.4,0,0.2,1) !important;
}
.stTabs [data-baseweb="tab"]:hover {
    color: var(--text-2) !important;
    background: rgba(13,148,136,0.04) !important;
}
.stTabs [aria-selected="true"] {
    background: rgba(13,148,136,0.1) !important;
    color: var(--accent) !important;
    border: none !important;
    font-weight: 600 !important;
}
.stTabs [data-baseweb="tab-highlight"] {
    display: none !important;
}
.stTabs [data-baseweb="tab-border"] {
    display: none !important;
}

/* ═══════════════ SCROLLBAR ═══════════════ */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: var(--bg-primary); }
::-webkit-scrollbar-thumb { background: rgba(0,0,0,0.12); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: rgba(0,0,0,0.2); }

/* ═══════════════ CAPTION / HR ═══════════════ */
.stCaption {
    color: var(--text-4) !important;
    font-family: var(--mono) !important;
    font-size: 0.68rem !important;
}
hr {
    border-color: var(--border) !important;
    opacity: 0.5 !important;
}

/* ═══════════════ ANIMATIONS ═══════════════ */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(16px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes fadeIn {
    from { opacity: 0; }
    to   { opacity: 1; }
}
@keyframes slideInRight {
    from { opacity: 0; transform: translateX(20px); }
    to   { opacity: 1; transform: translateX(0); }
}
@keyframes pulse-dot {
    0%, 100% { opacity: 1; transform: scale(1); }
    50%      { opacity: 0.4; transform: scale(0.85); }
}
@keyframes shimmer {
    0%   { background-position: -200% 0; }
    100% { background-position: 200% 0; }
}
@keyframes borderGlow {
    0%, 100% { border-color: rgba(56,189,248,0.15); }
    50%      { border-color: rgba(56,189,248,0.35); }
}
@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50%      { transform: translateY(-6px); }
}
@keyframes gradientShift {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* ═══════════════ CUSTOM COMPONENTS ═══════════════ */
.topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.9rem 2rem;
    background: var(--glass);
    backdrop-filter: blur(24px);
    -webkit-backdrop-filter: blur(24px);
    border-bottom: 1px solid var(--glass-border);
    margin: -1rem -1rem 2rem -1rem;
    animation: fadeIn 0.5s ease;
}
.topbar-left {
    display: flex;
    align-items: center;
    gap: 14px;
}
.topbar-logo {
    font-family: var(--sans);
    font-size: 1.2rem;
    font-weight: 800;
    background: linear-gradient(135deg, var(--accent) 0%, var(--green) 50%, var(--accent-dim) 100%);
    background-size: 200% 200%;
    animation: gradientShift 6s ease infinite;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -0.01em;
}
.topbar-logo-dim {
    font-weight: 400;
    opacity: 0.6;
}
.topbar-version {
    background: rgba(13,148,136,0.08);
    border: 1px solid rgba(13,148,136,0.18);
    color: var(--accent);
    font-family: var(--mono);
    font-size: 0.56rem;
    font-weight: 600;
    letter-spacing: 0.14em;
    padding: 4px 12px;
    border-radius: 20px;
    text-transform: uppercase;
}
.topbar-status {
    display: flex;
    align-items: center;
    gap: 10px;
    font-family: var(--mono);
    font-size: 0.66rem;
    color: var(--text-3);
    letter-spacing: 0.1em;
    text-transform: uppercase;
}
.status-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: var(--green);
    box-shadow: 0 0 8px var(--green-glow), 0 0 3px var(--green);
    animation: pulse-dot 2.5s ease-in-out infinite;
    flex-shrink: 0;
}
.status-dot-static {
    animation: none;
}

/* Panel Labels */
.panel-label {
    font-family: var(--mono);
    font-size: 0.62rem;
    font-weight: 600;
    color: var(--text-3);
    letter-spacing: 0.16em;
    text-transform: uppercase;
    margin-bottom: 1.2rem;
    display: flex;
    align-items: center;
    gap: 12px;
    animation: fadeIn 0.6s ease;
}
.panel-label-num {
    color: var(--accent);
    font-weight: 700;
    font-size: 0.66rem;
}
.panel-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, var(--border-2), transparent);
}

/* Metadata Chips */
.meta-row {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 0.8rem;
    animation: fadeInUp 0.4s ease;
}
.meta-chip {
    background: var(--glass);
    backdrop-filter: blur(8px);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 5px 12px;
    font-family: var(--mono);
    font-size: 0.66rem;
    color: var(--text-3);
    display: flex;
    align-items: center;
    gap: 6px;
    transition: all 0.2s;
}
.meta-chip:hover {
    border-color: var(--accent-dim);
    color: var(--text-2);
}
.meta-chip b {
    color: var(--accent);
    font-weight: 600;
}

/* Empty States */
.empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 240px;
    border: 1.5px dashed var(--border-2);
    border-radius: var(--radius-lg);
    color: var(--text-4);
    font-family: var(--mono);
    font-size: 0.74rem;
    gap: 0.8rem;
    background: var(--glass);
    backdrop-filter: blur(8px);
    letter-spacing: 0.08em;
    animation: fadeIn 0.6s ease;
    transition: all 0.35s cubic-bezier(0.4,0,0.2,1);
    text-transform: uppercase;
}
.empty-state:hover {
    border-color: rgba(13,148,136,0.25);
    background: rgba(13,148,136,0.02);
}
.empty-icon {
    font-size: 2.8rem;
    opacity: 0.15;
    animation: float 4s ease-in-out infinite;
    margin-bottom: 0.2rem;
}
.empty-subtitle {
    font-size: 0.62rem;
    opacity: 0.35;
    letter-spacing: 0.06em;
    font-weight: 400;
}

/* Result Header */
.result-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1rem;
    padding-bottom: 0.8rem;
    border-bottom: 1px solid var(--border);
    animation: fadeIn 0.5s ease;
}
.result-status {
    display: flex;
    align-items: center;
    gap: 10px;
    font-family: var(--mono);
    font-size: 0.72rem;
    font-weight: 600;
    color: var(--green);
    letter-spacing: 0.1em;
    text-transform: uppercase;
}
.result-time {
    font-family: var(--mono);
    font-size: 0.66rem;
    color: var(--text-4);
    letter-spacing: 0.06em;
}

/* Result Body */
.result-body {
    background: var(--glass);
    backdrop-filter: blur(12px);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.8rem 2rem;
    font-size: 0.88rem;
    line-height: 1.85;
    color: var(--text);
    max-height: 65vh;
    overflow-y: auto;
    animation: fadeInUp 0.5s ease;
    box-shadow: var(--shadow-md);
}
.result-body h1, .result-body h2, .result-body h3 {
    color: var(--accent) !important;
    font-family: var(--sans) !important;
    margin-top: 1.4em !important;
    margin-bottom: 0.5em !important;
    font-weight: 700 !important;
}
.result-body h4, .result-body h5, .result-body h6 {
    color: var(--text) !important;
    font-family: var(--sans) !important;
    margin-top: 1.1em !important;
    margin-bottom: 0.4em !important;
    font-weight: 600 !important;
}
.result-body code {
    background: var(--surface-3) !important;
    color: var(--accent-dim) !important;
    padding: 2px 7px !important;
    border-radius: 5px !important;
    font-family: var(--mono) !important;
    font-size: 0.82em !important;
    border: 1px solid var(--border) !important;
}
.result-body pre {
    background: var(--bg-primary) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
    padding: 1.2rem !important;
    overflow-x: auto !important;
    margin: 0.8em 0 !important;
}
.result-body pre code {
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
}
.result-body strong {
    color: var(--text) !important;
    font-weight: 600 !important;
}
.result-body ul, .result-body ol {
    padding-left: 1.5em !important;
    margin: 0.5em 0 !important;
}
.result-body li {
    margin-bottom: 0.35em !important;
}
.result-body blockquote {
    border-left: 3px solid var(--accent) !important;
    padding-left: 1.2em !important;
    color: var(--text-2) !important;
    font-style: normal !important;
    margin: 0.8em 0 !important;
    background: rgba(13,148,136,0.04) !important;
    border-radius: 0 var(--radius-sm) var(--radius-sm) 0 !important;
    padding: 0.9em 1.2em !important;
    font-size: 0.86rem !important;
    line-height: 1.7 !important;
}

/* ═══════════════ SIDEBAR CUSTOM ═══════════════ */
.sidebar-brand {
    text-align: center;
    padding: 0.8rem 0 1.4rem 0;
    border-bottom: 1px solid var(--border);
    margin-bottom: 1.4rem;
}
.sidebar-brand-icon {
    font-size: 2.2rem;
    margin-bottom: 0.4rem;
    filter: drop-shadow(0 0 10px rgba(13,148,136,0.2));
}
.sidebar-brand-name {
    font-family: var(--sans);
    font-size: 1rem;
    font-weight: 700;
    color: var(--text);
    letter-spacing: 0em;
}
.sidebar-brand-sub {
    font-family: var(--mono);
    font-size: 0.56rem;
    color: var(--text-4);
    letter-spacing: 0.16em;
    text-transform: uppercase;
    margin-top: 4px;
}
.sidebar-label {
    font-family: var(--mono);
    font-size: 0.58rem;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: var(--text-4);
    margin-bottom: 0.7rem;
    margin-top: 0.6rem;
    display: flex;
    align-items: center;
    gap: 7px;
}
.sidebar-label-icon {
    color: var(--accent);
    font-size: 0.68rem;
}
.tip-item {
    display: flex;
    align-items: flex-start;
    gap: 10px;
    font-size: 0.74rem;
    color: var(--text-3);
    margin-bottom: 0.35rem;
    font-family: var(--sans);
    line-height: 1.55;
    padding: 7px 10px;
    border-radius: 8px;
    transition: all 0.2s;
}
.tip-item:hover {
    background: rgba(13,148,136,0.04);
    color: var(--text-2);
}
.tip-arrow {
    color: var(--accent);
    flex-shrink: 0;
    font-size: 0.82rem;
}
.sidebar-footer {
    font-family: var(--mono);
    font-size: 0.56rem;
    color: var(--text-4);
    padding-top: 1.2rem;
    border-top: 1px solid var(--border);
    letter-spacing: 0.08em;
    line-height: 2;
    text-align: center;
}
.sidebar-stats {
    display: flex;
    justify-content: center;
    gap: 24px;
    margin: 0.8rem 0 1rem 0;
    padding: 14px 10px;
    background: var(--surface);
    border-radius: var(--radius-sm);
    border: 1px solid var(--border);
}
.stat-item {
    text-align: center;
}
.stat-value {
    font-family: var(--mono);
    font-size: 1.2rem;
    font-weight: 700;
    color: var(--accent);
    line-height: 1.3;
}
.stat-label {
    font-family: var(--mono);
    font-size: 0.52rem;
    color: var(--text-4);
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-top: 2px;
}

/* ═══════════════ HISTORY PANEL ═══════════════ */
.history-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 8px 10px;
    background: var(--surface-2);
    border: 1px solid var(--border);
    border-radius: 8px;
    margin-bottom: 6px;
    cursor: pointer;
    transition: all 0.2s;
    font-family: var(--mono);
    font-size: 0.68rem;
    color: var(--text-3);
}
.history-item:hover {
    border-color: var(--accent-dim);
    background: rgba(13,148,136,0.04);
    color: var(--text-2);
}
.history-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: var(--accent);
    flex-shrink: 0;
    opacity: 0.6;
}
.history-name {
    flex: 1;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}
.history-time {
    color: var(--text-4);
    font-size: 0.6rem;
    flex-shrink: 0;
}

/* ═══════════════ PROCESSING ANIMATION ═══════════════ */
.processing-container {
    padding: 2.5rem 1.5rem;
    text-align: center;
    animation: fadeIn 0.4s ease;
}
.processing-orb {
    width: 60px;
    height: 60px;
    margin: 0 auto 1.5rem auto;
    border-radius: 50%;
    background: linear-gradient(135deg, var(--accent), var(--green));
    box-shadow: 0 0 30px var(--accent-glow);
    animation: pulse-dot 1.8s ease-in-out infinite;
}
.processing-title {
    font-family: var(--mono);
    font-size: 0.82rem;
    font-weight: 600;
    color: var(--text);
    letter-spacing: 0.08em;
    margin-bottom: 0.6rem;
    text-transform: uppercase;
}
.processing-step {
    font-family: var(--mono);
    font-size: 0.7rem;
    color: var(--text-3);
    letter-spacing: 0.06em;
    margin-bottom: 0.3rem;
}
.processing-bar {
    width: 200px;
    height: 3px;
    margin: 1rem auto 0 auto;
    border-radius: 2px;
    background: var(--surface-3);
    overflow: hidden;
}
.processing-bar-inner {
    height: 100%;
    width: 40%;
    border-radius: 2px;
    background: linear-gradient(90deg, var(--accent), var(--green), var(--accent));
    background-size: 200% 100%;
    animation: shimmer 1.5s linear infinite;
}

/* ═══════════════ ACTION BAR ═══════════════ */
.action-bar {
    display: flex;
    gap: 8px;
    padding: 12px 16px;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    margin-top: 1rem;
    animation: fadeInUp 0.5s ease 0.2s both;
}

/* ═══════════════ KEYBOARD SHORTCUTS ═══════════════ */
.kbd {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 2px 6px;
    background: var(--surface-2);
    border: 1px solid var(--border-2);
    border-radius: 4px;
    font-family: var(--mono);
    font-size: 0.6rem;
    color: var(--text-3);
    min-width: 20px;
    text-align: center;
}

/* ═══════════════ COPY BUTTON ═══════════════ */
.copy-btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
    width: 100%;
    padding: 0.6rem 1rem;
    background: var(--surface-2);
    border: 1px solid var(--border-2);
    border-radius: var(--radius-sm);
    font-family: var(--mono);
    font-size: 0.72rem;
    font-weight: 500;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--text-2);
    cursor: pointer;
    transition: all 0.25s cubic-bezier(0.4,0,0.2,1);
    height: 40px;
}
.copy-btn:hover {
    border-color: var(--accent);
    color: var(--accent);
    background: rgba(13,148,136,0.06);
}
.copy-btn.copied {
    border-color: var(--green);
    color: var(--green);
    background: rgba(5,150,105,0.06);
}

/* ═══════════════ NOTION-STYLE RESULT ENHANCEMENTS ═══════════════ */
.result-body h3 {
    border-bottom: 1px solid var(--border) !important;
    padding-bottom: 0.4em !important;
    margin-top: 1.6em !important;
}
.result-body h3:first-child {
    margin-top: 0 !important;
}
.result-body hr {
    border: none !important;
    height: 1px !important;
    background: var(--border-2) !important;
    margin: 1.5em 0 !important;
}
.result-body ol {
    counter-reset: notion-counter !important;
}
.result-body ol > li {
    position: relative !important;
}
</style>
""", unsafe_allow_html=True)

# ── Top bar ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="topbar">
    <div class="topbar-left">
        <div class="topbar-logo">⚡ ScreenSight<span class="topbar-logo-dim">.ai</span></div>
        <div class="topbar-version">v3.0 pro</div>
    </div>
    <div class="topbar-status">
        <div class="status-dot"></div>
        GROQ VISION · ONLINE
    </div>
</div>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    # Brand
    st.markdown("""
    <div class="sidebar-brand">
        <div class="sidebar-brand-icon">⚡</div>
        <div class="sidebar-brand-name">ScreenSight AI</div>
        <div class="sidebar-brand-sub">Intelligent Screenshot Analysis</div>
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

    # Configuration Section
    st.markdown('<div class="sidebar-label"><span class="sidebar-label-icon">⚙</span> Configuration</div>', unsafe_allow_html=True)

    # Load API key from environment as default (supports .env file)
    env_key = os.environ.get("GROQ_API_KEY", os.environ.get("OPENAI_API_KEY", ""))

    api_key = st.text_input(
        "GROQ API KEY",
        value=env_key,
        type="password",
        placeholder="gsk_••••••••••••••••••••",
        help="Free key from console.groq.com — auto-loaded from .env if available.",
    )

    model_choice = st.selectbox(
        "MODEL",
        options=["meta-llama/llama-4-scout-17b-16e-instruct"],
        index=0,
        help="Groq's active vision model",
    )

    st.markdown("---")

    # Tips Section
    st.markdown('<div class="sidebar-label"><span class="sidebar-label-icon">💡</span> Quick Tips</div>', unsafe_allow_html=True)

    tips = [
        ("📸", "Clear, high-res screenshots yield best results"),
        ("📁", "Supports PNG, JPG, WEBP, and GIF formats"),
        ("📏", "Max recommended size: 4 MB (auto-resized)"),
        ("🎯", "Best for errors, code, terminals, and UI screens"),
        ("⚡", "Analysis typically takes 3–8 seconds"),
    ]
    for icon, tip in tips:
        st.markdown(f'<div class="tip-item"><span class="tip-arrow">{icon}</span>{tip}</div>', unsafe_allow_html=True)

    st.markdown("---")

    # History Section
    st.markdown('<div class="sidebar-label"><span class="sidebar-label-icon">📋</span> Session History</div>', unsafe_allow_html=True)

    if st.session_state.history:
        for i, entry in enumerate(reversed(st.session_state.history)):
            short_name = (entry["name"][:20] + "…") if len(entry["name"]) > 20 else entry["name"]
            if st.button(f"📄 {short_name}", key=f"history_{i}", use_container_width=True):
                st.session_state.last_result = entry["result"]
                st.session_state.last_filename = entry["name"]
                st.session_state.analysis_time = entry.get("time", None)
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


# ── Main layout ───────────────────────────────────────────────────────────────
col_left, col_right = st.columns([1, 1.6], gap="large")

# ── LEFT COLUMN — Upload ─────────────────────────────────────────────────────
with col_left:
    st.markdown('<div class="panel-label"><span class="panel-label-num">01</span> Upload Target</div>', unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Drop screenshot here",
        type=["png", "jpg", "jpeg", "webp", "gif"],
        label_visibility="collapsed",
    )

    if uploaded_file:
        st.image(uploaded_file, use_column_width=True)

        file_size = format_file_size(len(uploaded_file.getvalue()))
        name_short = (uploaded_file.name[:24] + "…") if len(uploaded_file.name) > 24 else uploaded_file.name
        ftype = uploaded_file.type.split("/")[-1].upper()

        # Get image dimensions
        try:
            from PIL import Image
            import io
            img = Image.open(io.BytesIO(uploaded_file.getvalue()))
            dims = f"{img.width}×{img.height}"
        except Exception:
            dims = "N/A"

        st.markdown(f"""
        <div class="meta-row">
            <div class="meta-chip"><b>FILE</b> {name_short}</div>
            <div class="meta-chip"><b>SIZE</b> {file_size}</div>
            <div class="meta-chip"><b>TYPE</b> {ftype}</div>
            <div class="meta-chip"><b>DIM</b> {dims}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        explain_clicked = st.button(">> RUN ANALYSIS", use_container_width=True)
    else:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-icon">◈</div>
            <div>NO FILE SELECTED</div>
            <div class="empty-subtitle">drag & drop or click to browse</div>
            <div class="empty-subtitle">PNG · JPG · WEBP · GIF</div>
        </div>
        """, unsafe_allow_html=True)
        explain_clicked = False

# ── RIGHT COLUMN — Analysis Output ──────────────────────────────────────────
with col_right:
    st.markdown('<div class="panel-label"><span class="panel-label-num">02</span> Analysis Output</div>', unsafe_allow_html=True)

    if not uploaded_file and not st.session_state.last_result:
        st.markdown("""
        <div class="empty-state" style="min-height:300px;">
            <div class="empty-icon">◉</div>
            <div>AWAITING INPUT</div>
            <div class="empty-subtitle">upload a screenshot to begin analysis</div>
        </div>
        """, unsafe_allow_html=True)

    elif explain_clicked:
        if not api_key:
            st.error("API key required -- enter your Groq key in the sidebar.")
        else:
            # Custom processing animation
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
                save_uploaded_image(image_bytes, uploaded_file.name)

                start_time = time.time()

                result = analyze_screenshot(
                    image_bytes=image_bytes,
                    file_name=uploaded_file.name,
                    api_key=api_key,
                    model=model_choice,
                )

                elapsed = round(time.time() - start_time, 1)

                st.session_state.last_result = result
                st.session_state.last_filename = uploaded_file.name
                st.session_state.analysis_time = elapsed
                st.session_state.total_analyses += 1

                # Add to history
                st.session_state.history.append({
                    "name": uploaded_file.name,
                    "result": result,
                    "time": elapsed,
                    "timestamp": datetime.now().strftime("%H:%M"),
                })

                processing_placeholder.empty()
                st.rerun()

            except Exception as e:
                processing_placeholder.empty()
                st.error(f"Analysis failed: {str(e)}")
                st.markdown("---")
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

    # ── Display result ────────────────────────────────────────────────────────
    if st.session_state.last_result:
        result_text = st.session_state.last_result
        elapsed = st.session_state.analysis_time

        # Result header
        time_display = f"{elapsed}s" if elapsed else "--"
        st.markdown(f"""
        <div class="result-header">
            <div class="result-status">
                <div class="status-dot status-dot-static"></div>
                ANALYSIS COMPLETE
            </div>
            <div class="result-time">⏱ {time_display} · {st.session_state.last_filename or 'screenshot'}</div>
        </div>
        """, unsafe_allow_html=True)

        # Tabs for different views
        tab_formatted, tab_raw = st.tabs(["FORMATTED", "RAW"])

        with tab_formatted:
            st.markdown('<div class="result-body">', unsafe_allow_html=True)
            st.markdown(result_text)
            st.markdown('</div>', unsafe_allow_html=True)

        with tab_raw:
            st.code(result_text, language="markdown")

        # Action bar
        st.markdown("<br>", unsafe_allow_html=True)

        fname = st.session_state.get("last_filename", "screenshot")
        acol1, acol2, acol3, acol4, acol5 = st.columns([1, 1, 1, 1, 1])

        with acol1:
            # Copy to clipboard using JavaScript
            import html
            escaped_text = html.escape(result_text).replace("\n", "\\n").replace("'", "\\'")
            copy_id = "copy-btn-main"
            st.markdown(f"""
            <button class="copy-btn" id="{copy_id}" onclick="
                navigator.clipboard.writeText('{escaped_text}'.replace(/\\n/g, '\n')).then(function() {{
                    var btn = document.getElementById('{copy_id}');
                    btn.textContent = 'COPIED!';
                    btn.classList.add('copied');
                    setTimeout(function() {{
                        btn.textContent = 'COPY TEXT';
                        btn.classList.remove('copied');
                    }}, 2000);
                }});
            ">COPY TEXT</button>
            """, unsafe_allow_html=True)
        with acol2:
            st.download_button(
                label="SAVE .TXT",
                data=result_text,
                file_name=f"analysis_{fname}.txt",
                mime="text/plain",
                use_container_width=True,
            )
        with acol3:
            st.download_button(
                label="SAVE .MD",
                data=result_text,
                file_name=f"analysis_{fname}.md",
                mime="text/markdown",
                use_container_width=True,
            )
        with acol4:
            word_count = len(result_text.split())
            char_count = len(result_text)
            st.markdown(f"""
            <div style="font-family:var(--mono);font-size:0.64rem;color:var(--text-4);padding:8px 0;text-align:center;letter-spacing:0.06em;">
                {word_count} WORDS
            </div>
            """, unsafe_allow_html=True)
        with acol5:
            if st.button("CLEAR", use_container_width=True):
                st.session_state.last_result = None
                st.session_state.last_filename = None
                st.session_state.analysis_time = None
                st.rerun()