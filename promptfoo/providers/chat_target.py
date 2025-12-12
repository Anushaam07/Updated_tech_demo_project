
# promptfoo/providers/chat_target.py
"""
Promptfoo HTTP provider for the /chat endpoint with extra sanitization.
"""

from __future__ import annotations
import json
import os
import urllib.error
import urllib.request
from typing import Any, Dict
import re

# Defaults
DEFAULT_BASE_URL = os.getenv("PROMPTFOO_RAG_BASE_URL", "http://127.0.0.1:8000")
DEFAULT_FILE_ID = os.getenv("PROMPTFOO_RAG_FILE_ID", "file_1764804070911_2370suvck")
DEFAULT_ENTITY_ID = os.getenv("PROMPTFOO_RAG_ENTITY_ID", "test1")
DEFAULT_K = int(os.getenv("PROMPTFOO_RAG_K", "4"))
DEFAULT_TIMEOUT = float(os.getenv("PROMPTFOO_RAG_TIMEOUT", "180"))
JWT_TOKEN = os.getenv("PROMPTFOO_RAG_JWT")

# Secret-detection regexes (same idea as server side) - redact in UI output too
_SCRUB_PATTERNS = [
    (re.compile(r'\bsk_live_[A-Za-z0-9_\-]{8,}\b', re.IGNORECASE), '[REDACTED_API_KEY]'),
    (re.compile(r'\bsk_test_[A-Za-z0-9_\-]{8,}\b', re.IGNORECASE), '[REDACTED_API_KEY]'),
    (re.compile(r'\bsk-[A-Za-z0-9_\-]{8,}\b', re.IGNORECASE), '[REDACTED_API_KEY]'),
    (re.compile(r'\bAKIA[0-9A-Z]{8,}\b', re.IGNORECASE), '[REDACTED_AWS_KEY]'),
    (re.compile(r'-----BEGIN PRIVATE KEY-----[\s\S]+?-----END PRIVATE KEY-----', re.IGNORECASE), '[REDACTED_PRIVATE_KEY]'),
    (re.compile(r'\b(?:\d[ -]*?){13,19}\b'), '[REDACTED_CREDIT_CARD]'),
    (re.compile(r'\b\d{3}-\d{2}-\d{4}\b'), '[REDACTED_SSN]'),
    (re.compile(r'\beyJ[0-9A-Za-z_\-]+\.[0-9A-Za-z_\-]+\.[0-9A-Za-z_\-]+\b'), '[REDACTED_JWT]'),
    (re.compile(r'(?i)(api[_\-\s]?key|secret[_\-\s]?key|access[_\-\s]?token)[:=]\s*\S+'), '[REDACTED_SECRET]'),
]

def _build_payload(prompt: str, config: Dict[str, Any], context: Dict[str, Any]):
    vars_ctx = (context or {}).get("vars", {})
    payload = {
        "query": prompt,
        "file_id": vars_ctx.get("file_id") or config.get("defaultFileId") or DEFAULT_FILE_ID,
        "entity_id": vars_ctx.get("entity_id") or config.get("defaultEntityId") or DEFAULT_ENTITY_ID,
        "k": vars_ctx.get("k") or config.get("defaultK") or DEFAULT_K,
        "model": vars_ctx.get("model") or config.get("defaultModel") or "gemini-2.0-flash",
        "temperature": vars_ctx.get("temperature") or config.get("defaultTemperature") or 0.7,
    }
    body_extras = config.get("bodyExtras")
    if isinstance(body_extras, dict):
        payload.update(body_extras)
    return payload

def _scrub_text(s: str) -> str:
    if s is None:
        return s
    out = s
    for cre, repl in _SCRUB_PATTERNS:
        out = cre.sub(repl, out)
    return out

def _scrub_raw(parsed):
    """
    Remove document content from sources before sending to Promptfoo UI,
    and redact any secrets from 'answer' and source contents.
    """
    try:
        if isinstance(parsed, dict):
            # scrub answer if present
            if "answer" in parsed and isinstance(parsed["answer"], str):
                parsed["answer"] = _scrub_text(parsed["answer"])

            # scrub sources: hide content entirely to avoid UI leak OR redact secrets
            if "sources" in parsed and isinstance(parsed["sources"], list):
                for s in parsed["sources"]:
                    if isinstance(s, dict):
                        content = s.get("content")
                        if isinstance(content, str) and content.strip():
                            redacted = _scrub_text(content)
                            s["content"] = "(hidden for security)"
                            s["_redacted_preview"] = redacted[:200] + ("..." if len(redacted) > 200 else "")
                        else:
                            s["content"] = "(hidden for security)"
        return parsed
    except Exception:
        return parsed

def _format_output(parsed: Any) -> str:
    """
    Format chat response - show only the (scrubbed) answer text for Promptfoo UI.
    """
    if parsed is None:
        return "(empty response)"

    if isinstance(parsed, str):
        return _scrub_text(parsed)

    if isinstance(parsed, dict):
        return parsed.get("answer", "(no answer)")

    return json.dumps(parsed, indent=2)

def call_api(prompt: str, options: Dict[str, Any] | None = None,
             context: Dict[str, Any] | None = None):

    options = options or {}
    config = options.get("config", {})

    base_url = config.get("baseUrl", DEFAULT_BASE_URL).rstrip("/")
    endpoint = config.get("endpoint", "/chat")
    method = config.get("method", "POST").upper()
    url = f"{base_url}{endpoint}"

    payload = _build_payload(prompt, config, context or {})
    data = json.dumps(payload).encode("utf-8")

    headers = {"Content-Type": "application/json"}
    if config.get("includeAuth", True) and JWT_TOKEN:
        headers["Authorization"] = f"Bearer {JWT_TOKEN}"

    request = urllib.request.Request(url, data=data, headers=headers, method=method)

    try:
        with urllib.request.urlopen(request, timeout=DEFAULT_TIMEOUT) as response:
            raw_body = response.read().decode("utf-8")
            try:
                parsed_json = json.loads(raw_body)
            except json.JSONDecodeError:
                parsed_json = raw_body

            # SCRUB SENSITIVE FIELDS
            scrubbed = _scrub_raw(parsed_json)

            # PRETTY UI OUTPUT
            formatted_output = _format_output(scrubbed)

            return {
                "output": formatted_output,  
                "raw": scrubbed           
            }

    except urllib.error.HTTPError as err:
        body = err.read().decode("utf-8", errors="ignore")
        return {"output": f"HTTP {err.code}: {body}", "raw": None}

    except Exception as exc:
        return {"output": f"Error: {str(exc)}", "raw": None}
