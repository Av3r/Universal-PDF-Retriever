"""RAG Engine service handling search, memory, and citations."""
from llama_index.core import VectorStoreIndex
from llama_index.core.query_engine import CitationQueryEngine
from llama_index.core.chat_engine import CondenseQuestionChatEngine
from src.services.vector_store import VectorDBService
from llama_index.core.postprocessor import SimilarityPostprocessor

class RAGEngineService:
    """Manages retrieval logic and chat engine generation."""

    def __init__(self, db_service: VectorDBService) -> None:
        self.db_service = db_service

    def get_chat_engine(self) -> CondenseQuestionChatEngine:
        """Creates a RAG engine supporting chat history and strict citations."""
        vector_store = self.db_service.get_vector_store()
        
        # Load the index from the existing vector store without re-parsing
        index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
        
        # Step 1: Engine that answers single queries with source citations
        query_engine = CitationQueryEngine.from_args(
            index,
            similarity_top_k=8,
            citation_chunk_size=512,
            node_postprocessors=[
                # Rejects all chunks whose similarity to the question is less than, for example, 55%
                SimilarityPostprocessor(similarity_cutoff=0.55) # 0.75 was too strict for data, which can be noisy. Adjust as needed.
            ]
        )
        
        # Step 2: Wrap the query engine with memory (Context Awareness)
        # CondenseQuestion rewrites contextual questions (e.g., "And what about 2023?")
        # into standalone queries before hitting the vector database.
        chat_engine = CondenseQuestionChatEngine.from_defaults(
            query_engine=query_engine,
            verbose=True
        )
        
        return chat_engine