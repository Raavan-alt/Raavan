import os
import uuid
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import Project, ProjectStatus
from app.schemas.schemas import ProjectOut
from app.auth_utils import get_current_admin

router     = APIRouter()
UPLOAD_DIR = "uploads/projects"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def save_image(file: UploadFile) -> str:
    """Save uploaded image and return its URL path."""
    ext      = os.path.splitext(file.filename)[1]
    filename = f"{uuid.uuid4().hex}{ext}"
    filepath = os.path.join(UPLOAD_DIR, filename)
    with open(filepath, "wb") as f:
        f.write(file.file.read())
    return f"/uploads/projects/{filename}"


# ── Public endpoints ───────────────────────────────────────

@router.get("/", response_model=List[ProjectOut])
def list_projects(
    status: Optional[ProjectStatus] = Query(None, description="Filter by status"),
    skip:   int = Query(0,  ge=0),
    limit:  int = Query(6,  ge=1, le=50),
    db:     Session = Depends(get_db)
):
    """
    List all projects. Supports filtering by status and pagination.
    Used by: Project Gallery page (filter tabs + Load More button).
    """
    query = db.query(Project)
    if status:
        query = query.filter(Project.status == status)
    return query.order_by(Project.created_at.desc()).offset(skip).limit(limit).all()


@router.get("/{project_id}", response_model=ProjectOut)
def get_project(project_id: int, db: Session = Depends(get_db)):
    """Get a single project by ID."""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


# ── Admin-only endpoints ───────────────────────────────────

@router.post("/", response_model=ProjectOut, status_code=201)
def create_project(
    title:        str              = Form(...),
    description:  str              = Form(...),
    status:       ProjectStatus    = Form(...),
    before_image: Optional[UploadFile] = File(None),
    after_image:  Optional[UploadFile] = File(None),
    db:           Session          = Depends(get_db),
    _:            object           = Depends(get_current_admin)
):
    """Create a new project with optional before/after images. Admin only."""
    project = Project(
        title        = title,
        description  = description,
        status       = status,
        before_image = save_image(before_image) if before_image else None,
        after_image  = save_image(after_image)  if after_image  else None,
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


@router.put("/{project_id}", response_model=ProjectOut)
def update_project(
    project_id:   int,
    title:        Optional[str]           = Form(None),
    description:  Optional[str]           = Form(None),
    status:       Optional[ProjectStatus] = Form(None),
    before_image: Optional[UploadFile]    = File(None),
    after_image:  Optional[UploadFile]    = File(None),
    db:           Session                 = Depends(get_db),
    _:            object                  = Depends(get_current_admin)
):
    """Update project details and/or images. Admin only."""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if title:        project.title       = title
    if description:  project.description = description
    if status:       project.status      = status
    if before_image: project.before_image = save_image(before_image)
    if after_image:  project.after_image  = save_image(after_image)

    db.commit()
    db.refresh(project)
    return project


@router.delete("/{project_id}", status_code=204)
def delete_project(
    project_id: int,
    db:         Session = Depends(get_db),
    _:          object  = Depends(get_current_admin)
):
    """Delete a project. Admin only."""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    db.delete(project)
    db.commit()
