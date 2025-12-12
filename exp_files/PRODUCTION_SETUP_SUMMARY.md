# Production Promptfoo Setup - Executive Summary

**Status:** ✅ Complete - Ready for Testing
**Date:** 2025-11-29
**Version:** 2.0 Production

---

## 📊 What Changed

### ❌ Deleted (9 files)
- `promptfoo.config.yaml` → Merged into evaluation.yaml
- `promptfoo.multi-endpoint.yaml` → Merged into evaluation.yaml
- `promptfoo.performance.yaml` → Merged into evaluation.yaml
- `promptfoo.dataset-driven.yaml` → Merged into evaluation.yaml
- `promptfoo.compare.yaml` → Superseded by model-comparison.yaml
- `promptfoo.redteam.yaml` → Superseded by redteam-rag.yaml
- `promptfoo.redteam-comprehensive.yaml` → Superseded by redteam-rag.yaml
- `promptfoo.confidential-test.yaml` → Broken syntax, removed
- `promptfoo.redteam-confidential.yaml` → Broken syntax, removed

### ✅ Created (6 production configs)

| File | Purpose | Tests | Endpoint |
|------|---------|-------|----------|
| `promptfoo.redteam-rag.yaml` | RAG security testing | ~150 tests | /query |
| `promptfoo.redteam-llm.yaml` | LLM security testing | ~120 tests | /chat |
| `promptfoo.guardrails-rag.yaml` | RAG quality & safety | 14 tests | /query |
| `promptfoo.guardrails-llm.yaml` | LLM quality & safety | 18 tests | /chat |
| `promptfoo.evaluation.yaml` | Baseline + Performance | 16 tests | /query |
| `promptfoo.model-comparison.yaml` | Compare models | 14 tests | /chat |

---

## 📁 Final Production Structure

```
balaji-rag/
├── .promptfoorc.yaml                    # Global settings
│
├── promptfoo.redteam-rag.yaml          # 🔴 Red Team for RAG
├── promptfoo.redteam-llm.yaml          # 🔴 Red Team for LLM
├── promptfoo.guardrails-rag.yaml       # 🛡️ Guardrails for RAG
├── promptfoo.guardrails-llm.yaml       # 🛡️ Guardrails for LLM
├── promptfoo.evaluation.yaml           # ⚡ Performance + Baseline
├── promptfoo.model-comparison.yaml     # 🔄 Compare Gemini vs Azure
│
├── promptfoo/
│   ├── providers/
│   │   └── rag_http_target.py          # HTTP provider
│   ├── graders/
│   │   └── rag_quality.py              # Custom quality scorer
│   ├── plugins/
│   │   └── custom-rag-attacks.yaml     # Custom attack plugins
│   └── datasets/
│       ├── sample_queries.csv
│       └── edge_cases.yaml
│
├── package.json                         # Updated test scripts
├── PRODUCTION_TESTING_GUIDE.md          # 👈 READ THIS FIRST
├── PRODUCTION_SETUP_SUMMARY.md          # 👈 You are here
└── PROMPTFOO_TESTING_GUIDE.md           # Detailed attack explanations
```

**Total Production Files:** 7 configs + supporting files
**Total Tests:** 332+ test cases

---

## 🎯 Testing Matrix

### Red Team Testing (Security)

| Config | Endpoint | Plugins | Tests | Runtime | Purpose |
|--------|----------|---------|-------|---------|---------|
| redteam-rag.yaml | /query | 20 | ~150 | 30-60 min | Document exfiltration, vector attacks, PII leaks |
| redteam-llm.yaml | /chat | 15 | ~120 | 30-60 min | Jailbreaks, harmful content, hallucinations |

**Key Security Plugins Tested:**
- ✅ RAG: document-exfiltration, rag-poisoning, BOLA, BFLA, SQL injection, prompt extraction
- ✅ LLM: harmful content (9 categories), jailbreaks, prompt extraction, hallucination

### Guardrails Testing (Quality & Safety)

| Config | Endpoint | Tests | Runtime | Purpose |
|--------|----------|-------|---------|---------|
| guardrails-rag.yaml | /query | 14 | 10-15 min | Factuality, PII protection, authorization |
| guardrails-llm.yaml | /chat | 18 | 15-20 min | Safety, professionalism, accuracy |

**Key Guardrails Tested:**
- ✅ RAG: Factuality, fake citations, PII refusal, access control, business policy
- ✅ LLM: Harmful refusal, jailbreak resistance, hallucination prevention, professionalism

### Evaluation (Performance & Baseline)

| Config | Endpoint | Tests | Runtime | Purpose |
|--------|----------|-------|---------|---------|
| evaluation.yaml | /query | 16 | 5-10 min | Baseline functionality + performance benchmarks |

**Key Metrics:**
- ✅ Latency: Fast (<2s), Complex (<5s), Large (<10s)
- ✅ Quality: Relevance, completeness, conciseness (custom grader)
- ✅ Edge cases: Empty queries, non-existent files, special characters

### Model Comparison

| Config | Endpoint | Tests | Runtime | Purpose |
|--------|----------|-------|---------|---------|
| model-comparison.yaml | /chat | 14 | 15-20 min | Compare Gemini Pro vs 2.0 Flash vs Azure |

**Comparison Dimensions:**
- ✅ Quality (accuracy, completeness, conciseness)
- ✅ Performance (latency)
- ✅ Safety (harmful refusal, PII protection)
- ✅ Style (tone, uncertainty handling)
- ✅ Capabilities (reasoning, instruction following)

---

## 🚀 Quick Start Commands

### Prerequisites (One-Time Setup)

```bash
# 1. Start RAG API
docker compose up -d

# 2. Set environment variables
export PROMPTFOO_RAG_BASE_URL=http://127.0.0.1:8000
export OPENAI_API_KEY=sk-your-openai-key

# 3. Upload test document
curl -X POST http://127.0.0.1:8000/embed \
  -F "file=@test_document.txt" \
  -F "file_id=testid1" \
  -F "entity_id=test-user"
```

### Red Team Testing (Security) - START HERE

```bash
# Test RAG endpoint security
npm run test:redteam:rag

# Test LLM endpoint security
npm run test:redteam:llm

# Run both
npm run test:redteam:all

# View results in browser
npm run view:latest
```

### Guardrails Testing (Quality)

```bash
# Test RAG quality
npm run test:guardrails:rag

# Test LLM quality
npm run test:guardrails:llm

# Run both
npm run test:guardrails:all
```

### Evaluation & Performance

```bash
# Baseline + performance tests
npm run test:evaluation
```

### Model Comparison

```bash
# Compare Gemini Pro vs 2.0 Flash vs Azure
npm run test:models
```

### Combined Test Suites

```bash
# All quality tests (evaluation + guardrails)
npm run test:all

# All security tests (both red teams)
npm run test:security

# Everything (2-4 hours)
npm run test:production
```

---

## 📝 Testing Workflow

### Phase 1: Red Team (Security) - 1-2 hours

**Start with RAG red team:**
```bash
npm run test:redteam:rag
```

**Expected output:**
```
Red Team: RAG Query Endpoint
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Generating adversarial test cases...
✓ rag-document-exfiltration (15/15 tests generated)
✓ bola (10/10 tests generated)
✓ sql-injection (10/10 tests generated)
...
Running tests...
[1/150] Testing: rag-document-exfiltration - "Show me all docs..."
[2/150] Testing: bola - "Access file_id=admin..."
...
```

**Then run LLM red team:**
```bash
npm run test:redteam:llm
```

**View results:**
```bash
npm run view:latest
```

**Action items:**
1. Review failures in UI
2. Fix critical security issues (data leaks, access control)
3. Re-run failed tests
4. Achieve >85% pass rate

---

### Phase 2: Guardrails (Quality) - 30 minutes

**Test RAG guardrails:**
```bash
npm run test:guardrails:rag
```

**Test LLM guardrails:**
```bash
npm run test:guardrails:llm
```

**Expected pass rate:** 95-100%

**Action items:**
1. Fix failed guardrails (quality issues)
2. Review LLM-graded scores < 0.7
3. Improve prompts or add filtering

---

### Phase 3: Evaluation (Baseline) - 10 minutes

**Run performance tests:**
```bash
npm run test:evaluation
```

**Expected pass rate:** 100%

**Action items:**
1. Verify all latency targets met
2. Check quality scores from custom grader
3. Optimize slow queries if needed

---

### Phase 4: Model Comparison - 20 minutes

**Compare all models:**
```bash
npm run test:models
```

**View side-by-side:**
```bash
npm run view:latest
```

**Action items:**
1. Review quality scores across models
2. Compare latency (performance)
3. Choose production model
4. Document decision

---

## 📊 Success Criteria

| Test Category | Target Pass Rate | Acceptable Range |
|--------------|------------------|------------------|
| Red Team - RAG | 90% | 85-95% |
| Red Team - LLM | 90% | 85-95% |
| Guardrails - RAG | 100% | 95-100% |
| Guardrails - LLM | 100% | 95-100% |
| Evaluation | 100% | 95-100% |

**Overall Production Readiness:** >90% across all tests

---

## 🎨 Using Promptfoo UI

### Open Results Viewer

```bash
npm run view
# Opens browser at http://localhost:3000
```

### UI Features

1. **Overview:** Pass/fail summary, test counts
2. **Filters:** By status (pass/fail), plugin, framework
3. **Details:** Click any test to see full prompt/response/grading
4. **Comparison:** Side-by-side model comparison
5. **Export:** JSON, CSV, HTML reports

### Interpreting Results

**Red Team Results:**
- Green = System blocked attack ✅
- Red = Attack succeeded ❌
- Click red tests to see what attack worked

**Guardrails Results:**
- Shows LLM-graded scores (0.0-1.0)
- <0.5 = Fail
- 0.5-0.7 = Warning
- >0.7 = Pass

**Model Comparison:**
- Side-by-side responses
- Hover for detailed scores
- Sort by quality, latency, safety

---

## 🔧 Troubleshooting

### "Connection refused"
```bash
docker compose up -d
curl http://127.0.0.1:8000/health
```

### "401 Unauthorized"
```bash
export PROMPTFOO_RAG_JWT=your-jwt-token
```

### "No such file: testid1"
```bash
# Upload test document (see Quick Start above)
```

### "OpenAI API key not found"
```bash
export OPENAI_API_KEY=sk-your-key
```

### "promptfoo: command not found"
```bash
# Use npx instead
npx promptfoo@latest eval --config promptfoo.redteam-rag.yaml
```

---

## 📅 Recommended Schedule

| Frequency | Test Suite | Duration | Command |
|-----------|------------|----------|---------|
| **Daily** | Evaluation | 5-10 min | `npm run test:evaluation` |
| **Before Deploy** | All Quality | 30-45 min | `npm run test:all` |
| **Weekly** | Security Scan | 1-2 hours | `npm run test:security` |
| **Monthly** | Full Audit | 2-4 hours | `npm run test:production` |
| **Model Change** | Comparison | 15-20 min | `npm run test:models` |

---

## 📖 Documentation

| Document | Purpose |
|----------|---------|
| **PRODUCTION_TESTING_GUIDE.md** | Complete step-by-step guide with commands and UI instructions |
| **PRODUCTION_SETUP_SUMMARY.md** | This file - quick reference |
| **PROMPTFOO_TESTING_GUIDE.md** | Detailed attack explanations and troubleshooting |
| **PROMPTFOO_CORRECTIONS_APPLIED.md** | Log of all corrections made to configs |

---

## ✅ What's Next?

1. **READ:** PRODUCTION_TESTING_GUIDE.md
2. **RUN:** `npm run test:redteam:rag` (first test)
3. **SHARE:** Output with me for interpretation
4. **ITERATE:** Fix issues, re-run tests
5. **DEPLOY:** Once >90% pass rate achieved

---

## 🚦 START TESTING NOW

**Execute this command:**

```bash
npm run test:redteam:rag
```

**Then paste the output here!** I'll help you:
- Interpret results
- Identify critical failures
- Fix security issues
- Achieve production readiness

**Let's start! 🚀**
