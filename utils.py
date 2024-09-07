import os, requests, aiohttp
from pydantic import BaseModel, parse_obj_as
from typing import List, Dict, Tuple
from aiogram import types

TOKEN = os.getenv('GPN_CHATBOT_TOKEN')


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


INFO_MODE_MESSAGE = """Тут будет длинное и подробно описание..."""


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