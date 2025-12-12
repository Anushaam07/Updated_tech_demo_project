# System Architecture Documentation

## Table of Contents
1. [Architecture Overview](#architecture-overview)
2. [System Components](#system-components)
3. [Technology Stack Details](#technology-stack-details)
4. [Database Schema](#database-schema)
5. [API Layer Architecture](#api-layer-architecture)
6. [Security Architecture](#security-architecture)
7. [Scalability Considerations](#scalability-considerations)
8. [Deployment Architecture](#deployment-architecture)

---

## Architecture Overview

### High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                           CLIENT LAYER                               │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │                     Web Browser (Client)                       │  │
│  │  ┌─────────────────┐  ┌──────────────────┐  ┌──────────────┐ │  │
│  │  │  index.html     │  │   style.css      │  │   app.js     │ │  │
│  │  │  (UI Structure) │  │   (Styling)      │  │   (Logic)    │ │  │
│  │  └─────────────────┘  └──────────────────┘  └──────────────┘ │  │
│  └───────────────────────────────────────────────────────────────┘  │
└────────────────────────────────┬────────────────────────────────────┘
                                 │ HTTP/HTTPS
                                 │ REST API
                                 ↓
┌─────────────────────────────────────────────────────────────────────┐
│                        APPLICATION LAYER                             │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │                    FastAPI Application                         │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌───────────────────┐   │  │
│  │  │  Middleware  │  │   Routes     │  │    Services       │   │  │
│  │  │  - CORS      │  │  - Document  │  │  - Guardrails     │   │  │
│  │  │  - Logging   │  │  - Chat      │  │  - Vector Store   │   │  │
│  │  │  - Security  │  │  - Health    │  │  - Database       │   │  │
│  │  └──────────────┘  └──────────────┘  └───────────────────┘   │  │
│  └───────────────────────────────────────────────────────────────┘  │
└────────┬──────────────────────────────────┬─────────────────────────┘
         │                                  │
         │ Embeddings                       │ Vector Operations
         │                                  │
         ↓                                  ↓
┌─────────────────────────┐    ┌──────────────────────────────────────┐
│   EXTERNAL AI LAYER     │    │        DATA LAYER                    │
│  ┌───────────────────┐  │    │  ┌────────────────────────────────┐ │
│  │ Embedding Models  │  │    │  │   Vector Database              │ │
│  │ - Azure OpenAI   │  │    │  │   ┌──────────────────────────┐ │ │
│  │ - Google Gemini  │  │    │  │   │ PostgreSQL + pgvector    │ │ │
│  │ - HuggingFace    │  │    │  │   │  OR                      │ │ │
│  │ - Ollama         │  │    │  │   │ MongoDB Atlas            │ │ │
│  │ - Bedrock        │  │    │  │   └──────────────────────────┘ │ │
│  │ - VertexAI       │  │    │  │                                │ │
│  └───────────────────┘  │    │  │   Stores:                      │ │
│                         │    │  │   - Document embeddings        │ │
│  ┌───────────────────┐  │    │  │   - Metadata                   │ │
│  │   Chat Models     │  │    │  │   - User associations          │ │
│  │ - GPT-4o-mini    │  │    │  └────────────────────────────────┘ │
│  │ - Gemini 1.5     │  │    └──────────────────────────────────────┘
│  └───────────────────┘  │
└─────────────────────────┘
```

### Request Flow for Document Upload

```
┌──────────┐
│  Client  │
└─────┬────┘
      │ 1. POST /embed (multipart/form-data)
      │    file: document.pdf
      │    file_id: "doc-123"
      ↓
┌─────────────────────────────────────┐
│  FastAPI Server                     │
│  ┌───────────────────────────────┐  │
│  │ Middleware Stack              │  │
│  │ - CORS validation             │  │
│  │ - Request logging             │  │
│  │ - Security checks             │  │
│  └───────────────────────────────┘  │
│              ↓                      │
│  ┌───────────────────────────────┐  │
│  │ document_routes.py            │  │
│  │ - Validate file               │  │
│  │ - Save temporarily            │  │
│  └───────────────────────────────┘  │
│              ↓                      │
│  ┌───────────────────────────────┐  │
│  │ document_loader.py            │  │
│  │ - Detect file type            │  │
│  │ - Extract text                │  │
│  │ - Clean content               │  │
│  └───────────────────────────────┘  │
│              ↓                      │
│  ┌───────────────────────────────┐  │
│  │ Text Splitter                 │  │
│  │ - Chunk into 1500 chars       │  │
│  │ - Overlap 100 chars           │  │
│  └───────────────────────────────┘  │
│              ↓                      │
└──────────────┬──────────────────────┘
               │ 2. For each chunk
               │    embed(chunk_text)
               ↓
┌─────────────────────────────────────┐
│  Embedding Provider API             │
│  (Azure/OpenAI/Gemini/etc.)        │
│                                     │
│  chunk_text → [1536-dim vector]    │
└─────────────────┬───────────────────┘
                  │ 3. Return embeddings
                  ↓
┌─────────────────────────────────────┐
│  FastAPI Server                     │
│  ┌───────────────────────────────┐  │
│  │ Vector Store Service          │  │
│  │ - Prepare documents           │  │
│  │ - Add metadata                │  │
│  └───────────────────────────────┘  │
│              ↓                      │
└──────────────┬──────────────────────┘
               │ 4. INSERT INTO database
               │    embedding + metadata
               ↓
┌─────────────────────────────────────┐
│  Vector Database                    │
│  (PostgreSQL/MongoDB)               │
│                                     │
│  Store:                             │
│  - embedding: vector(1536)          │
│  - content: text                    │
│  - metadata: json {                 │
│      file_id, user_id, page, etc.   │
│    }                                │
└─────────────────┬───────────────────┘
                  │ 5. Success response
                  ↓
┌─────────────────────────────────────┐
│  Client                             │
│  Display: "Document uploaded!"      │
└─────────────────────────────────────┘
```

### Request Flow for Question Answering

```
┌──────────┐
│  Client  │
└─────┬────┘
      │ 1. POST /chat
      │    {
      │      "query": "What is RAG?",
      │      "file_id": "doc-123",
      │      "model": "azure-gpt4o-mini",
      │      "k": 4
      │    }
      ↓
┌─────────────────────────────────────────────────────────────┐
│  FastAPI Server                                             │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ Middleware + Validation                               │  │
│  └───────────────────────────────────────────────────────┘  │
│              ↓                                              │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ Guardrails Service                                    │  │
│  │ INPUT VALIDATION                                      │  │
│  │ ┌───────────────────────────────────────────────────┐ │  │
│  │ │ Check query for sensitive keywords:               │ │  │
│  │ │ - "password", "ssn", "api key", etc.             │ │  │
│  │ │                                                   │ │  │
│  │ │ Pattern matching:                                 │ │  │
│  │ │ - Prompt injection attempts                       │ │  │
│  │ │ - Data exfiltration patterns                      │ │  │
│  │ │ - Jailbreak attempts                              │ │  │
│  │ │                                                   │ │  │
│  │ │ Decision:                                         │ │  │
│  │ │ ✓ ALLOW - Continue processing                     │ │  │
│  │ │ ✗ BLOCK - Return error to client                  │ │  │
│  │ └───────────────────────────────────────────────────┘ │  │
│  └───────────────────────────────────────────────────────┘  │
│              ↓ (if allowed)                                 │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ Generate Query Embedding                              │  │
│  │ - Check cache first                                   │  │
│  │ - If miss: call embedding API                         │  │
│  └───────────────────────────────────────────────────────┘  │
│              ↓                                              │
└──────────────┬──────────────────────────────────────────────┘
               │ 2. embed("What is RAG?")
               ↓
┌─────────────────────────────────────┐
│  Embedding Provider                 │
│  Return: [0.123, -0.456, ...]      │
└─────────────────┬───────────────────┘
                  │ 3. Query vector
                  ↓
┌─────────────────────────────────────────────────────────────┐
│  Vector Database                                            │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ Vector Similarity Search                              │  │
│  │                                                       │  │
│  │ SELECT content, metadata,                             │  │
│  │        embedding <=> query_vector AS distance         │  │
│  │ FROM langchain_pg_embedding                           │  │
│  │ WHERE metadata->>'file_id' = 'doc-123'               │  │
│  │   AND metadata->>'user_id' = 'user-456'              │  │
│  │ ORDER BY distance ASC                                 │  │
│  │ LIMIT 4;                                              │  │
│  │                                                       │  │
│  │ Returns top 4 most similar chunks:                    │  │
│  │ 1. "RAG stands for Retrieval..." (score: 0.89)       │  │
│  │ 2. "The RAG system combines..." (score: 0.85)        │  │
│  │ 3. "Benefits of RAG include..." (score: 0.82)        │  │
│  │ 4. "RAG architecture consists..." (score: 0.78)      │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────┬───────────────────────────────────────────┘
                  │ 4. Return chunks
                  ↓
┌─────────────────────────────────────────────────────────────┐
│  FastAPI Server                                             │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ Build LLM Prompt                                      │  │
│  │                                                       │  │
│  │ System: "Answer based only on the context..."        │  │
│  │                                                       │  │
│  │ Context:                                              │  │
│  │ 1. RAG stands for Retrieval...                       │  │
│  │ 2. The RAG system combines...                        │  │
│  │ 3. Benefits of RAG include...                        │  │
│  │ 4. RAG architecture consists...                      │  │
│  │                                                       │  │
│  │ Question: What is RAG?                                │  │
│  └───────────────────────────────────────────────────────┘  │
│              ↓                                              │
└──────────────┬──────────────────────────────────────────────┘
               │ 5. Query LLM with prompt
               ↓
┌─────────────────────────────────────────────────────────────┐
│  AI Model (GPT-4o-mini or Gemini)                          │
│                                                             │
│  Process prompt and generate answer based on context        │
│                                                             │
│  Answer: "RAG stands for Retrieval-Augmented Generation.   │
│  It's a technique that combines document retrieval with     │
│  AI text generation to provide accurate, grounded answers." │
└─────────────────┬───────────────────────────────────────────┘
                  │ 6. Return generated answer
                  ↓
┌─────────────────────────────────────────────────────────────┐
│  FastAPI Server                                             │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ Guardrails Service                                    │  │
│  │ OUTPUT VALIDATION                                     │  │
│  │ ┌───────────────────────────────────────────────────┐ │  │
│  │ │ Redact sensitive patterns:                        │ │  │
│  │ │ - API keys: sk_live_xxx → [REDACTED_API_KEY]     │ │  │
│  │ │ - Secrets: secret=xxx → [REDACTED_SECRET]        │ │  │
│  │ │ - Credit cards: 4532-... → [REDACTED_CC]         │ │  │
│  │ │ - SSN: 123-45-6789 → [REDACTED_SSN]              │ │  │
│  │ │ - Private keys: -----BEGIN → [REDACTED_KEY]      │ │  │
│  │ └───────────────────────────────────────────────────┘ │  │
│  └───────────────────────────────────────────────────────┘  │
│              ↓                                              │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ Format Response                                       │  │
│  │ {                                                     │  │
│  │   "answer": "RAG stands for...",                      │  │
│  │   "sources": [                                        │  │
│  │     {"content": "...", "score": 0.89},               │  │
│  │     {"content": "...", "score": 0.85}                │  │
│  │   ],                                                  │  │
│  │   "model_used": "azure-gpt4o-mini"                   │  │
│  │ }                                                     │  │
│  └───────────────────────────────────────────────────────┘  │
│              ↓                                              │
└──────────────┬──────────────────────────────────────────────┘
               │ 7. JSON response
               ↓
┌─────────────────────────────────────────────────────────────┐
│  Client                                                     │
│  Display answer + sources in chat interface                 │
└─────────────────────────────────────────────────────────────┘
```

---

## System Components

### 1. Client Layer (Frontend)

**Location**: `static/`

#### Components:
- **index.html**: Single-page application structure
- **style.css**: Modern dark theme, responsive design
- **app.js**: All client-side logic

#### Features:
- Drag-and-drop file upload
- Real-time chat interface
- Document management (list, select, delete)
- Settings panel (model, temperature, k)
- Source citation display
- Error handling and user feedback

#### State Management:
```javascript
const state = {
    uploadedDocuments: [],      // List of uploaded files
    selectedDocumentId: null,   // Currently selected doc
    messages: [],               // Chat history
    settings: {
        model: 'azure-gpt4o-mini',
        temperature: 0.7,
        k: 4
    }
};
```

---

### 2. Application Layer (Backend)

**Location**: `app/`

#### Core Components:

##### 2.1 Main Application (`main.py`)
- FastAPI application instance
- Lifespan context manager
- Middleware registration
- Route inclusion
- Static file serving

**Key Features**:
```python
# Thread pool for CPU-bound tasks
max_workers = min(os.cpu_count(), 8)
thread_pool = ThreadPoolExecutor(max_workers)

# Async database connection pool
await PSQLDatabase.get_pool()

# Vector index creation
await ensure_vector_indexes()
```

##### 2.2 Configuration (`app/config.py`)
- Environment variable management
- Embedding provider initialization
- Vector store factory
- Logging configuration
- Database connection strings

**Configuration Flow**:
```
Environment Variables (.env)
         ↓
config.py reads and validates
         ↓
Initialize services:
 - Embeddings
 - Vector Store
 - Database Connections
 - Logging
```

##### 2.3 Models (`app/models.py`)
Pydantic models for type safety and validation:
- `ChatRequest` - Chat API input
- `ChatResponse` - Chat API output
- `QueryRequestBody` - Vector search input
- `DocumentResponse` - Document retrieval output
- `StoreDocument` - Document storage metadata

##### 2.4 Middleware (`app/middleware.py`)
- **Security Middleware**: JWT validation, request sanitization
- **CORS Middleware**: Cross-origin request handling
- **Logging Middleware**: Request/response logging

##### 2.5 Routes Layer (`app/routes/`)

**Document Routes** (`document_routes.py`):
- `POST /embed` - Upload and embed document
- `POST /query` - Vector similarity search
- `GET /documents` - Retrieve documents
- `DELETE /documents` - Delete documents
- `POST /text` - Extract text only
- `GET /ids` - List all document IDs
- `GET /health` - Health check

**Chat Routes** (`chat_routes_with_external_guardrails.py`):
- `POST /chat` - Main chat endpoint (protected)
- Guardrail integration
- LLM query handling
- Response formatting

**Unsafe Chat Routes** (`chat_unsafe_routes.py`):
- `POST /chat-unsafe` - Demo endpoint WITHOUT guardrails
- For comparison and testing

**Guardrails Routes** (`guardrails_routes.py`):
- `POST /guardrails/validate` - Test guardrail validation
- `GET /guardrails/policies` - List active policies
- Development and testing endpoints

##### 2.6 Services Layer (`app/services/`)

**Guardrails Service** (`guardrails.py`):
```python
class AdaptiveGuardrail:
    - policies: List[GuardrailPolicy]         # 15+ default policies
    - examples: List[GuardrailExample]        # Training examples
    - sensitive_keywords: List[str]           # 200+ keywords
    - sensitive_patterns: Dict[Pattern, str]  # Regex patterns

    def analyze_prompt(prompt: str) -> GuardrailResponse:
        # Validate input against policies
        # Return ALLOW or BLOCK decision

    def redact_sensitive_data(text: str) -> str:
        # Redact API keys, passwords, etc.
        # Return sanitized text
```

**Database Service** (`database.py`):
- PostgreSQL connection pool management
- Async query execution
- Connection lifecycle management

**Vector Store Factory** (`vector_store/factory.py`):
```python
def get_vector_store(connection_string, embeddings, collection_name, mode):
    if mode == "async":
        return AsyncPgVector(...)
    elif mode == "atlas-mongo":
        return AtlasMongoVector(...)
    else:
        return ExtendedPGVector(...)
```

**Vector Store Implementations**:
- `AsyncPgVector` - Async PostgreSQL operations
- `ExtendedPGVector` - Sync PostgreSQL operations
- `AtlasMongoVector` - MongoDB Atlas integration

##### 2.7 Utilities (`app/utils/`)

**Document Loader** (`document_loader.py`):
```python
def get_loader(filename, content_type, file_path):
    # Returns appropriate loader based on file type
    # Supports: PDF, DOCX, TXT, MD, CSV, XLSX, PPTX, etc.

def clean_text(text):
    # Remove null bytes, normalize whitespace
    # Handle encoding issues

def process_documents(docs):
    # Extract and format document chunks
```

**Health Check** (`health.py`):
```python
async def is_health_ok():
    # Check database connectivity
    # Check vector store availability
    # Return True/False
```

---

### 3. External AI Layer

#### Embedding Providers

**Supported Providers** (8 total):

1. **Azure OpenAI**
   - Model: text-embedding-3-small
   - Dimensions: 1536
   - Authentication: API key + endpoint

2. **OpenAI**
   - Model: text-embedding-3-small
   - Dimensions: 1536
   - Authentication: API key

3. **Google Gemini**
   - Model: gemini-embedding-001
   - Dimensions: 768
   - Authentication: API key

4. **HuggingFace (sentence-transformers)**
   - Model: all-MiniLM-L6-v2
   - Dimensions: 384
   - Local execution

5. **HuggingFace TEI**
   - Model: Configurable
   - Endpoint-based
   - Fast inference

6. **Ollama**
   - Model: nomic-embed-text
   - Local execution
   - Self-hosted

7. **AWS Bedrock**
   - Model: amazon.titan-embed-text-v1
   - Dimensions: 1536
   - AWS credentials required

8. **Google VertexAI**
   - Model: text-embedding-004
   - Service account required
   - GCP integration

#### Chat Models

1. **Azure OpenAI (GPT-4o-mini)**
   ```python
   ChatOpenAI(
       model="gpt-4o-mini",
       api_key=AZURE_CHAT_API_KEY,
       azure_endpoint=AZURE_CHAT_ENDPOINT,
       temperature=0.7
   )
   ```

2. **Google Gemini (gemini-1.5-flash)**
   ```python
   genai.GenerativeModel(
       model_name='gemini-1.5-flash',
       api_key=GEMINI_API_KEY
   )
   ```

---

### 4. Data Layer

#### PostgreSQL with pgvector

**Schema**:
```sql
CREATE TABLE langchain_pg_embedding (
    uuid UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    collection_id UUID,
    embedding VECTOR(1536),              -- Vector representation
    document TEXT,                        -- Original chunk text
    cmetadata JSONB,                      -- Metadata
    custom_id TEXT,                       -- file_id

    -- Indexes for performance
    -- GIN index for metadata filtering
    -- HNSW index for vector similarity
);

-- Metadata structure
{
    "file_id": "doc-123",
    "user_id": "user-456",
    "digest": "md5_hash",
    "source": "document.pdf",
    "page": 3
}
```

**Vector Operations**:
```sql
-- Similarity search (cosine distance)
SELECT document, cmetadata,
       embedding <=> query_vector AS distance
FROM langchain_pg_embedding
WHERE cmetadata->>'file_id' = 'doc-123'
  AND cmetadata->>'user_id' = 'user-456'
ORDER BY distance ASC
LIMIT 4;

-- Distance operators:
-- <=>  cosine distance
-- <->  L2 distance
-- <#>  inner product
```

#### MongoDB Atlas (Alternative)

**Collection Structure**:
```json
{
    "_id": ObjectId("..."),
    "embedding": [0.123, -0.456, ...],    // Vector array
    "text": "Document chunk content",
    "metadata": {
        "file_id": "doc-123",
        "user_id": "user-456",
        "source": "document.pdf",
        "page": 3
    }
}
```

**Vector Search Index**:
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
            "path": "metadata.file_id",
            "type": "filter"
        }
    ]
}
```

---

## Technology Stack Details

### Backend Technologies

#### FastAPI Framework
**Why FastAPI?**
- **Performance**: Async/await support, comparable to Node.js
- **Type Safety**: Pydantic integration for validation
- **Auto Documentation**: OpenAPI/Swagger generation
- **Modern Python**: Uses Python 3.7+ type hints
- **WebSocket Support**: For future real-time features

#### Langchain Framework
**Purpose**: LLM application orchestration
**Key Components Used**:
- `RecursiveCharacterTextSplitter` - Intelligent text chunking
- `VectorStore` - Abstract vector database interface
- `Embeddings` - Abstract embedding provider interface
- `ChatOpenAI` / `ChatGoogleGenerativeAI` - LLM interfaces

#### Database Technologies

**PostgreSQL + pgvector**:
- **ACID Compliance**: Reliable transactions
- **JSON Support**: Flexible metadata storage
- **Vector Extension**: Native vector operations
- **Performance**: HNSW indexing for fast search
- **Maturity**: Well-established, production-proven

**MongoDB Atlas**:
- **Cloud-Native**: Fully managed service
- **Flexible Schema**: Easy metadata evolution
- **Vector Search**: Built-in vector similarity
- **Scalability**: Horizontal scaling support

### Async Architecture

**Why Async?**
```python
# Synchronous (blocking)
def process_document(file):
    text = extract_text(file)    # Blocks thread
    embedding = get_embedding(text)  # Blocks thread
    store(embedding)              # Blocks thread

# Asynchronous (non-blocking)
async def process_document(file):
    text = await extract_text(file)    # Releases thread
    embedding = await get_embedding(text)  # Releases thread
    await store(embedding)        # Releases thread
```

**Benefits**:
- Handle 100s of concurrent requests
- Efficient I/O waiting (network, database)
- Better resource utilization
- Lower latency

**Thread Pool for CPU-Bound Tasks**:
```python
# Document parsing, embedding calculation
await run_in_executor(thread_pool, cpu_bound_task)
```

---

## Database Schema

### PostgreSQL pgvector Schema

**Table: langchain_pg_embedding**
```sql
CREATE TABLE langchain_pg_embedding (
    uuid UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    collection_id UUID,
    embedding VECTOR(1536),
    document TEXT,
    cmetadata JSONB,
    custom_id TEXT
);
```

**Indexes**:
```sql
-- GIN index for fast JSON queries
CREATE INDEX idx_cmetadata ON langchain_pg_embedding
USING GIN (cmetadata);

-- HNSW index for fast vector similarity
CREATE INDEX idx_embedding ON langchain_pg_embedding
USING hnsw (embedding vector_cosine_ops);

-- B-tree index for custom_id (file_id)
CREATE INDEX idx_custom_id ON langchain_pg_embedding (custom_id);
```

**Collection Management**:
```sql
CREATE TABLE langchain_pg_collection (
    uuid UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) UNIQUE,
    cmetadata JSONB
);
```

### MongoDB Schema

**Collection: embeddings** (or custom name)
```json
{
    "_id": "auto-generated",
    "embedding": [Array of 1536 floats],
    "text": "Document chunk text",
    "metadata": {
        "file_id": "string",
        "user_id": "string",
        "digest": "md5_hash",
        "source": "filename",
        "page": number,
        "chunk_index": number
    },
    "created_at": ISODate("...")
}
```

**Indexes**:
```javascript
// Vector search index (Atlas UI)
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
            },
            "metadata.user_id": {
                "type": "string"
            }
        }
    }
}
```

---

## API Layer Architecture

### API Design Principles

1. **RESTful**: Standard HTTP methods (GET, POST, DELETE)
2. **JSON**: All payloads in JSON format
3. **Stateless**: No server-side session management
4. **Versioned**: Ready for API versioning (v1, v2)
5. **Documented**: Auto-generated OpenAPI docs

### Endpoint Categories

**Document Management**:
- Upload, retrieve, delete documents
- Text extraction
- Document listing

**Query & Search**:
- Vector similarity search
- Multi-document search
- Context retrieval

**Chat & RAG**:
- Question answering
- Multi-turn conversations (frontend manages history)
- Model selection

**Administration**:
- Health checks
- Guardrail testing
- Policy management

### Error Handling

**HTTP Status Codes**:
```
200 OK - Successful operation
400 Bad Request - Invalid input
401 Unauthorized - Missing/invalid authentication
403 Forbidden - Insufficient permissions
404 Not Found - Resource doesn't exist
422 Unprocessable Entity - Validation error
500 Internal Server Error - Server-side error
503 Service Unavailable - Database/AI service down
```

**Error Response Format**:
```json
{
    "detail": "Error message",
    "status_code": 400,
    "type": "validation_error"
}
```

---

## Security Architecture

### Defense in Depth

```
┌─────────────────────────────────────────────────────────┐
│ Layer 1: Network Security                               │
│ - CORS policies                                         │
│ - Rate limiting (can be added)                          │
│ - HTTPS (in production)                                 │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ Layer 2: Authentication & Authorization                 │
│ - JWT token validation (optional)                       │
│ - User identification                                   │
│ - Entity-based multi-tenancy                            │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ Layer 3: Input Validation (Guardrails)                  │
│ - Sensitive query detection                             │
│ - Prompt injection prevention                           │
│ - Jailbreak attempt blocking                            │
│ - Policy enforcement                                    │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ Layer 4: Data Access Control                            │
│ - User isolation (user_id filtering)                    │
│ - Document ownership validation                         │
│ - Metadata-based filtering                              │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ Layer 5: Output Validation (Guardrails)                 │
│ - Sensitive data redaction                              │
│ - API key masking                                       │
│ - PII removal                                           │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ Layer 6: Audit & Monitoring                             │
│ - Request logging                                       │
│ - Error tracking                                        │
│ - Security event logging                                │
└─────────────────────────────────────────────────────────┘
```

### Guardrails Architecture

**Three-Stage Security**:

1. **Pre-Processing** (Input Validation)
   - Check query for sensitive keywords
   - Pattern matching for attacks
   - Policy evaluation
   - Risk assessment

2. **Processing** (Data Access Control)
   - User-based filtering
   - Document ownership checks
   - Authorized data retrieval only

3. **Post-Processing** (Output Sanitization)
   - Redact sensitive patterns
   - Remove leaked credentials
   - Validate response safety

---

## Scalability Considerations

### Horizontal Scaling

**Current Architecture**:
```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │
┌──────▼──────┐
│  FastAPI    │
│  Instance   │
└──────┬──────┘
       │
┌──────▼──────┐
│  Database   │
└─────────────┘
```

**Scaled Architecture**:
```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │
┌──────▼──────────────┐
│  Load Balancer      │
│  (nginx/AWS ALB)    │
└────┬────┬────┬──────┘
     │    │    │
┌────▼┐ ┌─▼───┐ ┌▼────┐
│App 1│ │App 2│ │App 3│
└────┬┘ └─┬───┘ └┬────┘
     │    │      │
     └────┴──┬───┘
           ┌─▼────────────┐
           │  Database    │
           │  (Replicated)│
           └──────────────┘
```

### Performance Optimizations

**1. Database Level**:
- Vector indexes (HNSW for approximate nearest neighbor)
- Connection pooling
- Query optimization
- Database replication (read replicas)

**2. Application Level**:
- Async I/O operations
- Thread pool for CPU tasks
- LRU caching for embeddings
- Response caching (Redis can be added)

**3. AI Model Level**:
- Batch embedding requests
- Model result caching
- Streaming responses (can be added)

### Bottleneck Analysis

**Potential Bottlenecks**:
1. **Embedding API calls** - Network latency, rate limits
   - Solution: Batch requests, local models (Ollama)

2. **Vector search** - Database query time
   - Solution: Better indexes, approximate search

3. **LLM API calls** - Response generation time
   - Solution: Streaming, faster models, caching

4. **Document processing** - CPU-bound parsing
   - Solution: Thread pool, distributed workers

---

## Deployment Architecture

### Docker Compose Deployment

**Components**:
```yaml
services:
  db:
    image: ankane/pgvector:latest
    # PostgreSQL with pgvector

  fastapi:
    build: .
    # Application server
    depends_on:
      - db
```

**Benefits**:
- Single command deployment
- Isolated environments
- Consistent across dev/prod
- Easy rollback

### Production Deployment Options

#### Option 1: Cloud VM (AWS EC2, Google Compute)
```
┌────────────────────────────────────────┐
│  VM Instance                           │
│  ┌──────────────────────────────────┐  │
│  │  Docker Compose                  │  │
│  │  - PostgreSQL container          │  │
│  │  - FastAPI container             │  │
│  │  - Nginx container (optional)    │  │
│  └──────────────────────────────────┘  │
└────────────────────────────────────────┘
```

#### Option 2: Kubernetes
```
┌────────────────────────────────────────┐
│  Kubernetes Cluster                    │
│  ┌──────────────────────────────────┐  │
│  │  Deployment: fastapi (3 replicas)│  │
│  └──────────────────────────────────┘  │
│  ┌──────────────────────────────────┐  │
│  │  StatefulSet: postgresql         │  │
│  └──────────────────────────────────┘  │
│  ┌──────────────────────────────────┐  │
│  │  Service: load balancer          │  │
│  └──────────────────────────────────┘  │
└────────────────────────────────────────┘
```

#### Option 3: Serverless (AWS Lambda, Cloud Run)
```
┌────────────────────────────────────────┐
│  Serverless Function                   │
│  - FastAPI app                         │
│  - Auto-scaling                        │
│  - Pay-per-request                     │
└───────────────┬────────────────────────┘
                │
┌───────────────▼────────────────────────┐
│  Managed Database                      │
│  - AWS RDS (PostgreSQL)                │
│  - Google Cloud SQL                    │
│  - MongoDB Atlas                       │
└────────────────────────────────────────┘
```

### Environment-Specific Configurations

**Development**:
```env
DEBUG_RAG_API=True
VECTOR_DB_TYPE=pgvector
DB_HOST=localhost
```

**Staging**:
```env
DEBUG_RAG_API=False
VECTOR_DB_TYPE=pgvector
DB_HOST=staging-db.internal
JWT_SECRET=staging-secret
```

**Production**:
```env
DEBUG_RAG_API=False
VECTOR_DB_TYPE=atlas-mongo
ATLAS_MONGO_DB_URI=mongodb+srv://...
JWT_SECRET=production-secret
CONSOLE_JSON=True  # Structured logging
```

---

## Summary

The RAG application architecture is designed with:

✅ **Modularity**: Clear separation of concerns
✅ **Scalability**: Async operations, connection pooling
✅ **Security**: Multi-layer defense, guardrails
✅ **Flexibility**: Multiple providers, databases
✅ **Reliability**: Error handling, health checks
✅ **Maintainability**: Type safety, logging, documentation
✅ **Performance**: Caching, indexing, optimization
✅ **Testability**: Comprehensive test coverage

The system can handle production workloads while remaining easy to understand, extend, and maintain.
