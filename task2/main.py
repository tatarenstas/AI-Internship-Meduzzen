import os
import argparse
from dotenv import load_dotenv
from openai import OpenAI
from tool_assistant import ToolAssistant

def load_api_key() -> str:
    load_dotenv()
    return os.getenv("OPENAI_API_KEY")

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("-prompt", type=str, default="You are a helpful assistant that answers only using the results from the tools.")
    args = parser.parse_args()

    api_key = load_api_key()
    if not api_key:
        raise ValueError("Set the OPENAI_API_KEY environment variable.")

    client = OpenAI(api_key=api_key)

    assistant = ToolAssistant(client=client, system_prompt=args.prompt)
    assistant.run()

if __name__ == "__main__":
    main()
