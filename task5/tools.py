from openai import OpenAI
from vector_store import VectorStore

def get_dialog_text(messages: list) -> str:
    dialog_lines = []
    for msg in messages:
        if msg.get("role") in ("user", "assistant"):
            speaker = "User" if msg["role"] == "user" else "Assistant"
            content = msg.get("content", "")
            dialog_lines.append(f"{speaker}: {content}")
    return "\n".join(dialog_lines)

def semantic_search_tool(kb: VectorStore, query: str) -> str:
    results = kb.search(query)
    return "\n".join(results)

def summarize_session_tool(client: OpenAI, messages: list) -> str:
    dialog_text = get_dialog_text(messages)
    prompt = (
        "Please summarize the following conversation in natural language:\n\n"
        f"{dialog_text}\n\nSummary:"
    )

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()