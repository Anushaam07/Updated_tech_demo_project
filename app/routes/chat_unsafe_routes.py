# app/routes/chat_routes.py
"""
UNSAFE Chat Endpoint for Demo Purposes ONLY

This file provides /chat-unsafe endpoint to demonstrate data leakage.
It intentionally has NO guardrails protection, NO redaction, NO filtering.
Production uses chat_routes_with_external_guardrails.py with full protection.

"""

import os
from typing import List
from fastapi import APIRouter, Request, HTTPException, status
from openai import AzureOpenAI
import google.generativeai as genai
import ollama

from app.config import logger, vector_store
from app.models import ChatRequest, SimpleChatResponse
from app.services.vector_store.async_pg_vector import AsyncPgVector

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


# ----------------------- RAG Prompt & Messages (UNSAFE - NO PROTECTION) -----------------------
def format_sources_for_context_unsafe(sources: List[tuple]) -> str:
    """
    Format retrieved sources WITHOUT any redaction.
    This will expose ALL sensitive data in documents!
    """
    context_parts = []
    for idx, (doc, score) in enumerate(sources, 1):
        # NO REDACTION - Shows raw content including secrets!
        context_parts.append(f"[Source {idx}] (Relevance: {score:.3f})\n{doc.page_content}\n")
    return "\n".join(context_parts)


def create_rag_prompt_unsafe(query: str, context: str) -> str:
    """
    Create a RAG prompt WITHOUT security instructions.
    The LLM will answer any question including sensitive data requests!
    """
    return f"""You are a helpful AI assistant that answers questions based on the provided document context.

INSTRUCTIONS:
1. Answer the question using ONLY the information from the provided sources below
2. If the answer cannot be found in the sources, say "I cannot find this information in the provided document"
3. Be specific and cite which source number you're using when possible
4. Keep your answer concise but complete

SOURCES:
{context}

QUESTION:
{query}

ANSWER:"""


def create_chat_messages_unsafe(query: str, context: str) -> List[dict]:
    """
    Create messages for chat completion WITHOUT security constraints.
    No instructions to block sensitive data!
    """
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
async def retrieve_relevant_documents(query: str, file_id: str, k: int, request: Request) -> List[tuple]:
    """Retrieve relevant documents from vector store."""
    try:
        embedding = vector_store.embedding_function.embed_query(query)
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


# ----------------------- LLM Response Generation (UNSAFE) -----------------------
async def generate_azure_response_unsafe(messages: List[dict], temperature: float) -> str:
    """
    Generate response using Azure OpenAI WITHOUT any redaction.
    ⚠️ Output may contain sensitive data!
    """
    try:
        client = get_azure_client()
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=temperature,
            max_tokens=1000
        )
        # NO REDACTION - Return raw output
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Azure OpenAI error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Azure OpenAI error: {str(e)}"
        )


async def generate_gemini_response_unsafe(prompt: str, temperature: float, model_name: str = 'gemini-2.5-flash') -> str:
    """
    Generate response using Google Gemini WITHOUT any redaction.
    ⚠️ Output may contain sensitive data!
    """
    try:
        model = get_gemini_client(model_name)
        generation_config = {"temperature": temperature, "max_output_tokens": 1000}
        response = model.generate_content(prompt, generation_config=generation_config)

        try:
            text = response.text
        except (ValueError, AttributeError):
            # Gemini blocked the response
            return "I apologize, but I cannot generate a response for this query at the moment. Please try rephrasing your question or try a different query."

        # NO REDACTION - Return raw output
        return text
    except Exception as e:
        logger.error(f"Gemini API error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Gemini API error: {str(e)}"
        )


async def generate_ollama_response_unsafe(prompt: str, temperature: float) -> str:
    """
    Generate response using Ollama WITHOUT any redaction.
    Output may contain sensitive data!
    """
    try:
        ollama_host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
        ollama_model = os.getenv("OLLAMA_MODEL", "deepseek-r1:latest")
        client = ollama.Client(host=ollama_host)

        response = client.generate(
            model=ollama_model,
            prompt=prompt,
            options={
                "temperature": temperature,
                "num_predict": 1000,
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

        # NO REDACTION - Return raw output
        return resp_text
    except Exception as e:
        logger.error(f"Ollama error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ollama error: {str(e)}"
        )


# ----------------------- UNSAFE Chat Endpoint (FOR DEMO ONLY) -----------------------
@router.post("/chat-unsafe", response_model=SimpleChatResponse)
async def chat_with_documents_unsafe(request: Request, body: ChatRequest):
    """
     UNSAFE DEMO ENDPOINT - NO GUARDRAILS PROTECTION! 

    This endpoint demonstrates what happens WITHOUT security controls:
    - NO input validation / guardrails
    - NO sensitive query blocking
    - NO data redaction
    - NO output filtering

    Use this to demonstrate the BEFORE state in demos.
    The /chat endpoint (with guardrails) is the AFTER state.

     FOR DEMONSTRATION PURPOSES ONLY - DO NOT USE IN PRODUCTION! 
    """
    try:
        # ═══════════════════════════════════════════════════════════
        # NO GUARDRAIL VALIDATION - ALL QUERIES ALLOWED
        # ═══════════════════════════════════════════════════════════

        # Retrieve documents WITHOUT sanitization
        logger.warning(f"[UNSAFE DEMO] Retrieving documents for query: {body.query[:80]}...")
        documents = await retrieve_relevant_documents(body.query, body.file_id, body.k, request)

        if not documents:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No relevant documents found for the query"
            )

        # ═══════════════════════════════════════════════════════════
        # NO REDACTION - RAW CONTENT WITH SECRETS EXPOSED
        # ═══════════════════════════════════════════════════════════
        context = format_sources_for_context_unsafe(documents)
        logger.warning(f"[UNSAFE DEMO] Retrieved {len(documents)} documents - NO REDACTION APPLIED")

        # ═══════════════════════════════════════════════════════════
        # GENERATE RESPONSE WITHOUT SECURITY CONSTRAINTS
        # ═══════════════════════════════════════════════════════════
        if body.model and body.model.lower().startswith("azure"):
            messages = create_chat_messages_unsafe(body.query, context)
            answer = await generate_azure_response_unsafe(messages, body.temperature)
            model_used = "Azure GPT-4o-mini (UNSAFE)"

        elif body.model and body.model.lower().startswith("gemini"):
            prompt = create_rag_prompt_unsafe(body.query, context)
            answer = await generate_gemini_response_unsafe(prompt, body.temperature, body.model)
            model_used = f"Google Gemini ({body.model}) (UNSAFE)"

        elif body.model and body.model.lower().startswith("ollama"):
            prompt = create_rag_prompt_unsafe(body.query, context)
            answer = await generate_ollama_response_unsafe(prompt, body.temperature)
            model_used = f"Ollama ({os.getenv('OLLAMA_MODEL', 'deepseek-r1:latest')}) (UNSAFE)"

        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported model: {body.model}"
            )

        # ═══════════════════════════════════════════════════════════
        #  RETURN RAW ANSWER - MAY CONTAIN SENSITIVE DATA
        # ═══════════════════════════════════════════════════════════
        logger.warning(f"[UNSAFE DEMO] Generated UNPROTECTED response using {model_used}")
        logger.warning("[UNSAFE DEMO] Response may contain passwords, API keys, SSN, and other sensitive data!")

        return SimpleChatResponse(answer=answer)

    except HTTPException:
        raise
    except Exception as e:
        logger.exception("[UNSAFE DEMO] Unexpected error in unsafe chat endpoint")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )