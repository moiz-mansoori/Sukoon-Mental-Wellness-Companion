import os
import requests
from typing import List, Optional
from huggingface_hub import InferenceClient
from config.settings import EMBEDDING_MODEL

class EmbeddingService:
    def __init__(self, model_name: Optional[str] = None):
        """
        Local Embedding Service using Sentence Transformers.
        Runs locally on your machine or server.
        No API key required.
        """
        self.model_name = model_name or "sentence-transformers/all-MiniLM-L6-v2"
        self.hf_token = os.getenv("HF_TOKEN")
        
        if self.hf_token:
            self.client = InferenceClient(token=self.hf_token)
            self.use_api = True
            print(f"Using Hugging Face Inference API ({self.model_name})")
        else:
            self.use_api = False
            print("HF_TOKEN not found. Falling back to local SentenceTransformers.")
            try:
                from sentence_transformers import SentenceTransformer
                self.model = SentenceTransformer(model_name or EMBEDDING_MODEL)
            except Exception as e:
                print(f"Error loading local embedding model: {e}")
                self.model = None

    def embed_text(self, text: str) -> List[float]:
        """Generate embedding for a single text locally."""
        if self.use_api:
            try:
                # feature_extraction returns the embedding as a list of floats
                embedding = self.client.feature_extraction(text, model=self.model_name)
                # Ensure it's returned as a list
                if hasattr(embedding, "tolist"):
                    return embedding.tolist()
                return list(embedding)
            except Exception as e:
                print(f"HF API Error: {e}. Falling back to local.")
                self.use_api = False
            
        if not self.model:
            raise ValueError("Embedding model not initialized.")
        
        embedding = self.model.encode(text)
        return embedding.tolist()

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for a batch of texts locally."""
        if self.use_api:
            try:
                embeddings = self.client.feature_extraction(texts, model=self.model_name)
                # Hugging Face returns a list of lists for batches
                return [list(e) for e in embeddings]
            except Exception as e:
                print(f"HF API Error: {e}. Falling back to local.")
                self.use_api = False

        if not self.model:
            raise ValueError("Embedding model not initialized.")
            
        embeddings = self.model.encode(texts)
        return embeddings.tolist()
