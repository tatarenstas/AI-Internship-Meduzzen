# Internship Summary: Building AI-Powered Tools

## Overview
Throughout my internship, I embarked on a series of practical AI projects focused on building real-world applications using OpenAI’s GPT-4o, Whisper, and embedding models. These tasks spanned a wide spectrum of AI capabilities — from conversational interfaces and semantic search to audio transcription, tool calling, and memory-based assistants.

## ✅ Achievements

### 1. GPT-4o CLI Chatbot (Streaming + Logs)
- **Developed** a command-line chatbot with real-time GPT-4o responses.
- **Integrated** full conversation memory, token tracking, and session logging in Markdown/JSON.
- **Supported** custom system prompts with clean CLI command handling.

### 2. Tool Assistant with Function Calling
- **Created** a mini assistant capable of calling Python functions based on natural language queries.
- **Implemented** functions including weather simulation, area calculation, and Wikipedia summarization.
- **Logged** each function call and arguments automatically.

### 3. Local Semantic Search Engine
- **Developed** a document search tool using OpenAI embeddings and FAISS for local vector storage.
- **Enabled** users to enter queries in natural language and receive responses enhanced by GPT-4o based on top-matching context.
- **Constructed** reusable modules for vector storage and query handling.

### 4. Audio Transcriber & Summarizer
- **Created** a tool to transcribe audio files using Whisper and summarize them via GPT-4o.
- **Supported** batch file processing with flexible output modes (summary, keywords, or title).
- **Logged** transcripts and summaries for future reference.

### 5. Capstone: Full AI Assistant with Memory, Audio/Text Input & Tools
- **Integrated** all previous components into a unified assistant with text and voice input.
- **Integrated** a vector knowledge base that could be updated via commands (/update_kb_text, /update_kb_voice).
- **Enabled** semantic search, session summarization, and streamed GPT-4o replies.
- **Designed** the system for modularity, maintainability, and real-time interaction.

## 🧠 Learning Outcomes

1. **Advanced API Usage**: Gained in-depth experience with OpenAI’s GPT-4o, embeddings, and Whisper.
2. **Function Calling & Tool Integration**: Enabled GPT to call custom tools for hybrid reasoning.
3. **Vector Search Fundamentals**: Worked with FAISS and cosine similarity for efficient local semantic search.
4. **Audio Processing**: Utilized Whisper to handle and transcribe various audio formats.
5. **CLI Design**: Designed intuitive command-line interfaces with argument parsing, command handling, and logging.
6. **Modular Architecture**: Advocated the separation of concerns using reusable components and clean code practices.

## 🧩 Key Technologies Used
- **Programming & APIs**: Python, OpenAI SDK v1
- **AI Models**: GPT-4o, Whisper, Embeddings (text-embedding-3-small)
- **Search & Storage**: FAISS, cosine similarity
- **Utilities**: dotenv, argparse, wikipedia, rich
- **Systems & Tools**: CLI tools, logging systems, semantic search engines

## 📌 Final Reflection
This internship provided a holistic understanding of creating AI assistants that are not only interactive but also context-aware, tool-augmented, and capable of learning through conversations. I gained hands-on experience in designing intelligent, modular systems that bridge the gap between raw AI capabilities and practical user applications.
