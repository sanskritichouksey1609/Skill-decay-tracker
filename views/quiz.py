import streamlit as st
from datetime import datetime
from utils.session import get_user_data, save_field
from utils.config import QUIZ_QUESTION_COUNT
from utils.ai_client import generate_quiz


def _is_correct(user_ans, correct_ans) -> bool:
    if user_ans is None:
        return False
    return str(user_ans).strip().lower() == str(correct_ans).strip().lower()


def show():
    st.markdown("""
        <div style="padding:1rem 0 0.5rem;">
            <h1 style="color:#2D2420;font-size:1.9rem;font-weight:700;margin:0;">Quiz</h1>
            <p style="color:#7A6A62;margin-top:4px;">Test your knowledge with AI-generated questions</p>
        </div>
    """, unsafe_allow_html=True)

    user   = get_user_data()
    skills = user.get("skills", [])

    if not skills:
        st.markdown('<div class="page-card" style="text-align:center;padding:2rem;"><div style="color:#2D2420;margin-top:8px;">No skills added yet</div><div style="color:#7A6A62;font-size:0.85rem;">Go to Skills page first</div></div>', unsafe_allow_html=True)
        return

    # -- Setup ----------------------------------------------------------------
    if st.session_state.quiz_state is None:
        col = st.columns([1, 2, 1])[1]
        with col:
            st.markdown('<div class="page-card">', unsafe_allow_html=True)
            st.markdown("#### Start a Quiz")
            skill_names = [s["name"] for s in skills]
            selected    = st.selectbox("Choose skill", skill_names)
            skill_obj   = next(s for s in skills if s["name"] == selected)
            st.markdown(f'<div style="color:#7A6A62;font-size:0.85rem;margin:4px 0 12px;">Level: <span style="color:#8B6F5E;">{skill_obj["level"]}</span> · {QUIZ_QUESTION_COUNT} questions</div>', unsafe_allow_html=True)
            if st.button("Generate Quiz", use_container_width=True, type="primary"):
                with st.spinner("AI is crafting your quiz..."):
                    questions = generate_quiz(skill_obj["name"], skill_obj["level"], QUIZ_QUESTION_COUNT)
                st.session_state.quiz_state = {
                    "skill": selected, "level": skill_obj["level"],
                    "questions": questions, "answers": {}, "submitted": False,
                }
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        return

    qs = st.session_state.quiz_state

    # -- Answer phase ---------------------------------------------------------
    if not qs["submitted"]:
        total    = len(qs["questions"])
        answered = sum(1 for v in qs["answers"].values() if v is not None)
        st.markdown(f'<div style="color:#7A6A62;font-size:0.85rem;margin-bottom:4px;">{answered}/{total} answered</div>', unsafe_allow_html=True)
        st.progress(answered / total if total else 0)
        st.markdown("<br>", unsafe_allow_html=True)

        for i, q in enumerate(qs["questions"]):
            st.markdown(
                f'<div class="quiz-card"><div style="color:#8B6F5E;font-size:0.78rem;font-weight:600;margin-bottom:6px;">QUESTION {i+1} OF {total}</div>'
                f'<div style="color:#2D2420;font-size:1rem;font-weight:500;">{q["question"]}</div></div>',
                unsafe_allow_html=True,
            )
            qs["answers"][i] = st.radio(f"q{i}", q["options"], key=f"q_{i}", index=None, label_visibility="collapsed")
            st.markdown("<br>", unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            if st.button("Discard", use_container_width=True):
                st.session_state.quiz_state = None
                st.rerun()
        with c2:
            if st.button("Submit", use_container_width=True, type="primary"):
                unanswered = [i for i in range(total) if qs["answers"].get(i) is None]
                if unanswered:
                    st.warning(f"{len(unanswered)} question(s) unanswered.")
                else:
                    qs["submitted"] = True
                    st.rerun()
        return

    # -- Results --------------------------------------------------------------
    correct = sum(1 for i, q in enumerate(qs["questions"]) if _is_correct(qs["answers"].get(i), q["answer"]))
    score   = round(correct / len(qs["questions"]) * 100)
    color   = "#6B8F71" if score >= 70 else "#C49A3C" if score >= 40 else "#C4614A"
    grade   = "Excellent!" if score >= 80 else "Good job!" if score >= 60 else "Keep practicing!"

    st.markdown(f'<div class="score-display"><div class="score-num" style="color:{color};">{score}%</div><div class="score-label">{correct}/{len(qs["questions"])} correct · {grade}</div></div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-header"><h3>Review</h3></div>', unsafe_allow_html=True)

    for i, q in enumerate(qs["questions"]):
        user_ans   = qs["answers"].get(i)
        is_correct = _is_correct(user_ans, q["answer"])
        css_class  = "correct" if is_correct else "wrong"
        result     = "Correct" if is_correct else "Wrong"
        wrong_line = f'<div style="font-size:0.85rem;color:#7A6A62;">Correct answer: <span style="color:#6B8F71;">{q["answer"]}</span></div>' if not is_correct else ""
        st.markdown(
            f'<div class="quiz-card {css_class}"><div style="font-size:0.78rem;color:#7A6A62;margin-bottom:4px;">Q{i+1}</div>'
            f'<div style="color:#2D2420;font-weight:500;margin-bottom:8px;">[{result}] {q["question"]}</div>'
            f'<div style="font-size:0.85rem;color:#7A6A62;">Your answer: <span style="color:{"#6B8F71" if is_correct else "#C4614A"};">{user_ans}</span></div>'
            f'{wrong_line}<div style="font-size:0.82rem;color:#7A6A62;margin-top:6px;font-style:italic;">{q.get("explanation","")}</div></div>',
            unsafe_allow_html=True,
        )

    # Save to disk
    weak_topics = [q["question"] for i, q in enumerate(qs["questions"]) if not _is_correct(qs["answers"].get(i), q["answer"])]
    history = user.get("quiz_history", [])
    history.append({"skill": qs["skill"], "score": score, "timestamp": datetime.now().isoformat(), "weak_topics": weak_topics})
    save_field("quiz_history", history)

    if st.button("Take Another Quiz", use_container_width=True, type="primary"):
        st.session_state.quiz_state = None
        st.rerun()
