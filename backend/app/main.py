from fastapi import FastAPI
from app import models
from app.database import engine
from app.routers import games, users, reviews

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Game Vault API")
app.include_router(games.router)
app.include_router(users.router)
app.include_router(reviews.router)
