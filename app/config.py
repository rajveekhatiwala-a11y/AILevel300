"""
Configuration Management for RAG System
"""
import os
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings(BaseSettings):
    """Application settings from environment variables"""
    
    # Azure OpenAI Configuration
    azure_openai_endpoint: str = os.getenv("AZURE_OPENAI_ENDPOINT", "")
    azure_openai_api_key: str = os.getenv("AZURE_OPENAI_API_KEY", "")
    azure_openai_deployment_name: str = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4")
    azure_openai_api_version: str = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")
    azure_openai_embedding_deployment: str = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT", "text-embedding-ada-002")
    
    # Azure AI Search Configuration
    azure_search_endpoint: str = os.getenv("AZURE_SEARCH_ENDPOINT", "")
    azure_search_api_key: str = os.getenv("AZURE_SEARCH_API_KEY", "")
    azure_search_index_name: str = os.getenv("AZURE_SEARCH_INDEX_NAME", "documents-index")
    
    # Document Configuration
    document_path: str = os.getenv("DOCUMENT_PATH", r"C:\Users\rajvkha\Downloads\DocumentQnA_RAG_DataSet\sample_docs")
    chunk_size: int = int(os.getenv("CHUNK_SIZE", "1000"))
    chunk_overlap: int = int(os.getenv("CHUNK_OVERLAP", "200"))
    
    # Application Configuration
    app_host: str = os.getenv("APP_HOST", "0.0.0.0")
    app_port: int = int(os.getenv("APP_PORT", "8000"))
    debug: bool = os.getenv("DEBUG", "True").lower() == "true"
    
    # Additional settings
    max_tokens: int = 1500
    temperature: float = 0.7
    top_k_results: int = 5
    
    class Config:
        env_file = ".env"
        case_sensitive = False
    
    def validate_azure_config(self) -> bool:
        """Validate Azure configuration"""
        required_fields = [
            self.azure_openai_endpoint,
            self.azure_openai_api_key,
            self.azure_search_endpoint,
            self.azure_search_api_key
        ]
        return all(required_fields)
    
    def get_document_path(self) -> Path:
        """Get document path as Path object"""
        return Path(self.document_path)

# Global settings instance
settings = Settings()
