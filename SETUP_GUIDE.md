# Complete Setup Guide - Step by Step

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Installation Steps](#installation-steps)
3. [Configuration](#configuration)
4. [Running the Application](#running-the-application)
5. [Verification](#verification)
6. [Troubleshooting](#troubleshooting)
7. [Advanced Setup](#advanced-setup)

---

## Prerequisites

### Required Software

#### 1. Python 3.11 or Higher
**Check if installed:**
```bash
python --version
# or
python3 --version
```

**Install Python:**
- **Windows**: Download from [python.org](https://www.python.org/downloads/)
- **macOS**:
  ```bash
  brew install python@3.11
  ```
- **Linux (Ubuntu/Debian)**:
  ```bash
  sudo apt update
  sudo apt install python3.11 python3.11-venv python3-pip
  ```

#### 2. PostgreSQL with pgvector Extension

**Option A: Docker (Recommended)**
```bash
# Check if Docker is installed
docker --version

# If not installed:
# Windows/Mac: Download Docker Desktop from docker.com
# Linux:
sudo apt install docker.io docker-compose
```

**Option B: Native PostgreSQL Installation**
- **Version Required**: PostgreSQL 12.16+, 13.12+, 14.9+, or 15.4+
- **Extension**: pgvector 0.5.0+

**Installing pgvector:**
```bash
# Ubuntu/Debian
sudo apt install postgresql-15-pgvector

# macOS
brew install pgvector

# Or from source:
git clone https://github.com/pgvector/pgvector.git
cd pgvector
make
make install
```

#### 3. Node.js 18+ (for Promptfoo testing - optional)
```bash
# Check version
node --version

# Install
# Windows/Mac: Download from nodejs.org
# Linux:
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs
```

#### 4. Git (for cloning repository)
```bash
git --version

# Install if needed
# Windows: Download from git-scm.com
# macOS: brew install git
# Linux: sudo apt install git
```

---

## Installation Steps

### Step 1: Clone the Repository

```bash
# Clone the repository
git clone <your-repo-url>
cd Updated_tech_demo_project

# If you're starting from this directory, you can skip cloning
```

### Step 2: Create Python Virtual Environment

**Why virtual environment?**
- Isolates project dependencies
- Prevents version conflicts
- Easy to reproduce

**Create and activate:**

**Linux/macOS:**
```bash
# Create virtual environment
python3 -m venv venv

# Activate
source venv/bin/activate

# You should see (venv) in your terminal prompt
```

**Windows (Command Prompt):**
```cmd
# Create virtual environment
python -m venv venv

# Activate
venv\Scripts\activate.bat
```

**Windows (PowerShell):**
```powershell
# Create virtual environment
python -m venv venv

# Activate
venv\Scripts\Activate.ps1

# If you get an error about execution policy:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Step 3: Install Python Dependencies

```bash
# Make sure virtual environment is activated
# You should see (venv) in your prompt

# Install all dependencies
pip install -r requirements.txt

# This will install:
# - FastAPI and Uvicorn (web framework)
# - Langchain ecosystem (LLM orchestration)
# - Database drivers (PostgreSQL, MongoDB)
# - Document processing libraries
# - AI provider SDKs
# - And more...

# Installation may take 5-10 minutes
```

**Verify installation:**
```bash
pip list | grep fastapi
pip list | grep langchain
```

### Step 4: Set Up Database

#### Option A: Using Docker (Recommended)

```bash
# Start PostgreSQL with pgvector
docker compose -f db-compose.yaml up -d

# This creates:
# - PostgreSQL 15 with pgvector extension
# - Persistent volume for data
# - Exposed on port 5433

# Verify it's running
docker ps
# You should see a container named "rag_db"

# Check logs
docker logs rag_db
```

#### Option B: Using Existing PostgreSQL

If you have PostgreSQL already installed:

1. **Enable pgvector extension:**
   ```sql
   -- Connect to your database
   psql -U postgres

   -- Create database
   CREATE DATABASE rag_db;

   -- Connect to it
   \c rag_db

   -- Enable pgvector
   CREATE EXTENSION vector;

   -- Verify
   SELECT * FROM pg_extension WHERE extname = 'vector';
   ```

2. **Create user (optional):**
   ```sql
   CREATE USER rag_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE rag_db TO rag_user;
   ```

#### Option C: Using MongoDB Atlas (Alternative)

If you prefer MongoDB over PostgreSQL:

1. **Create Atlas account** at mongodb.com/cloud/atlas
2. **Create a cluster** (free tier available)
3. **Create database and collection**
4. **Set up vector search index** (see MongoDB section below)
5. **Get connection string**

---

## Configuration

### Step 1: Create Environment File

```bash
# Copy the example environment file
cp .env.example .env

# Edit it with your favorite editor
nano .env
# or
vim .env
# or
code .env  # if using VS Code
```

### Step 2: Configure Required Variables

Open `.env` and configure the following:

#### Minimal Configuration (PostgreSQL + Azure OpenAI)

```env
#------------------------------------------------------------
# DATABASE CONFIGURATION
#------------------------------------------------------------
# Vector database type: "pgvector" or "atlas-mongo"
VECTOR_DB_TYPE=pgvector

# PostgreSQL settings (if using pgvector)
POSTGRES_DB=rag_db
POSTGRES_USER=rag_user
POSTGRES_PASSWORD=your_secure_password_here
DB_HOST=localhost
DB_PORT=5432

# If using Docker Compose for database:
DB_HOST=localhost
DB_PORT=5433  # Note: Docker maps 5432 to 5433

# Collection name for vector storage
COLLECTION_NAME=documents

#------------------------------------------------------------
# EMBEDDINGS CONFIGURATION
#------------------------------------------------------------
# Embedding provider: openai, azure, huggingface, google_genai, etc.
EMBEDDINGS_PROVIDER=azure

# Embedding model
EMBEDDINGS_MODEL=text-embedding-3-small

#------------------------------------------------------------
# AZURE OPENAI CONFIGURATION
#------------------------------------------------------------
# Your Azure OpenAI API key
RAG_AZURE_OPENAI_API_KEY=your-azure-api-key-here

# Your Azure OpenAI endpoint
RAG_AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/

# API version
RAG_AZURE_OPENAI_API_VERSION=2023-05-15

#------------------------------------------------------------
# CHAT MODEL CONFIGURATION
#------------------------------------------------------------
# Azure chat endpoint (can be same as embeddings)
AZURE_CHAT_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_CHAT_API_KEY=your-azure-api-key-here
AZURE_CHAT_DEPLOYMENT=gpt-4o-mini  # Your deployment name

#------------------------------------------------------------
# APPLICATION SETTINGS
#------------------------------------------------------------
# Server host and port
RAG_HOST=0.0.0.0
RAG_PORT=8000

# Upload directory
RAG_UPLOAD_DIR=./uploads/

# Text processing
CHUNK_SIZE=1500
CHUNK_OVERLAP=100

# Debug mode
DEBUG_RAG_API=True  # Set to False in production
```

#### Alternative: OpenAI Configuration

If using OpenAI directly (not Azure):

```env
#------------------------------------------------------------
# OPENAI CONFIGURATION
#------------------------------------------------------------
EMBEDDINGS_PROVIDER=openai
EMBEDDINGS_MODEL=text-embedding-3-small

RAG_OPENAI_API_KEY=sk-your-openai-api-key-here

# Optional: Custom base URL or proxy
# RAG_OPENAI_BASEURL=https://api.openai.com/v1
# RAG_OPENAI_PROXY=http://proxy:8080
```

#### Alternative: Google Gemini Configuration

```env
#------------------------------------------------------------
# GOOGLE GEMINI CONFIGURATION
#------------------------------------------------------------
EMBEDDINGS_PROVIDER=google_genai
EMBEDDINGS_MODEL=gemini-embedding-001

RAG_GOOGLE_API_KEY=your-google-api-key-here

# For chat
GEMINI_API_KEY=your-google-api-key-here
```

#### Alternative: Local Embeddings (HuggingFace)

```env
#------------------------------------------------------------
# HUGGINGFACE LOCAL EMBEDDINGS
#------------------------------------------------------------
EMBEDDINGS_PROVIDER=huggingface
EMBEDDINGS_MODEL=sentence-transformers/all-MiniLM-L6-v2

# No API key needed - runs locally
```

#### Alternative: MongoDB Atlas

```env
#------------------------------------------------------------
# MONGODB ATLAS CONFIGURATION
#------------------------------------------------------------
VECTOR_DB_TYPE=atlas-mongo

ATLAS_MONGO_DB_URI=mongodb+srv://username:password@cluster.mongodb.net/dbname
COLLECTION_NAME=embeddings
ATLAS_SEARCH_INDEX=vector_index
```

### Step 3: Optional Configuration

#### JWT Authentication (Optional)
```env
# If you want to require authentication
JWT_SECRET=your-very-secure-secret-key-here
```

#### Advanced Settings
```env
# Thread pool size (default: CPU count, max 8)
RAG_THREAD_POOL_SIZE=4

# PostgreSQL connection via Unix socket
POSTGRES_USE_UNIX_SOCKET=False

# PDF image extraction
PDF_EXTRACT_IMAGES=False

# Structured JSON logging
CONSOLE_JSON=False

# PostgreSQL query debugging
DEBUG_PGVECTOR_QUERIES=False
```

### Step 4: Verify Configuration

```bash
# Check if all required variables are set
python -c "
from app.config import (
    POSTGRES_DB, EMBEDDINGS_PROVIDER, RAG_AZURE_OPENAI_API_KEY
)
print('Configuration loaded successfully!')
print(f'Database: {POSTGRES_DB}')
print(f'Embeddings: {EMBEDDINGS_PROVIDER}')
"
```

---

## Running the Application

### Method 1: Direct Python Execution (Development)

```bash
# Make sure virtual environment is activated
# and you're in the project root directory

# Start the server
uvicorn main:app --host 0.0.0.0 --port 8000

# Or with auto-reload for development:
uvicorn main:app --reload

# You should see:
# INFO:     Started server process
# INFO:     Waiting for application startup.
# INFO:     Application startup complete.
# INFO:     Uvicorn running on http://0.0.0.0:8000
```

**What happens on startup:**
1. Loads environment variables
2. Initializes database connection pool
3. Creates vector indexes
4. Initializes embedding provider
5. Starts web server

### Method 2: Using Docker Compose (Production)

```bash
# Start everything (database + application)
docker compose up -d

# This starts:
# - PostgreSQL with pgvector (port 5433)
# - FastAPI application (port 8000)

# View logs
docker compose logs -f

# Stop everything
docker compose down

# Stop and remove volumes (deletes data!)
docker compose down -v
```

### Method 3: Docker for Database Only

```bash
# Start only database
docker compose -f db-compose.yaml up -d

# Then run application locally
uvicorn main:app --reload
```

---

## Verification

### Step 1: Check Server Health

```bash
# In a new terminal (keep server running)

# Health check endpoint
curl http://localhost:8000/health

# Expected response:
# {"status":"UP"}

# If using PowerShell on Windows:
Invoke-WebRequest -Uri http://localhost:8000/health
```

### Step 2: Access Web Interface

1. Open your web browser
2. Navigate to: `http://localhost:8000`
3. You should see the RAG chatbot interface

**Expected interface:**
- Upload section at the top
- Chat interface in the center
- Document list on the right
- Settings panel (gear icon)

### Step 3: Test Document Upload

1. Click "Choose File" or drag-and-drop a document
2. Upload a simple text file (create one for testing):

```bash
# Create a test document
echo "Artificial Intelligence is the simulation of human intelligence by machines. \
RAG stands for Retrieval-Augmented Generation, which combines document retrieval \
with AI text generation to provide accurate answers." > test_document.txt
```

3. Upload `test_document.txt`
4. Wait for "Document uploaded successfully" message
5. Document should appear in the document list

### Step 4: Test Question Answering

1. Select the uploaded document (click checkmark icon)
2. Type a question: "What is RAG?"
3. Press Enter
4. You should receive an answer with source citations

**Expected response:**
```
Answer: RAG stands for Retrieval-Augmented Generation,
which combines document retrieval with AI text generation
to provide accurate answers.

Sources:
📄 test_document.txt (Score: 0.92)
"RAG stands for Retrieval-Augmented Generation, which
combines document retrieval..."
```

### Step 5: Test API Directly

```bash
# Test embedding endpoint
curl -X POST "http://localhost:8000/embed" \
  -F "file=@test_document.txt" \
  -F "file_id=test-doc-1"

# Test query endpoint
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is RAG?",
    "file_id": "test-doc-1",
    "k": 4
  }'

# Test chat endpoint
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is artificial intelligence?",
    "file_id": "test-doc-1",
    "model": "azure-gpt4o-mini",
    "k": 4,
    "temperature": 0.7
  }'
```

### Step 6: Check API Documentation

Visit: `http://localhost:8000/docs`

This opens the interactive Swagger UI where you can:
- View all available endpoints
- See request/response schemas
- Test endpoints directly in the browser

---

## Troubleshooting

### Problem 1: ModuleNotFoundError

**Error:**
```
ModuleNotFoundError: No module named 'fastapi'
```

**Solution:**
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

---

### Problem 2: Database Connection Error

**Error:**
```
Could not connect to PostgreSQL database
```

**Solution:**
```bash
# Check if Docker container is running
docker ps

# If not running, start it
docker compose -f db-compose.yaml up -d

# Check logs
docker logs rag_db

# Verify connection details in .env
# Make sure DB_HOST and DB_PORT match Docker settings

# If using Docker:
DB_HOST=localhost  # or 127.0.0.1
DB_PORT=5433  # Docker maps 5432 to 5433
```

---

### Problem 3: pgvector Extension Missing

**Error:**
```
extension "vector" does not exist
```

**Solution:**

If using Docker:
```bash
# The Docker image (ankane/pgvector) includes pgvector
# Just restart the container
docker compose -f db-compose.yaml down
docker compose -f db-compose.yaml up -d
```

If using native PostgreSQL:
```bash
# Install pgvector extension
sudo apt install postgresql-15-pgvector

# Connect to database
psql -U postgres -d rag_db

# Enable extension
CREATE EXTENSION vector;
```

---

### Problem 4: API Key Invalid

**Error:**
```
AuthenticationError: Invalid API key
```

**Solution:**
```bash
# Check your .env file
cat .env | grep API_KEY

# Make sure there are no spaces or quotes
# CORRECT:
RAG_AZURE_OPENAI_API_KEY=abc123def456

# INCORRECT:
RAG_AZURE_OPENAI_API_KEY = "abc123def456"
RAG_AZURE_OPENAI_API_KEY='abc123def456'

# Restart the server after fixing
```

---

### Problem 5: Port Already in Use

**Error:**
```
ERROR: [Errno 48] Address already in use
```

**Solution:**
```bash
# Find what's using port 8000
# Linux/Mac:
lsof -i :8000
kill -9 <PID>

# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Or use a different port:
uvicorn main:app --port 8001
```

---

### Problem 6: Embedding Timeout

**Error:**
```
TimeoutError: Request timeout during embedding
```

**Solution:**
```bash
# Reduce chunk size in .env
CHUNK_SIZE=1000  # Default is 1500

# Reduce batch size for embeddings
EMBEDDINGS_CHUNK_SIZE=50  # Default is 200

# Check your internet connection
# Check API service status
curl https://status.openai.com
```

---

### Problem 7: Out of Memory

**Error:**
```
MemoryError: Unable to allocate memory
```

**Solution:**
```bash
# Reduce thread pool size
RAG_THREAD_POOL_SIZE=2

# Use smaller embedding model
EMBEDDINGS_PROVIDER=huggingface
EMBEDDINGS_MODEL=sentence-transformers/all-MiniLM-L6-v2

# Process smaller documents
# Split large files before uploading
```

---

### Problem 8: Docker Permission Denied

**Error:**
```
permission denied while trying to connect to Docker daemon
```

**Solution:**
```bash
# Linux: Add user to docker group
sudo usermod -aG docker $USER
newgrp docker

# Or run with sudo (not recommended)
sudo docker compose up
```

---

## Advanced Setup

### Setup with MongoDB Atlas

1. **Create Atlas Account**
   - Go to mongodb.com/cloud/atlas
   - Sign up for free account
   - Create a new cluster (free M0 tier available)

2. **Create Database and Collection**
   ```javascript
   // In Atlas UI or mongosh
   use rag_database
   db.createCollection("embeddings")
   ```

3. **Create Vector Search Index**
   - Go to Atlas UI → Database → Collections
   - Click "Search Indexes" → "Create Index"
   - Use JSON editor:
   ```json
   {
     "mappings": {
       "dynamic": true,
       "fields": {
         "embedding": {
           "dimensions": 1536,
           "similarity": "cosine",
           "type": "knnVector"
         },
         "metadata.file_id": {
           "type": "string"
         }
       }
     }
   }
   ```
   - Name it: `vector_index`

4. **Get Connection String**
   - Click "Connect" → "Connect your application"
   - Copy connection string
   - Replace `<password>` with your actual password

5. **Update .env**
   ```env
   VECTOR_DB_TYPE=atlas-mongo
   ATLAS_MONGO_DB_URI=mongodb+srv://username:password@cluster.mongodb.net/rag_database
   COLLECTION_NAME=embeddings
   ATLAS_SEARCH_INDEX=vector_index
   ```

---

### Setup with Different Embedding Providers

#### Using Ollama (Local, Free)

1. **Install Ollama**
   ```bash
   # Linux
   curl https://ollama.ai/install.sh | sh

   # macOS
   brew install ollama

   # Windows: Download from ollama.ai
   ```

2. **Pull Embedding Model**
   ```bash
   ollama pull nomic-embed-text
   ```

3. **Update .env**
   ```env
   EMBEDDINGS_PROVIDER=ollama
   EMBEDDINGS_MODEL=nomic-embed-text
   OLLAMA_BASE_URL=http://localhost:11434
   ```

#### Using AWS Bedrock

```env
EMBEDDINGS_PROVIDER=bedrock
EMBEDDINGS_MODEL=amazon.titan-embed-text-v1
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_DEFAULT_REGION=us-east-1
```

#### Using Google VertexAI

```env
EMBEDDINGS_PROVIDER=vertexai
EMBEDDINGS_MODEL=text-embedding-004
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
```

---

### Setup with LibreChat Integration

This RAG API can be used as a backend for LibreChat:

1. **Clone LibreChat** (if you haven't already)
   ```bash
   git clone https://github.com/danny-avila/LibreChat.git
   cd LibreChat
   ```

2. **Configure LibreChat**
   - Edit `librechat.yaml`
   - Add RAG endpoint configuration

3. **Update docker-compose.override.yml**
   ```yaml
   rag_api:
     image: your-rag-api-image
     environment:
       - RAG_OPENAI_API_KEY=${RAG_OPENAI_API_KEY}
   ```

4. **Start both services**
   ```bash
   docker compose up -d
   ```

---

### Setup Promptfoo Testing

1. **Install Promptfoo**
   ```bash
   npm install -g promptfoo@latest
   ```

2. **Set Environment Variables**
   ```bash
   export PROMPTFOO_RAG_BASE_URL=http://localhost:8000
   export OPENAI_API_KEY=your-openai-key  # For LLM grading
   ```

3. **Run Tests**
   ```bash
   # Basic evaluation
   npm run test:baseline

   # Security testing
   npm run test:security

   # All tests
   npm run test:all
   ```

---

### Production Deployment Checklist

Before deploying to production:

- [ ] Set `DEBUG_RAG_API=False`
- [ ] Use strong `JWT_SECRET`
- [ ] Enable HTTPS (reverse proxy)
- [ ] Set up database backups
- [ ] Configure monitoring (logs, metrics)
- [ ] Set up rate limiting
- [ ] Use production database (not Docker)
- [ ] Enable structured logging (`CONSOLE_JSON=True`)
- [ ] Set appropriate `CHUNK_SIZE` and `CHUNK_OVERLAP`
- [ ] Test with production data volumes
- [ ] Set up health check monitoring
- [ ] Configure auto-restart (systemd, PM2, etc.)
- [ ] Review and adjust thread pool size
- [ ] Set up API key rotation
- [ ] Configure firewall rules
- [ ] Set up SSL certificates
- [ ] Test failover scenarios

---

## Next Steps

Once setup is complete:

1. **Read the Documentation**
   - [PROJECT_DOCUMENTATION.md](./PROJECT_DOCUMENTATION.md) - Complete project overview
   - [ARCHITECTURE.md](./ARCHITECTURE.md) - System architecture
   - [API_DOCUMENTATION.md](./API_DOCUMENTATION.md) - API reference

2. **Try Examples**
   - Upload various document types
   - Test different questions
   - Experiment with settings

3. **Integrate with Your Application**
   - Use REST API endpoints
   - Implement authentication
   - Customize for your use case

4. **Run Tests**
   - Unit tests: `pytest tests/`
   - Security tests: `npm run test:security`
   - Load tests: Configure Promptfoo performance tests

5. **Contribute**
   - Report issues
   - Submit pull requests
   - Share improvements

---

## Support

If you encounter issues not covered in this guide:

1. Check existing GitHub issues
2. Review application logs: `docker logs rag_fastapi`
3. Check database logs: `docker logs rag_db`
4. Enable debug mode: `DEBUG_RAG_API=True`
5. Create a new GitHub issue with:
   - Error message
   - Steps to reproduce
   - Environment details
   - Relevant logs

---

**Congratulations!** 🎉

Your RAG application should now be up and running. Start uploading documents and asking questions!
