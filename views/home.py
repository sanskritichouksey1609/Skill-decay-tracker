import streamlit as st
from utils.session import get_user_data
from components.metric_cards import metric_row
from components.recent_activity import activity_feed


def show():
    user         = get_user_data()
    username     = user.get("username", "Guest")
    skills       = user.get("skills", [])
    quiz_history = user.get("quiz_history", [])
    notes        = user.get("notes", [])
    avg_score    = round(sum(q["score"] for q in quiz_history) / len(quiz_history), 1) if quiz_history else 0

    st.markdown(f"""
        <div style="padding:1.5rem 0 0.5rem;">
            <h1 style="color:#2D2420;font-size:1.9rem;font-weight:700;margin:0;">
                Welcome back, <span style="color:#8B6F5E;">{username}</span>
            </h1>
            <p style="color:#7A6A62;margin-top:4px;">Here's your learning snapshot</p>
        </div>
    """, unsafe_allow_html=True)

    metric_row([
        {"label": "Skills Tracked", "value": len(skills),       "icon": ""},
        {"label": "Quizzes Taken",  "value": len(quiz_history), "icon": ""},
        {"label": "Avg Score",      "value": f"{avg_score}%",   "icon": ""},
        {"label": "Study Notes",    "value": len(notes),        "icon": ""},
    ])

    st.markdown("<br>", unsafe_allow_html=True)
    col_left, col_right = st.columns([3, 2])

    with col_left:
        st.markdown('<div class="section-header"><h3>Recent Activity</h3></div>', unsafe_allow_html=True)
        activities = []
        for q in sorted(quiz_history, key=lambda x: str(x.get("timestamp", "")), reverse=True)[:5]:
            activities.append({"type": "quiz", "description": f"Completed <b>{q['skill']}</b> quiz — scored <b>{q['score']}%</b>", "timestamp": q.get("timestamp")})
        for n in sorted(notes, key=lambda x: str(x.get("timestamp", "")), reverse=True)[:5]:
            activities.append({"type": "note", "description": f"Generated notes on <b>{n['topic']}</b> ({n['skill']})", "timestamp": n.get("timestamp")})
        activity_feed(activities)

    with col_right:
        st.markdown('<div class="section-header"><h3>Your Skills</h3></div>', unsafe_allow_html=True)
        if not skills:
            st.markdown('<div class="page-card" style="text-align:center;color:#7A6A62;padding:1.5rem;">No skills yet<br><small>Go to Skills page to add some</small></div>', unsafe_allow_html=True)
        else:
            level_color = {"Beginner": "#6B8F71", "Intermediate": "#C49A3C", "Pro": "#C4614A"}
            badges = "".join(f'<span class="skill-badge {s["level"].lower()}"><span style="color:{level_color.get(s["level"],"#8B6F5E")}">●</span> {s["name"]}</span>' for s in skills)
            st.markdown(f'<div class="page-card">{badges}</div>', unsafe_allow_html=True)

        if quiz_history:
            last = quiz_history[-1]
            tip_color = "#6B8F71" if last["score"] >= 70 else "#C49A3C"
            st.markdown(f'<div class="page-card" style="border-color:{tip_color};margin-top:8px;"><div style="color:{tip_color};font-size:0.8rem;font-weight:600;">LAST QUIZ</div><div style="color:#2D2420;margin-top:4px;">{last["skill"]} — {last["score"]}%</div></div>', unsafe_allow_html=True)
