import faiss
import json
import os
import numpy as np
from typing import List
from openai import OpenAI

class VectorStore:
    def __init__(self, client: OpenAI, embedding_model: str, storage_path: str = "kb.json") -> None:
        self.client = client
        self.embedding_model = embedding_model
        self.index = faiss.IndexFlatIP(1536)
        self.texts: List[str] = []
        self.storage_path = storage_path

        if os.path.exists(self.storage_path):
            self._load()

    def add_text(self, text: str) -> None:
        embedding = self._get_embedding(text)
        norm = np.linalg.norm(embedding)
        if norm == 0:
            return

        normed = (embedding / norm).astype(np.float32)
        normed_2d = normed[np.newaxis, :]  # shape (1, 1536)

        self.index.add(normed_2d)
        self.texts.append(text)
        self._save(text, normed.tolist())

    def search(self, query: str, top_k: int = 3) -> List[str]:
        embedding = self._get_embedding(query)
        norm = np.linalg.norm(embedding)
        if norm == 0 or self.index.ntotal == 0:
            return ["Nothing found."]

        query_vec = (embedding / norm).astype(np.float32).reshape(1, -1)
        _, indices = self.index.search(query_vec, top_k)

        return [self.texts[i] for i in indices[0] if i < len(self.texts)]

    def _get_embedding(self, text: str) -> np.ndarray:
        response = self.client.embeddings.create(
            model=self.embedding_model,
            input=[text]
        )
        return np.array(response.data[0].embedding, dtype=np.float32)

    def _save(self, text: str, embedding: List[float]) -> None:
        record = {"text": text, "embedding": embedding}
        data = []

        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except json.JSONDecodeError:
                pass

        data.append(record)

        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def _load(self) -> None:
        with open(self.storage_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            for item in data:
                text = item["text"]
                embedding = np.array(item["embedding"], dtype=np.float32).reshape(1, -1)
                self.index.add(embedding)
                self.texts.append(text)
