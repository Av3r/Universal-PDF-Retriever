"""Service for Qdrant Vector Database operations."""
import qdrant_client
from llama_index.core import StorageContext
from llama_index.vector_stores.qdrant import QdrantVectorStore
from qdrant_client import AsyncQdrantClient

from src.config import config


class VectorDBService:
    """Manages connection and operations for the Qdrant database."""

    def __init__(self) -> None:
        # Standardowy klient (synchroniczny) - używany np. podczas wczytywania plików (ingest)
        self.client = qdrant_client.QdrantClient(url=config.qdrant_url)

        # NOWE: Asynchroniczny klient - używany przez Chainlit do chatu na żywo
        self.aclient = AsyncQdrantClient(url=config.qdrant_url)

        self.collection = config.qdrant_collection_name

    def get_vector_store(self) -> QdrantVectorStore:
        """Returns the QdrantVectorStore instance."""
        return QdrantVectorStore(
            client=self.client,
            aclient=self.aclient,  # Wstrzykujemy asynchronicznego klienta!
            collection_name=self.collection
        )

    def get_storage_context(self) -> StorageContext:
        """Returns the StorageContext required for index creation/loading."""
        return StorageContext.from_defaults(vector_store=self.get_vector_store())
