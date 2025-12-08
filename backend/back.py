import os

from dotenv import load_dotenv
from typing import Annotated, TypedDict

from langchain_groq import ChatGroq

from langgraph.graph import START, END, StateGraph



## Load Env ##
load_dotenv()


## LLM ##
llm = ChatGroq(
    groq_api_key = os.getenv("GROQ_API_KEY"),
    model_name="openai/gpt-oss-20b"      
)

## Check llm
print(llm.invoke("how are you").content)
