"""
使用openai的gpt模型
"""

import json
from typing import Any, Iterable, Union, cast, overload, Literal

from openai import OpenAI, Stream
from openai.types.chat import (ChatCompletionChunk, ChatCompletionMessageParam,
                               ChatCompletion)
from openai.types.shared import ChatModel

from .messages import ChatCompletionMessages


class ChatBot:

    def __init__(self) -> None:
        self.client = OpenAI()

    @overload
    def ask(
        self,
        prompt: Iterable[ChatCompletionMessages],
        model: ChatModel,
        temperature: float,
        stream: Literal[True],
        **kwargs: Any,
    ) -> Iterable[str]:
        ...

    @overload
    def ask(
        self,
        prompt: Iterable[ChatCompletionMessages],
        model: ChatModel,
        temperature: float,
        stream: Literal[False],
        **kwargs: Any,
    ) -> str:
        ...

    def ask(
        self,
        prompt: Iterable[ChatCompletionMessages],
        model: ChatModel,
        temperature: float = 0,
        stream: bool = False,
        **kwargs: Any,
    ) -> Union[str, Iterable[str]]:
        completion = self.client.chat.completions.create(
            model=model,
            messages=cast(Iterable[ChatCompletionMessageParam],
                          map(dict, prompt)),
            temperature=temperature,
            stream=stream,
            **kwargs,
        )
        if isinstance(completion, Stream):
            # return completion
            return self.stream_to_str(completion)

        assert isinstance(completion, ChatCompletion)
        return completion.choices[0].message.model_dump().get(
            "content", "error")

    # stream 解包成 iterable[str]
    @staticmethod
    def stream_to_str(stream: Stream[ChatCompletionChunk]) -> Iterable[str]:
        for chunk in stream:
            # yield chunk.choices[0].model_dump().get("content", "error")
            yield chunk.choices[0].delta.content or ""
