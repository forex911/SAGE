# styles.py
# SAGE AI — Complete CSS Design System


def get_css():
    """Return the complete CSS design system."""
    return """<style>
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

    --accent:        #0d9488;
    --accent-dim:    #0f766e;
    --accent-glow:   rgba(13, 148, 136, 0.1);
    --green:         #059669;
    --green-dim:     #047857;
    --green-glow:    rgba(5, 150, 105, 0.1);
    --amber:         #d97706;
    --red:           #dc2626;
    --purple:        #7c3aed;

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

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [class*="css"] {
    font-family: var(--sans) !important;
    background: var(--bg-primary) !important;
    color: var(--text) !important;
}
.stApp { background: var(--bg-primary) !important; }

/* ═══════════════ AMBIENT BACKGROUND ═══════════════ */
.stApp::before {
    content: '';
    position: fixed; inset: 0;
    background:
        radial-gradient(ellipse 70% 50% at 10% 0%, rgba(13,148,136,0.03) 0%, transparent 55%),
        radial-gradient(ellipse 55% 45% at 90% 100%, rgba(217,119,6,0.02) 0%, transparent 50%);
    pointer-events: none; z-index: 0;
}

/* ═══════════════ HIDE STREAMLIT DEFAULTS ═══════════════ */
#MainMenu, footer, header { visibility: hidden !important; }
.stDeployButton { display: none !important; }
[data-testid="stToolbar"] { display: none !important; }
[data-testid="stDecoration"] { display: none !important; }

/* ═══════════════ GLOBAL TEXT COLOR FIX ═══════════════ */
.main [data-testid="stMarkdownContainer"] p,
.main [data-testid="stMarkdownContainer"] li,
.main [data-testid="stMarkdownContainer"] span,
.main [data-testid="stMarkdownContainer"] td,
.main [data-testid="stMarkdownContainer"] th,
.main [data-testid="stMarkdownContainer"] div:not(.topbar):not(.sidebar-brand):not(.sidebar-stats):not(.meta-row) {
    color: var(--text) !important;
}
.main [data-testid="stMarkdownContainer"] h1,
.main [data-testid="stMarkdownContainer"] h2,
.main [data-testid="stMarkdownContainer"] h3 {
    color: var(--accent) !important;
    background: transparent !important;
    -webkit-text-fill-color: var(--accent) !important;
}
.main [data-testid="stMarkdownContainer"] h4,
.main [data-testid="stMarkdownContainer"] h5,
.main [data-testid="stMarkdownContainer"] h6 {
    color: var(--text) !important;
    background: transparent !important;
    -webkit-text-fill-color: var(--text) !important;
}

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
.stTextInput label, .stSelectbox label {
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
.stSelectbox > div > div:hover { border-color: var(--accent-dim) !important; }

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
    overflow: hidden !important;
    height: 46px !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: var(--shadow-lg) !important;
    background: linear-gradient(135deg, var(--accent) 0%, #2dd4bf 100%) !important;
}
.stButton > button:active {
    transform: translateY(0px) !important;
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
}

/* ═══════════════ FILE UPLOADER ═══════════════ */
[data-testid="stFileUploader"] {
    background: var(--surface) !important;
    border: 2px dashed var(--border-2) !important;
    border-radius: var(--radius) !important;
    transition: all 0.35s cubic-bezier(0.4,0,0.2,1) !important;
    padding: 1.2rem !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: var(--accent) !important;
    box-shadow: var(--shadow-md) !important;
}

/* ═══════════════ IMAGE ═══════════════ */
[data-testid="stImage"] img {
    border-radius: var(--radius) !important;
    border: 1px solid var(--border) !important;
    box-shadow: var(--shadow-md) !important;
    transition: all 0.3s ease !important;
}

/* ═══════════════ ALERTS ═══════════════ */
.stAlert {
    border-radius: var(--radius-sm) !important;
    font-family: var(--mono) !important;
    font-size: 0.82rem !important;
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
.stTabs [data-baseweb="tab-highlight"],
.stTabs [data-baseweb="tab-border"] { display: none !important; }

/* ═══════════════ SCROLLBAR ═══════════════ */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: var(--bg-primary); }
::-webkit-scrollbar-thumb { background: rgba(0,0,0,0.12); border-radius: 3px; }

/* ═══════════════ CHAT ELEMENTS ═══════════════ */
[data-testid="stChatMessage"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    padding: 0.8rem 1rem !important;
    margin-bottom: 0.5rem !important;
    box-shadow: var(--shadow-sm) !important;
}
[data-testid="stChatInput"] {
    border-color: var(--border-2) !important;
}
[data-testid="stChatInput"] textarea {
    font-family: var(--sans) !important;
    color: var(--text) !important;
    background: var(--surface) !important;
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
@keyframes pulse-dot {
    0%, 100% { opacity: 1; transform: scale(1); }
    50%      { opacity: 0.4; transform: scale(0.85); }
}
@keyframes shimmer {
    0%   { background-position: -200% 0; }
    100% { background-position: 200% 0; }
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

/* ═══════════════ TOPBAR ═══════════════ */
.topbar {
    display: flex; align-items: center; justify-content: space-between;
    padding: 0.9rem 2rem;
    background: var(--glass);
    backdrop-filter: blur(24px);
    border-bottom: 1px solid var(--glass-border);
    margin: -1rem -1rem 2rem -1rem;
    animation: fadeIn 0.5s ease;
}
.topbar-logo {
    font-family: var(--sans); font-size: 1.2rem; font-weight: 800;
    background: linear-gradient(135deg, var(--accent) 0%, var(--green) 50%, var(--accent-dim) 100%);
    background-size: 200% 200%;
    animation: gradientShift 6s ease infinite;
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text;
}
.topbar-logo-dim { font-weight: 400; opacity: 0.6; }
.topbar-status {
    display: flex; align-items: center; gap: 10px;
    font-family: var(--mono); font-size: 0.66rem;
    color: var(--text-3); letter-spacing: 0.1em; text-transform: uppercase;
}
.status-dot {
    width: 7px; height: 7px; border-radius: 50%;
    background: var(--green);
    box-shadow: 0 0 8px var(--green-glow), 0 0 3px var(--green);
    animation: pulse-dot 2.5s ease-in-out infinite;
}
.status-dot-static { animation: none; }

/* ═══════════════ PANEL LABELS ═══════════════ */
.panel-label {
    font-family: var(--mono); font-size: 0.62rem; font-weight: 600;
    color: var(--text-3); letter-spacing: 0.16em; text-transform: uppercase;
    margin-bottom: 1.2rem;
    display: flex; align-items: center; gap: 12px;
    animation: fadeIn 0.6s ease;
}
.panel-label-num { color: var(--accent); font-weight: 700; font-size: 0.66rem; }
.panel-label::after {
    content: ''; flex: 1; height: 1px;
    background: linear-gradient(90deg, var(--border-2), transparent);
}

/* ═══════════════ META CHIPS ═══════════════ */
.meta-row {
    display: flex; flex-wrap: wrap; gap: 8px;
    margin-top: 0.8rem; animation: fadeInUp 0.4s ease;
}
.meta-chip {
    background: var(--glass); backdrop-filter: blur(8px);
    border: 1px solid var(--border); border-radius: 6px;
    padding: 5px 12px; font-family: var(--mono);
    font-size: 0.66rem; color: var(--text-3);
    display: flex; align-items: center; gap: 6px;
    transition: all 0.2s;
}
.meta-chip b { color: var(--accent); font-weight: 600; }

/* ═══════════════ EMPTY STATE ═══════════════ */
.empty-state {
    display: flex; flex-direction: column; align-items: center; justify-content: center;
    min-height: 240px; border: 1.5px dashed var(--border-2);
    border-radius: var(--radius-lg); color: var(--text-4);
    font-family: var(--mono); font-size: 0.74rem;
    gap: 0.8rem; background: var(--glass);
    letter-spacing: 0.08em; animation: fadeIn 0.6s ease;
    text-transform: uppercase;
}
.empty-state:hover { border-color: rgba(13,148,136,0.25); }
.empty-icon { font-size: 2.8rem; opacity: 0.15; animation: float 4s ease-in-out infinite; }
.empty-subtitle { font-size: 0.62rem; opacity: 0.35; letter-spacing: 0.06em; }

/* ═══════════════ RESULT HEADER ═══════════════ */
.result-header {
    display: flex; align-items: center; justify-content: space-between;
    margin-bottom: 1rem; padding-bottom: 0.8rem;
    border-bottom: 1px solid var(--border);
    animation: fadeIn 0.5s ease;
}
.result-status {
    display: flex; align-items: center; gap: 10px;
    font-family: var(--mono); font-size: 0.72rem; font-weight: 600;
    color: var(--green); letter-spacing: 0.1em; text-transform: uppercase;
}
.result-time {
    font-family: var(--mono); font-size: 0.66rem;
    color: var(--text-4); letter-spacing: 0.06em;
}

/* ═══════════════ RESULT BODY (rendered HTML) ═══════════════ */
.result-body {
    background: var(--surface);
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
    color: var(--accent);
    font-family: var(--sans);
    margin-top: 1.4em;
    margin-bottom: 0.5em;
    font-weight: 700;
    background: transparent;
}
.result-body h3 {
    border-bottom: 1px solid var(--border);
    padding-bottom: 0.4em;
    margin-top: 1.6em;
}
.result-body h3:first-child { margin-top: 0; }
.result-body h4, .result-body h5, .result-body h6 {
    color: var(--text);
    font-family: var(--sans);
    margin-top: 1.1em;
    margin-bottom: 0.4em;
    font-weight: 600;
}
.result-body p, .result-body li, .result-body td, .result-body th, .result-body span {
    color: var(--text);
    background: transparent;
}
.result-body code {
    background: var(--surface-3);
    color: var(--accent-dim);
    padding: 2px 7px;
    border-radius: 5px;
    font-family: var(--mono);
    font-size: 0.82em;
    border: 1px solid var(--border);
}
.result-body pre {
    background: #1e293b;
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    padding: 1.2rem;
    overflow-x: auto;
    margin: 0.8em 0;
}
.result-body pre code {
    background: transparent;
    border: none;
    padding: 0;
    color: #e2e8f0;
    font-size: 0.82rem;
}
.result-body strong { color: var(--text); font-weight: 600; }
.result-body ul, .result-body ol { padding-left: 1.5em; margin: 0.5em 0; }
.result-body li { margin-bottom: 0.35em; }
.result-body blockquote {
    border-left: 3px solid var(--accent);
    padding: 0.9em 1.2em;
    color: var(--text-2);
    background: rgba(13,148,136,0.04);
    border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
    margin: 0.8em 0;
    font-size: 0.86rem;
    line-height: 1.7;
}
.result-body hr {
    border: none;
    height: 1px;
    background: var(--border-2);
    margin: 1.5em 0;
}
.result-body a {
    color: var(--accent);
    text-decoration: underline;
}

/* ═══════════════ SIDEBAR CUSTOM ═══════════════ */
.sidebar-brand {
    text-align: center;
    padding: 0.8rem 0 1.4rem 0;
    border-bottom: 1px solid var(--border);
    margin-bottom: 1.4rem;
}
.sidebar-brand-icon {
    font-size: 2.2rem; margin-bottom: 0.4rem;
    filter: drop-shadow(0 0 10px rgba(13,148,136,0.2));
}
.sidebar-brand-name {
    font-family: var(--sans); font-size: 1rem;
    font-weight: 700; color: var(--text);
}
.sidebar-brand-sub {
    font-family: var(--mono); font-size: 0.56rem;
    color: var(--text-4); letter-spacing: 0.16em;
    text-transform: uppercase; margin-top: 4px;
}
.sidebar-label {
    font-family: var(--mono); font-size: 0.58rem;
    letter-spacing: 0.16em; text-transform: uppercase;
    color: var(--text-4); margin-bottom: 0.7rem; margin-top: 0.6rem;
    display: flex; align-items: center; gap: 7px;
}
.sidebar-label-icon { color: var(--accent); font-size: 0.68rem; }
.sidebar-stats {
    display: flex; justify-content: center; gap: 24px;
    margin: 0.8rem 0 1rem 0; padding: 14px 10px;
    background: var(--surface); border-radius: var(--radius-sm);
    border: 1px solid var(--border);
}
.stat-value {
    font-family: var(--mono); font-size: 1.2rem;
    font-weight: 700; color: var(--accent); line-height: 1.3; text-align: center;
}
.stat-label {
    font-family: var(--mono); font-size: 0.52rem;
    color: var(--text-4); letter-spacing: 0.12em;
    text-transform: uppercase; margin-top: 2px; text-align: center;
}
.tip-item {
    display: flex; align-items: flex-start; gap: 10px;
    font-size: 0.74rem; color: var(--text-3);
    margin-bottom: 0.35rem; font-family: var(--sans);
    line-height: 1.55; padding: 7px 10px;
    border-radius: 8px; transition: all 0.2s;
}
.tip-item:hover { background: rgba(13,148,136,0.04); color: var(--text-2); }
.tip-arrow { color: var(--accent); flex-shrink: 0; font-size: 0.82rem; }
.sidebar-footer {
    font-family: var(--mono); font-size: 0.56rem;
    color: var(--text-4); padding-top: 1.2rem;
    border-top: 1px solid var(--border);
    letter-spacing: 0.08em; line-height: 2; text-align: center;
}

/* ═══════════════ PROCESSING ANIMATION ═══════════════ */
.processing-container {
    padding: 2.5rem 1.5rem; text-align: center; animation: fadeIn 0.4s ease;
}
.processing-orb {
    width: 60px; height: 60px; margin: 0 auto 1.5rem auto;
    border-radius: 50%;
    background: linear-gradient(135deg, var(--accent), var(--green));
    box-shadow: 0 0 30px var(--accent-glow);
    animation: pulse-dot 1.8s ease-in-out infinite;
}
.processing-title {
    font-family: var(--mono); font-size: 0.82rem; font-weight: 600;
    color: var(--text); letter-spacing: 0.08em;
    margin-bottom: 0.6rem; text-transform: uppercase;
}
.processing-step {
    font-family: var(--mono); font-size: 0.7rem;
    color: var(--text-3); letter-spacing: 0.06em; margin-bottom: 0.3rem;
}
.processing-bar {
    width: 200px; height: 3px; margin: 1rem auto 0 auto;
    border-radius: 2px; background: var(--surface-3); overflow: hidden;
}
.processing-bar-inner {
    height: 100%; width: 40%; border-radius: 2px;
    background: linear-gradient(90deg, var(--accent), var(--green), var(--accent));
    background-size: 200% 100%;
    animation: shimmer 1.5s linear infinite;
}

/* ═══════════════ COPY BUTTON ═══════════════ */
.copy-btn {
    display: inline-flex; align-items: center; justify-content: center;
    gap: 6px; width: 100%; padding: 0.6rem 1rem;
    background: var(--surface-2); border: 1px solid var(--border-2);
    border-radius: var(--radius-sm); font-family: var(--mono);
    font-size: 0.72rem; font-weight: 500; letter-spacing: 0.08em;
    text-transform: uppercase; color: var(--text-2);
    cursor: pointer; transition: all 0.25s cubic-bezier(0.4,0,0.2,1);
    height: 40px;
}
.copy-btn:hover {
    border-color: var(--accent); color: var(--accent);
    background: rgba(13,148,136,0.06);
}
.copy-btn.copied {
    border-color: var(--green); color: var(--green);
    background: rgba(5,150,105,0.06);
}

hr { border-color: var(--border) !important; opacity: 0.5 !important; }
</style>
"""
