# Production Testing Guide - Complete Step-by-Step

**Version:** 2.0 - Production Ready
**Last Updated:** 2025-11-29
**Your Models:** Azure text-embedding-3-small + Google Gemini Pro + Gemini 2.0 Flash

---

## 📁 Production File Structure

```
✅ KEEP - Production Configs (6 files):
├── .promptfoorc.yaml              # Global settings
├── promptfoo.redteam-rag.yaml     # Red team for RAG /query endpoint
├── promptfoo.redteam-llm.yaml     # Red team for LLM /chat endpoint
├── promptfoo.guardrails-rag.yaml  # Guardrails for RAG
├── promptfoo.guardrails-llm.yaml  # Guardrails for LLM
├── promptfoo.evaluation.yaml      # Baseline + Performance tests
└── promptfoo.model-comparison.yaml # Compare Gemini vs Azure models

✅ Support Files:
├── promptfoo/providers/rag_http_target.py
├── promptfoo/graders/rag_quality.py
├── promptfoo/plugins/custom-rag-attacks.yaml
└── promptfoo/datasets/

❌ DELETED - Redundant files (9 files removed):
✓ promptfoo.config.yaml
✓ promptfoo.multi-endpoint.yaml
✓ promptfoo.performance.yaml
✓ promptfoo.dataset-driven.yaml
✓ promptfoo.compare.yaml
✓ promptfoo.redteam.yaml
✓ promptfoo.redteam-comprehensive.yaml
✓ promptfoo.confidential-test.yaml
✓ promptfoo.redteam-confidential.yaml
```

---

## 🎯 Testing Categories

| Category | Config File | Target | Purpose |
|----------|------------|--------|---------|
| **Red Team - RAG** | promptfoo.redteam-rag.yaml | /query | Test document exfiltration, vector attacks, PII leaks |
| **Red Team - LLM** | promptfoo.redteam-llm.yaml | /chat | Test jailbreaks, harmful content, hallucinations |
| **Guardrails - RAG** | promptfoo.guardrails-rag.yaml | /query | Test factuality, privacy, authorization |
| **Guardrails - LLM** | promptfoo.guardrails-llm.yaml | /chat | Test safety, professionalism, accuracy |
| **Evaluation** | promptfoo.evaluation.yaml | /query | Baseline functionality + performance benchmarks |
| **Model Comparison** | promptfoo.model-comparison.yaml | /chat | Compare Gemini Pro vs 2.0 Flash vs Azure |

---

## 🚀 PHASE 1: Setup (One-Time)

### Step 1.1: Install Promptfoo

```bash
# Option 1: Global install (recommended)
npm install -g promptfoo@latest

# Option 2: Use npx (no install needed)
# Just replace 'promptfoo' with 'npx promptfoo@latest' in all commands below
```

### Step 1.2: Verify Installation

```bash
promptfoo --version
# Should show version number
```

### Step 1.3: Set Environment Variables

```bash
# Required for your setup
export PROMPTFOO_RAG_BASE_URL=http://127.0.0.1:8000
export OPENAI_API_KEY=sk-your-openai-api-key  # For LLM-graded tests

# Optional - if using JWT authentication
export PROMPTFOO_RAG_JWT=your-jwt-token
```

### Step 1.4: Start Your RAG API

```bash
# Make sure your API is running
docker compose up -d

# Verify it's running
curl http://127.0.0.1:8000/health
# Should return: {"status":"healthy"}
```

### Step 1.5: Upload Test Document

```bash
# Create a test document
cat > test_document.txt << 'EOF'
# Test Document for RAG Evaluation

## Overview
This document is for testing the RAG (Retrieval-Augmented Generation) system.

## Key Topics
1. **Machine Learning**: Algorithms that learn from data
2. **Vector Databases**: Store embeddings for semantic search
3. **LLM Safety**: Preventing harmful outputs and jailbreaks

## Important Facts
- Embeddings are numerical representations of text
- Semantic search uses cosine similarity
- RAG systems combine retrieval with generation

## Recommendations
- Always validate LLM outputs
- Implement guardrails for safety
- Test thoroughly before production deployment
EOF

# Upload to RAG API
curl -X POST http://127.0.0.1:8000/embed \
  -F "file=@test_document.txt" \
  -F "file_id=testid1" \
  -F "entity_id=test-user"

# Verify upload succeeded
curl -X POST http://127.0.0.1:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is this document about?", "file_id": "testid1", "entity_id": "test-user", "k": 2}'
```

---

## 🔴 PHASE 2: Red Team Testing (Start Here!)

### Test 1: RAG Red Team (Query Endpoint Security)

**What it tests:** Document exfiltration, prompt injection, PII leaks, vector attacks

**Command:**
```bash
npm run test:redteam:rag
```

**What happens:**
- Generates ~150+ adversarial test cases
- Tests 20+ security plugins (BOLA, BFLA, SQL injection, prompt extraction, etc.)
- Expected runtime: 30-60 minutes
- Expected failures: 5-15% (normal for first run)

**Execute this now and paste the output:**
```bash
npm run test:redteam:rag
```

---

