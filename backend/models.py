from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from datetime import datetime


# ── Auth ─────────────────────────────────────────────────────────────────────

class RegisterRequest(BaseModel):
    username: str
    email: EmailStr
    password: str

    @field_validator("username")
    @classmethod
    def username_valid(cls, v):
        if len(v) < 3:
            raise ValueError("Username must be at least 3 characters")
        return v

    @field_validator("password")
    @classmethod
    def password_valid(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ── Skills ───────────────────────────────────────────────────────────────────

class Skill(BaseModel):
    name: str
    level: str  # Beginner | Intermediate | Pro


class SkillsUpdateRequest(BaseModel):
    skills: list[Skill]


# ── Quiz ─────────────────────────────────────────────────────────────────────

class QuizRequest(BaseModel):
    skill: str
    level: str
    num_questions: int = 5


class QuizQuestion(BaseModel):
    question: str
    options: list[str]
    answer: str
    explanation: str


class QuizSubmitRequest(BaseModel):
    skill: str
    score: int
    weak_topics: list[str] = []


# ── Notes ────────────────────────────────────────────────────────────────────

class NotesRequest(BaseModel):
    skill: str
    topic: str


# ── Profile ──────────────────────────────────────────────────────────────────

class ProfileUpdateRequest(BaseModel):
    email: Optional[EmailStr] = None
    reminder_days: Optional[int] = None


# ── Analytics ────────────────────────────────────────────────────────────────

class QuizRecord(BaseModel):
    skill: str
    score: int
    timestamp: datetime
    weak_topics: list[str] = []
