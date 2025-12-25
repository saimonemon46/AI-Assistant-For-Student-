from langgraph.graph import StateGraph, START, END
from app.graph.state import State
from app.graph.nodes import (
    detect_file_node,
    pdf_extractor_node,
    image_extractor_node,
    chat_node
)

def build_graph():
    graph = StateGraph(State)

    graph.add_node("detect_file", detect_file_node)
    graph.add_node("pdf_extractor", pdf_extractor_node)
    graph.add_node("image_extractor", image_extractor_node)
    graph.add_node("chat", chat_node)

    graph.add_edge(START, "detect_file")

    graph.add_conditional_edges(
        "detect_file",
        lambda s:
            "pdf_extractor" if s["file_type"] == "pdf"
            else "image_extractor" if s["file_type"] == "image"
            else "chat",
        {
            "pdf_extractor": "pdf_extractor",
            "image_extractor": "image_extractor",
            "chat": "chat"
        }
    )

    graph.add_edge("pdf_extractor", "chat")
    graph.add_edge("image_extractor", "chat")
    graph.add_edge("chat", END)

    return graph.compile()
