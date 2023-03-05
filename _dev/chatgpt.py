import openai
import tiktoken

class ChatGPT:
    MAX_TOKEN = 4097
    def __init__(self,api_key,max_tokens=512,setting='') -> None:
        openai.api_key = api_key
        self.max_tokens = max_tokens
        self.setting = setting
        self.enc = tiktoken.get_encoding("gpt2")

    def chat(self,message,past_messages=[]):
        chat_history = self.organize_memory(message,past_messages)
        if len(chat_history) == 0:
            return 'SYSTEM: Too much input', []
        result = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=chat_history,
            max_tokens = self.max_tokens
        )
        response_message = {"role": "assistant", "content": result.choices[0].message.content}
        chat_history.append(response_message)
        response_message_text = result.choices[0].message.content
        return response_message_text, chat_history

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
                print('burst:',tokens)
                return past_messages[-i:]
        return past_messages
