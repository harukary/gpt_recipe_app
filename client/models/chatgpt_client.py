import openai
import tiktoken

class ChatGPT:
    MAX_TOKEN = 4097
    def __init__(self,api_key,reply_tokens=512,setting='') -> None:
        openai.api_key = api_key
        self.reply_tokens = reply_tokens
        self.setting = setting
        self.enc = tiktoken.get_encoding("gpt2")
        self.past_messages = []

    def chat(self,message):
        input_history = self.organize_memory(message,self.past_messages)
        if len(input_history) == 0:
            return 'SYSTEM: Too much input', []
        result = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=input_history,
            max_tokens = self.reply_tokens
        )
        response_message = {"role": "assistant", "content": result.choices[0].message.content}
        self.past_messages.append(response_message)
        response_message_text = result.choices[0].message.content
        return response_message_text, input_history

    def organize_memory(self,message,past_messages):
        if len(past_messages) == 0 and len(self.setting) != 0:
            system = {"role": "system", "content": self.setting}
            past_messages.append(system)
        new_message = {"role": "user", "content": message}
        past_messages.append(new_message)
        tokens = 0
        for i,m in enumerate(reversed(past_messages)):
            tokens += len(self.enc.encode(m['content']))
            if tokens > self.MAX_TOKEN - self.max_tokens:
                # print('burst:',tokens)
                return past_messages[-i:]
        return past_messages
