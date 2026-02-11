"""Standalone script to trigger the ingestion pipeline."""
from src.config import init_llm_settings
from src.services.ingestion import IngestionService
from src.services.vector_store import VectorDBService


def main():
    """Entry point for database ingestion."""
    init_llm_settings()

    # Dependency Injection
    db_service = VectorDBService()
    ingestion_service = IngestionService(db_service=db_service)

    # Run the ETL pipeline
    ingestion_service.run_pipeline()

if __name__ == "__main__":
    main()
