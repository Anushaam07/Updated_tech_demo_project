# Promptfoo Reusable Integration Guide

## 🎯 Overview

This guide explains how to implement the comprehensive Promptfoo testing framework used in this RAG application into **any other application**. The framework provides automated testing, security scanning, quality assurance, and performance benchmarking.

---

## 📦 What You Get

When you implement this Promptfoo integration, you'll have:

- ✅ **8 Test Configurations** covering evaluation, security, performance, and quality
- ✅ **Custom Providers** for testing your specific endpoints
- ✅ **Custom Graders** for domain-specific quality metrics
- ✅ **Security Testing** with OWASP/NIST/MITRE compliance
- ✅ **CI/CD Integration** with GitHub Actions
- ✅ **NPM Scripts** for easy test execution
- ✅ **Comprehensive Documentation**

---

## 🚀 Quick Start for Any Application

### Step 1: Install Promptfoo

```bash
npm install --save-dev promptfoo@latest
# or globally
npm install -g promptfoo@latest
```

### Step 2: Copy Core Files

Copy these files from this project to your project:

```
your-project/
├── .promptfoorc.yaml              # Global configuration
├── package.json                    # NPM scripts (merge with yours)
├── promptfoo/
│   ├── README.md                   # Testing documentation
│   ├── providers/                  # Custom providers for your API
│   ├── graders/                    # Custom quality graders
│   ├── plugins/                    # Custom security plugins
│   └── datasets/                   # Test datasets
```

### Step 3: Customize for Your Application

#### A. Update Provider Files

Edit `promptfoo/providers/*.py` to match your API endpoints:

```python
# Example: promptfoo/providers/your_api_target.py
import os
import requests

def call_api(prompt, options, context):
    """Call your API endpoint."""
    base_url = os.getenv("YOUR_API_BASE_URL", "http://localhost:8000")

    response = requests.post(
        f"{base_url}/your-endpoint",
        json={
            "query": prompt,
            # Add your specific parameters
        },
        headers={
            "Authorization": f"Bearer {os.getenv('YOUR_API_TOKEN', '')}"
        }
    )

    return {
        "output": response.json()["result"],
        "tokenUsage": {
            "total": response.json().get("tokens", 0)
        }
    }
```

#### B. Create Test Configuration

Create `promptfoo.config.yaml`:

```yaml
description: 'Baseline tests for Your Application'

providers:
  - id: python:promptfoo/providers/your_api_target.py
    label: 'Your API'

prompts:
  - '{{query}}'

tests:
  - vars:
      query: 'Test query 1'
    assert:
      - type: contains
        value: 'expected result'
      - type: latency
        threshold: 5000  # 5 seconds

  - vars:
      query: 'Test query 2'
    assert:
      - type: is-json
      - type: javascript
        value: 'output.length > 0'

env:
  YOUR_API_BASE_URL: 'http://localhost:8000'
  YOUR_API_TOKEN: '${YOUR_API_TOKEN}'
```

---

## 📋 Test Suite Templates

### 1. Baseline Regression Tests

**File**: `promptfoo.config.yaml`

**Purpose**: Quick smoke tests to catch regressions

**When to run**: Every commit, before deployment

**Example**:
```yaml
description: 'Baseline API Tests'

providers:
  - python:promptfoo/providers/your_target.py

tests:
  - description: 'Basic functionality'
    vars:
      input: 'test input'
    assert:
      - type: contains
        value: 'expected output'
      - type: latency
        threshold: 2000
```

### 2. Multi-Endpoint Tests

**File**: `promptfoo.multi-endpoint.yaml`

**Purpose**: Test multiple API endpoints

**Example**:
```yaml
providers:
  - id: python:promptfoo/providers/endpoint1_target.py
    label: 'Endpoint 1'
  - id: python:promptfoo/providers/endpoint2_target.py
    label: 'Endpoint 2'

tests:
  - vars:
      query: 'test'
    assert:
      - type: is-json
      - type: contains
        value: 'success'
```

### 3. Security Red Team

**File**: `promptfoo.redteam.yaml`

**Purpose**: Test for security vulnerabilities

**Example**:
```yaml
redteam:
  purpose: 'Test API security'

  plugins:
    - harmful:content
    - harmful:privacy
    - harmful:sql-injection
    - harmful:shell-injection
    - pii
    - rbac
    - bola
    - bfla
    - ssrf
    - competitors

  numTests: 5

providers:
  - python:promptfoo/providers/your_target.py
```

### 4. Performance Testing

**File**: `promptfoo.performance.yaml`

**Purpose**: Benchmark latency and throughput

