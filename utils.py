import os, requests, aiohttp
from pydantic import BaseModel, parse_obj_as
from typing import List, Dict, Tuple

TOKEN = os.getenv('GPN_CHATBOT_TOKEN')
# URL = os.getenv('GPN_API_URL')

WELCOME_MESSAGE = """Привет! 
Добро пожаловать в Math Club 

Скоро ты поймёшь, что подготовка к экзаменам может быть весёлой и интересной!
Выбери режим, чтобы начать:"""

# FEEDBACK_MESSAGE = "Пожалуйста, оцените качество ответа виртуального ассистента!"

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

class DocumentProvisionReference(BaseModel):
    content: str
    meta: Dict[str, str]


class ComplexQueryAnswerResponse(BaseModel):
    question: str
    answer: str
    sources: str
    provisions: List[DocumentProvisionReference]


class StringListResponse(BaseModel):
    response: List[str]
    
    
# async def query_docs_async(body, template_id=1) -> ComplexQueryAnswerResponse:
#     url = f"{URL}/api/docs/query/{template_id}"
#     headers = {"Content-Type": "text/plain"}
    
#     async with aiohttp.ClientSession() as session:
#         async with session.post(url, data=body, headers=headers) as response:
            
#             if response.status == 200:
#                 resp_json = await response.json()
#                 return ComplexQueryAnswerResponse.parse_obj(resp_json)
#             else:
#                 raise Exception(f"Failed with status code {response.status}")
            

# async def find_doc_provisions(body) -> StringListResponse:
#     url = f"{URL}/api/docs/provisions"
#     headers = {"Content-Type": "text/plain"}
    
#     async with aiohttp.ClientSession() as session:
#         async with session.post(url, data=body, headers=headers) as response:
            
#             if response.status == 200:
#                 resp_json = await response.json()
#                 return StringListResponse.parse_obj(resp_json)
#             else:
#                 raise Exception(f"Failed with status code {response.status}")


def parse_provisions(provisions: DocumentProvisionReference) -> Tuple[str, Tuple]:
    contents = set()
    metas = set()
    
    for i in provisions:
        meta = ", ".join(i.meta.values())
        content_text = i.content
        content = ":\n".join([meta, content_text])
        metas.update([meta])
        contents.update([content])
        
    meta = "\n".join(metas)
    return meta, tuple(contents)
          

def parse_model_response(response: ComplexQueryAnswerResponse) -> Tuple[str, Tuple]:
    
    question = response.question
    answer = response.answer
    provisions = response.provisions
    
    meta, contents = parse_provisions(provisions)
    model_answer = TEMPLATE.format(question=question, meta=meta, answer=answer)
    
    return model_answer, tuple(contents)


def parse_docs_response(provisions: StringListResponse) -> Tuple:
    return tuple(provisions.response)


# async def get_model_response_from_api(text: str) -> Tuple[str, Tuple]:
#     body = text.strip('\'"')
#     response = await query_docs_async(body)
#     return parse_model_response(response)


# async def get_docs_from_api(text: str) -> Tuple:
#     body = text.strip('\'"')
#     provisions = await find_doc_provisions(body)
#     print(provisions)
#     return parse_docs_response(provisions)

async def get_response(text: str) -> Tuple[str, Tuple]:
    return TEMPLATE.format(hints='', similar_tasks='', solving='')