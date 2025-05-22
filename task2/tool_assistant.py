import os
import json
import wikipedia
from datetime import datetime

class ToolAssistant:
    def __init__(self, client, system_prompt: str):
        self.client = client
        self.system_prompt = system_prompt
        self.messages = [{"role": "system", "content": system_prompt}]
        self.function_map = {
            "get_weather": self.get_weather,
            "calculate_area": self.calculate_area,
            "search_wikipedia": self.search_wikipedia
        }
        self.function_definitions = [
            {
                "name": "get_weather",
                "description": "Get fake weather for a city",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "city": {"type": "string", "description": "City name"}
                    },
                    "required": ["city"]
                }
            },
            {
                "name": "calculate_area",
                "description": "Calculate area of a circle by radius",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "radius": {"type": "number", "description": "Radius of the circle"}
                    },
                    "required": ["radius"]
                }
            },
            {
                "name": "search_wikipedia",
                "description": "Search Wikipedia for a summary of a query",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Search query"}
                    },
                    "required": ["query"]
                }
            }
        ]

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

    def log_function_call(self, name: str, args: dict) -> None:
        os.makedirs("logs", exist_ok=True)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"logs/{timestamp}_{name}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump({
                "timestamp": timestamp,
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

            self.messages.append({"role": "user", "content": user_input})

            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=self.messages,
                functions=self.function_definitions,
                function_call="auto"
            )

            reply = response.choices[0].message

            if reply.function_call:
                name = reply.function_call.name
                args = json.loads(reply.function_call.arguments)
                print(f"[GPT triggers {name}({args})]")

                result = self.function_map[name](**args)
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
                print("\n> GPT:", final_content)
                self.messages.append({"role": "assistant", "content": final_content})
            else:
                print("\n> GPT:", reply.content)
                self.messages.append({"role": "assistant", "content": reply.content})
