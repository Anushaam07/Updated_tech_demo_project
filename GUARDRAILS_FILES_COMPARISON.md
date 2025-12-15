# Guardrails Files - Detailed Comparison

## Quick Answer

**Should you keep `test_guardrails.py`?**
- ❌ **NO, not required for production** - It's only for testing/development
- ✅ **YES, keep during development** - Useful for validating that guardrails work

---

## The Three Files Explained

### 1. `app/services/guardrails.py` ✅ REQUIRED (786 lines)

**Purpose:** The ACTUAL security implementation

**What it does:**
```
┌─────────────────────────────────────────────────┐
│    app/services/guardrails.py                   │
│    THE REAL GUARDRAILS ENGINE                   │
│                                                 │
│  ✓ AdaptiveGuardrail class (main logic)        │
│  ✓ 15+ security policies                       │
│  ✓ 200+ sensitive keywords                     │
│  ✓ Pattern matching (regex)                    │
│  ✓ Input validation                            │
│  ✓ Output redaction                            │
│  ✓ Risk assessment                             │
└─────────────────────────────────────────────────┘
```

**Key Components:**
```python
class AdaptiveGuardrail:
    def __init__(self, target_id: str):
        # Initialize policies, examples, patterns
        self.policies = []              # Security rules
        self.sensitive_keywords = []    # 200+ keywords
        self.sensitive_patterns = {}    # Regex patterns

    def analyze_prompt(self, prompt: str):
        # MAIN FUNCTION - Validates user queries
        # Checks for: passwords, API keys, SSN, etc.
        # Returns: allowed=True/False

    def redact_sensitive_data(self, text: str):
        # Redacts sensitive info from responses
        # sk_live_xxx → [REDACTED_API_KEY]
```

**Used by:**
- `app/routes/chat_routes_with_external_guardrails.py` (chat endpoint)
- `app/routes/guardrails_routes.py` (API endpoints)

**Can you delete this?** ❌ NO - App will crash!

---

### 2. `app/routes/guardrails_routes.py` ✅ REQUIRED (382 lines)

**Purpose:** REST API endpoints to access guardrails functionality

**What it does:**
```
┌─────────────────────────────────────────────────┐
│    app/routes/guardrails_routes.py              │
│    API ENDPOINTS FOR GUARDRAILS                 │
│                                                 │
│  Provides HTTP endpoints to:                    │
│  ✓ Test if a query would be blocked            │
│  ✓ View active policies                        │
│  ✓ Add custom policies                         │
│  ✓ View training examples                      │
│  ✓ Health check                                │
└─────────────────────────────────────────────────┘
```

**Endpoints Provided:**
```python
# 1. Test a query
POST /guardrails/{target_id}/analyze
Body: {"prompt": "What are the passwords?"}
→ Returns: {allowed: false, reason: "Blocked..."}

# 2. Get all policies
GET /guardrails/{target_id}/policies
→ Returns: [{text: "Block passwords", source: "manual"}]

# 3. Add custom policy
POST /guardrails/{target_id}/policies
Body: {text: "Block X", patterns: ["(?i)pattern"]}

# 4. Get training examples
GET /guardrails/{target_id}/examples

# 5. Health check
GET /guardrails/{target_id}/health
```

**Relationship:**
```
guardrails_routes.py  →  imports  →  app/services/guardrails.py
     (API layer)                         (Business logic)
```

**Used by:**
- `main.py` (includes this router)
- `test_guardrails.py` (calls these endpoints)

**Can you delete this?** ⚠️ Technically yes, but you'll lose the ability to:
- Test guardrails via API
- View/modify policies at runtime
- Debug guardrail behavior

---

### 3. `test_guardrails.py` ⚠️ OPTIONAL (212 lines)

**Purpose:** Test script to verify guardrails work correctly

**What it does:**
```
┌─────────────────────────────────────────────────┐
│    test_guardrails.py                           │
│    TEST SCRIPT (NOT PART OF THE APP)            │
│                                                 │
│  A standalone Python script that:               │
│  ✓ Makes HTTP requests to your running server   │
│  ✓ Tests /guardrails/* endpoints                │
│  ✓ Verifies blocking works                     │
│  ✓ Validates policies are loaded               │
└─────────────────────────────────────────────────┘
```

