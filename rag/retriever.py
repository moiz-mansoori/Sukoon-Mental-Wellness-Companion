from typing import List, Dict, Any, Optional
import os
import json
from .embeddings import EmbeddingService
from .vector_store import VectorStore

class WellnessRetriever:
    def __init__(self, embedding_service: EmbeddingService, vector_store: VectorStore):
        """
        Initialize the retriever.
        """
        self.embedding_service = embedding_service
        self.vector_store = vector_store

    def retrieve(self, query: str, n_results: int = 2) -> List[Dict[str, Any]]:
        """
        Retrieve relevant wellness wisdom.
        """
        query_embedding = self.embedding_service.embed_text(query)
        results = self.vector_store.search(query_embedding, n_results=n_results)
        return results

    def format_context_for_prompt(self, results: List[Dict[str, Any]]) -> str:
        """
        Format retrieved results into a context string for the LLM.
        """
        if not results:
            return ""
            
        context_parts = []
        for res in results:
            content = res["content"]
            # Treat context as lived wisdom/insights
            context_parts.append(content)
            
        return "\n\n".join(context_parts)
