# Integrated collaborating approach (single model)

**Name:** Daybreak Integrated Collaborating Model (**DICM**)  
**One line:** Everyone and every tool has a **defined role** in one daily pipeline—nothing works alone, nothing auto-contacts customers.

---

## Who collaborates (5 people + tools)

| Actor | Role in DICM |
| --- | --- |
| **Coordinator** | Runs departure board; approves AI drafts; sends only rule-passing follow-ups; fixes uncertain data |
| **Duty lead (T1 or T2, rotating weekly)** | Co-leads 15-min huddle; escalates Park-lane conflicts |
| **Technicians T1–T4 (tiered)** | Parallel work by skill level—photo human check, prep, parts plan, standby |
| **Rules engine** | Shared “referee”—48h, opt-out, closed cases |
| **AI assist (capped API in production)** | Drafts email + upload link text; inbox labels; tech checklists—**never sends** |
| **Existing tools kept** | Shared inbox, spreadsheet export, optional OneDrive/Dropbox file-request link in drafts |

---

## One pipeline (run every working day)

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Huddle (15 min) — Coordinator + rotating duty lead       │
│    • Top rows on departure board (wait + quote value)       │
│    • All uncertain / Park-lane cases                          │
└───────────────────────────┬─────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. Three-speed lanes — Express / Standard / Park            │
│    Express → technicians (human photo check, quote prep)      │
│    Standard → rules + coordinator drafts + parallel tech work │
│    Park → humans only (opt-out, bad data, closed)           │
└───────────────────────────┬─────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. Rules gate — who may be contacted at all                 │
└───────────────────────────┬─────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. AI assist — drafts + labels + checklists                 │
│    Coordinator approves every customer message              │
└───────────────────────────┬─────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. Tiered technician board — assign by level + load         │
└───────────────────────────┬─────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ 6. Cost & risk check — stay within INR 1,500 tool cap       │
└─────────────────────────────────────────────────────────────┘
```

---

## What we combined (nothing wasted)

| Source idea | Inside DICM as |
| --- | --- |
| Spreadsheet + inbox | Steps 1–2 input; not replaced |
| File-request (buy) | Text in AI draft emails (Step 4) |
| Rules queue (build) | Step 3 |
| Tiered technicians (build) | Step 5 |
| AI assist (build/buy) | Step 4 with human gate |
| Three-speed lanes (process) | Step 2 |
| Departure board (process) | Step 1 ordering |
| Rotating duty lead (process) | Step 1 facilitator |
| Daily huddle (process) | Step 1 ritual |

---

## Run the unified model

```text
cd Mystri-Applicant-Assessments/track-b
python3 experiment.py --write output/integrated_report.json
python3 -m unittest discover -s tests -v
```

JSON root object includes **`integrated_model`** with `collaboration_flow`, `comparison`, `cost_structure`, and all sub-layers.

---

## Why this is the “best combined” answer for Track B

- **Optimistic:** parallel manpower + AI speed + express lane  
- **Unique:** lanes + departure board + rotating lead + tiered techs in **one** pipeline  
- **Feasible:** Python stdlib prototype; no vendor lock-in  
- **Maintainable:** policy in code; AI swappable  
- **Risk-aware:** Park lane + approve gates + technician photo human check  
- **Cross-platform:** Windows / macOS / Linux, Python 3.10+

Decision detail and numbers: **`DECISION.md`**. Evidence: **`output/integrated_report.json`**.
