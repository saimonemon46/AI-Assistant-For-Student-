import os

from dotenv import load_dotenv
from typing import Annotated, TypedDict

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

from langgraph.graph import START, END, StateGraph



## Load Env ##
load_dotenv()


## LLM ##
llm = ChatGroq(
    groq_api_key = os.getenv("GROQ_API_KEY"),
    model_name="openai/gpt-oss-20b"      
)

# ## Check llm
# print(llm.invoke("how are you").content)

##### Chat Function ######
def generate_response(input : str):
    # user input as HumanMessage
    messages = [HumanMessage(content=input)]
    response = llm.invoke(messages)
    return response.content

##### Test Chat Function ######
if __name__ == "__main__":
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit', 'bye']:
            break
        response = generate_response(user_input)
        print("AI:", response)