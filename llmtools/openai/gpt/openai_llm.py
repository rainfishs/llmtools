"""
使用 Openai 的 GPT 模型
"""

from typing import Any, Iterable, Union, overload, Literal

from openai import OpenAI, Stream
from openai.types.chat import ChatCompletionChunk
from openai.types.shared import ChatModel

from .messages import ChatCompletionMessages


class ChatBot(OpenAI):

    @overload
    def ask(
        self,
        prompt: Iterable[ChatCompletionMessages],
        model: ChatModel | str,
        *,
        stream: Literal[True],
        **kwargs: Any,
    ) -> Iterable[str]:
        ...

    @overload
    def ask(
        self,
        prompt: Iterable[ChatCompletionMessages],
        model: ChatModel | str,
        *,
        stream: Literal[False] = False,
        **kwargs: Any,
    ) -> str:
        ...

    def ask(
        self,
        prompt: Iterable[ChatCompletionMessages],
        model: ChatModel | str,
        stream: bool = False,
        **kwargs: Any,
    ) -> Union[str, Iterable[str]]:
        kwargs["model"] = model
        kwargs["messages"] = map(dict, prompt)
        if stream:
            return self.stream_to_str(
                self.chat.completions.create(stream=stream, **kwargs))
        else:
            return (self.chat.completions.create(
                stream=stream,
                **kwargs,
            )).choices[0].message.model_dump().get("content", "error")

    # stream 解包成 iterable[str]
    @staticmethod
    def stream_to_str(stream: Stream[ChatCompletionChunk]) -> Iterable[str]:
        for chunk in stream:
            yield chunk.choices[0].delta.content or ""
