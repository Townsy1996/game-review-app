from sqlalchemy import (
    Column,
    Float,
    String,
    Text,
    ForeignKey,
    DateTime,
    ARRAY,
    Boolean,
    Date,
    UniqueConstraint,
    Enum,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.enums import AgeRating


# Postgres tables in the database
class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    is_admin = Column(Boolean, nullable=False, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    reviews = relationship("Review", back_populates="user")


class Game(Base):
    __tablename__ = "games"
    __table_args__ = (
        UniqueConstraint("title", "release_date", name="uq_title_release_date"),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False, index=True)
    platforms = Column(ARRAY(String), nullable=False)
    genres = Column(ARRAY(String), nullable=False)
    description = Column(Text, nullable=True)
    release_date = Column(Date, nullable=False, index=True)
    developer = Column(String, nullable=False, index=True)
    publisher = Column(String, nullable=False, index=True)
    age_rating = Column(Enum(AgeRating), nullable=False)
    is_multiplayer = Column(Boolean, nullable=True)
    is_couch_coop = Column(Boolean, nullable=True)
    cover_image_url = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    reviews = relationship(
        "Review", back_populates="game", cascade="all, delete-orphan"
    )


class Review(Base):
    __tablename__ = "reviews"
    __table_args__ = (
        UniqueConstraint("user_id", "game_id", name="uq_user_game_review"),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    rating = Column(Float, nullable=False)
    comment = Column(Text, nullable=True)
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    game_id = Column(
        UUID(as_uuid=True), ForeignKey("games.id"), nullable=False, index=True
    )

    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    user = relationship("User", back_populates="reviews")
    game = relationship("Game", back_populates="reviews")
