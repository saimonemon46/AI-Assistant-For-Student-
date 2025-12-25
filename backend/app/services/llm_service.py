from langchain_groq import ChatGroq
from app.config.settings import GROQ_API_KEY, GROQ_MODEL

def get_llm():
    return ChatGroq(
        groq_api_key=GROQ_API_KEY,
        model_name=GROQ_MODEL
    )
