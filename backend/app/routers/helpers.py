from fastapi import status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from app.models import Review, User


async def get_review_or_404(db: AsyncSession, review_id: UUID) -> Review:
    result = await db.execute(select(Review).where(Review.id == review_id))
    review = result.scalars().first()
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Review not found"
        )
    return review


def check_review_owner_or_admin(
    review: Review, current_user: User, action: str = "update"
) -> None:
    if review.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Not authorised to {action} this review",
        )
