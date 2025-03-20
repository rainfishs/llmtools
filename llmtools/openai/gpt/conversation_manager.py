import inspect
from typing import Any, Iterable, List, Literal, overload
from .messages import ChatCompletionMessages, UserMessage, AssistantMessage
from .openai_llm import ChatBot
from openai.types.shared import ChatModel
import functools


class ConversationManager():

    def __init__(self, bot: ChatBot, model: ChatModel | str):
        self.bot = bot
        self.model = model
        self.history: List[ChatCompletionMessages] = []

    def rollback_messages(self, n: int = 2):
        self.history = self.history[:-n]

    def get_last_message(self) -> ChatCompletionMessages:
        return self.history[-1]

    def get_history(self) -> List[ChatCompletionMessages]:
        return self.history

    def clear_history(self):
        self.history = []

    @overload
    def __call__(self,
                 input: str,
                 stream: Literal[False] = False,
                 **kwargs: Any) -> str:
        ...

    @overload
    def __call__(self, input: str, stream: Literal[True],
                 **kwargs: Any) -> Iterable[str]:
        ...

    def __call__(self,
                 input: str,
                 stream: bool = False,
                 **kwargs: Any) -> str | Iterable[str]:
        self.history.append(UserMessage(content=input))
        if stream:
            response = self.bot.ask(self.history,
                                    model=self.model,
                                    stream=True,
                                    **kwargs)
            response = self.interceptsteam(response)
            return response
        response = self.bot.ask(self.history, model=self.model)
        self.history.append(AssistantMessage(content=response))
        return response

    #類似的生成器包裝，用來攔截 yield 的值 加入到對話歷史中
    def interceptsteam(self, stream: Iterable[str]) -> Iterable[str]:
        response = ""
        for text in stream:
            if text == "":
                continue
            response += text
            yield text
        self.history.append(AssistantMessage(content=response))
