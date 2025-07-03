# 🎧 Task 4 – Audio Transcriber and Summarizer

This project presents a CLI-based tool designed to transcribe and summarize audio files using OpenAI's Whisper and GPT-4o. The application enhances user interaction with audio content by providing a concise summary, key topics, or even generating a catchy title.

## ✨ Features

- Audio transcription via OpenAI’s Whisper service.
- Summarization, keyword extraction, or title generation using GPT-4o.
- Multiple audio file processing for batch mode.
- Logs summaries and transcripts for reference.

## 🔧 Components

- **OpenAI Whisper**: Converts audio files into plain text transcripts.
- **GPT-4o**: Processes transcripts to generate summaries, key points, or titles.
- **Logging**: Stores transcripts and summaries for audit and review.

## 📁 Folder Structure

```
Task 4/
├── main.py                  # Entry point: loads API key, sets up and runs the audio summarizer
├── audio_summarizer.py      # Contains logic for transcription and summarization
├── .env                     # Contains your OpenAI API key
├── .env.sample              # sample .env file for reference
├── logs/                    # Auto-generated folder for transcript and summary logs
├── .gitignore               # gitignore file
└── README.md                # This file
```

## 🚀 How to Run

1. **Install dependencies**

```bash
pip install openai python-dotenv
```

2. **Configure API Key:**

Create a `.env` file with the following content:

```
OPENAI_API_KEY=sk-...
```

3. **Start the Audio Summarizer:**

```bash
python main.py
```

4. **Interact with the Application:**

- Enter the path(s) to your audio file(s) when prompted.
- Type `exit` to end the session.

## 🧩 How It Works

1. **Audio Transcription with Whisper**: The user uploads audio files (.mp3, .wav, .m4a), which are transcribed into text.
2. **Summarization with GPT-4o**: The transcript is processed based on user-selected mode (summary, extract keywords, or generate title).
3. **Logging Results**: Saves transcript and summary into the `logs/` directory for future reference.

## 🌟 Bonus Features

- **Mode Flag**: Allows switching between summarization, keyword extraction, or title generation.
- **Batch Processing**: Enter multiple file paths separated by `;` for processing in a single run.
- **Summary Logging**: Records each session's output along with generated summaries in markdown format.

## 💾 Logging

Transcripts and GPT-4o summaries are stored in the `logs/` directory, organized with timestamps and unique identifiers for easy retrieval.

---

## 📝 Notes

- Ensure the OpenAI API key provided is valid and authorized for required API access.
- Experiment with different prompts to enhance the quality of summarization and other outputs with GPT-4o.

This application provides a versatile tool for quickly processing and summarizing audio content, proving useful for meetings, podcasts, and more.