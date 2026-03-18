from fastapi import APIRouter, Depends, HTTPException
from backend.models import ProfileUpdateRequest
from backend import database as db
from backend.auth import get_current_user

router = APIRouter(prefix="/api/profile", tags=["Profile"])


@router.get("/")
def get_profile(username: str = Depends(get_current_user)):
    user = db.get_user(username)
    return {k: v for k, v in user.items() if k != "password_hash"}


@router.patch("/")
def update_profile(req: ProfileUpdateRequest, username: str = Depends(get_current_user)):
    updates = req.model_dump(exclude_none=True)
    if not updates:
        raise HTTPException(status_code=400, detail="No fields to update")
    updated = db.update_user(username, updates)
    return {k: v for k, v in updated.items() if k != "password_hash"}
