"""Service responsible for parsing complex PDFs and loading vectors."""
from llama_parse import LlamaParse
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from src.services.vector_store import VectorDBService

class IngestionService:
    """Processes local documents and stores them in the vector database."""

    def __init__(self, db_service: VectorDBService, data_dir: str = "./data") -> None:
        self.db_service = db_service
        self.data_dir = data_dir

    def run_pipeline(self) -> None:
        """Main flow: Parse (LlamaParse) -> Chunking -> Embedding -> Vector DB."""
        print(f"[*] Starting ingestion process from directory: {self.data_dir}")
        
        # Universal parsing instructions enforcing table extraction and noise reduction
        parsing_instructions = (
            "You are parsing a professional document. "
            "1. Extract all tables precisely into Markdown format. "
            "2. Strictly ignore and exclude page headers and page footers. "
            "3. Do not extract or include the table of contents. "
            "Focus only on the actual content and data."
        )

        parser = LlamaParse(
            result_type="markdown",
            parsing_instruction=parsing_instructions,
            verbose=True
        )
        
        file_extractor = {".pdf": parser}
        
        # Read documents from the target directory
        documents = SimpleDirectoryReader(
            self.data_dir, 
            file_extractor=file_extractor
        ).load_data()
        
        print(f"[*] Extracted {len(documents)} document chunks. Building index...")
        
        # Store embeddings into Qdrant
        storage_context = self.db_service.get_storage_context()
        VectorStoreIndex.from_documents(
            documents,
            storage_context=storage_context,
            show_progress=True
        )
        print("[+] Ingestion completed successfully. Database is ready!")