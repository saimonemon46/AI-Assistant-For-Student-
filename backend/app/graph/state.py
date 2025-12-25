from typing import TypedDict, List

class State(TypedDict):
    messages: List[dict]
    file_type: str
    content: str
