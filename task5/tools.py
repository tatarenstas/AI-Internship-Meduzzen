from openai import OpenAI
from vector_store import VectorStore

def search_kb_tool(client: OpenAI, kb: VectorStore, query: str) -> str:
    results = kb.search(query, k=1)
    return f"{results[0]}"

def summarize_session(client: OpenAI, messages: list) -> str:
    msg = messages + [{"role": "user", "content": "Summarize this conversation."}]
    res = client.chat.completions.create(
        model="gpt-4o",
        messages=msg
    )
    return res.choices[0].message.content.strip()
