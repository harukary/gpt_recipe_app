import openai; openai.api_key = open('../../open_ai.key', 'r').read()
import tiktoken

class ChatGPT:
    def __init__(self,max_tokens=150,temperature=0.9,setting=''):
        self.enc = tiktoken.get_encoding("gpt2")

        self.max_tokens = max_tokens
        self.temperature = temperature
        self.setting = setting
        self.setting_tokens = len(self.enc.encode(setting))

        self.past_messages = []

    
    def complete(self,messages):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
        )
        return response.choices[0].message.content

    def filter_messages(self,messages):
        tokens = self.setting_tokens
        for i,m in enumerate(reversed(messages)):
            tokens += len(self.enc.encode(m['content']))
            if tokens > self.MAX_TOKEN - self.max_tokens:
                print('burst:',tokens)
                return messages[-i:]
        return messages
    
    def chat(self,message):
        messages = []
        if len(self.setting) != 0:
            messages.append({"role": "system", "content": self.setting})
        new_message = {"role": "user", "content": message}
        self.past_messages.append(new_message)
        messages += self.filter_messages(self.past_messages)
        response = self.complete(messages)
        return response