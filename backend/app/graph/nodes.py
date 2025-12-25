import mimetypes
from app.graph.state import State
from app.services.pdf_service import extract_text_from_pdf
from app.services.ocr_service import extract_text_from_image
from app.services.llm_service import get_llm

llm = get_llm()

# -----------------------------
# Detect file type
# -----------------------------
def detect_file_node(state: State):
    last_message = state["messages"][-1]

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
        state["file_type"] = "text"
        state["content"] = last_message["content"]

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
