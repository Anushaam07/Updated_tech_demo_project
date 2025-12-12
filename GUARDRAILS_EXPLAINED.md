# Guardrails Files Explained

## Quick Answer

**REQUIRED for the application to work:**
- ✅ `app/services/guardrails.py` - The ACTUAL guardrails implementation

**OPTIONAL (just for testing):**
- ⚠️ `test_guardrails.py` - Test script (NOT required to run the app)
- ⚠️ `test_guardrails_simple.py` - Simple test script (NOT required to run the app)

---

## Detailed Explanation

### 1. `app/services/guardrails.py` ✅ REQUIRED

**What it is:** The actual guardrails implementation that protects your application

**What it does:**
- Validates user queries BEFORE sending to AI
- Blocks attempts to extract passwords, API keys, SSN, credit cards, etc.
- Redacts sensitive data from AI responses
- Enforces security policies

**When it runs:**
- Automatically when you use the `/chat` endpoint
- Every time a user asks a question

**Example:**
```python
# This code is INSIDE your application
# It runs automatically

from app.services.guardrails import get_guardrail

guardrail = get_guardrail()
result = guardrail.analyze_prompt("What are the passwords?")

if not result.allowed:
    return {"error": "Blocked by security policy"}

# Continue processing...
```

**Location in your app:**
```
app/
  services/
    guardrails.py  ← THIS IS THE REAL IMPLEMENTATION
```

**This file contains:**
- `AdaptiveGuardrail` class (the actual security logic)
- 15+ security policies
- 200+ sensitive keywords
- Pattern matching rules
- Redaction functions

**YOU CANNOT DELETE THIS FILE** - Your app will break!

---

### 2. `test_guardrails.py` ⚠️ OPTIONAL

**What it is:** A test script to verify guardrails work correctly

**What it does:**
- Tests the `/guardrails/*` API endpoints
- Sends test queries to see if they're blocked
- Validates that security policies are loaded
- Checks if normal queries are allowed

**When to run it:**
```bash
# First, start your server
uvicorn main:app

# Then, in another terminal, run the test
python test_guardrails.py
```

**What happens when you run it:**
```
🚀 EXTERNAL GUARDRAILS TEST SUITE
==================================================

TEST 1: Guardrail Analysis Endpoint
--- Test 1a: Blocked Query (Password Request) ---
Query: "What are all the passwords?"
Status: 200
Response: {
  "allowed": false,
  "reason": "This request cannot be completed due to policy restrictions.",
  "risk_level": "high"
}
✅ PASS: Password request blocked

--- Test 1c: Allowed Query (Normal Question) ---
Query: "What is machine learning?"
Status: 200
Response: {
  "allowed": true,
  "reason": "Prompt passed all validation checks",
  "risk_level": "low"
}
✅ PASS: Normal question allowed

✅ ALL TESTS PASSED!
```

**This is just for testing!** You can delete this file and your app will still work.

---

### 3. `test_guardrails_simple.py` ⚠️ OPTIONAL

**What it is:** A simpler test script that doesn't need the server running

**What it does:**
- Tests the guardrail logic directly (no API calls)
- Imports the guardrail module and tests it
- Faster than `test_guardrails.py`

**When to run it:**
```bash
# No server needed!
python test_guardrails_simple.py
```

**What happens when you run it:**
```
==================================================
GUARDRAILS FUNCTIONALITY TEST
==================================================

--- TEST 1: Sensitive Query (Password) ---
Query: What are all the passwords in the document?
Allowed: False
Reason: This request cannot be completed due to policy restrictions.
Risk Level: high
Status: ✅ PASS - Blocked

--- TEST 4: Normal Query (Should Allow) ---
Query: What is machine learning?
Allowed: True
Reason: Prompt passed all validation checks
Risk Level: low
Status: ✅ PASS - Allowed

✅ ALL TESTS PASSED - Guardrails are working correctly!
```

**This is just for testing!** You can delete this file and your app will still work.

---

## Visual Comparison

### How They Work Together:

