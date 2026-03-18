import os
from dotenv import load_dotenv

load_dotenv()

APP_NAME = os.getenv("APP_NAME", "SkillTrack AI")
SECRET_KEY = os.getenv("SECRET_KEY", "changeme")
AI_PROVIDER = os.getenv("AI_PROVIDER", "openai")  # "openai" or "gemini"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
DEBUG = os.getenv("DEBUG", "True") == "True"

PROFICIENCY_LEVELS = ["Beginner", "Intermediate", "Pro"]

AVAILABLE_SKILLS = [
    "Python", "JavaScript", "React", "Node.js", "FastAPI",
    "MySQL", "PostgreSQL", "MongoDB", "Docker", "Kubernetes",
    "Machine Learning", "Data Science", "TypeScript", "Go", "Rust",
]

QUIZ_QUESTION_COUNT = 5
RETENTION_REMINDER_DAYS = 3
