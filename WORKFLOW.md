# Complete Workflow Guide - RAG Application

This document provides a **detailed, step-by-step explanation** of how the RAG application works from start to finish. Perfect for beginners who want to understand every aspect of the system.

## Table of Contents
1. [System Startup](#1-system-startup)
2. [Document Upload Flow](#2-document-upload-flow)
3. [Chat Query Flow](#3-chat-query-flow)
4. [Vector Search Deep Dive](#4-vector-search-deep-dive)
5. [Guardrails System](#5-guardrails-system)
6. [Frontend-Backend Interaction](#6-frontend-backend-interaction)
7. [Database Operations](#7-database-operations)
8. [Error Handling](#8-error-handling)

---

## 1. System Startup

### What Happens When You Start the Application?

```
STEP 1: Load Environment Variables
    ↓
[main.py]
    ├─ Load .env file
    ├─ Read configuration (DB credentials, API keys, etc.)
    └─ Set up logging

STEP 2: Initialize Database Connection
    ↓
[app/services/database.py]
    ├─ Create PostgreSQL connection pool
    │  ├─ Host: DB_HOST (e.g., localhost)
    │  ├─ Port: DB_PORT (e.g., 5432)
    │  ├─ Database: POSTGRES_DB (e.g., rag_db)
    │  └─ User: POSTGRES_USER/POSTGRES_PASSWORD
    └─ Test connection with simple query

STEP 3: Initialize Vector Store
    ↓
[app/config.py] get_vector_store()
    ├─ Check VECTOR_DB_TYPE from environment
    │  ├─ IF "pgvector" → AsyncPgVector
    │  └─ IF "atlas-mongo" → AtlasMongoVector
    │
    ├─ Create vector store instance
    │  ├─ Connect to database
    │  ├─ Verify pgvector extension exists
    │  └─ Check/create collection table
    │
    └─ Return vector_store object

STEP 4: Initialize Embeddings
    ↓
[app/config.py] get_embeddings()
    ├─ Check EMBEDDINGS_PROVIDER
    │  ├─ IF "azure" → AzureOpenAIEmbeddings
    │  ├─ IF "openai" → OpenAIEmbeddings
    │  ├─ IF "huggingface" → HuggingFaceEmbeddings
    │  └─ etc.
    │
    ├─ Initialize with API keys/endpoints
    └─ Return embeddings object

STEP 5: Set Up API Routes
    ↓
[main.py]
    ├─ app = FastAPI()
    ├─ Include document_routes (POST /embed, GET /ids, etc.)
    ├─ Include chat_routes (POST /chat, POST /chat-unsafe)
    ├─ Include guardrails_routes (POST /guardrails/.../analyze)
    ├─ Mount static files (HTML/CSS/JS)
    └─ Add health check endpoint (GET /health)

STEP 6: Start Server
    ↓
[main.py]
    └─ uvicorn.run(app, host="0.0.0.0", port=8000)
       └─ Server listening on http://0.0.0.0:8000
          └─ Ready to accept requests!
```

**What You See:**
```bash
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

---

## 2. Document Upload Flow

### Step-by-Step: From UI Upload to Vector Storage

#### Phase 1: User Interaction (Frontend)

**Location:** `static/js/app.js` (lines 777+)

```
USER ACTION: Drag & drop file OR click upload button
    ↓
Event Listener: 'drop' or 'change' event
    ↓
uploadFile(file) function triggered
    │
    ├─ Validate file type
    │  └─ Check extension: .pdf, .docx, .txt, .csv, .xlsx, .pptx, .md
    │
    ├─ Generate file_id
    │  └─ Create unique ID: `doc_${Date.now()}_${Math.random()}`
    │
    ├─ Create FormData
    │  └─ formData.append('file', file)
    │  └─ formData.append('file_id', fileId)
    │  └─ formData.append('entity_id', currentUserId) // optional
    │
    ├─ Show upload progress
    │  └─ Display progress bar (0%)
    │  └─ Disable upload button
    │
    └─ Make HTTP Request
       └─ fetch('http://localhost:8000/embed', {
             method: 'POST',
             body: formData
          })
```

**What the User Sees:**
- File name appears
- Progress bar animates
- "Uploading..." message
- Green checkmark when done

#### Phase 2: Backend Receives Request

**Location:** `app/routes/document_routes.py` → `embed_file()`

```
BACKEND RECEIVES: POST /embed
    ↓
FastAPI Request Handler
    │
    ├─ Parse multipart/form-data
    │  ├─ Extract file: UploadFile object
    │  ├─ Extract file_id: string
    │  └─ Extract entity_id: string (optional)
    │
    ├─ Validate inputs
    │  ├─ Check file is not empty
    │  ├─ Check file_id is provided
    │  └─ Check file extension is supported
    │
    └─ Call save_upload_file_async()
```

#### Phase 3: Save File to Disk

**Location:** `app/routes/document_routes.py` → `save_upload_file_async()`

```
SAVE FILE TO DISK
    │
    ├─ Determine save path
    │  └─ path = ./uploads/{entity_id}/{filename}
    │     Example: ./uploads/user123/document.pdf
    │
    ├─ Create directory if not exists
    │  └─ os.makedirs(directory, exist_ok=True)
    │
    ├─ Write file in chunks (async)
    │  └─ async with aiofiles.open(path, 'wb') as f:
    │        while chunk := await upload_file.read(8192):
    │            await f.write(chunk)
    │
    └─ Return saved file path
```

**File System Structure:**
```
uploads/
└── user123/
    ├── document.pdf
    ├── report.docx
    └── data.csv
```

#### Phase 4: Load and Extract Text

**Location:** `app/routes/document_routes.py` → `load_file_content()`

```
LOAD FILE CONTENT
    │
    ├─ Determine file type
    │  └─ extension = Path(file_path).suffix
    │     Examples: .pdf, .docx, .txt
    │
    ├─ Get appropriate loader
    │  └─ loader = get_loader(file_path, extension)
    │     │
    │     ├─ IF .pdf → PyPDFLoader
    │     ├─ IF .docx → Docx2txtLoader
    │     ├─ IF .txt → TextLoader (with encoding detection)
    │     ├─ IF .csv → CSVLoader
    │     ├─ IF .xlsx → UnstructuredExcelLoader
    │     └─ IF .pptx → UnstructuredPowerPointLoader
    │
    ├─ Load document
    │  └─ documents = loader.load()
    │     └─ Returns: List[Document]
    │        Each Document has:
    │        ├─ page_content: "text content..."
    │        └─ metadata: {source, page, etc.}
    │
    └─ Extract text
       └─ Join all pages/sections into single text
```

**Example for PDF:**
```python
# Input: document.pdf (5 pages)
# Loader: PyPDFLoader
# Output: List of 5 Document objects
[
  Document(page_content="Page 1 text...", metadata={page: 0, source: "document.pdf"}),
  Document(page_content="Page 2 text...", metadata={page: 1, source: "document.pdf"}),
  ...
]
```

#### Phase 5: Split Text into Chunks

**Location:** `app/routes/document_routes.py` → `store_data_in_vector_db()`

```
TEXT CHUNKING
    │
    ├─ Initialize splitter
    │  └─ RecursiveCharacterTextSplitter(
    │        chunk_size=1500,      # Max characters per chunk
    │        chunk_overlap=100,    # Overlap between chunks
    │        separators=["\n\n", "\n", ".", "!", "?", " "]
    │     )
    │
    ├─ Split documents
    │  └─ chunks = text_splitter.split_documents(documents)
    │
    └─ Add metadata to each chunk
       └─ For each chunk:
          └─ chunk.metadata.update({
                'file_id': file_id,
                'entity_id': entity_id,
                'chunk_index': index,
                'total_chunks': len(chunks),
                'digest': hash(chunk.page_content)
             })
```

**Example:**
```
Original text: "This is a long document with multiple paragraphs..."
(3000 characters)
    ↓
Split into chunks:
    ↓
Chunk 1: [0:1500] "This is a long document with..."
    Overlap: [1400:1500]
Chunk 2: [1400:2900] "...multiple paragraphs that contain..."
    Overlap: [2800:2900]
Chunk 3: [2800:3000] "...important information."
```

**Why Overlap?**
- Prevents cutting sentences in half
- Maintains context across chunk boundaries
- Improves retrieval accuracy

#### Phase 6: Generate Embeddings

**Location:** `app/config.py` → `embeddings.embed_documents()`

```
GENERATE EMBEDDINGS
    │
    ├─ Prepare text chunks
    │  └─ texts = [chunk.page_content for chunk in chunks]
    │     Example: ["This is chunk 1...", "This is chunk 2...", ...]
    │
    ├─ Call embedding API
    │  │
    │  ├─ IF Azure OpenAI:
    │  │  └─ POST https://your-endpoint.openai.azure.com/embeddings
    │  │     Body: {
    │  │       input: texts,
    │  │       model: "text-embedding-3-small"
    │  │     }
    │  │     Response: {
    │  │       data: [
    │  │         {embedding: [0.123, -0.456, 0.789, ...]}, // 1536 numbers
    │  │         ...
    │  │       ]
    │  │     }
    │  │
    │  ├─ IF Google Gemini:
    │  │  └─ Call genai.embed_content()
    │  │
    │  └─ IF Ollama (local):
    │     └─ Call ollama.embeddings()
    │
    └─ Return embeddings
       └─ List of vectors: [[0.1, 0.2, ...], [0.3, 0.4, ...], ...]
          Each vector: 1536 dimensions (for text-embedding-3-small)
```

**What is an Embedding?**
```
Text: "The cat sat on the mat"
    ↓
Embedding API (neural network)
    ↓
Vector: [0.123, -0.456, 0.789, 0.234, ..., -0.987]
        (1536 numbers that capture the meaning)

Similar text: "A feline rested on the rug"
    ↓
Vector: [0.118, -0.442, 0.801, 0.229, ..., -0.991]
        (Very similar numbers = similar meaning)

Different text: "Quantum physics is complex"
    ↓
Vector: [-0.876, 0.234, -0.123, 0.987, ..., 0.456]
        (Very different numbers = different meaning)
```

#### Phase 7: Store in Vector Database

**Location:** `app/config.py` → `vector_store.add_documents()`

**For PostgreSQL + pgvector:**

```
STORE IN DATABASE
    │
    ├─ Prepare data for insertion
    │  └─ For each chunk + embedding:
    │     ├─ text = chunk.page_content
    │     ├─ embedding = chunk.embedding_vector
    │     └─ metadata = chunk.metadata (as JSONB)
    │
    ├─ Insert into PostgreSQL
    │  └─ INSERT INTO langchain_pg_embedding
    │        (uuid, collection_id, embedding, document, cmetadata)
    │     VALUES
    │        (gen_random_uuid(),
    │         '{collection_name}',
    │         '[0.123, -0.456, ...]',  -- vector type
    │         'This is chunk 1...',
    │         '{"file_id": "doc_123", "entity_id": "user123", ...}')
    │
    ├─ Create index (if not exists)
    │  └─ CREATE INDEX ON langchain_pg_embedding
    │     USING ivfflat (embedding vector_cosine_ops)
    │     WITH (lists = 100);
    │
    └─ Commit transaction
```

**Database Schema:**
```sql
Table: langchain_pg_embedding
┌──────────────┬──────────────┬─────────────────────────────────┐
│ uuid         │ VARCHAR      │ Unique ID for this chunk        │
│ collection_id│ VARCHAR      │ Collection name                  │
│ embedding    │ VECTOR(1536) │ 1536-dim embedding vector       │
│ document     │ TEXT         │ Actual text content             │
│ cmetadata    │ JSONB        │ {file_id, entity_id, ...}       │
│ custom_id    │ VARCHAR      │ file_id for filtering           │
└──────────────┴──────────────┴─────────────────────────────────┘
```

**Example Row:**
```
uuid: "550e8400-e29b-41d4-a716-446655440000"
collection_id: "testcollection"
embedding: [0.123, -0.456, 0.789, ..., -0.987]  (1536 numbers)
document: "This is the first chunk of the document..."
cmetadata: {
  "file_id": "doc_20250116_001",
  "entity_id": "user123",
  "chunk_index": 0,
  "total_chunks": 10,
  "source": "document.pdf",
  "page": 0
}
custom_id: "doc_20250116_001"
```

#### Phase 8: Return Response

```
RETURN TO FRONTEND
    │
    ├─ Create response object
    │  └─ {
    │       "status": "success",
    │       "message": "Document embedded successfully",
    │       "file_id": "doc_20250116_001",
    │       "filename": "document.pdf",
    │       "chunks_created": 10
    │     }
    │
    └─ HTTP 200 OK
       └─ Response sent to frontend
```

**Frontend Receives:**
```javascript
// Success response
{
  status: "success",
  file_id: "doc_20250116_001",
  filename: "document.pdf"
}
    ↓
Frontend updates:
    ├─ Hide progress bar
    ├─ Add document to list
    ├─ Auto-select document
    └─ Show success message
```

---

## 3. Chat Query Flow

### Step-by-Step: From User Question to AI Answer

#### Phase 1: User Types Question

**Location:** `static/js/app.js` → `sendMessage()`

```
USER TYPES: "What are the main findings in this document?"
    ↓
USER CLICKS: Send button (or presses Enter)
    ↓
sendMessage() function triggered
    │
    ├─ Validate inputs
    │  ├─ Check document is selected
    │  └─ Check query is not empty
    │
    ├─ Create request payload
    │  └─ {
    │       query: "What are the main findings in this document?",
    │       file_id: "doc_20250116_001",
    │       model: "azure-gpt4o-mini",  // from settings
    │       k: 4,                       // from settings
    │       temperature: 0.7,           // from settings
    │       entity_id: "user123"
    │     }
    │
    ├─ Update UI (optimistic)
    │  ├─ Add user message to chat
    │  ├─ Show typing indicator
    │  └─ Scroll to bottom
    │
    └─ Make HTTP Request
       └─ fetch('http://localhost:8000/chat', {
             method: 'POST',
             headers: {'Content-Type': 'application/json'},
             body: JSON.stringify(payload)
          })
```

#### Phase 2: Backend Receives Request

**Location:** `app/routes/chat_routes_with_external_guardrails.py` → `chat_with_documents()`

```
BACKEND RECEIVES: POST /chat
    ↓
FastAPI Request Handler
    │
    ├─ Parse JSON body
    │  └─ request: ChatRequest object
    │     ├─ query: str
    │     ├─ file_id: str
    │     ├─ model: str
    │     ├─ k: int (default 4)
    │     └─ temperature: float (default 0.7)
    │
    └─ Start processing
```

#### Phase 3: Guardrail Validation (Security Check)

**Location:** `app/services/guardrails.py` → `validate_with_guardrail()`

```
GUARDRAIL VALIDATION
    │
    ├─ Get guardrail instance
    │  └─ guardrail = get_guardrail(target_id)
    │     └─ AdaptiveGuardrail instance with policies
    │
    ├─ Analyze prompt
    │  └─ result = guardrail.analyze_prompt(query)
    │     │
    │     ├─ CHECK 1: Sensitive Data Patterns
    │     │  └─ Regex patterns for:
    │     │     ├─ Passwords: "password", "passwd", "pwd"
    │     │     ├─ API Keys: "api[_-]?key", "token"
    │     │     ├─ SSNs: "\d{3}-\d{2}-\d{4}"
    │     │     ├─ Credit Cards: "\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}"
    │     │     └─ Emails: "[a-z0-9]+@[a-z0-9]+\.[a-z]+"
    │     │
    │     ├─ CHECK 2: Prompt Injection
    │     │  └─ Patterns for:
    │     │     ├─ "Ignore previous instructions"
    │     │     ├─ "You are now in DAN mode"
    │     │     ├─ "Pretend you are..."
    │     │     └─ "Forget all your rules"
    │     │
    │     └─ CHECK 3: Custom Policies
    │        └─ User-defined regex rules
    │
    ├─ Calculate risk score
    │  └─ risk_level = "low" | "medium" | "high"
    │
    └─ Make decision
       │
       ├─ IF BLOCKED:
       │  └─ Return {
       │       allowed: false,
       │       reason: "Query contains sensitive data request",
       │       detected_patterns: ["password"],
       │       risk_level: "high"
       │     }
       │
       └─ IF ALLOWED:
          └─ Return {
                allowed: true,
                reason: "Query passed all security checks",
                risk_level: "low"
              }
```

**Example Blocked Query:**
```
Query: "What is the admin password in the document?"
    ↓
Guardrail detects: "password"
    ↓
Risk level: HIGH
    ↓
Decision: BLOCKED
    ↓
Response to user: "I cannot help with requests for passwords or credentials."
```

**Example Allowed Query:**
```
Query: "What are the main findings in this document?"
    ↓
Guardrail checks: No sensitive patterns detected
    ↓
Risk level: LOW
    ↓
Decision: ALLOWED
    ↓
Continue to next phase
```

#### Phase 4: Embed User Query

**Location:** `app/config.py` → `embeddings.embed_query()`

```
EMBED USER QUERY
    │
    ├─ Input query
    │  └─ "What are the main findings in this document?"
    │
    ├─ Call embedding API
    │  └─ Same API as document embedding
    │     BUT: embed_query() instead of embed_documents()
    │     (Single query vs. batch of documents)
    │
    └─ Get query vector
       └─ query_embedding = [0.234, -0.567, 0.890, ..., -0.123]
          (1536 dimensions, same space as document embeddings)
```

**Why Embed the Query?**
- To find documents with similar meaning
- Query and documents must be in the same vector space
- Cosine similarity works in vector space

#### Phase 5: Vector Similarity Search

**Location:** `app/services/vector_store/async_pg_vector.py` → `similarity_search_with_score()`

```
VECTOR SEARCH
    │
    ├─ Build SQL query
    │  └─ SELECT
    │       document,           -- Text content
    │       cmetadata,          -- Metadata (file_id, etc.)
    │       embedding,          -- Vector
    │       embedding <=> $1 AS distance  -- Cosine distance
    │     FROM langchain_pg_embedding
    │     WHERE
    │       cmetadata->>'file_id' = $2  -- Filter by file_id
    │     ORDER BY distance ASC  -- Most similar first
    │     LIMIT $3;              -- Top k results
    │
    │     Parameters:
    │     $1 = query_embedding (vector)
    │     $2 = file_id ("doc_20250116_001")
    │     $3 = k (4)
    │
    ├─ Execute query
    │  └─ Uses pgvector's <=> operator
    │     (Cosine distance: 0 = identical, 2 = opposite)
    │
    └─ Return results
       └─ [
            (Document("Main findings include..."), 0.15),  -- distance 0.15
            (Document("The study revealed..."), 0.23),     -- distance 0.23
            (Document("Key conclusions are..."), 0.31),     -- distance 0.31
            (Document("Further research..."), 0.42)        -- distance 0.42
          ]
```

**How Cosine Distance Works:**
```
Query Vector:    [0.2, 0.3, 0.5, ...]
Document Vector: [0.3, 0.4, 0.6, ...]
    ↓
Cosine Distance = 1 - (dot_product / (norm1 * norm2))
    ↓
Distance: 0.15 (very similar)
Score: 0.85 (1 - 0.15) → 85% relevance
```

**pgvector Index Types:**
- **IVFFlat**: Inverted file index (fast, approximate)
- **HNSW**: Hierarchical Navigable Small World (faster, more accurate)

#### Phase 6: Format Context for LLM

**Location:** `app/routes/chat_routes_with_external_guardrails.py` → `format_sources_for_context()`

```
FORMAT CONTEXT
    │
    ├─ Convert distance to similarity score
    │  └─ similarity = 1 - distance
    │     └─ [0.85, 0.77, 0.69, 0.58]  (higher = more relevant)
    │
    ├─ Format each source
    │  └─ For each (document, score):
    │     └─ "[Source {index}] (Relevance: {score:.2f})\n{content}\n\n"
    │
    └─ Create context string
       └─ """
          [Source 1] (Relevance: 0.85)
          Main findings include improved efficiency by 40% and reduced costs by 25%.

          [Source 2] (Relevance: 0.77)
          The study revealed significant correlation between training and performance.

          [Source 3] (Relevance: 0.69)
          Key conclusions are that early intervention improves outcomes substantially.

          [Source 4] (Relevance: 0.58)
          Further research is needed to validate these findings in larger populations.
          """
```

#### Phase 7: LLM Generation

**Location:** `app/routes/chat_routes_with_external_guardrails.py` → Model-specific sections

**For Azure GPT-4o-mini:**
```
LLM GENERATION
    │
    ├─ Create system prompt
    │  └─ """You are a helpful assistant that answers questions based on
    │       the provided context. Use only the information in the context
    │       to answer. If the answer is not in the context, say so.
    │       Always cite your sources using [Source X] notation."""
    │
    ├─ Create user prompt
    │  └─ """Context:
    │       {formatted_context}
    │
    │       Question: {user_query}
    │
    │       Answer based only on the context above:"""
    │
    ├─ Call Azure OpenAI API
    │  └─ response = client.chat.completions.create(
    │       model="gpt-4o-mini",
    │       messages=[
    │         {"role": "system", "content": system_prompt},
    │         {"role": "user", "content": user_prompt}
    │       ],
    │       temperature=0.7,    # User setting
    │       max_tokens=1000
    │     )
    │
    └─ Extract answer
       └─ answer = response.choices[0].message.content
```

**Example LLM Response:**
```
"Based on the provided context, the main findings include:

1. **Improved Efficiency**: The study showed a 40% improvement in efficiency [Source 1]
2. **Cost Reduction**: Costs were reduced by 25% [Source 1]
3. **Training Correlation**: There was a significant correlation between training and performance [Source 2]
4. **Early Intervention**: Early intervention substantially improves outcomes [Source 3]

The research also notes that further validation is needed in larger populations [Source 4]."
```

**For Google Gemini:**
```
LLM GENERATION (Gemini)
    │
    ├─ Initialize Gemini model
    │  └─ model = genai.GenerativeModel('gemini-2.0-flash-exp')
    │
    ├─ Create prompt (combine system + user)
    │  └─ full_prompt = f"{system_prompt}\n\n{user_prompt}"
    │
    ├─ Generate content
    │  └─ response = model.generate_content(
    │       full_prompt,
    │       generation_config=genai.GenerationConfig(
    │         temperature=0.7,
    │         max_output_tokens=1000
    │       )
    │     )
    │
    └─ Extract answer
       └─ answer = response.text
```

**For Ollama (Local):**
```
LLM GENERATION (Ollama)
    │
    ├─ Connect to Ollama server
    │  └─ client = ollama.Client(host=OLLAMA_HOST)
    │
    ├─ Generate response
    │  └─ response = client.generate(
    │       model='deepseek-r1:1.5b',
    │       prompt=full_prompt,
    │       options={
    │         'temperature': 0.7,
    │         'num_predict': 1000
    │       }
    │     )
    │
    └─ Extract answer
       └─ answer = response['response']
```

#### Phase 8: Return Response to Frontend

```
RETURN RESPONSE
    │
    ├─ Create response object
    │  └─ {
    │       "answer": "Based on the provided context, the main findings include..."
    │     }
    │
    │     (Simplified response - just answer text)
    │
    │     OR (if detailed mode):
    │
    │     {
    │       "answer": "Based on the provided context...",
    │       "sources": [
    │         {"content": "Main findings include...", "score": 0.85, "page": 1},
    │         {"content": "The study revealed...", "score": 0.77, "page": 2},
    │         ...
    │       ],
    │       "model_used": "azure-gpt4o-mini",
    │       "tokens_used": 450
    │     }
    │
    └─ HTTP 200 OK
       └─ Response sent to frontend
```

#### Phase 9: Frontend Displays Response

**Location:** `static/js/app.js` → Response handler

```
FRONTEND RECEIVES RESPONSE
    │
    ├─ Remove typing indicator
    │
    ├─ Create AI message object
    │  └─ {
    │       type: 'ai',
    │       text: response.answer,
    │       timestamp: new Date(),
    │       sources: response.sources || []
    │     }
    │
    ├─ Render message in chat
    │  └─ renderMessage(message)
    │     │
    │     ├─ Create message bubble (different color for AI)
    │     ├─ Format markdown (if any)
    │     ├─ Add source citations
    │     │  └─ For each source:
    │     │     └─ <div class="source">
    │     │          [Source {i}] (Relevance: {score})
    │     │          {content}
    │     │        </div>
    │     └─ Add timestamp
    │
    └─ Scroll chat to bottom
       └─ Smooth scroll animation
```

**What User Sees:**
```
┌────────────────────────────────────────────┐
│ User (just now)                            │
│ What are the main findings in this         │
│ document?                                  │
└────────────────────────────────────────────┘

┌────────────────────────────────────────────┐
│ AI Assistant (just now)                    │
│                                            │
│ Based on the provided context, the main    │
│ findings include:                          │
│                                            │
│ 1. **Improved Efficiency**: 40% improvement│
│    [Source 1]                              │
│ 2. **Cost Reduction**: 25% reduction       │
│    [Source 1]                              │
│ 3. **Training Correlation**: Significant   │
│    [Source 2]                              │
│                                            │
│ ━━━ Sources ━━━                           │
│ [Source 1] (Relevance: 0.85)              │
│ Main findings include improved...          │
│                                            │
│ [Source 2] (Relevance: 0.77)              │
│ The study revealed...                      │
└────────────────────────────────────────────┘
```

---

## 4. Vector Search Deep Dive

### How Does Vector Similarity Work?

#### Concept: From Text to Numbers

```
TRADITIONAL SEARCH (Keyword)
Query: "king"
    ↓
Find exact matches: "king"
    ↓
Misses: "monarch", "ruler", "sovereign"

VECTOR SEARCH (Semantic)
Query: "king"
    ↓
Convert to vector: [0.2, 0.3, 0.5, -0.1, ...]
    ↓
Find similar vectors:
    - "monarch" → [0.21, 0.29, 0.52, -0.09, ...]  ✓ Similar!
    - "ruler" → [0.19, 0.31, 0.48, -0.11, ...]    ✓ Similar!
    - "apple" → [-0.5, 0.1, -0.2, 0.8, ...]       ✗ Different!
```

#### Mathematical Explanation

**Cosine Similarity:**
```
Vector A: [a1, a2, a3, ..., a1536]
Vector B: [b1, b2, b3, ..., b1536]

Dot Product: A · B = (a1×b1) + (a2×b2) + ... + (a1536×b1536)
Magnitude A: ||A|| = √(a1² + a2² + ... + a1536²)
Magnitude B: ||B|| = √(b1² + b2² + ... + b1536²)

Cosine Similarity = (A · B) / (||A|| × ||B||)

Result ranges from -1 to 1:
  1.0  = Identical meaning
  0.5  = Somewhat similar
  0.0  = Unrelated
 -1.0  = Opposite meaning

pgvector uses cosine distance = 1 - cosine_similarity:
  0.0  = Identical
  0.5  = Somewhat different
  1.0  = Opposite
```

**Example Calculation:**
```
Query vector:    [0.5, 0.3, 0.2]
Document vector: [0.6, 0.4, 0.1]

Dot product: (0.5×0.6) + (0.3×0.4) + (0.2×0.1) = 0.3 + 0.12 + 0.02 = 0.44

||Query|| = √(0.5² + 0.3² + 0.2²) = √0.38 ≈ 0.616
||Doc||   = √(0.6² + 0.4² + 0.1²) = √0.53 ≈ 0.728

Cosine Similarity = 0.44 / (0.616 × 0.728) ≈ 0.981

Cosine Distance = 1 - 0.981 = 0.019 (very similar!)
```

#### pgvector Index Strategies

**1. IVFFlat (Inverted File Index)**
```
CREATE INDEX ON langchain_pg_embedding
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

How it works:
    ├─ Divide vectors into 100 clusters (lists)
    ├─ During search:
    │  ├─ Find closest cluster(s)
    │  └─ Search only within those clusters
    └─ Trade-off: Speed vs. accuracy (may miss some results)

Good for: Large datasets (>100k vectors), when speed > accuracy
```

**2. HNSW (Hierarchical Navigable Small World)**
```
CREATE INDEX ON langchain_pg_embedding
USING hnsw (embedding vector_cosine_ops);

How it works:
    ├─ Create graph of connections between vectors
    ├─ During search:
    │  ├─ Navigate graph from layer to layer
    │  └─ Follow nearest neighbors
    └─ Trade-off: More memory, but faster and more accurate

Good for: When accuracy is critical, faster than IVFFlat
```

---

## 5. Guardrails System

### Security Policies Explained

**Location:** `app/services/guardrails.py` → `AdaptiveGuardrail`

#### Built-in Policy Categories

**1. Sensitive Data Detection**
```python
SENSITIVE_PATTERNS = {
    'passwords': [
        r'\bpassword\b',
        r'\bpwd\b',
        r'\bpasswd\b',
        r'what.*password',
        r'show.*password'
    ],

    'api_keys': [
        r'api[_-]?key',
        r'access[_-]?token',
        r'secret[_-]?key',
        r'[A-Za-z0-9]{32,}'  # 32+ char strings (potential keys)
    ],

    'ssn': [
        r'\d{3}-\d{2}-\d{4}',  # 123-45-6789
        r'\d{3}\s\d{2}\s\d{4}', # 123 45 6789
        r'\b\d{9}\b'            # 123456789
    ],

    'credit_cards': [
        r'\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}',  # 4444-3333-2222-1111
        r'\b[45]\d{15}\b'  # Visa/Mastercard
    ],

    'emails': [
        r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    ],

    'phone_numbers': [
        r'\+?1?\s?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}',  # US format
        r'\+\d{1,3}\s?\d{4,14}'  # International
    ]
}
```

**2. Prompt Injection Detection**
```python
INJECTION_PATTERNS = [
    # Instruction Overrides
    r'ignore\s+(previous|prior|all)\s+instructions',
    r'forget\s+(everything|all|your\s+instructions)',
    r'disregard\s+(previous|prior|above)',

    # Role-play Attacks
    r'you\s+are\s+now\s+(?:a\s+)?(?:DAN|jailbreak)',
    r'pretend\s+(?:you\s+)?(?:are|to\s+be)',
    r'act\s+as\s+(?:if|a)',

    # Context Manipulation
    r'new\s+instructions',
    r'system\s+prompt',
    r'override\s+mode',

    # Data Exfiltration
    r'show\s+me\s+(?:all|the)\s+data',
    r'export\s+(?:all|the)',
    r'dump\s+(?:database|data)',

    # Testing/Probing
    r'test\s+mode',
    r'debug\s+mode',
    r'developer\s+mode'
]
```

**3. Policy Violation Checking**
```python
def analyze_prompt(self, prompt: str) -> GuardrailResult:
    """
    Analyze prompt for security violations
    """
    result = {
        'allowed': True,
        'reason': '',
        'detected_patterns': [],
        'risk_level': 'low'
    }

    # Check sensitive data patterns
    for category, patterns in SENSITIVE_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, prompt, re.IGNORECASE):
                result['allowed'] = False
                result['reason'] = f'Query contains {category}'
                result['detected_patterns'].append(category)
                result['risk_level'] = 'high'
                return result

    # Check prompt injection patterns
    for pattern in INJECTION_PATTERNS:
        if re.search(pattern, prompt, re.IGNORECASE):
            result['allowed'] = False
            result['reason'] = 'Potential prompt injection detected'
            result['detected_patterns'].append('injection')
            result['risk_level'] = 'critical'
            return result

    # Check custom policies
    for policy in self.custom_policies:
        if re.search(policy['pattern'], prompt, re.IGNORECASE):
            if policy['action'] == 'block':
                result['allowed'] = False
                result['reason'] = f"Policy violation: {policy['name']}"
                result['detected_patterns'].append(policy['name'])
                result['risk_level'] = policy['severity']
                return result

    return result
```

#### Custom Policy API

**Add Custom Policy:**
```bash
POST /guardrails/my-app/policies
Content-Type: application/json

{
  "name": "Block Crypto Queries",
  "pattern": "bitcoin|ethereum|crypto|blockchain",
  "action": "block",
  "severity": "medium",
  "description": "Block cryptocurrency-related queries"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Policy added successfully",
  "policy_id": "policy_001"
}
```

**Test Policy:**
```bash
POST /guardrails/my-app/analyze
Content-Type: application/json

{
  "prompt": "What is the Bitcoin price in this document?"
}
```

**Response:**
```json
{
  "allowed": false,
  "reason": "Policy violation: Block Crypto Queries",
  "detected_patterns": ["Block Crypto Queries"],
  "risk_level": "medium"
}
```

---

## 6. Frontend-Backend Interaction

### Complete Request/Response Cycle

#### Document Upload Request
```
FRONTEND                            BACKEND

uploadFile(file)
    ├─ Create FormData
    │  └─ file, file_id, entity_id
    │
    └─ fetch('/embed', {POST})     →  embed_file()
                                       ├─ Save file
                                       ├─ Load content
                                       ├─ Split chunks
                                       ├─ Generate embeddings
                                       └─ Store in DB
                                            ↓
    ← HTTP 200 OK                   ← Return metadata
       {
         status: "success",
         file_id: "doc_123",
         filename: "document.pdf",
         chunks_created: 10
       }
    │
    └─ Update UI
       ├─ Hide progress bar
       ├─ Add to document list
       └─ Show success message
```

#### Chat Request
```
FRONTEND                            BACKEND

sendMessage()
    ├─ Get user input
    ├─ Show typing indicator
    │
    └─ fetch('/chat', {POST})      →  chat_with_documents()
       {                               ├─ Guardrail validation
         query: "...",                 ├─ Embed query
         file_id: "doc_123",           ├─ Vector search
         model: "azure-gpt4o-mini",    ├─ Format context
         k: 4,                         └─ LLM generation
         temperature: 0.7                   ↓
       }
                                    ← HTTP 200 OK
    ← Response                       {
       {                               answer: "Based on...",
         answer: "Based on the..."     sources: [...]
       }                             }
    │
    └─ Display answer
       ├─ Remove typing indicator
       ├─ Add AI message
       └─ Show sources
```

#### Error Handling
```
FRONTEND                            BACKEND

Request                          →  Processing...
                                    ↓
                                    Error occurs!
                                    (e.g., API key invalid)
                                    ↓
    ← HTTP 500                   ← Return error
       {                           {
         detail: "Azure OpenAI      detail: "...",
         API key is invalid"        error_type: "APIError"
       }                           }
    │
    └─ Show error message
       └─ Display in chat:
          "Sorry, an error occurred.
           Please try again."
```

---

## 7. Database Operations

### PostgreSQL + pgvector Schema

**Tables:**
```sql
-- Main embedding storage
CREATE TABLE langchain_pg_embedding (
    uuid UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    collection_id VARCHAR(255),
    embedding VECTOR(1536),    -- pgvector type
    document TEXT,
    cmetadata JSONB,
    custom_id VARCHAR(255)
);

-- Indexes for performance
CREATE INDEX idx_collection_id
    ON langchain_pg_embedding(collection_id);

CREATE INDEX idx_custom_id
    ON langchain_pg_embedding(custom_id);

CREATE INDEX idx_file_id
    ON langchain_pg_embedding((cmetadata->>'file_id'));

CREATE INDEX idx_embedding_cosine
    ON langchain_pg_embedding
    USING ivfflat (embedding vector_cosine_ops)
    WITH (lists = 100);
```

**Common Queries:**

**1. Insert Document Chunk:**
```sql
INSERT INTO langchain_pg_embedding
    (collection_id, embedding, document, cmetadata, custom_id)
VALUES
    ('testcollection',
     '[0.123, -0.456, ...]',  -- 1536 floats
     'This is the document text...',
     '{"file_id": "doc_123", "entity_id": "user123", "page": 0}'::JSONB,
     'doc_123');
```

**2. Vector Similarity Search:**
```sql
SELECT
    document,
    cmetadata,
    embedding <=> $1 AS distance
FROM langchain_pg_embedding
WHERE
    cmetadata->>'file_id' = $2
ORDER BY distance ASC
LIMIT $3;

-- Parameters:
-- $1 = query_embedding (vector)
-- $2 = file_id
-- $3 = k (limit)
```

**3. Delete Document:**
```sql
DELETE FROM langchain_pg_embedding
WHERE cmetadata->>'file_id' = $1;

-- Parameter:
-- $1 = file_id
```

**4. Get All File IDs:**
```sql
SELECT DISTINCT cmetadata->>'file_id' AS file_id
FROM langchain_pg_embedding
WHERE cmetadata->>'entity_id' = $1;

-- Parameter:
-- $1 = entity_id (user ID)
```

### MongoDB Atlas Alternative

**Collection Schema:**
```javascript
{
  _id: ObjectId("..."),
  embedding: [0.123, -0.456, ...],  // 1536 floats
  text: "This is the document text...",
  metadata: {
    file_id: "doc_123",
    entity_id: "user123",
    page: 0,
    chunk_index: 0
  }
}
```

**Vector Search Index:**
```json
{
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
    }
  ]
}
```

**Vector Search Query:**
```javascript
db.collection.aggregate([
  {
    $search: {
      knnBeta: {
        vector: [0.123, -0.456, ...],  // query embedding
        path: "embedding",
        k: 4,
        filter: {
          "metadata.file_id": "doc_123"
        }
      }
    }
  },
  {
    $project: {
      text: 1,
      metadata: 1,
      score: { $meta: "searchScore" }
    }
  }
]);
```

---

## 8. Error Handling

### Common Errors and Responses

#### 1. File Upload Errors

**Error: File too large**
```
Request: POST /embed (file size: 100MB)
    ↓
Backend: Check file size
    ↓
Size > MAX_SIZE (50MB)
    ↓
Response: HTTP 413
{
  "detail": "File too large. Maximum size is 50MB."
}
    ↓
Frontend: Display error
    "File is too large. Please upload a file smaller than 50MB."
```

**Error: Unsupported file type**
```
Request: POST /embed (file: document.xyz)
    ↓
Backend: Check file extension
    ↓
Extension not in [.pdf, .docx, .txt, ...]
    ↓
Response: HTTP 400
{
  "detail": "Unsupported file type: .xyz. Supported types: pdf, docx, txt, csv, xlsx, pptx, md"
}
```

#### 2. Chat Errors

**Error: No document selected**
```
Request: POST /chat
{
  "query": "What is this about?",
  "file_id": null
}
    ↓
Backend: Validate file_id
    ↓
file_id is null
    ↓
Response: HTTP 400
{
  "detail": "file_id is required"
}
```

**Error: Document not found**
```
Request: POST /chat
{
  "query": "What is this about?",
  "file_id": "doc_nonexistent"
}
    ↓
Backend: Search vector store
    ↓
No results found for file_id
    ↓
Response: HTTP 404
{
  "detail": "No documents found with file_id: doc_nonexistent"
}
```

**Error: Guardrail blocked**
```
Request: POST /chat
{
  "query": "What is the admin password?"
}
    ↓
Backend: Guardrail validation
    ↓
Blocked: Contains "password"
    ↓
Response: HTTP 403
{
  "detail": "Query blocked by guardrails",
  "reason": "Query contains password request",
  "risk_level": "high"
}
```

#### 3. API Errors

**Error: Azure OpenAI API key invalid**
```
Backend: Call Azure OpenAI
    ↓
Azure API Response: 401 Unauthorized
    ↓
Response: HTTP 500
{
  "detail": "Azure OpenAI API authentication failed. Please check your API key."
}
```

**Error: Rate limit exceeded**
```
Backend: Call embedding API
    ↓
API Response: 429 Too Many Requests
    ↓
Backend: Retry with exponential backoff
    ├─ Wait 1 second → Retry
    ├─ Wait 2 seconds → Retry
    └─ Wait 4 seconds → Retry
        ↓
    If still failing:
        ↓
Response: HTTP 503
{
  "detail": "Service temporarily unavailable. Rate limit exceeded. Please try again later."
}
```

#### 4. Database Errors

**Error: Database connection failed**
```
Startup: Initialize database
    ↓
PostgreSQL connection refused
    ↓
Application fails to start
    ↓
Error message:
"Could not connect to database at localhost:5432.
Please ensure PostgreSQL is running."
```

**Error: pgvector extension not installed**
```
Startup: Check pgvector extension
    ↓
SELECT * FROM pg_extension WHERE extname = 'vector'
    ↓
No results
    ↓
Error message:
"pgvector extension not found. Please install it:
CREATE EXTENSION vector;"
```

---

## Summary

This workflow document has covered:

1. **System Startup**: How the application initializes all components
2. **Document Upload**: Complete flow from file upload to vector storage
3. **Chat Query**: Step-by-step processing of user questions
4. **Vector Search**: How semantic search works mathematically
5. **Guardrails**: Security policies and validation
6. **Frontend-Backend**: Communication patterns and data flow
7. **Database**: Schema, queries, and operations
8. **Error Handling**: Common errors and responses

**Key Takeaways:**

- **RAG** = Retrieval (vector search) + Augmented (add context) + Generation (LLM)
- **Embeddings** convert text to numbers that capture meaning
- **Vector search** finds similar meanings, not just keywords
- **Guardrails** protect against malicious inputs
- **Async operations** keep the system responsive

This system provides a production-ready foundation for building document-based AI applications with security and scalability built in.
