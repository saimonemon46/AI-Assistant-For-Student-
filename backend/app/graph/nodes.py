import mimetypes
from graph.state import State
from services.pdf_service import extract_text_from_pdf
from services.ocr_service import extract_text_from_image
from services.llm_service import get_llm

from services.news_service import fetch_news, summarize_news

llm = get_llm()

# -----------------------------
# Detect file type
# -----------------------------
def detect_file_node(state: State):
    last_message = state["messages"][-1]
    content = last_message.get("content", "").strip().lower()

    # Check for news request first
    if "news" in content:
        state["file_type"] = "news"
        state["mode"] = "news"
        state["content"] = content

    # Check if a file path is provided
    elif "file_path" in last_message:
        file_path = last_message["file_path"]
        mime, _ = mimetypes.guess_type(file_path)

        if mime is None:
            raise ValueError("Cannot detect file type")

        if "pdf" in mime:
            state["file_type"] = "pdf"
            state["mode"] = "pdf_extractor"
        elif "image" in mime:
            state["file_type"] = "image"
            state["mode"] = "image_extractor"
        else:
            raise ValueError(f"Unsupported file type: {mime}")

        state["content"] = file_path

    # Otherwise treat as normal text
    else:
        state["file_type"] = "text"
        state["mode"] = "chat"
        state["content"] = last_message.get("content", "")

    return state




# -----------------------------
# PDF extractor
# -----------------------------
def pdf_extractor_node(state: State):
    state["content"] = extract_text_from_pdf(state["content"])
    return state


# -----------------------------
# Image extractor
# -----------------------------
def image_extractor_node(state: State):
    state["content"] = extract_text_from_image(state["content"])
    return state


# -----------------------------
# Chat agent
# -----------------------------
def chat_node(state: State):
    response = llm.invoke(
        [{"role": "user", "content": state["content"]}]
    )
    state["messages"].append({
        "role": "assistant",
        "content": response.content
    })
    return state


# ------------------------------
# Articles agent 
# ------------------------------
def news_node(state: State):
    # Last message as topic, default to "latest"
    topic = state["messages"][-1].get("content", "latest")
    
    articles = fetch_news(topic)
    summary = summarize_news(articles)

    state["messages"].append({
        "role": "assistant",
        "content": summary
    })
    return state