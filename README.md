# 🤖 RAG Application with Interactive Chatbot UI

## 🌟 Overview

This project is a comprehensive **Retrieval-Augmented Generation (RAG)** application that combines powerful document analysis with an intuitive chatbot interface. Built with FastAPI and Langchain, it provides enterprise-grade document processing, vector search, and AI-powered question answering.

### 🎯 What's New

**Interactive Chatbot UI** - A beautiful web interface for document upload and conversational querying:
- 🎨 Modern, responsive design with dark theme
- 📁 Drag-and-drop document upload
- 💬 Real-time chat with your documents
- 🤖 Multiple AI models (Azure GPT-4o-mini, Google Gemini)
- 📊 Source citations with relevance scores
- ⚙️ Adjustable parameters (temperature, retrieval count)

**Access the UI:** Simply start the server and navigate to `http://localhost:8000`

### 🔑 Key Capabilities

- **Interactive Web UI**: Upload documents and chat with them through an elegant interface
- **Multiple AI Models**: Azure OpenAI GPT-4o-mini and Google Gemini support
- **Flexible Vector Storage**: PostgreSQL/pgvector or MongoDB Atlas
- **Multiple Embedding Providers**: Azure, OpenAI, Gemini, HuggingFace, Ollama, Bedrock, VertexAI
- **Security Testing**: Comprehensive Promptfoo integration with OWASP/NIST/MITRE compliance
- **Production-Ready**: Async operations, thread pooling, error handling
- **RESTful API**: Well-documented endpoints for programmatic access

### 📚 Use Cases

1. **Document Q&A**: Upload PDFs, DOCX, or TXT files and ask questions
2. **Research Assistant**: Query across multiple research papers
3. **Knowledge Base**: Build a searchable knowledge base from your documents
4. **LibreChat Integration**: Use as a RAG backend for LibreChat
5. **API Integration**: Programmatic access for custom applications

## ✨ Features

### 🎨 Interactive Chatbot UI
- **Document Upload**: Drag-and-drop or click to upload (PDF, DOCX, TXT, MD, CSV, XLSX, PPTX)
- **Chat Interface**: Real-time conversational interface with typing indicators
- **Source Display**: View exact document chunks used for each answer
- **Document Management**: Upload, select, and delete documents with ease
- **Model Selection**: Switch between Azure GPT-4o-mini and Google Gemini
- **Customizable Settings**: Adjust temperature, retrieval count (k), and more

### 🔧 Core API Features
- **Document Management**: Add, retrieve, and delete documents with file-level organization
- **Vector Search**: Semantic search powered by pgvector or MongoDB Atlas
- **RAG Chat**: AI-powered answers grounded in your documents
- **Multiple Embeddings**: Support for 8+ embedding providers
- **Asynchronous**: High-performance async operations with thread pooling

### 🔐 Security & Testing
- **Promptfoo Integration**: 8 comprehensive test configurations
- **Red Team Testing**: OWASP LLM/API Top 10, NIST AI RMF, MITRE ATLAS
- **Quality Assurance**: Custom graders for accuracy and relevance
- **Performance Benchmarking**: Latency and cost tracking
- **CI/CD Ready**: GitHub Actions workflows included

## 📖 Documentation

- **[USER_GUIDE.md](./USER_GUIDE.md)** - Complete guide for using the chatbot UI and API
- **[PROMPTFOO_REUSABLE_GUIDE.md](./PROMPTFOO_REUSABLE_GUIDE.md)** - How to implement Promptfoo in other projects
- **[PROMPTFOO_IMPLEMENTATION_AUDIT.md](./PROMPTFOO_IMPLEMENTATION_AUDIT.md)** - Security testing feature audit
- **[.env.example](./.env.example)** - Environment variables template
- **API Docs**: http://localhost:8000/docs (when running)

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL with pgvector extension (or MongoDB Atlas)
- Azure OpenAI account OR Google Gemini API key
- Node.js 18+ (for Promptfoo testing)

### 1. Installation

```bash
# Clone repository
git clone <your-repo-url>
cd demo-rag-1-ansa

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# Install Node dependencies for Promptfoo
npm install
```

### 2. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your credentials
```

**Minimum Configuration:**
```env
# Vector Database
VECTOR_DB_TYPE=pgvector
POSTGRES_DB=rag_db
POSTGRES_USER=rag_user
POSTGRES_PASSWORD=your_password
DB_HOST=localhost

# Embeddings (Azure recommended)
EMBEDDINGS_PROVIDER=azure
EMBEDDINGS_MODEL=text-embedding-3-small
RAG_AZURE_OPENAI_API_KEY=your-azure-key
RAG_AZURE_OPENAI_ENDPOINT=https://ai-40mini.cognitiveservices.azure.com/

# Chat Models
AZURE_CHAT_ENDPOINT=https://ai-40mini.cognitiveservices.azure.com/
AZURE_CHAT_API_KEY=your-azure-key
GEMINI_API_KEY=your-gemini-key  # Optional
```

### 3. Start Database

```bash
# Using Docker (recommended)
docker compose -f db-compose.yaml up -d

# Or connect to existing PostgreSQL with pgvector extension
```

### 4. Run the Application

```bash
# Start the server
uvicorn main:app --host 0.0.0.0 --port 8000

