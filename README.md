<p align="center">
  <a href="https://elamcb.github.io/AQUA/">
    <img src="docs/aqua-logo.png" alt="A.Q.U.A — AI Quality and Uncertainty Architect" width="420">
  </a>
</p>

<p align="center">
  <a href="https://elamcb.github.io/AQUA/"><img src="https://img.shields.io/badge/A.Q.U.A-site-0891b2?style=for-the-badge" alt="A.Q.U.A site"></a>
</p>

<p align="center">
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT"></a>
  <img src="https://img.shields.io/badge/python-3.11+-blue.svg" alt="Python 3.11+">
  <img src="https://img.shields.io/badge/status-alpha-orange.svg" alt="Status: Alpha">
  <img src="https://img.shields.io/badge/docker-required-blue.svg" alt="Docker required">
</p>

<p align="center"><strong>Autonomous testing with explicit uncertainty.</strong><br>
AI that explains <em>why</em> it tests, not just <em>what</em> it found.</p>

---

## The Problem

Current AI testing tools promise autonomy but deliver black boxes:

- **They generate tests** — but can't explain *why* these scenarios matter
- **They report failures** — but hide their confidence in the diagnosis
- **They suggest fixes** — but auto-merge without accountability

In regulated environments, this isn't autonomy. It's liability dressed as innovation.

**A.Q.U.A is different.**

---

## What A.Q.U.A Does

A.Q.U.A is an autonomous AI testing engine built on a single principle: **every decision carries uncertainty, and that uncertainty must be visible, auditable, and actionable.**

| Capability | What It Means |
|-----------|---------------|
| **Causal Scenario Generation** | Traces code changes through impact graphs to generate targeted test scenarios — with explicit rationale for each |
| **Uncertainty-Quantified Execution** | Runs tests in isolated sandboxes and reports results with confidence intervals, not just pass/fail |
| **Explainable Root Cause Analysis** | Diagnoses failures with alternative hypotheses ranked by probability — never a single "AI said so" answer |
| **Recommendation Engine** | Suggests fixes with risk assessment, but **never auto-merges** — human judgment is the final gate |
| **Production Validation** | Validates test effectiveness against real-world traffic shadows, catching model drift and performance degradation post-deployment |

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    A.Q.U.A ARCHITECTURE                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    │
│  │   INGEST    │───→│   REASON    │───→│   EXECUTE   │    │
│  │             │    │             │    │             │    │
│  │ • Git diffs │    │ • Causal    │    │ • Sandbox   │    │
│  │ • Code AST  │    │   impact    │    │   orchestra-│   │
│  │ • API specs │    │   analysis  │    │   tion      │    │
│  │ • Runtime   │    │ • Scenario  │    │ • Parallel  │    │
│  │   telemetry │    │   generation│    │   execution │    │
│  │ • Historical│    │ • Uncertainty│   │ • Trace     │    │
│  │   failures  │    │   modeling  │    │   collection│    │
│  └─────────────┘    └─────────────┘    └─────────────┘    │
│         │                  │                  │            │
│         └──────────────────┼──────────────────┘            │
│                            ↓                                │
│                   ┌─────────────┐                           │
│                   │   EXPLAIN   │                           │
│                   │             │                           │
│                   │ • Confidence│                           │
│                   │   scores per│                           │
│                   │   scenario  │                           │
│                   │ • Alternative│                          │
│                   │   hypotheses│                           │
│                   │ • Decision  │                           │
│                   │   trails    │                           │
│                   └─────────────┘                           │
│                            ↓                                │
│                   ┌─────────────┐                           │
│                   │   CONNECT   │                           │
│                   │             │                           │
│                   │ • Shadow    │                           │
│                   │   integration│                          │
│                   │ • Manager   │                           │
│                   │   briefs      │                           │
│                   │ • Stakeholder│                          │
│                   │   dashboards  │                           │
│                   └─────────────┘                           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Core Principles

Three rules that govern every A.Q.U.A decision — from scenario generation to production validation.

| | Principle | In one line |
|:---:|-----------|-------------|
| **01** | **Uncertainty Is a Feature** | Every output includes confidence, rationale, and ranked alternatives |
| **02** | **Human-in-the-Loop** | A.Q.U.A recommends. Humans decide. |
| **03** | **Production Truth** | Sandboxes lie. Shadow traffic tells the truth. |

---

### 01 · Uncertainty Is a Feature, Not a Bug

Every output ships with confidence, rationale, and ranked alternatives — never a single "AI said so."

**Example** — `87%` confidence on *Expired coupon rejection at checkout*:

| Alternative | Probability |
|-------------|-------------|
| Coupon service timeout causes silent failure | 9% |
| Currency conversion masks coupon value | 4% |

<details>
<summary>Full JSON output</summary>

