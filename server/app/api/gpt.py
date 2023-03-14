from fastapi import APIRouter, UploadFile
router = APIRouter()

from core.recipe_gpt import RecipeImporter
recipe_importer = RecipeImporter('config/recipe_format.json')

from models.gpt import RecipeText, RecipeJson, RecipeUrl
from models.recipes import Recipe

@router.post("/gpt/recipes/text_to_recipe")
async def text_to_recipe(data: RecipeText):
    return recipe_importer.text_to_recipe(data.text)

import shutil
IMG_DIR = 'database/images/'
@router.post("/gpt/recipes/img_to_recipe")
async def img_to_recipe(data: UploadFile):
    path = IMG_DIR + data.filename
    with open(path, 'wb+') as buffer:
        shutil.copyfileobj(data.file, buffer)
    return recipe_importer.image_to_recipe(path)

@router.post("/gpt/recipes/url_to_recipe")
async def url_to_recipe(data: RecipeUrl):
    return recipe_importer.url_to_recipe(data.url)

@router.post("/gpt/recipes/recipe_to_recipe")
async def recipe_to_recipe(data: RecipeJson):
    return recipe_importer.recipe_to_recipe(data.recipe_json)