# Or with hot reload for development
uvicorn main:app --reload
```

### 5. Access the Chatbot UI

Open your browser and navigate to:
```
http://localhost:8000
```

You should see the interactive chatbot interface! 🎉

## 💬 Using the Chatbot

1. **Upload a Document**: Drag and drop or click to upload (PDF, DOCX, TXT, etc.)
2. **Select Document**: Click the checkmark icon next to the uploaded document
3. **Ask Questions**: Type your question in the chat box and press Enter
4. **View Results**: Get AI-generated answers with source citations
5. **Adjust Settings**: Change model, temperature, or retrieval parameters as needed

See [USER_GUIDE.md](./USER_GUIDE.md) for detailed instructions.

## 🔌 API Endpoints

### Interactive UI
- `GET /` - Chatbot web interface

### Document Operations
- `POST /embed` - Upload and embed document
- `POST /query` - Vector similarity search
- `POST /chat` - RAG-based chat (NEW)
- `GET /documents` - Get documents by IDs
- `DELETE /documents` - Delete documents
- `GET /ids` - List all document IDs
- `GET /health` - Health check

### Example: Chat with Document

```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are the main findings?",
    "file_id": "your-file-id",
    "model": "azure-gpt4o-mini",
    "k": 4,
    "temperature": 0.7
  }'
```

## Setup (Detailed)

### Getting Started

- **Configure `.env` file based on [.env.example](./.env.example)**
- **Setup pgvector database:**
  - Run an existing PSQL/PGVector setup, or,
  - Docker: `docker compose up` (also starts RAG API)
    - or, use docker just for DB: `docker compose -f ./db-compose.yaml up`
- **Run API**:
  - Docker: `docker compose up` (also starts PSQL/pgvector)
    - or, use docker just for RAG API: `docker compose -f ./api-compose.yaml up`
  - Local:
    - Make sure to setup `DB_HOST` to the correct database hostname
    - Run the following commands (preferably in a [virtual environment](https://realpython.com/python-virtual-environments-a-primer/))
```bash
pip install -r requirements.txt
uvicorn main:app
```

### Environment Variables

The following environment variables are required to run the application:

- `RAG_OPENAI_API_KEY`: The API key for OpenAI API Embeddings (if using default settings).
    - Note: `OPENAI_API_KEY` will work but `RAG_OPENAI_API_KEY` will override it in order to not conflict with LibreChat setting.
- `RAG_OPENAI_BASEURL`: (Optional) The base URL for your OpenAI API Embeddings
- `RAG_OPENAI_PROXY`: (Optional) Proxy for OpenAI API Embeddings
    - Note: When using with LibreChat, you can also set `HTTP_PROXY` and `HTTPS_PROXY` environment variables in the `docker-compose.override.yml` file (see [Proxy Configuration](#proxy-configuration) section below)
- `VECTOR_DB_TYPE`: (Optional) select vector database type, default to `pgvector`.
- `POSTGRES_USE_UNIX_SOCKET`: (Optional) Set to "True" when connecting to the PostgreSQL database server with Unix Socket.
- `POSTGRES_DB`: (Optional) The name of the PostgreSQL database, used when `VECTOR_DB_TYPE=pgvector`.
- `POSTGRES_USER`: (Optional) The username for connecting to the PostgreSQL database.
- `POSTGRES_PASSWORD`: (Optional) The password for connecting to the PostgreSQL database.
- `DB_HOST`: (Optional) The hostname or IP address of the PostgreSQL database server.
- `DB_PORT`: (Optional) The port number of the PostgreSQL database server.
- `RAG_HOST`: (Optional) The hostname or IP address where the API server will run. Defaults to "0.0.0.0"
- `RAG_PORT`: (Optional) The port number where the API server will run. Defaults to port 8000.
- `JWT_SECRET`: (Optional) The secret key used for verifying JWT tokens for requests.
  - The secret is only used for verification. This basic approach assumes a signed JWT from elsewhere.
  - Omit to run API without requiring authentication

- `COLLECTION_NAME`: (Optional) The name of the collection in the vector store. Default value is "testcollection".
- `CHUNK_SIZE`: (Optional) The size of the chunks for text processing. Default value is "1500".
- `CHUNK_OVERLAP`: (Optional) The overlap between chunks during text processing. Default value is "100".
- `RAG_UPLOAD_DIR`: (Optional) The directory where uploaded files are stored. Default value is "./uploads/".
- `PDF_EXTRACT_IMAGES`: (Optional) A boolean value indicating whether to extract images from PDF files. Default value is "False".
- `DEBUG_RAG_API`: (Optional) Set to "True" to show more verbose logging output in the server console, and to enable postgresql database routes
- `DEBUG_PGVECTOR_QUERIES`: (Optional) Set to "True" to enable detailed PostgreSQL query logging for pgvector operations. Useful for debugging performance issues with vector database queries.
- `CONSOLE_JSON`: (Optional) Set to "True" to log as json for Cloud Logging aggregations
- `EMBEDDINGS_PROVIDER`: (Optional) either "openai", "bedrock", "azure", "huggingface", "huggingfacetei", "google_genai", "vertexai", or "ollama", where "huggingface" uses sentence_transformers; defaults to "openai"
- `EMBEDDINGS_MODEL`: (Optional) Set a valid embeddings model to use from the configured provider.
    - **Defaults**
    - openai: "text-embedding-3-small"
    - azure: "text-embedding-3-small" (will be used as your Azure Deployment)
    - huggingface: "sentence-transformers/all-MiniLM-L6-v2"
    - huggingfacetei: "http://huggingfacetei:3000". Hugging Face TEI uses model defined on TEI service launch.
    - vertexai: "text-embedding-004"
    - ollama: "nomic-embed-text"
    - bedrock: "amazon.titan-embed-text-v1"
    - google_genai: "gemini-embedding-001"
- `RAG_AZURE_OPENAI_API_VERSION`: (Optional) Default is `2023-05-15`. The version of the Azure OpenAI API.
- `RAG_AZURE_OPENAI_API_KEY`: (Optional) The API key for Azure OpenAI service.
    - Note: `AZURE_OPENAI_API_KEY` will work but `RAG_AZURE_OPENAI_API_KEY` will override it in order to not conflict with LibreChat setting.
- `RAG_AZURE_OPENAI_ENDPOINT`: (Optional) The endpoint URL for Azure OpenAI service, including the resource.
    - Example: `https://YOUR_RESOURCE_NAME.openai.azure.com`.
    - Note: `AZURE_OPENAI_ENDPOINT` will work but `RAG_AZURE_OPENAI_ENDPOINT` will override it in order to not conflict with LibreChat setting.
