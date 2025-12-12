# """Promptfoo HTTP provider for exercising rag_api endpoints.

# This script is executed by Promptfoo when a provider entry is defined like:

#   providers:
#     - id: file://promptfoo/providers/rag_http_target.py
#       label: rag_api_query
#       config:
#         endpoint: /query
#         method: POST
#         defaultFileId: testid1

# It converts the adversarial or test prompt coming from Promptfoo into an HTTP
# request against the local FastAPI server. Configure the following environment
# variables to control behavior without editing the file:

# - PROMPTFOO_RAG_BASE_URL (default http://127.0.0.1:8000)
# - PROMPTFOO_RAG_JWT (optional bearer token for secured deployments)
# - PROMPTFOO_RAG_FILE_ID (default testid1)
# - PROMPTFOO_RAG_ENTITY_ID (default promptfoo-tester)
# - PROMPTFOO_RAG_K (default 4)
# - PROMPTFOO_RAG_TIMEOUT (default 30 seconds)
# """
# from __future__ import annotations

# import json
# import os
# import urllib.error
# import urllib.request
# from typing import Any, Dict

# DEFAULT_BASE_URL = os.getenv("PROMPTFOO_RAG_BASE_URL", "http://127.0.0.1:8000")
# DEFAULT_FILE_ID = os.getenv("PROMPTFOO_RAG_FILE_ID", "testid1")
# DEFAULT_ENTITY_ID = os.getenv("PROMPTFOO_RAG_ENTITY_ID", "promptfoo-tester")
# DEFAULT_K = int(os.getenv("PROMPTFOO_RAG_K", "4"))
# DEFAULT_TIMEOUT = float(os.getenv("PROMPTFOO_RAG_TIMEOUT", "30"))
# JWT_TOKEN = os.getenv("PROMPTFOO_RAG_JWT")


# def _build_payload(prompt: str, config: Dict[str, Any], context: Dict[str, Any]):
#     vars_ctx = (context or {}).get("vars", {})
#     payload = {
#         "query": prompt,
#         "file_id": vars_ctx.get("file_id")
#         or config.get("defaultFileId")
#         or DEFAULT_FILE_ID,
#         "entity_id": vars_ctx.get("entity_id")
#         or config.get("defaultEntityId")
#         or DEFAULT_ENTITY_ID,
#         "k": vars_ctx.get("k") or config.get("defaultK") or DEFAULT_K,
#     }

#     body_extras = config.get("bodyExtras")
#     if isinstance(body_extras, dict):
#         payload.update(body_extras)

#     return payload


# def call_api(prompt: str, options: Dict[str, Any] | None = None, context: Dict[str, Any] | None = None):
#     options = options or {}
#     config = options.get("config", {})
#     base_url = config.get("baseUrl", DEFAULT_BASE_URL).rstrip("/")
#     endpoint = config.get("endpoint", "/query")
#     method = config.get("method", "POST").upper()
#     url = f"{base_url}{endpoint}"

#     payload = _build_payload(prompt, config, context or {})
#     data = json.dumps(payload).encode("utf-8")

#     headers = {"Content-Type": "application/json"}
#     if config.get("includeAuth", True) and JWT_TOKEN:
#         headers["Authorization"] = f"Bearer {JWT_TOKEN}"

#     request = urllib.request.Request(url, data=data, headers=headers, method=method)

#     try:
#         with urllib.request.urlopen(request, timeout=DEFAULT_TIMEOUT) as response:
#             raw_body = response.read().decode("utf-8")
#             try:
#                 parsed = json.loads(raw_body)
#             except json.JSONDecodeError:
#                 parsed = raw_body

#             output = _extract_text(parsed)
#             return {"output": output, "raw": parsed}
#     except urllib.error.HTTPError as err:
#         body = err.read().decode("utf-8", errors="ignore")
#         return {"output": "", "error": f"HTTP {err.code}: {body}"}
#     except Exception as exc:  # pragma: no cover - defensive logging path
#         return {"output": "", "error": str(exc)}


# def _extract_text(parsed_response: Any) -> str:
#     """Attempt to pull a representative text snippet from rag_api responses."""
#     if isinstance(parsed_response, list) and parsed_response:
#         first = parsed_response[0]
#         if isinstance(first, list) and first:
#             candidate = first[0]
#             if isinstance(candidate, dict):
#                 return candidate.get("page_content") or json.dumps(candidate)
#             return json.dumps(candidate)
#         if isinstance(first, dict):
#             return first.get("page_content") or json.dumps(first)
#         return json.dumps(first)

#     if isinstance(parsed_response, dict):
#         return parsed_response.get("page_content") or json.dumps(parsed_response)

#     if isinstance(parsed_response, str):
#         return parsed_response

#     return json.dumps(parsed_response)



#####################


# """Promptfoo HTTP provider for exercising rag_api endpoints.

