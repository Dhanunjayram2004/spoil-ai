import os
import requests
import chromadb

class MemoryManager:
    def __init__(self, db_path="./vector_db", collection_name="linux_workspace"):
        # Initialize the persistent ChromaDB client inside your project folder
        self.chroma_client = chromadb.PersistentClient(path=db_path)
        self.collection = self.chroma_client.get_or_create_collection(name=collection_name)
        
        # Ollama local embedding endpoint
        self.embed_url = "http://localhost:11434/api/embeddings"
        self.embedding_model = "nomic-embed-text"

    def _get_embedding(self, text: str) -> list:
        """Helper to fetch vector embeddings from the local Ollama instance."""
        try:
            response = requests.post(
                self.embed_url,
                json={"model": self.embedding_model, "prompt": text},
                timeout=10
            )
            response.raise_for_status()
            return response.json().get("embedding", [])
        except Exception as e:
            print(f"[Error generating embedding]: {e}")
            return []

    def retrieve_rag_context(self, query: str, n_results: int = 2) -> str:
        """
        Embeds the user query, searches the vector database, 
        and returns formatted text context for the agent's prompt.
        """
        query_vector = self._get_embedding(query)
        
        if not query_vector:
            return ""

        try:
            # Query ChromaDB for the top matching document chunks
            results = self.collection.query(
                query_embeddings=[query_vector],
                n_results=n_results
            )
            
            documents = results.get("documents", [[]])[0]
            
            if not documents:
                return ""
            
            # Format the retrieved chunks into a clean string block for the LLM
            return "\n---\n".join(documents)
          

        except Exception as e:
            print(f"[Error retrieving RAG context]: {e}")
            return ""
