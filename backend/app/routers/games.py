from typing import Annotated
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from app.database import get_db
from app.models import Game
from app.schemas import GameCreate, GameResponse, GameUpdate
from uuid import UUID

router = APIRouter(prefix="/games", tags=["Games"])


@router.post("/", response_model=GameResponse, status_code=status.HTTP_201_CREATED)
def create_game(game: GameCreate, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(
        select(Game).where(
            Game.title == game.title, Game.release_date == game.release_date
        )
    )

    existing_game = result.scalars().first()

    if existing_game:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Game with this title and release date already exists",
        )

    new_game = Game(**game.model_dump())

    db.add(new_game)
    db.commit()
    db.refresh(new_game)

    return new_game


@router.get("/", response_model=list[GameResponse])
def get_all_games(db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(Game))
    games = result.scalars().all()
    return games


@router.get("/{game_id}", response_model=GameResponse)
def get_game(game_id: UUID, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(Game).where(Game.id == game_id))
    game = result.scalars().first()
    if game:
        return game
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Game not found")


@router.put("/{game_id}", response_model=GameResponse)
def update_game_full(
    game_id: UUID, game_data: GameCreate, db: Annotated[Session, Depends(get_db)]
):
    result = db.execute(select(Game).where(Game.id == game_id))
    game = result.scalars().first()
    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Game not found"
        )

    for key, value in game_data.model_dump().items():
        setattr(game, key, value)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A game with this title and release date already exists.",
        )
    db.refresh(game)

    return game


@router.patch("/{game_id}", response_model=GameResponse)
def update_game_partial(
    game_id: UUID, game_data: GameUpdate, db: Annotated[Session, Depends(get_db)]
):

    result = db.execute(select(Game).where(Game.id == game_id))
    game = result.scalars().first()
    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Game not found"
        )

    update_data = game_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(game, field, value)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A game with this title and release date already exists.",
        )

    db.refresh(game)
    return game


@router.delete("/{game_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_game(game_id: UUID, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(Game).where(Game.id == game_id))
    game = result.scalars().first()
    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Game not found"
        )
    db.delete(game)
    db.commit()
