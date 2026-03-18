import streamlit as st
from utils.session import get_user_data, save_field
from utils.config import AVAILABLE_SKILLS, PROFICIENCY_LEVELS

LEVEL_COLOR = {"Beginner": "#6B8F71", "Intermediate": "#C49A3C", "Pro": "#C4614A"}
LEVEL_LABEL = {"Beginner": "Beginner", "Intermediate": "Intermediate", "Pro": "Pro"}


def show():
    st.markdown("""
        <div style="padding:1rem 0 0.5rem;">
            <h1 style="color:#2D2420;font-size:1.9rem;font-weight:700;margin:0;">Skill Management</h1>
            <p style="color:#7A6A62;margin-top:4px;">Add skills you want to master</p>
        </div>
    """, unsafe_allow_html=True)

    user  = get_user_data()
    current_skills = {s["name"]: s for s in user.get("skills", [])}
    remaining = [s for s in AVAILABLE_SKILLS if s not in current_skills]

    col_add, col_list = st.columns([1, 2])

    with col_add:
        st.markdown('<div class="page-card">', unsafe_allow_html=True)
        st.markdown("#### Add a Skill")
        if not remaining:
            st.success("You've added all available skills!")
        else:
            with st.form("add_skill_form"):
                skill = st.selectbox("Skill", remaining)
                level = st.selectbox("Proficiency Level", PROFICIENCY_LEVELS,
                                     format_func=lambda l: f"{LEVEL_LABEL[l]} — {l}")
                st.markdown("<br>", unsafe_allow_html=True)
                submitted = st.form_submit_button("Add Skill", use_container_width=True, type="primary")
            if submitted:
                updated = user.get("skills", []) + [{"name": skill, "level": level}]
                save_field("skills", updated)
                st.success(f"Added **{skill}** ({level})")
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with col_list:
        st.markdown("#### Your Skills")
        skills = user.get("skills", [])
        if not skills:
            st.markdown('<div class="page-card" style="text-align:center;color:#7A6A62;padding:2rem;">No skills added yet</div>', unsafe_allow_html=True)
        else:
            for s in skills:
                c1, c2, c3 = st.columns([3, 2, 1])
                color = LEVEL_COLOR.get(s["level"], "#8B6F5E")
                c1.markdown(f'<div style="color:#2D2420;font-weight:600;padding:8px 0;">{s["name"]}</div>', unsafe_allow_html=True)
                c2.markdown(f'<div style="color:{color};padding:8px 0;">{s["level"]}</div>', unsafe_allow_html=True)
                if c3.button("X", key=f"rm_{s['name']}", help=f"Remove {s['name']}"):
                    updated = [x for x in skills if x["name"] != s["name"]]
                    save_field("skills", updated)
                    st.rerun()
                st.markdown('<hr style="border-color:#E8E0D8;margin:0;">', unsafe_allow_html=True)
