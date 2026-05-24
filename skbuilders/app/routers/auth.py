from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import AdminUser
from app.schemas.schemas import LoginRequest, TokenOut
from app.auth_utils import hash_password, verify_password, create_access_token

router = APIRouter()


@router.post("/login", response_model=TokenOut)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    """Admin login — returns a JWT bearer token."""
    user = db.query(AdminUser).filter(AdminUser.username == payload.username).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}


@router.post("/register", status_code=201)
def register_admin(payload: LoginRequest, db: Session = Depends(get_db)):
    """
    Register the first admin account.
    Remove or protect this endpoint after initial setup!
    """
    existing = db.query(AdminUser).filter(AdminUser.username == payload.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already taken")

    new_admin = AdminUser(
        username        = payload.username,
        hashed_password = hash_password(payload.password)
    )
    db.add(new_admin)
    db.commit()
    return {"message": f"Admin '{payload.username}' created successfully"}
