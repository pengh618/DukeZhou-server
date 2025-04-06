from fastapi.routing import APIRouter
from fastapi import Request
from sse_starlette.sse import EventSourceResponse
from openai import OpenAI
from settings.config import settings
from core.llm import LLM
from dao.AgentDao import AgentDao

router = APIRouter()
api_key = settings.api_key
base_url = 'https://api.openai.com/v1'
@router.get("/generate")
async def generate_json(input: str):
    openai_llm = LLM(
        api_key=api_key,
        base_url=base_url,
    )

    dao = AgentDao()

    pt = await dao.get_prompt_by_code("dream")
    pt = pt.replace("{{input}}", input)

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

    stream =  openai_llm.openai_chat(
        prompt=pt,
        history=[],
    )

    return EventSourceResponse(
        (
            {"event": "message", "data": chunk.choices[0].delta.content}
            for chunk in stream
            if chunk.choices[0].delta.content is not None
        ),
        media_type="text/event-stream",
    )

