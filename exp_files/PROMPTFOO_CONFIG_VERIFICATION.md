# Promptfoo Configuration Verification Report

## Executive Summary

**Total Config Files:** 11
**Files with Issues:** 5
**Files OK:** 6
**Critical Issues:** 3
**Warnings:** 7

---

## Configuration Files Status

### ✅ Files Without Issues

1. **promptfoo.config.yaml** - Baseline tests ✓
2. **promptfoo.multi-endpoint.yaml** - Multi-endpoint tests ✓
3. **promptfoo.compare.yaml** - A/B comparison tests ✓
4. **promptfoo.redteam.yaml** - Focused red team ✓
5. **promptfoo.redteam-comprehensive.yaml** - Comprehensive red team ✓
6. **.promptfoorc.yaml** - Global configuration ✓

### ⚠️ Files with Minor Issues (Warnings)

#### 1. promptfoo.guardrails.yaml
**Issues:**
- Line 39, 56, 65, 78, 85, 101, 112, 124: Using `metric:` instead of `type:`
- Promptfoo uses `type:` for assertion types in newer versions

**Impact:** Low - `metric:` is deprecated but still works
**Fix:** Change all `metric:` to `type:`

#### 2. promptfoo.performance.yaml
**Issues:**
- Line 82: Using `metric:` instead of `type:`
- Line 46: Missing `file_id` and `entity_id` in vars for k=10 test

**Impact:** Low - Minor inconsistency
**Fix:**
- Change `metric:` to `type:`
- Add missing vars in defaultTest

#### 3. promptfoo.dataset-driven.yaml
**Issues:**
- Not using custom grader despite having one available
- Missing edge cases from edge_cases.yaml dataset

**Impact:** Medium - Missing quality scoring
**Fix:** Add custom grader reference and edge cases

### 🔴 Files with Critical Issues

#### 1. promptfoo.confidential-test.yaml
**Critical Issues:**
- Line 30-36, 38-52, 54-76, etc: Using `assert:` instead of `assertions:`
- Promptfoo requires `assertions:` (plural) at test level
- Using deprecated syntax `vars:` under tests without proper structure

**Impact:** HIGH - Config will fail to run
**Fix:** Rewrite with correct `assertions:` syntax

#### 2. promptfoo.redteam-confidential.yaml
**Critical Issues:**
- Line 61: Plugin `pii-direct` should be `pii:direct`
- Line 70: Plugin `pii-social-engineering` doesn't exist (should be `pii:social`)
- Line 187-197: `purpose` should be a single string, not a list
- Line 200-264: `assertions` cannot be defined at root level in redteam config

**Impact:** HIGH - Invalid plugin names will cause failures
**Fix:** Correct plugin names and structure

---

## Detailed Issues and Corrections

### Issue 1: `metric:` vs `type:` in Assertions

**Files Affected:**
- promptfoo.guardrails.yaml
- promptfoo.performance.yaml

**Problem:**
```yaml
# ❌ Deprecated syntax
assertions:
  - metric: llm-rubric
    value: "..."
```

**Solution:**
```yaml
# ✅ Correct syntax
assertions:
  - type: llm-rubric
    value: "..."
```

**Why:** Promptfoo v0.80+ uses `type:` for all assertion types. `metric:` is backward compatible but deprecated.

---

### Issue 2: `assert:` vs `assertions:`

**Files Affected:**
- promptfoo.confidential-test.yaml

**Problem:**
```yaml
# ❌ Wrong syntax
tests:
  - vars:
      query: "..."
    assert:  # Should be 'assertions'
      - type: not-contains
```

**Solution:**
```yaml
# ✅ Correct syntax
tests:
  - vars:
      query: "..."
    assertions:  # Plural
      - type: not-contains
```

---

### Issue 3: Invalid Plugin Names

**Files Affected:**
- promptfoo.redteam-confidential.yaml

**Invalid Plugin Names:**
- `pii-direct` → Should be `pii:direct`
- `pii-social-engineering` → Should be `pii:social`
- `pii-session` → Should be `pii:session`

**Valid Plugin Reference:**
https://www.promptfoo.dev/docs/red-team/plugins/

**Correct Plugin Names:**
```yaml
plugins:
  - pii:direct
  - pii:social
  - pii:session
  - pii:api-db
  - prompt-extraction
  - sql-injection
  - shell-injection
  - ssrf
  - bola
  - bfla
  - rbac
  - excessive-agency
  - hallucination
  - competitors
  - contracts
  - debug-access
  - indirect-prompt-injection
```

---

### Issue 4: RedTeam Config Structure

**Problem:**
```yaml
# ❌ Wrong - assertions at root level
redteam:
  plugins:
    - pii:direct

assertions:  # This is invalid in redteam configs
  - type: not-contains
```

