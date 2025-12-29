"""
RAG Pipeline Implementation
Integrates Azure OpenAI, Azure AI Search, and LangChain
"""
import os
import logging
from typing import List, Dict, Optional, Tuple
import json

# Azure imports
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex,
    SimpleField,
    SearchableField,
    SearchField,
    SearchFieldDataType,
    VectorSearch,
    HnswAlgorithmConfiguration,
    VectorSearchProfile,
    SemanticConfiguration,
    SemanticSearch,
    SemanticPrioritizedFields,
    SemanticField
)
from azure.core.credentials import AzureKeyCredential

# LangChain imports
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores.azuresearch import AzureSearch
from langchain_core.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.docstore.document import Document

from app.config import settings
from app.document_loader import DocumentLoader

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RAGPipeline:
    """RAG Pipeline for document Q&A using LangChain"""
    
    def __init__(self):
        """Initialize RAG pipeline with Azure services and LangChain"""
        self.settings = settings
        
        # Initialize LangChain Azure OpenAI LLM
        self.llm = AzureChatOpenAI(
            azure_endpoint=self.settings.azure_openai_endpoint,
            api_key=self.settings.azure_openai_api_key,
            api_version=self.settings.azure_openai_api_version,
            deployment_name=self.settings.azure_openai_deployment_name,
            temperature=self.settings.temperature,
            max_tokens=self.settings.max_tokens
        )
        
        # Initialize LangChain Azure OpenAI Embeddings
        self.embeddings = AzureOpenAIEmbeddings(
            azure_endpoint=self.settings.azure_openai_endpoint,
            api_key=self.settings.azure_openai_api_key,
            api_version=self.settings.azure_openai_api_version,
            deployment=self.settings.azure_openai_embedding_deployment
        )
        
        # Initialize Azure Search clients (for index management)
        self.search_index_client = SearchIndexClient(
            endpoint=self.settings.azure_search_endpoint,
            credential=AzureKeyCredential(self.settings.azure_search_api_key)
        )
        
        # Initialize LangChain text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.settings.chunk_size,
            chunk_overlap=self.settings.chunk_overlap,
            separators=["\n\n", "\n", " ", ""]
        )
        
        # Initialize document loader
        self.document_loader = DocumentLoader(self.settings.document_path)
        
        # Vector store will be initialized during ingestion
        self.vector_store = None
        self.qa_chain = None
        
        logger.info("RAG Pipeline initialized with LangChain")
    
    def create_search_index(self):
        """Create Azure AI Search index with vector search capabilities"""
        try:
            # Define the index schema
            fields = [
                SimpleField(name="id", type=SearchFieldDataType.String, key=True),
                SearchableField(name="content", type=SearchFieldDataType.String),
                SearchableField(name="metadata", type=SearchFieldDataType.String),  # LangChain metadata field
                SearchableField(name="source", type=SearchFieldDataType.String, filterable=True),
                SimpleField(name="file_path", type=SearchFieldDataType.String),
                SimpleField(name="file_type", type=SearchFieldDataType.String, filterable=True),
                SimpleField(name="chunk_id", type=SearchFieldDataType.String),
                SimpleField(name="chunk_index", type=SearchFieldDataType.Int32),
                SearchField(
                    name="content_vector",
                    type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
                    searchable=True,
                    vector_search_dimensions=1536,  # Ada-002 embedding size
                    vector_search_profile_name="vector-profile"
                )
            ]
            
            # Configure vector search
            vector_search = VectorSearch(
                algorithms=[
                    HnswAlgorithmConfiguration(name="hnsw-config")
                ],
                profiles=[
                    VectorSearchProfile(
                        name="vector-profile",
                        algorithm_configuration_name="hnsw-config"
                    )
                ]
            )
            
            # Configure semantic search
            semantic_config = SemanticConfiguration(
                name="semantic-config",
                prioritized_fields=SemanticPrioritizedFields(
                    title_field=None,
                    content_fields=[SemanticField(field_name="content")]
                )
            )
            
            semantic_search = SemanticSearch(configurations=[semantic_config])
            
            # Create the index
            index = SearchIndex(
                name=self.settings.azure_search_index_name,
                fields=fields,
                vector_search=vector_search,
                semantic_search=semantic_search
            )
            
            result = self.search_index_client.create_or_update_index(index)
            logger.info(f"Search index '{result.name}' created successfully")
            
        except Exception as e:
            logger.error(f"Error creating search index: {str(e)}")
            raise
    
    def delete_search_index(self):
        """Delete the Azure AI Search index"""
        try:
            self.search_index_client.delete_index(self.settings.azure_search_index_name)
            logger.info(f"Search index '{self.settings.azure_search_index_name}' deleted successfully")
        except Exception as e:
            logger.warning(f"Could not delete search index: {str(e)}")
    
    def ingest_documents(self):
        """Load, chunk, embed, and index documents using LangChain"""
        try:
            # Recreate index to ensure it has correct schema
            logger.info("Recreating search index with correct schema...")
            self.delete_search_index()
            self.create_search_index()
            
            # Load documents
            logger.info("Loading documents...")
            documents = self.document_loader.load_all_documents()
            
            if not documents:
                logger.warning("No documents found to ingest")
                return
            
            # Get document stats
            stats = self.document_loader.get_document_stats(documents)
            logger.info(f"Document stats: {stats}")
            
            # Convert to LangChain Document format
            langchain_docs = []
            for doc in documents:
                langchain_docs.append(Document(
                    page_content=doc['content'],
                    metadata={
                        'source': doc['source'],
                        'file_path': doc['file_path'],
                        'file_type': doc['file_type']
                    }
                ))
            
            # Split documents using LangChain text splitter
            logger.info("Chunking documents with LangChain...")
            chunks = self.text_splitter.split_documents(langchain_docs)
            logger.info(f"Created {len(chunks)} chunks from {len(documents)} documents")
            
            # Initialize vector store with Azure Search
            logger.info("Indexing documents into Azure AI Search with LangChain...")
            self.vector_store = AzureSearch(
                azure_search_endpoint=self.settings.azure_search_endpoint,
                azure_search_key=self.settings.azure_search_api_key,
                index_name=self.settings.azure_search_index_name,
                embedding_function=self.embeddings.embed_query
            )
            
            # Add documents to vector store
            self.vector_store.add_documents(documents=chunks)
            
            # Create QA chain
            self._create_qa_chain()
            
            logger.info(f"Successfully ingested {len(documents)} documents ({len(chunks)} chunks)")
            
        except Exception as e:
            logger.error(f"Error ingesting documents: {str(e)}", exc_info=True)
            raise
    
    def _create_qa_chain(self):
        """Create LangChain QA chain with custom prompt"""
        try:
            # Create custom prompt template
            prompt_template = """You are an intelligent assistant helping users find information from company documents.
Use the following context to answer the question. If the answer is not in the context, say "I don't have enough information to answer that question."

Context:
{context}

Question: {question}

Provide a clear, detailed answer based on the context. Always cite the sources you used."""
            
            PROMPT = PromptTemplate(
                template=prompt_template,
                input_variables=["context", "question"]
            )
            
            # Create RetrievalQA chain
            self.qa_chain = RetrievalQA.from_chain_type(
                llm=self.llm,
                chain_type="stuff",
                retriever=self.vector_store.as_retriever(
                    search_type="hybrid",
                    search_kwargs={"k": self.settings.top_k_results}
                ),
                chain_type_kwargs={"prompt": PROMPT},
                return_source_documents=True
            )
            
            logger.info("QA chain created successfully")
            
        except Exception as e:
            logger.error(f"Error creating QA chain: {str(e)}", exc_info=True)
            raise
    
    def _init_vector_store_for_query(self):
        """Initialize vector store for querying (when not ingesting)"""
        try:
            if self.vector_store is None:
                self.vector_store = AzureSearch(
                    azure_search_endpoint=self.settings.azure_search_endpoint,
                    azure_search_key=self.settings.azure_search_api_key,
                    index_name=self.settings.azure_search_index_name,
                    embedding_function=self.embeddings.embed_query
                )
                self._create_qa_chain()
        except Exception as e:
            logger.error(f"Error initializing vector store: {str(e)}", exc_info=True)
            raise
    
    def query(self, question: str) -> Dict[str, any]:
        """
        Complete RAG query pipeline using LangChain
        
        Args:
            question: User question
            
        Returns:
            Dictionary with answer, sources, and metadata
        """
        try:
            logger.info(f"Processing query: {question}")
            
            # Initialize vector store if not already done
            self._init_vector_store_for_query()
            
            # Run the QA chain
            result = self.qa_chain({"query": question})
            
            # Extract answer and sources
            answer = result['result']
            source_documents = result.get('source_documents', [])
            
            # Extract unique sources from metadata
            sources = list(set([
                doc.metadata.get('source', 'Unknown') 
                for doc in source_documents
            ]))
            
            logger.info(f"Query processed successfully with {len(source_documents)} source chunks")
            
            return {
                'answer': answer,
                'sources': sources,
                'context_chunks': len(source_documents)
            }
            
        except Exception as e:
            logger.error(f"Error processing query: {str(e)}", exc_info=True)
            return {
                'answer': f"An error occurred: {str(e)}",
                'sources': [],
                'context_chunks': 0
            }
