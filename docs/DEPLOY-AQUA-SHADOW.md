# Deploy A.Q.U.A with Shadow (Hyper-Agent)

Shadow is the leadership and brief layer: [github.com/ElaMCB/Hyper-Agent](https://github.com/ElaMCB/Hyper-Agent)  
A.Q.U.A is the uncertainty-quantified testing engine: [github.com/ElaMCB/AQUA](https://github.com/ElaMCB/AQUA)

Together they form a **test → brief** loop: A.Q.U.A produces `aqua-report.json`; Shadow surfaces low-confidence scenarios in the morning brief.

---

## 1. Shared data contract

Copy or sync the schema in both repos (keep versions aligned):

| File | Purpose |
|------|---------|
| `schemas/aqua-report.schema.json` | JSON Schema for `aqua_report` payloads |
| `examples/aqua-report.json` | Reference output (AQUA) |
| `data/aqua-report.json` | Live file Shadow reads (Hyper-Agent) |

---

## 2. Local full stack

### Terminal A — generate a report (AQUA)

```bash
git clone https://github.com/ElaMCB/AQUA.git
cd AQUA
pip install -r requirements.txt

# Analyze changes on current branch vs main
python -m aqua analyze \
  --repo /path/to/your/app \
  --base main \
  --head HEAD \
  --output aqua-report.json

# Preview markdown (what CI posts on PRs)
python -m aqua render --input aqua-report.json --format markdown
```

### Terminal B — ingest into Shadow

```bash
git clone https://github.com/ElaMCB/Hyper-Agent.git
cd Hyper-Agent
pip install -r requirements.txt

cp /path/to/aqua-report.json data/aqua-report.json
```

Edit `config/config.yaml`:

```yaml
integrations:
  aqua:
    enabled: true
    report_path: data/aqua-report.json
    alert_threshold: 0.75
    include_in_brief: true
```

```bash
python src/main.py brief
# or: python src/main.py headquarters
```

---

## 3. CI on pull requests (AQUA repo)

The workflow `.github/workflows/aqua-pr.yml` in AQUA:

1. Runs `python -m aqua analyze` on the PR diff  
2. Uploads `aqua-report.json` as an artifact  
3. Posts a markdown summary as a PR comment  

To feed Shadow in CI, download the artifact into `Hyper-Agent/data/` in a downstream job or nightly workflow.

---

## 4. Shadow config reference

```yaml
integrations:
  aqua:
    enabled: true
    report_path: data/aqua-report.json   # relative to Hyper-Agent repo root
    alert_threshold: 0.75                # brief flags scenarios below this
    include_in_brief: true
    endpoint: ""                         # optional HTTP URL when AQUA API ships
    timeout_seconds: 10
```

Shadow docs: [Hyper-Agent/docs/INTEGRATION-AQUA.md](https://github.com/ElaMCB/Hyper-Agent/blob/main/docs/INTEGRATION-AQUA.md)

---

## 5. Field guide for managers

| AQUA field | Shadow brief behavior |
|------------|----------------------|
| `confidence < alert_threshold` | Listed as **manager review** with impact |
| `impact: high` | Prioritized in brief bullets |
| `production_drift` | Count surfaced when present |
| `recommendations` | Available in full report; brief shows scenario summary |

---

## 6. Roadmap

| Step | Status |
|------|--------|
| Shared JSON schema | Done |
| AQUA `analyze` → `aqua-report.json` | MVP (heuristic scenarios) |
| Shadow brief ingestion | Done |
| PR comment via GitHub Actions | Done |
| AQUA HTTP API on `:8000` | Planned |
| Single workflow: AQUA → Shadow → PR comment | Planned |
