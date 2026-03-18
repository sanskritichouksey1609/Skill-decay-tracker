"""
AI content generation — Gemini only (google-genai SDK).
"""
import json
import time
from google import genai
from google.genai.errors import ClientError
from utils.config import GEMINI_API_KEY

_client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None
_MODEL  = "gemini-2.5-flash"


def _call_ai(prompt: str, retries: int = 3) -> str | None:
    if _client is None:
        return None
    for attempt in range(retries):
        try:
            response = _client.models.generate_content(model=_MODEL, contents=prompt)
            return response.text
        except ClientError as e:
            if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                wait = 35 * (attempt + 1)  # 35s, 70s, 105s
                import streamlit as st
                st.warning(f"⏳ Gemini rate limit hit — waiting {wait}s before retry ({attempt+1}/{retries})...")
                time.sleep(wait)
            else:
                raise
    return None


# ── Quiz generation ───────────────────────────────────────────────────────────

QUIZ_PROMPT = """
Generate {n} multiple-choice quiz questions about {skill} for a {level} learner.
Return ONLY a valid JSON array, no markdown, no extra text:
[
  {{
    "question": "...",
    "options": ["A", "B", "C", "D"],
    "answer": "A",
    "explanation": "..."
  }}
]
"""


def _mock_questions(skill: str, n: int) -> list[dict]:
    return [
        {
            "question": f"Sample {skill} question {i+1}?",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "answer": "Option A",
            "explanation": "Add your Gemini API key to .env to get real questions.",
        }
        for i in range(n)
    ]


def generate_quiz(skill: str, level: str, n: int = 5) -> list[dict]:
    raw = _call_ai(QUIZ_PROMPT.format(skill=skill, level=level, n=n))
    if raw is None:
        return _mock_questions(skill, n)
    try:
        raw = raw.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
        questions = json.loads(raw)
        # Normalize: if answer is a single letter (A/B/C/D), map it to the full option text
        letter_map = {"A": 0, "B": 1, "C": 2, "D": 3}
        for q in questions:
            ans = q.get("answer", "").strip()
            if ans.upper() in letter_map and len(q.get("options", [])) == 4:
                q["answer"] = q["options"][letter_map[ans.upper()]]
        return questions
    except (json.JSONDecodeError, IndexError):
        return _mock_questions(skill, n)


# ── Notes generation ──────────────────────────────────────────────────────────

NOTES_PROMPT = """
Create concise, well-structured study notes about "{topic}" in {skill}.
Use markdown with headers, bullet points, and code examples where relevant.
Target a learner who struggled with this topic in a quiz.
"""


def generate_notes(skill: str, topic: str) -> str:
    raw = _call_ai(NOTES_PROMPT.format(skill=skill, topic=topic))
    if raw is None:
        return f"## {topic} in {skill}\n\n> Add your Gemini API key to `.env` to generate real notes."
    return raw
