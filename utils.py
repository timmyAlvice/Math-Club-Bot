import os, re
# import os, requests, aiohttp
# from pydantic import BaseModel, parse_obj_as
# from typing import List, Dict, Tuple
# from aiogram import types

# TOKEN = os.getenv("GPN_CHATBOT_TOKEN")

WELCOME_MESSAGE = """Привет! 
Добро пожаловать в Math Club 

Скоро ты поймёшь, что подготовка к экзаменам может быть весёлой и интересной!
Выбери режим, чтобы начать:"""


ERROR_MESSAGE = "Что-то пошло не так..."


TEMPLATE = """СОВЕТЫ:

1. Совет 1
2. Совет 2
3. Совет 3
{hints}

==========

Похожие задачи:

1. Задача 1
2. Задача 2
3. Задача 3
{similar_tasks}

==========

Эталонное решение:

Решение задачи
{solving}"""


PROBLEM_MODE_MESSAGE = """Каждое правильно решённое задание даёт тебе 100 очков
Тебе нужно набрать 500, чтобы открыть тест по теме
Удачи!"""


TEST_MODE_MESSAGE = """Чтобы пройти тест тебе нужно ответить верно на 7 из 10 вопросов
Удачи!"""


PROFILE_MODE_MESSAGE = """{name}

Уровень 💪: Математический нубик
Очки 🎯: 1200
Дней до ЕГЭ 📅: 150

Пройденные задания ✍🏻:
1. Планиметрия 🔲
2. Векторы 🔲
3. Стереометрия 🔲
4. Начала теории вероятности 🔲
5. Вероятности сложных событий 🔲
6. Простейшие уравнения 🔲
7. Вычисления и преобразования 🔲
8. Производная и первообразная 🔲
9. Задачи с прикладным содержанием 🔲
10. Текстовые задачи 🔲
11. Графики функций 🔲
12. Наибольшее и наименьшее значение функций ✅

Достижания ⭐:
Достижение 1
Достижение 2
Достижение 3"""


INFO_MODE_MESSAGE = """Гайд по использованию"""
ABOUT_MESSAGE = """Информация о проекте и авторах"""


CHOOSE_TASK_MESSAGE = """Выбери номер задания:
1. Планиметрия
2. Векторы
3. Стереометрия
4. Начала теории вероятности
5. Вероятности сложных событий
6. Простейшие уравнения
7. Вычисления и преобразования
8. Производная и первообразная
9. Задачи с прикладным содержанием
10. Текстовые задачи
11. Графики функций
12. Наибольшее и наименьшее значение функций
"""

SYS_PROMPT = """
Ты учитель математики.
Тебе нужно сравнить решение задачи твоего ученика с эталонным.
Укажи на ошибки, если они есть. Если решение отсутствует сопоставь только ответ, ничего не пиши про решение.
А так же дай рекомендации по решению, которые будут полезны твоему ученику.
Вконце выдвени свой вердикт: верный ответ или не верный, верным ответом считается только полное совпадение ответа ученика с эталонным ответом.
Если ты ошибёшься в оценивании отввета, ученик может сильно постарадать, а ты как учитель получишь штраф 5000 рублей.
Все математические выражения должны быть хорошо читаемы в формате Markdown в Telegram

Строго следуй данному шаблону для обратной связи оценивания ученика:
[
- Ошибки: [Ошибка 1, Ошибка 2, Ошибка 3] (пропусти этот пункт, если нет ошибок или не представленно решение)
- Советы по решению: [Совет 1, Совет 2, Совет 3] (пропусти этот пункт, если не представленно решение)
- Ответ: [Верный / Не верный] (если ответ ученика полностью совпадает с эталонным решением, то ответ верный, иначе не верный)
]
"""

