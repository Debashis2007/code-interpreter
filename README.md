# Use Case: Code Interpreter / Data Analysis

**Design doc:** [docs/DESIGN.md](./docs/DESIGN.md) — architecture, patterns, and why.


**Parent system design:** [07 — Agent Runtime with Hard Containment](../07-agent-runtime-containment.md)

## Users & problem

Users upload CSVs and ask the model to analyze with Python. Execution must be powerful inside a box—and powerless against the host or other tenants.

## Requirements & SLOs

| Requirement | Target |
|-------------|--------|
| Isolation | Micro-VM / strong sandbox per session |
| Quotas | CPU, mem, disk, time |
| Network | Deny by default (or tightly proxied) |
| Artifacts | Charts/files returned safely |

## Design (from parent)

```
Model proposes run_code → policy allow
  → cold/warm micro-VM → execute
  → capture stdout/files → scrub → observe to model
  → destroy/reset VM
```

Reuse policy engine + sandbox + egress deny from **07**.

## Specializations

| Concern | Code interpreter choice |
|---------|-------------------------|
| Images | Curated package set; no arbitrary pip to net by default |
| Files | Size caps; virus scan uploads |
| Warm pools | Snapshot boot for latency |
| Secrets | Never mount cloud credentials |

## Failure modes

- Crypto miner / fork bomb → cgroup + wall time kill.
- SSRF via code → no egress or force proxy deny list.
- State bleed between users → unique VM; wipe filesystem.



## Run (self-contained POC)

This folder is a **standalone** project (safe to split into its own GitHub repo).

```bash
cd code-interpreter
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
PYTHONPATH=. python -m uvicorn app.main:app --reload --port 8000
```

```bash
curl -s http://127.0.0.1:8000/health | jq
```

curl -s -X POST http://127.0.0.1:8000/execute -H 'Content-Type: application/json' -d '{"code":"print(1+1)"}' | jq
