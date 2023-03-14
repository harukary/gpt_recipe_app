from pydantic import BaseModel, create_model
import json

recipe_format = json.loads(open('config/recipe_format.json', 'r').read())
Recipe = create_model('Recipe', **recipe_format)