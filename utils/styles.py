GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

* { font-family: 'Inter', sans-serif; }

/* -- App background -- */
[data-testid="stAppViewContainer"] { background: #FAF7F4 !important; }
[data-testid="stHeader"] { background: transparent !important; }
section[data-testid="stSidebar"] {
    background: #F2EDE8 !important;
    border-right: 1px solid #E8E0D8;
}

/* -- Sidebar nav radio -- */
div[data-testid="stSidebar"] .stRadio label {
    color: #7A6A62 !important;
    font-size: 0.95rem;
    padding: 8px 12px;
    border-radius: 8px;
    transition: all 0.2s;
}
div[data-testid="stSidebar"] .stRadio label:hover { background: #E8E0D8; color: #2D2420 !important; }

/* -- Metric card -- */
.metric-card {
    background: #FFFFFF;
    border-radius: 16px;
    padding: 1.4rem 1.2rem;
    border: 1px solid #E8E0D8;
    text-align: center;
    transition: transform 0.2s, box-shadow 0.2s;
    margin-bottom: 8px;
}
.metric-card:hover { transform: translateY(-3px); box-shadow: 0 8px 24px rgba(139,111,94,0.12); }
.metric-card .icon { font-size: 1.8rem; margin-bottom: 6px; }
.metric-card .value { color: #8B6F5E; font-size: 2rem; font-weight: 700; margin: 0; line-height: 1; }
.metric-card .label { color: #7A6A62; font-size: 0.78rem; margin-top: 4px; text-transform: uppercase; letter-spacing: 0.05em; }

/* -- Skill badge -- */
.skill-badge {
    display: inline-flex; align-items: center; gap: 6px;
    background: #F2EDE8; color: #8B6F5E;
    border-radius: 20px; padding: 5px 14px; margin: 4px;
    font-size: 0.82rem; border: 1px solid #E8E0D8;
}
.skill-badge.beginner { border-color: #6B8F71; color: #6B8F71; }
.skill-badge.intermediate { border-color: #C49A3C; color: #C49A3C; }
.skill-badge.pro { border-color: #C4614A; color: #C4614A; }

/* -- Buttons -- */
.stButton > button {
    border-radius: 10px !important; font-weight: 600 !important;
    border: none !important; transition: all 0.2s !important;
}
.stButton > button:hover { transform: translateY(-1px); box-shadow: 0 4px 12px rgba(139,111,94,0.25) !important; }

/* -- Primary button -- */
.stButton > button[kind="primary"] {
    background: #8B6F5E !important;
    color: white !important;
}

/* -- Inputs -- */
.stTextInput input, .stSelectbox select, .stTextArea textarea {
    background: #FFFFFF !important; border: 1px solid #E8E0D8 !important;
    border-radius: 10px !important; color: #2D2420 !important;
}
.stTextInput input:focus { border-color: #8B6F5E !important; box-shadow: 0 0 0 2px rgba(139,111,94,0.15) !important; }

/* -- Tabs -- */
.stTabs [data-baseweb="tab-list"] { background: #F2EDE8; border-radius: 12px; padding: 4px; gap: 4px; }
.stTabs [data-baseweb="tab"] { border-radius: 8px !important; color: #7A6A62 !important; font-weight: 500; }
.stTabs [aria-selected="true"] { background: #8B6F5E !important; color: white !important; }

/* -- Cards / containers -- */
.page-card {
    background: #FFFFFF; border-radius: 16px;
    padding: 1.5rem; border: 1px solid #E8E0D8; margin-bottom: 1rem;
}

/* -- Activity item -- */
.activity-item {
    display: flex; align-items: center; gap: 14px;
    padding: 12px 16px; border-radius: 12px;
    background: #FFFFFF; border: 1px solid #E8E0D8;
    margin-bottom: 8px; transition: background 0.2s;
}
.activity-item:hover { background: #F2EDE8; }
.activity-icon { font-size: 1.5rem; min-width: 36px; text-align: center; }
.activity-desc { color: #2D2420; font-size: 0.9rem; }
.activity-time { color: #7A6A62; font-size: 0.75rem; margin-top: 2px; }

/* -- Quiz question card -- */
.quiz-card {
    background: #FFFFFF; border-radius: 14px;
    padding: 1.2rem 1.5rem; border: 1px solid #E8E0D8; margin-bottom: 1rem;
}
.quiz-card.correct { border-color: #6B8F71; background: rgba(107,143,113,0.05); }
.quiz-card.wrong   { border-color: #C4614A; background: rgba(196,97,74,0.05); }

/* -- Score ring -- */
.score-display {
    text-align: center; padding: 2rem;
    background: #FFFFFF;
    border-radius: 20px; border: 1px solid #E8E0D8;
}
.score-display .score-num { font-size: 4rem; font-weight: 700; color: #8B6F5E; line-height: 1; }
.score-display .score-label { color: #7A6A62; font-size: 0.9rem; margin-top: 8px; }

/* -- Section header -- */
.section-header {
    display: flex; align-items: center; gap: 10px;
    margin-bottom: 1rem; padding-bottom: 0.5rem;
    border-bottom: 1px solid #E8E0D8;
}
.section-header h3 { color: #2D2420; margin: 0; font-size: 1.1rem; font-weight: 600; }

/* -- Expander -- */
.streamlit-expanderHeader { background: #F2EDE8 !important; border-radius: 10px !important; }

/* -- Dataframe -- */
.stDataFrame { border-radius: 12px; overflow: hidden; }

/* -- Progress bar -- */
.stProgress > div > div { background: linear-gradient(90deg, #8B6F5E, #C4A882) !important; border-radius: 4px; }

/* -- Alerts -- */
.stSuccess { background: rgba(107,143,113,0.1) !important; border: 1px solid #6B8F71 !important; border-radius: 10px !important; }
.stError   { background: rgba(196,97,74,0.1)  !important; border: 1px solid #C4614A !important; border-radius: 10px !important; }
.stWarning { background: rgba(196,154,60,0.1) !important; border: 1px solid #C49A3C !important; border-radius: 10px !important; }
.stInfo    { background: rgba(196,168,130,0.1) !important; border: 1px solid #C4A882 !important; border-radius: 10px !important; }
</style>
"""


def inject_css():
    import streamlit as st
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
