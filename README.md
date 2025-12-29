# Enterprise RAG Document Q&A System

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.9+-green)
![Azure](https://img.shields.io/badge/azure-ai-orange)

**Intelligent Document Q&A System using Azure AI Foundry, Azure AI Search, LangChain, and RAG Architecture**

## 🎯 Overview

An enterprise-grade Retrieval-Augmented Generation (RAG) system that enables natural language querying of enterprise documents. The system ingests documents, creates vector embeddings, and provides accurate, context-aware answers with source citations.

## ✨ Features

- **Multi-Format Document Support**: PDF, DOCX, TXT, Markdown
- **Hybrid Search**: Combines vector similarity and keyword search
- **Azure AI Integration**: Powered by Azure OpenAI and Azure AI Search
- **Source Citations**: All answers include document sources
- **Interactive Web UI**: Modern, responsive chat interface
- **Real-time Processing**: Fast document ingestion and query response
- **Scalable Architecture**: Designed for enterprise-scale deployments

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     User Interface (Web)                     │
│            (HTML/CSS/JavaScript + FastAPI Backend)           │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    RAG Pipeline (Python)                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Document   │  │   Chunking   │  │  Embeddings  │      │
│  │    Loader    │─▶│   Engine     │─▶│  Generator   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└────────────────────────────┬────────────────────────────────┘
                             │
                ┌────────────┴────────────┐
                ▼                         ▼
┌──────────────────────────┐  ┌──────────────────────────┐
│   Azure AI Search        │  │   Azure OpenAI           │
│   - Vector Index         │  │   - GPT-4 (Generation)   │
│   - Hybrid Search        │  │   - Ada-002 (Embeddings) │
│   - Semantic Ranking     │  │   - Chat Completion      │
└──────────────────────────┘  └──────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- Azure subscription with:
  - Azure OpenAI Service
  - Azure AI Search Service
- Enterprise documents in supported formats

### Installation

1. **Clone or navigate to the project directory**:
   ```powershell
   cd C:\Users\rajvkha\Downloads\Apprentice\RAG
   ```

2. **Create and activate a virtual environment**:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. **Install dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:
   - Copy `.env.example` to `.env`:
     ```powershell
     Copy-Item .env.example .env
     ```
   - Edit `.env` and add your Azure credentials:
     ```
     AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
     AZURE_OPENAI_API_KEY=your-api-key-here
     AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4
     AZURE_OPENAI_EMBEDDING_DEPLOYMENT=text-embedding-ada-002
     
     AZURE_SEARCH_ENDPOINT=https://your-search-service.search.windows.net
     AZURE_SEARCH_API_KEY=your-search-api-key
     AZURE_SEARCH_INDEX_NAME=documents-index
     
     DOCUMENT_PATH=C:\\Users\\rajvkha\\Downloads\\DocumentQnA_RAG_DataSet\\sample_docs
     ```

5. **Test the system** (optional):
   ```powershell
   python test_system.py
   ```

6. **Start the application**:
   ```powershell
   python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

7. **Access the web interface**:
   Open your browser to: http://localhost:8000

## 📋 Usage Guide

### Step 1: Ingest Documents

1. Place your enterprise documents in the configured `DOCUMENT_PATH`
2. Click the **"📁 Ingest Documents"** button in the web interface
3. Wait for the ingestion process to complete (progress shown in UI)

### Step 2: Ask Questions

1. Type your question in the chat input box
2. Press Enter or click **"Send"**
3. Receive AI-generated answers with source citations

### Sample Queries

Try these example queries:

- **Policy Questions**:
  - "What is the company vacation policy?"
  - "How many sick days do employees get?"
  
- **Process Questions**:
  - "How do I submit an expense report?"
  - "What is the process for requesting time off?"
  
- **Requirement Questions**:
  - "What are the requirements for remote work?"
  - "What equipment is provided to new employees?"
  
- **General Information**:
  - "What are the company's core values?"
  - "What is the dress code policy?"

## 📁 Project Structure

```
RAG/
├── app/
│   ├── __init__.py              # Package initialization
│   ├── config.py                # Configuration management
│   ├── document_loader.py       # Document ingestion
│   ├── main.py                  # FastAPI application
│   └── rag_pipeline.py          # RAG implementation
│
├── static/
│   ├── css/
│   │   └── style.css            # UI styles
│   └── js/
│       └── app.js               # Frontend logic
│
├── templates/
│   └── index.html               # Main UI template
│
├── utils/
│   ├── __init__.py
│   ├── chunking.py              # Text chunking utilities
│   └── embeddings.py            # Embedding utilities
│
├── sample_docs/                 # Sample documents
│   ├── company_policies.md
│   ├── product_specifications.txt
│   └── technical_documentation.md
│
├── .env.example                 # Environment template
├── requirements.txt             # Python dependencies
├── test_system.py               # Test suite
└── README.md                    # This file
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `AZURE_OPENAI_ENDPOINT` | Azure OpenAI service endpoint | Yes |
| `AZURE_OPENAI_API_KEY` | Azure OpenAI API key | Yes |
| `AZURE_OPENAI_DEPLOYMENT_NAME` | GPT model deployment name | Yes |
| `AZURE_OPENAI_EMBEDDING_DEPLOYMENT` | Embedding model deployment | Yes |
| `AZURE_SEARCH_ENDPOINT` | Azure AI Search endpoint | Yes |
| `AZURE_SEARCH_API_KEY` | Azure AI Search API key | Yes |
| `AZURE_SEARCH_INDEX_NAME` | Search index name | Yes |
| `DOCUMENT_PATH` | Path to enterprise documents | Yes |
| `CHUNK_SIZE` | Document chunk size (chars) | No (default: 1000) |
| `CHUNK_OVERLAP` | Chunk overlap (chars) | No (default: 200) |

### Supported Document Formats

- **PDF** (.pdf)
- **Microsoft Word** (.docx)
- **Text** (.txt)
- **Markdown** (.md)

## 🎨 API Endpoints

### Health Check
```
GET /api/health
```
Check system health status.

### Configuration
```
GET /api/config
```
Get current system configuration.

### Document Ingestion
```
POST /api/ingest
```
Ingest documents from configured path.

**Response**:
```json
{
  "status": "success",
  "message": "Documents ingested successfully"
}
```

### Query Documents
```
POST /api/query
```
Query documents with natural language.

**Request Body**:
```json
{
  "question": "What is the company vacation policy?"
}
```

**Response**:
```json
{
  "answer": "According to the company policy...",
  "sources": ["company_policies.md"],
  "context_chunks": 3
}
```

## 🧪 Testing

Run the test suite to verify system functionality:

```powershell
python test_system.py
```

The test suite verifies:
- ✅ Configuration loading
- ✅ Document loading from filesystem
- ✅ Document chunking and processing
- ✅ Azure service connectivity (if configured)

## 🔒 Security Best Practices

1. **Never commit `.env` file** to version control
2. **Use Azure Key Vault** for production deployments
3. **Rotate API keys regularly**
4. **Implement authentication** for production use
5. **Use HTTPS** for all communications
6. **Sanitize user inputs** before processing

## 📊 Performance Optimization

### Document Processing
- Batch size: 10 documents per batch (configurable)
- Parallel processing for embeddings
- Caching for frequently accessed documents

### Search Performance
- Hybrid search (vector + keyword)
- Semantic ranking for improved relevance
- Top-K results: 5 (configurable)

### Response Generation
- Token limit: 1500 (configurable)
- Temperature: 0.7 (balanced creativity)
- Streaming responses (future enhancement)

## 🐛 Troubleshooting

### Common Issues

**Issue**: "Azure configuration incomplete"
- **Solution**: Verify all Azure credentials in `.env` file

**Issue**: "No documents found"
- **Solution**: Check `DOCUMENT_PATH` and ensure documents exist

**Issue**: "Connection timeout"
- **Solution**: Verify Azure service endpoints and network connectivity

**Issue**: "Embedding generation failed"
- **Solution**: Check Azure OpenAI deployment name and quota limits

### Debug Mode

Enable debug logging by setting in `.env`:
```
DEBUG=True
```

## 📈 Future Enhancements

- [ ] Multi-language support
- [ ] Document versioning
- [ ] Advanced analytics dashboard
- [ ] User authentication and authorization
- [ ] Conversation history
- [ ] Export chat transcripts
- [ ] Custom prompt templates
- [ ] Integration with Microsoft Teams/Slack
- [ ] Streaming responses
- [ ] Document metadata filtering

## 🤝 Contributing

This is an educational/capstone project. For improvements or suggestions, please refer to the course materials or contact your instructor.

## 📝 License

This project is created for educational purposes as part of a capstone project.

## 👥 Credits

**Capstone Project**: Gen AI RAG Document Q&A with Enterprise Data  
**Course**: Azure AI Foundry, AI Search, LangChain and RAG  
**Reference**: [GenAI-DocQnA-RAG](https://github.com/dharanidharmadupu/GenAI-DocQnA-RAG)

## 📞 Support

For issues or questions:
1. Review this README
2. Check the troubleshooting section
3. Run the test suite
4. Review application logs
5. Consult Azure documentation

## 🎓 Learning Resources

- [Azure OpenAI Service Documentation](https://learn.microsoft.com/en-us/azure/cognitive-services/openai/)
- [Azure AI Search Documentation](https://learn.microsoft.com/en-us/azure/search/)
- [LangChain Documentation](https://python.langchain.com/)
- [RAG Pattern Guide](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/rag/rag-solution-design-and-evaluation-guide)

---

**Built with ❤️ using Azure AI, LangChain, and FastAPI**
