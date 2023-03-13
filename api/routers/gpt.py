from fastapi import APIRouter

router = APIRouter()


@router.get("/gpt/recipes")
async def recipe_to_recipe(recipe):
    return {"message": "Get all users"}


@router.get("/gpt/{user_id}")
async def read_user(user_id: int):
    return {"message": f"Get user with id {user_id}"}


@router.post("/gpt")
async def create_user():
    return {"message": "Create a new user"}
