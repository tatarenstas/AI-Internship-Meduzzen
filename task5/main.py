import os
from openai import OpenAI
from dotenv import load_dotenv

from assistant import AssistantApp


def main() -> None:
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    chat_model = os.getenv("OPENAI_CHAT_MODEL")
    embedding_model = os.getenv("OPENAI_EMBEDDING_MODEL")

    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in .env file.")

    client = OpenAI(api_key=api_key)
    app = AssistantApp(client, chat_model=chat_model, embedding_model=embedding_model)
    app.run()


if __name__ == "__main__":
    main()
