from fastapi.routing import APIRouter
from fastapi import Request
from sse_starlette.sse import EventSourceResponse
from openai import OpenAI
from settings.config import settings
from core.llm import LLM
from dao.AgentDao import AgentDao  # Ensure AgentDao supports async methods

router = APIRouter()
api_key = settings.api_key
openrouter_key = settings.openrouter_key

base_url = 'https://api.openai.com/v1'
openrouter_api_url = 'https://openrouter.ai/api/v1'

openai_llm = LLM(
    api_key=api_key,
    base_url=base_url,
)

deppseek_llm = LLM( 
    api_key=openrouter_key,
    base_url=openrouter_api_url,
    model="deepseek/deepseek-chat-v3-0324:free"
)

@router.get("/generate_json")
async def generate_json(code:str, input: str):

    async def generate_data(input: str):
        dao = AgentDao()
        prompt = await dao.get_prompt_by_code(code)
        print(prompt)
        prompt = prompt.replace("{{input}}", input)

        stream =  openai_llm.openai_chat(
            prompt=prompt,
            history=[],
        )

        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content
        yield "[DONE]"

    return EventSourceResponse(
        generate_data(input),
        media_type="text/event-stream",
    )

@router.get("/items/")
async def read_items(request: Request):
    for key, value in request.query_params.items():
        print(f"{key}: {value}")
    name = request.query_params.get("code")
    if name is None:
        name = "default_name"  # 动态设置默认值
    return {"name": name}

@router.get("/generate_md")
async def generate_md(request: Request):
    code = request.query_params.get("code")

    async def generate_data(input: str):
        dao = AgentDao()
        prompt = await dao.get_prompt_by_code(code)
        print(prompt)
        # prompt = prompt.replace("{{input}}", input)
        for key, value in request.query_params.items():        
            prompt = prompt.replace(f"{{{key}}}", value)
            print(f"{key}: {value}")

        print(prompt)

        stream =  deppseek_llm.openai_chat(
            prompt=prompt,
            history=[],
        )

        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content
        yield "[DONE]"

    return EventSourceResponse(
        generate_data(input),
        media_type="text/event-stream",
    )

# json_str = """
#     {
#         "梦境解读结果": "在这里提供梦境的解释和意义",
#         "简介": "在这里简要介绍梦境的背景和情节",
#         "概述": "在这里总结梦境中的主要情节和感受",
#         "关键符号": {
#             "符号1": "解释和意义",
#             "符号2": "解释和意义",
#             "符号3": "解释和意义"
#         },
#         "潜在意义": "在这里探讨梦境中可能隐藏的深层含义和象征意义",
#         "总结": "在这里总结梦境解读的要点和结论"
#     }
#     """
# propmt = (
#     "请解释以下梦的内容:" + input + "，按如下格式组织json字符串:" + agent.propmt
# )