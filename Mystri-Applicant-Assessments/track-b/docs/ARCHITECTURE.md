# Architecture — DICM Core (Product 1)

## System context

```text
┌─────────────────────────────────────────────────────────┐
│  Mystri synthetic data (read-only for submit)           │
│  data/cases.csv  requests.csv  events.csv  scenario.json│
└───────────────────────────┬─────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│  starter.load_inputs()                                  │
└───────────────────────────┬─────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│  experiment.py  ──►  integrated_model.run_and_write_trace│
│       │                    │                            │
│       │                    ├── pipeline modules (below) │
│       │                    └── PipelineTrace (log lines)  │
│       ▼                                                 │
│  output/integrated_report.json                          │
│  output/dicm_pipeline_trace.log                         │
│  output/customer_structured_responses.json              │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
                     Terminal summary (CLI)
```

**Mode:** assessment **dry-run** — no outbound integrations.

---

## Pipeline phases (orchestration)

Order in `integrated_model.run_integrated_pipeline`:

| Phase | Module(s) | Trace phase labels |
| --- | --- | --- |
| Load | `starter` | `LOAD`, `START` |
| Policy validation | `data_policy` | `VALIDATE` |
| Customer registry | `customer_registry` | `CUSTOMER_REGISTRY` |
| Media samples | `media_intake` | `MEDIA` |
| Rules triage | `queue_engine` | `RULES` |
| Structured receipts | `customer_acknowledgment` | `CUSTOMER_ACK` |
| Lanes / board | `lane_model`, `team_workboard` | `HUDDLE`, `DEPARTURE_BOARD`, `LANES` |
| AI assist | `ai_assist` | `AI_ASSIST` |
| Technicians | `team_workboard` | `TECH` |
| Cost | `cost_model` | `COST` |
| Follow-ups | `pipeline_trace`, `integrated_model` | `COORDINATOR`, `CUSTOMER`, `END` |

---

## Module dependency (logical)

```text
experiment.py
  ├── console_io
  ├── starter
  ├── integrated_model
  │     ├── queue_engine
  │     ├── data_policy
  │     ├── customer_registry
  │     ├── media_intake
  │     ├── customer_acknowledgment
  │     ├── lane_model
  │     ├── team_workboard
  │     ├── ai_assist
  │     ├── cost_model
  │     ├── approaches
  │     └── pipeline_trace
  └── approaches (report ranking)

product1/verify_product1.py  → subprocess: starter, experiment, unittest
```

---

## Key design decisions

1. **Rules before AI** — `queue_engine` dispositions drive contact eligibility; AI never overrides.
2. **Human gates** — `AiSuggestion.human_gate`; coordinator approval simulated before `CUSTOMER` lines.
3. **Single trace file** — `PipelineTrace` append-only narrative for reviewers.
4. **Structured customer JSON** — versioned schema `daybreak.customer_ack.v1`.
5. **Baseline comparison** — naive pending set vs `propose` disposition IDs in report.

---

## Data flow (one request)

```text
request row + case row + scenario.snapshot_at
    → triage_request() → RowResult(disposition, reason)
    → if received on file → build_submission_acknowledgment()
    → if propose → build_customer_deliveries() + AI drafts
    → trace.log(...) + JSON report sections
```

---

## Extension points (not implemented in Product 1)

| Hook | Future |
| --- | --- |
| `--output-dir` | Centralized output path |
| `--intake-dir` | Product 2 local uploads |
| LLM backend | Swap `ai_assist` templates |
| SMTP | Real send behind flag |

See `PRODUCTS.md` for Product 2 / 3 boundaries.
