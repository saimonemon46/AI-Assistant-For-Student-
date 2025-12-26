from services.llm_service import get_llm

class ChatAgent:
    def __init__(self):
        self.llm = get_llm()

    def handle(self, content: str) -> str:
        response = self.llm.invoke([{"role": "user", "content": content}])
        return response.content
