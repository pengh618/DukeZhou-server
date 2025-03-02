from fastapi.routing import APIRouter
from fastapi import Request
from sse_starlette.sse import EventSourceResponse
import asyncio
from openai import OpenAI
from httpx import AsyncClient
import os

router = APIRouter()
api_key = os.getenv("OPENAI_API_KEY")

@router.get("/")
async def root(request: Request):
    g = event_generator(request)
    return EventSourceResponse(g)

async def event_generator(request: Request):
    res_str = "梦境解读结果"
    for i in res_str:
        if await request.is_disconnected():
            print("连接已中断")
            break
        yield {"event": "message", "retry": 15000, "data": i}
        await asyncio.sleep(0.2)


@router.get("/generate")
async def generate_json(input: str):
    client = OpenAI(api_key=api_key, base_url="https://api.openai.com/v1")
    json_str = """
        {
            "梦境解读结果": "在这里提供梦境的解释和意义",
            "简介": "在这里简要介绍梦境的背景和情节",
            "概述": "在这里总结梦境中的主要情节和感受",
            "关键符号": {
                "符号1": "解释和意义",
                "符号2": "解释和意义",
                "符号3": "解释和意义"
            },
            "潜在意义": "在这里探讨梦境中可能隐藏的深层含义和象征意义",
            "总结": "在这里总结梦境解读的要点和结论"
        }
        """
    new_json_str = (
        "请解释以下梦的内容:" + input + "，按如下格式组织json字符串:" + json_str
    )

    stream = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": new_json_str}],
        stream=True,
    )

    return EventSourceResponse(
        (
            {"event": "message", "data": chunk.choices[0].delta.content}
            for chunk in stream
            if chunk.choices[0].delta.content is not None
        ),
        media_type="text/event-stream",
    )

