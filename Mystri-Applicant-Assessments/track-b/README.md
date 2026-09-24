# Track B submission — Daybreak DICM (Product 1)

**Applicant:** Santheesh S · **Track:** B · **Effort:** 4 hours 35 minutes (275 min) — **`HANDOVER.md`**

I completed Mystri **Track B — Find the worthwhile automation** for fictional **Daybreak Repairs** (four technicians, one coordinator). The owner’s line—“we lose eight hours a week chasing customers; can AI fix this?”—is a **claim I tested**, not a fact I assumed. I focused on **collecting missing information** before quoting (photos, serial numbers, access), implemented a **dry-run DICM pipeline** on the supplied CSVs, and documented limits as per my observation.

For run steps and proof files, see **`HANDOVER.md`** and **`PROJECT_README.md`**. The official assignment PDF remains in **`../briefs/`**; this README describes **what I built and where to read it**.

---

## The problem I chose and the decision I recorded

Daybreak’s scenario allows up to **two engineering weeks** and **INR 1,500/month** tool budget—these are **constraints in the pack**, not proof customers would pay.

I treated the export as a **small synthetic snapshot** with incomplete time logging. I separated **waiting time**, **logged coordinator minutes**, and **quote value** (not profit). I did **not** treat the owner’s **8 hours/week** as measured truth; **`DECISION.md`** shows logged effort is far lower and explains why.

**My recommendation (summary):** adopt **DICM (Daybreak Integrated Collaborating Model)**—one daily pipeline combining inbox/spreadsheet habits, rules, lanes, tiered technicians, human-gated AI **templates**, and optional file-request **wording** in drafts—not a single vendor or autonomous AI. Full reasoning, alternatives, calculations, and net **+12 min/week** scenario band are in **`DECISION.md`**.

---

## What I implemented (deliverables mapped to the brief)

### 1. Decision note — **`DECISION.md`**

- **Users and workflow:** coordinator + tiered technicians; missing-info follow-ups without wrong reminders.  
- **Calculations:** deduplicated **`event_id`**; **400** logged minutes in window; **15** pending requests; **13** naive vs **5** rules-based drafts; **8** IDs the rules block (examples **R012**, **R029**).  
- **Alternatives compared:** process-only review, OneDrive/Dropbox file request, custom rules queue, hybrid DICM.  
- **Technical claim checked:** file-request products **collect files** but do **not** enforce 48h spacing, opt-outs, or row reconciliation—verified against vendor docs in **`SOURCES.md`**.  
- **Recommendation + limits:** hybrid DICM; what would change my mind and **continue/stop** pilot criteria at the end of the note.  
- **Net value:** transparent scenario table for the **selected** workflow (not the owner’s 8h claim).

### 2. Working experiment — **`experiment.py`** and modules

I built a **stdlib-only Python 3.10+** prototype that **reads the supplied CSVs** and tests the central idea: a **reviewable follow-up queue** with baseline comparison.

**What it does:**

- **`queue_engine.py`** — each request is **propose**, **exclude**, or **uncertain** with a stated reason (48h, opt-out, closed case, received, conflicts).  
- **`integrated_model.py`** — runs validation, customer register, media samples, rules, lanes, technician board, AI assist mocks, cost view, trace, and simulated customer receipts in **one pipeline**.  
- **Baseline:** naive “remind every pending + followup_allowed=1” vs rules-based **propose** set on the same snapshot.  
- **Changed-input check:** tests move **R009** to 1h before snapshot → **exclude** with 48h reason (`tests/test_queue.py`).  
- **No-action check:** all requests received → **0** proposals (`test_no_action_when_all_requests_received`).  
- **Edge case:** **R018** pending + **`received_at`** → **uncertain**.  
- **Outputs on pack data:** **`output/integrated_report.json`**, **`output/dicm_pipeline_trace.log`**, **`output/customer_structured_responses.json`**.  
- **Gate:** **`python product1/verify_product1.py`** → **`PRODUCT 1 PASS`** and **38** unit tests.

I connected the experiment to the file-request claim: the pipeline **simulates** upload-link text in AI drafts but **proves** follow-up **policy** in code and trace—not live OneDrive.

**What it does not prove:** real sends, customer satisfaction, production LLM value, or the owner’s 8h/week (`docs/RULES_AND_LIMITATIONS.md`).

