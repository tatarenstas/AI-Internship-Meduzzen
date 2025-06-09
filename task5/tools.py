from openai import OpenAI
from vector_store import VectorStore

def semantic_search_tool(kb: VectorStore, query: str) -> str:
    results = kb.search(query)
    return "\n".join(results)

def summarize_session_tool(client: OpenAI, messages: list) -> str:
    prompt = "Please summarize the session in natural language."
    session_messages = [{"role": "system", "content": prompt}] + messages

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=session_messages
    )
    return response.choices[0].message.content
