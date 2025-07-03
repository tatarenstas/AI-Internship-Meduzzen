import os
import uuid

from openai import OpenAI
from datetime import datetime
from typing import List, Tuple

from vector_store import VectorStore


class SemanticSearchApp:
    def __init__(self, client: OpenAI) -> None:
        self.store = VectorStore(client)
        self.client = client
        self.log_path = self._init_log_file()

    def _init_log_file(self) -> str:
        os.makedirs("logs", exist_ok=True)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        unique_id = uuid.uuid4()
        path = f"logs/session_{timestamp}_{unique_id}.md"
        with open(path, "w", encoding="utf-8") as f:
            f.write(f"# Chat Log – {timestamp}\n\n")
        return path

    def _log_to_file(self, question: str, answer: str, context: List[Tuple[str, str]]) -> None:
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(f"## Question:\n{question}\n\n")
            f.write("### Top Matches:\n")
            for i, (doc_id, text) in enumerate(context, 1):
                f.write(f"- **Source #{i} ({doc_id})**: {text}\n")
            f.write("\n## GPT Answer:\n")
            f.write(answer + "\n\n---\n\n")

    def query_gpt(self, context: List[Tuple[str, str]], question: str) -> str:
        labeled_context = "\n".join(
            [f"Source #{i+1}: {text}" for i, (_, text) in enumerate(context)]
        )

        messages = [
            {"role": "system", "content": "You are a helpful assistant. Answer based on the labeled sources."},
            {"role": "user", "content": f"{labeled_context}\n\nQuestion: {question}"}
        ]
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=messages
        )
        return response.choices[0].message.content

    def run_from_file(self, filepath: str) -> None:
        self._load_corpus_from_file(filepath)

        print("[Semantic Search Ready] Type a question or 'exit' to quit.\n")
        while True:
            query = input("You: ")
            if query.lower() in ["exit", "quit"]:
                print(f"Session logged in {self.log_path}")
                break

            results = self.store.search(query)
            print("\n→ Top 3 Matches:")
            for i, (doc_id, text) in enumerate(results, 1):
                print(f"[{i}] ({doc_id}) {text}")

            print("\n→ Sending to GPT-4o...")
            answer = self.query_gpt(results, query)
            print("\n> GPT:", answer)

            self._log_to_file(query, answer, results)

    def _load_corpus_from_file(self, path: str) -> None:
        if not os.path.exists(path):
            raise FileNotFoundError(f"Corpus file '{path}' not found.")

        with open(path, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]

        for idx, line in enumerate(lines):
            self.store.add_text(f"doc{idx+1}", line)

        print(f"Loaded {len(lines)} documents from '{path}' into FAISS.")
