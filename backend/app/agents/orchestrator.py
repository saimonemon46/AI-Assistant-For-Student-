from graph.state import State
from services.llm_service import get_llm

llm = get_llm()

INTENTS = ["chat", "study", "news", "exam"]


### Holds everything into the state by classifying user intent
def orchestrator_node(state: State) -> State:
    """
    Decide user intent and attach it to state.
    This node must be deterministic and minimal.
    """

    user_input = state.get("input") or state["messages"][-1].get("content", "")

    prompt = f"""
You are an intent classifier for a student assistant.

Classify the intent into exactly ONE of:
{", ".join(INTENTS)}

Rules:
- "news" → current affairs, headlines, latest updates
- "study" → notes, PDFs, Images, explanations, learning
- "exam" → quizzes, tests, mock exams
- "chat" → everything else

Return ONLY the intent word.
Input:
{user_input}
"""

    response = llm.invoke([
        {"role": "user", "content": prompt}
    ])

    intent = response.content.strip().lower()

    if intent not in INTENTS:
        intent = "chat"  # fallback, not optimism

    state["intent"] = intent
    return state