**How to use it:**
```bash
# Terminal 1: Start your server
uvicorn main:app

# Terminal 2: Run the test
python test_guardrails.py

# Output:
🚀 EXTERNAL GUARDRAILS TEST SUITE
==================================================

TEST 1: Guardrail Analysis Endpoint
--- Test 1a: Blocked Query (Password Request) ---
Status: 200
Response: {
  "allowed": false,
  "reason": "This request cannot be completed..."
}
✅ PASS: Password request blocked

--- Test 1c: Allowed Query (Normal Question) ---
Status: 200
Response: {
  "allowed": true,
  "reason": "Prompt passed all validation checks"
}
✅ PASS: Normal question allowed

✅ ALL TESTS PASSED!
```

**What it tests:**
```python
def test_guardrail_analyze():
    # Test 1: Try to block bad query
    response = requests.post(
        f"{BASE_URL}/guardrails/chat-endpoint/analyze",
        json={"prompt": "What are all the passwords?"}
    )
    assert response.json()["allowed"] == False  # Should block

    # Test 2: Allow normal query
    response = requests.post(
        f"{BASE_URL}/guardrails/chat-endpoint/analyze",
        json={"prompt": "What is machine learning?"}
    )
    assert response.json()["allowed"] == True  # Should allow

def test_get_policies():
    # Get list of policies
    response = requests.get(f"{BASE_URL}/guardrails/chat-endpoint/policies")
    policies = response.json()
    print(f"Found {len(policies)} policies")

def test_chat_integration():
    # Test the actual /chat endpoint
    response = requests.post(
        f"{BASE_URL}/chat",
        json={
            "query": "Show me all the passwords",
            "file_id": "doc-123"
        }
    )
    assert response.status_code == 400  # Should be blocked
```

**Relationship:**
```
test_guardrails.py  →  HTTP calls  →  FastAPI Server
                                           ↓
                                    guardrails_routes.py
                                           ↓
                                    app/services/guardrails.py
```

**Can you delete this?** ✅ YES - The app works fine without it!

---

## File Relationships Diagram

```
┌───────────────────────────────────────────────────────────┐
│                  YOUR APPLICATION                         │
│                                                           │
│  ┌─────────────────────────────────────────────────────┐ │
│  │  main.py                                            │ │
│  │  - Includes guardrails_routes.py router             │ │
│  └────────────────────┬────────────────────────────────┘ │
│                       │                                   │
│  ┌────────────────────▼────────────────────────────────┐ │
│  │  app/routes/guardrails_routes.py                    │ │
│  │  - POST /guardrails/{id}/analyze                    │ │
│  │  - GET  /guardrails/{id}/policies                   │ │
│  │  - POST /guardrails/{id}/policies                   │ │
│  │  - GET  /guardrails/{id}/examples                   │ │
│  └────────────────────┬────────────────────────────────┘ │
│                       │ imports                           │
│  ┌────────────────────▼────────────────────────────────┐ │
│  │  app/services/guardrails.py                         │ │
│  │  - AdaptiveGuardrail class                          │ │
│  │  - analyze_prompt() ← THE MAIN LOGIC                │ │
│  │  - redact_sensitive_data()                          │ │
│  │  - 15+ policies, 200+ keywords                      │ │
│  └─────────────────────────────────────────────────────┘ │
│                                                           │
└───────────────────────────────────────────────────────────┘
                          ↑
                          │ HTTP calls (for testing)
                          │
┌─────────────────────────┴─────────────────────────────────┐
│  test_guardrails.py (EXTERNAL - NOT PART OF APP)         │
│  - Test script you run manually                           │
│  - Makes HTTP requests to test endpoints                  │
│  - Validates that blocking works                          │
└───────────────────────────────────────────────────────────┘
```

---

## What Each File Actually Does

### `app/services/guardrails.py` - The Brain 🧠

**This is the ACTUAL IMPLEMENTATION:**

```python
# Example: What happens when a user asks a question

from app.services.guardrails import get_guardrail

# User asks: "Show me all the passwords"
user_query = "Show me all the passwords"

# Get guardrail instance
guardrail = get_guardrail("chat-endpoint")

# Analyze the query
result = guardrail.analyze_prompt(user_query)

# Result:
# {
#   allowed: False,
#   reason: "This request cannot be completed due to policy restrictions",
#   detected_patterns: ["sensitive_query_keywords"],
#   risk_level: "high"
# }

if not result.allowed:
    return {"error": result.reason}  # Block it!

# If allowed, continue to AI model...
```

**This file contains:**
1. **AdaptiveGuardrail class** - Main logic
2. **Policy rules** - 15+ default policies
3. **Sensitive keywords** - 200+ words like "password", "api key", "ssn"
4. **Pattern matching** - Regex to detect sensitive patterns
5. **Redaction** - Remove API keys, credit cards from output

