import streamlit as st
from backend.database import get_user, create_user, update_user, _load

DEFAULT_USERNAME = "Guest"


def init_session():
    if "quiz_state" not in st.session_state:
        st.session_state.quiz_state = None

    # Load all users from disk into session
    if "users_db" not in st.session_state:
        db_data = _load()
        st.session_state.users_db = db_data["users"]

    # Ensure default Guest user exists
    if DEFAULT_USERNAME not in st.session_state.users_db:
        create_user(DEFAULT_USERNAME, "guest@skilltrack.ai", "")
        st.session_state.users_db = _load()["users"]

    if "current_user" not in st.session_state:
        st.session_state.current_user = DEFAULT_USERNAME


def get_user_data() -> dict:
    uname = st.session_state.get("current_user", DEFAULT_USERNAME)
    # Always sync from disk to stay fresh
    st.session_state.users_db = _load()["users"]
    return st.session_state.users_db.get(uname, {})


def save_field(field: str, value):
    """Persist a single field for the current user."""
    uname = st.session_state.get("current_user", DEFAULT_USERNAME)
    update_user(uname, {field: value})
    st.session_state.users_db = _load()["users"]
