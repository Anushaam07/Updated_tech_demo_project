# 🤖 RAG Chatbot - Complete User Guide

## 📋 Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Quick Start](#quick-start)
4. [Detailed Setup](#detailed-setup)
5. [Using the Chatbot UI](#using-the-chatbot-ui)
6. [API Endpoints](#api-endpoints)
7. [Promptfoo Security & Testing](#promptfoo-security--testing)
8. [Configuration Guide](#configuration-guide)
9. [Troubleshooting](#troubleshooting)
10. [Advanced Usage](#advanced-usage)

---

## 🌟 Overview

This is a comprehensive RAG (Retrieval-Augmented Generation) application with:

- **Interactive Web UI** for document upload and chat
- **Multiple AI Models** (Azure GPT-4o-mini, Google Gemini)
- **Vector Search** with PostgreSQL pgvector or MongoDB Atlas
- **Security Testing** with Promptfoo (OWASP/NIST/MITRE compliance)
- **Multiple Embedding Providers** (Azure, OpenAI, Gemini, HuggingFace, etc.)

---

## ✨ Features

### 🎨 Interactive Chatbot UI
- Drag-and-drop document upload
- Real-time chat interface
- Document management
- Source citation in responses
- Model selection (Azure GPT-4o-mini or Gemini)
- Adjustable temperature and retrieval parameters

### 🔐 Security & Testing
- **Promptfoo Integration** with 8 test configurations
- **Red Team Testing** for security vulnerabilities
- **Quality Assurance** with custom graders
- **Performance Benchmarking**
- **CI/CD Ready** with GitHub Actions

### 📄 Supported Document Types
- PDF, DOCX, DOC
- TXT, MD, CSV
- XLSX, XLS, PPTX
- And more...

### 🤖 AI Models
- **Azure OpenAI GPT-4o-mini** - Fast and cost-effective
- **Google Gemini Pro** - Alternative model option

### 📊 Embedding Providers
- Azure OpenAI
- OpenAI
- Google Gemini
- HuggingFace
- Ollama
- AWS Bedrock
- Google VertexAI

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL with pgvector extension (or MongoDB Atlas)
- Azure OpenAI account OR Google Gemini API key
- Node.js 18+ (for Promptfoo testing)

### 1. Clone and Setup

```bash
# Clone repository
git clone <your-repo-url>
cd demo-rag-1-ansa

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
npm install  # For Promptfoo
```

### 2. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your credentials
nano .env  # or use your preferred editor
```

**Minimum required configuration:**

```env
# Vector Database
VECTOR_DB_TYPE=pgvector
POSTGRES_DB=rag_db
POSTGRES_USER=rag_user
POSTGRES_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

# Embeddings (Azure recommended)
EMBEDDINGS_PROVIDER=azure
EMBEDDINGS_MODEL=text-embedding-3-small
RAG_AZURE_OPENAI_API_KEY=your-azure-key
RAG_AZURE_OPENAI_ENDPOINT=https://ai-40mini.cognitiveservices.azure.com/
RAG_AZURE_OPENAI_API_VERSION=2024-02-01

# Chat Models
AZURE_CHAT_ENDPOINT=https://ai-40mini.cognitiveservices.azure.com/
AZURE_CHAT_API_KEY=your-azure-chat-key
GEMINI_API_KEY=your-gemini-key  # Optional
```

### 3. Start Database

**Using Docker:**
```bash
docker compose -f db-compose.yaml up -d
```

**Or connect to existing PostgreSQL:**
- Ensure pgvector extension is installed: `CREATE EXTENSION vector;`

### 4. Run the Application

```bash
# Start the RAG API
uvicorn main:app --host 0.0.0.0 --port 8000

# Or with hot reload for development
uvicorn main:app --reload
```

### 5. Access the Chatbot

Open your browser and navigate to:
```
http://localhost:8000
```

You should see the interactive chatbot interface! 🎉

---

## 📖 Detailed Setup

### Database Setup

#### Option 1: PostgreSQL with pgvector (Recommended)

**Using Docker:**
```bash
# Start PostgreSQL with pgvector
docker compose -f db-compose.yaml up -d

# Check if running
docker ps
```

**Manual Installation:**
```sql
-- Connect to PostgreSQL
psql -U postgres

-- Create database
CREATE DATABASE rag_db;

-- Connect to database
\c rag_db

-- Install pgvector extension
CREATE EXTENSION vector;

-- Create user
CREATE USER rag_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE rag_db TO rag_user;
```

#### Option 2: MongoDB Atlas

```env
VECTOR_DB_TYPE=atlas-mongo
ATLAS_MONGO_DB_URI=mongodb+srv://user:pass@cluster.mongodb.net/
COLLECTION_NAME=rag_collection
ATLAS_SEARCH_INDEX=vector_index
```

Create vector search index in MongoDB Atlas:
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

### API Keys Setup

#### Azure OpenAI

1. Go to [Azure Portal](https://portal.azure.com)
2. Create/select Azure OpenAI resource
3. Get API key and endpoint from "Keys and Endpoint"
4. Deploy models:
   - `text-embedding-3-small` for embeddings
   - `gpt-4o-mini` for chat

#### Google Gemini

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create API key
3. Add to `.env`: `GEMINI_API_KEY=your-key`

---

## 🎨 Using the Chatbot UI

### 1. Upload Documents

**Method 1: Drag and Drop**
- Drag files from your computer to the upload area
- Supported: PDF, DOCX, TXT, MD, CSV, XLSX, PPTX

**Method 2: Click to Upload**
- Click the upload area
- Select file from file picker

**What happens:**
- File is uploaded to server
- Document is split into chunks
- Chunks are embedded and stored in vector database
- Document appears in "Your Documents" list

### 2. Select Document

Click the checkmark icon (✓) next to any uploaded document to:
- Make it the active document for chat
- Enable the send button
- Show document name in chat input area

### 3. Ask Questions

**Simple Query:**
```
What is this document about?
```

**Specific Questions:**
```
What are the key findings in section 2?
How much did revenue increase?
List all the recommendations mentioned.
```

**Follow-up Questions:**
```
Can you explain that in more detail?
What else does it say about [topic]?
```

### 4. Adjust Settings

**Model Selection:**
- **Azure GPT-4o-mini**: Faster, cost-effective, good for most uses
- **Google Gemini**: Alternative model, different capabilities

**Results (k):** Number of document chunks to retrieve (1-10)
- Lower (2-3): Faster, more focused
- Higher (5-8): More comprehensive, may include irrelevant info

**Temperature:** Creativity of responses (0.0-1.0)
- 0.0: Deterministic, focused
- 0.7: Balanced (recommended)
- 1.0: Creative, diverse

### 5. View Sources

Each AI response includes:
- **Answer**: Generated response based on documents
- **Sources**: Actual document chunks used
- **Relevance Scores**: How relevant each source is

This allows you to:
- Verify the AI's answer
- See exact text from your document
- Understand which parts were used

### 6. Manage Documents

**Delete Document:**
- Click trash icon next to document
- Confirm deletion
- Document and embeddings are removed

**View All Documents:**
- Scroll through "Your Documents" list
- See upload date and file size

---

## 🔌 API Endpoints

### Upload & Embed Document

```bash
POST /embed
Content-Type: multipart/form-data

file: <file>
file_id: "unique-id"
entity_id: "user-id"  # optional
```

**Response:**
```json
{
  "status": true,
  "message": "File processed successfully",
  "file_id": "unique-id",
  "filename": "document.pdf",
  "known_type": "pdf"
}
```

### Query Documents (Vector Search)

```bash
POST /query
Content-Type: application/json

{
  "query": "What is this about?",
  "file_id": "unique-id",
  "k": 4,
  "entity_id": "user-id"  # optional
}
```

**Response:**
```json
[
  [
    {
      "page_content": "Document content...",
      "metadata": {
        "file_id": "unique-id",
        "user_id": "user-id",
        "digest": "abc123"
      }
    },
    0.85  // similarity score
  ]
]
```

### Chat with Documents (RAG)

```bash
POST /chat
Content-Type: application/json

{
  "query": "Explain the main findings",
  "file_id": "unique-id",
  "model": "azure-gpt4o-mini",  // or "gemini"
  "k": 4,
  "temperature": 0.7
}
```

**Response:**
```json
{
  "answer": "Based on the documents, the main findings are...",
  "sources": [
    {
      "content": "Source text...",
      "score": 0.89,
      "metadata": {...}
    }
  ],
  "model_used": "Azure GPT-4o-mini"
}
```

### List All Documents

```bash
GET /ids
```

**Response:**
```json
["file-id-1", "file-id-2", "file-id-3"]
```

### Delete Documents

```bash
DELETE /documents
Content-Type: application/json

["file-id-1", "file-id-2"]
```

**Response:**
```json
{
  "message": "Documents for 2 files deleted successfully"
}
```

### Health Check

```bash
GET /health
```

**Response:**
```json
{"status": "UP"}
```

---

## 🔒 Promptfoo Security & Testing

### Quick Start

```bash
# Install Promptfoo
npm install

# Set environment variables
export PROMPTFOO_RAG_BASE_URL="http://127.0.0.1:8000"
export OPENAI_API_KEY="sk-your-key"  # for LLM-graded tests

# Run baseline tests
npm run test:baseline

# View results in browser
npm run view
```

### Available Test Suites

| Command | Purpose | Duration | Cost |
|---------|---------|----------|------|
| `npm run test:baseline` | Quick regression tests | ~30s | $0.01 |
| `npm run test:multi-endpoint` | Test all endpoints | ~1min | $0.02 |
| `npm run test:guardrails` | Quality & policy checks | ~2min | $0.15 |
| `npm run test:performance` | Latency & concurrency | ~1min | $0.02 |
| `npm run test:dataset` | CSV-driven tests | ~2min | $0.20 |
| `npm run test:redteam` | Security scan (focused) | ~5min | $0.50 |
| `npm run test:redteam:full` | Comprehensive security | ~30min | $2.50 |
| `npm run test:all` | All eval tests | ~7min | $0.40 |
| `npm run test:nightly` | Complete suite | ~45min | $3.00 |

### Security Coverage

Promptfoo tests for:

**RAG-Specific:**
- Document exfiltration
- Vector poisoning
- Prompt extraction
- Embedding attacks

**OWASP Top 10:**
- Injection attacks (SQL, Shell, Prompt)
- Broken access control
- Security misconfiguration
- Sensitive data exposure

**Privacy:**
- PII leakage (direct, session, social engineering)
- Cross-tenant data isolation
- RBAC violations

**Network:**
- SSRF attacks
- Debug access exposure

For detailed Promptfoo guide, see [PROMPTFOO_REUSABLE_GUIDE.md](./PROMPTFOO_REUSABLE_GUIDE.md)

---

## ⚙️ Configuration Guide

### Embedding Providers

#### Azure OpenAI (Recommended)
```env
EMBEDDINGS_PROVIDER=azure
EMBEDDINGS_MODEL=text-embedding-3-small
RAG_AZURE_OPENAI_API_KEY=your-key
RAG_AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
RAG_AZURE_OPENAI_API_VERSION=2024-02-01
```

#### OpenAI
```env
EMBEDDINGS_PROVIDER=openai
EMBEDDINGS_MODEL=text-embedding-3-small
RAG_OPENAI_API_KEY=sk-your-key
```

#### Google Gemini
```env
EMBEDDINGS_PROVIDER=google_genai
EMBEDDINGS_MODEL=gemini-embedding-001
RAG_GOOGLE_API_KEY=your-key
```

#### HuggingFace (Local, Free)
```env
EMBEDDINGS_PROVIDER=huggingface
EMBEDDINGS_MODEL=sentence-transformers/all-MiniLM-L6-v2
```

#### Ollama (Local, Free)
```env
EMBEDDINGS_PROVIDER=ollama
EMBEDDINGS_MODEL=nomic-embed-text
OLLAMA_BASE_URL=http://localhost:11434
```

### Chat Models

#### Azure GPT-4o-mini
```env
AZURE_CHAT_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_CHAT_API_KEY=your-key
```

#### Google Gemini
```env
GEMINI_API_KEY=your-key
```

### Chunking Strategy

```env
CHUNK_SIZE=1500          # Characters per chunk
CHUNK_OVERLAP=100        # Overlap between chunks
```

**Guidelines:**
- **Small chunks (500-800)**: Better precision, more chunks
- **Medium chunks (1000-1500)**: Balanced (recommended)
- **Large chunks (2000-3000)**: More context, fewer chunks

**Overlap:**
- **Low (50-100)**: Less redundancy
- **Medium (100-200)**: Recommended
- **High (200-400)**: Maximum context retention

---

## 🔧 Troubleshooting

### Common Issues

#### 1. Database Connection Failed

**Error:** `Could not connect to database`

**Solutions:**
```bash
# Check if PostgreSQL is running
docker ps  # Should show database container

# Check connection string
echo $DB_HOST $DB_PORT

# Test connection
psql -h localhost -U rag_user -d rag_db
```

#### 2. Upload Fails

**Error:** `Failed to upload file`

**Checkcklist:**
- File size < 100MB
- File type is supported
- Upload directory exists and is writable
- Sufficient disk space

**Solution:**
```bash
# Create upload directory
mkdir -p uploads

# Check permissions
chmod 755 uploads
```

#### 3. Chat Returns No Response

**Error:** `No relevant documents found`

**Causes:**
- Document not selected
- File not uploaded properly
- Query too different from document content

**Solutions:**
- Ensure document is selected (green checkmark)
- Try rephrasing query
- Increase `k` value (5-8)
- Check if embeddings were created: `GET /ids`

#### 4. API Key Errors

**Error:** `Azure OpenAI error` or `Gemini API error`

**Solutions:**
```bash
# Verify API keys are set
echo $AZURE_CHAT_API_KEY
echo $GEMINI_API_KEY

# Check key validity in Azure Portal or Google AI Studio
# Ensure model deployments exist (Azure)
# Check API quota/billing
```

#### 5. Promptfoo Tests Fail

**Error:** `Provider not found`

**Solutions:**
```bash
# Ensure API is running
curl http://localhost:8000/health

# Check environment variables
echo $PROMPTFOO_RAG_BASE_URL

# Test provider manually
python promptfoo/providers/rag_http_target.py
```

### Performance Issues

#### Slow Queries

**Solutions:**
- Reduce `k` value (2-4)
- Use faster embedding model
- Enable pgvector indexes (automatic)
- Reduce chunk size

#### High Memory Usage

**Solutions:**
```env
# Reduce thread pool size
RAG_THREAD_POOL_SIZE=2

# Use smaller embedding model
EMBEDDINGS_MODEL=sentence-transformers/all-MiniLM-L6-v2
```

---

## 🚀 Advanced Usage

### Custom Prompts

Edit `app/routes/chat_routes.py` to customize system prompts:

```python
def create_chat_messages(query: str, context: str) -> List[dict]:
    system_prompt = """Your custom system prompt here.
    Be specific, be accurate, cite sources."""

    # ... rest of function
```

### Reranking for Better Accuracy

Add a reranking step in `chat_routes.py`:

```python
from sentence_transformers import CrossEncoder

reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

# After retrieving documents
scores = reranker.predict([(query, doc.page_content) for doc, _ in documents])
reranked = sorted(zip(documents, scores), key=lambda x: x[1], reverse=True)
```

### Hybrid Search

Combine vector search with keyword search for better results.

### Multi-Document Chat

Modify to query across multiple documents:

```python
POST /chat
{
  "query": "Compare findings across documents",
  "file_ids": ["doc1", "doc2", "doc3"],
  "model": "azure-gpt4o-mini"
}
```

### Authentication

Enable JWT authentication:

```env
JWT_SECRET=your-secret-key
```

Add JWT token to requests:
```bash
Authorization: Bearer your-jwt-token
```

---

## 📚 Additional Resources

- **Promptfoo Documentation**: [PROMPTFOO_IMPLEMENTATION_AUDIT.md](./PROMPTFOO_IMPLEMENTATION_AUDIT.md)
- **Reusable Integration Guide**: [PROMPTFOO_REUSABLE_GUIDE.md](./PROMPTFOO_REUSABLE_GUIDE.md)
- **API Documentation**: http://localhost:8000/docs (when running)
- **Promptfoo Official Docs**: https://www.promptfoo.dev/docs/

---

## 🎯 Best Practices

1. **Start Small**: Upload 1-2 documents first, test thoroughly
2. **Use Appropriate Models**: Azure GPT-4o-mini for most use cases
3. **Tune Parameters**: Adjust k, temperature, chunk size based on results
4. **Monitor Costs**: Use cheaper models for testing
5. **Regular Testing**: Run Promptfoo baseline tests before deployments
6. **Security First**: Run red team tests weekly
7. **Document Everything**: Keep notes on what works for your use case

---

## 💡 Tips for Better Results

**For Querying:**
- Be specific in questions
- Use terminology from the document
- Start with simple questions, then go deeper
- Check sources to verify answers

**For Document Preparation:**
- Use clear, well-structured documents
- Remove unnecessary formatting
- Ensure text is selectable (not scanned images)
- Break large documents into logical sections

**For Accuracy:**
- Increase `k` for comprehensive answers (6-8)
- Decrease temperature for factual queries (0.3-0.5)
- Use Azure GPT-4o-mini for best balance
- Review sources for accuracy

---

## 📞 Support

For issues or questions:
1. Check this guide first
2. Review error logs: `uvicorn main:app --log-level debug`
3. Test with Promptfoo: `npm run test:baseline`
4. Check API docs: http://localhost:8000/docs

---

**Ready to start? Follow the [Quick Start](#quick-start) guide above!** 🚀
