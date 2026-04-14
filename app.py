"""
NEXUS · Multi-Agent Intelligence Platform
Enterprise-grade Streamlit frontend with premium dark UI, live agent pipeline,
report history, multi-format export, and metrics dashboard.
"""

import time
import uuid
import datetime

# ── Load .env BEFORE any crewai/agent imports ────────────────────────────────
from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from crewai import Task, Crew

from agents.researcher import researcher
from agents.analyst import analyst
from agents.writer import writer
from agents.reviewer import reviewer
from config.settings import settings
from utils.helpers import (
    export_markdown, export_json, export_txt,
    get_report_metrics, format_elapsed, sanitize_filename, truncate
)

# ── Page Config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="NEXUS · Intelligence Platform",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Premium CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;0,600;1,400&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">

<style>
/* ── Foundations ── */
:root {
  --bg-base:      #07080d;
  --bg-surface:   #0d0f1a;
  --bg-elevated:  #131629;
  --bg-hover:     #1a1e35;
  --border:       rgba(99,120,210,0.18);
  --border-glow:  rgba(99,120,210,0.45);

  --accent-blue:  #5b8af0;
  --accent-gold:  #f0b429;
  --accent-teal:  #3dd6c0;
  --accent-rose:  #f05b7a;
  --accent-violet:#9b6bf4;

  --text-primary: #e8eaf6;
  --text-secondary:#98a0c8;
  --text-muted:   #515878;

  --radius-sm: 8px;
  --radius-md: 14px;
  --radius-lg: 20px;

  --font-display: 'Syne', sans-serif;
  --font-body:    'DM Sans', sans-serif;
  --font-mono:    'JetBrains Mono', monospace;

  --glow-blue: 0 0 30px rgba(91,138,240,0.25), 0 0 60px rgba(91,138,240,0.10);
  --glow-gold: 0 0 20px rgba(240,180,41,0.30);
  --shadow-card: 0 4px 24px rgba(0,0,0,0.5), 0 1px 0 rgba(255,255,255,0.04) inset;
}

/* ── Global Reset ── */
html, body, [class*="css"] {
  font-family: var(--font-body) !important;
  background-color: var(--bg-base) !important;
  color: var(--text-primary) !important;
}

/* Remove default Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 2rem 3rem !important; max-width: 1400px !important; }
.stApp { background: var(--bg-base); }
.stApp > header { display: none; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg-base); }
::-webkit-scrollbar-thumb { background: rgba(91,138,240,0.3); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--accent-blue); }

/* ── Animated grid background ── */
.stApp::before {
  content: '';
  position: fixed; inset: 0; z-index: 0; pointer-events: none;
  background-image:
    linear-gradient(rgba(91,138,240,0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(91,138,240,0.03) 1px, transparent 1px);
  background-size: 60px 60px;
  mask-image: radial-gradient(ellipse at 50% 0%, black 40%, transparent 80%);
}

/* ── Topbar ── */
.nexus-topbar {
  position: relative;
  padding: 2.5rem 0 2rem;
  border-bottom: 1px solid var(--border);
  margin-bottom: 2rem;
  overflow: hidden;
}
.nexus-topbar::before {
  content: '';
  position: absolute; top: 0; left: -10%; right: -10%; height: 1px;
  background: linear-gradient(90deg, transparent, var(--accent-blue), var(--accent-gold), var(--accent-blue), transparent);
  opacity: 0.6;
  animation: shimmer 4s ease-in-out infinite;
}
@keyframes shimmer { 0%,100%{opacity:0.3} 50%{opacity:0.8} }

.nexus-brand {
  display: flex; align-items: center; gap: 14px;
}
.nexus-logo {
  width: 44px; height: 44px;
  background: linear-gradient(135deg, var(--accent-blue), var(--accent-violet));
  clip-path: polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%);
  display: flex; align-items: center; justify-content: center;
  font-size: 1.2rem;
  box-shadow: var(--glow-blue);
  animation: logoPulse 3s ease-in-out infinite;
}
@keyframes logoPulse { 0%,100%{box-shadow: var(--glow-blue)} 50%{box-shadow: 0 0 50px rgba(91,138,240,0.5), 0 0 100px rgba(91,138,240,0.2)} }

