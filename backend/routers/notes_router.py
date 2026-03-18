from fastapi import APIRouter, Depends
from fastapi.responses import Response
from datetime import datetime
from backend.models import NotesRequest
from backend import database as db
from backend.auth import get_current_user
from utils.ai_client import generate_notes
from utils.pdf_export import export_notes_pdf

router = APIRouter(prefix="/api/notes", tags=["Notes"])


@router.post("/generate")
def generate(req: NotesRequest, username: str = Depends(get_current_user)):
    content = generate_notes(req.skill, req.topic)
    note = {
        "skill": req.skill,
        "topic": req.topic,
        "content": content,
        "timestamp": datetime.utcnow().isoformat(),
    }
    user = db.get_user(username)
    notes = user.get("notes", [])
    notes.append(note)
    db.update_user(username, {"notes": notes})
    return note


@router.get("/")
def list_notes(username: str = Depends(get_current_user)):
    user = db.get_user(username)
    return {"notes": user.get("notes", [])}


@router.post("/export-pdf")
def export_pdf(req: NotesRequest, username: str = Depends(get_current_user)):
    """Generate notes and return as a downloadable PDF."""
    content = generate_notes(req.skill, req.topic)
    pdf_bytes = export_notes_pdf(req.skill, req.topic, content)
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{req.skill}_{req.topic}.pdf"'},
    )