**Example**:
```yaml
tests:
  - description: 'Latency test'
    vars:
      query: 'test'
    assert:
      - type: latency
        threshold: 1000
      - type: perplexity-score
        threshold: 0.8

  - description: 'Concurrent requests'
    vars:
      query: 'test'
    options:
      maxConcurrency: 10
    assert:
      - type: latency
        threshold: 3000
```

---

## 🔧 Creating Custom Components

### Custom Provider Template

```python
# promptfoo/providers/custom_provider.py
import os
import requests
from typing import Dict, Any, Optional

def call_api(prompt: str, options: Optional[Dict] = None, context: Optional[Dict] = None) -> Dict[str, Any]:
    """
    Custom provider for your API.

    Args:
        prompt: The input text/query
        options: Provider-specific options
        context: Additional context from test config

    Returns:
        Dict with 'output' and optional 'tokenUsage', 'cost'
    """
    # Get configuration from environment
    api_url = os.getenv("YOUR_API_URL", "http://localhost:8000")
    api_key = os.getenv("YOUR_API_KEY", "")

    # Parse options
    opts = options or {}
    timeout = int(opts.get("timeout", "30"))

    # Make API call
    try:
        response = requests.post(
            f"{api_url}/your-endpoint",
            json={
                "input": prompt,
                "options": opts
            },
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            timeout=timeout
        )
        response.raise_for_status()

        result = response.json()

        return {
            "output": result["output"],
            "tokenUsage": {
                "total": result.get("tokens", 0),
                "prompt": result.get("prompt_tokens", 0),
                "completion": result.get("completion_tokens", 0)
            },
            "cost": result.get("cost", 0.0)
        }

    except requests.exceptions.RequestException as e:
        return {
            "error": f"API call failed: {str(e)}",
            "output": ""
        }

# Required for Promptfoo to load the provider
if __name__ == "__main__":
    # Test the provider
    result = call_api("test query")
    print(result)
```

### Custom Grader Template

```python
# promptfoo/graders/custom_grader.py
from typing import Dict, Any

def get_assert(output: str, context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Custom grader for evaluating outputs.

    Args:
        output: The output from your provider
        context: Test context including 'vars', 'prompt', etc.

    Returns:
        Dict with 'pass' (bool), 'score' (0-1), 'reason' (str)
    """
    # Your custom evaluation logic
    score = 0.0
    reasons = []

    # Example: Check output length
    if len(output) > 10:
        score += 0.3
        reasons.append("Output has sufficient length")

    # Example: Check for specific keywords
    if "important_keyword" in output.lower():
        score += 0.4
        reasons.append("Contains required keyword")

    # Example: Check format
    try:
        import json
        json.loads(output)
        score += 0.3
        reasons.append("Valid JSON format")
    except:
        pass

    return {
        "pass": score >= 0.7,
        "score": score,
        "reason": "; ".join(reasons) if reasons else "No criteria met"
    }
```

---

## 📊 NPM Scripts Template

Add these to your `package.json`:

```json
{
  "scripts": {
    "test:baseline": "promptfoo eval --config promptfoo.config.yaml",
    "test:security": "promptfoo redteam run --config promptfoo.redteam.yaml",
    "test:performance": "promptfoo eval --config promptfoo.performance.yaml",
    "test:all": "npm run test:baseline && npm run test:security",
    "view": "promptfoo view",
    "cache:clear": "promptfoo cache clear"
  }
}
```

---

## 🔐 Environment Variables

Create `.env` file with your API configuration:

```bash
# Your API Configuration
YOUR_API_BASE_URL=http://localhost:8000
YOUR_API_KEY=your_api_key_here
YOUR_API_TIMEOUT=30

# Promptfoo Configuration
PROMPTFOO_CACHE_ENABLED=true
PROMPTFOO_SHARING=false

# OpenAI for LLM-graded tests (optional)
OPENAI_API_KEY=your_openai_key_for_grading
```

---

## 🎯 Integration Checklist

### Phase 1: Basic Setup
- [ ] Install Promptfoo
- [ ] Copy `.promptfoorc.yaml`
- [ ] Create basic `promptfoo.config.yaml`
- [ ] Add npm scripts to `package.json`

### Phase 2: Custom Providers
- [ ] Create provider for your main endpoint
- [ ] Test provider manually
- [ ] Add environment variables
- [ ] Write basic assertions

### Phase 3: Test Suites
- [ ] Baseline regression tests
- [ ] Multi-endpoint tests (if applicable)
- [ ] Performance benchmarks
- [ ] Security red team tests

