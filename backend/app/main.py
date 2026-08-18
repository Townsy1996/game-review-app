from fastapi import FastAPI
from app import models
from app.database import engine
from app.routers import games, users

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Game Vault API")
app.include_router(games.router)
app.include_router(users.router)
