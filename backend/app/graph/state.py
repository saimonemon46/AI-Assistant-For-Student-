from typing import TypedDict, List, Literal, Optional

class Message(TypedDict):
    role: Literal["user", "assistant", "system"]
    content: str

class State(TypedDict):
    messages: List[Message]
    file_type: Literal["", "pdf", "image"]
    content: str