### Phase 4: Advanced Features
- [ ] Custom graders for quality metrics
- [ ] Custom plugins for domain-specific attacks
- [ ] Dataset-driven tests
- [ ] CI/CD integration

### Phase 5: Documentation
- [ ] Document test suites
- [ ] Create troubleshooting guide
- [ ] Add usage examples
- [ ] Document environment variables

---

## 🔄 CI/CD Integration

### GitHub Actions Example

```yaml
name: Promptfoo Tests

on:
  pull_request:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'

      - name: Install dependencies
        run: npm install

      - name: Start API (if needed)
        run: |
          # Start your API server
          npm run start:api &
          sleep 5

      - name: Run baseline tests
        env:
          YOUR_API_BASE_URL: http://localhost:8000
          YOUR_API_KEY: ${{ secrets.API_KEY }}
        run: npm run test:baseline

      - name: Run security tests
        if: github.event_name == 'pull_request'
        run: npm run test:security

      - name: Upload results
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: promptfoo-results
          path: promptfoo-output/
```

---

## 💡 Best Practices

### 1. Start Simple
Begin with basic regression tests, then gradually add complexity.

### 2. Use Environment Variables
Never hardcode API keys or URLs in test configs.

### 3. Organize by Purpose
Separate configs for different testing purposes:
- `promptfoo.config.yaml` - Fast baseline tests
- `promptfoo.redteam.yaml` - Security tests
- `promptfoo.performance.yaml` - Performance tests

### 4. Cache Results
Enable caching to save API costs during development:
```yaml
cache:
  enabled: true
  path: ./.promptfoo-cache
```

### 5. Progressive Testing
Run cheap tests frequently, expensive tests on schedule:
- Every commit: Baseline
- Every PR: Baseline + Performance
- Daily: Security scan
- Weekly: Comprehensive red team

### 6. Document Assertions
Add descriptions to your assertions:
```yaml
assert:
  - type: contains
    value: 'success'
    metric: 'Response contains success indicator'
```

---

## 🛠️ Troubleshooting

### Provider Not Found
```bash
Error: Cannot find provider python:promptfoo/providers/target.py
```
**Solution**: Ensure Python file has executable permissions and correct path.

### Tests Timing Out
```yaml
defaultTest:
  options:
    timeout: 60000  # Increase timeout to 60 seconds
```

### API Authentication Fails
Check environment variables are loaded:
```bash
echo $YOUR_API_KEY
```

### High API Costs
Reduce number of test variations:
```yaml
redteam:
  numTests: 3  # Reduce from default 10
```

---

## 📚 Resources

- **Promptfoo Documentation**: https://www.promptfoo.dev/docs/
- **Red Team Guide**: https://www.promptfoo.dev/red-teaming/
- **Custom Providers**: https://www.promptfoo.dev/docs/providers/custom/
- **Assertions Reference**: https://www.promptfoo.dev/docs/configuration/expected-outputs/

---

## 🎓 Example Use Cases

### REST API Testing
```yaml
providers:
  - id: python:promptfoo/providers/rest_api_target.py
tests:
  - vars:
      endpoint: '/users'
      method: 'GET'
    assert:
      - type: is-json
      - type: javascript
        value: 'JSON.parse(output).length > 0'
```

### GraphQL API Testing
```yaml
providers:
  - id: python:promptfoo/providers/graphql_target.py
tests:
  - vars:
      query: '{ users { id name } }'
    assert:
      - type: contains
        value: 'data'
      - type: is-json
```

### Microservices Testing
```yaml
providers:
  - id: python:promptfoo/providers/service1_target.py
    label: 'User Service'
  - id: python:promptfoo/providers/service2_target.py
    label: 'Order Service'

scenarios:
  - description: 'Multi-service workflow'
    tests:
      - provider: 'User Service'
        vars: { action: 'create_user' }
      - provider: 'Order Service'
        vars: { action: 'create_order' }
```

---

## ✅ Summary

This Promptfoo integration provides:

1. **Automated Testing** - Catch bugs before deployment
2. **Security Scanning** - OWASP/NIST compliance
3. **Quality Assurance** - Custom graders for your domain
4. **Performance Monitoring** - Track latency and costs
5. **CI/CD Ready** - GitHub Actions integration
6. **Cost Effective** - Caching and smart test scheduling

**Time to implement**: 2-4 hours for basic setup, 1-2 days for full integration

**Maintenance**: ~30 minutes per week to update test cases

**ROI**: Catches issues early, reduces production bugs, ensures security compliance

---

For questions or issues with this integration guide, please refer to the main project documentation or open an issue.
