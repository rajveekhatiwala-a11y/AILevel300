"""
FastAPI Main Application
Enterprise RAG Document Q&A System
"""
from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging
from typing import Optional

from app.config import settings
from app.rag_pipeline import RAGPipeline

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Enterprise RAG Document Q&A System",
    description="Intelligent Document Q&A using Azure AI Foundry, AI Search, and LangChain",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Initialize RAG pipeline (lazy loading)
rag_pipeline: Optional[RAGPipeline] = None


# Pydantic models
class QueryRequest(BaseModel):
    """Request model for queries"""
    question: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "question": "What is the company vacation policy?"
            }
        }


class QueryResponse(BaseModel):
    """Response model for queries"""
    answer: str
    sources: list[str]
    context_chunks: int


class IngestionResponse(BaseModel):
    """Response model for document ingestion"""
    status: str
    message: str


class HealthResponse(BaseModel):
    """Response model for health check"""
    status: str
    message: str


# Helper function to get RAG pipeline
def get_rag_pipeline() -> RAGPipeline:
    """Get or initialize RAG pipeline"""
    global rag_pipeline
    if rag_pipeline is None:
        logger.info("Initializing RAG pipeline...")
        rag_pipeline = RAGPipeline()
    return rag_pipeline


# Routes
@app.get("/")
async def root(request: Request):
    """Serve the main UI"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "RAG system is running"
    }


@app.post("/api/setup-index")
async def setup_index():
    """Initialize Azure AI Search index"""
    try:
        pipeline = get_rag_pipeline()
        pipeline.create_search_index()
        
        return {
            "status": "success",
            "message": "Search index created successfully"
        }
    except Exception as e:
        logger.error(f"Error creating index: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/ingest", response_model=IngestionResponse)
async def ingest_documents():
    """Ingest documents from the configured path"""
    try:
        pipeline = get_rag_pipeline()
        
        # First create/update the index
        pipeline.create_search_index()
        
        # Then ingest documents
        pipeline.ingest_documents()
        
        return {
            "status": "success",
            "message": "Documents ingested successfully"
        }
    except Exception as e:
        logger.error(f"Error ingesting documents: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/query", response_model=QueryResponse)
async def query_documents(request: QueryRequest):
    """Query documents using RAG pipeline"""
    try:
        if not request.question or not request.question.strip():
            raise HTTPException(status_code=400, detail="Question cannot be empty")
        
        pipeline = get_rag_pipeline()
        result = pipeline.query(request.question)
        
        return {
            "answer": result['answer'],
            "sources": result['sources'],
            "context_chunks": result['context_chunks']
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/config")
async def get_config():
    """Get system configuration (non-sensitive data)"""
    return {
        "document_path": settings.document_path,
        "chunk_size": settings.chunk_size,
        "chunk_overlap": settings.chunk_overlap,
        "top_k_results": settings.top_k_results,
        "azure_configured": settings.validate_azure_config()
    }


# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize application on startup"""
    logger.info("Starting Enterprise RAG Document Q&A System")
    logger.info(f"Document path: {settings.document_path}")
    logger.info(f"Azure configured: {settings.validate_azure_config()}")
    
    if not settings.validate_azure_config():
        logger.warning("Azure configuration incomplete. Please update .env file.")


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Shutting down Enterprise RAG Document Q&A System")


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host=settings.app_host,
        port=settings.app_port,
        reload=settings.debug
    )
