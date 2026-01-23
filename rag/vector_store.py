import chromadb
from chromadb.config import Settings
import os
from typing import List, Dict, Any, Optional

class VectorStore:
    def __init__(self, persist_directory: str = "./chroma_db"):
        """
        Initialize ChromaDB client.
        """
        self.persist_directory = persist_directory
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collection = None

    def initialize_collection(self, name: str = "sukoon_wisdom"):
        """
        Initialize or get the collection.
        """
        self.collection = self.client.get_or_create_collection(
            name=name,
            metadata={"hnsw:space": "cosine"}
        )

    def add_documents(self, documents: List[Dict[str, Any]], embeddings: List[List[float]]):
        """
        Add documents to the collection.
        """
        if not self.collection:
            self.initialize_collection()
        
        ids = [doc["id"] for doc in documents]
        metadatas = [doc["metadata"] for doc in documents]
        documents_text = [doc["content"] for doc in documents]
        
        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            metadatas=metadatas,
            documents=documents_text
        )

    def search(self, query_embedding: List[float], n_results: int = 3) -> List[Dict[str, Any]]:
        """
        Search for similar documents.
        """
        if not self.collection:
            self.initialize_collection()
            
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            include=["documents", "metadatas", "distances"]
        )
        
        formatted_results = []
        if results["documents"]:
            for i in range(len(results["documents"][0])):
                formatted_results.append({
                    "content": results["documents"][0][i],
                    "metadata": results["metadatas"][0][i],
                    "distance": results["distances"][0][i]
                })
        
        return formatted_results
