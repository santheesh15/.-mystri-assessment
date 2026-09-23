# Daybreak Track B — Product 1 (DICM Core)

**Daybreak Integrated Collaborating Model (DICM)** — Mystri Track B assessment deliverable.  
Dry-run missing-info follow-ups: rules, team lanes, human-gated AI assist, structured customer receipts.

| | |
| --- | --- |
| **Product** | Product 1 — DICM Core (`product1/`, `PRODUCTS.md`) |
| **Branch** | `cursor/track-b-submission-edb7` |
| **Entry point** | `experiment.py` |
| **Verification** | `python product1/verify_product1.py` (Windows: `python`; Unix: `python3`) |

Mystri assignment brief remains in [`README.md`](README.md) (original pack instructions).

---

## Quick start

```bash
cd Mystri-Applicant-Assessments/track-b
python product1/verify_product1.py
```

Outputs land in **`output/`** (single folder):

| File | Purpose |
| --- | --- |
| `integrated_report.json` | Full DICM run report |
| `dicm_pipeline_trace.log` | Unified audit trace (START → END) |
| `customer_structured_responses.json` | OK / not-OK receipt payloads |

---

## Documentation map

| Document | Audience | Contents |
| --- | --- | --- |
| [`docs/SETUP.md`](docs/SETUP.md) | Developer / reviewer | Prerequisites, install, commands, portability |
| [`docs/TECH_STACK.md`](docs/TECH_STACK.md) | Technical | Languages, dependencies, constraints |
| [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) | Technical | Pipeline, modules, data flow |
| [`docs/CONFIGURATION.md`](docs/CONFIGURATION.md) | Operator | CLI flags, paths, scenario/data |
| [`docs/REFERENCE.md`](docs/REFERENCE.md) | Developer | Modules, constants, helpers, tests |
| [`DECISION.md`](DECISION.md) | Reviewer | Business decision (submit) |
| [`HANDOVER.md`](HANDOVER.md) | Reviewer | Run commands, evidence (submit) |
| [`INTEGRATED_MODEL.md`](INTEGRATED_MODEL.md) | Reviewer | DICM narrative |
| [`product1/README.md`](product1/README.md) | Reviewer | 5-minute verification path |

---

## What this is / is not

| In scope | Out of scope (Product 1) |
| --- | --- |
| CLI experiment on Mystri CSVs | Web app / production site |
| Dry-run customer touchpoints | Real email / SMS / WhatsApp |
| Mock AI assist (templates) | Production LLM API |
| JSON + log evidence | CRM write-back to live systems |

---

## License / data

Synthetic Mystri data only (`data/`). Do not use for real customers. Assessment submission — see `HANDOVER.md`.
