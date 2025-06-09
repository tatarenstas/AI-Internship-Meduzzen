from openai import OpenAI

def transcribe(client: OpenAI, path: str) -> str:
    try:
        with open(path, "rb") as f:
            res = client.audio.transcriptions.create(
                model="whisper-1",
                file=f
            )
        return res.text
    except Exception as e:
        print(f"Error during transcription: {e}")
        return ""
