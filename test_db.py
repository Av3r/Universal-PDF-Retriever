import qdrant_client
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.qdrant import QdrantVectorStore

from src.config import config, init_llm_settings


def test_retrieval():
    print("Initializing LLM and Embeddings...")
    init_llm_settings()

    print("Connection to Qdrant...")
    client = qdrant_client.QdrantClient(url="http://localhost:6333")
    vector_store = QdrantVectorStore(client=client, collection_name=config.qdrant_collection_name)

    index = VectorStoreIndex.from_vector_store(vector_store=vector_store)

    # Create a direct retriever (data fetcher) - without chat, just the search engine
    retriever = index.as_retriever(similarity_top_k=5)

    #query = "Jaka jest strategia banku?"
    query = "jaki był depozyt na koniec 2024 r."
    print(f"\nSzukam w bazie zapytania: '{query}'")

    nodes = retriever.retrieve(query)

    if not nodes:
        print("❌ ERROR: No results returned from the database! Vectors do not match.")
    else:
        print(f"✅ SUCCESS! Found {len(nodes)} results:")
        for idx, node in enumerate(nodes, 1):
            score = node.score
            page = node.node.metadata.get('page_label', 'N/A')
            print(f"\n--- RESULT {idx} (Score: {score:.4f}, Page: {page}) ---")
            print(node.node.get_text()[:200] + "...")

if __name__ == "__main__":
    test_retrieval()
