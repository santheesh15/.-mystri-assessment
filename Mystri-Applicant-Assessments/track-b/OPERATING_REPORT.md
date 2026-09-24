# Operating report — people + AI 

> **Primary entry point:** the single combined approach is **`INTEGRATED_MODEL.md`** (DICM). This file adds detail; run `python3 experiment.py` for the unified JSON report.

**Daybreak Repairs · Track B prototype · dry-run only · snapshot 2026-09-07**

This report shows **where humans work**, **where AI assists**, **cost/time structure**, **risks**, and **how to run on any OS** (Python 3.10+ stdlib).

---

## 1. Operating model (optimistic industry pattern)

| Lane | Role | Responsibility | AI role | Human gate |
| --- | --- | --- | --- | --- |
| A | **Coordinator** | Rule-checked customer follow-ups; inbox/data cleanup | Draft email text; suggest reply labels | **Approve every send**; confirm status changes |
| B | **Technicians T1–T4 (tiered)** | Work split by **skill level** (1=apprentice → 4=lead); load balanced inside each tier | Prep checklists by case type | **Technician sign-off**; harder tasks go to senior ranks |
| C | **Rules engine** | 48h gap, opt-out, closed cases, conflicts → uncertain | None (deterministic) | Update rules in git when policy changes |
| D | **Uncertain queue** | Messy rows (e.g. pending + received date) | Flag only; no auto-fix | Coordinator reconciles inbox vs CSV |

**Unique combination:** AI speeds **writing and sorting**; people keep **authority on contact and quality**. Technicians work **while** coordinator chases missing photos—parallel throughput.

### Technician hierarchy (work levels)

| Rank | ID | Typical role | Takes work level | Max tasks (capacity) |
| ---: | --- | --- | --- | ---: |
| 4 | **T1** | Lead technician | Level 4 (photo quality sign-off) | 3 |
| 3 | **T2** | Senior technician | Level 3+ (prep while waiting, parts plan) | 3 |
| 2 | **T3** | Technician | Level 2+ | 4 |
| 1 | **T4** | Apprentice | Level 1 (standby briefs) | 4 |

| Task | Work level | Meaning |
| --- | ---: | --- |
| `human_photo_quality_check` | 4 | Hardest judgment — lead/senior only |
| `prep_quote_while_waiting_for_photo` | 3 | Skilled prep in parallel |
| `hold_parts_plan` | 3 | Quote-stage planning |
| `standby_case_brief` | 1 | Readiness / low-risk monitoring |

Assignment algorithm: sort tasks hardest-first, assign to the **least busy** technician whose **rank ≥ task level** and who is under **capacity** (see `team_workboard.assign_by_hierarchy`).

---

## 2. Where we adopt AI (maximum utilisation, feasible)

| # | Adoption point | What AI does | What it must *not* do | Prototype module |
| --- | --- | --- | --- | --- |
| 1 | Reminder email | Draft polite request from case context | Auto-send | `ai_assist.draft_reminder_email` |
| 2 | Inbox reply triage | Suggest label (photo received / opt-out / unclear) | Auto-update CRM row | `ai_assist.classify_customer_reply` |
| 3 | Technician prep | Checklist for service type | Quote customer or order parts | `ai_assist.technician_prep_checklist` |
| 4 | Photo path | Route to human review; flag data conflicts | Auto-approve “good photo” | `ai_assist.photo_screening_decision` |
| 5 | **Multi-format intake** | Detect JPEG/PNG/WebP/GIF/PDF/CSV/text; HEIC/unknown → human | Pretend all uploads are one format | `media_intake.assess_attachment` |

**Image processing principles used (stdlib prototype):** magic-byte identification, PNG IHDR dimension parse, JPEG SOF marker scan, minimum resolution gate, coarse brightness proxy on byte samples. **Blur, glare, and OCR** are explicitly **technician/human** or future Pillow/Tesseract— not auto-quoted here.

Production: normalize HEIC→JPEG, optional OpenCV blur detection, OCR for serial numbers in text attachments.

---

## 3. Cost reduction structure (scenario INR)

Generated numbers: run `python3 experiment.py --write output/queue_report.json` — see `cost_structure` in JSON.

| Layer | Cost (INR/month) | Time effect |
| --- | ---: | --- |
| Rules + team split (no AI) | 0 tools | Reduces wrong chase; shifts work to 4 techs |
| Optional LLM assist (capped) | ≤60% of INR 1,500 budget | Saves draft/triage minutes (assumption) |
| Human review (required) | Labor (not avoided) | Prevents mistakes; non-negotiable |
| **Net** | Tools capped; labor value from net minutes saved | See report output |

All rates are **labeled assumptions** in `cost_model.py`, not Mystri-verified Daybreak accounting.

---

## 4. Maintainability

- **Single language:** Python 3.10+ **standard library only** — no `pip install`, works on **Windows, macOS, Linux**.
- **Policy as code:** rules in `queue_engine.py`; change once, rerun `python3 -m unittest`.
- **Data unchanged:** read-only CSVs; outputs in `output/` (regenerated).
- **AI prompts:** keep versioned text files in a future repo folder; prototype uses functions with `production_note` fields.

---

## 5. Risk register and handling

| Risk | Impact | Mitigation in design |
| --- | --- | --- |
| AI sends wrong email | Customer trust | Dry-run + coordinator approve; no send API in prototype |
| AI marks photo “OK” incorrectly | Bad quote | **Technician human** quality check mandatory |
| Stale spreadsheet | Wrong reminder | Uncertain queue + coordinator reconcile |
| LLM cost overrun | Budget break | Cap at 60% of INR 1,500; fallback to templates |
| Model/platform change | Breakage | Abstract `ai_assist` module; rules engine independent of AI |
| Duplicate reminders | Complaints | 48h rule + opt-out + deduped event counts |

---

## 6. Commands for reviewer

```text
cd Mystri-Applicant-Assessments/track-b
python3 experiment.py --write output/queue_report.json
python3 -m unittest discover -s tests -v
```

Open `output/queue_report.json` → sections `team_workboard`, `cost_structure`, `ai_assist_samples`.

---

## 8. Out-of-box synthesis (unique + best existing)

We **do not** pick one vendor or one buzzword. The hybrid combines:

| Source | What we took |
| --- | --- |
| **Existing shop habit** | Shared inbox + spreadsheet exports (coordinator already uses these) |
| **Buy (proven SaaS patterns)** | File-request upload link in reminders; optional approval tool for quotes later |
| **Build** | Rules engine, tiered technicians, AI draft assist (mock) |
| **Out-of-box ops** | **Three-speed lanes** (Express / Standard / Park), **departure-board** priority sort, **rotating duty lead** (T1↔T2 weekly), **15-min daily huddle** on uncertain rows |

**Three-speed lanes**

- **Express** — photo received → technician quote path (fast lane)  
- **Standard** — missing info but safe to chase with rules + parallel tech prep  
- **Park** — opt-out, closed case, or messy data → human only  

**Why unique:** Most “AI fixes churn” pitches ignore **tiered manpower + lanes + buy/build split**. This model is optimistic (parallel work, AI drafts) but **feasible** (stdlib Python, no lock-in), **maintainable** (policy in code), and **risk-aware** (Park lane + human gates).

Run `python3 experiment.py` → JSON section `out_of_box_synthesis` for ranked approaches and top departure-board rows.

---

Uses `pathlib`, UTF-8 CSV (`utf-8-sig`), and `datetime.fromisoformat` — supported on all mainstream Python 3.10+ installs. No OS-specific shell features required.
