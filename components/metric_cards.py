import streamlit as st

def metric_card(label: str, value, icon: str = ""):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="value">{value}</div>
            <div class="label">{label}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def metric_row(metrics: list[dict]):
    cols = st.columns(len(metrics))
    for col, m in zip(cols, metrics):
        with col:
            metric_card(m.get("label", ""), m.get("value", ""), m.get("icon", ""))
