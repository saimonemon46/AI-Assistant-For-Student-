from langgraph.graph import StateGraph, START, END
from graph.state import State
from graph.nodes import (
    detect_file_node,
    pdf_extractor_node,
    image_extractor_node,
    chat_node,
    news_node
)

def build_graph():
    graph = StateGraph(State)

    # Nodes
    graph.add_node("detect_file", detect_file_node)
    graph.add_node("pdf_extractor", pdf_extractor_node)
    graph.add_node("image_extractor", image_extractor_node)
    graph.add_node("chat", chat_node)
    graph.add_node("news", news_node)

    # Start -> detect_file
    graph.add_edge(START, "detect_file")

    # Conditional routing based on mode set in detect_file_node
    graph.add_conditional_edges(
        "detect_file",
        lambda s: s.get("mode", "chat"),
        {
            "pdf_extractor": "pdf_extractor",
            "image_extractor": "image_extractor",
            "chat": "chat",
            "news": "news"
        }
    )

    # All processing nodes -> chat node for final response
    graph.add_edge("pdf_extractor", "chat")
    graph.add_edge("image_extractor", "chat")
    graph.add_edge("news", END)

    # Chat node -> END
    graph.add_edge("chat", END)

    return graph.compile()
