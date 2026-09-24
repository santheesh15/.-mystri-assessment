# Track B product lines

| Product | Status | Purpose |
| --- | --- | --- |
| **Product 1 — DICM Core** | **Complete (submit this)** | Mystri Track B scoped deliverable: decision + experiment + dry-run evidence |
| Product 2 — DICM Pilot | Not started | Pilot hooks: HTML report, approval queue, intake folder, generic verify — see **`docs/FUTURE_SCOPE.md`** |
| Product 3 — DICM Vision | Not started | Production: Graph/LLM/messaging/web/DB — see **`docs/FUTURE_SCOPE.md`** |

**Official submission:** **Product 1 only.** See **`PROJECT_README.md`** and **`product1/README.md`** for the reviewer path.

---

## Product 1 — DICM Core (in scope)

**One-line pitch:** Missing-info follow-ups via **Daybreak Integrated Collaborating Model (DICM)** — rules, lanes, tiered technicians, human-gated AI assist, dry-run customer touchpoints only.

### Mystri deliverables

| Deliverable | File(s) |
| --- | --- |
| Project guide (setup, architecture, reference) | **`PROJECT_README.md`**, **`docs/`** |
| Decision note | `DECISION.md` |
| Runnable experiment | `experiment.py` + modules below |
| Sources | `SOURCES.md` |
| Handover | `HANDOVER.md` |
| Supporting narrative | `INTEGRATED_MODEL.md`, `OPERATING_REPORT.md` |

### Scoped capabilities (Product 1)

- [x] CSV loader (`starter.py`) — starter data unchanged  
- [x] Rules follow-up queue — 48h, opt-out, closed cases, received, uncertain conflicts (`queue_engine.py`)  
- [x] Baseline comparison — naive pending vs rules proposals  
- [x] Data & policy validation (`data_policy.py`)  
- [x] Customer register + spam discard (`customer_registry.py`)  
- [x] Multi-format media intake samples + basic image checks (`media_intake.py`)  
- [x] Three-speed lanes + departure board + rotating duty lead (`lane_model.py`)  
- [x] Tiered technician workboard (`team_workboard.py`)  
- [x] AI assist mock with human gates (`ai_assist.py`)  
- [x] Cost / time scenario (`cost_model.py`)  
- [x] Approach ranking context (`approaches.py`)  
- [x] Unified DICM orchestration (`integrated_model.py`)  
- [x] Structured customer receipt responses — OK / not OK / under review (`customer_acknowledgment.py`)  
- [x] Single audit trace log (`pipeline_trace.py`)  
- [x] **Dry-run only** — no real email, SMS, cloud APIs, or CRM write-back  

### Generated outputs (after `python3 experiment.py`)

| Output | Role |
| --- | --- |
| `output/integrated_report.json` | Full experiment report |
| `output/dicm_pipeline_trace.log` | START → … → CUSTOMER_ACK → CUSTOMER → END |
| `output/customer_structured_responses.json` | Structured receipt payloads |

### Verify Product 1

```text
cd Mystri-Applicant-Assessments/track-b
python3 product1/verify_product1.py
```

### Explicitly out of Product 1 (Product 2 / 3 later)

Live messaging, Microsoft Graph / OneDrive, production LLM, web app, database backend, WhatsApp API, autonomous send, mutating `data/*.csv`, pilot ROI claims.

**Planned roadmap (not built):** **`docs/FUTURE_SCOPE.md`**.
