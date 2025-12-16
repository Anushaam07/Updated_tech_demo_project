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
