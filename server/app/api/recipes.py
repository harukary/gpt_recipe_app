from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

app = FastAPI()

# SQLiteデータベースの初期化
conn = sqlite3.connect("recipes.db")
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS recipes (
                  id INTEGER PRIMARY KEY,
                  name TEXT NOT NULL,
                  description TEXT NOT NULL,
                  ingredients TEXT NOT NULL,
                  instructions TEXT NOT NULL
                )""")
conn.commit()
conn.close()


# レシピのモデル
class Recipe(BaseModel):
    name: str
    description: str
    ingredients: str
    instructions: str


# レシピのCRUD
@app.post("/recipes")
def create_recipe(recipe: Recipe):
    conn = sqlite3.connect("recipes.db")
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO recipes (name, description, ingredients, instructions)
                      VALUES (?, ?, ?, ?)""",
                   (recipe.name, recipe.description, recipe.ingredients, recipe.instructions))
    conn.commit()
    recipe_id = cursor.lastrowid
    conn.close()
    return {"id": recipe_id, **recipe.dict()}


@app.get("/recipes/{recipe_id}")
def read_recipe(recipe_id: int):
    conn = sqlite3.connect("recipes.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM recipes WHERE id = ?", (recipe_id,))
    recipe = cursor.fetchone()
    conn.close()
    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return {"id": recipe[0], "name": recipe[1], "description": recipe[2],
            "ingredients": recipe[3], "instructions": recipe[4]}


@app.get("/recipes")
def read_recipes():
    conn = sqlite3.connect("recipes.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM recipes")
    recipes = cursor.fetchall()
    conn.close()
    return [{"id": recipe[0], "name": recipe[1], "description": recipe[2],
             "ingredients": recipe[3], "instructions": recipe[4]} for recipe in recipes]


@app.put("/recipes/{recipe_id}")
def update_recipe(recipe_id: int, recipe: Recipe):
    conn = sqlite3.connect("recipes.db")
    cursor = conn.cursor()
    cursor.execute("""UPDATE recipes SET name = ?, description = ?, ingredients = ?, instructions = ?
                      WHERE id = ?""",
                   (recipe.name, recipe.description, recipe.ingredients, recipe.instructions, recipe_id))
    conn.commit()
    conn.close()
    return {"id": recipe_id, **recipe.dict()}


@app.delete("/recipes/{recipe_id}")
def delete_recipe(recipe_id: int):
    conn = sqlite3.connect("recipes.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM recipes WHERE id = ?", (recipe_id,))
    conn.commit()
    conn.close()
    return {"message": "Recipe deleted successfully"}

