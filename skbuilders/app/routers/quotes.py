from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import QuoteRequest
from app.schemas.schemas import QuoteCreate, QuoteOut
from app.auth_utils import get_current_admin

router = APIRouter()


# ── Public endpoint ────────────────────────────────────────

@router.post("/", response_model=QuoteOut, status_code=201)
def submit_quote(payload: QuoteCreate, db: Session = Depends(get_db)):
    """
    Submit a 'Request a Quote' form.
    Called from the frontend quote/contact form.
    """
    quote = QuoteRequest(**payload.model_dump())
    db.add(quote)
    db.commit()
    db.refresh(quote)
    return quote


# ── Admin-only endpoints ───────────────────────────────────

@router.get("/", response_model=List[QuoteOut])
def list_quotes(
    skip:  int = 0,
    limit: int = 20,
    db:    Session = Depends(get_db),
    _:     object  = Depends(get_current_admin)
):
    """List all quote requests. Admin only."""
    return db.query(QuoteRequest).order_by(
        QuoteRequest.created_at.desc()
    ).offset(skip).limit(limit).all()


@router.patch("/{quote_id}/read", response_model=QuoteOut)
def mark_as_read(
    quote_id: int,
    db:       Session = Depends(get_db),
    _:        object  = Depends(get_current_admin)
):
    """Mark a quote request as read. Admin only."""
    quote = db.query(QuoteRequest).filter(QuoteRequest.id == quote_id).first()
    if not quote:
        raise HTTPException(status_code=404, detail="Quote request not found")
    quote.is_read = True
    db.commit()
    db.refresh(quote)
    return quote


@router.delete("/{quote_id}", status_code=204)
def delete_quote(
    quote_id: int,
    db:       Session = Depends(get_db),
    _:        object  = Depends(get_current_admin)
):
    """Delete a quote request. Admin only."""
    quote = db.query(QuoteRequest).filter(QuoteRequest.id == quote_id).first()
    if not quote:
        raise HTTPException(status_code=404, detail="Quote request not found")
    db.delete(quote)
    db.commit()
