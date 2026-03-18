import streamlit as st
from datetime import datetime
from utils.session import get_user_data, save_field
from utils.ai_client import generate_notes
from utils.pdf_export import export_notes_pdf


def show():
    st.markdown("""
        <div style="padding:1rem 0 0.5rem;">
            <h1 style="color:#2D2420;font-size:1.9rem;font-weight:700;margin:0;">Study Notes</h1>
            <p style="color:#7A6A62;margin-top:4px;">AI-generated notes on any topic</p>
        </div>
    """, unsafe_allow_html=True)

    user   = get_user_data()
    skills = [s["name"] for s in user.get("skills", [])]

    if not skills:
        st.markdown('<div class="page-card" style="text-align:center;padding:2rem;"><div style="color:#2D2420;margin-top:8px;">No skills added yet</div><div style="color:#7A6A62;font-size:0.85rem;">Go to Skills page first</div></div>', unsafe_allow_html=True)
        return

    col_gen, col_lib = st.columns([1, 1])

    with col_gen:
        st.markdown('<div class="page-card">', unsafe_allow_html=True)
        st.markdown("#### Generate Notes")
        with st.form("notes_form"):
            skill     = st.selectbox("Skill", skills)
            topic     = st.text_input("Topic", placeholder="e.g. list comprehensions, async/await")
            submitted = st.form_submit_button("Generate", use_container_width=True, type="primary")
        st.markdown('</div>', unsafe_allow_html=True)

        if submitted:
            if not topic.strip():
                st.warning("Please enter a topic.")
            else:
                with st.spinner("AI is writing your notes..."):
                    content = generate_notes(skill, topic)
                note = {"skill": skill, "topic": topic, "content": content, "timestamp": datetime.now().isoformat()}
                notes = user.get("notes", []) + [note]
                save_field("notes", notes)
                st.success("Notes generated!")
                st.markdown('<div class="page-card">', unsafe_allow_html=True)
                st.markdown(content)
                pdf_bytes = export_notes_pdf(skill, topic, content)
                st.download_button("Download PDF", pdf_bytes, file_name=f"{skill}_{topic}.pdf", mime="application/pdf", use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

    with col_lib:
        st.markdown("#### Notes Library")
        notes = user.get("notes", [])
        if not notes:
            st.markdown('<div class="page-card" style="text-align:center;color:#7A6A62;padding:2rem;">No notes yet</div>', unsafe_allow_html=True)
        else:
            for n in reversed(notes):
                ts_str = str(n.get("timestamp", ""))[:10]
                with st.expander(f"{n['skill']} — {n['topic']}  ·  {ts_str}"):
                    st.markdown(n["content"])
                    pdf_bytes = export_notes_pdf(n["skill"], n["topic"], n["content"])
                    st.download_button("Download PDF", pdf_bytes,
                                       file_name=f"{n['skill']}_{n['topic']}.pdf",
                                       mime="application/pdf",
                                       key=f"dl_{n['skill']}_{n['topic']}_{ts_str}")
