from graph.state import State
from agents.chat_agent import ChatAgent
from agents.news_agent import NewsAgent
from agents.study_agent import StudyAgent

chat_agent = ChatAgent()
news_agent = NewsAgent()
study_agent = StudyAgent()

def detect_file_node(state: State):
    last_message = state["messages"][-1]
    content = last_message.get("content", "").strip().lower()

    if "news" in content:
        state["file_type"] = "news"
        state["mode"] = "news"
        state["content"] = content
    elif "file_path" in last_message:
        file_path = last_message["file_path"]
        if file_path.lower().endswith(".pdf"):
            state["file_type"] = "pdf"
            state["mode"] = "pdf_extractor"
        elif file_path.lower().endswith((".jpg", ".png", ".jpeg")):
            state["file_type"] = "image"
            state["mode"] = "image_extractor"
        else:
            state["file_type"] = "unknown"
            state["mode"] = "chat"
        state["content"] = file_path
    else:
        state["file_type"] = "text"
        state["mode"] = "chat"
        state["content"] = content

    return state

def pdf_extractor_node(state: State):
    state["content"] = study_agent.handle_pdf(state["content"])
    return state

def image_extractor_node(state: State):
    state["content"] = study_agent.handle_image(state["content"])
    return state

def chat_node(state: State):
    response = chat_agent.handle(state["content"])
    state["messages"].append({"role": "assistant", "content": response})
    return state

def news_node(state: State):
    topic = state["messages"][-1].get("content", "latest")
    response = news_agent.handle(topic)
    state["messages"].append({"role": "assistant", "content": response})
    return state
