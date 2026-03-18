from fastapi import APIRouter, Depends
from datetime import datetime
from backend.models import QuizRequest, QuizSubmitRequest
from backend import database as db
from backend.auth import get_current_user
from utils.ai_client import generate_quiz

router = APIRouter(prefix="/api/quiz", tags=["Quiz"])


@router.post("/generate")
def generate(req: QuizRequest, username: str = Depends(get_current_user)):
    questions = generate_quiz(req.skill, req.level, req.num_questions)
    return {"skill": req.skill, "level": req.level, "questions": questions}


@router.post("/submit")
def submit_quiz(req: QuizSubmitRequest, username: str = Depends(get_current_user)):
    user = db.get_user(username)
    record = {
        "skill": req.skill,
        "score": req.score,
        "weak_topics": req.weak_topics,
        "timestamp": datetime.utcnow().isoformat(),
    }
    history = user.get("quiz_history", [])
    history.append(record)
    db.update_user(username, {"quiz_history": history})
    return {"message": "Quiz result saved", "record": record}


@router.get("/history")
def quiz_history(username: str = Depends(get_current_user)):
    user = db.get_user(username)
    return {"history": user.get("quiz_history", [])}
