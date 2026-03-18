from fastapi import APIRouter, Depends
from backend.models import SkillsUpdateRequest, Skill
from backend import database as db
from backend.auth import get_current_user

router = APIRouter(prefix="/api/skills", tags=["Skills"])


@router.get("/")
def get_skills(username: str = Depends(get_current_user)):
    user = db.get_user(username)
    return {"skills": user["skills"]}


@router.post("/")
def add_skill(skill: Skill, username: str = Depends(get_current_user)):
    user = db.get_user(username)
    skills = user["skills"]
    if any(s["name"] == skill.name for s in skills):
        return {"message": "Skill already added", "skills": skills}
    skills.append(skill.model_dump())
    db.update_user(username, {"skills": skills})
    return {"message": "Skill added", "skills": skills}


@router.delete("/{skill_name}")
def remove_skill(skill_name: str, username: str = Depends(get_current_user)):
    user = db.get_user(username)
    skills = [s for s in user["skills"] if s["name"] != skill_name]
    db.update_user(username, {"skills": skills})
    return {"message": "Skill removed", "skills": skills}


@router.put("/")
def replace_skills(req: SkillsUpdateRequest, username: str = Depends(get_current_user)):
    skills = [s.model_dump() for s in req.skills]
    db.update_user(username, {"skills": skills})
    return {"skills": skills}
