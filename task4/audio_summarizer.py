import os
import uuid
from datetime import datetime
from openai import OpenAI
from typing import Optional


class AudioSummarizerApp:
    def __init__(self, client: OpenAI, mode: str = "summary") -> None:
        self.client = client
        self.mode = mode

    def transcribe(self, file_path: str) -> Optional[str]:
        try:
            with open(file_path, "rb") as audio_file:
                transcript = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file
                )
            return transcript.text
        except Exception as e:
            print(f"[Error transcribing file]: {e}")
            return None

    def summarize(self, transcript: str) -> str:
        if self.mode == "summary":
            prompt = f"Please summarize the following transcript:\n\n{transcript}"
        elif self.mode == "extract_keywords":
            prompt = f"Extract key topics or bullet points from this transcript:\n\n{transcript}"
        elif self.mode == "generate_title":
            prompt = f"Generate a short, relevant title for this transcript:\n\n{transcript}"
        else:
            prompt = f"Summarize the following transcript:\n\n{transcript}"

        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=messages
        )
        return response.choices[0].message.content.strip()

    def log_summary(self, filename: str, transcript: str, summary: str) -> None:
        os.makedirs("logs", exist_ok=True)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        unique_id = uuid.uuid4()
        base = os.path.basename(filename).replace(" ", "_")
        log_file = f"logs/{timestamp}_{base}_{unique_id}.md"

        with open(log_file, "w", encoding="utf-8") as f:
            f.write(f"# {self.mode.capitalize()} Log ({timestamp})\n")
            f.write(f"**File:** {filename}\n\n")
            f.write("## Transcript\n")
            f.write(transcript + "\n\n")
            f.write(f"## {self.mode.capitalize()}\n")
            f.write(summary + "\n")

        print(f"Log saved to {log_file}")

    def process_file(self, path: str) -> None:
        print(f"→ Transcribing '{path}'...")
        transcript = self.transcribe(path)
        if not transcript:
            return

        print("→ Transcript preview:")
        print(transcript[:500] + ("..." if len(transcript) > 500 else ""))

        print(f"→ Running GPT-4o ({self.mode})...")
        summary = self.summarize(transcript)

        print("\n> GPT Result:")
        print(summary)

        self.log_summary(path, transcript, summary)

    def run(self) -> None:
        print(f"Audio Summarizer [{self.mode}] is ready. Enter audio file path(s) or type 'exit'.")
        while True:
            raw_input = input("> Enter path(s) to audio file(s): ").strip()
            if raw_input.lower() == "exit":
                break

            paths = [p.strip() for p in raw_input.split(";") if p.strip()]
            for path in paths:
                if not os.path.exists(path):
                    print(f"File not found: {path}")
                    continue
                self.process_file(path)
