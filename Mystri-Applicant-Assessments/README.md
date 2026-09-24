# Mystri Track B submission

This repository folder contains **Track B only**.

| Path | Purpose |
| --- | --- |
| **`track-b/`** | All code, data, docs — **start here** |
| **`track-b/output/`** | Generated proof files (created when you run verify or `experiment.py`) |
| **`briefs/`** | Track B assignment PDF only |

##  Order of Run(Windows PowerShell)

**Step 1 — verify** (runs tests and **writes / updates** these files under **`track-b\output\`**):

- `integrated_report.json`
- `dicm_pipeline_trace.log`
- `customer_structured_responses.json`

Terminal should show **`PRODUCT 1 PASS`**. Terminal text is not saved as a file; the proof is in **`output\`**.

```powershell
cd Mystri-Applicant-Assessments\track-b
python product1\verify_product1.py
```

**Step 2 — open outputs and narrative** (Notepad does not run automatically; run these after Step 1):

```powershell
notepad output\dicm_pipeline_trace.log
notepad output\customer_structured_responses.json
notepad output\integrated_report.json
notepad DECISION.md
notepad HANDOVER.md
```

Optional: `explorer output` to open the output folder in File Explorer.

Full detail, macOS/Linux, and screenshot: **`track-b/HANDOVER.md`**, **`track-b/PROJECT_README.md`**, **`track-b/docs/SETUP.md`**.

**Applicant total time:** 4 hours 35 minutes (275 min) — documented in **`track-b/HANDOVER.md`**.

**Future scope:** HTML dashboard, generic verify on changed data, live LLM/messaging/CRM — tech and build order in **`track-b/docs/FUTURE_SCOPE.md`**.