**Solution:**
```yaml
# ✅ Correct - use plugin config or grading instructions
redteam:
  plugins:
    - id: pii:direct
      config:
        # Plugin-specific config

  # Use purpose and grading instructions instead
  purpose: |
    Test if system leaks PII...
```

---

### Issue 5: Custom Provider Path

**Files Affected:**
- promptfoo.confidential-test.yaml
- promptfoo.redteam-confidential.yaml

**Problem:**
```yaml
# Current
providers:
  - id: "python:./promptfoo/providers/rag_http_target.py"
```

**Verification Needed:**
The provider exists and is executable, but should use `file://` protocol:

**Solution:**
```yaml
# ✅ Better syntax
providers:
  - id: file://promptfoo/providers/rag_http_target.py
    label: "RAG Query Endpoint"
```

---

## Files Requiring Corrections

### High Priority (Must Fix Before Testing)

1. **promptfoo.confidential-test.yaml** - Rewrite with correct assertions syntax
2. **promptfoo.redteam-confidential.yaml** - Fix plugin names and structure

### Medium Priority (Should Fix)

3. **promptfoo.guardrails.yaml** - Change `metric:` to `type:`
4. **promptfoo.performance.yaml** - Fix metric/type and add missing vars
5. **promptfoo.dataset-driven.yaml** - Add custom grader

---

## Verification Checklist

Before running tests, verify:

- [ ] All config files use `assertions:` (plural) not `assert:`
- [ ] All assertions use `type:` not `metric:`
- [ ] All plugin names use correct format (`pii:direct` not `pii-direct`)
- [ ] Custom providers use `file://` protocol
- [ ] Red team configs don't have root-level `assertions:`
- [ ] All referenced files exist:
  - [ ] promptfoo/providers/rag_http_target.py ✓
  - [ ] promptfoo/graders/rag_quality.py ✓
  - [ ] promptfoo/datasets/sample_queries.csv ✓
  - [ ] promptfoo/datasets/edge_cases.yaml ✓
  - [ ] promptfoo/plugins/custom-rag-attacks.yaml ✓

---

## Testing Commands (After Fixes)

```bash
# Test individual configs for syntax errors
npx promptfoo@latest eval --config promptfoo.config.yaml --dry-run
npx promptfoo@latest eval --config promptfoo.guardrails.yaml --dry-run
npx promptfoo@latest redteam run --config promptfoo.redteam.yaml --dry-run

# If any fail, check:
# 1. YAML syntax (use yamllint or online validator)
# 2. Plugin names (check promptfoo docs)
# 3. Provider paths (must exist and be executable)
```

---

## Recommended Test Order

After fixing all issues:

1. **Start Simple:**
   ```bash
   npm run test:baseline
   ```

2. **Add Complexity:**
   ```bash
   npm run test:guardrails
   npm run test:performance
   ```

3. **Security Testing:**
   ```bash
   npm run test:redteam
   npm run test:redteam:full
   ```

4. **Custom Tests:**
   ```bash
   npx promptfoo eval --config promptfoo.confidential-test.yaml
   ```

---

## Next Steps

1. ✅ Fix critical issues in confidential-test and redteam-confidential configs
2. ✅ Update metric → type in guardrails and performance configs
3. ✅ Add custom grader to dataset-driven config
4. ✅ Test each config with --dry-run flag
5. ✅ Upload test documents to RAG API
6. ✅ Run baseline tests first
7. ✅ Proceed with full test suite

---

## Summary of Corrections Needed

| File | Issues | Priority | Status |
|------|--------|----------|--------|
| promptfoo.config.yaml | None | - | ✅ Ready |
| promptfoo.multi-endpoint.yaml | None | - | ✅ Ready |
| promptfoo.guardrails.yaml | metric→type | Medium | ⚠️ Needs fix |
| promptfoo.performance.yaml | metric→type, missing vars | Medium | ⚠️ Needs fix |
| promptfoo.dataset-driven.yaml | Missing grader | Low | ⚠️ Could improve |
| promptfoo.compare.yaml | None | - | ✅ Ready |
| promptfoo.redteam.yaml | None | - | ✅ Ready |
| promptfoo.redteam-comprehensive.yaml | None | - | ✅ Ready |
| promptfoo.confidential-test.yaml | assert→assertions | High | 🔴 Must fix |
| promptfoo.redteam-confidential.yaml | Plugin names, structure | High | 🔴 Must fix |
| .promptfoorc.yaml | None | - | ✅ Ready |

**Files Ready to Use:** 6/11 (55%)
**Files Need Minor Fixes:** 3/11 (27%)
**Files Need Major Fixes:** 2/11 (18%)
