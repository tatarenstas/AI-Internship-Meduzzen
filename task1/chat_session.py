import os
import json
from datetime import datetime
from typing import List, Dict
import tiktoken


class ChatSession:
    def __init__(self, system_prompt: str = "You are a helpful assistant.") -> None:
        self.messages: List[Dict[str, str]] = [{"role": "system", "content": system_prompt}]
        self.total_tokens: int = 0
        self.start_time: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def add_message(self, role: str, content: str) -> None:
        self.messages.append({"role": role, "content": content})

    def update_token_count(self, model: str = "gpt-4o") -> None:
        self.total_tokens = self.count_tokens(self.messages, model)

    def save_log(self, folder: str = "logs", format: str = "md") -> None:
        os.makedirs(folder, exist_ok=True)
        filename = f"{folder}/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.{format}"

        if format == "json":
            self.write_to_json(filename, {
                "start_time": self.start_time,
                "messages": self.messages,
                "total_tokens": self.total_tokens
            })
        else:
            self.write_to_md(filename, self.messages, self.start_time, self.total_tokens)

        print(f"[Conversation saved to {filename}]")

    @staticmethod
    def count_tokens(messages: List[Dict[str, str]], model: str = "gpt-4o") -> int:
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

    @staticmethod
    def write_to_json(filename: str, data: Dict) -> None:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    @staticmethod
    def write_to_md(filename: str, messages: List[Dict[str, str]], start_time: str, total_tokens: int) -> None:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"# Conversation — {start_time}\n\n")
            for msg in messages:
                role = "**You**" if msg["role"] == "user" else "**Assistant**"
                f.write(f"{role}: {msg['content']}\n\n")
            f.write(f"---\n**Total tokens used**: {total_tokens}\n")
