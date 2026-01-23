import requests
import os
from typing import List, Optional
from dotenv import load_dotenv

load_dotenv()

class EmbeddingService:
    def __init__(self, api_key: Optional[str] = None):
        """
        Lightweight Embedding Service using Jina AI Cloud API.
        Zero local inference required.
        """
        self.api_key = api_key or os.getenv("JINA_API_KEY")
        self.api_url = "https://api.jina.ai/v1/embeddings"
        self.model = "jina-embeddings-v3" # Latest cloud model

    def embed_text(self, text: str) -> List[float]:
        """Generate embedding for a single text via Cloud API."""
        if not self.api_key:
            raise ValueError("JINA_API_KEY not found in .env")

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        data = {
            "model": self.model,
            "input": [text]
        }
        
        response = requests.post(self.api_url, headers=headers, json=data)
        response.raise_for_status()
        
        return response.json()["data"][0]["embedding"]

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for a batch of texts via Cloud API."""
        if not self.api_key:
            raise ValueError("JINA_API_KEY not found in .env")

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        data = {
            "model": self.model,
            "input": texts
        }
        
        response = requests.post(self.api_url, headers=headers, json=data)
        response.raise_for_status()
        
        results = response.json()["data"]
        # Sort by index to maintain original order
        sorted_results = sorted(results, key=lambda x: x["index"])
        return [r["embedding"] for r in sorted_results]