SYS_PROMPT = """
Ты учитель математики страшмх классов.  
Тебе нужно сравнить решение задачи твоего ученика с эталонным.  
Укажи на ошибки, если они есть. Если решение отсутствует, сопоставь только ответ, ничего не пиши про решение.  
Также дай рекомендации по решению, которые будут полезны твоему ученику.  
В конце выдвини свой вердикт: верный ответ или не верный. Верным ответом считается только полное совпадение ответа ученика с эталонным ответом.  
Если ты ошибёшься в оценивании ответа, ученик может сильно пострадать, а ты как учитель получишь штраф 5000 рублей.  
Все математические выражения должны быть хорошо читаемы в формате Markdown в Telegram.
Не в коем случае не экранируй символы!!! Это очень важно!
Если в ответе нет ошибок или решения пропусти ненужные пункты!
Строго следуй данному шаблону внутри квадратных скобок '[]' для обратной связи оценивания ученика:
[
***Ошибки:*** ⚠️
1. Ошибка 1
2. Ошибка 2
3. Ошибка 3

***Советы по решению:*** ✍️
1. Совет 1
2. Совет 2
3. Совет 3

***Ответ:*** ***ВЕРНЫЙ*** ✅ / ***НЕ ВЕРНЫЙ*** ❌
]
"""

COMPARE_LLM_PROMPT = """
Задача:
{problem}

Эталонное решение задачи:
[
{solution_explanation}

Ответ:
{answer}
]

Решение или ответ ученика:
[
{user_solution}
]
"""


test_12 = [
    {
        "question": "AgACAgIAAxkBAAIBS2bbhopsjZV40Qs-DOGU2EBfos2yAAJB6TEbBv7gSvMPhA2JUd02AQADAgADeAADNgQ",
        "answer": 1  # Индекс правильного ответа
    },
    {
        "question": "AgACAgIAAxkBAAIBTWbbhpRUBo5zfAQMDxEsTlYLt6bdAAJA6TEbBv7gSozKaxtdJETVAQADAgADeAADNgQ",
        "answer": 0
    },
    {
        "question": "AgACAgIAAxkBAAIBT2bbhprt3E-RefsAAQQsAUajfcnW5gACP-kxGwb-4EpIfXTi_o38RAEAAwIAA3gAAzYE",
        "answer": 0
    },
    {
        "question": "AgACAgIAAxkBAAIBUWbbhqqm9v-aIbFWE2bmnmTXrRoXAAJD6TEbBv7gSlx9nATNYQTcAQADAgADeAADNgQ",
        "answer": 0
    },
    {
        "question": "AgACAgIAAxkBAAIBU2bbhrWiD9chTZU9QRoQEvqe_u2bAAJC6TEbBv7gSrBJ4JKm6UDIAQADAgADeAADNgQ",
        "answer": 0
    },
    {
        "question": "AgACAgIAAxkBAAIBVWbbhr18DWDnOyCPKCQ_kT_gKeujAAI96TEbBv7gSiAuLd3_IJLNAQADAgADeAADNgQ",
        "answer": 2
    },
    {
        "question": "AgACAgIAAxkBAAIBV2bbhs38WJpQc0UmXPXRDsX1102VAAI-6TEbBv7gShCdwibzwR3yAQADAgADeAADNgQ",
        "answer": 1
    },
    {
        "question": "AgACAgIAAxkBAAIBWWbbhtlNdJ4sBHyEcinLoxcvtLzEAAI86TEbBv7gSjG5P2VCp9QiAQADAgADeAADNgQ",
        "answer": 0
    },
    {
        "question": "AgACAgIAAxkBAAIBXGbbhvh5gw98ekeKF2Tfpj7sQqorAAI66TEbBv7gSrqR-D3QvfQKAQADAgADeAADNgQ",
        "answer": 0
    },
    {
        "question": "AgACAgIAAxkBAAIBXmbbhwABuhhA2BNN3ASYISv-S9V_mgACO-kxGwb-4EopqUv5R2OVGQEAAwIAA3gAAzYE",
        "answer": 1
    },
]


OPTIONS = ["A", "B", "C", "D"]


async def get_response(text: str) -> str:
    return TEMPLATE.format(hints='', similar_tasks='', solving='')


def extract_text_in_brackets(text):
    # Используем регулярное выражение для поиска текста внутри квадратных скобок
    pattern = r'\[\s*([\s\S]*?)\s*\]'
    match = re.search(pattern, text)
    
    if match:
        # Возвращаем найденный текст, убирая лишние отступы
        result = match.group(1).strip()

        for i in "-.()[]=+-/":
            result = result.replace(i, f'\\{i}')

        result = result.replace(r'\\', '\\')

        return result
    
    else:
        return "Не сработал re в квадратных скобках"