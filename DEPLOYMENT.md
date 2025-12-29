# Deployment Guide

This guide covers deployment options for the Enterprise RAG Document Q&A System.

## Deployment Options

### 1. Local Development (Covered in README.md)

### 2. Azure App Service Deployment

#### Prerequisites
- Azure CLI installed
- Azure subscription
- Docker installed (optional)

#### Steps

1. **Prepare for deployment**:
   ```powershell
   # Create requirements.txt with pinned versions
   pip freeze > requirements.txt
   ```

2. **Create Azure App Service**:
   ```bash
   # Login to Azure
   az login
   
   # Create resource group (if not exists)
   az group create --name rg-rag-system --location eastus
   
   # Create App Service Plan
   az appservice plan create \
     --name plan-rag-system \
     --resource-group rg-rag-system \
     --sku B2 \
     --is-linux
   
   # Create Web App
   az webapp create \
     --resource-group rg-rag-system \
     --plan plan-rag-system \
     --name mycompany-rag-app \
     --runtime "PYTHON:3.9"
   ```

3. **Configure App Settings**:
   ```bash
   # Set environment variables
   az webapp config appsettings set \
     --resource-group rg-rag-system \
     --name mycompany-rag-app \
     --settings \
       AZURE_OPENAI_ENDPOINT="your-endpoint" \
       AZURE_OPENAI_API_KEY="your-key" \
       AZURE_SEARCH_ENDPOINT="your-search-endpoint" \
       AZURE_SEARCH_API_KEY="your-search-key"
   ```

4. **Deploy the application**:
   ```bash
   # Deploy from local directory
   az webapp up \
     --resource-group rg-rag-system \
     --name mycompany-rag-app \
     --runtime "PYTHON:3.9"
   ```

### 3. Docker Container Deployment

1. **Create Dockerfile**:
   ```dockerfile
   FROM python:3.9-slim
   
   WORKDIR /app
   
   # Install dependencies
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   
   # Copy application
   COPY . .
   
   # Expose port
   EXPOSE 8000
   
   # Run application
   CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
   ```

2. **Build and run**:
   ```bash
   # Build image
   docker build -t rag-system:latest .
   
   # Run container
   docker run -p 8000:8000 \
     -e AZURE_OPENAI_ENDPOINT="your-endpoint" \
     -e AZURE_OPENAI_API_KEY="your-key" \
     rag-system:latest
   ```

### 4. Azure Container Instances

```bash
# Create container registry
az acr create \
  --resource-group rg-rag-system \
  --name mycompanyregistry \
  --sku Basic

# Build and push image
az acr build \
  --registry mycompanyregistry \
  --image rag-system:latest .

# Deploy to Container Instances
az container create \
  --resource-group rg-rag-system \
  --name rag-system-container \
  --image mycompanyregistry.azurecr.io/rag-system:latest \
  --dns-name-label mycompany-rag \
  --ports 8000 \
  --environment-variables \
    AZURE_OPENAI_ENDPOINT="your-endpoint" \
    AZURE_OPENAI_API_KEY="your-key"
```

### 5. Azure Kubernetes Service (AKS)

For enterprise-scale deployments with high availability.

```bash
# Create AKS cluster
az aks create \
  --resource-group rg-rag-system \
  --name aks-rag-system \
  --node-count 2 \
  --enable-managed-identity \
  --generate-ssh-keys

# Get credentials
az aks get-credentials \
  --resource-group rg-rag-system \
  --name aks-rag-system

# Create Kubernetes deployment
kubectl create deployment rag-system \
  --image=mycompanyregistry.azurecr.io/rag-system:latest

# Expose as service
kubectl expose deployment rag-system \
  --type=LoadBalancer \
  --port=80 \
  --target-port=8000
```

## Production Considerations

### Security

1. **Use Azure Key Vault**:
   ```python
   from azure.keyvault.secrets import SecretClient
   from azure.identity import DefaultAzureCredential
   
   credential = DefaultAzureCredential()
   client = SecretClient(vault_url="https://myvault.vault.azure.net/", credential=credential)
   
   api_key = client.get_secret("OpenAI-ApiKey").value
   ```

2. **Enable HTTPS**: Configure SSL/TLS certificates

3. **Add Authentication**: Implement Azure AD authentication

4. **Network Security**: Use Virtual Networks and Private Endpoints

### Performance

1. **Enable Caching**:
   ```python
   from functools import lru_cache
   
   @lru_cache(maxsize=100)
   def get_embeddings(text: str):
       # Your embedding logic
       pass
   ```

2. **Use Redis for Session Management**:
   ```bash
   pip install redis
   ```

3. **Configure Auto-scaling**:
   ```bash
   az monitor autoscale create \
     --resource-group rg-rag-system \
     --resource mycompany-rag-app \
     --resource-type Microsoft.Web/sites \
     --name autoscale-rag \
     --min-count 2 \
     --max-count 10 \
     --count 2
   ```

### Monitoring

1. **Enable Application Insights**:
   ```bash
   az monitor app-insights component create \
     --app rag-system-insights \
     --location eastus \
     --resource-group rg-rag-system
   ```

2. **Add logging**:
   ```python
   import logging
   from opencensus.ext.azure.log_exporter import AzureLogHandler
   
   logger = logging.getLogger(__name__)
   logger.addHandler(AzureLogHandler(
       connection_string='InstrumentationKey=your-key'
   ))
   ```

### Backup and Disaster Recovery

1. **Backup Search Index**:
   - Regular snapshots of Azure AI Search
   - Document version control

2. **Multi-region Deployment**:
   - Deploy to multiple Azure regions
   - Use Azure Traffic Manager for load balancing

## Cost Optimization

1. **Use Azure Reserved Instances** for predictable workloads
2. **Implement request caching** to reduce API calls
3. **Monitor usage** with Azure Cost Management
4. **Use spot instances** for non-critical workloads

## CI/CD Pipeline

### GitHub Actions Example

```yaml
name: Deploy RAG System

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        python test_system.py
    
    - name: Deploy to Azure
      uses: azure/webapps-deploy@v2
      with:
        app-name: 'mycompany-rag-app'
        publish-profile: ${{ secrets.AZURE_WEBAPP_PUBLISH_PROFILE }}
```

## Health Checks

Implement health check endpoint for monitoring:

```python
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "azure_openai": check_openai_health(),
            "azure_search": check_search_health()
        }
    }
```

## Post-Deployment

1. **Test the deployment**:
   ```bash
   curl https://mycompany-rag-app.azurewebsites.net/api/health
   ```

2. **Monitor logs**:
   ```bash
   az webapp log tail \
     --resource-group rg-rag-system \
     --name mycompany-rag-app
   ```

3. **Configure alerts**:
   - Set up alerts for errors
   - Monitor response times
   - Track API usage and costs

---

**For support**, refer to Azure documentation or contact your cloud administrator.
