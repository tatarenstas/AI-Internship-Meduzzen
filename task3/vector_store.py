import faiss
import numpy as np
from typing import List, Tuple
from openai import OpenAI


class VectorStore:
    def __init__(self, client: OpenAI, dim: int = 1536) -> None:
        self.client = client
        self.model = "text-embedding-3-small"
        self.texts: List[str] = []
        self.ids: List[str] = []
        self.index = faiss.IndexFlatIP(dim)

    def _get_embedding(self, text: str) -> List[float]:
        response = self.client.embeddings.create(input=[text], model=self.model)
        return response.data[0].embedding

    def _normalize(self, vec: np.ndarray) -> np.ndarray:
        return vec / np.linalg.norm(vec)

    def add_text(self, doc_id: str, text: str) -> None:
        emb = self._get_embedding(text)
        norm = self._normalize(np.array(emb)).astype("float32")
        self.index.add(np.array([norm]))
        self.texts.append(text)
        self.ids.append(doc_id)

    def search(self, query: str, top_k: int = 3) -> List[Tuple[str, str]]:
        query_emb = self._get_embedding(query)
        norm_query = self._normalize(np.array(query_emb)).astype("float32")
        D, I = self.index.search(np.array([norm_query]), top_k)
        return [(self.ids[i], self.texts[i]) for i in I[0]]

    def get_by_id(self, idx: int) -> Tuple[str, str]:
        return self.ids[idx], self.texts[idx]