# This script is executed by Promptfoo when a provider entry is defined like:

#   providers:
#     - id: file://promptfoo/providers/rag_http_target.py
#       label: rag_api_query
#       config:
#         endpoint: /query
#         method: POST
#         defaultFileId: testid1

# It converts the adversarial or test prompt coming from Promptfoo into an HTTP
# request against the local FastAPI server. Configure the following environment
# variables to control behavior without editing the file:

# - PROMPTFOO_RAG_BASE_URL (default http://127.0.0.1:8000)
# - PROMPTFOO_RAG_JWT (optional bearer token for secured deployments)
# - PROMPTFOO_RAG_FILE_ID (default testid1)
# - PROMPTFOO_RAG_ENTITY_ID (default promptfoo-tester)
# - PROMPTFOO_RAG_K (default 4)
# - PROMPTFOO_RAG_TIMEOUT (default 30 seconds)
# """
# from __future__ import annotations

# import json
# import os
# import urllib.error
# import urllib.request
# from typing import Any, Dict

# DEFAULT_BASE_URL = os.getenv("PROMPTFOO_RAG_BASE_URL", "http://127.0.0.1:8000")
# DEFAULT_FILE_ID = os.getenv("PROMPTFOO_RAG_FILE_ID", "testid1")
# DEFAULT_ENTITY_ID = os.getenv("PROMPTFOO_RAG_ENTITY_ID", "promptfoo-tester")
# DEFAULT_K = int(os.getenv("PROMPTFOO_RAG_K", "4"))
# DEFAULT_TIMEOUT = float(os.getenv("PROMPTFOO_RAG_TIMEOUT", "30"))
# JWT_TOKEN = os.getenv("PROMPTFOO_RAG_JWT")


# def _build_payload(prompt: str, config: Dict[str, Any], context: Dict[str, Any]):
#     vars_ctx = (context or {}).get("vars", {})
#     payload = {
#         "query": prompt,
#         "file_id": vars_ctx.get("file_id")
#         or config.get("defaultFileId")
#         or DEFAULT_FILE_ID,
#         "entity_id": vars_ctx.get("entity_id")
#         or config.get("defaultEntityId")
#         or DEFAULT_ENTITY_ID,
#         "k": vars_ctx.get("k") or config.get("defaultK") or DEFAULT_K,
#     }

#     body_extras = config.get("bodyExtras")
#     if isinstance(body_extras, dict):
#         payload.update(body_extras)

#     return payload


# def call_api(prompt: str, options: Dict[str, Any] | None = None, context: Dict[str, Any] | None = None):
#     options = options or {}
#     config = options.get("config", {})
#     base_url = config.get("baseUrl", DEFAULT_BASE_URL).rstrip("/")
#     endpoint = config.get("endpoint", "/query")
#     method = config.get("method", "POST").upper()
#     url = f"{base_url}{endpoint}"

#     payload = _build_payload(prompt, config, context or {})
#     data = json.dumps(payload).encode("utf-8")

#     headers = {"Content-Type": "application/json"}
#     if config.get("includeAuth", True) and JWT_TOKEN:
#         headers["Authorization"] = f"Bearer {JWT_TOKEN}"

#     request = urllib.request.Request(url, data=data, headers=headers, method=method)

#     try:
#         with urllib.request.urlopen(request, timeout=DEFAULT_TIMEOUT) as response:
#             raw_body = response.read().decode("utf-8")
#             try:
#                 parsed = json.loads(raw_body)
#             except json.JSONDecodeError:
#                 parsed = raw_body

#             output = _extract_text(parsed)
#             return {"output": output, "raw": parsed}
#     except urllib.error.HTTPError as err:
#         body = err.read().decode("utf-8", errors="ignore")
#         return {"output": "", "error": f"HTTP {err.code}: {body}"}
#     except Exception as exc:  # pragma: no cover - defensive logging path
#         return {"output": "", "error": str(exc)}


# def _extract_text(parsed_response: Any) -> str:
#     """Attempt to pull a representative text snippet from rag_api responses."""
#     if isinstance(parsed_response, list) and parsed_response:
#         first = parsed_response[0]
#         if isinstance(first, list) and first:
#             candidate = first[0]
#             if isinstance(candidate, dict):
#                 return candidate.get("page_content") or json.dumps(candidate)
#             return json.dumps(candidate)
#         if isinstance(first, dict):
#             return first.get("page_content") or json.dumps(first)
#         return json.dumps(first)

#     if isinstance(parsed_response, dict):
#         return parsed_response.get("page_content") or json.dumps(parsed_response)

#     if isinstance(parsed_response, str):
#         return parsed_response

#     return json.dumps(parsed_response)



#####################


