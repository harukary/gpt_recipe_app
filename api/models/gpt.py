import openai
openai.api_key = open('../../opem_ai.key', 'r').read()

from .recipes import Recipe

class RecipeGPT:
    def __init__(self) -> None:
        pass

