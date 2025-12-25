import requests
from services.llm_service import get_llm
from config.settings import YOUR_NEWSAPI_KEY

llm = get_llm()
NEWS_API_KEY = YOUR_NEWSAPI_KEY  # register free account

def fetch_news(topic: str = "latest", limit: int = 5):
    url = "https://gnews.io/api/v4/search"
    params = {
        "q": topic,
        "lang": "en",
        "max": 5,
        "apikey": NEWS_API_KEY
    }


    response = requests.get(url, params=params)
    data = response.json()
    articles = data.get("articles", [])
    return articles

def summarize_news(articles):
    if not articles:
        return "No news found."

    combined_text = "\n".join([f"Title: {a['title']}\nDescription: {a['description'] or ''}" for a in articles])
    
    prompt = f"Summarize these news articles in simple terms for a student:\n\n{combined_text}"
    response = llm.invoke([{"role": "user", "content": prompt}])
    return response.content
