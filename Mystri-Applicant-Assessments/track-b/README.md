# Track B submission — Daybreak DICM (Product 1)

**Applicant:** Santheesh S · **Track:** B · **Effort:** 4 hours 35 minutes (275 min) — see **`HANDOVER.md`**

This folder is my **completed Mystri Track B deliverable**: a decision on missing-information follow-ups at fictional **Daybreak Repairs**, plus a **runnable dry-run pipeline** (DICM Core) on the supplied CSV snapshot.

---

## What I implemented

I built **Product 1 — DICM Core**: one integrated daily pipeline that combines:

- **Rules-based follow-up queue** (`queue_engine.py`) — 48-hour gap, opt-out, closed cases, received items, uncertain conflicts  
- **Baseline comparison** — **13** naive pending reminders vs **5** rule-based drafts; **8** request IDs blocked on the pack data  
- **Coordinator + tiered technicians + three-speed lanes** — orchestrated in **`integrated_model.py`**  
- **Human-gated AI assist** (templates only, no live LLM) — **`ai_assist.py`**  
- **Structured customer receipts** (OK / not OK / under review) — JSON + trace, **simulated send only**  
- **Full audit trace** — **`output/dicm_pipeline_trace.log`** (START → END)  
- **38 unit tests** + **`product1/verify_product1.py`** gate → **`PRODUCT 1 PASS`**

I did **not** change Mystri **`data/*.csv`** for grading. All customer contact in code is **dry-run**.

---

## What this submission shows

| Question | Where the answer lives |
| --- | --- |
| Should Daybreak build, buy, or change process? | **`DECISION.md`** — recommend **DICM hybrid**; honest limits on 8 h/week claim |
| Did I check external “file request” claims? | **`SOURCES.md`** + **`RESOURCE_STARTERS.md`** |
| How does the model work day to day? | **`INTEGRATED_MODEL.md`**, **`OPERATING_REPORT.md`** |
| Architecture, setup, rules, future plan | **`docs/`** — especially **`ARCHITECTURE.md`**, **`SETUP.md`**, **`FUTURE_SCOPE.md`** |
| How to run and grade this repo | **`HANDOVER.md`**, **`PROJECT_README.md`**, **`product1/README.md`** |

The fictional case study (four technicians, one coordinator, synthetic **`@example.invalid`** data) comes from the Mystri pack. My work is the **analysis, decision, code, tests, and `output/` artifacts** above—not a copy of the original assignment brief.

---

## Verify this work (reviewers)

From this folder (`track-b`):

```powershell
python product1\verify_product1.py
```

Expected: **`PRODUCT 1 PASS`**. Proof files are written under **`output/`** (see **`HANDOVER.md`** for opening them in Notepad).

macOS/Linux: `python3 product1/verify_product1.py`

---

## Scenario context (fixed snapshot)

- **Synthetic data**; observation **24 Aug – 6 Sep 2026**; rules use **`data/scenario.json`** snapshot **7 Sep 2026, 09:00 IST** — not the PC clock.  
- Field meanings: **`DATA_DICTIONARY.md`**. Interview flavour text: **`USER_NOTES.md`** (fictional, not market proof).

---

## How I spent time (275 min)

| Activity | Minutes |
| --- | ---: |
| Read the scenario and inspect the data | 40 |
| Targeted external research | 55 |
| Analyze, compare and choose an approach | 40 |
| Build and check the experiment | 95 |
| Decision note, docs, verification, and handover | 45 |
| **Total** | **275** |

---

## Product scope

- **Submitted and graded:** **Product 1 only** — **`PRODUCTS.md`**  
- **Planned later (not built):** Product 2 pilot / Product 3 vision — **`docs/FUTURE_SCOPE.md`**

---

## Original Mystri Track B brief

The assessment’s official instructions (word limits, rubric, deliverable checklist) are **not duplicated here**; this README describes **what I delivered**. For pack file listings and constraints, see **`DATA_DICTIONARY.md`** and the PDF in **`../briefs/`**.
