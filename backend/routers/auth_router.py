from fastapi import APIRouter, HTTPException, status
from backend.models import RegisterRequest, LoginRequest, TokenResponse
from backend import database as db
from backend.auth import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/api/auth", tags=["Auth"])


@router.post("/register", status_code=201)
def register(req: RegisterRequest):
    if db.get_user(req.username):
        raise HTTPException(status_code=400, detail="Username already taken")
    if db.get_user_by_email(req.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    user = db.create_user(req.username, req.email, hash_password(req.password))
    return {"message": "Account created", "username": user["username"]}


@router.post("/login", response_model=TokenResponse)
def login(req: LoginRequest):
    user = db.get_user(req.username)
    if not user or not verify_password(req.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": user["username"]})
    return TokenResponse(access_token=token)
