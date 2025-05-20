import os
import json
from datetime import datetime
from typing import List, Dict
import tiktoken


def count_tokens(messages: List[Dict], model="gpt-4o") -> int:
    try:
        encoding = tiktoken.encoding_for_model(model)
    except Exception:
        encoding = tiktoken.get_encoding("cl100k_base")

    total = 0
    for m in messages:
        total += 4  # every message overhead
        for key, value in m.items():
            total += len(encoding.encode(value))
    total += 2  # priming
    return total


class ChatSession:
    def __init__(self, system_prompt="You are a helpful assistant."):
        self.system_prompt = system_prompt
        self.messages = [{"role": "system", "content": system_prompt}]
        self.total_tokens = 0
        self.start_time = datetime.now()
        self.start_time_str = self.start_time.strftime("%Y-%m-%d %H:%M:%S")

    def add_message(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})

    def update_token_count(self, model="gpt-4o"):
        self.total_tokens = count_tokens(self.messages, model)

    def save_log(self, folder="logs", format="md"):
        os.makedirs(folder, exist_ok=True)
        filename = f"{folder}/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.{format}"

        summary_text = self.summary()

        if format == "json":
            with open(filename, "w", encoding="utf-8") as f:
                json.dump({
                    "start_time": self.start_time_str,
                    "system_prompt": self.system_prompt,
                    "messages": self.messages,
                    "total_tokens": self.total_tokens,
                    "summary": summary_text.strip().split('\n')  # у json - масив рядків
                }, f, indent=2)
        else:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(f"# Conversation — {self.start_time_str}\n\n")
                f.write(f"**System Prompt**: {self.system_prompt}\n\n")
                for msg in self.messages:
                    if msg["role"] == "system":
                        continue
                    if msg["role"] == "user":
                        f.write(f"**You**: {msg['content']}\n\n")
                    elif msg["role"] == "assistant":
                        f.write(f"**Assistant**: {msg['content']}\n\n")
                f.write(f"---\n**Total tokens used**: {self.total_tokens}\n\n")
                f.write(f"## Session Summary\n")
                f.write(summary_text)

        print(f"[Conversation saved to {filename}]")

    def summary(self):
        user_msgs = sum(1 for m in self.messages if m["role"] == "user")
        assistant_msgs = sum(1 for m in self.messages if m["role"] == "assistant")
        duration = datetime.now() - self.start_time
        duration_sec = int(duration.total_seconds())

        summary_text = (
            f"Session Summary:\n"
            f"- System Prompt: {self.system_prompt}\n"
            f"- User messages: {user_msgs}\n"
            f"- Assistant messages: {assistant_msgs}\n"
            f"- Total tokens used: {self.total_tokens}\n"
            f"- Duration: {duration_sec} seconds\n"
        )
        return summary_text
