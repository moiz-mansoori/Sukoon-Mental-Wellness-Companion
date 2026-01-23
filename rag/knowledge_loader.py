import os
import json
from typing import List, Dict, Any
from .embeddings import EmbeddingService
from .vector_store import VectorStore

def load_knowledge_base(directory: str) -> List[Dict[str, Any]]:
    """
    Load knowledge base from JSON files.
    """
    documents = []
    if not os.path.exists(directory):
        return []
        
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            file_path = os.path.join(directory, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                category = filename.replace(".json", "")
                if isinstance(data, list):
                    for i, item in enumerate(data):
                        documents.append({
                            "id": f"{category}_{i}",
                            "content": item["content"],
                            "metadata": {
                                "category": category,
                                "tags": ", ".join(item.get("tags", [])),
                                **{k: v for k, v in item.items() if k not in ["content", "tags"]}
                            }
                        })
    return documents

def index_knowledge_base(vector_store: VectorStore, embedding_service: EmbeddingService, knowledge_dir: str):
    """
    Index all documents from the knowledge base directory.
    """
    documents = load_knowledge_base(knowledge_dir)
    if not documents:
        return
        
    embeddings = embedding_service.embed_batch([doc["content"] for doc in documents])
    vector_store.add_documents(documents, embeddings)
