#!/usr/bin/env python
from fastapi.routing import APIRouter
from settings.config import settings
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI
import json

router = APIRouter()

# 定义期望的数据结构
class Result(BaseModel):
    result: str = Field(description="在这里提供梦境的解释和意义")
    intro: str = Field(description="在这里简要介绍梦境的背景和情节")
    summary: str = Field(description="在这里总结梦境中的主要情节和感受")
    关键符号: dict = Field(description="在这里提供梦境中重要的符号和关键词")
    latent_meaning: str = Field(
        description="在这里探讨梦境中可能隐藏的深层含义和象征意义"
    )
    conclusion: str = Field(description="在这里总结梦境的主要内容和结局")

@router.post("/generate_json")
async def generate_json(input: str):
    client = ChatOpenAI(
        api_key=settings.api_key,
        model="gpt-4o-mini",
        temperature=0.8,
    )
    # 设置解析器并注入指令到提示模板中
    parser = JsonOutputParser(pydantic_object=Result)

    prompt = PromptTemplate(
        template="请解释下面的梦境.{query}\n{format_instructions}\n",
        input_variables=["query"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )
    chain = prompt | client | parser
    result = chain.invoke({"query": input})
    return result


@router.post("/generate")
async def generate(input: str):
    from openai import OpenAI
    try:
        client = OpenAI(api_key=settings.api_key, base_url=settings.api_base)
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
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a creative AI."},
                {"role": "user", "content": new_json_str},
            ],
            temperature=0.8,
        )
        result = response.choices[0].message.content.strip()[7:-3]
        # Parse the response content as JSON
        parsed_result = json.loads(result)
        return parsed_result
    except Exception as e:
        return {"异常": str(e)}
        