```json
{
  "scenario": "Expired coupon rejection at checkout",
  "confidence": 0.87,
  "rationale": "Payment validation refactor removed explicit expiry check; historical pattern shows 73% of similar changes introduced coupon bypass",
  "alternative_hypotheses": [
    {
      "description": "Coupon service timeout causes silent failure",
      "probability": 0.09,
      "evidence": "No timeout handling in new async path"
    },
    {
      "description": "Currency conversion masks coupon value",
      "probability": 0.04,
      "evidence": "Unrelated change in conversion layer"
    }
  ],
  "recommended_action": "Add explicit expiry assertion before payment processing"
}
```

</details>

---

### 02 · Human-in-the-Loop by Design

A.Q.U.A recommends. Humans decide. Autonomy stops at the merge button.

| A.Q.U.A | → | Human gate |
|---------|---|------------|
| Generate scenario | → | Review and approve test plan |
| Identify failure | → | Review diagnosis and alternatives |
| Suggest fix | → | Edit, validate, and merge |
| Flag production drift | → | Review trend and authorize response |

---

### 03 · Production Truth Over Synthetic Confidence

Tests pass in sandboxes. Reality happens in production. A.Q.U.A validates test effectiveness against real traffic.

| Track | What it catches |
|-------|-----------------|
| **Model drift detection** | Scenarios that no longer match the codebase — stale tests creating false confidence |
| **Performance degradation** | Passing tests that mask real slowdowns users feel in production |
| **Real-world effectiveness** | Sandbox passes that never correlated with preventing actual production bugs |

---

## Quick Start

> **Naming:** The product is **A.Q.U.A**. The repo, package, and CLI use **AQUA** / `aqua` — same project, different surfaces.

### Prerequisites

- Python 3.11+
- Docker (for sandbox execution)
- Git

### Installation

```bash
git clone https://github.com/ElaMCB/AQUA.git
cd AQUA
pip install -r requirements.txt
```

### Configure

```bash
cp .env.example .env
# Edit .env:
# OPENAI_API_KEY=sk-...          # For LLM reasoning
# ANTHROPIC_API_KEY=sk-...       # Alternative LLM
# LOCAL_LLM_URL=http://...       # Ollama/vLLM for private inference
# AZDO_PAT=...                   # Azure DevOps integration
```

### Run Your First Analysis

```bash
# Analyze a PR and generate uncertainty-quantified test scenarios
python -m aqua analyze \
  --repo /path/to/your/code \
  --pr 42 \
  --output aqua-report.json

# Review the report
cat aqua-report.json | python -m aqua render --format markdown
```

### Execute Tests

```bash
# Run generated scenarios in isolated sandboxes
python -m aqua execute \
  --scenarios aqua-report.json \
  --parallel 10 \
  --output results/

# Review results with confidence scores
python -m aqua report --results results/
```

---

## Integration with Shadow

A.Q.U.A feeds Shadow (Hyper-Agent), creating the only platform that connects autonomous testing to leadership decision-making:

```yaml
# shadow/config.yaml
integrations:
  aqua:                            # lowercase key — AQUA service identifier
    enabled: true
    endpoint: http://localhost:8000
    include_in_brief: true
    alert_threshold: 0.75        # Flag scenarios with confidence < 75%
```

Shadow's morning brief then includes:

- Overnight A.Q.U.A test results with confidence scores
- Scenarios requiring manager attention (low confidence, high impact)
- Production drift alerts
- Recommended actions with full decision trails

---

## Roadmap

| Phase | Focus | Status |
|-------|-------|--------|
| Alpha | Causal graph construction, scenario generation, basic sandbox execution | In progress |
| Beta | Uncertainty quantification, alternative hypothesis ranking, Shadow integration | Planned |
| v1.0 | Production validation framework, full audit trails, enterprise governance | Planned |
| v2.0 | Multi-repo causal graphs, cross-service impact analysis, predictive drift modeling | Future |

---

## Purpose

Autonomous AI can generate tests, diagnose failures, and suggest fixes — but most tools hide how confident they are. In production and regulated environments, a black-box pass/fail is not enough.

A.Q.U.A exists to make **uncertainty visible**: every scenario, diagnosis, and recommendation ships with rationale, confidence, and alternatives — so humans stay in control.

- **For engineers:** A.Q.U.A generates better scenarios because it explains its reasoning
- **For managers:** A.Q.U.A integrates with Shadow to turn test results into leadership intelligence
- **For compliance:** A.Q.U.A provides full audit trails — every decision, every confidence score, every alternative considered

---

<p align="center">
  <em>"The measure of intelligence is the ability to change."</em> — Albert Einstein<br><br>
  <em>"The measure of trustworthy AI is the ability to say 'I'm not sure.'"</em> — A.Q.U.A
</p>
