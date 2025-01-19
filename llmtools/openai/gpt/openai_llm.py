"""
使用openai的gpt模型
"""

import json
from typing import Any, Iterable, Literal, cast, Union

from openai import OpenAI, Stream
from openai.types.chat import (
    ChatCompletionChunk,
    ChatCompletionMessageParam,
    ChatCompletionToolChoiceOptionParam,
)

from .messages import ChatCompletionMessages
from collections import defaultdict

defaultmodeltypes = Literal["gpt4", "gpt4v", "gpt3", "gpt4o"]

modelmap = defaultdict(lambda key: key, {
    "gpt4": "gpt-4",
    "gpt4v": "gpt-4-0125-preview",
    "gpt3": "gpt-3.5-turbo-0125",
    "gpt4o": "gpt-4o-2024-05-13",
})

modeltype = Union[defaultmodeltypes , str]

class LLM:
    def __init__(self) -> None:
        self.client = OpenAI()

    def ask(
        self,
        prompt: Iterable[ChatCompletionMessages],
        model: modeltype,
        temperature: float = 0,
        stream: bool = False,
    ) -> str | Stream[ChatCompletionChunk]:
        completion = self.client.chat.completions.create(
            model=modelmap[model],
            messages=cast(Iterable[ChatCompletionMessageParam], map(dict, prompt)),
            temperature=temperature,
            stream=stream,
        )
        if stream or isinstance(completion, Stream):
            return completion
        return completion.choices[0].message.model_dump().get("content", "error")

    def ask_tools(
        self,
        prompt: str,
        model: modeltype,
        tools: Iterable[Any],
        tool_choice: ChatCompletionToolChoiceOptionParam,
        temperature: float = 0,
        stream: bool = False,
    ) -> str | list[dict[str, Any]] | Stream[ChatCompletionChunk]:
        completion = self.client.chat.completions.create(
            model=modelmap[model],
            messages=[{"role": "system", "content": prompt}],
            tools=tools,
            tool_choice=tool_choice,
            temperature=temperature,
            stream=stream,
        )
        # 如果是stream就直接回傳
        if stream or isinstance(completion, Stream):
            return completion
        # 一般response如果是content就回傳content
        if completion.choices[0].model_dump()["message"]["content"] is not None:
            return completion.choices[0].model_dump()["message"]["content"]
        # 最後就只剩下tool call, 返回list[dict] ,每個 dict 有 name 跟 arguments
        return [
            {
                "name": tool_call["function"]["name"],
                "arguments": json.loads(tool_call["function"]["arguments"]),
            }
            for tool_call in completion.choices[0].model_dump()["message"]["tool_calls"]
        ]
