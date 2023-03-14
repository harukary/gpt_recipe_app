from fastapi import FastAPI

from api.gpt import router as recipe_gpt

def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(recipe_gpt)
    return app

app = create_app()

@app.get("/")
def read_root():
    return {"GPTRecipesApp": "Running"}