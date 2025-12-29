# 📖 Quick Reference Card

## Essential Commands

### Start Application
```powershell
# Easy way
.\start.ps1

# Manual way
.\venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Run Tests
```powershell
python test_system.py
```

### Access Application
```
http://localhost:8000
```

---

## API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | Main UI |
| `/api/health` | GET | Health check |
| `/api/config` | GET | Get configuration |
| `/api/ingest` | POST | Ingest documents |
| `/api/query` | POST | Query documents |

---

## Environment Variables

```env
# Required
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=text-embedding-ada-002
AZURE_SEARCH_ENDPOINT=https://your-search.search.windows.net
AZURE_SEARCH_API_KEY=your-search-key
DOCUMENT_PATH=C:\\path\\to\\documents

# Optional (with defaults)
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
APP_PORT=8000
DEBUG=True
```

---

## File Structure

```
RAG/
├── app/                    # Core application code
│   ├── config.py          # Configuration
│   ├── document_loader.py # Document ingestion
│   ├── main.py            # FastAPI app
│   └── rag_pipeline.py    # RAG logic
├── static/                # Frontend assets
├── templates/             # HTML templates
├── utils/                 # Utility functions
├── .env                   # Your configuration (create from .env.example)
└── requirements.txt       # Python dependencies
```

---

## Common Tasks

### Change Document Path
Edit `.env`:
```env
DOCUMENT_PATH=C:\\your\\new\\path
```

### Change Port
Edit `.env`:
```env
APP_PORT=8001
```

### Adjust Chunk Size
Edit `.env`:
```env
CHUNK_SIZE=1500
CHUNK_OVERLAP=300
```

### View Logs
Check terminal output where application is running

---

## Supported File Types

- `.pdf` - PDF documents
- `.docx` - Microsoft Word documents
- `.txt` - Plain text files
- `.md` - Markdown files

---

## Troubleshooting Quick Fixes

| Problem | Quick Fix |
|---------|-----------|
| Azure config error | Check `.env` file credentials |
| No documents found | Verify `DOCUMENT_PATH` |
| Port in use | Change `APP_PORT` in `.env` |
| Slow responses | Check internet connection |
| Auth failed | Regenerate Azure API keys |

---

## Sample Queries

```
Policy Queries:
- What is the company vacation policy?
- How many sick days do employees get?

Process Queries:
- How do I submit an expense report?
- What is the process for requesting time off?

Technical Queries:
- What are the product specifications?
- How does the authentication system work?
```

---

## Performance Tips

1. **Optimal chunk size**: 800-1200 characters
2. **Overlap**: 10-20% of chunk size
3. **Top-K results**: 3-7 documents
4. **Document count**: <1000 for best performance

---

## Cost Monitoring

**Typical costs (per 1000 queries)**:
- Embeddings: ~$0.10
- GPT-4 responses: ~$1.50-3.00
- AI Search: Included in service tier

**Monitor**: Azure Cost Management dashboard

---

## Security Checklist

- [ ] `.env` file not in version control
- [ ] API keys rotated regularly
- [ ] HTTPS enabled for production
- [ ] Authentication implemented
- [ ] Input validation enabled

---

## Documentation Files

- `README.md` - Complete user guide
- `GETTING_STARTED.md` - Setup tutorial
- `AZURE_SETUP.md` - Azure configuration
- `DEPLOYMENT.md` - Production deployment
- `PROJECT_SUMMARY.md` - Project overview
- `QUICK_REFERENCE.md` - This file

---

## Keyboard Shortcuts (Web UI)

- `Enter` - Send message
- `Shift+Enter` - New line in textarea

---

## Resources

- Azure Portal: https://portal.azure.com
- Azure OpenAI Docs: https://learn.microsoft.com/azure/ai-services/openai/
- Azure AI Search Docs: https://learn.microsoft.com/azure/search/
- FastAPI Docs: https://fastapi.tiangolo.com/
- LangChain Docs: https://python.langchain.com/

---

**Print this page for quick reference! 📄**

Last Updated: December 24, 2025
