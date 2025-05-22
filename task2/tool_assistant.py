import os
import json
import uuid
import wikipedia

from openai import OpenAI
from datetime import datetime
from typing import Dict, Any

from tool_definitions import FUNCTION_DEFINITIONS


class ToolAssistant:
    def __init__(self, client: OpenAI, system_prompt: str) -> None:
        self.client = client
        self.system_prompt = system_prompt
        self.messages = [{"role": "system", "content": system_prompt}]
        self.function_map = {
            "get_weather": self.get_weather,
            "calculate_area": self.calculate_area,
            "search_wikipedia": self.search_wikipedia
        }
        self.function_definitions = FUNCTION_DEFINITIONS

    def get_weather(self, city: str) -> str:
        return f"It's sunny and 22°C in {city} today."

    def calculate_area(self, radius: float) -> str:
        area = 3.1415 * radius * radius
        return f"The area of a circle with radius {radius} is {area:.2f}."

    def search_wikipedia(self, query: str) -> str:
        try:
            print(f"Searching Wikipedia for '{query}'...")
            return wikipedia.summary(query, sentences=2)
        except Exception as e:
            return f"Sorry, I couldn't find anything on Wikipedia for '{query}'."

    def log_function_call(self, name: str, args: Dict[str, Any]) -> None:
        os.makedirs("logs", exist_ok=True)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        unique_id = uuid.uuid4()
        filename = f"logs/{timestamp}_{unique_id}_{name}.json"

        with open(filename, "w", encoding="utf-8") as f:
            json.dump({
                "timestamp": timestamp,
                "uuid": str(unique_id),
                "function": name,
                "arguments": args
            }, f, indent=2)
        print(f"[Function call logged to {filename}]")

    def run(self) -> None:
        print(f"[System Prompt]: {self.system_prompt}\n")

        while True:
            user_input = input("> You: ")
            if user_input.lower() == "exit":
                break
            self.handle_input(user_input)

    def handle_input(self, user_input: str) -> None:
        self.messages.append({"role": "user", "content": user_input})

        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=self.messages,
            functions=self.function_definitions,
            function_call="auto"
        )

        reply = response.choices[0].message

        if reply.function_call:
            self._handle_function_call(reply)
        else:
            self._print_and_store(reply.content)

    def _handle_function_call(self, reply: Any) -> None:
        name = reply.function_call.name
        args = json.loads(reply.function_call.arguments)
        print(f"[GPT triggers {name}({args})]")

        func = self.function_map.get(name)
        if not func:
            print(f"[⚠️ Unknown function: {name}]")
            return

        result = func(**args)
        print("→ Function result:", result)

        self.log_function_call(name, args)

        self.messages.append({
            "role": "function",
            "name": name,
            "content": result
        })

        follow_up = self.client.chat.completions.create(
            model="gpt-4o",
            messages=self.messages
        )
        final_content = follow_up.choices[0].message.content
        self._print_and_store(final_content)

    def _print_and_store(self, content: str) -> None:
        print("\n> GPT:", content)
        self.messages.append({"role": "assistant", "content": content})
