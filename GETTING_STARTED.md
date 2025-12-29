# 🚀 Getting Started Guide

## Welcome to the Enterprise RAG Document Q&A System!

This guide will help you get your RAG system up and running in **less than 15 minutes**.

---

## 📋 Pre-Flight Checklist

Before you begin, make sure you have:

- [ ] Python 3.9 or higher installed
- [ ] An Azure subscription
- [ ] Documents ready to ingest (in the sample_docs folder or custom path)
- [ ] 15 minutes of your time

---

## 🎯 Step-by-Step Setup

### Step 1: Set Up Azure Services (10 minutes)

#### Option A: Using Azure Portal (Recommended for beginners)

1. **Go to Azure Portal**: https://portal.azure.com

2. **Create Azure OpenAI Resource**:
   - Search for "Azure OpenAI" → Click "Create"
   - Fill in the details:
     - Name: `mycompany-openai-rag`
     - Region: East US (or your preferred region)
     - Pricing: Standard S0
   - Click "Review + Create" → "Create"
   
3. **Deploy Models**:
   - Open your Azure OpenAI resource
   - Go to "Model deployments" or click "Go to Azure OpenAI Studio"
   - Deploy these models:
     - **GPT-4** (or GPT-3.5-Turbo): Name it `gpt-4`
     - **text-embedding-ada-002**: Name it `text-embedding-ada-002`
   
4. **Get OpenAI Credentials**:
   - Go to "Keys and Endpoint"
   - Copy:
     - ✍️ Endpoint (e.g., `https://mycompany-openai-rag.openai.azure.com/`)
     - ✍️ Key 1

5. **Create Azure AI Search Resource**:
   - Search for "Azure Cognitive Search" → Click "Create"
   - Fill in the details:
     - Name: `mycompany-search-rag`
     - Region: Same as OpenAI resource
     - Pricing: Basic (sufficient for development)
   - Click "Review + Create" → "Create"

6. **Get Search Credentials**:
   - Open your Search resource
   - Go to "Keys"
   - Copy:
     - ✍️ URL (e.g., `https://mycompany-search-rag.search.windows.net`)
     - ✍️ Primary admin key

📝 **Save these credentials - you'll need them in Step 3!**

#### Option B: Using Azure CLI (For advanced users)

See [AZURE_SETUP.md](AZURE_SETUP.md) for detailed CLI instructions.

---

### Step 2: Set Up Your Development Environment (3 minutes)

1. **Open PowerShell** and navigate to the project:
   ```powershell
   cd C:\Users\rajvkha\Downloads\Apprentice\RAG
   ```

2. **Create a virtual environment**:
   ```powershell
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```
   
   > 💡 If you get an execution policy error, run:
   > ```powershell
   > Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   > ```

4. **Install dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```
   
   ⏱️ This will take 2-3 minutes. Grab a coffee! ☕

---

### Step 3: Configure the Application (2 minutes)

1. **Create your environment file**:
   ```powershell
   Copy-Item .env.example .env
   ```

2. **Edit the .env file**:
   ```powershell
   notepad .env
   ```

3. **Replace the placeholders** with your Azure credentials from Step 1:

   ```env
   # Azure OpenAI Configuration
   AZURE_OPENAI_ENDPOINT=https://mycompany-openai-rag.openai.azure.com/
   AZURE_OPENAI_API_KEY=your-actual-key-from-step-1
   AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4
   AZURE_OPENAI_API_VERSION=2024-02-15-preview
   AZURE_OPENAI_EMBEDDING_DEPLOYMENT=text-embedding-ada-002
   
   # Azure AI Search Configuration
   AZURE_SEARCH_ENDPOINT=https://mycompany-search-rag.search.windows.net
   AZURE_SEARCH_API_KEY=your-actual-search-key-from-step-1
   AZURE_SEARCH_INDEX_NAME=documents-index
   
   # Document Configuration (Update if your documents are elsewhere)
   DOCUMENT_PATH=C:\\Users\\rajvkha\\Downloads\\DocumentQnA_RAG_DataSet\\sample_docs
   CHUNK_SIZE=1000
   CHUNK_OVERLAP=200
   
   # Application Configuration
   APP_HOST=0.0.0.0
   APP_PORT=8000
   DEBUG=True
   ```

4. **Save and close** the file

---

### Step 4: Verify Everything Works (1 minute)

Run the test suite:
```powershell
python test_system.py
```

✅ **Expected output**:
```
🧪 RAG System Test Suite

============================================================
Testing Configuration
============================================================
Document Path: C:\Users\rajvkha\Downloads\...
Chunk Size: 1000
Chunk Overlap: 200
Top K Results: 5
Azure Configured: True

✅ Azure configuration looks good

============================================================
Testing Document Loading
============================================================
✅ Loaded 3 documents

Document Statistics:
  Total Documents: 3
  Total Characters: 15,234
  Average Chars/Doc: 5,078
  File Types: {'md': 2, 'txt': 1}

============================================================
Test Summary
============================================================
Configuration: ✅ PASSED
Document Loading: ✅ PASSED
Document Chunking: ✅ PASSED

