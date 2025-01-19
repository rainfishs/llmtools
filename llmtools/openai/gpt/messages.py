from typing import Iterable, Union

from openai.types.chat import ChatCompletionMessageToolCallParam


class _MessageToParam:
    def __iter__(self):
        for key, value in self.__dict__.items():
            if value is not None:
                yield key, value

    def __repr__(self):
        return f"{self.__class__.__name__}({', '.join(f'{key}={value!r}' for key, value in self)})"


class SystemMessage(_MessageToParam):
    def __init__(self, content: str, name: str | None = None):
        self.role = "system"
        self.content = content
        self.name = name


class UserMessage(_MessageToParam):
    def __init__(self, content: str, name: str | None = None):
        self.role = "user"
        self.content = content
        self.name = name


class AssistantMessage(_MessageToParam):
    def __init__(
        self,
        content: str | None = None,
        name: str | None = None,
        tool_calls: Iterable[ChatCompletionMessageToolCallParam] | None = None,
    ):
        self.role = "assistant"
        self.content = content
        self.name = name
        self.tool_calls = tool_calls


class ToolMessage(_MessageToParam):
    def __init__(self, content: str, tool_call_id: str):
        self.role = "tool"
        self.content = content
        self.tool_call_id = tool_call_id


ChatCompletionMessages = Union[
    SystemMessage,
    UserMessage,
    AssistantMessage,
    ToolMessage,
]
