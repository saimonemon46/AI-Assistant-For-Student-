import os
import mimetypes

from PIL import Image
import pytesseract

from dotenv import load_dotenv
from typing import TypedDict, List

from langchain_groq import ChatGroq
from langchain_community.document_loaders import PyPDFLoader
from langgraph.graph import START, END, StateGraph

## Load environment ##
load_dotenv()

## Initialize LLM ##
llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="openai/gpt-oss-20b"
)

# -----------------------------
# Define state structure
# -----------------------------
class State(TypedDict):
    messages: List[dict]
    file_type: str
    content: str

# -----------------------------
# Node: Detect file type
# -----------------------------
def detect_file_node(state: State):
    last_message = state['messages'][-1]

    # If message contains a file path
    if "file_path" in last_message:
        file_path = last_message["file_path"]
        mime, _ = mimetypes.guess_type(file_path)

        if mime is None:
            raise ValueError("Cannot detect file type")

        if "pdf" in mime:
            state["file_type"] = "pdf"
        elif "image" in mime:
            state["file_type"] = "image"
        else:
            raise ValueError(f"Unsupported file type: {mime}")

        state["content"] = file_path
    else:
        # Normal text
        state["file_type"] = "text"
        state["content"] = last_message["content"]

    return state

# -----------------------------
# Node: PDF extractor
# -----------------------------
def pdf_extractor_node(state: State):
    pdf_path = state["content"]
    loader = PyPDFLoader(pdf_path)

    # Correct way to get all pages as text
    documents = loader.load()  # returns list of Document objects
    text = "".join(doc.page_content for doc in documents)

    state["content"] = text
    return state

# -----------------------------
# Node: image extractor
# -----------------------------
def image_extractor_node(state: State):
    path = state["content"]
    # Extract text from the image
    text = pytesseract.image_to_string(Image.open(path))
    if not text.strip():
        text = "[No text detected in the image]"
    
    state["content"] = text
    return state

# -----------------------------
# Node: Chat LLM
# -----------------------------
def chat_node(state: State):
    user_content = state.get("content", "")
    msgs = [{"role": "user", "content": user_content}]
    response = llm.invoke(msgs)
    state["messages"].append({"role": "assistant", "content": response.content})
    return state

# -----------------------------
# Build LangGraph
# -----------------------------
graph = StateGraph(State)

graph.add_node("detect_file_node", detect_file_node)
graph.add_node("pdf_extractor_node", pdf_extractor_node)
graph.add_node("image_extractor_node", image_extractor_node)
graph.add_node("chat_node", chat_node)

graph.add_edge(START, "detect_file_node")

# Conditional routing
graph.add_conditional_edges(
    "detect_file_node",
    lambda s: 
        "pdf_extractor_node" if s["file_type"] == "pdf"
        else "image_extractor_node" if s["file_type"] == "image"
        else "chat_node",
    {
        "pdf_extractor_node": "pdf_extractor_node", 
        "image_extractor_node" : "image_extractor_node",
        "chat_node": "chat_node"}
)

graph.add_edge("pdf_extractor_node", "chat_node")
graph.add_edge("image_extractor_node", "chat_node")
graph.add_edge("chat_node", END)

# -----------------------------
# Main loop
# -----------------------------
if __name__ == "__main__":
    state: State = {
        "messages": [],
        "file_type": "",
        "content": ""
    }

    app = graph.compile()  # Compile once

    print("AI Agent started. Type 'exit' to quit.")
    print("To send a PDF, type: file:<full_path_to_pdf>")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ["exit", "quit", "bye"]:
            break

        # Add user input
        if user_input.startswith("file:"):
            file_path = user_input.replace("file:", "").strip()
            state["messages"].append({"role": "user", "file_path": file_path})
        else:
            state["messages"].append({"role": "user", "content": user_input})

        # Invoke LangGraph
        state = app.invoke(state)

        # Print latest assistant reply
        print("AI:", state["messages"][-1]["content"])
