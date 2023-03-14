from chatgpt_client import ChatGPT

class RecipeChatGPT:
    def __init__(self,api_key) -> None:
        self.chatgpt = ChatGPT(api_key)
        self.recipe_importer = self.chatgpt.generate_model()
        self.support_ai = self.chatgpt.generate_model()
        self.dietitian = self.chatgpt.generate_model()
        self.recipe_format = open('data/recipe_format.json','r').read()

    def 