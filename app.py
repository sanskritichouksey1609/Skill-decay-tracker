"""
SkillTrack AI — Streamlit entry point
Run: streamlit run app.py
"""
import streamlit as st
from utils.session import init_session, get_user_data
from utils.styles import inject_css
from utils.scheduler import start_scheduler

st.set_page_config(
    page_title="SkillTrack AI",
    page_icon="S",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_css()
init_session()
start_scheduler()

user = get_user_data()

# -- Sidebar ------------------------------------------------------------------
with st.sidebar:
    st.markdown(
        '<div style="padding:1rem 0 0.5rem;text-align:center;">'
        '<div style="color:#8B6F5E;font-weight:700;font-size:1.3rem;">SkillTrack AI</div>'
        '</div>',
        unsafe_allow_html=True,
    )

    uname    = user.get("username", "Guest")
    initials = uname[:2].upper()
    st.markdown(
        f'<div style="display:flex;align-items:center;gap:10px;background:#F2EDE8;'
        f'border-radius:12px;padding:10px 14px;margin-bottom:12px;">'
        f'<div style="width:32px;height:32px;border-radius:50%;'
        f'background:linear-gradient(135deg,#8B6F5E,#C4A882);'
        f'display:flex;align-items:center;justify-content:center;'
        f'font-size:0.8rem;font-weight:700;color:white;">{initials}</div>'
        f'<div style="color:#2D2420;font-size:0.9rem;font-weight:500;">{uname}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div style="color:#7A6A62;font-size:0.72rem;text-transform:uppercase;'
        'letter-spacing:0.08em;padding:0 4px;margin-bottom:6px;">Navigation</div>',
        unsafe_allow_html=True,
    )

    NAV = {
        "Home":      "Home",
        "Skills":    "Skills",
        "Quiz":      "Quiz",
        "Notes":     "Notes",
        "Analytics": "Analytics",
        "Profile":   "Profile",
    }
    page = st.radio("nav", list(NAV.keys()), label_visibility="collapsed")

    skill_count = len(user.get("skills", []))
    quiz_count  = len(user.get("quiz_history", []))
    st.markdown(
        f'<div style="margin-top:1rem;padding-top:1rem;border-top:1px solid #E8E0D8;'
        f'display:flex;gap:16px;justify-content:center;">'
        f'<div style="text-align:center;"><div style="color:#8B6F5E;font-weight:700;">{skill_count}</div>'
        f'<div style="color:#7A6A62;font-size:0.72rem;">Skills</div></div>'
        f'<div style="text-align:center;"><div style="color:#8B6F5E;font-weight:700;">{quiz_count}</div>'
        f'<div style="color:#7A6A62;font-size:0.72rem;">Quizzes</div></div>'
        f'</div>',
        unsafe_allow_html=True,
    )

# -- Routing ------------------------------------------------------------------
route = NAV[page]

if route == "Home":
    from views import home;            home.show()
elif route == "Skills":
    from views import skill_selection; skill_selection.show()
elif route == "Quiz":
    from views import quiz;            quiz.show()
elif route == "Notes":
    from views import notes;           notes.show()
elif route == "Analytics":
    from views import analytics;       analytics.show()
elif route == "Profile":
    from views import profile;         profile.show()
