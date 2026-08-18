from datetime import date, datetime
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator
import string
from app.enums import AgeRating, Genre


# User Pydantic Schemas
class UserBase(BaseModel):
    username: str = Field(min_length=3, max_length=30)
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=64)

    @field_validator("password")
    @classmethod
    def validate_password_complexity(cls, v: str) -> str:
        if not any(char.isupper() for char in v):
            raise ValueError("Password must contain at least one uppercase letter")

        if not any(char.isdigit() for char in v):
            raise ValueError("Password must contain at least one number")

        if not any(char in string.punctuation for char in v):
            raise ValueError("Password must contain at least one special character")

        return v


class UserUpdate(BaseModel):
    username: Optional[str] = Field(min_length=3, max_length=30)
    email: Optional[EmailStr]


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(UserBase):
    id: UUID
    is_active: bool
    is_admin: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# Game Pydantic Schemas
class GameBase(BaseModel):
    title: str = Field(min_length=1, max_length=80)
    platforms: List[str]
    genres: List[Genre]
    release_date: date
    developer: str
    publisher: str
    age_rating: AgeRating
    description: Optional[str] = None
    is_multiplayer: Optional[bool] = None
    is_couch_coop: Optional[bool] = None
    cover_image_url: Optional[str] = None


class GameCreate(GameBase):
    pass


class GameUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=80)
    platforms: Optional[List[str]] = None
    genres: Optional[List[Genre]] = None
    release_date: Optional[date] = None
    developer: Optional[str] = None
    publisher: Optional[str] = None
    age_rating: Optional[AgeRating] = None
    description: Optional[str] = None
    is_multiplayer: Optional[bool] = None
    is_couch_coop: Optional[bool] = None
    cover_image_url: Optional[str] = None


class GameResponse(GameBase):

    model_config = ConfigDict(from_attributes=True)
    id: UUID
    created_at: datetime
    updated_at: datetime


# Review Pydantic Schemas
class ReviewBase(BaseModel):
    rating: float = Field(ge=0.1, le=10.0)
    comment: Optional[str] = Field(default=None, min_length=1, max_length=1000)


class ReviewCreate(ReviewBase):
    game_id: UUID


class ReviewUpdate(BaseModel):
    rating: Optional[float] = Field(default=None, ge=0.1, le=10.0)
    comment: Optional[str] = Field(default=None, min_length=1, max_length=1000)


class ReviewResponse(ReviewBase):
    id: UUID
    user_id: Optional[UUID]
    game_id: UUID
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
