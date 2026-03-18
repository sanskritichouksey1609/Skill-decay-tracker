"""
SkillTrack AI — FastAPI Backend
Run with: uvicorn backend.main:app --reload --port 8000
Docs at:  http://localhost:8000/docs
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import (
    auth_router,
    skills_router,
    quiz_router,
    notes_router,
    analytics_router,
    profile_router,
)

app = FastAPI(
    title="SkillTrack AI API",
    description="Backend API for SkillTrack AI learning management system",
    version="1.0.0",
)

# Allow Streamlit frontend (localhost:8501) to call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "http://127.0.0.1:8501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register all routers
app.include_router(auth_router.router)
app.include_router(skills_router.router)
app.include_router(quiz_router.router)
app.include_router(notes_router.router)
app.include_router(analytics_router.router)
app.include_router(profile_router.router)


@app.get("/")
def root():
    return {"message": "SkillTrack AI API is running", "docs": "/docs"}


@app.get("/health")
def health():
    return {"status": "ok"}
