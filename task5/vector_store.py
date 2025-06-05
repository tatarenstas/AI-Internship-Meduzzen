import faiss
import json
import os
import numpy as np
from typing import List
from openai import OpenAI

class VectorStore:
    def __init__(self, client: OpenAI, storage_path: str = "kb.json") -> None:
        self.client = client
        self.index = faiss.IndexFlatIP(1536)
        self.texts = []
        self.storage_path = storage_path

        if os.path.exists(self.storage_path):
            self._load()

    def add_text(self, text: str) -> None:
        emb = self._get_embedding(text)
        norm = np.linalg.norm(emb)
        if norm == 0:
            return
        normed = (emb / norm).astype("float32")
        self.index.add(np.array([normed]))
        self.texts.append(text)
        self._save(text, normed.tolist())

    def search(self, query: str, k: int = 1) -> List[str]:
        emb = self._get_embedding(query)
        norm = np.linalg.norm(emb)
        if norm == 0 or self.index.ntotal == 0:
            return ["Nothing found."]
        q = np.array([emb / norm]).astype("float32")
        D, I = self.index.search(q, k)
        return [self.texts[i] for i in I[0] if i < len(self.texts)]

    def _get_embedding(self, text: str) -> np.ndarray:
        res = self.client.embeddings.create(
            model="text-embedding-3-small",
            input=[text]
        )
        return np.array(res.data[0].embedding, dtype=np.float32)

    def _save(self, text: str, embedding: List[float]) -> None:
        record = {"text": text, "embedding": embedding}
        data = []
        if os.path.exists(self.storage_path):
            with open(self.storage_path, "r", encoding="utf-8") as f:
                try:
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
                embedding = np.array(item["embedding"], dtype=np.float32)
                self.index.add(np.array([embedding]))
                self.texts.append(text)
