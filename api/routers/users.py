from fastapi import APIRouter

router = APIRouter()


@router.get("/users")
async def read_users():
    return {"message": "Get all users"}


@router.get("/users/{user_id}")
async def read_user(user_id: int):
    return {"message": f"Get user with id {user_id}"}


@router.post("/users")
async def create_user():
    return {"message": "Create a new user"}
