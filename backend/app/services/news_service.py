import requests
from services.llm_service import get_llm
from config.settings import YOUR_NEWSAPI_KEY

llm = get_llm()

def fetch_news(topic: str = "latest", limit: int = 5):
    url = "https://gnews.io/api/v4/search"
    params = {
        "q": topic,
        "lang": "en",
        "max": limit,
        "apikey": YOUR_NEWSAPI_KEY
    }

    response = requests.get(url, params=params, timeout=10)

    if response.status_code != 200:
        return []

    data = response.json()
    return data.get("articles", [])


def summarize_news(articles):
    if not articles:
        return "No relevant news found at the moment."

    combined_text = "\n\n".join(
        f"Title: {a.get('title', 'No title')}\n"
        f"Description: {a.get('description', '')}"
        for a in articles
    )

    prompt = (
        "Summarize the following news for a student.\n"
        "Use simple language.\n"
        "Highlight facts useful for exams.\n\n"
        f"{combined_text}"
    )

    response = llm.invoke([
        {"role": "user", "content": prompt}
    ])

    return response.content
