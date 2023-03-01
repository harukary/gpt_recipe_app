from fastapi import FastAPI

from app.routers import users, recipes, calendar

def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(users.router)
    # app.include_router(recipes.router)
    # app.include_router(calendar.router)
    return app

app = create_app()

@app.get("/")
def read_root():
    return {"RecipeGPT": "Running"}