
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from .models import ClientRequest, WebsiteProject
from .schemas import (
    ClientRequestCreate,
    ClientRequestOut,
    ProjectCreate,
    ProjectOut,
)

# Initialize database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI application
app = FastAPI(
    title="AstraAI API",
    version="1.0.0",
)

# Allow requests from the deployed frontend and local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://astraai-project-intelligence.onrender.com",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health():
    return {"status": "healthy", "app": "AstraAI"}


@app.get("/api/requests", response_model=list[ClientRequestOut])
def list_requests(db: Session = Depends(get_db)):
    return db.query(ClientRequest).order_by(ClientRequest.id.desc()).all()


@app.post(
    "/api/requests",
    response_model=ClientRequestOut,
    status_code=201,
)
def create_request(
    payload: ClientRequestCreate,
    db: Session = Depends(get_db),
):
    fields = {
        key: value.strip()
        for key, value in payload.model_dump().items()
    }

    for key, value in fields.items():
        if not value:
            raise HTTPException(
                status_code=422,
                detail=f"{key} cannot be blank.",
            )

    item = ClientRequest(**fields, status="pending")
    db.add(item)
    db.commit()
    db.refresh(item)

    return item


@app.get("/api/projects", response_model=list[ProjectOut])
def list_projects(db: Session = Depends(get_db)):
    return db.query(WebsiteProject).order_by(WebsiteProject.id.desc()).all()


@app.post(
    "/api/requests/{request_id}/generate",
    response_model=ProjectOut,
    status_code=201,
)
def generate_project(
    request_id: int,
    payload: ProjectCreate,
    db: Session = Depends(get_db),
):
    item = (
        db.query(ClientRequest)
        .filter(ClientRequest.id == request_id)
        .first()
    )

    if not item:
        raise HTTPException(
            status_code=404,
            detail="Client request not found.",
        )

    if item.project:
        raise HTTPException(
            status_code=409,
            detail="A project already exists for this request.",
        )

    project = WebsiteProject(
        request_id=item.id,
        name=payload.project_name.strip(),
        status="draft",
    )

    item.status = "in_progress"
    db.add(project)
    db.commit()
    db.refresh(project)

    return project


@app.post(
    "/api/projects/{project_id}/approve",
    response_model=ProjectOut,
)
def approve_project(
    project_id: int,
    db: Session = Depends(get_db),
):
    project = (
        db.query(WebsiteProject)
        .filter(WebsiteProject.id == project_id)
        .first()
    )

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found.",
        )

    project.status = "approved"
    db.commit()
    db.refresh(project)

    return project


@app.post(
    "/api/projects/{project_id}/publish",
    response_model=ProjectOut,
)
def publish_project(
    project_id: int,
    db: Session = Depends(get_db),
):
    project = (
        db.query(WebsiteProject)
        .filter(WebsiteProject.id == project_id)
        .first()
    )

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found.",
        )

    if project.status != "approved":
        raise HTTPException(
            status_code=409,
            detail="Approve the project before publishing.",
        )

    project.status = "published"
    db.commit()
    db.refresh(project)

    return project
