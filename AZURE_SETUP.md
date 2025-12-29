# Azure AI Setup Guide

This guide will help you set up the required Azure services for the Enterprise RAG Document Q&A System.

## Prerequisites

- An active Azure subscription
- Azure CLI installed (optional but recommended)
- Sufficient permissions to create resources

## Step 1: Create Azure OpenAI Resource

### Using Azure Portal

1. **Navigate to Azure Portal**: https://portal.azure.com

2. **Create Azure OpenAI Resource**:
   - Click "Create a resource"
   - Search for "Azure OpenAI"
   - Click "Create"
   - Fill in the details:
     - **Subscription**: Select your subscription
     - **Resource Group**: Create new or use existing
     - **Region**: Choose a supported region (e.g., East US, West Europe)
     - **Name**: Enter a unique name (e.g., `mycompany-openai`)
     - **Pricing Tier**: Select Standard S0

3. **Deploy Models**:
   After the resource is created:
   
   **a) Deploy GPT-4 Model**:
   - Go to your Azure OpenAI resource
   - Click "Model deployments" or "Azure OpenAI Studio"
   - Click "Create new deployment"
   - Select model: `gpt-4` or `gpt-35-turbo`
   - Enter deployment name: `gpt-4` (remember this name)
   - Click "Create"
   
   **b) Deploy Embedding Model**:
   - Click "Create new deployment" again
   - Select model: `text-embedding-ada-002`
   - Enter deployment name: `text-embedding-ada-002`
   - Click "Create"

4. **Get API Credentials**:
   - Go to "Keys and Endpoint"
   - Copy:
     - **Endpoint**: `https://your-resource.openai.azure.com/`
     - **Key 1**: Your API key

### Using Azure CLI

```bash
# Login to Azure
az login

# Create resource group
az group create --name rg-rag-system --location eastus

# Create Azure OpenAI resource
az cognitiveservices account create \
  --name mycompany-openai \
  --resource-group rg-rag-system \
  --kind OpenAI \
  --sku S0 \
  --location eastus

# Get endpoint and key
az cognitiveservices account show \
  --name mycompany-openai \
  --resource-group rg-rag-system \
  --query properties.endpoint

az cognitiveservices account keys list \
  --name mycompany-openai \
  --resource-group rg-rag-system
```

## Step 2: Create Azure AI Search Resource

### Using Azure Portal

1. **Create Azure AI Search**:
   - Click "Create a resource"
   - Search for "Azure Cognitive Search" or "Azure AI Search"
   - Click "Create"
   - Fill in the details:
     - **Subscription**: Select your subscription
     - **Resource Group**: Same as OpenAI resource
     - **Service Name**: Enter unique name (e.g., `mycompany-search`)
     - **Location**: Same region as OpenAI
     - **Pricing Tier**: Basic or Standard (Basic is sufficient for development)

2. **Get API Credentials**:
   - Go to your Search resource
   - Click "Keys"
   - Copy:
     - **URL**: `https://your-search-service.search.windows.net`
     - **Primary admin key**: Your API key

### Using Azure CLI

```bash
# Create Azure AI Search
az search service create \
  --name mycompany-search \
  --resource-group rg-rag-system \
  --sku basic \
  --location eastus

# Get endpoint and key
az search service show \
  --name mycompany-search \
  --resource-group rg-rag-system \
  --query hostName

az search admin-key show \
  --service-name mycompany-search \
  --resource-group rg-rag-system
```

## Step 3: Configure Your Application

1. **Create `.env` file** in your project root:
   ```
   cp .env.example .env
   ```

2. **Update `.env` with your credentials**:
   ```env
   # Azure OpenAI Configuration
   AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
   AZURE_OPENAI_API_KEY=your-openai-api-key-here
   AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4
   AZURE_OPENAI_API_VERSION=2024-02-15-preview
   AZURE_OPENAI_EMBEDDING_DEPLOYMENT=text-embedding-ada-002
   
   # Azure AI Search Configuration
   AZURE_SEARCH_ENDPOINT=https://your-search-service.search.windows.net
   AZURE_SEARCH_API_KEY=your-search-api-key-here
   AZURE_SEARCH_INDEX_NAME=documents-index
   
   # Document Configuration
   DOCUMENT_PATH=C:\\Users\\rajvkha\\Downloads\\DocumentQnA_RAG_DataSet\\sample_docs
   CHUNK_SIZE=1000
   CHUNK_OVERLAP=200
   
   # Application Configuration
   APP_HOST=0.0.0.0
   APP_PORT=8000
   DEBUG=True
   ```

## Step 4: Verify Setup

1. **Test configuration**:
   ```powershell
   python test_system.py
   ```

2. **Expected output**:
   ```
   ✅ Azure configuration looks good
   ✅ Document loading works
   ✅ Document chunking works
   ```

## Pricing Information

### Azure OpenAI Pricing (as of 2024)
- **GPT-4**: ~$0.03 per 1K input tokens, ~$0.06 per 1K output tokens
- **Ada-002 Embeddings**: ~$0.0001 per 1K tokens

### Azure AI Search Pricing
- **Basic Tier**: ~$75/month (3 replicas, 15GB storage)
- **Standard S1**: ~$250/month (12 replicas, 25GB storage)

### Cost Estimation for Development
- Development/Testing: ~$10-50/month
- Production (small): ~$100-300/month
- Production (medium): ~$500-1000/month

**Tip**: Use Azure Cost Management to monitor your spending.

## Security Best Practices

1. **Never commit API keys** to version control
2. **Use Azure Key Vault** for production:
   ```bash
   # Create Key Vault
   az keyvault create \
     --name mycompany-keyvault \
     --resource-group rg-rag-system \
     --location eastus
   
   # Store secrets
   az keyvault secret set \
     --vault-name mycompany-keyvault \
     --name "OpenAI-ApiKey" \
     --value "your-api-key"
   ```

3. **Enable Azure AD authentication** for production
4. **Use managed identities** when possible
5. **Implement network restrictions** for production

## Troubleshooting

### Issue: "Resource not available in region"
**Solution**: Choose a different region. Check [Azure OpenAI region availability](https://learn.microsoft.com/en-us/azure/cognitive-services/openai/concepts/models#model-summary-table-and-region-availability)

### Issue: "Insufficient quota"
**Solution**: Request quota increase through Azure Portal:
1. Go to Azure OpenAI resource
2. Click "Quotas"
3. Request increase

### Issue: "Deployment not found"
**Solution**: Verify deployment name matches exactly in `.env` file

### Issue: "Authentication failed"
**Solution**: 
- Verify API keys are correct
- Check if keys have been rotated
- Ensure no extra spaces in `.env` file

## Additional Resources

- [Azure OpenAI Service Documentation](https://learn.microsoft.com/en-us/azure/cognitive-services/openai/)
- [Azure AI Search Documentation](https://learn.microsoft.com/en-us/azure/search/)
- [Azure Pricing Calculator](https://azure.microsoft.com/en-us/pricing/calculator/)
- [Azure Free Account](https://azure.microsoft.com/en-us/free/)

## Next Steps

After completing this setup:

1. ✅ Verify all credentials are in `.env`
2. ✅ Run `python test_system.py`
3. ✅ Start the application: `python -m uvicorn app.main:app --reload`
4. ✅ Access the web interface: http://localhost:8000
5. ✅ Click "Ingest Documents" to load your data
6. ✅ Start asking questions!

---

**Need Help?** Review the main README.md or check Azure documentation.
