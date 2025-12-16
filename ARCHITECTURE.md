# Technical Architecture

Deep dive into the technical architecture, design patterns, and implementation details of the RAG application.

## Table of Contents

1. [System Architecture](#system-architecture)
2. [Technology Stack](#technology-stack)
3. [Design Patterns](#design-patterns)
4. [Data Flow Architecture](#data-flow-architecture)
5. [Database Design](#database-design)
6. [Security Architecture](#security-architecture)
7. [Performance Optimizations](#performance-optimizations)
8. [Scalability Considerations](#scalability-considerations)
9. [Deployment Architecture](#deployment-architecture)

---

## System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLIENT LAYER                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │   Browser    │  │  Mobile App  │  │  External Services   │  │
│  │  (Web UI)    │  │   (API)      │  │     (API Calls)      │  │
│  └──────────────┘  └──────────────┘  └──────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │ HTTP/HTTPS (REST API)
┌────────────────────────────▼────────────────────────────────────┐
│                   APPLICATION LAYER (FastAPI)                    │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              Middleware Stack                             │  │
│  │  ├─ CORS Handler                                          │  │
│  │  ├─ JWT Authentication (Optional)                         │  │
│  │  ├─ Rate Limiting                                         │  │
│  │  └─ Error Handler                                         │  │
│  └──────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                   API Routes                              │  │
│  │  ├─ Document Routes (/embed, /documents, /ids, /delete)  │  │
│  │  ├─ Query Routes (/query, /query-multiple)               │  │
│  │  ├─ Chat Routes (/chat, /chat-unsafe)                    │  │
│  │  └─ Guardrails Routes (/guardrails/...)                  │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────┐
│                      SERVICE LAYER                               │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────────┐  │
│  │   Document   │  │  Guardrails  │  │   Vector Store      │  │
│  │   Service    │  │   Service    │  │   Service           │  │
│  └──────────────┘  └──────────────┘  └─────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────┐
│                    INTEGRATION LAYER                             │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────────┐  │
│  │  Embeddings  │  │     LLM      │  │    File Loaders     │  │
│  │  (Azure/     │  │  (Azure/     │  │   (LangChain)       │  │
│  │   OpenAI)    │  │   Gemini)    │  │                     │  │
│  └──────────────┘  └──────────────┘  └─────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────┐
│                    PERSISTENCE LAYER                             │
│  ┌──────────────────┐  ┌─────────────────┐  ┌───────────────┐  │
│  │   PostgreSQL     │  │   File System   │  │   MongoDB     │  │
│  │  + pgvector      │  │   (Uploads)     │  │   (Optional)  │  │
│  │  (Vector DB)     │  │                 │  │               │  │
│  └──────────────────┘  └─────────────────┘  └───────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

### Component Responsibilities

**Client Layer**
- Renders UI
- Handles user interactions
- Makes API calls
- Displays results

**Application Layer (FastAPI)**
- Request routing
- Input validation
- Authentication/authorization
- Response formatting
- Error handling

**Service Layer**
- Business logic
- Document processing
- Security validation
- Data transformation

**Integration Layer**
- External API calls
- File format handling
- Vector operations
- LLM interactions

**Persistence Layer**
- Data storage
- Vector storage
- File storage
- Caching (future)

---

## Technology Stack

### Backend Framework

**FastAPI**
- **Why**: High performance, async support, automatic API docs
- **Features Used**:
  - Async endpoints for non-blocking I/O
  - Pydantic models for validation
  - Dependency injection
  - OpenAPI schema generation

**Example:**
```python
@app.post("/chat", response_model=SimpleChatResponse)
async def chat_with_documents(request: ChatRequest):
    # Async processing
    results = await vector_store.asimilarity_search(...)
    return {"answer": answer}
```

### Async Runtime

**Uvicorn**
- ASGI server
- Async event loop
- High concurrency support
- Low latency

**Configuration:**
```python
uvicorn.run(
    app,
    host="0.0.0.0",
    port=8000,
    workers=4,  # Multiple worker processes
    loop="uvloop"  # Fast async loop
)
```

### Vector Database

**PostgreSQL + pgvector**

**Advantages:**
- SQL interface (familiar to developers)
- ACID compliance
- JSON support (JSONB) for metadata
- Excellent tooling ecosystem
- Cost-effective

**pgvector Extension:**
- Native vector type: `VECTOR(1536)`
- Distance operators: `<->` (cosine), `<#>` (inner product)
- Indexing: IVFFlat, HNSW
- Efficient similarity search

**Schema:**
```sql
CREATE TABLE langchain_pg_embedding (
    uuid UUID PRIMARY KEY,
    collection_id VARCHAR(255),
    embedding VECTOR(1536),
    document TEXT,
    cmetadata JSONB,
    custom_id VARCHAR(255)
);
```

**Alternative: MongoDB Atlas**

**Advantages:**
- Cloud-native
- Horizontal scalability
- Flexible schema
- Built-in vector search

**When to Use:**
- Large-scale deployments (millions of vectors)
- Need horizontal scaling
- Already using MongoDB
- Cloud-first strategy

### Embeddings

**Multiple Providers Supported:**

1. **Azure OpenAI** (Recommended)
   - Model: text-embedding-3-small (1536 dim)
   - Latency: ~100-200ms
   - Cost: $0.00002 per 1K tokens
   - Enterprise SLA

2. **OpenAI**
   - Model: text-embedding-3-small/large
   - Latency: ~150-250ms
   - Cost: $0.00002 per 1K tokens

3. **HuggingFace (Local)**
   - Model: sentence-transformers/all-MiniLM-L6-v2
   - Latency: ~50-100ms (CPU), ~10-20ms (GPU)
   - Cost: Free (local compute)
   - Embedding dim: 384

4. **Ollama (Local)**
   - Model: nomic-embed-text
   - Latency: ~30-50ms
   - Cost: Free (local compute)
   - Privacy: No data leaves local network

**Factory Pattern:**
```python
def get_embeddings():
    provider = os.getenv("EMBEDDINGS_PROVIDER", "azure")

    if provider == "azure":
        return AzureOpenAIEmbeddings(...)
    elif provider == "openai":
        return OpenAIEmbeddings(...)
    elif provider == "huggingface":
        return HuggingFaceEmbeddings(...)
    # etc.
```

### LLM Models

**1. Azure GPT-4o-mini**
```python
client = AzureOpenAI(
    api_key=AZURE_CHAT_API_KEY,
    api_version="2024-02-15-preview",
    azure_endpoint=AZURE_CHAT_ENDPOINT
)

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[...],
    temperature=0.7
)
```

**Characteristics:**
- Fast (500-1000 tokens/sec)
- Cost-effective ($0.15/1M input tokens)
- Good reasoning
- 128K context window

**2. Google Gemini 2.0 Flash**
```python
model = genai.GenerativeModel('gemini-2.0-flash-exp')
response = model.generate_content(prompt)
```

**Characteristics:**
- Very fast (1000+ tokens/sec)
- Free tier available
- 1M context window
- Multimodal (future use)

**3. Ollama (DeepSeek R1)**
```python
client = ollama.Client(host=OLLAMA_HOST)
response = client.generate(
    model='deepseek-r1:1.5b',
    prompt=prompt
)
```

**Characteristics:**
- Local execution (privacy)
- No API costs
- Customizable
- Latency depends on hardware

---

## Design Patterns

### 1. Factory Pattern

**Used For:** Creating embeddings and vector store instances

**Implementation:**
```python
# app/config.py

def get_embeddings() -> Embeddings:
    """Factory for creating embedding instances"""
    provider = os.getenv("EMBEDDINGS_PROVIDER")

    if provider == "azure":
        return AzureOpenAIEmbeddings(...)
    elif provider == "openai":
        return OpenAIEmbeddings(...)
    # ... other providers

def get_vector_store() -> VectorStore:
    """Factory for creating vector store instances"""
    db_type = os.getenv("VECTOR_DB_TYPE")

    if db_type == "pgvector":
        return AsyncPgVector(...)
    elif db_type == "atlas-mongo":
        return AtlasMongoVector(...)
```

**Benefits:**
- Easy to add new providers
- Configuration-driven
- Decouples creation from usage

### 2. Strategy Pattern

**Used For:** Different guardrail policies

**Implementation:**
```python
# app/services/guardrails.py

class GuardrailPolicy(ABC):
    @abstractmethod
    def validate(self, prompt: str) -> GuardrailResult:
        pass

class SensitiveDataPolicy(GuardrailPolicy):
    def validate(self, prompt: str) -> GuardrailResult:
        # Check for passwords, API keys, etc.
        ...

class PromptInjectionPolicy(GuardrailPolicy):
    def validate(self, prompt: str) -> GuardrailResult:
        # Check for injection patterns
        ...

class AdaptiveGuardrail:
    def __init__(self):
        self.policies = [
            SensitiveDataPolicy(),
            PromptInjectionPolicy(),
            CustomPolicyHandler()
        ]

    def analyze_prompt(self, prompt: str) -> GuardrailResult:
        for policy in self.policies:
            result = policy.validate(prompt)
            if not result.allowed:
                return result
        return GuardrailResult(allowed=True)
```

**Benefits:**
- Easy to add new policies
- Each policy is independent
- Testable in isolation

### 3. Dependency Injection

**Used For:** Database connections, services

**Implementation:**
```python
# app/services/database.py

async def get_db_pool():
    """Dependency that provides database connection pool"""
    pool = await create_pool(...)
    try:
        yield pool
    finally:
        await pool.close()

# app/routes/document_routes.py

@app.post("/embed")
async def embed_file(
    file: UploadFile,
    db: asyncpg.Pool = Depends(get_db_pool)
):
    # Use db pool
    ...
```

**Benefits:**
- Loose coupling
- Easy testing (mock dependencies)
- Resource management

### 4. Repository Pattern

**Used For:** Data access abstraction

**Implementation:**
```python
# app/services/vector_store/async_pg_vector.py

class AsyncPgVector:
    """Repository for vector operations"""

    async def add_documents(self, documents: List[Document]):
        """Abstract INSERT operations"""
        ...

    async def similarity_search(self, query: str, k: int):
        """Abstract SELECT with vector search"""
        ...

    async def delete_by_file_id(self, file_id: str):
        """Abstract DELETE operations"""
        ...
```

**Benefits:**
- Database agnostic
- Easy to switch implementations
- Testable with mocks

### 5. Adapter Pattern

**Used For:** Different file formats

**Implementation:**
```python
# app/utils/document_loader.py

def get_loader(file_path: str, extension: str):
    """Adapter for different file formats"""

    if extension == ".pdf":
        return PyPDFLoader(file_path)
    elif extension == ".docx":
        return Docx2txtLoader(file_path)
    elif extension == ".txt":
        return TextLoader(file_path)
    # ... other formats
```

**Benefits:**
- Uniform interface
- Easy to add formats
- Hide format complexity

### 6. Async/Await Pattern

**Used For:** Non-blocking I/O operations

**Implementation:**
```python
@app.post("/chat")
async def chat_with_documents(request: ChatRequest):
    # Non-blocking database query
    results = await vector_store.asimilarity_search(...)

    # Non-blocking LLM call
    response = await llm_client.generate(...)

    return {"answer": response}
```

**Benefits:**
- High concurrency
- Better resource utilization
- Lower latency for concurrent requests

---

## Data Flow Architecture

### Document Upload Flow

```
User Upload
    ↓
[API Layer] FastAPI Endpoint
    ├─ Validate request (Pydantic)
    ├─ Check file size/type
    └─ Call service
        ↓
[Service Layer] Document Service
    ├─ Save file to disk (async I/O)
    ├─ Load document (file format adapter)
    ├─ Split into chunks (RecursiveCharacterTextSplitter)
    └─ Call embedding service
        ↓
[Integration Layer] Embeddings API
    ├─ Batch process chunks
    ├─ Call Azure/OpenAI API
    └─ Return vectors
        ↓
[Service Layer] Vector Store Service
    ├─ Format documents with metadata
    ├─ Insert into database (async batch)
    └─ Create indexes (if needed)
        ↓
[Persistence Layer] PostgreSQL
    ├─ Store vectors in pgvector table
    └─ Commit transaction
        ↓
[API Layer] Return response
    └─ {status: "success", file_id: "..."}
```

### Chat Query Flow

```
User Query
    ↓
[API Layer] FastAPI Endpoint
    ├─ Validate request (Pydantic)
    └─ Call guardrail service
        ↓
[Service Layer] Guardrail Service
    ├─ Check sensitive patterns
    ├─ Check injection patterns
    └─ Return validation result
        ↓
[Service Layer] Embeddings Service
    └─ Convert query to vector
        ↓
[Service Layer] Vector Store Service
    ├─ Execute similarity search
    ├─ Filter by file_id
    └─ Return top K results
        ↓
[Service Layer] Context Formatter
    └─ Format retrieved chunks
        ↓
[Integration Layer] LLM Service
    ├─ Create system + user prompt
    ├─ Call LLM API (Azure/Gemini/Ollama)
    └─ Stream or get full response
        ↓
[API Layer] Return response
    └─ {answer: "..."}
```

### Error Propagation

```
Database Error
    ↓
[Persistence Layer] Raises exception
    ↓
[Service Layer] Catches, logs, re-raises
    ↓
[API Layer] FastAPI error handler
    ├─ Log error with context
    ├─ Format error response
    └─ Return HTTP 500
        ↓
[Client] Receives error
    └─ Display user-friendly message
```

---

## Database Design

### PostgreSQL Schema

**Main Table:**
```sql
CREATE TABLE langchain_pg_embedding (
    uuid UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    collection_id VARCHAR(255) NOT NULL,
    embedding VECTOR(1536) NOT NULL,
    document TEXT NOT NULL,
    cmetadata JSONB NOT NULL DEFAULT '{}',
    custom_id VARCHAR(255)
);
```

**Indexes:**
```sql
-- Collection index
CREATE INDEX idx_collection_id
    ON langchain_pg_embedding(collection_id);

-- Custom ID index (file_id)
CREATE INDEX idx_custom_id
    ON langchain_pg_embedding(custom_id);

-- Metadata index (JSONB)
CREATE INDEX idx_file_id
    ON langchain_pg_embedding USING GIN ((cmetadata->>'file_id'));

CREATE INDEX idx_entity_id
    ON langchain_pg_embedding USING GIN ((cmetadata->>'entity_id'));

-- Vector index for similarity search
CREATE INDEX idx_embedding_cosine
    ON langchain_pg_embedding
    USING ivfflat (embedding vector_cosine_ops)
    WITH (lists = 100);

-- Alternative: HNSW index (faster, more memory)
CREATE INDEX idx_embedding_hnsw
    ON langchain_pg_embedding
    USING hnsw (embedding vector_cosine_ops);
```

**Connection Pooling:**
```python
# app/services/database.py

async def get_connection_pool():
    pool = await asyncpg.create_pool(
        host=DB_HOST,
        port=DB_PORT,
        database=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        min_size=5,     # Minimum connections
        max_size=20,    # Maximum connections
        command_timeout=60,
        server_settings={
            'jit': 'off',  # Disable JIT for vector operations
            'max_parallel_workers_per_gather': '4'
        }
    )
    return pool
```

### MongoDB Schema (Alternative)

**Collection:**
```javascript
{
  _id: ObjectId("..."),
  embedding: [0.123, -0.456, ...],  // 1536 floats
  text: "Document content",
  metadata: {
    file_id: "doc_123",
    entity_id: "user123",
    chunk_index: 0,
    source: "document.pdf",
    page: 0,
    upload_date: ISODate("2025-01-16T10:30:00Z")
  }
}
```

**Vector Search Index:**
```json
{
  "name": "vector_index",
  "type": "vectorSearch",
  "definition": {
    "fields": [
      {
        "type": "vector",
        "path": "embedding",
        "numDimensions": 1536,
        "similarity": "cosine"
      },
      {
        "type": "filter",
        "path": "metadata.file_id"
      },
      {
        "type": "filter",
        "path": "metadata.entity_id"
      }
    ]
  }
}
```

### Data Partitioning Strategy

**Partition by Entity (Multi-tenancy):**
```sql
-- PostgreSQL table partitioning
CREATE TABLE langchain_pg_embedding_user1
    PARTITION OF langchain_pg_embedding
    FOR VALUES IN ('user1');

CREATE TABLE langchain_pg_embedding_user2
    PARTITION OF langchain_pg_embedding
    FOR VALUES IN ('user2');
```

**Benefits:**
- Improved query performance
- Easier data management
- Data isolation

---

## Security Architecture

### Authentication Flow

```
User Request
    ↓
[Middleware] JWT Validator
    ├─ Extract token from header
    ├─ Verify signature (JWT_SECRET)
    ├─ Check expiration
    └─ Extract user claims
        ↓
    ├─ IF VALID:
    │   └─ Add user_id to request context
    │      └─ Continue to endpoint
    │
    └─ IF INVALID:
        └─ Return 401 Unauthorized
```

**Implementation:**
```python
# app/middleware.py

def verify_jwt(token: str) -> Dict:
    try:
        payload = jwt.decode(
            token,
            JWT_SECRET,
            algorithms=["HS256"]
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(401, "Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(401, "Invalid token")

@app.middleware("http")
async def jwt_middleware(request: Request, call_next):
    if request.url.path in ["/health", "/docs", "/"]:
        return await call_next(request)

    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    payload = verify_jwt(token)
    request.state.user = payload

    return await call_next(request)
```

### Guardrails Architecture

```
User Query
    ↓
[Guardrails Engine]
    │
    ├─ [Policy 1: Sensitive Data]
    │  ├─ Regex patterns
    │  ├─ Risk scoring
    │  └─ Decision: ALLOW/BLOCK
    │
    ├─ [Policy 2: Prompt Injection]
    │  ├─ Pattern matching
    │  ├─ Context analysis
    │  └─ Decision: ALLOW/BLOCK
    │
    └─ [Policy 3: Custom Rules]
       ├─ User-defined patterns
       └─ Decision: ALLOW/BLOCK
           ↓
    Aggregate Results
        ├─ IF ANY BLOCKED → Return 403
        └─ IF ALL ALLOWED → Continue
```

### Data Isolation

**Row-Level Security (Future):**
```sql
-- Enable RLS
ALTER TABLE langchain_pg_embedding ENABLE ROW LEVEL SECURITY;

-- Policy: Users can only see their own data
CREATE POLICY user_isolation ON langchain_pg_embedding
    FOR ALL
    USING (cmetadata->>'entity_id' = current_user);
```

**Application-Level Filtering:**
```python
# Always filter by entity_id
results = await vector_store.similarity_search(
    query=query,
    k=k,
    filter={"entity_id": user.entity_id}
)
```

---

## Performance Optimizations

### 1. Async Operations

**Database Queries:**
```python
# Bad: Blocking
results = vector_store.similarity_search(query)

# Good: Non-blocking
results = await vector_store.asimilarity_search(query)
```

**Concurrency:**
```python
# Sequential (slow)
for file_id in file_ids:
    results = await search(file_id)

# Concurrent (fast)
tasks = [search(file_id) for file_id in file_ids]
results = await asyncio.gather(*tasks)
```

### 2. Connection Pooling

```python
# Bad: New connection per request
conn = await asyncpg.connect(...)
result = await conn.fetch(...)
await conn.close()

# Good: Reuse pool
pool = await asyncpg.create_pool(...)
async with pool.acquire() as conn:
    result = await conn.fetch(...)
```

### 3. Batch Processing

**Embeddings:**
```python
# Bad: One at a time
embeddings = []
for text in texts:
    emb = embeddings_api.embed_query(text)
    embeddings.append(emb)

# Good: Batch
embeddings = embeddings_api.embed_documents(texts)  # Single API call
```

### 4. Caching (Future Enhancement)

**Query Cache:**
```python
from functools import lru_cache
import hashlib

@lru_cache(maxsize=1000)
def get_query_embedding(query: str):
    return embeddings.embed_query(query)
```

**Redis Cache:**
```python
import redis

redis_client = redis.Redis()

def get_or_compute(key, compute_fn):
    cached = redis_client.get(key)
    if cached:
        return cached

    result = compute_fn()
    redis_client.setex(key, 3600, result)  # 1 hour TTL
    return result
```

### 5. Index Optimization

**Vector Index Tuning:**
```sql
-- IVFFlat: Balance between speed and accuracy
CREATE INDEX idx_embedding
    ON langchain_pg_embedding
    USING ivfflat (embedding vector_cosine_ops)
    WITH (lists = FLOOR(SQRT(row_count)));

-- HNSW: Faster queries, more memory
CREATE INDEX idx_embedding
    ON langchain_pg_embedding
    USING hnsw (embedding vector_cosine_ops)
    WITH (m = 16, ef_construction = 64);
```

### 6. Query Optimization

**Use Covering Indexes:**
```sql
-- Index includes all needed columns
CREATE INDEX idx_covering
    ON langchain_pg_embedding (custom_id)
    INCLUDE (document, cmetadata);
```

**Limit Result Sets:**
```sql
-- Always use LIMIT
SELECT * FROM langchain_pg_embedding
    ORDER BY embedding <=> $1
    LIMIT 10;  -- Don't return all results
```

---

## Scalability Considerations

### Horizontal Scaling

**Load Balancer:**
```
            ┌─────────────┐
            │Load Balancer│
            └─────┬───────┘
                  │
        ┌─────────┼─────────┐
        │         │         │
    ┌───▼───┐ ┌──▼───┐ ┌──▼───┐
    │API 1  │ │API 2 │ │API 3 │
    └───┬───┘ └──┬───┘ └──┬───┘
        │        │        │
        └────────┼────────┘
                 │
        ┌────────▼─────────┐
        │  Database Pool   │
        └──────────────────┘
```

**Configuration:**
```yaml
# docker-compose.yaml
services:
  api:
    image: rag-api:latest
    replicas: 3
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 4G
```

### Database Scaling

**Read Replicas:**
```
┌──────────────┐
│   Primary    │ (Writes)
└──────┬───────┘
       │ Replication
    ┌──┴──┬──────┐
    │     │      │
┌───▼─┐ ┌─▼──┐ ┌─▼──┐
│Rep 1│ │Rep2│ │Rep3│ (Reads)
└─────┘ └────┘ └────┘
```

**Sharding (Future):**
```
User shard key (entity_id % 4):
    ├─ Shard 0: users 0, 4, 8, ...
    ├─ Shard 1: users 1, 5, 9, ...
    ├─ Shard 2: users 2, 6, 10, ...
    └─ Shard 3: users 3, 7, 11, ...
```

### Caching Strategy

**Multi-Layer Cache:**
```
Request
    ↓
[L1: Application Cache] (LRU, in-memory)
    ↓ Miss
[L2: Redis] (Distributed cache)
    ↓ Miss
[L3: Database] (Source of truth)
```

### Rate Limiting

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/chat")
@limiter.limit("100/hour")  # 100 requests per hour
async def chat(request: Request):
    ...
```

---

## Deployment Architecture

### Docker Compose

```yaml
version: '3.8'

services:
  # PostgreSQL with pgvector
  db:
    image: pgvector/pgvector:pg16
    environment:
      POSTGRES_DB: rag_db
      POSTGRES_USER: rag_user
      POSTGRES_PASSWORD: password
    volumes:
      - pgdata:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  # RAG API
  api:
    build: .
    depends_on:
      - db
    environment:
      DB_HOST: db
      POSTGRES_DB: rag_db
    ports:
      - "8000:8000"
    volumes:
      - ./uploads:/app/uploads

  # Ollama (optional)
  ollama:
    image: ollama/ollama:latest
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama

volumes:
  pgdata:
  ollama_data:
```

### Kubernetes Deployment

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: rag-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: rag-api
  template:
    metadata:
      labels:
        app: rag-api
    spec:
      containers:
      - name: api
        image: rag-api:latest
        ports:
        - containerPort: 8000
        env:
        - name: DB_HOST
          value: postgres-service
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: password
        resources:
          requests:
            memory: "2Gi"
            cpu: "1"
          limits:
            memory: "4Gi"
            cpu: "2"
---
apiVersion: v1
kind: Service
metadata:
  name: rag-api-service
spec:
  selector:
    app: rag-api
  ports:
  - port: 80
    targetPort: 8000
  type: LoadBalancer
```

### Cloud Deployment Options

**1. AWS:**
- **Compute**: ECS/EKS
- **Database**: RDS PostgreSQL + pgvector
- **Storage**: S3
- **Load Balancer**: ALB
- **Embeddings**: Bedrock

**2. Azure:**
- **Compute**: AKS/Container Apps
- **Database**: Azure Database for PostgreSQL
- **Storage**: Blob Storage
- **Load Balancer**: Application Gateway
- **Embeddings**: Azure OpenAI

**3. Google Cloud:**
- **Compute**: GKE/Cloud Run
- **Database**: Cloud SQL PostgreSQL
- **Storage**: Cloud Storage
- **Load Balancer**: Cloud Load Balancing
- **Embeddings**: Vertex AI

---

## Summary

This architecture provides:

**Modularity**: Clean separation of concerns
**Scalability**: Horizontal and vertical scaling options
**Flexibility**: Multiple providers, databases, models
**Performance**: Async operations, caching, pooling
**Security**: Authentication, guardrails, data isolation
**Maintainability**: Design patterns, dependency injection
**Observability**: Logging, monitoring, health checks

The system is production-ready and can scale from single-server deployments to multi-region cloud infrastructure.
