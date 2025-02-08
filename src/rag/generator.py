from openai import AsyncOpenAI
from config.keys import OPENAI_API_KEY, TOGETHER_API_KEY
from config.models import OPENAI_MODEL, TOGETHER_MODEL
from together import Together


class Generator:
    def __init__(self):
        # self.client = AsyncOpenAI(api_key=OPENAI_API_KEY)
        self.client = Together(api_key=TOGETHER_API_KEY)

    async def generate_answer(self, question: str, context: str) -> str:
        prompt = f"""
        Ты медицинский ассистент под названием Trauma. Отвечай строго на основе контекста.
        Если информации недостаточно, то скажи "Я не могу дать точный ответ"
        
        Контекст: {context}
        
        Вопрос: {question}
        Ответ:
        """

        response = self.client.chat.completions.create(
            model=TOGETHER_MODEL,
            messages=[{'role': 'user', 'content': prompt}],
            temperature=0.7,
            max_tokens=1024
        )

        return response.choices[0].message.content