"""
Promptfoo HTTP provider for exercising rag_api endpoints.

This script is executed by Promptfoo when a provider entry is defined like:

  providers:
    - id: file://promptfoo/providers/rag_http_target.py
      label: rag_api_query
      config:
        endpoint: /query
        method: POST
        defaultFileId: testid1

Environment variables supported:
- PROMPTFOO_RAG_BASE_URL (default http://127.0.0.1:8000)
- PROMPTFOO_RAG_JWT (optional bearer token)
- PROMPTFOO_RAG_FILE_ID (default testid1)
- PROMPTFOO_RAG_ENTITY_ID (default promptfoo-tester)
- PROMPTFOO_RAG_K (default 4)
- PROMPTFOO_RAG_TIMEOUT (default 30)
"""

from __future__ import annotations
import json
import os
import urllib.error
import urllib.request
from typing import Any, Dict

# -------------------------------------------
# Defaults
# -------------------------------------------

DEFAULT_BASE_URL = os.getenv("PROMPTFOO_RAG_BASE_URL", "http://127.0.0.1:8000")
DEFAULT_FILE_ID = os.getenv("PROMPTFOO_RAG_FILE_ID", "testid1")
DEFAULT_ENTITY_ID = os.getenv("PROMPTFOO_RAG_ENTITY_ID", "promptfoo-tester")
DEFAULT_K = int(os.getenv("PROMPTFOO_RAG_K", "4"))
DEFAULT_TIMEOUT = float(os.getenv("PROMPTFOO_RAG_TIMEOUT", "30"))
JWT_TOKEN = os.getenv("PROMPTFOO_RAG_JWT")


# -------------------------------------------
# Build Payload
# -------------------------------------------

def _build_payload(prompt: str, config: Dict[str, Any], context: Dict[str, Any]):
    vars_ctx = (context or {}).get("vars", {})

    payload = {
        "query": prompt,
        "file_id": vars_ctx.get("file_id")
        or config.get("defaultFileId")
        or DEFAULT_FILE_ID,
        "entity_id": vars_ctx.get("entity_id")
        or config.get("defaultEntityId")
        or DEFAULT_ENTITY_ID,
        "k": vars_ctx.get("k") or config.get("defaultK") or DEFAULT_K,
    }

    # Extra user config
    body_extras = config.get("bodyExtras")
    if isinstance(body_extras, dict):
        payload.update(body_extras)

    return payload


# -------------------------------------------
# SAFE SCRUBBER (removes sensitive data!)
# -------------------------------------------

def _scrub_raw(parsed):
    """
    Remove page_content and sensitive text before sending to Promptfoo UI.
    Prevents leaking emails, SSNs, API keys, passwords, etc.
    """
    try:
        # RAG returns: [ [ {doc}, score ], ... ]
        if isinstance(parsed, list):
            for entry in parsed:
                try:
                    document, score = entry
                    if isinstance(document, dict):
                        document["page_content"] = "(hidden)"
                except:
                    continue

        # Chat returns: { answer: "...", sources: [...] }
        if isinstance(parsed, dict) and "sources" in parsed:
            for s in parsed["sources"]:
                if isinstance(s, dict):
                    s["content"] = "(hidden)"

        return parsed

    except Exception:
        return parsed


# -------------------------------------------
# HUMAN-READABLE OUTPUT FOR PROMPTFOO UI
# -------------------------------------------

def _format_output(parsed: Any) -> str:
    """
    Minimal output - show only document count and scores.
    """

    if parsed is None:
        return "(empty response)"

    if parsed == []:
        return "(no documents matched this query)"

    if isinstance(parsed, str):
        return parsed

    if isinstance(parsed, list):
        lines = []
        lines.append(f"Found {len(parsed)} documents:")
        for idx, entry in enumerate(parsed, 1):
            try:
                document, score = entry
                lines.append(f"  Document #{idx}: Score {round(score, 4)}")
            except Exception:
                return json.dumps(parsed, indent=2)

        return "\n".join(lines)

    if isinstance(parsed, dict):
        # Show only high-level info (answer, model)
        safe = {
            "answer": parsed.get("answer"),
            "model_used": parsed.get("model_used"),
            "source_count": len(parsed.get("sources", [])),
        }
        return json.dumps(safe, indent=2)

    return json.dumps(parsed, indent=2)


# -------------------------------------------
# Call API
# -------------------------------------------

def call_api(prompt: str, options: Dict[str, Any] | None = None,
             context: Dict[str, Any] | None = None):

    options = options or {}
    config = options.get("config", {})

    base_url = config.get("baseUrl", DEFAULT_BASE_URL).rstrip("/")
    endpoint = config.get("endpoint", "/query")
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
                "output": formatted_output,  # Shown in Promptfoo UI
                "raw": scrubbed              # Used for assertions
            }

    except urllib.error.HTTPError as err:
        body = err.read().decode("utf-8", errors="ignore")
        return {"output": f"HTTP {err.code}: {body}", "raw": None}

    except Exception as exc:
        return {"output": f"Error: {str(exc)}", "raw": None}