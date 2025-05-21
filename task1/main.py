import os
import argparse
from dotenv import load_dotenv
from openai import OpenAI
from rich.console import Console
from chat_session import ChatSession

def load_api_key() -> str:
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in .env file")
    return api_key

def stream_chat(session: ChatSession, client: OpenAI) -> None:
    try:
        console.print("Assistant is typing...\n", style="dim")

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=session.messages,
            stream=True,
        )

        full_reply = ""
        for chunk in response:
            content = chunk.choices[0].delta.content or ""
            print(content, end="", flush=True)
            full_reply += content

        print()
        session.add_message("assistant", full_reply)
        session.update_token_count()

        console.print(f"[Tokens (approx): {session.total_tokens}]", style="blue")

    except Exception as e:
        console.print(f"[Error]: {str(e)}", style="bold red")

def main() -> None:
    parser = argparse.ArgumentParser(description="GPT-4o CLI Chat")
    parser.add_argument("-prompt", type=str, help="Custom system prompt")
    args = parser.parse_args()

    system_prompt = args.prompt or "You are a helpful assistant."
    session = ChatSession(system_prompt)

    console.print(f"[System Prompt]: {system_prompt}", style="bold cyan")

    api_key = load_api_key()
    client = OpenAI(api_key=api_key)

    while True:
        try:
            user_input = input("\n> You: ")
            if user_input.strip().lower() in ["exit", "quit"]:
                session.save_log(format="md")
                break

            session.add_message("user", user_input)
            stream_chat(session, client)

        except KeyboardInterrupt:
            console.print("\n[Interrupted]", style="yellow")
            session.save_log(format="md")
            break

if __name__ == "__main__":
    console = Console()
    main()
