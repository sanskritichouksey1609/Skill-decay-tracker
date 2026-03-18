from fastapi import APIRouter, Depends
from collections import Counter
from backend import database as db
from backend.auth import get_current_user

router = APIRouter(prefix="/api/analytics", tags=["Analytics"])


@router.get("/summary")
def summary(username: str = Depends(get_current_user)):
    user = db.get_user(username)
    history = user.get("quiz_history", [])

    if not history:
        return {
            "total_quizzes": 0,
            "avg_score": 0,
            "skills_tracked": len(user.get("skills", [])),
            "notes_count": len(user.get("notes", [])),
            "per_skill": [],
            "weak_topics": [],
        }

    avg_score = round(sum(q["score"] for q in history) / len(history), 1)

    # Per-skill averages
    skill_scores: dict[str, list] = {}
    for q in history:
        skill_scores.setdefault(q["skill"], []).append(q["score"])
    per_skill = [
        {"skill": s, "avg_score": round(sum(v) / len(v), 1), "attempts": len(v)}
        for s, v in skill_scores.items()
    ]

    # Weak topics frequency
    all_weak = [t for q in history for t in q.get("weak_topics", [])]
    weak_topics = [{"topic": t, "count": c} for t, c in Counter(all_weak).most_common(10)]

    return {
        "total_quizzes": len(history),
        "avg_score": avg_score,
        "skills_tracked": len(user.get("skills", [])),
        "notes_count": len(user.get("notes", [])),
        "per_skill": per_skill,
        "weak_topics": weak_topics,
    }


@router.get("/history")
def score_history(username: str = Depends(get_current_user)):
    user = db.get_user(username)
    return {"history": user.get("quiz_history", [])}
