import os

from openai import OpenAI
from dotenv import load_dotenv
from argparse import ArgumentParser

from audio_summarizer import AudioSummarizerApp

def main() -> None:
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in .env file.")

    parser = ArgumentParser()
    parser.add_argument("--mode", type=str, default="summary", help="summary | extract_keywords | generate_title")
    args = parser.parse_args()

    client = OpenAI(api_key=api_key)
    app = AudioSummarizerApp(client, mode=args.mode)
    app.run()

if __name__ == "__main__":
    main()
