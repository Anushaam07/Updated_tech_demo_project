# app/routes/chat_routes_with_external_guardrails.py
"""
Clean Chat Routes with External Guardrails

This implementation follows Promptfoo's Adaptive Guardrails Architecture:
- Guardrails are applied EXTERNALLY via the guardrail service
- /chat endpoint is a NORMAL endpoint without embedded security logic
- Input validation happens BEFORE the request reaches this endpoint
"""

import os
from typing import List
from fastapi import APIRouter, Request, HTTPException, status
from openai import AzureOpenAI
import google.generativeai as genai
import ollama

from app.config import logger, vector_store
from app.models import ChatRequest, ChatResponse, SourceDocument, SimpleChatResponse
from app.services.vector_store.async_pg_vector import AsyncPgVector
from app.services.guardrails import get_guardrail

router = APIRouter()


# ----------------------- LLM Clients -----------------------
def get_azure_client():
    """Initialize Azure OpenAI client for chat completions."""
    endpoint = os.getenv("AZURE_CHAT_ENDPOINT", "https://ai-40mini.cognitiveservices.azure.com/")
    api_key = os.getenv("AZURE_CHAT_API_KEY", "")

    if not api_key:
        raise ValueError("AZURE_CHAT_API_KEY environment variable not set")

    return AzureOpenAI(
        api_version="2024-12-01-preview",
        azure_endpoint=endpoint,
        api_key=api_key
    )


def get_gemini_client(model_name: str = 'gemini-2.5-flash'):
    """Initialize Google Gemini client."""
    api_key = os.getenv("GEMINI_API_KEY", "")

    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set")

    genai.configure(api_key=api_key)
    return genai.GenerativeModel(model_name)


# ----------------------- RAG Prompt & Messages -----------------------
def format_sources_for_context(sources: List[tuple]) -> str:
    """Format retrieved sources into a context string for the LLM."""
    context_parts = []
    for idx, (doc, score) in enumerate(sources, 1):
        context_parts.append(f"[Source {idx}] (Relevance: {score:.3f})\n{doc.page_content}\n")
    return "\n".join(context_parts)


def create_rag_prompt(query: str, context: str) -> str:
    """Create a RAG prompt that instructs the LLM to answer based on context."""
    return f"""You are a helpful AI assistant that answers questions based on the provided document context.

IMPORTANT INSTRUCTIONS:
1. Answer the question using ONLY the information from the provided sources below
2. If the answer cannot be found in the sources, say "I cannot find this information in the provided document"
3. Be specific and cite which source number you're using when possible
4. If sources contradict each other, mention both perspectives
5. Keep your answer concise but complete

SOURCES:
{context}

QUESTION:
{query}

ANSWER:"""


def create_chat_messages(query: str, context: str) -> List[dict]:
    """Create messages for chat completion API."""
    system_prompt = """You are a helpful AI assistant specialized in answering questions about documents.
You must ONLY use the information provided in the sources to answer questions.
If the information is not in the sources, clearly state that you cannot answer based on the provided documents.
Be accurate, concise, and always cite your sources when possible."""

    user_prompt = f"""Based on the following sources from the document, please answer the question.

SOURCES:
{context}

QUESTION: {query}"""

    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]


# ----------------------- Document Retrieval -----------------------
async def retrieve_relevant_documents(
    query: str,
    file_id: str,
    k: int,
    request: Request
) -> List[tuple]:
    """Retrieve relevant documents from vector store."""
    try:
        # Get embedding for the query
        embedding = vector_store.embedding_function.embed_query(query)

        # Search for similar documents
        if isinstance(vector_store, AsyncPgVector):
            documents = await vector_store.asimilarity_search_with_score_by_vector(
                embedding,
                k=k,
                filter={"file_id": file_id},
                executor=request.app.state.thread_pool,
            )
        else:
            documents = vector_store.similarity_search_with_score_by_vector(
                embedding, k=k, filter={"file_id": file_id}
            )

        return documents
    except Exception as e:
        logger.error(f"Error retrieving documents: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve documents: {str(e)}"
        )


# ----------------------- LLM Response Generation -----------------------
async def generate_azure_response(messages: List[dict], temperature: float) -> str:
    """Generate response using Azure OpenAI."""
    try:
        client = get_azure_client()
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=temperature,
            max_tokens=1000
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Azure OpenAI error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Azure OpenAI error: {str(e)}"
        )


async def generate_gemini_response(
    prompt: str,
    temperature: float,
    model_name: str = 'gemini-2.5-flash'
) -> str:
    """Generate response using Google Gemini."""
    try:
        model = get_gemini_client(model_name)

        generation_config = {
            "temperature": temperature,
            "max_output_tokens": 1000,
        }

        response = model.generate_content(
            prompt,
            generation_config=generation_config
        )

        # Simple text extraction with graceful error handling
        try:
            return response.text
        except (ValueError, AttributeError):
            # Gemini blocked the response - return friendly message
            return "I apologize, but I cannot generate a response for this query at the moment. Please try rephrasing your question or try a different query."

    except Exception as e:
        logger.error(f"Gemini API error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Gemini API error: {str(e)}"
        )