.nexus-wordmark {
  font-family: var(--font-display) !important;
  font-size: 1.75rem; font-weight: 800; letter-spacing: -0.02em;
  background: linear-gradient(135deg, var(--text-primary), var(--accent-blue));
  -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
  line-height: 1;
}
.nexus-sub {
  font-size: 0.72rem; letter-spacing: 0.14em; text-transform: uppercase;
  color: var(--text-muted); font-weight: 500; margin-top: 2px;
}
.nexus-badge {
  margin-left: auto;
  padding: 4px 12px;
  background: rgba(91,138,240,0.12);
  border: 1px solid rgba(91,138,240,0.3);
  border-radius: 100px;
  font-size: 0.7rem; font-family: var(--font-mono) !important;
  color: var(--accent-blue); letter-spacing: 0.08em;
}

/* ── Cards ── */
.card {
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 1.5rem 1.75rem;
  box-shadow: var(--shadow-card);
  transition: border-color 0.2s, box-shadow 0.2s;
}
.card:hover { border-color: var(--border-glow); box-shadow: var(--shadow-card), var(--glow-blue); }

.card-sm {
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: 1rem 1.25rem;
  box-shadow: var(--shadow-card);
}

/* ── Agent Pipeline ── */
.pipeline-header {
  font-family: var(--font-display) !important;
  font-size: 0.7rem; font-weight: 700; letter-spacing: 0.15em;
  text-transform: uppercase; color: var(--text-muted);
  margin-bottom: 1rem;
}

.pipeline-track {
  display: flex; align-items: center; gap: 0; 
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 1rem 1.5rem;
  overflow: hidden;
}
.agent-node {
  flex: 1; display: flex; flex-direction: column; align-items: center;
  gap: 0.5rem; position: relative; padding: 0.5rem;
  transition: transform 0.2s;
}
.agent-node:hover { transform: translateY(-2px); }

.agent-icon {
  width: 48px; height: 48px; border-radius: 14px;
  display: flex; align-items: center; justify-content: center;
  font-size: 1.4rem; font-weight: 700;
  border: 1px solid;
  transition: box-shadow 0.3s, border-color 0.3s;
  position: relative;
}

.agent-icon.idle     { background: rgba(255,255,255,0.04); border-color: rgba(255,255,255,0.08); color: var(--text-muted); }
.agent-icon.running  { background: rgba(91,138,240,0.15); border-color: var(--accent-blue); box-shadow: 0 0 20px rgba(91,138,240,0.4); animation: agentPulse 1.2s ease-in-out infinite; }
.agent-icon.done     { background: rgba(61,214,192,0.12); border-color: var(--accent-teal); color: var(--accent-teal); }
.agent-icon.error    { background: rgba(240,91,122,0.12); border-color: var(--accent-rose); color: var(--accent-rose); }

@keyframes agentPulse { 0%,100%{box-shadow: 0 0 20px rgba(91,138,240,0.4)} 50%{box-shadow: 0 0 35px rgba(91,138,240,0.7)} }

.agent-label {
  font-size: 0.65rem; text-align: center; line-height: 1.3;
  font-weight: 600; letter-spacing: 0.04em;
  color: var(--text-secondary);
}
.agent-label.running { color: var(--accent-blue); }
.agent-label.done    { color: var(--accent-teal); }

.pipeline-arrow {
  color: var(--text-muted); font-size: 1rem; padding: 0 0.25rem;
  opacity: 0.4;
}
.pipeline-arrow.active { color: var(--accent-blue); opacity: 1; animation: arrowFlow 0.8s ease-in-out infinite alternate; }
@keyframes arrowFlow { from{opacity:0.5} to{opacity:1} }

/* ── Status dot ── */
.status-dot {
  position: absolute; top: -3px; right: -3px;
  width: 10px; height: 10px; border-radius: 50%;
  border: 2px solid var(--bg-surface);
}
.status-dot.running { background: var(--accent-blue); animation: dotPulse 1s ease-in-out infinite; }
.status-dot.done    { background: var(--accent-teal); }
.status-dot.error   { background: var(--accent-rose); }
.status-dot.idle    { background: var(--text-muted); }
@keyframes dotPulse { 0%,100%{transform:scale(1);opacity:1} 50%{transform:scale(1.4);opacity:0.7} }

/* ── Input ── */
.stTextInput > div > div > input {
  background: var(--bg-elevated) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius-md) !important;
  color: var(--text-primary) !important;
  font-family: var(--font-body) !important;
  font-size: 1rem !important;
  padding: 0.85rem 1.1rem !important;
  transition: border-color 0.2s, box-shadow 0.2s !important;
}
.stTextInput > div > div > input:focus {
  border-color: var(--accent-blue) !important;
  box-shadow: 0 0 0 3px rgba(91,138,240,0.15) !important;
  outline: none !important;
}
.stTextInput > div > div > input::placeholder { color: var(--text-muted) !important; }
.stTextInput label { font-size: 0.75rem !important; font-weight: 600 !important; letter-spacing: 0.1em !important; text-transform: uppercase !important; color: var(--text-secondary) !important; }

/* ── Buttons ── */
.stButton > button {
  background: linear-gradient(135deg, var(--accent-blue), var(--accent-violet)) !important;
  border: none !important;
  border-radius: var(--radius-md) !important;
  color: white !important;
  font-family: var(--font-display) !important;
  font-weight: 700 !important;
  font-size: 0.85rem !important;
  letter-spacing: 0.06em !important;
  text-transform: uppercase !important;
  padding: 0.75rem 1.5rem !important;
  transition: all 0.2s !important;
  box-shadow: 0 4px 20px rgba(91,138,240,0.3) !important;
}
.stButton > button:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 8px 30px rgba(91,138,240,0.5) !important;
  filter: brightness(1.1) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* Secondary button variant */
div[data-testid="stHorizontalBlock"] > div:nth-child(2) .stButton > button {
  background: var(--bg-elevated) !important;
  border: 1px solid var(--border) !important;
  color: var(--text-secondary) !important;
  box-shadow: none !important;
}
div[data-testid="stHorizontalBlock"] > div:nth-child(2) .stButton > button:hover {
  border-color: var(--border-glow) !important;
  color: var(--text-primary) !important;
  box-shadow: none !important;
}

/* Download buttons */
.stDownloadButton > button {
  background: var(--bg-elevated) !important;
  border: 1px solid var(--border) !important;
  color: var(--text-secondary) !important;
  font-size: 0.78rem !important;
  padding: 0.5rem 1rem !important;
  border-radius: var(--radius-sm) !important;
  text-transform: none !important;
  letter-spacing: 0.02em !important;
  box-shadow: none !important;
}
.stDownloadButton > button:hover {
  border-color: var(--accent-gold) !important;
  color: var(--accent-gold) !important;
  transform: none !important;
  box-shadow: var(--glow-gold) !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
  background: var(--bg-surface) !important;
  border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] * { font-family: var(--font-body) !important; }

.sidebar-section {
  background: var(--bg-elevated);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: 1rem 1.1rem;
  margin-bottom: 1rem;
}
.sidebar-title {
  font-family: var(--font-display) !important;
  font-size: 0.68rem; font-weight: 700; letter-spacing: 0.15em;
  text-transform: uppercase; color: var(--text-muted); margin-bottom: 0.75rem;
}

/* Toggles */
.stToggle > label { color: var(--text-secondary) !important; font-size: 0.85rem !important; }

/* Selectbox */
.stSelectbox > div > div {
  background: var(--bg-elevated) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius-sm) !important;
  color: var(--text-primary) !important;
}

/* Slider */
.stSlider > div > div > div > div { background: var(--accent-blue) !important; }

/* ── Metrics row ── */
.metric-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 0.75rem; margin-bottom: 1.5rem; }
.metric-card {
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: 1rem 1.1rem;
  text-align: center;
}
.metric-value {
  font-family: var(--font-display) !important;
  font-size: 1.7rem; font-weight: 800; line-height: 1;
  background: linear-gradient(135deg, var(--accent-blue), var(--accent-gold));
  -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
  margin-bottom: 0.25rem;
}
.metric-label {
  font-size: 0.68rem; text-transform: uppercase; letter-spacing: 0.12em;
  color: var(--text-muted); font-weight: 600;
}

/* ── Report Output ── */
.report-container {
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 2rem 2.25rem;
  line-height: 1.8;
  box-shadow: var(--shadow-card);
  position: relative;
  overflow: hidden;
}
.report-container::before {
  content: '';
  position: absolute; top: 0; left: 0; right: 0; height: 3px;
  background: linear-gradient(90deg, var(--accent-blue), var(--accent-violet), var(--accent-gold));
}
.report-container h1, .report-container h2, .report-container h3 {
  font-family: var(--font-display) !important;
  color: var(--text-primary) !important;
}
.report-container p { color: var(--text-secondary) !important; }
.report-container strong { color: var(--text-primary) !important; }
.report-container code {
  font-family: var(--font-mono) !important;
  background: var(--bg-elevated) !important;
  padding: 2px 6px !important;
  border-radius: 4px !important;
  font-size: 0.85em !important;
  color: var(--accent-teal) !important;
}

/* ── History items ── */
.history-item {
  background: var(--bg-elevated);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: 0.85rem 1rem;
  margin-bottom: 0.5rem;
  cursor: pointer;
  transition: border-color 0.2s, background 0.2s;
}
.history-item:hover { border-color: var(--border-glow); background: var(--bg-hover); }
.history-topic {
  font-size: 0.82rem; font-weight: 600; color: var(--text-primary);
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}
.history-meta {
  font-size: 0.68rem; color: var(--text-muted); margin-top: 3px;
  font-family: var(--font-mono) !important;
}

/* ── Agent output expanders ── */
.streamlit-expanderHeader {
  background: var(--bg-elevated) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius-md) !important;
  color: var(--text-primary) !important;
  font-family: var(--font-display) !important;
  font-weight: 600 !important;
}
.streamlit-expanderContent {
  background: var(--bg-surface) !important;
  border: 1px solid var(--border) !important;
  border-top: none !important;
  color: var(--text-secondary) !important;
  font-family: var(--font-body) !important;
}

/* ── Alerts ── */
.stAlert {
  background: var(--bg-elevated) !important;
  border-radius: var(--radius-md) !important;
  border: 1px solid var(--border) !important;
  color: var(--text-secondary) !important;
}

/* ── Divider ── */
hr { border-color: var(--border) !important; }

/* ── Section labels ── */
.section-label {
  font-family: var(--font-display) !important;
  font-size: 0.7rem; font-weight: 700; letter-spacing: 0.18em;
  text-transform: uppercase; color: var(--text-muted);
  margin-bottom: 0.75rem; display: flex; align-items: center; gap: 8px;
}
.section-label::after {
  content: ''; flex: 1; height: 1px; background: var(--border);
}

/* ── Success/info toast ── */
.stSuccess {
  background: rgba(61,214,192,0.08) !important;
  border: 1px solid rgba(61,214,192,0.25) !important;
  color: var(--accent-teal) !important;
  border-radius: var(--radius-md) !important;
}
.stWarning {
  background: rgba(240,180,41,0.08) !important;
  border: 1px solid rgba(240,180,41,0.2) !important;
  color: var(--accent-gold) !important;
  border-radius: var(--radius-md) !important;
}
.stError {
  background: rgba(240,91,122,0.08) !important;
  border: 1px solid rgba(240,91,122,0.2) !important;
  color: var(--accent-rose) !important;
  border-radius: var(--radius-md) !important;
}
.stSpinner > div { border-top-color: var(--accent-blue) !important; }

/* ── Chip tags ── */
.chip {
  display: inline-flex; align-items: center; gap: 4px;
  background: rgba(91,138,240,0.1);
  border: 1px solid rgba(91,138,240,0.2);
  border-radius: 100px;
  padding: 3px 10px;
  font-size: 0.7rem; font-weight: 600;
  color: var(--accent-blue); letter-spacing: 0.06em;
  margin-right: 6px; margin-bottom: 6px;
}

/* Progress bar */
.stProgress > div > div > div > div {
  background: linear-gradient(90deg, var(--accent-blue), var(--accent-violet)) !important;
}

/* ── Animation helpers ── */
@keyframes fadeIn { from{opacity:0;transform:translateY(12px)} to{opacity:1;transform:translateY(0)} }
.fade-in { animation: fadeIn 0.4s ease both; }
</style>
""", unsafe_allow_html=True)


# ── Session State Initialization ────────────────────────────────────────────
def init_session():
    defaults = {
        "history": [],           # list of report dicts
        "agent_states": {        # idle | running | done | error
            "researcher": "idle",
            "analyst": "idle",
            "writer": "idle",
            "reviewer": "idle",
        },
        "current_result": None,
        "current_topic": "",
        "current_agent_outputs": [],
        "is_running": False,
        "elapsed_time": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_session()


# ── Agent Pipeline Renderer ──────────────────────────────────────────────────
AGENTS_META = [
    {"key": "researcher", "label": "Research\nSpecialist", "icon": "🔭", "color": "#5b8af0"},
    {"key": "analyst",    "label": "Strategic\nAnalyst",    "icon": "📊", "color": "#9b6bf4"},
    {"key": "writer",     "label": "Principal\nWriter",     "icon": "✍️", "color": "#f0b429"},
    {"key": "reviewer",   "label": "Editorial\nDirector",  "icon": "⚖️", "color": "#3dd6c0"},
]

def render_pipeline():
    """Render pipeline using native Streamlit columns - avoids HTML leaking in st.empty()."""
    states = st.session_state.agent_states

    STATE_BORDER = {"idle": "#2a2e47", "running": "#5b8af0", "done": "#3dd6c0", "error": "#f05b7a"}
    STATE_TEXT   = {"idle": "#515878", "running": "#5b8af0", "done": "#3dd6c0", "error": "#f05b7a"}
    STATE_BG     = {"idle": "rgba(255,255,255,0.02)", "running": "rgba(91,138,240,0.12)",
                    "done": "rgba(61,214,192,0.08)",  "error":   "rgba(240,91,122,0.08)"}
    STATE_SYMBOL = {"idle": "—", "running": "●", "done": "✓", "error": "✗"}

    st.markdown(
        '<p style="font-size:0.7rem;font-weight:700;letter-spacing:0.15em;' +
        'text-transform:uppercase;color:#515878;margin:0 0 0.6rem 0">⬡ Agent Pipeline</p>',
        unsafe_allow_html=True,
    )

    cols = st.columns([3, 1, 3, 1, 3, 1, 3])
    agent_col_idx = [0, 2, 4, 6]
    arrow_col_idx = [1, 3, 5]

    for i, agent in enumerate(AGENTS_META):
        state   = states[agent["key"]]
        border  = STATE_BORDER[state]
        text    = STATE_TEXT[state]
        bg      = STATE_BG[state]
        symbol  = STATE_SYMBOL[state]
        glow    = "box-shadow:0 0 16px rgba(91,138,240,0.4);" if state == "running" else ""
        label   = agent["label"].replace("\n", "<br>")

        with cols[agent_col_idx[i]]:
            st.markdown(
                f'<div style="background:{bg};border:1px solid {border};border-radius:14px;' +
                f'padding:1rem 0.4rem 0.8rem;text-align:center;{glow}">' +
                f'  <div style="font-size:1.5rem;line-height:1">{agent["icon"]}</div>' +
                f'  <div style="font-size:0.63rem;font-weight:700;color:{text};' +
                f'      letter-spacing:0.04em;margin-top:0.4rem;line-height:1.4">{label}</div>' +
                f'  <div style="margin-top:0.35rem;font-size:0.68rem;color:{text};font-weight:800">' +
                f'    {symbol} {state.upper()}</div></div>',
                unsafe_allow_html=True,
            )

    for j, col_idx in enumerate(arrow_col_idx):
        left_state  = states[AGENTS_META[j]["key"]]
        active      = left_state in ("running", "done")
        arrow_color = "#5b8af0" if active else "#252840"
        with cols[col_idx]:
            st.markdown(
                f'<div style="text-align:center;padding-top:1.4rem;' +
                f'font-size:1.4rem;color:{arrow_color};line-height:1">›</div>',
                unsafe_allow_html=True,
            )


# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    # Logo in sidebar
    st.markdown("""
    <div style="display:flex;align-items:center;gap:10px;padding:0.5rem 0 1.5rem">
      <div style="width:32px;height:32px;background:linear-gradient(135deg,#5b8af0,#9b6bf4);
                  clip-path:polygon(50% 0%,100% 25%,100% 75%,50% 100%,0% 75%,0% 25%);
                  display:flex;align-items:center;justify-content:center;font-size:0.9rem">⬡</div>
      <span style="font-family:'Syne',sans-serif;font-weight:800;font-size:1.1rem;
                   background:linear-gradient(135deg,#e8eaf6,#5b8af0);
                   -webkit-background-clip:text;-webkit-text-fill-color:transparent">NEXUS</span>
    </div>
    """, unsafe_allow_html=True)

    # ── Configuration ──
    st.markdown('<div class="sidebar-title">⚙ Configuration</div>', unsafe_allow_html=True)
    
    with st.container():
        show_pipeline = st.toggle("Live Agent Pipeline", value=True)
        show_steps = st.toggle("Show Agent Outputs", value=True)
        use_memory = st.toggle("Enable Memory", value=True)
    
    st.markdown("---")

    # ── Model Settings ──
    st.markdown('<div class="sidebar-title">🧠 Model</div>', unsafe_allow_html=True)
    model_choice = st.selectbox(
        "LLM Model",
        ["gpt-4o-mini", "gpt-4o", "gpt-4-turbo"],
        label_visibility="collapsed"
    )
    temperature = st.slider("Temperature", 0.0, 1.0, 0.3, 0.05, help="Lower = more factual, Higher = more creative")
    
    st.markdown("---")

    # ── Topic Presets ──
    st.markdown('<div class="sidebar-title">💡 Quick Topics</div>', unsafe_allow_html=True)
    
    EXAMPLE_TOPICS = [
        "AI job market in 2025",
        "Quantum computing breakthroughs",
        "Climate tech investment trends",
        "Generative AI in healthcare",
        "Web3 & DeFi evolution",
        "Geopolitical impact on supply chains",
        "Future of remote work",
        "Cybersecurity landscape 2025",
    ]
    selected_example = None
    for topic in EXAMPLE_TOPICS:
        if st.button(f"› {topic}", key=f"preset_{topic}", use_container_width=True):
            selected_example = topic

    st.markdown("---")

    # ── History ──
    if st.session_state.history:
        st.markdown('<div class="sidebar-title">📂 Recent Reports</div>', unsafe_allow_html=True)
        for item in reversed(st.session_state.history[-8:]):
            ts = item.get("timestamp", "")
            words = item.get("metrics", {}).get("words", "—")
            st.markdown(f"""
            <div class="history-item">
              <div class="history-topic">{item['topic'][:40]}</div>
              <div class="history-meta">{ts} · {words} words</div>
            </div>
            """, unsafe_allow_html=True)

    # ── Footer ──
    st.markdown("---")
    st.markdown(f"""
    <div style="text-align:center;padding:0.5rem 0">
      <div style="font-family:'JetBrains Mono',monospace;font-size:0.65rem;color:#515878">
        NEXUS v{settings.app_version}
      </div>
      <div style="font-size:0.65rem;color:#515878;margin-top:2px">
        Multi-Agent Intelligence Platform
      </div>
    </div>
    """, unsafe_allow_html=True)


# ── Top Bar ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="nexus-topbar">
  <div class="nexus-brand">
    <div class="nexus-logo">⬡</div>
    <div>
      <div class="nexus-wordmark">NEXUS</div>
      <div class="nexus-sub">Multi-Agent Intelligence Platform</div>
    </div>
    <div class="nexus-badge">v2.0 · Enterprise</div>
  </div>
</div>
""", unsafe_allow_html=True)


# ── Main Input Area ───────────────────────────────────────────────────────────
st.markdown('<div class="section-label">Research Topic</div>', unsafe_allow_html=True)

# Pre-fill from sidebar presets
default_topic = st.session_state.get("prefill_topic", "")
if selected_example:
    default_topic = selected_example
    st.session_state["prefill_topic"] = selected_example

topic_col, btn_col, clr_col = st.columns([5, 1.2, 0.8])

with topic_col:
    user_input = st.text_input(
        "topic",
        value=default_topic,
        placeholder="e.g.  Impact of AI on the future of software engineering…",
        label_visibility="collapsed",
    )

with btn_col:
    generate_btn = st.button("⬡  Generate", use_container_width=True)

with clr_col:
    clear_btn = st.button("Clear", use_container_width=True)

if clear_btn:
    for key in ["current_result", "current_topic", "current_agent_outputs",
                "prefill_topic", "elapsed_time"]:
        st.session_state[key] = None if key != "current_agent_outputs" else []
    st.session_state.agent_states = {k: "idle" for k in st.session_state.agent_states}
    st.rerun()


# ── Pipeline Visualization ────────────────────────────────────────────────────
if show_pipeline:
    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
    pipeline_placeholder = st.empty()
    with pipeline_placeholder.container():
        render_pipeline()


# ── Core Task Runner ──────────────────────────────────────────────────────────
def run_pipeline(topic: str, memory: bool) -> dict | None:
    """Execute the 4-agent CrewAI pipeline and return results."""

    def set_state(agent_key: str, state: str):
        st.session_state.agent_states[agent_key] = state
        if show_pipeline:
            pipeline_placeholder.empty()
            with pipeline_placeholder.container():
                render_pipeline()

    agent_outputs = []
    start_time = time.time()

    try:
        # ── Define Tasks ─────────────────────────────────────────
        research_task = Task(
            description=(
                f"Conduct comprehensive research on: '{topic}'. "
                "Use web search to gather current facts, statistics, expert opinions, "
                "key players, recent developments, market data, and contextual background. "
                "Organize findings under clear subheadings. Cite sources where possible. "
                "Aim for depth and breadth — leave no critical dimension unexplored."
            ),
            agent=researcher,
            expected_output=(
                "A thorough research brief with multiple sections covering: "
                "current state, key data/statistics, major players/stakeholders, "
                "recent developments (last 12 months), challenges, and opportunities. "
                "Minimum 400 words."
            ),
        )

        analysis_task = Task(
            description=(
                "Using the research findings provided, perform a deep analytical assessment. "
                "Identify: (1) the top 5 key trends with supporting data, "
                "(2) a SWOT analysis framework, "
                "(3) quantitative metrics and their significance, "
                "(4) risk factors and mitigation strategies, "
                "(5) strategic implications and competitive dynamics. "
                "Use the calculator tool for any numerical analysis needed."
            ),
            agent=analyst,
            context=[research_task],
            expected_output=(
                "A structured analytical report with: executive insights, trend analysis, "
                "SWOT framework, risk matrix, and 5–7 evidence-backed strategic findings."
            ),
        )

        writing_task = Task(
            description=(
                "Using the analytical insights provided, write a comprehensive professional report. "
                "Structure: (1) Executive Summary (3–4 sentences capturing the essence), "
                "(2) Background & Context, (3) Key Findings & Analysis, "
                "(4) Strategic Implications, (5) Risks & Considerations, "
                "(6) Recommendations (at least 5 specific, actionable items), "
                "(7) Conclusion & Outlook. "
                "Use clear headers, concise paragraphs, and data callouts. "
                "Tone: authoritative, objective, strategic."
            ),
            agent=writer,
            context=[analysis_task],
            expected_output=(
                "A fully structured, publication-ready intelligence report with all 7 sections, "
                "clear headings, data references, and actionable recommendations. "
                "Minimum 600 words."
            ),
        )

        review_task = Task(
            description=(
                "Critically review and elevate the draft report to publication standard. "
                "Tasks: (1) Strengthen the executive summary to maximize impact, "
                "(2) Verify all claims have supporting logic, "
                "(3) Sharpen and make recommendations more specific and measurable, "
                "(4) Improve flow, clarity, and sentence variety, "
                "(5) Add a '⚡ Key Takeaways' section at the top with 5 bullet points, "
                "(6) Add a 'Future Outlook' subsection in the conclusion. "
                "Ensure the final document is error-free, coherent, and executive-ready."
            ),
            agent=reviewer,
            context=[writing_task],
            expected_output=(
                "The final polished intelligence report with: Key Takeaways section, "
                "all 7 body sections, verified recommendations, and Future Outlook. "
                "Professional tone throughout. Ready for C-suite delivery."
            ),
        )

        # ── Execute with live status updates ──────────────────────
        tasks = [research_task, analysis_task, writing_task, review_task]
        agent_keys = ["researcher", "analyst", "writer", "reviewer"]

        # Mark first agent as running
        set_state("researcher", "running")

        crew = Crew(
            agents=[researcher, analyst, writer, reviewer],
            tasks=tasks,
            verbose=settings.agent_verbose,
            memory=memory,
        )

        # Run the crew
        result = crew.kickoff()

        # Collect per-task outputs & update states sequentially
        for i, (task_out, key) in enumerate(zip(result.tasks_output, agent_keys)):
            set_state(key, "done")
            if i + 1 < len(agent_keys):
                set_state(agent_keys[i + 1], "running")
            agent_outputs.append({
                "name": AGENTS_META[i]["label"].replace("\n", " "),
                "icon": AGENTS_META[i]["icon"],
                "role": [researcher, analyst, writer, reviewer][i].role,
                "output": task_out.raw,
            })

        elapsed = time.time() - start_time
        metrics = get_report_metrics(result.raw)

        return {
            "topic": topic,
            "result": result.raw,
            "agent_outputs": agent_outputs,
            "elapsed": elapsed,
            "metrics": metrics,
            "timestamp": datetime.datetime.now().strftime("%b %d, %H:%M"),
            "id": str(uuid.uuid4())[:8],
        }

    except Exception as exc:
        # Mark active agent as error
        for key in agent_keys:
            if st.session_state.agent_states[key] == "running":
                set_state(key, "error")
                break
        st.error(f"**Pipeline Error:** {exc}")
        return None


# ── Generate Button Handler ───────────────────────────────────────────────────
if generate_btn:
    if not user_input or not user_input.strip():
        st.warning("Please enter a research topic before generating.")
    else:
        # Reset states
        st.session_state.agent_states = {k: "idle" for k in st.session_state.agent_states}
        st.session_state.current_result = None
        st.session_state.is_running = True

        with st.spinner(""):
            report = run_pipeline(user_input.strip(), use_memory)

        if report:
            st.session_state.current_result = report["result"]
            st.session_state.current_topic = report["topic"]
            st.session_state.current_agent_outputs = report["agent_outputs"]
            st.session_state.elapsed_time = report["elapsed"]

            # Save to history
            st.session_state.history.append({
                "topic": report["topic"],
                "result": report["result"],
                "agent_outputs": report["agent_outputs"],
                "metrics": report["metrics"],
                "timestamp": report["timestamp"],
                "id": report["id"],
            })
            if len(st.session_state.history) > settings.max_history_items:
                st.session_state.history.pop(0)

        st.session_state.is_running = False
        st.rerun()


# ── Results Display ────────────────────────────────────────────────────────────
if st.session_state.current_result:
    result_text = st.session_state.current_result
    topic = st.session_state.current_topic
    agent_outputs = st.session_state.current_agent_outputs
    metrics = get_report_metrics(result_text)
    elapsed = st.session_state.elapsed_time

    st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)
    st.success(f"✓ Report ready · Generated in {format_elapsed(elapsed or 0)}")

    # ── Metrics Row ──
    st.markdown(f"""
    <div class="metric-grid fade-in">
      <div class="metric-card">
        <div class="metric-value">{metrics['words']:,}</div>
        <div class="metric-label">Words</div>
      </div>
      <div class="metric-card">
        <div class="metric-value">{metrics['reading_time']}</div>
        <div class="metric-label">Min. Read</div>
      </div>
      <div class="metric-card">
        <div class="metric-value">{metrics['paragraphs']}</div>
        <div class="metric-label">Sections</div>
      </div>
      <div class="metric-card">
        <div class="metric-value">{format_elapsed(elapsed or 0)}</div>
        <div class="metric-label">Gen. Time</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Export Controls ──
    st.markdown('<div class="section-label">Export Report</div>', unsafe_allow_html=True)
    safe_name = sanitize_filename(topic)
    exp1, exp2, exp3 = st.columns(3)
    with exp1:
        st.download_button(
            "⬇ Markdown (.md)",
            export_markdown(topic, result_text, agent_outputs),
            file_name=f"nexus_{safe_name}.md",
            mime="text/markdown",
            use_container_width=True,
        )
    with exp2:
        st.download_button(
            "⬇ JSON (.json)",
            export_json(topic, result_text, agent_outputs),
            file_name=f"nexus_{safe_name}.json",
            mime="application/json",
            use_container_width=True,
        )
    with exp3:
        st.download_button(
            "⬇ Plain Text (.txt)",
            export_txt(topic, result_text),
            file_name=f"nexus_{safe_name}.txt",
            mime="text/plain",
            use_container_width=True,
        )

    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

    # ── Final Report ──
    st.markdown('<div class="section-label">Intelligence Report</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="report-container fade-in">', unsafe_allow_html=True)
    st.markdown(result_text)
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Agent Pipeline Breakdown ──
    if show_steps and agent_outputs:
        st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
        st.markdown('<div class="section-label">Agent Pipeline Breakdown</div>', unsafe_allow_html=True)
        for agent in agent_outputs:
            with st.expander(f"{agent['icon']}  {agent['name']} · {agent['role']}"):
                st.markdown(agent["output"])

# ── Empty State ───────────────────────────────────────────────────────────────
elif not st.session_state.is_running:
    st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div class="card fade-in" style="text-align:center;padding:3rem 2rem">
      <div style="font-size:3rem;margin-bottom:1rem;opacity:0.4">⬡</div>
      <div style="font-family:'Syne',sans-serif;font-size:1.2rem;font-weight:700;
                  color:#515878;margin-bottom:0.5rem">Ready for Research</div>
      <div style="color:#3a3f5c;font-size:0.85rem;max-width:420px;margin:0 auto;line-height:1.6">
        Enter a topic above and click Generate to deploy the 4-agent intelligence pipeline —
        Research → Analysis → Writing → Editorial Review.
      </div>
      <div style="margin-top:1.5rem;display:flex;gap:8px;justify-content:center;flex-wrap:wrap">
        <span class="chip">🔭 Senior Researcher</span>
        <span class="chip">📊 Strategic Analyst</span>
        <span class="chip">✍️ Principal Writer</span>
        <span class="chip">⚖️ Editorial Director</span>
      </div>
    </div>
    """, unsafe_allow_html=True)
