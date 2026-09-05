import os
import requests
import chromadb

WORKSPACE_DIR = "/opt/spoil"
DB_PATH = "/opt/spoil/vector_db"

def get_embedding(text):
    try:
        response = requests.post(
            "http://localhost:11434/api/embeddings",
            json={"model": "nomic-embed-text", "prompt": text},
            timeout=10
        )
        return response.json().get("embedding", [])
    except Exception as e:
        print(f"Embedding error: {e}")
        return []

def chunk_text(text, chunk_size=400):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

def ingest_workspace():
    print(f"Connecting to ChromaDB at {DB_PATH}...")
    client = chromadb.PersistentClient(path=DB_PATH)
    collection = client.get_or_create_collection(name="linux_workspace")

    print("Scanning python and markdown files (English only)...")
    doc_id = 0
    
    batch_embeddings = []
    batch_documents = []
    batch_metadatas = []
    batch_ids = []
    BATCH_SIZE = 100  

    for root, _, files in os.walk(WORKSPACE_DIR):
        for file in files:
            if file.endswith((".py", ".md")):
                filepath = os.path.join(root, file)

                skip_folders = ["venv", "__pycache__", ".git", "assets", "images", ".github", "vector_db"]
                if file == "rag.py" or any(x in filepath for x in skip_folders):
                    continue

                lang_codes = ["/es/", "/fr/", "/tr/", "/zh/", "/ja/", "/ru/", "/vn/", "/it/", "/de/"]
                if any(lang in filepath for lang in lang_codes):
                    continue

                # Ikkada print statement pettam, so file progress telustundi
                print(f"Processing: {filepath}")

                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        content = f.read()

                    chunks = chunk_text(content)
                    for chunk in chunks:
                        embedding = get_embedding(chunk)
                        if embedding:
                            batch_embeddings.append(embedding)
                            batch_documents.append(chunk)
                            batch_metadatas.append({"source": filepath})
                            batch_ids.append(f"chunk_{doc_id}")
                            doc_id += 1

                            if len(batch_embeddings) >= BATCH_SIZE:
                                collection.add(
                                    embeddings=batch_embeddings,
                                    documents=batch_documents,
                                    metadatas=batch_metadatas,
                                    ids=batch_ids
                                )
                                batch_embeddings = []
                                batch_documents = []
                                batch_metadatas = []
                                batch_ids = []
                except Exception as e:
                    print(f"Could not read {filepath}: {e}")

    if batch_embeddings:
        collection.add(
            embeddings=batch_embeddings,
            documents=batch_documents,
            metadatas=batch_metadatas,
            ids=batch_ids
        )

    print(f"\nDone! Successfully ingested {doc_id} chunks into the vector database rapidly.")

if __name__ == "__main__":
    ingest_workspace()
