import os, asyncio
from openai import OpenAI
from utils import SYS_PROMPT


SBER_TOKEN = os.getenv("SBER_TOKEN")
DEEP_SEEK_TOKEN = os.getenv("DEEP_SEEK_TOKEN")


class LLM:

    def __init__(self):
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=DEEP_SEEK_TOKEN,
        )

    async def generate_text(self, prompt: str) -> str:
        # Системный промт

        completion = self.client.chat.completions.create(
            model="deepseek/deepseek-r1-distill-llama-70b:free",
            messages=[
                {
                    "role": "system",
                    "content": SYS_PROMPT
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ], 
            temperature=0.3,  # Настройка температуры для более предсказуемых ответов
        )
        return completion.choices[0].message.content

giga_llm = LLM()