### 3. Sources and handover — **`SOURCES.md`**, **`HANDOVER.md`**

- **`SOURCES.md`:** external URLs (Microsoft, Dropbox, Jotform) with access dates, supported claims, and **limitations**; plus pack references (`DATA_DICTIONARY.md`, `USER_NOTES.md`).  
- **`HANDOVER.md`:** my name, email, time, **verify + notepad** reviewer steps, evidence table, tool use (Cursor), and **not proven** list.

I did not add fake interviews, invented test results, or cloud deployment.

---

## Evidence pack in this folder (Mystri data + my additions)

| File | Role in my submission |
| --- | --- |
| `data/cases.csv`, `events.csv`, `requests.csv` | Unchanged Mystri snapshot input |
| `data/scenario.json` | Fixed clock (**7 Sep 2026 09:00 IST**); rules use this, not PC time |
| `DATA_DICTIONARY.md` | Field meanings; I clarified ambiguous rows → **uncertain** in code |
| `USER_NOTES.md` | Fictional interviews—I used as context, not market proof |
| `RESOURCE_STARTERS.md` | Background links; my comparison is in **`SOURCES.md`** |
| `starter.py` | Loader I extended; **`experiment.py`** is the main demo |
| `output/*` | Generated proof after verify or **`experiment.py`** |
| `docs/*`, `INTEGRATED_MODEL.md`, `OPERATING_REPORT.md` | Architecture, setup, rules, future roadmap |
| `product1/` | Manifest + **`verify_product1.py`** |

---

## How to run what I built

**Load check only:**

```text
python starter.py
```

**Full pipeline + outputs:**

```text
python experiment.py
```

**Official submission check (tests + outputs + baseline on pack data):**

```powershell
python product1\verify_product1.py
```

(macOS/Linux: `python3`.) Run from this **`track-b`** folder. Requires **Python 3.10+**, **no pip packages**.

All records are synthetic. **My prototype is dry-run only**—drafts and trace lines, **no real email or messaging**. Constraints for contact logic align with **`DATA_DICTIONARY.md`**.

After verify, reviewers can open proof files—see **`HANDOVER.md`** (Notepad commands) and screenshot in **`docs/assets/`**.

---

## How I spent time (275 min)

Mystri’s brief targets **4 hours (240 min)**; I recorded **4 h 35 min** honestly.

| Activity | Minutes |
| --- | ---: |
| Read the scenario and inspect the data | 40 |
| Targeted external research | 55 |
| Analyze, compare and choose an approach | 40 |
| Build and check the experiment | 95 |
| Decision note, docs, verification, and handover | 45 |
| **Total, including setup and choosing Track B** | **275** |

---

## What this submission is designed to show reviewers

The Track B rubric asks for research, reasoning, a working check, scope, and clear handover. **This repo maps to that as follows:**

| Criterion | Weight | Where I show it |
| --- | ---: | --- |
| Research and source quality | 30% | **`SOURCES.md`**, file-request doc check in **`DECISION.md`** |
| Analysis and reasoning | 25% | **`DECISION.md`** calculations, questioned 8h/week premise |
| Working experiment and verification | 25% | **`experiment.py`**, baseline 13 vs 5, tests, **`output/`**, **`PRODUCT 1 PASS`** |
| Scope and prioritization | 10% | Pilot continue/stop in **`DECISION.md`**; **`docs/FUTURE_SCOPE.md`** for later phases |
| Handover and tool judgment | 10% | **`HANDOVER.md`**, tool notes, honest limits |

---

## Product scope and future work

- **Submitted for grading:** **Product 1 — DICM Core** only — **`PRODUCTS.md`**, **`product1/README.md`**.  
- **Not built (planned):** Product 2 pilot (HTML report, flex verify, intake folder) and Product 3 vision (Graph, LLM, messaging, web app)—**`docs/FUTURE_SCOPE.md`**.

---

## Quick navigation

| If you want… | Open… |
| --- | --- |
| My decision and math | **`DECISION.md`** |
| Run and verify | **`HANDOVER.md`**, **`docs/SETUP.md`** |
| Pipeline story | **`INTEGRATED_MODEL.md`** |
| Code map | **`docs/ARCHITECTURE.md`**, **`docs/REFERENCE.md`** |
| Full project index | **`PROJECT_README.md`** |