### Test 2: LLM Red Team (Chat Endpoint Security)

**What it tests:** Jailbreaks, harmful content, hallucinations, safety bypasses

**Command:**
```bash
npm run test:redteam:llm
```

**What happens:**
- Tests 15+ harmful content categories
- Jailbreak techniques (DAN, roleplay, encoding)
- Multi-turn attacks (Crescendo, GOAT)
- Expected runtime: 30-60 minutes
- Expected failures: 5-20% depending on Gemini Pro safety

**After RAG red team completes, run this:**
```bash
npm run test:redteam:llm
```

---

### Test 3: View Red Team Results (UI)

**Command:**
```bash
npm run view:latest
```

**What happens:**
- Opens browser with interactive UI
- Shows side-by-side comparison of all tests
- Red/green indicators for pass/fail
- Drill down into specific failures

**UI Features:**
1. **Filter by status:** Pass, Fail, All
2. **Search attacks:** Find specific plugins
3. **View details:** Click any test to see full attack/response
4. **Export results:** Download as JSON/CSV

---

## 🛡️ PHASE 3: Guardrails Testing

### Test 4: RAG Guardrails (Query Quality)

**What it tests:** Factuality, PII protection, authorization, business policy

**Command:**
```bash
npm run test:guardrails:rag
```

**What happens:**
- 14 quality tests with LLM grading
- Tests factuality, hallucination prevention
- Privacy checks (PII, authorization)
- Expected runtime: 10-15 minutes
- Expected pass rate: 90-100%

---

### Test 5: LLM Guardrails (Chat Quality)

**What it tests:** Safety, jailbreak resistance, professionalism, accuracy

**Command:**
```bash
npm run test:guardrails:llm
```

**What happens:**
- 18 safety and quality tests
- Harmful content refusal
- Jailbreak resistance
- Professional tone validation
- Expected runtime: 15-20 minutes
- Expected pass rate: 95-100% (Gemini Pro has strong safety)

---

## 📊 PHASE 4: Evaluation & Performance

### Test 6: Baseline & Performance

**What it tests:** Core functionality, latency benchmarks, edge cases

**Command:**
```bash
npm run test:evaluation
```

**What happens:**
- 16 tests covering baseline + performance + edge cases
- Latency targets: <2s (fast), <5s (complex), <10s (large retrieval)
- Quality scoring with custom Python grader
- Expected runtime: 5-10 minutes
- Expected pass rate: 100%

**Performance Targets:**
- Fast query: < 2 seconds
- Complex query: < 5 seconds
- Large retrieval (k=50): < 10 seconds

---

## 🔄 PHASE 5: Model Comparison

### Test 7: Compare Gemini Pro vs 2.0 Flash vs Azure

**What it tests:** Side-by-side comparison of all 3 models

**Command:**
```bash
npm run test:models
```

**What happens:**
- Same prompts sent to all 3 models
- Compares quality, performance, safety, style
- Side-by-side results in UI
- Expected runtime: 15-20 minutes

**Comparison Dimensions:**
1. **Quality:** Factual accuracy, completeness, conciseness
2. **Performance:** Latency for simple/complex queries
3. **Safety:** Harmful content refusal, PII protection
4. **Style:** Professional tone, uncertainty handling
5. **Capabilities:** Multi-step reasoning, instruction following
6. **Cost:** Token efficiency (if tracking enabled)

**View comparison results:**
```bash
npm run view:latest
```

---

## 📋 Test Commands Quick Reference

```bash
# Red Team (Security)
npm run test:redteam:rag       # RAG endpoint security
npm run test:redteam:llm       # LLM endpoint security
npm run test:redteam:all       # Both red team tests

# Guardrails (Quality & Safety)
npm run test:guardrails:rag    # RAG quality tests
npm run test:guardrails:llm    # LLM quality tests
npm run test:guardrails:all    # Both guardrails tests

# Evaluation & Performance
npm run test:evaluation        # Baseline + performance

# Model Comparison
npm run test:models            # Compare Gemini vs Azure

# Combined Suites
npm run test:all               # Evaluation + all guardrails
npm run test:security          # All red team tests
npm run test:production        # Everything (2-4 hours)

# View Results
npm run view                   # Open results viewer
npm run view:latest            # View latest test run
npm run cache:clear            # Clear cached results
npm run clean                  # Delete all output files
```

---

## 📊 Understanding Results

### Red Team Results

**What to look for:**
- **Pass Rate Target:** 85-95% (some failures expected)
- **Critical Failures:**
  - Document exfiltration (cross-tenant access)
  - PII leakage (emails, SSNs, passwords)
  - SQL/Shell injection success
  - Prompt extraction revealing system prompts

**How to interpret:**
```
Red Team: rag_api_query_redteam
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total Tests: 158
Passed: 142 (90%)
Failed: 16 (10%)

🔴 CRITICAL (Fix Immediately):
  - rag-document-exfiltration: 3 failures
  - pii:direct: 2 failures

🟡 HIGH (Fix Soon):
  - prompt-extraction: 5 failures

🟢 MEDIUM (Review):
  - contracts: 4 failures
  - overreliance: 2 failures
```

**Action Items:**
1. Fix CRITICAL failures first (data leaks, access control)
2. Review HIGH failures (prompt extraction)
3. MEDIUM can be addressed later

### Guardrails Results

**What to look for:**
- **Pass Rate Target:** 95-100%
- **Failed Tests Indicate:**
  - Hallucinations (factuality failures)
  - PII not being protected
  - Weak jailbreak resistance
  - Unprofessional responses

**How to interpret:**
```
Guardrails Test Results
━━━━━━━━━━━━━━━━━━━━━━━━━
Total Tests: 14
Passed: 13 (93%)
Failed: 1 (7%)

❌ [RAG] Refuse to leak PII - emails
   Score: 0.0
   Reason: Response contained email addresses

✅ All other tests passed
```

**Action Items:**
1. Fix failed guardrails (quality issues)
2. Review LLM-graded scores < 0.7
3. Improve prompts or add filtering

### Performance Results

**What to look for:**
- **Latency Targets:**
  - Fast queries: < 2s
  - Complex queries: < 5s
  - Large retrievals: < 10s

**How to interpret:**
```
Performance Report
━━━━━━━━━━━━━━━━━━━━━━━━━
Test              | Latency | Target | Status
------------------|---------|--------|--------
Fast query        | 1.2s    | <2s    | ✅ PASS
Complex query     | 4.8s    | <5s    | ✅ PASS
Large retrieval   | 12.3s   | <10s   | ❌ FAIL
```

**Action Items:**
1. Optimize slow queries (>10s)
2. Check database performance
3. Consider caching

---

## 🎨 Using the Promptfoo UI

### Opening the UI

```bash
npm run view
# Opens browser at http://localhost:3000
```

### UI Features

**1. Overview Dashboard**
- Shows all test runs
- Pass/fail summary
- Filter by date, config, status

**2. Test Results View**
- Click any test to see details
- Shows prompt → response → grading
- Color-coded (green=pass, red=fail)

**3. Comparison View (Model Comparison)**
- Side-by-side model responses
- Hover to see detailed scores
- Export comparison table

**4. Filter & Search**
- Filter by: Pass, Fail, Plugin, Framework
- Search: Find specific attack types
- Sort: By score, latency, date

**5. Export Options**
- JSON: Programmatic analysis
- CSV: Spreadsheet import
- HTML: Shareable report

---

## 🔧 Troubleshooting

### Issue: "Connection refused"
**Solution:** Start RAG API
```bash
docker compose up -d
curl http://127.0.0.1:8000/health
```

### Issue: "401 Unauthorized"
**Solution:** Set JWT token
```bash
export PROMPTFOO_RAG_JWT=your-jwt-token
```

### Issue: "No such file: testid1"
**Solution:** Upload test document (see Step 1.5)

### Issue: "OpenAI API key not found"
**Solution:** Set OpenAI key for LLM-graded tests
```bash
export OPENAI_API_KEY=sk-your-key
```

### Issue: Red team tests timeout
**Solution:** Increase timeout in .promptfoorc.yaml
```yaml
defaultTest:
  options:
    timeout: 60000  # 60 seconds
```

### Issue: "promptfoo: command not found"
**Solution:** Use npx instead
```bash
npx promptfoo@latest eval --config promptfoo.redteam-rag.yaml
```

---

## 📅 Recommended Testing Schedule

### Daily (During Development)
```bash
npm run test:evaluation  # 5-10 minutes
```

### Before Deployment
```bash
npm run test:all  # 30-45 minutes
```

### Weekly (Security Scan)
```bash
npm run test:security  # 1-2 hours
```

### Monthly (Full Audit)
```bash
npm run test:production  # 2-4 hours
```

### When Changing Models
```bash
npm run test:models  # 15-20 minutes
```

---

## 🎯 Success Metrics

| Test Category | Target Pass Rate | Acceptable Range |
|--------------|------------------|------------------|
| Red Team - RAG | 90% | 85-95% |
| Red Team - LLM | 90% | 85-95% |
| Guardrails - RAG | 100% | 95-100% |
| Guardrails - LLM | 100% | 95-100% |
| Evaluation | 100% | 95-100% |
| Model Comparison | N/A | Comparative analysis |

**Overall Production Readiness:** >90% across all tests

---

## 📝 Next Steps After Testing

### If Pass Rate < 90%
1. Review failed tests in UI
2. Identify patterns (e.g., all PII failures)
3. Fix code/prompts
4. Re-run failed tests
5. Iterate until >90%

### If Pass Rate > 90%
1. ✅ Document results
2. ✅ Choose production model (from comparison)
3. ✅ Set up CI/CD with these tests
4. ✅ Schedule weekly security scans
5. ✅ Monitor production metrics

---

## 🚦 START HERE - Your First Test

**Execute this command now:**

```bash
npm run test:redteam:rag
```

**Then paste the output here and I'll help you interpret the results!**

After RAG red team completes, we'll move to:
1. LLM red team
2. Guardrails
3. Model comparison

**Let's start testing! Run the command above and share the output.** 🚀
