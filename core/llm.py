import requests
import json
import logging
import random
from openai import OpenAI
from prompt.base_prompt import SYSTEM_PROMPT

LOGGER = logging.getLogger(__name__)

class LLM:
    def __init__(self, api_key: str, base_url: str = "https://api.openai.com/v1"):
        self.api_key = api_key
        self.base_url = base_url
        self.temperature = 0.5
        self.model = "gpt-4o-mini"  
        self.system_prompt = SYSTEM_PROMPT
        self.client = OpenAI(api_key=api_key, base_url=base_url)

        
    def openai_chat(self, prompt, history):
        # 实现与OpenAI的交互
        try:
            client = OpenAI(
                api_key= self.api_key,
                base_url= self.base_url,
            )

            messages = self._join_messages(prompt, history)
            # messages = self._fix_messages(messages)

            if not messages:
                return

            LOGGER.info(f'  messages:\n\n\n {messages}')

    # stream = client.chat.completions.create(
    #     model="gpt-4o-mini",
    #     messages=[{"role": "user", "content": new_json_str}],
    #     stream=True,
    # )

            stream = client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                stream=True,
            )

            # LOGGER.info(f'  response:\n\n\n {completion.model_dump_json()}')

            # if completion.choices and len(completion.choices) > 0:
            #     return completion.choices[0].message.content
            # else:
            #     return f"[OpenAI] Error:{completion.error.message}"

            print(f"  stream: {stream}")

            return stream

        except Exception as e:
            LOGGER.error(f"[OpenAI] API 调用出错: {str(e)}")
            return f"错误: {str(e)}"

    def _join_messages(self, prompt, history):
        if self.system_prompt:
            messages = [
                {"role": "system", "content": self.system_prompt},
                *history,
                {"role": "user", "content": prompt},
            ]
        else:
            messages = [
                *history,
                {"role": "user", "content": prompt},
            ]

        return messages