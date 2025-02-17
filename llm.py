import os, asyncio
from langchain_community.chat_models.gigachat import GigaChat


SBER_TOKEN = os.getenv("SBER_TOKEN")

class LLM:
    
    def __init__(self):
        
        self.llm = GigaChat(
            credentials=SBER_TOKEN, 
            model="GigaChat-Pro",
            # temperature=
            verify_ssl_certs=False
        )
        
        
    async def generate_text(self, prompt: str) -> str:
        return self.llm.invoke(prompt).content


giga_llm = LLM()