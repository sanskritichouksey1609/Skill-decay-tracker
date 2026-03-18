import streamlit as st
from utils.session import get_user_data, save_field


def show():
    st.markdown("""
        <div style="padding:1rem 0 0.5rem;">
            <h1 style="color:#2D2420;font-size:1.9rem;font-weight:700;margin:0;">Profile &amp; Settings</h1>
            <p style="color:#7A6A62;margin-top:4px;">Manage your preferences</p>
        </div>
    """, unsafe_allow_html=True)

    user  = get_user_data()
    uname = user.get("username", "Guest")

    col_info, col_settings = st.columns([1, 2])

    with col_info:
        initials  = uname[:2].upper()
        avg_score = round(sum(q["score"] for q in user.get("quiz_history", [])) / len(user["quiz_history"]), 1) if user.get("quiz_history") else 0
        st.markdown(f"""
            <div class="page-card" style="text-align:center;padding:2rem;">
                <div style="width:72px;height:72px;border-radius:50%;background:linear-gradient(135deg,#8B6F5E,#C4A882);
                    display:flex;align-items:center;justify-content:center;font-size:1.6rem;font-weight:700;color:white;margin:0 auto 12px;">
                    {initials}</div>
                <div style="color:#2D2420;font-size:1.2rem;font-weight:600;">{uname}</div>
                <div style="color:#7A6A62;font-size:0.85rem;margin-top:2px;">SkillTrack AI User</div>
                <div style="display:flex;justify-content:center;gap:20px;margin-top:16px;">
                    <div style="text-align:center;"><div style="color:#8B6F5E;font-weight:700;font-size:1.2rem;">{len(user.get("skills",[]))}</div><div style="color:#7A6A62;font-size:0.75rem;">Skills</div></div>
                    <div style="text-align:center;"><div style="color:#8B6F5E;font-weight:700;font-size:1.2rem;">{len(user.get("quiz_history",[]))}</div><div style="color:#7A6A62;font-size:0.75rem;">Quizzes</div></div>
                    <div style="text-align:center;"><div style="color:#8B6F5E;font-weight:700;font-size:1.2rem;">{avg_score}%</div><div style="color:#7A6A62;font-size:0.75rem;">Avg Score</div></div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    with col_settings:
        st.markdown('<div class="page-card">', unsafe_allow_html=True)
        st.markdown("#### Practice Reminders")
        reminder_days = st.slider("Every N days", min_value=1, max_value=14,
                                  value=user.get("reminder_days", 3), label_visibility="collapsed")
        st.markdown(f'<div style="color:#8B6F5E;font-size:0.9rem;margin:8px 0;">Reminder every <b>{reminder_days}</b> day{"s" if reminder_days > 1 else ""}</div>', unsafe_allow_html=True)
        if st.button("Save Reminder", use_container_width=True, type="primary"):
            save_field("reminder_days", reminder_days)
            st.success("Saved.")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="page-card" style="border-color:#C4614A;">', unsafe_allow_html=True)
        st.markdown("#### Reset All Data")
        st.markdown('<div style="color:#7A6A62;font-size:0.85rem;margin-bottom:12px;">Clear all skills, quizzes and notes.</div>', unsafe_allow_html=True)
        if st.button("Reset Data", use_container_width=True):
            save_field("skills", [])
            save_field("quiz_history", [])
            save_field("notes", [])
            st.session_state.quiz_state = None
            st.success("All data cleared.")
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
