from fastapi import FastAPI

app = FastAPI()

from app.routers import users, recipes, calendar

app.include_router(users.router)
# app.include_router(recipes.router)
# app.include_router(calendar.router)