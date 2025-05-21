
# 🧠 Task 1 — GPT-4o CLI Chat (Streaming, Tokens, Logs)

This is a command-line multi-turn chatbot built using the **OpenAI SDK v1**, GPT-4o, and Python.

It supports:
- ✅ Streaming assistant replies
- ✅ Full conversation context
- ✅ Token counting (via `tiktoken`)
- ✅ Custom system prompts
- ✅ Auto-saving logs in Markdown or JSON

---

## 📁 Folder structure

```
Task 1/
├── main.py             # Entry point (CLI)
├── chat_session.py     # ChatSession class (context, tokens, logging)
├── .env                # Your OpenAI API key
├── logs/               # Auto-generated logs
├── .gitignore          # gitignore file
└── README.md
```

---

## 🚀 How to run

1. Install dependencies:

```bash
pip install openai tiktoken rich python-dotenv
```

2. Add your `.env` file:

```
OPENAI_API_KEY=sk-...
```

3. Run the chat:

```bash
python main.py
```

Or with a custom prompt:

```bash
python main.py -prompt "You are a sarcastic assistant"
```

---

## ✍️ Commands

- `exit` or `quit` — Ends the conversation and saves the log
- Press `Ctrl+C` — Also exits and saves

---

## 💾 Logging

Conversations are saved automatically to the `logs/` folder when the session ends.

#### Example file: `logs/2025-05-20_21-30-43.md`

---

## 📌 Notes

- Requires OpenAI SDK **version 1.x**
