from typing import Annotated
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from app.database import get_db
from app.models import Review
from app.schemas import ReviewCreate, ReviewResponse, ReviewUpdate
from uuid import UUID

router = APIRouter(tags=["Reviews"])


@router.get("/reviews/{review_id}", response_model=ReviewResponse)
def get_review(review_id: UUID, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(Review).where(Review.id == review_id))
    review = result.scalars().first()
    if review:
        return review
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Review not found"
    )


@router.get("/games/{game_id}/reviews", response_model=list[ReviewResponse])
def get_reviews_for_game(game_id: UUID, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(Review).where(Review.game_id == game_id))
    reviews = result.scalars().all()
    return reviews


@router.get("/users/{user_id}/reviews", response_model=list[ReviewResponse])
def get_reviews_from_user(user_id: UUID, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(Review).where(Review.user_id == user_id))
    reviews = result.scalars().all()
    return reviews