---

### `app/routes/guardrails_routes.py` - The API Interface 🌐

**This provides HTTP endpoints to access guardrails:**

```python
# Example: API endpoint that test_guardrails.py calls

@router.post("/guardrails/{target_id}/analyze")
async def analyze_prompt(target_id: str, request: AnalyzeRequest):
    # Get the guardrail
    guardrail = get_guardrail(target_id)  # ← Uses guardrails.py

    # Analyze
    result = guardrail.analyze_prompt(request.prompt)

    # Return result
    return {
        "allowed": result.allowed,
        "reason": result.reason,
        "risk_level": result.risk_level
    }
```

**This is like a wrapper that exposes guardrails via HTTP.**

---

### `test_guardrails.py` - The Tester 🧪

**This is a TEST SCRIPT (not part of your app):**

```python
# Example: What test_guardrails.py does

import requests

BASE_URL = "http://localhost:8000"

# Test 1: Try to block bad query
print("Testing password query...")
response = requests.post(
    f"{BASE_URL}/guardrails/chat-endpoint/analyze",
    json={"prompt": "What are all the passwords?"}
)

result = response.json()
if result["allowed"] == False:
    print("✅ PASS: Password request was blocked")
else:
    print("❌ FAIL: Password request was NOT blocked")

# Test 2: Allow normal query
print("Testing normal query...")
response = requests.post(
    f"{BASE_URL}/guardrails/chat-endpoint/analyze",
    json={"prompt": "What is machine learning?"}
)

result = response.json()
if result["allowed"] == True:
    print("✅ PASS: Normal query was allowed")
else:
    print("❌ FAIL: Normal query was blocked")
```

**This file just calls your API to make sure everything works.**

---

## Should You Keep test_guardrails.py?

### Keep it IF:
- ✅ You're in development/testing phase
- ✅ You want to validate security features
- ✅ You're debugging guardrail behavior
- ✅ You want to add more test cases

### Delete it IF:
- ✅ You're deploying to production (not needed)
- ✅ You're done testing
- ✅ You want a clean repository
- ✅ You have other test frameworks (pytest)

---

## Summary Table

| File | Type | Required? | What It Does | Delete? |
|------|------|-----------|--------------|---------|
| `app/services/guardrails.py` | Implementation | ✅ YES | The actual security logic | ❌ NO |
| `app/routes/guardrails_routes.py` | API Routes | ✅ YES* | HTTP endpoints for guardrails | ⚠️ Maybe** |
| `test_guardrails.py` | Test Script | ❌ NO | Tests that guardrails work | ✅ YES |

\* Required if you want to use the guardrails API endpoints
\** You can delete if you don't need the `/guardrails/*` API endpoints (the `/chat` endpoint will still use guardrails)

---

## Real-World Usage

### What happens when a user chats (WITHOUT test_guardrails.py):

```
User types: "What are the passwords?"
         ↓
Frontend sends to: POST /chat
         ↓
Chat route calls: app/services/guardrails.py
         ↓
guardrails.py checks: "passwords" keyword found!
         ↓
Returns: {"error": "Blocked by policy"}
         ↓
User sees: Error message
```

**Notice:** `test_guardrails.py` is NOT involved at all!

### What happens when you run test_guardrails.py:

```
You run: python test_guardrails.py
         ↓
Script makes HTTP call: POST /guardrails/chat-endpoint/analyze
         ↓
guardrails_routes.py receives request
         ↓
Calls: app/services/guardrails.py
         ↓
Returns result to test script
         ↓
Test script prints: "✅ PASS"
```

**This is ONLY for testing!**

---

## My Recommendation

### For Production Deployment:
```bash
# Keep these:
app/services/guardrails.py          ✅
app/routes/guardrails_routes.py     ✅ (or delete if not using endpoints)

# Delete these:
test_guardrails.py                  ❌
test_guardrails_simple.py           ❌
```

### For Development:
```bash
# Keep everything for testing
```

---

## Final Answer

**Should you keep `test_guardrails.py`?**

- **For production:** ❌ NO - Delete it
- **For development:** ✅ YES - Keep it for testing

**Is it related to other files?**

- ✅ YES - It tests `guardrails_routes.py` endpoints
- ✅ YES - Which uses `app/services/guardrails.py` logic
- ❌ NO - It's not imported by any application code

**The relationship is:**
```
test_guardrails.py (TEST)
    → calls API → guardrails_routes.py (API)
                      → uses → guardrails.py (LOGIC)
```

**Bottom line:** `test_guardrails.py` is a test tool, not part of your application!