async def generate_ollama_response(prompt: str, temperature: float) -> str:
    """Generate response using Ollama (DeepSeek R1) - local LLM."""
    try:
        ollama_host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
        ollama_model = os.getenv("OLLAMA_MODEL", "deepseek-r1:latest")

        # Create Ollama client with custom host
        client = ollama.Client(host=ollama_host)

        # Generate response
        response = client.generate(
            model=ollama_model,
            prompt=prompt,
            options={
                "temperature": temperature,
                "num_predict": 1000,  # max tokens
            }
        )

        # Extract response text
        try:
            resp_text = response['response']
        except (TypeError, KeyError):
            resp_text = getattr(response, 'response', str(response))

        # DeepSeek R1 specific: Extract final answer after thinking tags
        if isinstance(resp_text, str):
            if "</think>" in resp_text:
                parts = resp_text.split("</think>")
                resp_text = parts[-1].strip() if len(parts) > 1 else resp_text
            resp_text = resp_text.replace("<think>", "").replace("</think>", "")

        return resp_text

    except Exception as e:
        logger.error(f"Ollama error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ollama error: {str(e)}"
        )


# ----------------------- Guardrail Integration -----------------------
async def validate_with_guardrail(query: str, target_id: str = "chat-endpoint") -> tuple[bool, str]:
    """
    Validate query with external guardrail service.

    This follows Promptfoo's architecture:
    1. User Input → Guardrail Validation → Decision
    2. If allowed=true → Process with LLM
    3. If allowed=false → Block and return error

    Args:
        query: User input to validate
        target_id: Guardrail target identifier

    Returns:
        Tuple of (allowed: bool, reason: str)
    """
    try:
        guardrail = get_guardrail(target_id)
        result = guardrail.analyze_prompt(query)

        logger.info(
            f"Guardrail validation: allowed={result.allowed}, "
            f"risk={result.risk_level}, reason={result.reason}"
        )

        return result.allowed, result.reason

    except Exception as e:
        logger.error(f"Guardrail validation error: {str(e)}")
        # Fail-safe: allow on guardrail error (or choose to block)
        return True, f"Guardrail error (fail-safe): {str(e)}"


# ----------------------- Chat Endpoint -----------------------
@router.post("/chat", response_model=SimpleChatResponse)
async def chat_with_documents(request: Request, body: ChatRequest):
    """
    Clean chat endpoint with EXTERNAL guardrails.

    Architecture Flow:
        1. User → /chat endpoint
        2. Call guardrail service for validation
        3. If blocked → Return error
        4. If allowed → Retrieve documents → Generate response → Return

    This endpoint is now a NORMAL endpoint without embedded security logic.
    All security validation happens via the external guardrail service.

    Supports:
    - Azure OpenAI GPT-4o-mini
    - Google Gemini
    - Ollama (DeepSeek R1)
    """
    try:
        # ═══════════════════════════════════════════════════════════
        # STEP 1: GUARDRAIL VALIDATION (EXTERNAL)
        # ═══════════════════════════════════════════════════════════
        allowed, reason = await validate_with_guardrail(body.query)

        if not allowed:
            logger.warning(f"Query blocked by guardrail: {reason}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=reason
            )

        # ═══════════════════════════════════════════════════════════
        # STEP 2: RETRIEVE DOCUMENTS (RAG)
        # ═══════════════════════════════════════════════════════════
        logger.info(f"Retrieving documents for query: {body.query[:80]}...")
        documents = await retrieve_relevant_documents(
            body.query,
            body.file_id,
            body.k,
            request
        )

        if not documents:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No relevant documents found for the query"
            )

        context = format_sources_for_context(documents)
        logger.info(f"Retrieved {len(documents)} relevant documents")

        # ═══════════════════════════════════════════════════════════
        # STEP 3: GENERATE LLM RESPONSE
        # ═══════════════════════════════════════════════════════════
        if body.model and body.model.lower().startswith("azure"):
            messages = create_chat_messages(body.query, context)
            answer = await generate_azure_response(messages, body.temperature)
            model_used = "Azure GPT-4o-mini"

        elif body.model and body.model.lower().startswith("gemini"):
            prompt = create_rag_prompt(body.query, context)
            answer = await generate_gemini_response(prompt, body.temperature, body.model)
            model_used = f"Google Gemini ({body.model})"

        elif body.model and body.model.lower().startswith("ollama"):
            prompt = create_rag_prompt(body.query, context)
            answer = await generate_ollama_response(prompt, body.temperature)
            model_used = f"Ollama ({os.getenv('OLLAMA_MODEL', 'deepseek-r1:latest')})"

        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported model: {body.model}"
            )

        # ═══════════════════════════════════════════════════════════
        # STEP 4: RETURN RESPONSE
        # ═══════════════════════════════════════════════════════════
        logger.info(f"Generated response using {model_used}")

        return SimpleChatResponse(answer=answer)

    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Unexpected error in chat endpoint")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )
