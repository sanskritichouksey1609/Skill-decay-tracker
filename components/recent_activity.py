import streamlit as st
from datetime import datetime


def activity_feed(activities: list[dict]):
    type_labels = {"quiz": "Quiz", "note": "Note", "skill": "Skill", "reminder": "Reminder"}

    if not activities:
        st.markdown(
            '<div class="page-card" style="text-align:center;color:#7A6A62;padding:2rem;">'
            'No activity yet — start by taking a quiz!'
            '</div>',
            unsafe_allow_html=True,
        )
        return

    for item in activities[:10]:
        label = type_labels.get(item.get("type", ""), "")
        ts = item.get("timestamp")
        if isinstance(ts, datetime):
            ts_str = ts.strftime("%b %d, %H:%M")
        elif ts:
            ts_str = str(ts)[:16].replace("T", " ")
        else:
            ts_str = "Just now"

        st.markdown(
            f"""
            <div class="activity-item">
                <div class="activity-icon" style="color:#8B6F5E;font-size:0.75rem;font-weight:600;text-transform:uppercase;">{label}</div>
                <div>
                    <div class="activity-desc">{item.get("description","")}</div>
                    <div class="activity-time">{ts_str}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
