from services.llm_service import get_llm
from services.news_service import fetch_news, summarize_news

class NewsAgent:
    def __init__(self):
        self.llm = get_llm()

    def handle(self, topic: str) -> str:
        articles = fetch_news(topic)
        summary = summarize_news(articles)
        return summary
