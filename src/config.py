"""Application configuration module using Pydantic."""
from pydantic_settings import BaseSettings, SettingsConfigDict
from llama_index.core import Settings
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
import os

class AppConfig(BaseSettings):
    """Main configuration class, reads variables from .env file."""
    openai_api_key: str
    llama_cloud_api_key: str
    qdrant_url: str = "http://localhost:6333"
    qdrant_collection_name: str = "universal_rag_collection"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

config = AppConfig()

# Universal prompt for the LLM
SYSTEM_PROMPT = """
You are a highly precise analytical assistant.
Your goal is to answer user questions strictly based on the provided document context.

RULES:
1. Do not hallucinate. If the answer is not present in the context, explicitly state: "I cannot find this information in the provided document."
2. Every factual or numerical claim must be supported by a direct quote from the text.
3. Be concise and professional.
4. IMPORTANT: Always generate your final response in Polish, regardless of the prompt language.
"""

def init_llm_settings() -> None:
    """Initialize global LLM and Embedding models for LlamaIndex."""
    os.environ["OPENAI_API_KEY"] = config.openai_api_key
    
    # Fast, cheap, and effective embedding model
    Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")
    
    # Cost-effective yet highly capable model for text generation
    Settings.llm = OpenAI(
        model="gpt-4o-mini",
        temperature=0,  # 0 ensures deterministic and analytical answers
        system_prompt=SYSTEM_PROMPT
    )