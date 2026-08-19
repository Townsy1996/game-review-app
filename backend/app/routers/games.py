from typing import Annotated
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from app.database import get_db
from app.models import Game
from app.schemas import GameCreate, GameResponse, GameUpdate
from uuid import UUID

router = APIRouter(prefix="/games", tags=["Games"])


@router.post("/", response_model=GameResponse, status_code=status.HTTP_201_CREATED)
async def create_game(game: GameCreate, db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(
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
    await db.commit()
    await db.refresh(new_game)

    return new_game


@router.get("/", response_model=list[GameResponse])
async def get_all_games(db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(select(Game))
    games = result.scalars().all()
    return games


@router.get("/{game_id}", response_model=GameResponse)
async def get_game(game_id: UUID, db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(select(Game).where(Game.id == game_id))
    game = result.scalars().first()
    if game:
        return game
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Game not found")


@router.put("/{game_id}", response_model=GameResponse)
async def update_game_full(
    game_id: UUID, game_data: GameCreate, db: Annotated[AsyncSession, Depends(get_db)]
):
    result = await db.execute(select(Game).where(Game.id == game_id))
    game = result.scalars().first()
    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Game not found"
        )

    for key, value in game_data.model_dump().items():
        setattr(game, key, value)

    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A game with this title and release date already exists.",
        )
    await db.refresh(game)

    return game


@router.patch("/{game_id}", response_model=GameResponse)
async def update_game_partial(
    game_id: UUID, game_data: GameUpdate, db: Annotated[AsyncSession, Depends(get_db)]
):

    result = await db.execute(select(Game).where(Game.id == game_id))
    game = result.scalars().first()
    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Game not found"
        )

    update_data = game_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(game, field, value)

    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A game with this title and release date already exists.",
        )

    await db.refresh(game)
    return game


@router.delete("/{game_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_game(game_id: UUID, db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(select(Game).where(Game.id == game_id))
    game = result.scalars().first()
    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Game not found"
        )
    await db.delete(game)
    await db.commit()
