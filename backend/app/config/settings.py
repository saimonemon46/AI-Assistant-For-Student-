import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "openai/gpt-oss-20b"
YOUR_NEWSAPI_KEY = os.getenv("NEWS_API_KEY")
