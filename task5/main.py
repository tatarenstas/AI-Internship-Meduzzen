import os
from openai import OpenAI
from dotenv import load_dotenv

from vector_store import VectorStore
from tools import search_kb_tool, summarize_session
from whisper_utils import transcribe

def main():
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is not set")

    client = OpenAI(api_key=api_key)
    kb = VectorStore(client)
    messages = []

    print("Assistant is ready. Type '/exit' to quit.")

    while True:
        user_input = input("> You: ").strip()

        if user_input == "/exit":
            print("Assistant: Goodbye!")
            break

        elif user_input == "/update_kb_text":
            print("Assistant: Enter knowledge text:")
            text = input("> ")
            kb.add_text(text)
            print("Assistant: Added.")

        elif user_input == "/update_kb_voice":
            print("Assistant: Enter path to audio file:")
            path = input("> ")
            if os.path.exists(path):
                transcript = transcribe(client, path)
                if transcript:
                    kb.add_text(transcript)
                    print("Assistant: Transcribed and added.")
                else:
                    print("Assistant: Transcription failed.")
            else:
                print("Assistant: File not found.")

        elif "search" in user_input.lower():
            result = search_kb_tool(client, kb, user_input)
            print(f"Assistant: {result}")
            messages.append({"role": "user", "content": user_input})
            messages.append({"role": "assistant", "content": result})

        elif "summary" in user_input.lower():
            result = summarize_session(client, messages)
            print(f"Assistant: {result}")
            messages.append({"role": "user", "content": user_input})
            messages.append({"role": "assistant", "content": result})

        else:
            messages.append({"role": "user", "content": user_input})
            print("Assistant is typing...")
            stream = client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                stream=True
            )
            reply = ""
            for chunk in stream:
                delta = chunk.choices[0].delta.content or ""
                print(delta, end="", flush=True)
                reply += delta
            print()
            messages.append({"role": "assistant", "content": reply})

if __name__ == "__main__":
    main()