from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from datetime import datetime
from app.models.models import ProjectStatus


# Projects
class ProjectBase(BaseModel):
    title:       str
    description: str
    status:      ProjectStatus


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    title:       Optional[str]           = None
    description: Optional[str]           = None
    status:      Optional[ProjectStatus] = None


class ProjectOut(ProjectBase):
    model_config = ConfigDict(from_attributes=True)

    id:           int
    before_image: Optional[str] = None
    after_image:  Optional[str] = None
    created_at:   datetime


# Quote Requests
class QuoteCreate(BaseModel):
    full_name:    str
    email:        EmailStr
    phone:        Optional[str] = None
    company:      Optional[str] = None
    project_type: Optional[str] = None
    message:      str


class QuoteOut(QuoteCreate):
    model_config = ConfigDict(from_attributes=True)

    id:         int
    is_read:    bool
    created_at: datetime


# Auth
class LoginRequest(BaseModel):
    username: str
    password: str


class TokenOut(BaseModel):
    access_token: str
    token_type:   str = "bearer"
