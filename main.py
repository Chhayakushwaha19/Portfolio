"""
FastAPI backend for Chhaya Kushwaha's Portfolio Website.
"""

from typing import List

from dotenv import load_dotenv
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import models
import schemas
from database import engine, get_db
from email_utils import send_contact_notification

# Load environment variables
load_dotenv()

# Create database tables automatically
models.Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title="Chhaya Kushwaha Portfolio API",
    version="1.0.0",
)
app.mount("/static", StaticFiles(directory="."), name="static")
# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# ---------------------------------------------------
# Profile Data
# ---------------------------------------------------

PROFILE = {
    "name": "Chhaya Kushwaha",
    "location": "Kanpur Nagar, India",
    "email": "chhayakushwaha100@gmail.com",
    "github": "https://github.com/Chhayakushwaha19",
    "linkedin": "https://linkedin.com/in/chhayakushwaha-754b64317",
    "headline": "Aspiring Full-Stack Developer",
    "education": [
        {
            "period": "2024 - 2027",
            "school": "Your College Name",
            "degree": "Bachelor of Computer Applications (BCA)",
        },
        {
            "period": "Completed",
            "school": "Chhatrapati Shivaji Inter College, Jarauli, Kanpur Nagar",
            "degree": "Intermediate",
        },
    ],
}

# ---------------------------------------------------
# Skills
# ---------------------------------------------------

SKILLS = {
    "core_and_languages": ["Python", "SQL"],
    "frontend": ["HTML", "CSS", "JavaScript"],
    "backend": ["FastAPI", "SQL"],
    "ai_and_tools": ["Generative AI", "Git", "GitHub"],
}

# ---------------------------------------------------
# Projects
# ---------------------------------------------------

PROJECTS = [
    {
        "name": "Health AI Assistant",
        "summary": "An AI-powered application that helps users analyze health reports and understand information in a simple way.",
        "tech": ["Python", "FastAPI", "Generative AI"],
    },
    {
        "name": "RAG System",
        "summary": "A RAG-based system that retrieves relevant information from documents and generates context-aware responses.",
        "tech": ["Python", "FastAPI", "Generative AI"],
    },
    {
        "name": "AI Chatbot",
        "summary": "An intelligent chatbot that answers user questions with helpful and context-aware responses.",
        "tech": ["Python", "Generative AI", "FastAPI"],
    },
]

# ---------------------------------------------------
# Routes
# ---------------------------------------------------

@app.get("/")
def home():
    return FileResponse("index.html")


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/profile")
def get_profile():
    return PROFILE


@app.get("/api/skills")
def get_skills():
    return SKILLS


@app.get("/api/projects")
def get_projects():
    return PROJECTS


# ---------------------------------------------------
# Contact Form API
# ---------------------------------------------------

@app.post("/api/contact", response_model=schemas.ContactOut)
def create_contact(
    payload: schemas.ContactCreate,
    db: Session = Depends(get_db),
):
    entry = models.ContactMessage(
        name=payload.name,
        email=payload.email,
        message=payload.message,
    )

    db.add(entry)
    db.commit()
    db.refresh(entry)

    try:
        send_contact_notification(
            payload.name,
            payload.email,
            payload.message,
        )
    except Exception as error:
        print("Email notification error:", error)

    return entry


# ---------------------------------------------------
# View Contact Messages
# ---------------------------------------------------

@app.get("/api/contact", response_model=List[schemas.ContactOut])
def list_contacts(db: Session = Depends(get_db)):
    messages = (
        db.query(models.ContactMessage)
        .order_by(models.ContactMessage.id.desc())
        .all()
    )
    return messages

