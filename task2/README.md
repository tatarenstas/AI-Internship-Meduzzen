# 🤖 Task 2 — GPT-4o Tool Assistant with Function Calling

This project demonstrates how to use **OpenAI GPT-4o's function calling** feature to create a command-line assistant capable of using Python tools to answer questions.

The assistant supports:
- 🌤️ **Fake Weather Reporting**
- 📐 **Circle Area Calculation**
- 🌐 **Wikipedia Summarization**

The assistant automatically decides which tool to call based on your natural language input — simulating a mini GPT-powered agent with tool usage.

---

## 📁 Folder Structure

```
Task 2/
├── main.py              # Entry point: loads API key, parses CLI args, runs assistant
├── tool_assistant.py    # Contains ToolAssistant class, tool functions, function calling logic, logging
├── .env                 # Contains your OpenAI API key
├── logs/                # Auto-generated folder for function call logs
├── .gitignore           # gitignore file
└── README.md            # This file
```

---

## 🚀 How to Run

1. **Install dependencies**

```bash
pip install openai wikipedia python-dotenv
```

2. **Add your `.env` file**:

```
OPENAI_API_KEY=sk-...
```

3. **Run the assistant**:

```bash
python main.py
```

4. **Run with a custom assistant personality**:

```bash
python main.py -prompt "You are a sarcastic assistant that always jokes"
```

---

## 🧠 Supported Tools

| Tool              | Description                            |
|-------------------|----------------------------------------|
| `get_weather`     | Fake weather response by city          |
| `calculate_area`  | Area of a circle from radius           |
| `search_wikipedia`| 2-line Wikipedia summary for query     |

---

## 💾 Logging

Each function call is automatically saved to `logs/` with a timestamp and arguments.

**Example:**

```
logs/2025-05-22_16-34-01_6bc82e48-3711-11f0-b713-e4a8dfe361a5_get_weather.json
```

---

## 📝 Notes

- Uses OpenAI SDK v1.x
- No streaming — simpler for tool execution
- Type `exit` to quit the assistant at any time
