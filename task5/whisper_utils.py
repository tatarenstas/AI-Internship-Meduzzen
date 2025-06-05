from openai import OpenAI

def transcribe(client: OpenAI, file_path: str):
    try:
        with open(file_path, "rb") as f:
            response = client.audio.transcriptions.create(
                model="whisper-1",
                file=f
            )
        return response.text

    except Exception as e:
        print(f"Error (in transcribe): {e}")