- `HF_TOKEN`: (Optional) if needed for `huggingface` option.
- `OLLAMA_BASE_URL`: (Optional) defaults to `http://ollama:11434`.
- `ATLAS_SEARCH_INDEX`: (Optional) the name of the vector search index if using Atlas MongoDB, defaults to `vector_index`
- `MONGO_VECTOR_COLLECTION`: Deprecated for MongoDB, please use `ATLAS_SEARCH_INDEX` and `COLLECTION_NAME`
- `AWS_DEFAULT_REGION`: (Optional) defaults to `us-east-1`
- `AWS_ACCESS_KEY_ID`: (Optional) needed for bedrock embeddings
- `AWS_SECRET_ACCESS_KEY`: (Optional) needed for bedrock embeddings
- `GOOGLE_API_KEY`, `GOOGLE_KEY`, `RAG_GOOGLE_API_KEY`: (Optional) Google API key for Google GenAI embeddings. Priority order: RAG_GOOGLE_API_KEY > GOOGLE_KEY > GOOGLE_API_KEY
- `AWS_SESSION_TOKEN`: (Optional) may be needed for bedrock embeddings
- `GOOGLE_APPLICATION_CREDENTIALS`: (Optional) needed for Google VertexAI embeddings. This should be a path to a service account credential file in JSON format, as accepted by [langchain](https://python.langchain.com/api_reference/google_vertexai/index.html)
- `RAG_CHECK_EMBEDDING_CTX_LENGTH` (Optional) Default is true, disabling this will send raw input to the embedder, use this for custom embedding models.

Make sure to set these environment variables before running the application. You can set them in a `.env` file or as system environment variables.

### Promptfoo-based Testing & Security

This project includes comprehensive [Promptfoo](https://www.promptfoo.dev/) integration for automated testing, security scanning, and quality assurance. Five test suites cover everything from basic regressions to full red-team assessments.

#### Quick Start

1. **Install Promptfoo**
   ```bash
   npm install --global promptfoo@latest
   # or run ad-hoc with npx promptfoo@latest ...
   ```

2. **Start the RAG API** (ensure database is running)
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

3. **Configure environment variables**
   ```powershell
   $env:PROMPTFOO_RAG_BASE_URL = "http://127.0.0.1:8000"
   $env:PROMPTFOO_RAG_JWT = "<your_jwt_token>"  # if auth enabled
   $env:OPENAI_API_KEY = "<your_key>"           # for LLM-graded tests
   ```

4. **Run test suites**
   ```bash
   # Quick baseline regression tests
   npx promptfoo@latest eval --config promptfoo.config.yaml
   
   # Test all API endpoints (/query, /embed, /text)
   npx promptfoo@latest eval --config promptfoo.multi-endpoint.yaml
   
   # Advanced guardrails (factuality, PII, policy compliance)
   npx promptfoo@latest eval --config promptfoo.guardrails.yaml
   
   # Focused RAG security red team
   npx promptfoo@latest redteam run --config promptfoo.redteam.yaml
   
   # Comprehensive security scan (40+ attack types)
   npx promptfoo@latest redteam run --config promptfoo.redteam-comprehensive.yaml
   ```

5. **View results**
   - HTML reports are auto-generated (path shown in terminal)
   - Or run: `npx promptfoo@latest view`

#### Test Suites Overview

| Config File | Purpose | Coverage |
|-------------|---------|----------|
| `promptfoo.config.yaml` | Baseline regressions | Basic query validation, leak prevention |
| `promptfoo.multi-endpoint.yaml` | Multi-endpoint tests | `/query`, `/embed`, `/text` endpoints |
| `promptfoo.guardrails.yaml` | Quality & policy | LLM-graded factuality, PII, toxicity, RBAC |
| `promptfoo.performance.yaml` | Performance & load | Latency, cost, concurrency, caching |
| `promptfoo.dataset-driven.yaml` | Data-driven testing | CSV/YAML datasets, custom graders |
| `promptfoo.compare.yaml` | A/B comparison | Compare different RAG configurations |
| `promptfoo.redteam.yaml` | RAG security | 7 plugins, RAG-specific attacks |
| `promptfoo.redteam-comprehensive.yaml` | Full red team | 40+ plugins, OWASP/NIST/MITRE compliance |

#### NPM Scripts (Convenience Commands)

```bash
# Quality & Regression Tests
npm run test:baseline          # Quick baseline checks
npm run test:multi-endpoint    # All endpoint tests
npm run test:guardrails        # LLM-graded quality
npm run test:quality           # All quality tests combined

# Performance & Data
npm run test:performance       # Latency, cost, concurrency
npm run test:dataset           # CSV-driven test cases
npm run test:compare           # A/B config comparison

# Security Tests
npm run test:redteam           # Focused red team
npm run test:redteam:full      # Comprehensive scan
npm run test:redteam:custom    # Custom RAG attack plugin
npm run test:security          # All security tests

# Full Suites
npm run test:all               # All eval tests
npm run test:nightly           # Complete nightly suite

# Utilities
npm run view                   # Open web UI viewer
npm run view:latest            # View latest results
npm run cache:clear            # Clear Promptfoo cache
npm run clean                  # Remove output files
```

#### Custom Providers

Three Python providers enable endpoint-specific testing:
- `promptfoo/providers/rag_http_target.py` – `/query` endpoint
- `promptfoo/providers/rag_embed_target.py` – `/embed` file uploads
- `promptfoo/providers/rag_text_target.py` – `/text` extraction

All providers are configurable via environment variables (no code changes needed).

#### Security Coverage

Red team suites test for:
- **RAG-specific**: Document exfiltration, vector poisoning, prompt extraction, embedding attacks
- **Authorization**: BOLA/BFLA, RBAC, cross-session leaks, cross-tenant isolation
- **Injection**: Prompt, SQL, shell, indirect injection
- **Privacy**: PII leaks (direct, session, social engineering, API/DB)
- **Network**: SSRF, debug access
- **Business logic**: Unauthorized commitments, competitor endorsements
- **Compliance**: OWASP LLM/API Top 10, NIST AI RMF, MITRE ATLAS

#### Advanced Features

**Custom Graders**: Python-based quality scoring for RAG responses
- `promptfoo/graders/rag_quality.py` – Multi-dimensional quality analysis (relevance, completeness, conciseness, factuality)

**Custom Plugins**: RAG-specific attack patterns
- `promptfoo/plugins/custom-rag-attacks.yaml` – Vector database exploits, semantic collision, metadata manipulation

**Dataset Testing**: CSV/YAML-driven test cases
- `promptfoo/datasets/sample_queries.csv` – Sample query variations
- `promptfoo/datasets/edge_cases.yaml` – Boundary conditions and error scenarios

**Global Configuration**: `.promptfoorc.yaml` sets defaults for:
- Output paths, caching, telemetry preferences
- Default timeouts, concurrency limits
- Environment variable presets

#### Documentation

See [`promptfoo/README.md`](./promptfoo/README.md) for:
- Detailed test suite descriptions
- Environment variable reference
- Extending tests with custom cases/graders
- Troubleshooting guide
- Best practices### Use Atlas MongoDB as Vector Database

Instead of using the default pgvector, we could use [Atlas MongoDB](https://www.mongodb.com/products/platform/atlas-vector-search) as the vector database. To do so, set the following environment variables

```env
VECTOR_DB_TYPE=atlas-mongo
ATLAS_MONGO_DB_URI=<mongodb+srv://...>
COLLECTION_NAME=<vector collection>
ATLAS_SEARCH_INDEX=<vector search index>
```

The `ATLAS_MONGO_DB_URI` could be the same or different from what is used by LibreChat. Even if it is the same, the `$COLLECTION_NAME` collection needs to be a completely new one, separate from all collections used by LibreChat. In addition,  create a vector search index for collection above (remember to assign `$ATLAS_SEARCH_INDEX`) with the following json:

```json
{
  "fields": [
    {
      "numDimensions": 1536,
      "path": "embedding",
      "similarity": "cosine",
      "type": "vector"
    },
    {
      "path": "file_id",
      "type": "filter"
    }
  ]
}
```

Follow one of the [four documented methods](https://www.mongodb.com/docs/atlas/atlas-vector-search/create-index/#procedure) to create the vector index.


### Proxy Configuration

When using the RAG API with LibreChat and you need to configure proxy settings, you can set the `HTTP_PROXY` and `HTTPS_PROXY` environment variables in the [`docker-compose.override.yml`](https://www.librechat.ai/docs/configuration/docker_override) file (from the LibreChat repository):

```yaml
rag_api:
    environment:
        - HTTP_PROXY=<your-proxy>
        - HTTPS_PROXY=<your-proxy>
```

This configuration will ensure that all HTTP/HTTPS requests from the RAG API container are routed through your specified proxy server.


### Cloud Installation Settings:

#### AWS:
Make sure your RDS Postgres instance adheres to this requirement:

`The pgvector extension version 0.5.0 is available on database instances in Amazon RDS running PostgreSQL 15.4-R2 and higher, 14.9-R2 and higher, 13.12-R2 and higher, and 12.16-R2 and higher in all applicable AWS Regions, including the AWS GovCloud (US) Regions.`

In order to setup RDS Postgres with RAG API, you can follow these steps:

* Create a RDS Instance/Cluster using the provided [AWS Documentation](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_CreateDBInstance.html).
* Login to the RDS Cluster using the Endpoint connection string from the RDS Console or from your IaC Solution output.
* The login is via the *Master User*.
* Create a dedicated database for rag_api:
``` create database rag_api;```.
* Create a dedicated user\role for that database:
``` create role rag;```

* Switch to the database you just created: ```\c rag_api```
* Enable the Vector extension: ```create extension vector;```
* Use the documentation provided above to set up the connection string to the RDS Postgres Instance\Cluster.

Notes:
  * Even though you're logging with a Master user, it doesn't have all the super user privileges, that's why we cannot use the command: ```create role x with superuser;```
  * If you do not enable the extension, rag_api service will throw an error that it cannot create the extension due to the note above.

### Dev notes:

#### Installing pre-commit formatter

Run the following commands to install pre-commit formatter, which uses [black](https://github.com/psf/black) code formatter:

```bash
pip install pre-commit
pre-commit install



# RAG Application with Interactive Chatbot UI

A production-ready **Retrieval-Augmented Generation (RAG)** application that combines document analysis with an intelligent chatbot interface. Upload documents, ask questions, and get AI-powered answers backed by your own content - all with built-in security guardrails.

## 🎯 What Does This Project Do?

This application allows you to:
- **Upload documents** (PDF, DOCX, TXT, CSV, XLSX, PPTX, and more)
- **Ask questions** about your documents using natural language
- **Get AI-powered answers** with source citations and relevance scores
- **Search semantically** across your document collection using vector embeddings
- **Protect against malicious inputs** with built-in security guardrails
- **Choose from multiple AI models** (Azure GPT-4o-mini, Google Gemini, local Ollama)

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (Web UI)                        │
│  - Document Upload Interface (Drag & Drop)                   │
│  - Chat Interface with Real-time Responses                   │
│  - Settings (Model, Temperature, K results)                  │
│  - Guardrails Toggle (Protected/Demo Mode)                   │
└─────────────────┬───────────────────────────────────────────┘
                  │ HTTP/REST API
┌─────────────────▼───────────────────────────────────────────┐
│                   FastAPI Backend                            │
│  ┌─────────────┬──────────────┬──────────────────────────┐  │
│  │ Document    │ Chat & RAG   │ Guardrails & Security    │  │
│  │ Processing  │ Endpoints    │ Layer                    │  │
│  └─────────────┴──────────────┴──────────────────────────┘  │
└─────────────────┬───────────────────────────────────────────┘
                  │
    ┌─────────────┼─────────────┐
    │             │             │
┌───▼────┐  ┌────▼─────┐  ┌───▼──────┐
│ Vector │  │  LLM     │  │ Document │
│ Store  │  │ Provider │  │ Storage  │
│        │  │          │  │          │
│PgVector│  │Azure GPT │  │  Local   │
│   or   │  │ Gemini   │  │ Uploads  │
│ MongoDB│  │ Ollama   │  │          │
└────────┘  └──────────┘  └──────────┘
```

## 🚀 Quick Start

### Prerequisites

- **Docker & Docker Compose** (recommended) OR
- **Python 3.11+** with pip
- **PostgreSQL** (with pgvector extension) OR **MongoDB Atlas**
- API keys for your chosen LLM provider (Azure OpenAI, Google Gemini, or Ollama)

### Option 1: Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Updated_tech_demo_project
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and configuration
   ```

3. **Start the application**
   ```bash
   docker-compose up -d
   ```

4. **Access the application**
   - Open your browser to: `http://localhost:8000`
   - API documentation: `http://localhost:8000/docs`

### Option 2: Local Development

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up PostgreSQL with pgvector**
   ```bash
   # Install PostgreSQL and pgvector extension
   # Create database: rag_db
   # Create user: rag_user
   ```

3. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your database and API credentials
   ```

4. **Run the application**
   ```bash
   python main.py
   ```

5. **Access at `http://localhost:8000`**

## 📋 Key Features

### 1. Multi-Format Document Support
- **PDF**: With optional image extraction
- **Word Documents**: DOCX format
- **Spreadsheets**: CSV, XLSX
- **Presentations**: PPTX
- **Text Files**: TXT, MD, XML, RST
- **eBooks**: ePub

### 2. Multiple LLM Providers
Choose your AI model:
- **Azure OpenAI**: GPT-4o-mini (production-grade, low latency)
- **Google Gemini**: Gemini 2.0 Flash (free tier available)
- **Ollama**: Local models like DeepSeek R1 (privacy-focused, no API calls)

### 3. Flexible Vector Databases
- **PostgreSQL + pgvector**: Powerful, standard SQL, excellent for most use cases
- **MongoDB Atlas**: Cloud-native, horizontally scalable

### 4. Multiple Embedding Providers
- OpenAI (text-embedding-3-small/large)
- Azure OpenAI
- HuggingFace (sentence-transformers)
- Google Gemini Embeddings
- AWS Bedrock
- Google VertexAI
- Ollama (local embeddings)

### 5. Built-in Security (Guardrails)
Protects against:
- **PII Leakage**: Blocks queries for passwords, API keys, SSNs, credit cards
- **Prompt Injection**: Detects jailbreak attempts and malicious prompts
- **Policy Violations**: Custom rules and regex patterns
- **Authentication Bypass**: Prevents credential extraction

### 6. Advanced Features
- **Semantic Search**: Find documents by meaning, not just keywords
- **Source Citations**: Every answer includes references with relevance scores
- **Async Architecture**: Non-blocking operations for high performance
- **Multi-tenancy**: User/entity isolation for data security
- **Health Monitoring**: Built-in health checks and status endpoints

## 🎨 User Interface Features

### Sidebar (Left Panel)
- **Drag-and-drop upload** with progress tracking
- **Document library** with metadata (size, upload date)
- **Settings panel**:
  - Choose model (Azure GPT-4o-mini, Gemini, Ollama)
  - Adjust temperature (0.0-1.0 for response creativity)
  - Set retrieval count (k = 1-10 results)
- **Guardrails toggle**: Switch between protected and demo mode
- **Advanced operations**: Direct embedding and vector search

### Chat Interface (Main Area)
- **Clean, modern design** with dark theme
- **Typing indicators** for AI responses
- **Source citations** with relevance scores for each answer
- **Auto-scrolling** message history
- **Clear chat** functionality
- **Selected document info** display

## 📖 Complete Workflow

### 1. Document Processing Flow

```
USER UPLOADS FILE (via UI)
    ↓
[Frontend] uploadFile() function
    ├─ Create FormData with file, file_id
    ├─ Show upload progress
    └─ POST /embed
           ↓
[Backend] embed_file() in document_routes.py
    ├─ Save file to ./uploads/{user_id}/{filename}
    ├─ Detect file type (PDF/DOCX/TXT/CSV/etc.)
    ├─ Load content using appropriate loader
    │  ├─ PDFLoader for .pdf
    │  ├─ Docx2txtLoader for .docx
    │  ├─ TextLoader for .txt
    │  └─ etc.
    ├─ Extract text from document
    ├─ Split text into chunks
    │  ├─ RecursiveCharacterTextSplitter
    │  ├─ CHUNK_SIZE = 1500 characters
    │  └─ CHUNK_OVERLAP = 100 characters
    ├─ Generate embeddings for each chunk
    │  └─ Call Azure/OpenAI/Gemini API
    │  └─ Returns 1536-dim vectors (for text-embedding-3-small)
    ├─ Store in vector database
    │  ├─ PostgreSQL: INSERT into langchain_pg_embedding
    │  └─ MongoDB: Insert into collection
    └─ Return metadata {file_id, filename, status}
           ↓
[Frontend] Updates document list and auto-selects
```

### 2. Chat Query Flow (Protected Mode)

```
USER TYPES QUESTION + SENDS
    ↓
[Frontend] sendMessage() in app.js
    ├─ Collect: query, file_id, model, k, temperature
    ├─ Display user message
    ├─ Show typing indicator
    └─ POST /chat
           ↓
[Backend] chat_with_documents() in chat_routes_with_external_guardrails.py
    │
    ├─ STEP 1: GUARDRAIL VALIDATION
    │  └─ validate_with_guardrail(query)
    │     ├─ Check for passwords, API keys, SSNs
    │     ├─ Check for PII (emails, phone numbers)
    │     ├─ Check for prompt injection patterns
    │     └─ If blocked → Return error with reason
    │
    ├─ STEP 2: EMBED QUERY
    │  └─ embeddings.embed_query(query)
    │     └─ Returns query vector [1536 dimensions]
    │
    ├─ STEP 3: VECTOR SEARCH
    │  └─ vector_store.similarity_search_with_score()
    │     ├─ PostgreSQL: cosine similarity
    │     │  └─ SELECT *, embedding <=> query_vector AS distance
    │     │     WHERE metadata->>'file_id' = {file_id}
    │     │     ORDER BY distance LIMIT k
    │     └─ MongoDB: $search operator
    │     └─ Returns: [(Document, score), ...] × k results
    │
    ├─ STEP 4: FORMAT CONTEXT
    │  └─ Create prompt with retrieved chunks:
    │     "[Source 1] (Relevance: 0.95)\n{chunk_text}\n..."
    │
    ├─ STEP 5: LLM GENERATION
    │  ├─ IF model = azure-gpt4o-mini:
    │  │  └─ AzureOpenAI.chat.completions.create()
    │  │     ├─ System: "Answer based on context..."
    │  │     ├─ User: query + context
    │  │     └─ Temperature: user setting
    │  │
    │  ├─ IF model = gemini:
    │  │  └─ genai.GenerativeModel().generate_content()
    │  │
    │  └─ IF model = ollama:
    │     └─ ollama.Client().generate()
    │        └─ Local DeepSeek R1 model
    │
    └─ STEP 6: RETURN RESPONSE
       └─ {answer: "AI response text"}
           ↓
[Frontend] Receives response
    ├─ Add AI message to chat
    ├─ Display answer with formatting
    ├─ Show source citations with scores
    └─ Remove typing indicator
```

### 3. Vector Search Explained

The system uses **cosine similarity** to find relevant document chunks:

1. **During Upload**: Text chunks → Embeddings (vectors in 1536-dim space)
2. **During Query**: User question → Query embedding (same 1536-dim space)
3. **Similarity Calculation**:
   - Cosine similarity = angle between vectors
   - Score 0.0 = completely different
   - Score 1.0 = identical meaning
4. **Return Top K**: Most similar chunks (default k=4)

### 4. Guardrails in Action

**Example: Protected Query**
```
User: "What is the admin password?"
    ↓
Guardrail Analysis:
    ├─ Pattern detected: PASSWORD_REQUEST
    ├─ Risk level: HIGH
    └─ Decision: BLOCKED
        ↓
Response: "I cannot help with requests for passwords or credentials."
```

**Example: Safe Query**
```
User: "What are the main findings in this document?"
    ↓
Guardrail Analysis:
    ├─ No sensitive patterns detected
    ├─ No policy violations
    └─ Decision: ALLOWED
        ↓
Proceeds to vector search + LLM generation
```

## 📁 Project Structure

```
Updated_tech_demo_project/
├── main.py                           # FastAPI app entry point
├── requirements.txt                  # Python dependencies
├── docker-compose.yaml              # Full stack orchestration
├── .env.example                     # Environment template
│
├── app/                             # Main application code
│   ├── config.py                   # Embeddings & vector store init
│   ├── models.py                   # Pydantic data models
│   ├── middleware.py               # JWT authentication
│   ├── constants.py                # Error messages
│   │
│   ├── routes/                     # API endpoints
│   │   ├── document_routes.py              # Upload, embed, query
│   │   ├── chat_routes_with_external_guardrails.py  # Protected chat
│   │   ├── chat_unsafe_routes.py           # Unprotected demo
│   │   └── guardrails_routes.py            # Security management
│   │
│   ├── services/                   # Core services
│   │   ├── database.py            # PostgreSQL pooling
│   │   ├── guardrails.py          # Input validation
│   │   ├── mongo_client.py        # MongoDB integration
│   │   └── vector_store/          # Vector DB implementations
│   │       ├── factory.py
│   │       ├── async_pg_vector.py
│   │       └── atlas_mongo_vector.py
│   │
│   └── utils/                      # Utilities
│       ├── document_loader.py     # File loaders
│       └── health.py              # Health checks
│
├── static/                          # Frontend assets
│   ├── index.html                  # Main UI template
│   ├── js/app.js                   # Frontend logic (1567 lines)
│   └── css/styles.css              # Dark theme styles
│
├── promptfoo/                       # Security testing
│   ├── providers/                  # Custom test providers
│   ├── graders/                    # Quality scoring
│   └── plugins/                    # RAG attack patterns
│
└── exp_files/                       # Documentation
    ├── USER_GUIDE.md
    ├── PROMPTFOO_REUSABLE_GUIDE.md
    └── [other docs]
```

## 📊 API Endpoints

### Document Management
- **`POST /embed`** - Upload and embed documents
  - Request: `file`, `file_id`, `entity_id` (optional)
  - Returns: `{status, message, file_id, filename}`

- **`GET /ids`** - List all document IDs

- **`GET /documents?ids=[]`** - Retrieve specific documents

- **`DELETE /documents`** - Delete documents by ID

- **`GET /documents/{id}/context`** - Get document content

### Query & Chat
- **`POST /query`** - Vector similarity search
  - Request: `{query, file_id, k, entity_id}`
  - Returns: List of matching documents with scores

- **`POST /query-multiple`** - Search multiple documents

- **`POST /chat`** - RAG chat with guardrails (PROTECTED)
  - Request: `{query, file_id, model, k, temperature}`
  - Returns: `{answer}` with source citations

- **`POST /chat-unsafe`** - Chat without guardrails (DEMO ONLY)

### Guardrails
- **`POST /guardrails/{target_id}/analyze`** - Validate prompt
- **`GET /guardrails/{target_id}/policies`** - Get active policies
- **`POST /guardrails/{target_id}/policies`** - Add custom policies

### Utilities
- **`GET /health`** - Health check
- **`GET /`** - Serve web UI
- **`GET /docs`** - API documentation (Swagger)

**Full API documentation at: `http://localhost:8000/docs`**

## 🔧 Configuration

### Essential Environment Variables

**Server Configuration**
```env
RAG_HOST=0.0.0.0
RAG_PORT=8000
DEBUG_RAG_API=False
```

**Vector Database (PostgreSQL)**
```env
VECTOR_DB_TYPE=pgvector
POSTGRES_DB=rag_db
POSTGRES_USER=rag_user
POSTGRES_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

**Embeddings (Azure OpenAI)**
```env
EMBEDDINGS_PROVIDER=azure
EMBEDDINGS_MODEL=text-embedding-3-small
RAG_AZURE_OPENAI_API_KEY=your_key
RAG_AZURE_OPENAI_ENDPOINT=https://your-endpoint.openai.azure.com/
CHUNK_SIZE=1500
CHUNK_OVERLAP=100
```

**Chat Models**
```env
# Azure OpenAI
AZURE_CHAT_ENDPOINT=https://your-endpoint.openai.azure.com/
AZURE_CHAT_API_KEY=your_key

# Google Gemini
GEMINI_API_KEY=your_key

# Ollama (local)
OLLAMA_HOST=http://localhost:11434
```

**Security (Optional)**
```env
JWT_SECRET=your_secret_key  # Enable JWT auth
```

### MongoDB Atlas Alternative

```env
VECTOR_DB_TYPE=atlas-mongo
MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/
MONGODB_DB_NAME=rag_db
COLLECTION_NAME=documents
ATLAS_SEARCH_INDEX=vector_index
```

## 🔒 Security Features

### Guardrails System

**Two Operating Modes:**

1. **Protected Mode (Default)** - Recommended
   - Uses `/chat` endpoint
   - Full guardrail validation
   - Blocks malicious queries
   - Production-ready

2. **Demo Mode (Unsafe)** - For testing only
   - Uses `/chat-unsafe` endpoint
   - No input validation
   - Shows what happens without protection

### What Gets Blocked?

**Sensitive Data Queries**
- Passwords, API keys, tokens, credentials
- SSNs, credit card numbers, bank accounts
- Personal addresses, phone numbers
- Authentication data (JWT, OAuth tokens)

**Jailbreak Attempts**
- Prompt injection patterns
- "DAN" (Do Anything Now) prompts
- Role-playing attacks ("Pretend you are...")
- Context window overflow attempts

**Policy Violations**
- Custom regex rules
- Configurable per-application policies
- Few-shot learning examples

### Authentication (Optional)

Enable JWT by setting `JWT_SECRET`:
```env
JWT_SECRET=your_secure_secret_key
```

All endpoints require:
```
Authorization: Bearer <your-jwt-token>
```

## 🧪 Testing & Quality Assurance

### Security Testing with Promptfoo

Comprehensive testing suite included:

```bash
# Install dependencies
npm install

# Run security tests
npx promptfoo@latest eval --config promptfoo-config.yaml

# View results
npx promptfoo@latest view
```

**Test Coverage:**
- 40+ attack patterns (OWASP, NIST, MITRE)
- Prompt injection tests
- PII extraction attempts
- Jailbreak scenarios
- Policy violation tests
- RAG-specific attacks (document exfiltration, vector poisoning)

## 🎓 For Developers & Beginners

### Understanding the Flow

**Think of this system like a smart librarian:**

1. **Uploading = Building the Library**
   - You give documents to the librarian
   - They read and organize them by topic/meaning
   - Each piece gets a "meaning fingerprint" (embedding vector)

2. **Asking Questions = Consulting the Librarian**
   - You ask a question
   - Librarian finds relevant sections (vector search)
   - Reads those sections to you
   - Gives you an answer with citations

3. **Guardrails = Security Guard**
   - Checks if your question is appropriate
   - Blocks dangerous requests
   - Protects sensitive information

### Key Concepts

**Embeddings**: Numbers that represent meaning
- Similar meanings → similar numbers
- "king" - "man" + "woman" ≈ "queen"
- Enables semantic search (search by meaning, not keywords)

**Vector Database**: Storage optimized for similarity search
- Traditional DB: "Find exact match"
- Vector DB: "Find similar meanings"

**RAG (Retrieval-Augmented Generation)**:
1. Retrieve relevant information from your documents
2. Augment the AI's knowledge with that information
3. Generate an answer based on facts, not hallucinations

### Extending the Application

**Add a New LLM Model:**
1. Edit `app/routes/chat_routes_with_external_guardrails.py`
2. Add model handling in the if/elif chain
3. Update frontend dropdown in `static/js/app.js`

**Add Custom Guardrail Rules:**
```python
POST /guardrails/my-app/policies
{
  "name": "Block crypto queries",
  "pattern": "bitcoin|ethereum|crypto",
  "severity": "high"
}
```

**Add New Document Format:**
1. Update `app/utils/document_loader.py`
2. Add LangChain loader import
3. Update `get_loader()` function with new extension

**Change Chunk Size:**
```env
CHUNK_SIZE=2000    # Larger chunks = more context
CHUNK_OVERLAP=200  # More overlap = better continuity
```

## 🐛 Troubleshooting

### Common Issues

**"Connection refused" on startup**
- Check PostgreSQL is running: `docker ps | grep postgres`
- Verify `DB_HOST` and `DB_PORT` in `.env`

**"Vector store initialization failed"**
- Ensure pgvector extension is installed
- Check database permissions
- Verify `VECTOR_DB_TYPE` matches your setup

**"API key invalid" errors**
- Double-check API keys in `.env`
- Ensure no extra spaces or quotes
- Verify endpoint URLs are correct

**File upload fails**
- Check file size (default max: 50MB)
- Verify supported format (PDF/DOCX/TXT/etc.)
- Check disk space and permissions

**Chat not responding**
- Select a document first in the UI
- Check model API keys are valid
- Review browser console (F12) for errors
- Check server logs: `docker logs <container>`

**Embeddings taking too long**
- Switch to faster provider (Azure > OpenAI > Gemini)
- Reduce chunk size
- Use local Ollama embeddings for privacy

## 📚 Additional Documentation

- **[WORKFLOW.md](./WORKFLOW.md)** - Detailed step-by-step workflow
- **[API_DOCUMENTATION.md](./API_DOCUMENTATION.md)** - Complete API reference
- **[ARCHITECTURE.md](./ARCHITECTURE.md)** - Technical deep-dive
- **[USER_GUIDE.md](./exp_files/USER_GUIDE.md)** - UI usage guide
- **[PROMPTFOO_REUSABLE_GUIDE.md](./exp_files/PROMPTFOO_REUSABLE_GUIDE.md)** - Security testing

## 🤝 Contributing

Contributions welcome! Process:
1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Make changes with tests
4. Run security tests: `npx promptfoo@latest eval`
5. Commit: `git commit -m "Add amazing feature"`
6. Push: `git push origin feature/amazing-feature`
7. Open Pull Request

## 🙏 Acknowledgments

Built with:
- [FastAPI](https://fastapi.tiangolo.com/) - High-performance web framework
- [LangChain](https://python.langchain.com/) - Document processing & embeddings
- [pgvector](https://github.com/pgvector/pgvector) - Vector similarity search
- [Promptfoo](https://www.promptfoo.dev/) - Security testing framework
- [Azure OpenAI](https://azure.microsoft.com/en-us/products/ai-services/openai-service)
- [Google Gemini](https://ai.google.dev/)
- [Ollama](https://ollama.ai/) - Local LLM runtime

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/your-repo/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-repo/discussions)

---

**Made with ❤️ for the RAG community**
