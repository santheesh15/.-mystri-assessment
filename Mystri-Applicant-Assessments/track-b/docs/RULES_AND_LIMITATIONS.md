# Rules and limitations — Product 1 (DICM Core)

## Project rules (repository)

| # | Rule |
| --- | --- |
| R1 | **Dry-run only** — no real email, SMS, WhatsApp, or customer messaging. All customer lines are simulated in logs/JSON. |
| R2 | **Do not mutate Mystri starter CSVs in `data/`** 
| R3 | **Use `scenario.json` snapshot time** for rule timing — not the computer’s live clock — when comparing to documented results (13 vs 5 drafts, etc.). |
| R4 | **Stdlib only** — no `pip install` requirements for Product 1 verify path. |
| R5 | **Human-in-the-loop** — AI (`ai_assist.py`) may suggest; rules + coordinator/technician gates decide; no autonomous send in code. |
| R6 | **Official verify** — submission proof is `python product1/verify_product1.py` from `track-b` with outputs under default **`output/`**. |
| R7 | **Product boundary** — grade **Product 1** only; Product 2/3 are not part of this handover unless explicitly labeled pilot/vision. |
| R8 | **Synthetic data** — `@example.invalid` contacts; not for production or real PII. |

---

## Business rules encoded in software (`queue_engine.py`)

These are the **Daybreak follow-up rules** the experiment implements:

| Rule | Behavior |
| --- | --- |
| **48-hour gap** | No `propose` if last request was &lt; `minimum_followup_gap_hours` (default 48) before snapshot. |
| **Opt-out** | `followup_allowed=0` → exclude (no chase). |
| **Closed case** | Case status completed / cancelled / scheduled → exclude contact for open requests. |
| **Already received** | `received` status or `received_at` set → exclude new reminder (item on file). |
| **Conflicting row** | e.g. `pending` + `received_at` → **uncertain** (coordinator; no auto contact). |
| **Missing contact / time** | Missing `contact_address` or `last_requested_at` → uncertain or exclude as coded. |
| **Quote approval** | Only when case status allows (e.g. quote_sent). |
| **Naive baseline** | All pending + followup_allowed=1 — compared to rules-based `propose` set. |

Disposition values: **`propose`**, **`exclude`**, **`uncertain`**.

---

## Data & policy rules (`data_policy.py`, `customer_registry.py`)

| Area | Rule |
| --- | --- |
| Validation | Syntax and policy findings on cases, requests, events; `pipeline_ok` when no blocking errors. |
| Customer registry | Case must exist; contact must match register pattern; spam/fake domains **discarded** from automation list. |
| Media intake (samples) | Multi-format sniff; weak/small/HEIC/unknown → human_review or reject in demo samples. |

---

## Output rules

| Rule | Detail |
| --- | --- |
| O1 | All primary artifacts for one run go under **`track-b/output/`** (default). |
| O2 | Re-running **`experiment.py`** or **`verify_product1.py`** **overwrites** those output files. |
| O3 | Trace file must contain `START`, `CUSTOMER_ACK`, `CUSTOMER` (dry-run), and `END` for a full pipeline pass. |
| O4 | JSON must include `integrated_model.comparison` with naive count &gt; rules-based drafts on pack data. |

---

## Limitations (what Product 1 does **not** prove or do)

### Operational / business

| Limitation | Notes |
| --- | --- |
| **Owner 8 h/week** | Not validated; logged events suggest ~2.4 h/week logged admin time in window. |
| **Net time savings** | Scenario ~+12 min/week on triage only in `DECISION.md` — not full shop workload. |
| **Customer satisfaction** | Not measured. |
| **Revenue / quote conversion** | Quote value in CSV ≠ profit or ROI. |
| **Production readiness** | Assessment prototype; not deployed operations. |

### Technical

| Limitation | Notes |
| --- | --- |
| **No web UI** | CLI + files only. |
| **No real LLM** | Templates stand in for AI; LLM necessity **not proven**. |
| **No inbox/CRM sync** | File request links discussed in docs; no Microsoft Graph / live OneDrive. |
| **No live messaging** | SMTP, WhatsApp Business, etc. out of scope. |
| **Media QC** | Stdlib sniff + basic checks; not full blur/OCR/HEIC pipeline. |
| **Events data** | Duplicate `event_id` possible; deduped manually in decision calculations. |
| **Changed CSVs** | Engine supports edits, but graded baseline assumes **original pack**. |

### Environment

| Limitation | Notes |
| --- | --- |
| **Python 3.10+** | Required; not tested on end-of-life Python 2. |
| **Windows console** | Older copies may need UTF-8 fix (`console_io.py`) or branch update. |
| **Mobile** | Not supported as a runtime target. |

---

## Mystri assessment alignment

| Required | Product 1 |
| --- | --- |
| Decision note | `DECISION.md` |
| Runnable experiment | `experiment.py` + tests |
| Sources | `SOURCES.md` |
| Handover | `HANDOVER.md` |
| Applicant total time | **4 h 35 min (275 min)** — `HANDOVER.md` time budget |
| Honest limits | This file + handover “Not proven” |

---

## Related docs

- Output commands: **`docs/SETUP.md`** → “Commands to generate outputs”
- CLI flags: **`docs/CONFIGURATION.md`**
- Scope checklist: **`PRODUCTS.md`**
- DICM narrative: **`INTEGRATED_MODEL.md`**
