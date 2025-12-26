from graph.graph import build_graph
from graph.state import State

def main():
    state: State = {
        "messages": [],
        "file_type": "",
        "mode": "",
        "content": ""
    }

    app = build_graph()

    print("AI Study Assistant started. Type 'exit' to quit.")
    print("Upload a file using: file:<full_path> or type text / news topic")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in {"exit", "quit", "bye"}:
            break

        if user_input.startswith("file:"):
            path = user_input.replace("file:", "").strip()
            state["messages"].append({"role": "user", "file_path": path})
        else:
            state["messages"].append({"role": "user", "content": user_input})

        state = app.invoke(state)

        # Print the latest assistant response
        print("AI:", state["messages"][-1]["content"])

if __name__ == "__main__":
    main()