🎉 All tests passed!
```

> ⚠️ If tests fail, check your .env file and Azure credentials!

---

### Step 5: Start the Application! (30 seconds)

**Option A: Using the startup script (Easiest)**
```powershell
.\start.ps1
```

**Option B: Manual start**
```powershell
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

✅ **You should see**:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

---

### Step 6: Access the Web Interface

1. **Open your browser** and go to:
   ```
   http://localhost:8000
   ```

2. **You should see** the beautiful Enterprise RAG Document Q&A interface! 🎉

---

## 🎮 Using the Application

### First Time Setup

1. **Click "📁 Ingest Documents"** button
   - This loads and indexes your documents
   - Takes 30-60 seconds depending on document count
   - You'll see a success message when complete

2. **Check the status**:
   - Green dot = System ready ✅
   - Azure Configured indicator should show ✅

### Asking Questions

**Method 1: Use Quick Queries**
- Click any of the sample query buttons (e.g., "Vacation Policy")

**Method 2: Type Your Own Question**
1. Type your question in the input box
2. Press Enter or click "Send"
3. Wait for the AI-powered response (usually 2-3 seconds)

### Understanding Responses

Each response includes:
- **Answer**: AI-generated answer based on your documents
- **Sources**: Which documents were used (with chunk count)
- **Citations**: Specific source references

Example:
```
Q: What is the company vacation policy?

A: According to the company policy, employees are entitled 
   to 15 days of paid vacation per year...

📚 Sources (3 chunks):
   📄 company_policies.md
```

---

## 📝 Sample Queries to Try

### Basic Queries
```
- What is the company vacation policy?
- How do I submit an expense report?
- What are the requirements for remote work?
```

### Complex Queries
```
- What is the process for requesting time off and what documents do I need?
- Compare the benefits between full-time and part-time employees
- What are all the policies related to working from home?
```

### Technical Queries
```
- How does the authentication system work?
- What are the technical specifications of Product X?
- Explain the deployment process
```

---

## 🔧 Troubleshooting

### Problem: "Azure configuration incomplete"
**Solution**: 
- Check your .env file
- Verify all Azure credentials are correct
- Run `python test_system.py` to diagnose

### Problem: "No documents found"
**Solution**:
- Verify DOCUMENT_PATH in .env points to correct location
- Check that documents exist in that folder
- Ensure documents are in supported formats (PDF, DOCX, TXT, MD)

### Problem: "Port 8000 already in use"
**Solution**:
- Change port in .env: `APP_PORT=8001`
- Or kill the existing process using port 8000

### Problem: Slow responses
**Solution**:
- Check your internet connection (Azure services are cloud-based)
- Verify Azure services are in the same region
- Check Azure OpenAI quota limits

### Problem: "Authentication failed"
**Solution**:
- Regenerate Azure API keys
- Update .env with new keys
- Restart the application

---

## 📚 Next Steps

### Explore the Documentation
- **README.md**: Comprehensive guide and API reference
- **AZURE_SETUP.md**: Detailed Azure setup instructions
- **DEPLOYMENT.md**: Production deployment guide
- **PROJECT_SUMMARY.md**: Project overview and features

### Customize Your System
1. **Add more documents**: Place them in your DOCUMENT_PATH
2. **Adjust chunking**: Modify CHUNK_SIZE and CHUNK_OVERLAP in .env
3. **Change results count**: Update top_k_results in config.py
4. **Modify UI**: Edit files in static/ and templates/

### Deploy to Production
- See [DEPLOYMENT.md](DEPLOYMENT.md) for production deployment options
- Consider Azure App Service, Docker, or Kubernetes

---

## 🎓 Learning Resources

### Azure Documentation
- [Azure OpenAI Service](https://learn.microsoft.com/en-us/azure/cognitive-services/openai/)
- [Azure AI Search](https://learn.microsoft.com/en-us/azure/search/)

### Technology Stack
- [FastAPI](https://fastapi.tiangolo.com/)
- [LangChain](https://python.langchain.com/)
- [RAG Pattern](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/rag/rag-solution-design-and-evaluation-guide)

---

## 💡 Tips for Success

1. **Start Small**: Test with 3-5 documents first
2. **Monitor Costs**: Keep an eye on Azure spending
3. **Iterate**: Try different chunk sizes for better results
4. **Document**: Keep notes on what works well
5. **Backup**: Keep copies of your .env file (securely!)

---

## 🆘 Need Help?

1. **Check test results**: `python test_system.py`
2. **Review logs**: Look at terminal output for errors
3. **Verify Azure**: Check Azure Portal for service status
4. **Read docs**: This README and other documentation files
5. **Azure Support**: Use Azure Support for Azure-specific issues

---

## 🎉 Success!

If you've followed all steps, you should now have:
- ✅ Fully functional RAG system
- ✅ Web interface accessible at localhost:8000
- ✅ Documents ingested and searchable
- ✅ AI-powered Q&A working

**Congratulations! You've built an enterprise-grade RAG system! 🎊**

Now start asking questions and exploring your documents in a whole new way!

---

**Ready to go?** Run `.\start.ps1` and visit http://localhost:8000! 🚀

*Questions? Check the other documentation files or run the test suite.*
