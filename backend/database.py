"""
JSON-file based persistence layer.
All data is saved to data/db.json on every write.
"""
import json
from pathlib import Path

DB_PATH = Path("data/db.json")


def _load() -> dict:
    if not DB_PATH.exists():
        DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        DB_PATH.write_text(json.dumps({"users": {}}))
    try:
        return json.loads(DB_PATH.read_text())
    except json.JSONDecodeError:
        return {"users": {}}


def _save(data: dict):
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    DB_PATH.write_text(json.dumps(data, indent=2, default=str))


def get_user(username: str) -> dict | None:
    return _load()["users"].get(username)


def get_user_by_email(email: str) -> dict | None:
    for u in _load()["users"].values():
        if u.get("email") == email:
            return u
    return None


def create_user(username: str, email: str, password_hash: str) -> dict:
    db = _load()
    if username in db["users"]:
        return db["users"][username]
    user = {
        "username": username,
        "email": email,
        "password_hash": password_hash,
        "skills": [],
        "quiz_history": [],
        "notes": [],
        "reminder_days": 3,
    }
    db["users"][username] = user
    _save(db)
    return user


def update_user(username: str, fields: dict) -> dict:
    db = _load()
    if username not in db["users"]:
        return {}
    db["users"][username].update(fields)
    _save(db)
    return db["users"][username]


def list_users() -> list[dict]:
    return list(_load()["users"].values())
