import os
from dotenv import load_dotenv
from openai import OpenAI
from semantic_search import SemanticSearchApp


def main() -> None:
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in .env file.")

    client = OpenAI(api_key=api_key)
    app = SemanticSearchApp(client)
    app.run_from_file("corpus.txt")


if __name__ == "__main__":
    main()
