# Complete Project Documentation

## Table of Contents
1. [Project Overview](#project-overview)
2. [What This Project Does](#what-this-project-does)
3. [Key Features](#key-features)
4. [Technology Stack](#technology-stack)
5. [Project Structure](#project-structure)
6. [How It Works - Step by Step](#how-it-works---step-by-step)
7. [Component Explanation](#component-explanation)
8. [Data Flow](#data-flow)
9. [Security Features](#security-features)
10. [Testing & Quality Assurance](#testing--quality-assurance)

---

## Project Overview

This is a **Retrieval-Augmented Generation (RAG) Application** with an interactive chatbot interface. It allows users to upload documents (PDF, DOCX, TXT, etc.) and ask questions about them. The system uses AI models to provide accurate answers based on the uploaded documents.

### What is RAG?
RAG (Retrieval-Augmented Generation) is an AI technique that:
1. **Retrieves** relevant information from your documents
2. **Augments** the AI model's knowledge with this information
3. **Generates** accurate answers based on the retrieved content

This prevents the AI from making things up and ensures answers are grounded in your actual documents.

---

## What This Project Does

### Primary Functions

1. **Document Upload & Processing**
   - Users upload documents through a web interface
   - System extracts text from various file formats
   - Text is split into manageable chunks
   - Each chunk is converted into mathematical vectors (embeddings)
   - Vectors are stored in a database for fast searching

2. **Semantic Search**
   - When you ask a question, it's converted to a vector
   - The system finds document chunks with similar meaning
   - Uses cosine similarity to rank relevance
   - Returns the most relevant passages

3. **AI-Powered Question Answering**
   - Takes your question + relevant document chunks
   - Sends them to an AI model (GPT-4o-mini or Gemini)
   - AI generates an answer based on the documents
   - Returns answer with source citations

4. **Security & Validation**
   - Validates all user inputs before processing
   - Blocks attempts to extract sensitive information
   - Redacts sensitive data from responses
   - Implements comprehensive security guardrails

---

## Key Features

### Interactive Web UI
- **Drag-and-drop document upload**
  - Supported formats: PDF, DOCX, TXT, MD, CSV, XLSX, PPTX
  - Real-time upload progress
  - Document management (view, select, delete)

- **Chat Interface**
  - Real-time conversational interface
  - Typing indicators for better UX
  - Message history
  - Source citations with relevance scores

- **Customizable Settings**
  - Model selection (Azure GPT-4o-mini, Google Gemini)
  - Temperature control (creativity vs. precision)
  - Retrieval count (k parameter)
  - Entity ID for multi-tenant scenarios

### Backend Features
- **Multiple AI Model Support**
  - Azure OpenAI (GPT-4o-mini)
  - Google Gemini (gemini-1.5-flash)
  - Extensible architecture for adding more models

- **Flexible Vector Storage**
  - PostgreSQL with pgvector extension
  - MongoDB Atlas Vector Search
  - Easy configuration via environment variables

- **8+ Embedding Providers**
  - Azure OpenAI
  - OpenAI
  - Google Gemini
  - HuggingFace (sentence-transformers)
  - HuggingFace TEI (Text Embeddings Inference)
  - Ollama
  - AWS Bedrock
  - Google VertexAI

- **Production-Ready Architecture**
  - Asynchronous operations for high performance
  - Thread pooling for CPU-bound tasks
  - Connection pooling for database
  - Comprehensive error handling
  - Structured logging (JSON support)

### Security Features
- **Adaptive Guardrails System**
  - Input validation before AI processing
  - Policy-based blocking of sensitive queries
  - Pattern matching for attack detection
  - Redaction of sensitive data in responses

- **Multi-Layer Security**
  - JWT authentication support (optional)
  - User isolation and authorization
  - CORS protection
  - Request validation
  - SQL injection prevention

### Testing & Quality Assurance
- **Promptfoo Integration**
  - 8 comprehensive test configurations
  - Red team testing for security
  - Quality assurance with custom graders
  - Performance benchmarking
  - OWASP/NIST/MITRE compliance testing

---

## Technology Stack

### Backend
- **Framework**: FastAPI (Python 3.11+)
  - Modern, fast web framework
  - Automatic API documentation
  - Async/await support
  - Type hints and validation

- **Language Models**
  - Langchain framework for LLM orchestration
  - Azure OpenAI API
  - Google Generative AI

- **Vector Databases**
  - PostgreSQL with pgvector extension
  - MongoDB Atlas Vector Search

- **Document Processing**
  - PyPDF for PDF files
  - Unstructured for complex documents
  - python-docx for Word documents
  - openpyxl for Excel files
  - python-pptx for PowerPoint

### Frontend
- **Pure JavaScript** (no framework)
- **HTML5/CSS3**
- **Responsive Design**
- **Modern UI with dark theme**

### Infrastructure
- **Docker** for containerization
- **Docker Compose** for orchestration
- **Uvicorn** ASGI server
- **Node.js** for Promptfoo testing

### Database
- **PostgreSQL 15+** with pgvector extension
  - Vector similarity search
  - ACID compliance
  - JSON support for metadata

- **MongoDB Atlas** (alternative)
  - Vector search capabilities
  - Cloud-native
  - Flexible schema

---

## Project Structure

```
Updated_tech_demo_project/
│
├── app/                          # Main application code
│   ├── __init__.py
│   ├── config.py                 # Configuration and settings
│   ├── constants.py              # Application constants
│   ├── models.py                 # Pydantic data models
│   ├── middleware.py             # Security middleware
│   │
│   ├── routes/                   # API endpoint definitions
│   │   ├── __init__.py
│   │   ├── document_routes.py   # Document upload/query endpoints
│   │   ├── chat_routes_with_external_guardrails.py  # Protected chat
│   │   ├── chat_unsafe_routes.py   # Demo: unsafe chat (no guardrails)
│   │   └── guardrails_routes.py    # Guardrail testing endpoints
│   │
│   ├── services/                # Business logic services
│   │   ├── __init__.py
│   │   ├── database.py          # PostgreSQL connection management
│   │   ├── mongo_client.py      # MongoDB connection management
│   │   ├── guardrails.py        # Security guardrails implementation
│   │   │
│   │   └── vector_store/        # Vector database implementations
│   │       ├── __init__.py
│   │       ├── factory.py       # Vector store factory pattern
│   │       ├── async_pg_vector.py      # Async PostgreSQL vector store
│   │       ├── extended_pg_vector.py   # Extended pgvector features
│   │       └── atlas_mongo_vector.py   # MongoDB Atlas vector store
│   │
│   └── utils/                   # Utility functions
│       ├── __init__.py
│       ├── document_loader.py   # Document loading and processing
│       └── health.py            # Health check utilities
│
├── static/                      # Frontend assets
│   ├── index.html              # Main web interface
│   ├── css/
│   │   └── style.css           # Styling
│   └── js/
│       └── app.js              # Frontend JavaScript logic
│
├── promptfoo/                   # Testing framework
│   ├── README.md               # Promptfoo documentation
│   ├── providers/              # Custom test providers
│   │   ├── rag_http_target.py       # HTTP endpoint testing
│   │   ├── rag_embed_target.py      # Embedding endpoint testing
│   │   ├── rag_text_target.py       # Text extraction testing
│   │   └── chat_target.py           # Chat endpoint testing
│   │
│   ├── graders/                # Custom quality graders
│   │   └── rag_quality.py      # RAG response quality grading
│   │
│   ├── plugins/                # Security test plugins
│   │   └── custom-rag-attacks.yaml  # RAG-specific attack patterns
│   │
│   └── datasets/               # Test datasets
│       ├── sample_queries.csv       # Sample test queries
│       └── edge_cases.yaml          # Edge case scenarios
│
├── tests/                       # Unit and integration tests
│   ├── utils/
│   └── services/
│
├── utils/                       # Utility scripts
│   └── docker/                 # Docker-related utilities
│
├── main.py                      # Application entry point
├── requirements.txt             # Python dependencies
├── requirements.lite.txt        # Minimal dependencies
├── Dockerfile                   # Docker image definition
├── Dockerfile.lite              # Lightweight Docker image
├── docker-compose.yaml          # Full stack composition
├── db-compose.yaml             # Database-only composition
├── api-compose.yaml            # API-only composition
│
├── .env.example                # Environment variables template
├── .pre-commit-config.yaml     # Pre-commit hooks
├── .promptfoorc.yaml           # Promptfoo configuration
│
├── promptfoo.*.yaml            # Various test configurations
│   ├── promptfoo.evaluation.yaml
│   ├── promptfoo.redteam.yaml
│   ├── promptfoo.redteam-rag.yaml
│   ├── promptfoo.guardrails-llm.yaml
│   ├── promptfoo.model-comparison.yaml
│   └── ...
│
├── package.json                # Node.js dependencies (Promptfoo)
├── package-lock.json
│
└── README.md                   # Main project documentation
```

### Key Directories Explained

- **`app/`**: Core application logic
  - `routes/`: API endpoint handlers
  - `services/`: Business logic and data access
  - `utils/`: Helper functions

- **`static/`**: Web interface files (HTML, CSS, JavaScript)

- **`promptfoo/`**: Comprehensive testing suite
  - Security testing
  - Quality assurance
  - Performance benchmarking

- **`tests/`**: Traditional unit/integration tests

---

## How It Works - Step by Step

### 1. Application Startup

```
┌─────────────────────────────────────────────────────┐
│ 1. Load environment variables from .env             │
│ 2. Initialize logging configuration                 │
│ 3. Connect to vector database (PostgreSQL/MongoDB)  │
│ 4. Initialize embedding provider                    │
│ 5. Create thread pool for async operations          │
│ 6. Start FastAPI server on port 8000               │
│ 7. Serve web UI at http://localhost:8000           │
└─────────────────────────────────────────────────────┘
```

**What happens in detail:**

1. **Environment Setup** (`app/config.py`)
   - Reads `.env` file for configuration
   - Validates required variables
   - Sets up database connections
   - Configures embedding models

2. **Database Initialization** (`main.py` - `lifespan` function)
   - Creates connection pool to PostgreSQL
   - Ensures pgvector extension is enabled
   - Creates vector indexes for performance
   - Sets up async query capabilities

3. **Thread Pool Creation**
   - Creates bounded thread pool (max 8 workers)
   - Used for CPU-bound operations
   - Prevents resource exhaustion
   - Example: Document parsing, embedding generation

4. **FastAPI Application Setup**
   - Registers all API routes
   - Configures CORS middleware
   - Sets up logging middleware
   - Adds security middleware
   - Mounts static file serving

---

### 2. Document Upload & Embedding

```
User uploads document.pdf
         ↓
┌─────────────────────────────────────────────────────┐
│ STEP 1: Receive File                                │
│ - POST /embed endpoint                              │
│ - Validate file type and size                       │
│ - Save to temporary location                        │
└─────────────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────────────┐
│ STEP 2: Extract Text                                │
│ - Detect file type (PDF, DOCX, etc.)               │
│ - Use appropriate loader (PyPDF, unstructured)     │
│ - Extract all text content                         │
│ - Clean text (remove null bytes, normalize)        │
└─────────────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────────────┐
│ STEP 3: Chunk Text                                  │
│ - Split into chunks (default: 1500 characters)     │
│ - With overlap (default: 100 characters)           │
│ - Preserve context across chunks                   │
│ - Example: "The quick brown fox..." (chunk 1)      │
│             "...fox jumps over..." (chunk 2)        │
└─────────────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────────────┐
│ STEP 4: Generate Embeddings                         │
│ - For each chunk:                                   │
│   • Send text to embedding model                    │
│   • Receive 1536-dimensional vector                 │
│   • Vector represents semantic meaning              │
│ - Example: "artificial intelligence"                │
│   → [0.234, -0.891, 0.456, ...]                    │
└─────────────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────────────┐
│ STEP 5: Store in Vector Database                    │
│ - Save each chunk with:                             │
│   • page_content: Original text                     │
│   • embedding: Vector representation                │
│   • metadata:                                       │
│     - file_id: Unique document identifier           │
│     - user_id: Who uploaded it                      │
│     - digest: MD5 hash for deduplication           │
│     - source: Original filename                     │
│     - page: Page number (if applicable)            │
└─────────────────────────────────────────────────────┘
         ↓
   Return success response to user
```

**Detailed Explanation:**

**STEP 1: File Reception** (`document_routes.py` - `embed_file`)
- User uploads file via drag-and-drop or file picker
- FastAPI receives multipart/form-data request
- File is validated (type, size limits)
- Saved to `./uploads/{user_id}/{filename}`
- Async file operations prevent blocking

**STEP 2: Text Extraction** (`utils/document_loader.py`)
- System detects file type from extension and MIME type
- Selects appropriate loader:
  - **PDF**: PyPDF with OCR support
  - **DOCX**: python-docx
  - **TXT/MD**: Direct read with encoding detection
  - **CSV**: pandas with custom parsing
  - **XLSX**: openpyxl
  - **PPTX**: python-pptx
- Extracts all text, preserving structure where possible
- Handles encoding issues (UTF-8, Latin-1, etc.)

**STEP 3: Text Chunking** (`document_routes.py` - `store_data_in_vector_db`)
- Uses `RecursiveCharacterTextSplitter`
- Splits on paragraph boundaries first
- Then sentences, then words if needed
- Overlap ensures context continuity
- Example with chunk_size=100, overlap=20:
  ```
  Chunk 1: "The artificial intelligence system processes data efficiently..."
  Chunk 2: "...processes data efficiently and generates accurate results..."
  ```

**STEP 4: Embedding Generation** (`app/config.py` - `init_embeddings`)
- Each chunk sent to embedding API
- Models convert text to vector:
  - Azure/OpenAI: text-embedding-3-small (1536 dimensions)
  - Gemini: text-embedding-004 (768 dimensions)
  - HuggingFace: all-MiniLM-L6-v2 (384 dimensions)
- Vector captures semantic meaning
- Similar meanings have similar vectors
- Distance between vectors = semantic similarity

**STEP 5: Database Storage** (`services/vector_store/`)
- PostgreSQL with pgvector:
  - Stores in `langchain_pg_embedding` table
  - Uses GIN index for fast search
  - HNSW index for approximate nearest neighbor
- MongoDB Atlas:
  - Stores in custom collection
  - Uses Atlas Vector Search index
- Metadata enables filtering by user, document, etc.

---

### 3. Question Answering Flow

```
User asks: "What are the main findings?"
         ↓
┌─────────────────────────────────────────────────────┐
│ STEP 1: Security Validation (Guardrails)            │
│ - Check for sensitive queries                       │
│ - Validate against policies                         │
│ - Block attempts to extract passwords, SSNs, etc.  │
│ - If blocked: Return error message                 │
└─────────────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────────────┐
│ STEP 2: Query Embedding                             │
│ - Convert question to vector                        │
│ - Use same embedding model as documents             │
│ - "What are the main findings?"                     │
│   → [0.123, -0.567, 0.890, ...]                    │
└─────────────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────────────┐
│ STEP 3: Vector Search                               │
│ - Calculate similarity with all document chunks     │
│ - Use cosine similarity metric                      │
│ - Rank by relevance score                          │
│ - Return top K results (default: k=4)              │
│                                                     │
│ Example Results:                                    │
│ 1. "The study found three key results..." (0.89)   │
│ 2. "Main findings include improved..." (0.85)      │
│ 3. "Our research demonstrates..." (0.82)           │
│ 4. "The primary conclusions are..." (0.78)         │
└─────────────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────────────┐
│ STEP 4: Context Preparation                         │
│ - Combine top K chunks into context                │
│ - Format as: "Context 1: ...\nContext 2: ..."      │
│ - Add metadata (source, page numbers)              │
│ - Prepare for LLM prompt                           │
└─────────────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────────────┐
│ STEP 5: LLM Query                                   │
│ - Build prompt:                                     │
│   System: "Answer based on context only"            │
│   Context: [Retrieved chunks]                       │
│   Question: "What are the main findings?"           │
│ - Send to AI model (GPT-4o-mini or Gemini)        │
│ - Model parameters:                                 │
│   • temperature: 0.7 (balanced creativity)          │
│   • max_tokens: Automatic                          │
│   • stop_sequences: None                           │
└─────────────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────────────┐
│ STEP 6: Response Processing                         │
│ - Receive AI-generated answer                       │
│ - Apply output guardrails:                          │
│   • Redact sensitive patterns                       │
│   • Validate response quality                       │
│ - Format response with:                             │
│   • answer: AI-generated text                       │
│   • sources: Retrieved chunks with scores           │
│   • model_used: Which AI model responded           │
└─────────────────────────────────────────────────────┘
         ↓
    Return JSON response to frontend
         ↓
    Display in chat interface
```

**Detailed Explanation:**

**STEP 1: Security Validation** (`services/guardrails.py`)
- Query passes through `AdaptiveGuardrail`
- Checks against 200+ sensitive keywords
- Pattern matching for attack attempts:
  - Prompt injection: "Ignore previous instructions..."
  - Data exfiltration: "List all passwords..."
  - Jailbreak attempts: "Act as an unrestricted AI..."
- Risk levels: low, medium, high, critical
- Blocked queries return friendly error message

**STEP 2: Query Embedding** (`document_routes.py` - `get_cached_query_embedding`)
- Same process as document embedding
- Uses LRU cache for repeated queries
- Cache size: 128 queries
- Significantly improves performance for common questions

**STEP 3: Vector Search** (`services/vector_store/`)
- PostgreSQL pgvector:
  ```sql
  SELECT *, embedding <=> query_vector AS distance
  FROM langchain_pg_embedding
  WHERE metadata->>'file_id' = 'user-file-id'
  ORDER BY distance
  LIMIT 4;
  ```
- Cosine similarity: 1.0 = identical, 0.0 = unrelated
- Typical good scores: 0.75+
- Filters by file_id, user_id for security

**STEP 4: Context Preparation** (`routes/chat_routes_with_external_guardrails.py`)
- Combines retrieved chunks
- Adds source information
- Formats for optimal LLM comprehension
- Example format:
  ```
  Context from document.pdf, page 3:
  "The main findings indicate that..."

  Context from document.pdf, page 7:
  "Additional results show..."
  ```

**STEP 5: LLM Query**
- **Azure GPT-4o-mini**:
  - Fast, cost-effective
  - Good for factual questions
  - 128k token context window

- **Google Gemini (gemini-1.5-flash)**:
  - Very fast inference
  - Competitive quality
  - 1M token context window
  - Direct API integration

- Prompt engineering:
  ```
  You are a helpful assistant that answers questions based only on
  the provided context. If the answer is not in the context, say so.

  Context:
  {retrieved_chunks}

  Question: {user_question}

  Answer:
  ```

**STEP 6: Response Processing**
- Output guardrails redact:
  - API keys: `sk_live_xxxxx` → `[REDACTED_API_KEY]`
  - Secrets: `secret_key=xxxxx` → `[REDACTED_SECRET]`
  - Credit cards: `4532-1234-5678-9010` → `[REDACTED_CREDIT_CARD]`
  - SSN: `123-45-6789` → `[REDACTED_SSN]`
- Response includes:
  - Answer text
  - Source citations
  - Relevance scores
  - Model identification

---

### 4. Frontend Interaction Flow

```
┌─────────────────────────────────────────────────────┐
│ User opens http://localhost:8000                    │
│ ↓                                                   │
│ Browser loads static/index.html                     │
│ ↓                                                   │
│ JavaScript (static/js/app.js) initializes           │
│ ↓                                                   │
│ Fetch uploaded documents (GET /ids)                 │
│ ↓                                                   │
│ Display document list                               │
└─────────────────────────────────────────────────────┘

When user uploads document:
┌─────────────────────────────────────────────────────┐
│ 1. File selected via drag-drop or file input        │
│ 2. JavaScript reads file                            │
│ 3. POST /embed with FormData                       │
│ 4. Show upload progress                            │
│ 5. On success: Refresh document list               │
│ 6. Display success notification                     │
└─────────────────────────────────────────────────────┘

When user asks question:
┌─────────────────────────────────────────────────────┐
│ 1. User types question and presses Enter            │
│ 2. Validate: document selected, question not empty  │
│ 3. Display user message in chat                    │
│ 4. Show "thinking" indicator                       │
│ 5. POST /chat with JSON body                       │
│ 6. Receive response                                │
│ 7. Display AI answer                               │
│ 8. Show source citations                           │
│ 9. Enable interactions again                       │
└─────────────────────────────────────────────────────┘
```

---

## Component Explanation

### 1. Main Application (`main.py`)

**Purpose**: Application entry point and lifecycle management

**Key Functions**:
```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize resources
    # - Thread pool for CPU-bound tasks
    # - Database connections
    # - Vector indexes

    yield  # Application runs

    # Shutdown: Cleanup resources
    # - Close thread pool
    # - Close database connections
```

**Why Async Lifespan?**
- Ensures proper resource initialization before handling requests
- Guarantees cleanup on shutdown
- Prevents resource leaks

---

### 2. Configuration (`app/config.py`)

**Purpose**: Centralized configuration management

**Key Components**:

1. **Environment Variable Loading**
   ```python
   POSTGRES_DB = get_env_variable("POSTGRES_DB", "mydatabase")
   EMBEDDINGS_PROVIDER = get_env_variable("EMBEDDINGS_PROVIDER", "openai")
   ```

2. **Embedding Initialization**
   - Supports 8 providers
   - Lazy initialization
   - Type safety with Enums

3. **Vector Store Factory**
   - Creates appropriate vector store based on config
   - Connection pooling
   - Async support

4. **Logging Configuration**
   - Structured logging
   - JSON output for cloud logging
   - Debug mode support
   - Request/response logging

---

### 3. Data Models (`app/models.py`)

**Purpose**: Type-safe data structures with validation

**Key Models**:

1. **ChatRequest**
   ```python
   class ChatRequest(BaseModel):
       query: str              # User's question
       file_id: str            # Which document to query
       model: str = "azure-gpt4o-mini"  # AI model
       k: int = 4             # Number of chunks to retrieve
       temperature: float = 0.7  # AI creativity
       entity_id: Optional[str] = None  # Multi-tenant support
   ```

2. **ChatResponse**
   ```python
   class ChatResponse(BaseModel):
       answer: str                    # AI-generated answer
       sources: List[SourceDocument]  # Retrieved chunks
       model_used: str                # Which model responded
   ```

3. **SourceDocument**
   ```python
   class SourceDocument(BaseModel):
       content: str           # Chunk text
       score: float          # Relevance score
       metadata: dict        # Source info (page, file, etc.)
   ```

**Why Pydantic Models?**
- Automatic validation
- Type checking
- JSON serialization
- API documentation generation
- Clear contracts between frontend and backend

---

### 4. Document Routes (`app/routes/document_routes.py`)

**Purpose**: Handle document upload, storage, and retrieval

**Key Endpoints**:

1. **POST /embed** - Upload and embed document
   - Async file upload
   - Concurrent processing
   - Error handling
   - Temporary file cleanup

2. **POST /query** - Search for relevant chunks
   - Vector similarity search
   - User authorization
   - Caching for performance
   - Score-based ranking

3. **GET /documents** - Retrieve document by ID
   - Batch retrieval support
   - Metadata filtering
   - Authorization checks

4. **DELETE /documents** - Remove documents
   - Batch deletion
   - Authorization validation
   - Cascade cleanup

5. **POST /text** - Extract text without embedding
   - Useful for preview
   - No database storage
   - Fast text extraction

---

### 5. Chat Routes (`app/routes/chat_routes_with_external_guardrails.py`)

**Purpose**: Protected chat endpoint with security guardrails

**Flow**:
```python
@router.post("/chat", response_model=ChatResponse)
async def chat_with_document(request: ChatRequest):
    # 1. Validate request
    # 2. Check guardrails (block sensitive queries)
    # 3. Retrieve relevant context
    # 4. Query AI model
    # 5. Apply output guardrails
    # 6. Return response
```

**Security Features**:
- Pre-flight guardrail checks
- Context redaction
- Output validation
- Error handling
- Rate limiting ready

---

### 6. Guardrails Service (`app/services/guardrails.py`)

**Purpose**: Adaptive security guardrails following Promptfoo patterns

**Architecture**:
```
┌──────────────────────────────────────────────────┐
│            AdaptiveGuardrail                     │
│                                                  │
│  ┌────────────────────────────────────────────┐ │
│  │  Policies (GuardrailPolicy)                │ │
│  │  - Block passwords                         │ │
│  │  - Block SSN                               │ │
│  │  - Block API keys                          │ │
│  │  - Block credit cards                      │ │
│  │  - etc. (15+ default policies)             │ │
│  └────────────────────────────────────────────┘ │
│                                                  │
│  ┌────────────────────────────────────────────┐ │
│  │  Examples (GuardrailExample)               │ │
│  │  - Training examples of attacks            │ │
│  │  - Jailbreak attempts                      │ │
│  │  - Extraction techniques                   │ │
│  └────────────────────────────────────────────┘ │
│                                                  │
│  ┌────────────────────────────────────────────┐ │
│  │  Pattern Matching                          │ │
│  │  - 200+ sensitive keywords                 │ │
│  │  - Regex patterns for data formats         │ │
│  │  - Attack signature detection              │ │
│  └────────────────────────────────────────────┘ │
│                                                  │
│  ┌────────────────────────────────────────────┐ │
│  │  Redaction Engine                          │ │
│  │  - API key patterns                        │ │
│  │  - Credit card numbers                     │ │
│  │  - SSN formats                             │ │
│  │  - Private keys                            │ │
│  └────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────┘
```

**Key Features**:
- Policy-based validation
- Pattern matching with regex
- Few-shot learning support
- Automatic redaction
- Risk assessment
- Extensible architecture

---

### 7. Vector Store (`app/services/vector_store/`)

**Purpose**: Abstract vector database operations

**Factory Pattern** (`factory.py`):
```python
def get_vector_store(connection_string, embeddings, collection_name, mode):
    if mode == "async":
        return AsyncPgVector(...)  # PostgreSQL async
    elif mode == "atlas-mongo":
        return AtlasMongoVector(...)  # MongoDB
    else:
        return ExtendedPGVector(...)  # PostgreSQL sync
```

**Implementations**:

1. **AsyncPgVector** - Async PostgreSQL
   - Non-blocking I/O
   - Connection pooling
   - High concurrency
   - Best for production

2. **ExtendedPGVector** - Sync PostgreSQL
   - Simpler code
   - Lower overhead
   - Good for development

3. **AtlasMongoVector** - MongoDB Atlas
   - Cloud-native
   - Flexible schema
   - Built-in vector search

---

### 8. Document Loader (`app/utils/document_loader.py`)

**Purpose**: Extract text from various file formats

**Supported Formats**:
- **PDF**: PyPDF with OCR, image extraction
- **DOCX**: python-docx for Word
- **TXT/MD**: Direct read, encoding detection
- **CSV**: pandas parsing
- **XLSX**: openpyxl for Excel
- **PPTX**: python-pptx for PowerPoint
- **Source Code**: 50+ programming languages

**Features**:
- Automatic encoding detection (chardet)
- UTF-8 conversion for compatibility
- Error handling for corrupted files
- Metadata preservation
- Temporary file management

---

## Data Flow

### Complete Request-Response Cycle

```
┌─────────────┐
│   Browser   │
└──────┬──────┘
       │ HTTP Request
       ↓
┌─────────────────────────────────────────┐
│         FastAPI Server                  │
│  ┌────────────────────────────────────┐ │
│  │ 1. CORS Middleware                 │ │
│  │    - Validate origin               │ │
│  │    - Add CORS headers              │ │
│  └────────────────────────────────────┘ │
│               ↓                         │
│  ┌────────────────────────────────────┐ │
│  │ 2. Logging Middleware              │ │
│  │    - Log request details           │ │
│  │    - Measure timing                │ │
│  └────────────────────────────────────┘ │
│               ↓                         │
│  ┌────────────────────────────────────┐ │
│  │ 3. Security Middleware             │ │
│  │    - JWT validation (optional)     │ │
│  │    - Request sanitization          │ │
│  └────────────────────────────────────┘ │
│               ↓                         │
│  ┌────────────────────────────────────┐ │
│  │ 4. Route Handler                   │ │
│  │    - Parse request body            │ │
│  │    - Validate with Pydantic        │ │
│  │    - Execute business logic        │ │
│  └────────────────────────────────────┘ │
│               ↓                         │
│  ┌────────────────────────────────────┐ │
│  │ 5. Guardrails Check                │ │
│  │    - Validate query                │ │
│  │    - Block sensitive requests      │ │
│  └────────────────────────────────────┘ │
│               ↓                         │
│  ┌────────────────────────────────────┐ │
│  │ 6. Vector Store Query              │ │
│  │    - Embed query                   │ │
│  │    - Search database               │ │
│  │    - Rank results                  │ │
│  └────────────────────────────────────┘ │
│               ↓                         │
│  ┌────────────────────────────────────┐ │
│  │ 7. LLM Query                       │ │
│  │    - Build prompt                  │ │
│  │    - Call AI model                 │ │
│  │    - Parse response                │ │
│  └────────────────────────────────────┘ │
│               ↓                         │
│  ┌────────────────────────────────────┐ │
│  │ 8. Response Guardrails             │ │
│  │    - Redact sensitive data         │ │
│  │    - Validate output               │ │
│  └────────────────────────────────────┘ │
│               ↓                         │
│  ┌────────────────────────────────────┐ │
│  │ 9. Format Response                 │ │
│  │    - Create JSON                   │ │
│  │    - Add metadata                  │ │
│  └────────────────────────────────────┘ │
│               ↓                         │
│  ┌────────────────────────────────────┐ │
│  │ 10. Logging Middleware             │ │
│  │     - Log response                 │ │
│  │     - Record metrics               │ │
│  └────────────────────────────────────┘ │
└─────────────────────────────────────────┘
       │ HTTP Response
       ↓
┌─────────────┐
│   Browser   │
│ - Parse JSON│
│ - Update UI │
└─────────────┘
```

---

## Security Features

### 1. Input Validation (Guardrails)

**What it blocks**:
- Password queries
- SSN requests
- API key extraction
- Credit card data
- Bank account info
- Private keys
- Salary information
- Personal contact details
- Bulk data extraction
- Prompt injection attempts
- Jailbreak techniques

**How it works**:
```python
# Before processing any query:
guardrail = get_guardrail()
result = guardrail.analyze_prompt(user_query)

if not result.allowed:
    return {"error": result.reason}

# Continue processing...
```

### 2. Output Redaction

**What it redacts**:
- API keys: `sk_live_xxxxx` → `[REDACTED_API_KEY]`
- AWS keys: `AKIAXXXXXXXX` → `[REDACTED_AWS_KEY]`
- Secrets: Long base64 strings → `[REDACTED_POTENTIAL_SECRET]`
- Private keys: PEM format → `[REDACTED_PRIVATE_KEY]`
- SSH keys: `ssh-rsa...` → `[REDACTED_SSH_KEY]`
- Credit cards: `4532-1234-5678-9010` → `[REDACTED_CREDIT_CARD]`
- SSN: `123-45-6789` → `[REDACTED_SSN]`
- JWT tokens: `eyJhbG...` → `[REDACTED_JWT]`

### 3. Authorization

**User Isolation**:
- Each document tagged with `user_id`
- Queries filtered by user
- Cross-user access prevented
- Entity-based multi-tenancy

**JWT Support** (optional):
```python
# In .env:
JWT_SECRET=your-secret-key

# In requests:
Authorization: Bearer <jwt-token>
```

### 4. Attack Prevention

**SQL Injection**: Prevented by using ORMs and parameterized queries
**XSS**: Input sanitization, output encoding
**CSRF**: CORS configuration
**DoS**: Rate limiting ready (can add middleware)
**Path Traversal**: Input validation on file paths

---

## Testing & Quality Assurance

### Promptfoo Integration

**8 Test Configurations**:

1. **promptfoo.evaluation.yaml** - Basic regression tests
2. **promptfoo.multi-endpoint.yaml** - All endpoints
3. **promptfoo.guardrails-llm.yaml** - Guardrail effectiveness
4. **promptfoo.performance.yaml** - Latency and cost
5. **promptfoo.dataset-driven.yaml** - Data-driven testing
6. **promptfoo.compare.yaml** - A/B comparison
7. **promptfoo.redteam.yaml** - Security focused
8. **promptfoo.redteam-comprehensive.yaml** - Full scan

**Running Tests**:
```bash
# Install Promptfoo
npm install -g promptfoo

# Set environment
export PROMPTFOO_RAG_BASE_URL=http://localhost:8000

# Run tests
npm run test:baseline          # Quick check
npm run test:security          # Security tests
npm run test:all              # Everything
```

**What it tests**:
- Response accuracy
- Guardrail effectiveness
- Performance metrics
- Security vulnerabilities
- OWASP compliance
- NIST AI RMF
- MITRE ATLAS coverage

---

## Summary

This RAG application provides a complete solution for document-based question answering with:

✅ **Modern Architecture**: FastAPI, async operations, type safety
✅ **Multiple AI Models**: Azure, Google, extensible design
✅ **Flexible Storage**: PostgreSQL or MongoDB
✅ **8+ Embedding Providers**: Choose what works for you
✅ **Interactive UI**: Beautiful, responsive web interface
✅ **Enterprise Security**: Guardrails, authorization, redaction
✅ **Comprehensive Testing**: Promptfoo integration
✅ **Production-Ready**: Docker, logging, error handling
✅ **Well-Documented**: Clear code, extensive docs

The system is designed to be:
- **Easy to use**: Simple web interface
- **Easy to deploy**: Docker Compose
- **Easy to extend**: Modular architecture
- **Easy to secure**: Built-in guardrails
- **Easy to test**: Comprehensive test suite

For more details, see:
- [ARCHITECTURE.md](./ARCHITECTURE.md) - System design details
- [SETUP_GUIDE.md](./SETUP_GUIDE.md) - Installation instructions
- [API_DOCUMENTATION.md](./API_DOCUMENTATION.md) - Complete API reference
- [README.md](./README.md) - Quick start guide
