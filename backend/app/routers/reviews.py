from typing import Annotated
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models import Review, Game
from app.schemas import ReviewCreate, ReviewResponse, ReviewUpdate
from uuid import UUID
from sqlalchemy.orm import joinedload
from app.auth import CurrentUser
from app.routers.helpers import get_review_or_404, check_review_owner_or_admin

router = APIRouter(tags=["Reviews"])


@router.get("/reviews/{review_id}", response_model=ReviewResponse)
async def get_review(review_id: UUID, db: Annotated[AsyncSession, Depends(get_db)]):
    return await get_review_or_404(db, review_id)


@router.get("/games/{game_id}/reviews", response_model=list[ReviewResponse])
async def get_reviews_for_game(
    game_id: UUID, db: Annotated[AsyncSession, Depends(get_db)]
):
    result = await db.execute(
        select(Review)
        .options(joinedload(Review.user), joinedload(Review.game))
        .where(Review.game_id == game_id)
    )
    reviews = result.scalars().all()
    return reviews


@router.get("/users/{user_id}/reviews", response_model=list[ReviewResponse])
async def get_reviews_from_user(
    user_id: UUID, db: Annotated[AsyncSession, Depends(get_db)]
):
    result = await db.execute(
        select(Review)
        .options(joinedload(Review.game), joinedload(Review.user))
        .where(Review.user_id == user_id)
    )
    reviews = result.scalars().all()
    return reviews


@router.post(
    "/reviews/create-review",
    response_model=ReviewResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_review(
    review: ReviewCreate,
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    result = await db.execute(select(Game).where(Game.id == review.game_id))
    game = result.scalars().first()
    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Game not found"
        )

    result = await db.execute(
        select(Review).where(
            Review.game_id == review.game_id, Review.user_id == current_user.id
        )
    )

    existing_review = result.scalars().first()
    if existing_review:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A review for this game already exists by the current user",
        )
    new_review = Review(**review.model_dump(), user_id=current_user.id)
    db.add(new_review)
    await db.commit()
    await db.refresh(new_review)
    new_review.user = current_user
    new_review.game = game

    return new_review


@router.patch("/reviews/{review_id}", response_model=ReviewResponse)
async def update_review(
    review_id: UUID,
    review_update: ReviewUpdate,
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    review = await get_review_or_404(db, review_id)
    check_review_owner_or_admin(review, current_user, action="update")

    update_data = review_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(review, field, value)

    await db.commit()
    await db.refresh(review)
    return review


@router.delete("/reviews/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_review(
    review_id: UUID,
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    review = await get_review_or_404(db, review_id)
    check_review_owner_or_admin(review, current_user, action="delete")

    await db.delete(review)
    await db.commit()
