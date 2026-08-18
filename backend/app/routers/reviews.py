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
