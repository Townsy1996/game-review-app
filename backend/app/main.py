from fastapi import FastAPI
from app.database import engine, Base
from app.routers import games, users, reviews
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(_app: FastAPI):
    # Startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown

    await engine.dispose()


app = FastAPI(title="Game Vault API", lifespan=lifespan)
app.include_router(games.router)
app.include_router(users.router)
app.include_router(reviews.router)
