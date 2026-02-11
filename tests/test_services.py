"""Basic unit tests verifying the correctness of services and configuration."""
import pytest
from unittest.mock import patch, MagicMock
from src.config import config
from src.services.vector_store import VectorDBService
from src.services.rag_engine import RAGEngineService

def test_config_loads_defaults():
    """Checks if Pydantic correctly loads default collection names."""
    assert config.qdrant_collection_name == "universal_rag_collection"
    assert config.qdrant_url is not None

@patch("src.services.vector_store.qdrant_client.QdrantClient")
@patch("src.services.vector_store.AsyncQdrantClient")
def test_vector_db_service_initialization(MockAsyncClient, MockClient):
    """
    Tests if the database service correctly initializes Qdrant clients
    (without connecting to a physical database - using Mocks).
    """
    # Initialize the service
    service = VectorDBService()
    
    # Verification
    assert service.collection == config.qdrant_collection_name
    # Ensure that the clients were called with the correct URL
    MockClient.assert_called_once_with(url=config.qdrant_url)
    MockAsyncClient.assert_called_once_with(url=config.qdrant_url)

@patch("src.services.vector_store.QdrantVectorStore")
@patch("src.services.vector_store.qdrant_client.QdrantClient")
@patch("src.services.vector_store.AsyncQdrantClient")
def test_rag_engine_service_dependency_injection(MockAsync, MockSync, MockStore):
    """Checks if RAGEngineService correctly accepts the injected database dependency."""
    db_service = VectorDBService()
    rag_service = RAGEngineService(db_service=db_service)
    
    # Verify that the injected service is exactly the same object
    assert rag_service.db_service == db_service