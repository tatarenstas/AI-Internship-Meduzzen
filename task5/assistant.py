import os
import json
import uuid
from datetime import datetime
from typing import Any, Dict

from openai import OpenAI

from vector_store import VectorStore
from whisper_utils import transcribe
from function_defs import FUNCTION_DEFINITIONS
from tools import semantic_search_tool, summarize_session_tool

class AssistantApp:
    def __init__(self, client: OpenAI, chat_model: str = "gpt-4o", embedding_model: str = "text-embedding-3-large"):
        self.client = client
        self.chat_model = chat_model
        self.kb = VectorStore(client, embedding_model=embedding_model)
        self.messages = []
        self.functions = FUNCTION_DEFINITIONS
        self.session_log = []
        os.makedirs("logs", exist_ok=True)

    def run(self):
        print("Assistant is ready. Type '/exit' to quit.")

        while True:
            user_input = input("> You: ").strip()
            if user_input == "/exit":
                print("Assistant: Goodbye!")
                self.save_session_log()
                break

            elif user_input == "/update_kb_text":
                print("Assistant: Enter knowledge text:")
                text = input("> ").strip()
                self.kb.add_text(text)
                print("Assistant: Added.")
                self.log_event("update_kb_text", {"text": text})

            elif user_input == "/update_kb_voice":
                print("Assistant: Enter path to audio file:")
                path = input("> ").strip()
                if os.path.exists(path):
                    transcript = transcribe(self.client, path)
                    if transcript:
                        self.kb.add_text(transcript)
                        print("Assistant: Transcribed and added.")
                        self.log_event("update_kb_voice", {"path": path, "transcript": transcript})
                    else:
                        print("Assistant: Transcription failed.")
                        self.log_event("update_kb_voice_failed", {"path": path})
                else:
                    print("Assistant: File not found.")
                    self.log_event("update_kb_voice_failed", {"path": path})

            else:
                self.messages.append({"role": "user", "content": user_input})
                self.log_event("user_message", {"content": user_input})

                response = self.client.chat.completions.create(
                    model=self.chat_model,
                    messages=self.messages,
                    functions=self.functions,
                    function_call="auto"
                )
                reply = response.choices[0].message

                if reply.function_call:
                    name = reply.function_call.name
                    args = json.loads(reply.function_call.arguments)
                    print(f"[GPT triggers {name}({args})]")
                    self.log_function_call(name, args)

                    if name == "semantic_search":
                        result = semantic_search_tool(self.kb, args["query"])
                        print("\n> KB Result:")
                        print(result)
                        self.messages.append({
                            "role": "function",
                            "name": name,
                            "content": result
                        })
                        self.log_event("function_result", {"function": name, "result": result})

                    elif name == "summarize_session":
                        summary = summarize_session_tool(self.client, self.messages)
                        print("\n> GPT Summary:")
                        print(summary)
                        self.messages.append({
                            "role": "function",
                            "name": name,
                            "content": summary
                        })
                        self.log_event("function_result", {"function": name, "result": summary})

                    follow_up = self.client.chat.completions.create(
                        model=self.chat_model,
                        messages=self.messages
                    )
                    final_content = follow_up.choices[0].message.content
                    print("> GPT:", final_content)
                    self.messages.append({"role": "assistant", "content": final_content})
                    self.log_event("assistant_message", {"content": final_content})

                else:
                    print("> GPT:", reply.content)
                    self.messages.append({"role": "assistant", "content": reply.content})
                    self.log_event("assistant_message", {"content": reply.content})

    def log_function_call(self, name: str, args: Dict[str, Any]) -> None:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        unique_id = uuid.uuid4()
        filename = f"logs/{timestamp}_{unique_id}_{name}.json"
        data = {
            "timestamp": timestamp,
            "uuid": str(unique_id),
            "function": name,
            "arguments": args
        }
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        print(f"[Function call logged to {filename}]")
        self.log_event("function_call_logged", {"filename": filename})

    def log_event(self, event_type: str, data: Dict[str, Any]) -> None:
        event = {
            "timestamp": datetime.now().isoformat(),
            "event": event_type,
            "data": data
        }
        self.session_log.append(event)

    def save_session_log(self, folder: str = "logs", format: str = "json") -> None:
        if not self.session_log:
            return
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = os.path.join(folder, f"session_log_{timestamp}.{format}")

        if format == "json":
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(self.session_log, f, indent=2, ensure_ascii=False)
        elif format == "md":
            with open(filename, "w", encoding="utf-8") as f:
                f.write("# Session Log\n\n")
                for event in self.session_log:
                    ts = event["timestamp"]
                    etype = event["event"]
                    content = event["data"].get("content", json.dumps(event["data"], ensure_ascii=False))
                    f.write(f"## {ts} - {etype}\n")
                    f.write(f"{content}\n\n")
        print(f"[Session log saved to {filename}]")
