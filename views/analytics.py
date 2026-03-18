import streamlit as st
import pandas as pd
import plotly.express as px
from utils.session import get_user_data

PLOTLY_LAYOUT = dict(
    template="plotly_white", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter", color="#7A6A62"), margin=dict(l=10, r=10, t=30, b=10),
)


def show():
    st.markdown("""
        <div style="padding:1rem 0 0.5rem;">
            <h1 style="color:#2D2420;font-size:1.9rem;font-weight:700;margin:0;">Analytics</h1>
            <p style="color:#7A6A62;margin-top:4px;">Track your learning progress over time</p>
        </div>
    """, unsafe_allow_html=True)

    user    = get_user_data()
    history = user.get("quiz_history", [])

    if not history:
        st.markdown('<div class="page-card" style="text-align:center;padding:3rem;"><div style="color:#2D2420;margin-top:12px;font-size:1.1rem;">No data yet</div><div style="color:#7A6A62;font-size:0.85rem;margin-top:4px;">Take some quizzes to see your analytics</div></div>', unsafe_allow_html=True)
        return

    df = pd.DataFrame(history)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values("timestamp")

    avg  = round(df["score"].mean(), 1)
    best = int(df["score"].max())
    last = int(df.iloc[-1]["score"])
    trend = "Up" if len(df) > 1 and df.iloc[-1]["score"] >= df.iloc[-2]["score"] else "Down"

    c1, c2, c3, c4 = st.columns(4)
    for col, val, label in [(c1, len(df), "Total Quizzes"), (c2, f"{avg}%", "Avg Score"), (c3, f"{best}%", "Best Score"), (c4, f"{last}% ({trend})", "Last Score")]:
        col.markdown(f'<div class="metric-card"><div class="value">{val}</div><div class="label">{label}</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col_l, col_r = st.columns([3, 2])

    with col_l:
        st.markdown('<div class="section-header"><h3>Score Over Time</h3></div>', unsafe_allow_html=True)
        fig = px.line(df, x="timestamp", y="score", color="skill", markers=True,
                      labels={"score": "Score (%)", "timestamp": "Date"},
                      color_discrete_sequence=["#8B6F5E", "#6B8F71", "#C49A3C", "#C4614A", "#C4A882"])
        fig.update_layout(**PLOTLY_LAYOUT)
        fig.update_traces(line=dict(width=2.5))
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        st.markdown('<div class="section-header"><h3>Avg by Skill</h3></div>', unsafe_allow_html=True)
        avg_df = df.groupby("skill")["score"].mean().reset_index()
        avg_df.columns = ["Skill", "Avg Score"]
        fig2 = px.bar(avg_df, x="Avg Score", y="Skill", orientation="h",
                      color="Avg Score", color_continuous_scale=["#C4614A", "#C49A3C", "#6B8F71"], range_color=[0, 100])
        fig2.update_layout(**PLOTLY_LAYOUT, coloraxis_showscale=False)
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown('<div class="section-header"><h3>Weak Topics</h3></div>', unsafe_allow_html=True)
    weak = [t for q in history for t in q.get("weak_topics", [])]
    if weak:
        weak_df = pd.Series(weak).value_counts().reset_index()
        weak_df.columns = ["Topic", "Times Missed"]
        fig3 = px.bar(weak_df.head(10), x="Times Missed", y="Topic", orientation="h",
                      color="Times Missed", color_continuous_scale=["#C49A3C", "#C4614A"])
        fig3.update_layout(**PLOTLY_LAYOUT, coloraxis_showscale=False)
        st.plotly_chart(fig3, use_container_width=True)
    else:
        st.markdown('<div class="page-card" style="text-align:center;border-color:#6B8F71;padding:1.5rem;"><div style="color:#6B8F71;margin-top:6px;">No weak topics — great work!</div></div>', unsafe_allow_html=True)
