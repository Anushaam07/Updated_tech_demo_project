# API Documentation

## Table of Contents
1. [Overview](#overview)
2. [Authentication](#authentication)
3. [Document Management Endpoints](#document-management-endpoints)
4. [Query & Search Endpoints](#query--search-endpoints)
5. [Chat Endpoints](#chat-endpoints)
6. [Guardrails Endpoints](#guardrails-endpoints)
7. [Health & Status Endpoints](#health--status-endpoints)
8. [Error Handling](#error-handling)
9. [Rate Limiting](#rate-limiting)
10. [Examples](#examples)

---

## Overview

**Base URL**: `http://localhost:8000`

**API Documentation**: `http://localhost:8000/docs` (Swagger UI)

**Alternative Documentation**: `http://localhost:8000/redoc` (ReDoc)

### API Characteristics

- **Protocol**: HTTP/HTTPS
- **Format**: JSON (except file uploads which use multipart/form-data)
- **Methods**: GET, POST, DELETE
- **Authentication**: Optional JWT (configurable)
- **CORS**: Enabled for all origins (configurable)

---

## Authentication

### Optional JWT Authentication

If `JWT_SECRET` is configured in `.env`, all endpoints require authentication.

**Request Header**:
```
Authorization: Bearer <your-jwt-token>
```

**JWT Payload Example**:
```json
{
  "id": "user-123",
  "email": "user@example.com",
  "exp": 1234567890
}
```

**Note**: This implementation validates JWT tokens but does not issue them. You must obtain tokens from your authentication service.

---

## Document Management Endpoints

### 1. Upload and Embed Document

Upload a document and create embeddings for semantic search.

**Endpoint**: `POST /embed`

**Content-Type**: `multipart/form-data`

**Request Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| file | File | Yes | Document file to upload |
| file_id | string | Yes | Unique identifier for this document |
| entity_id | string | No | Entity/organization ID for multi-tenancy |

**Supported File Types**:
- PDF (`.pdf`)
- Word Documents (`.docx`)
- Text Files (`.txt`, `.md`)
- CSV (`.csv`)
- Excel (`.xlsx`)
- PowerPoint (`.pptx`)
- Source Code (`.py`, `.js`, `.java`, etc.)

**Request Example (cURL)**:
```bash
curl -X POST "http://localhost:8000/embed" \
  -F "file=@document.pdf" \
  -F "file_id=doc-2024-001"
```

**Request Example (JavaScript)**:
```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);
formData.append('file_id', 'doc-2024-001');

const response = await fetch('http://localhost:8000/embed', {
  method: 'POST',
  body: formData
});

const result = await response.json();
```

**Request Example (Python)**:
```python
import requests

with open('document.pdf', 'rb') as f:
    files = {'file': f}
    data = {'file_id': 'doc-2024-001'}
    response = requests.post(
        'http://localhost:8000/embed',
        files=files,
        data=data
    )

print(response.json())
```

**Response (200 OK)**:
```json
{
  "status": true,
  "message": "File processed successfully.",
  "file_id": "doc-2024-001",
  "filename": "document.pdf",
  "known_type": "pdf"
}
```

**Response (400 Bad Request)**:
```json
{
  "detail": "Error during file processing: Unsupported file type"
}
```

**What Happens**:
1. File is uploaded and saved temporarily
2. Text is extracted from the document
3. Text is split into chunks (default: 1500 chars with 100 char overlap)
4. Each chunk is converted to embeddings (1536-dimensional vectors)
5. Embeddings are stored in vector database with metadata
6. Temporary file is deleted

---

### 2. Extract Text Only

Extract text from a document without creating embeddings.

**Endpoint**: `POST /text`

**Content-Type**: `multipart/form-data`

**Request Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| file | File | Yes | Document file to extract text from |
| file_id | string | Yes | Identifier for tracking |
| entity_id | string | No | Entity/organization ID |

**Request Example**:
```bash
curl -X POST "http://localhost:8000/text" \
  -F "file=@document.pdf" \
  -F "file_id=doc-2024-001"
```

**Response (200 OK)**:
```json
{
  "text": "Full extracted text content from the document...",
  "file_id": "doc-2024-001",
  "filename": "document.pdf",
  "known_type": "pdf"
}
```

**Use Cases**:
- Preview document content before embedding
- Text extraction for other purposes
- Validate document readability

---

### 3. Get All Document IDs

Retrieve list of all document IDs in the system.

**Endpoint**: `GET /ids`

**Request Example**:
```bash
curl http://localhost:8000/ids
```

**Response (200 OK)**:
```json
[
  "doc-2024-001",
  "doc-2024-002",
  "report-q4-2023",
  "user-manual-v2"
]
```

**Note**: Returns unique document IDs. Does not include document content or metadata.

---

### 4. Get Documents by IDs

Retrieve document chunks by their IDs.

**Endpoint**: `GET /documents`

**Query Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| ids | string[] | Yes | Array of document IDs |

**Request Example**:
```bash
curl "http://localhost:8000/documents?ids=doc-2024-001&ids=doc-2024-002"
```

**Response (200 OK)**:
```json
[
  {
    "page_content": "This is the content of the first chunk...",
    "metadata": {
      "file_id": "doc-2024-001",
      "user_id": "user-123",
      "source": "document.pdf",
      "page": 1,
      "digest": "5d41402abc4b2a76b9719d911017c592"
    }
  },
  {
    "page_content": "This is the content of another chunk...",
    "metadata": {
      "file_id": "doc-2024-002",
      "user_id": "user-123",
      "source": "report.docx",
      "page": 3,
      "digest": "7d793037a0760186574b0282f2f435e7"
    }
  }
]
```

**Response (404 Not Found)**:
```json
{
  "detail": "One or more IDs not found"
}
```

---

### 5. Get Document Context

Retrieve all chunks for a single document formatted for LLM context.

**Endpoint**: `GET /documents/{id}/context`

**Path Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| id | string | Yes | Document ID |

**Request Example**:
```bash
curl http://localhost:8000/documents/doc-2024-001/context
```

**Response (200 OK)**:
```json
{
  "context": "Chunk 1 content...\n\nChunk 2 content...\n\nChunk 3 content...",
  "chunks_count": 3,
  "file_id": "doc-2024-001"
}
```

---

### 6. Delete Documents

Delete documents and their embeddings from the database.

**Endpoint**: `DELETE /documents`

**Content-Type**: `application/json`

**Request Body**:
```json
["doc-2024-001", "doc-2024-002"]
```

**Request Example**:
```bash
curl -X DELETE "http://localhost:8000/documents" \
  -H "Content-Type: application/json" \
  -d '["doc-2024-001", "doc-2024-002"]'
```

**Response (200 OK)**:
```json
{
  "message": "Documents for 2 files deleted successfully"
}
```

**Response (404 Not Found)**:
```json
{
  "detail": "One or more IDs not found"
}
```

**What Gets Deleted**:
- All document chunks
- All embeddings
- All metadata
- NOTE: Original uploaded files are already deleted after processing

---

## Query & Search Endpoints

### 7. Vector Similarity Search

Search for relevant document chunks using semantic similarity.

**Endpoint**: `POST /query`

**Content-Type**: `application/json`

**Request Body**:
```json
{
  "query": "What are the main findings?",
  "file_id": "doc-2024-001",
  "k": 4,
  "entity_id": "org-456"
}
```

**Request Parameters**:
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| query | string | Yes | - | Search query text |
| file_id | string | Yes | - | Document to search within |
| k | integer | No | 4 | Number of results to return |
| entity_id | string | No | null | Entity ID for multi-tenancy |

**Request Example**:
```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is machine learning?",
    "file_id": "doc-2024-001",
    "k": 4
  }'
```

**Response (200 OK)**:
```json
[
  [
    {
      "page_content": "Machine learning is a subset of artificial intelligence...",
      "metadata": {
        "file_id": "doc-2024-001",
        "user_id": "user-123",
        "source": "ai-textbook.pdf",
        "page": 15
      }
    },
    0.8756  // Similarity score (0-1, higher = more relevant)
  ],
  [
    {
      "page_content": "ML algorithms learn from data patterns...",
      "metadata": {
        "file_id": "doc-2024-001",
        "source": "ai-textbook.pdf",
        "page": 16
      }
    },
    0.8423
  ],
  [
    {
      "page_content": "Deep learning is a type of machine learning...",
      "metadata": {
        "file_id": "doc-2024-001",
        "source": "ai-textbook.pdf",
        "page": 42
      }
    },
    0.7991
  ],
  [
    {
      "page_content": "Neural networks are fundamental to ML...",
      "metadata": {
        "file_id": "doc-2024-001",
        "source": "ai-textbook.pdf",
        "page": 43
      }
    },
    0.7654
  ]
]
```

**Response Format**:
Each result is a tuple: `[Document, SimilarityScore]`
- Document: Contains `page_content` and `metadata`
- SimilarityScore: Float between 0 and 1 (cosine similarity)

**Authorization**:
- Only returns documents owned by the authenticated user
- Or documents with matching `entity_id`

---

### 8. Query Multiple Documents

Search across multiple documents simultaneously.

**Endpoint**: `POST /query_multiple`

**Content-Type**: `application/json`

**Request Body**:
```json
{
  "query": "What are the main findings?",
  "file_ids": ["doc-2024-001", "doc-2024-002", "report-q4"],
  "k": 4
}
```

**Request Example**:
```bash
curl -X POST "http://localhost:8000/query_multiple" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are the key insights?",
    "file_ids": ["doc-2024-001", "doc-2024-002"],
    "k": 4
  }'
```

**Response**: Same format as `/query` but may include results from multiple documents.

---

## Chat Endpoints

### 9. Chat with Document (Protected)

Ask questions and get AI-generated answers based on document content. This endpoint includes security guardrails.

**Endpoint**: `POST /chat`

**Content-Type**: `application/json`

**Request Body**:
```json
{
  "query": "What are the main conclusions of this research?",
  "file_id": "doc-2024-001",
  "model": "azure-gpt4o-mini",
  "k": 4,
  "temperature": 0.7,
  "entity_id": "org-456"
}
```

**Request Parameters**:
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| query | string | Yes | - | Question to ask |
| file_id | string | Yes | - | Document to query |
| model | string | No | "azure-gpt4o-mini" | AI model to use |
| k | integer | No | 4 | Number of context chunks |
| temperature | float | No | 0.7 | AI creativity (0-1) |
| entity_id | string | No | null | Entity ID |

**Available Models**:
- `"azure-gpt4o-mini"` - Fast, cost-effective (default)
- `"gemini"` - Google Gemini 1.5 Flash

**Temperature Guide**:
- `0.0` - Deterministic, focused (best for factual questions)
- `0.3-0.5` - Slightly creative, consistent
- `0.7` - Balanced (default)
- `0.9-1.0` - Very creative, varied

**Request Example**:
```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is the main topic of this document?",
    "file_id": "doc-2024-001",
    "model": "azure-gpt4o-mini",
    "k": 4,
    "temperature": 0.5
  }'
```

**Response (200 OK)**:
```json
{
  "answer": "The main topic of this document is Retrieval-Augmented Generation (RAG), which is an AI technique that combines document retrieval with language model generation to provide accurate, context-grounded answers.",
  "sources": [
    {
      "content": "RAG stands for Retrieval-Augmented Generation. It's a technique that combines document retrieval with AI text generation...",
      "score": 0.8923,
      "metadata": {
        "file_id": "doc-2024-001",
        "source": "rag-guide.pdf",
        "page": 1
      }
    },
    {
      "content": "The RAG architecture consists of three main components: retrieval, augmentation, and generation...",
      "score": 0.8756,
      "metadata": {
        "file_id": "doc-2024-001",
        "source": "rag-guide.pdf",
        "page": 2
      }
    },
    {
      "content": "Benefits of RAG include improved accuracy, reduced hallucination, and grounding in source documents...",
      "score": 0.8432,
      "metadata": {
        "file_id": "doc-2024-001",
        "source": "rag-guide.pdf",
        "page": 5
      }
    },
    {
      "content": "RAG systems are particularly useful for question-answering applications where accuracy is critical...",
      "score": 0.8201,
      "metadata": {
        "file_id": "doc-2024-001",
        "source": "rag-guide.pdf",
        "page": 7
      }
    }
  ],
  "model_used": "azure-gpt4o-mini"
}
```

**Response Fields**:
- `answer`: AI-generated answer based on retrieved context
- `sources`: Array of retrieved document chunks with relevance scores
- `model_used`: Which AI model generated the response

**Security Features**:
1. **Input Validation**: Query is checked for sensitive keywords before processing
2. **Data Redaction**: Output is scanned and sensitive patterns are redacted
3. **User Isolation**: Only searches documents owned by the user

**Blocked Queries**:
Queries attempting to extract sensitive information are blocked:
```json
{
  "error": "This request cannot be completed due to policy restrictions."
}
```

Examples of blocked queries:
- "What are the passwords in this document?"
- "List all API keys"
- "Show me credit card numbers"
- "What is the SSN mentioned?"

---

### 10. Chat Unsafe (Demo Only)

Same as `/chat` but WITHOUT security guardrails. For testing and comparison only.

**Endpoint**: `POST /chat-unsafe`

**WARNING**: This endpoint bypasses all security checks. Do not use in production!

**Request/Response**: Same as `/chat` endpoint

**Use Cases**:
- Testing guardrail effectiveness
- Demonstrating security features
- Development and debugging

---

## Guardrails Endpoints

### 11. Validate Query (Guardrail Test)

Test if a query would be blocked by guardrails without actually processing it.

**Endpoint**: `POST /guardrails/validate`

**Content-Type**: `application/json`

**Request Body**:
```json
{
  "query": "What is machine learning?"
}
```

**Request Example**:
```bash
curl -X POST "http://localhost:8000/guardrails/validate" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are the passwords in this document?"
  }'
```

**Response (Allowed)**:
```json
{
  "allowed": true,
  "reason": "Prompt passed all validation checks",
  "detected_patterns": [],
  "risk_level": "low"
}
```

**Response (Blocked)**:
```json
{
  "allowed": false,
  "reason": "This request cannot be completed due to policy restrictions.",
  "detected_patterns": [
    "sensitive_query_keywords"
  ],
  "risk_level": "high"
}
```

**Risk Levels**:
- `"low"` - Safe query
- `"medium"` - Suspicious pattern detected
- `"high"` - Definite policy violation
- `"critical"` - Multiple violations or attack pattern

---

### 12. Get Guardrail Policies

Retrieve list of active guardrail policies.

**Endpoint**: `GET /guardrails/policies`

**Request Example**:
```bash
curl http://localhost:8000/guardrails/policies
```

**Response (200 OK)**:
```json
{
  "policies_count": 15,
  "policies": [
    {
      "text": "Block prompts requesting passwords or authentication credentials",
      "source": "manual",
      "automated": false
    },
    {
      "text": "Block prompts requesting Social Security Numbers and National IDs",
      "source": "manual",
      "automated": false
    },
    {
      "text": "Block prompts requesting API keys, tokens, secrets, and cloud credentials",
      "source": "manual",
      "automated": false
    }
  ]
}
```

---

## Health & Status Endpoints

### 13. Health Check

Check if the service is running and healthy.

**Endpoint**: `GET /health`

**Request Example**:
```bash
curl http://localhost:8000/health
```

**Response (200 OK)**:
```json
{
  "status": "UP"
}
```

**Response (503 Service Unavailable)**:
```json
{
  "status": "DOWN",
  "error": "Database connection failed"
}
```

**What's Checked**:
- Database connectivity
- Vector store availability
- Basic service health

**Use Cases**:
- Load balancer health checks
- Monitoring systems
- Deployment validation

---

### 14. Root Endpoint

Serves the web interface.

**Endpoint**: `GET /`

**Response**: HTML page (chatbot interface)

**Access**: Open `http://localhost:8000` in a browser

---

### 15. API Documentation

Interactive API documentation.

**Endpoints**:
- `GET /docs` - Swagger UI
- `GET /redoc` - ReDoc documentation
- `GET /openapi.json` - OpenAPI schema

---

## Error Handling

### Standard Error Response Format

```json
{
  "detail": "Error message describing what went wrong",
  "status_code": 400
}
```

### HTTP Status Codes

| Code | Meaning | When It Happens |
|------|---------|-----------------|
| 200 | OK | Request successful |
| 400 | Bad Request | Invalid input, validation error |
| 401 | Unauthorized | Missing or invalid authentication |
| 403 | Forbidden | Not authorized to access resource |
| 404 | Not Found | Resource doesn't exist |
| 422 | Unprocessable Entity | Request validation failed |
| 500 | Internal Server Error | Server-side error |
| 503 | Service Unavailable | Database or AI service down |

### Common Error Scenarios

#### 1. Invalid File Type
```json
{
  "detail": "Error during file processing: Unsupported file type"
}
```

#### 2. Document Not Found
```json
{
  "detail": "One or more IDs not found"
}
```

#### 3. Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "query"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

#### 4. Guardrail Block
```json
{
  "error": "This request cannot be completed due to policy restrictions."
}
```

#### 5. Database Error
```json
{
  "detail": "Database connection failed"
}
```

#### 6. AI Service Error
```json
{
  "detail": "Failed to generate response: API timeout"
}
```

---

## Rate Limiting

Currently, rate limiting is not enforced by default. To add rate limiting:

### Option 1: Application Level (slowapi)

```python
# In main.py
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/chat")
@limiter.limit("10/minute")
async def chat_endpoint(...):
    ...
```

### Option 2: Reverse Proxy (nginx)

```nginx
limit_req_zone $binary_remote_addr zone=api:10m rate=10r/m;

location /chat {
    limit_req zone=api burst=5;
    proxy_pass http://localhost:8000;
}
```

---

## Examples

### Complete Workflow Example (Python)

```python
import requests
import time

BASE_URL = "http://localhost:8000"

# 1. Upload a document
def upload_document(file_path, file_id):
    with open(file_path, 'rb') as f:
        files = {'file': f}
        data = {'file_id': file_id}
        response = requests.post(
            f"{BASE_URL}/embed",
            files=files,
            data=data
        )
    return response.json()

# 2. Wait for processing (if async)
time.sleep(2)

# 3. Query the document
def query_document(query, file_id):
    response = requests.post(
        f"{BASE_URL}/query",
        json={
            "query": query,
            "file_id": file_id,
            "k": 4
        }
    )
    return response.json()

# 4. Chat with the document
def chat_with_document(question, file_id):
    response = requests.post(
        f"{BASE_URL}/chat",
        json={
            "query": question,
            "file_id": file_id,
            "model": "azure-gpt4o-mini",
            "k": 4,
            "temperature": 0.7
        }
    )
    return response.json()

# 5. Delete the document
def delete_document(file_id):
    response = requests.delete(
        f"{BASE_URL}/documents",
        json=[file_id]
    )
    return response.json()

# Usage
if __name__ == "__main__":
    # Upload
    result = upload_document("research_paper.pdf", "research-001")
    print("Upload:", result)

    # Query
    results = query_document("What is the methodology?", "research-001")
    print(f"\nFound {len(results)} relevant chunks")

    # Chat
    answer = chat_with_document("Summarize the key findings", "research-001")
    print("\nAnswer:", answer['answer'])
    print(f"\nBased on {len(answer['sources'])} sources")

    # Delete
    delete_result = delete_document("research-001")
    print("\nDelete:", delete_result)
```

### Complete Workflow Example (JavaScript)

```javascript
const BASE_URL = 'http://localhost:8000';

// 1. Upload document
async function uploadDocument(file, fileId) {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('file_id', fileId);

  const response = await fetch(`${BASE_URL}/embed`, {
    method: 'POST',
    body: formData
  });

  return await response.json();
}

// 2. Query document
async function queryDocument(query, fileId) {
  const response = await fetch(`${BASE_URL}/query`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      query: query,
      file_id: fileId,
      k: 4
    })
  });

  return await response.json();
}

// 3. Chat with document
async function chatWithDocument(question, fileId) {
  const response = await fetch(`${BASE_URL}/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      query: question,
      file_id: fileId,
      model: 'azure-gpt4o-mini',
      k: 4,
      temperature: 0.7
    })
  });

  return await response.json();
}

// 4. Delete document
async function deleteDocument(fileId) {
  const response = await fetch(`${BASE_URL}/documents`, {
    method: 'DELETE',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify([fileId])
  });

  return await response.json();
}

// Usage
async function main() {
  // Get file from input element
  const fileInput = document.getElementById('fileInput');
  const file = fileInput.files[0];

  // Upload
  const uploadResult = await uploadDocument(file, 'doc-001');
  console.log('Upload:', uploadResult);

  // Wait a bit for processing
  await new Promise(resolve => setTimeout(resolve, 2000));

  // Query
  const queryResults = await queryDocument('What is this about?', 'doc-001');
  console.log('Query results:', queryResults.length, 'chunks found');

  // Chat
  const chatResult = await chatWithDocument('Summarize the main points', 'doc-001');
  console.log('Answer:', chatResult.answer);
  console.log('Sources:', chatResult.sources.length);

  // Delete
  const deleteResult = await deleteDocument('doc-001');
  console.log('Delete:', deleteResult);
}
```

### Testing with Postman

**Collection Structure**:
1. Environment Variables:
   - `base_url`: `http://localhost:8000`
   - `file_id`: `test-doc-001`

2. Requests:
   - Upload Document (POST /embed)
   - Query Document (POST /query)
   - Chat (POST /chat)
   - Get Documents (GET /documents?ids={{file_id}})
   - Delete Document (DELETE /documents)

**Pre-request Scripts** (for UUID generation):
```javascript
pm.environment.set('file_id', 'doc-' + Date.now());
```

---

## Best Practices

### 1. File Upload
- Always use unique `file_id` for each document
- Keep file sizes reasonable (< 50MB recommended)
- Handle upload errors gracefully
- Show upload progress to users

### 2. Querying
- Start with `k=4`, adjust based on results quality
- Use specific questions for better results
- Cache frequent queries if possible
- Handle empty results gracefully

### 3. Chat
- Use `temperature=0.3` for factual questions
- Use `temperature=0.7` for creative questions
- Show sources to users for transparency
- Implement conversation history in your frontend

### 4. Security
- Validate file types before upload
- Sanitize user inputs
- Implement rate limiting in production
- Enable JWT authentication for production
- Monitor for abuse patterns

### 5. Error Handling
- Always check response status codes
- Display user-friendly error messages
- Log errors for debugging
- Implement retry logic for transient failures

---

## API Versioning

Currently at version 1 (implicit). Future versions will use URL prefixing:
- v1: `/api/v1/embed`
- v2: `/api/v2/embed`

---

## Support

For API support:
- Interactive docs: `http://localhost:8000/docs`
- ReDoc documentation: `http://localhost:8000/redoc`
- GitHub Issues: [project repository]
- API status: Check `/health` endpoint

---

**End of API Documentation** 🎉