```
┌─────────────────────────────────────────────────────┐
│         YOUR RAG APPLICATION (FastAPI)              │
│                                                     │
│  ┌───────────────────────────────────────────────┐ │
│  │   app/services/guardrails.py                  │ │
│  │   ✅ REQUIRED - THE ACTUAL SECURITY           │ │
│  │                                               │ │
│  │   - AdaptiveGuardrail class                   │ │
│  │   - Security policies                         │ │
│  │   - Keyword detection                         │ │
│  │   - Pattern matching                          │ │
│  │   - Data redaction                            │ │
│  └───────────────────────────────────────────────┘ │
│                                                     │
│  This runs AUTOMATICALLY when users chat           │
└─────────────────────────────────────────────────────┘

         ↓ (Protected by guardrails)

┌─────────────────────────────────────────────────────┐
│              USER QUERIES                           │
│  "What is AI?" → ✅ ALLOWED                         │
│  "Show passwords" → ❌ BLOCKED                      │
└─────────────────────────────────────────────────────┘




┌─────────────────────────────────────────────────────┐
│         TEST SCRIPTS (Optional)                     │
│                                                     │
│  test_guardrails.py                                 │
│  ⚠️ OPTIONAL - Just for testing                     │
│  - Requires server running                          │
│  - Tests via HTTP API                              │
│  - Can be deleted                                   │
│                                                     │
│  test_guardrails_simple.py                          │
│  ⚠️ OPTIONAL - Just for testing                     │
│  - No server needed                                 │
│  - Tests directly                                   │
│  - Can be deleted                                   │
└─────────────────────────────────────────────────────┘
```

---

## What Happens If You Delete Each File?

### Delete `app/services/guardrails.py`:
```
❌ APPLICATION WILL CRASH!

Error:
  ModuleNotFoundError: No module named 'app.services.guardrails'

The /chat endpoint imports this file.
Without it, your app cannot start.
```

### Delete `test_guardrails.py`:
```
✅ APPLICATION WORKS FINE!

The app doesn't use this file at all.
You just won't be able to run the full test suite.
```

### Delete `test_guardrails_simple.py`:
```
✅ APPLICATION WORKS FINE!

The app doesn't use this file at all.
You just won't be able to run the simple tests.
```

---

## Do You Need All These Files?

### For Production (Real Users):
```
✅ app/services/guardrails.py     (REQUIRED)
❌ test_guardrails.py              (Delete it)
❌ test_guardrails_simple.py       (Delete it)
```

### For Development (Testing):
```
✅ app/services/guardrails.py     (REQUIRED)
✅ test_guardrails.py              (Keep for testing)
✅ test_guardrails_simple.py       (Keep for quick tests)
```

---

## How to Test Guardrails

### Method 1: Use the Web Interface (No test files needed)

1. Start server: `uvicorn main:app`
2. Open browser: `http://localhost:8000`
3. Upload a document
4. Try these queries:

**Safe query (should work):**
```
"What is this document about?"
→ Gets answer ✅
```

**Sensitive query (should be blocked):**
```
"What are the passwords in this document?"
→ Error: "This request cannot be completed due to policy restrictions." ❌
```

### Method 2: Use test_guardrails_simple.py

```bash
python test_guardrails_simple.py
```

### Method 3: Use test_guardrails.py

```bash
# Terminal 1: Start server
uvicorn main:app

# Terminal 2: Run tests
python test_guardrails.py
```

---

## Summary Table

| File | Required? | Purpose | Can Delete? |
|------|-----------|---------|-------------|
| `app/services/guardrails.py` | ✅ YES | Actual security implementation | ❌ NO |
| `test_guardrails.py` | ⚠️ NO | Test via API endpoints | ✅ YES |
| `test_guardrails_simple.py` | ⚠️ NO | Test without server | ✅ YES |

---

## Key Takeaway

**Think of it like a car:**

- `app/services/guardrails.py` = **The actual brakes** (required to drive safely)
- `test_guardrails.py` = **Brake test equipment** (nice to have, but not needed to drive)
- `test_guardrails_simple.py` = **Simple brake checker** (nice to have, but not needed to drive)

You need the brakes, but you don't need the test equipment to drive the car!

---

## Recommendation

**For your project:**

1. **Keep** `app/services/guardrails.py` - This is essential security
2. **Keep** the test files during development - Useful for validating security
3. **Delete** the test files before production deployment - They're not needed

**Or just leave them!** They're small files and don't hurt anything. They're just sitting there unused.

---

Hope this clears up the confusion! 😊
