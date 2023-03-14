from pydantic import BaseModel

class RecipeText(BaseModel):
    text: str

class RecipeJson(BaseModel):
    recipe_json: dict

class RecipeUrl(BaseModel):
    url: str