import time
import requests
import chromadb
import statistics

DB_PATH = "./vector_db"
COLLECTION_NAME = "linux_workspace"

EMBED_URL = "http://localhost:11434/api/embeddings"
EMBED_MODEL = "nomic-embed-text"

TEST_QUERIES = [
    "How can I enumerate SUID binaries on Linux?",
    "How do I find writable files and directories?",
    "How can I enumerate sudo permissions?",
    "How do I perform Linux privilege escalation?",
    "How can I find credentials stored in configuration files?",
    "How do I enumerate cron jobs?",
    "How can I enumerate running processes?",
    "How do I discover open ports on a Linux machine?",
    "How can I enumerate users on a Linux system?",
    "How do I find SSH private keys?",
]


def get_embedding(text):
    start = time.perf_counter()

    response = requests.post(
        EMBED_URL,
        json={
            "model": EMBED_MODEL,
            "prompt": text
        },
        timeout=10
    )

    response.raise_for_status()

    elapsed = (time.perf_counter() - start) * 1000

    return response.json()["embedding"], elapsed


def search(collection, query, k):
    embedding, embedding_ms = get_embedding(query)

    start = time.perf_counter()

    results = collection.query(
        query_embeddings=[embedding],
        n_results=k,
        include=["documents", "metadatas", "distances"]
    )

    search_ms = (time.perf_counter() - start) * 1000

    return results, embedding_ms, search_ms


client = chromadb.PersistentClient(path=DB_PATH)
collection = client.get_collection(name=COLLECTION_NAME)

print("=" * 70)
print("SPOIL RAG BENCHMARK")
print("=" * 70)

print(f"Collection : {COLLECTION_NAME}")
print(f"Documents  : {collection.count()}")

print()


for k in [2, 4, 6]:

    print("\n" + "=" * 70)
    print(f"TOP-K = {k}")
    print("=" * 70)

    embedding_times = []
    search_times = []

    for i, query in enumerate(TEST_QUERIES, 1):

        try:
            results, embedding_ms, search_ms = search(
                collection,
                query,
                k
            )

            embedding_times.append(embedding_ms)
            search_times.append(search_ms)

            documents = results["documents"][0]
            metadatas = results["metadatas"][0]
            distances = results["distances"][0]

            print(f"\n[{i}] {query}")

            print(
                f"Embedding: {embedding_ms:.1f} ms | "
                f"Chroma: {search_ms:.1f} ms"
            )

            for rank, (doc, meta, distance) in enumerate(
                zip(documents, metadatas, distances),
                1
            ):

                source = meta.get("source", "unknown")

                snippet = (
                    doc.replace("\n", " ")
                    .replace("\r", " ")
                )

                if len(snippet) > 180:
                    snippet = snippet[:180] + "..."

                print(f"\n  #{rank}")
                print(f"  Distance: {distance:.4f}")
                print(f"  Source:   {source}")
                print(f"  Text:     {snippet}")

        except Exception as e:
            print(f"\nERROR: {e}")

    print("\n" + "-" * 70)

    print(
        f"Embedding avg : "
        f"{statistics.mean(embedding_times):.1f} ms"
    )

    print(
        f"Embedding p95 : "
        f"{statistics.quantiles(embedding_times, n=20)[18]:.1f} ms"
    )

    print(
        f"Chroma avg    : "
        f"{statistics.mean(search_times):.1f} ms"
    )

    print(
        f"Chroma p95    : "
        f"{statistics.quantiles(search_times, n=20)[18]:.1f} ms"
    )

    print(
        f"Total avg     : "
        f"{statistics.mean([
            a + b
            for a, b in zip(embedding_times, search_times)
        ]):.1f} ms"
    )
