# Internship Week 1 - Capstone Project

## 📄 Title: Build a CLI AI Assistant with Memory, Tools, and Audio/Text Input

This project involves creating a modular command-line AI assistant capable of processing both text and audio input. The assistant updates a vector knowledge base based on user interactions and supports semantic searches using GPT-4o tools while maintaining a session dialogue in memory.

## ✨ Features

- **Text and Audio Input Handling**: Accepts user inputs through direct text or specified audio file paths.
- **Memory and Retrieval**: Updates and retrieves information from a vector knowledge base using semantic search.
- **Streamed Responses**: Provides real-time streamed replies using GPT-4o.
- **Session Summarization**: Generates session summaries on demand.
- **Flexible Commands**: Supports commands like `/update_kb_text`, `/update_kb_voice`, and `/exit`.

## 🔧 Components

- **Knowledge Base**: Utilizes OpenAI embeddings and FAISS for storing and retrieving information.
- **Whisper Integration**: Transcribes audio inputs into text.
- **GPT-4o Interactions**: Manages chatbot responses and operations.
- **Tools**: Implements semantic search and session summarization tools.

## Task Scope

### CLI Loop with Commands
- Handles general questions and commands like:
  - `/update_kb_text`: Capture and store text input in the knowledge base.
  - `/update_kb_voice`: Transcribe and store audio file content.
  - `/exit`: Gracefully exits the application.

### Knowledge Base (Vector DB)
- Embeds knowledge using OpenAI's text embeddings.
- Stores original text and vectors to enable retrieval.
- Allows GPT to query the knowledge base for relevant information.

### Whisper Integration
- Leverages Whisper for voice transcription.
- Integrates seamlessly for audio input handling.

### GPT-4o Interaction
- Utilizes `gpt-4o` for complex response generation.
- Maintains a complete dialogue history kept in memory.

## Folder Structure

```
Task5_Capstone/
├── main.py                # Entry point for the application
├── assistant.py           # Core logic for managing the AI assistant
├── function_defs.py       # Function definitions for tool operations
├── tools.py               # Contains implementation of the semantic search and session summarization
├── vector_store.py        # Logic for knowledge base vector storage and retrieval
├── whisper_utils.py       # Audio transcription utilities using Whisper
├── .env                   # Contains placeholder for API key
├── .gitignore             # File to ignore unnecessary files
└── README.md              # This file
```

## How to Run

1. **Install Dependencies**

```bash
pip install openai faiss-cpu python-dotenv
```

2. **Configure API Key:**

Create a `.env` file with the following content:

```
OPENAI_API_KEY=sk-...
OPENAI_CHAT_MODEL=gpt-4o
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
```

3. **Start the Assistant Application:**

```bash
python main.py
```

## How It Works

1. **User Commands**: The application handles user commands to update the knowledge base via text or audio.
2. **Vectorization and Storage**: Text data is vectorized and stored in a FAISS index.
3. **Semantic Search**: Queries trigger semantic searches within the knowledge base to find relevant information.
4. **Session Summarization**: Provides a human-readable session recap upon request.

## Bonus Challenges

- Save/load the knowledge base from a file.

## Logging

All interactions and session activities are logged for review and debugging purposes, stored in structured formats.