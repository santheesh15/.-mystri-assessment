# Product 1 — DICM Core (Track B submission)

This folder marks the **official scoped product** for Mystri Track B. All code lives in the parent `track-b/` directory; Product 1 is the **default behavior** of `experiment.py` (no extra flags required).

## Reviewer steps (copy in order)

**Do not edit `../data/`** before running.

**Windows (PowerShell) — from `track-b` folder:**

```powershell
cd "C:\path\to\...\Mystri-Applicant-Assessments\track-b"
python product1\verify_product1.py
notepad output\dicm_pipeline_trace.log
notepad output\customer_structured_responses.json
notepad output\integrated_report.json
notepad DECISION.md
notepad HANDOVER.md
```

1. First command must print **`PRODUCT 1 PASS`** (this also writes the **`output\`** folder).
2. **`notepad`** lines open the proof files — verify does **not** open them automatically.

![Windows example: verify PASS and Notepad commands](../docs/assets/verify-product1-pass-windows.png)

**macOS / Linux:**

```bash
cd Mystri-Applicant-Assessments/track-b
python3 product1/verify_product1.py
# then open output/dicm_pipeline_trace.log, output/*.json, DECISION.md, HANDOVER.md
```

Full detail: **`../HANDOVER.md`**, **`../docs/SETUP.md`**, **`../PROJECT_README.md`**.

## What Product 1 proves

- Rules-based drafts (**5**) vs naive pending chase (**13**); **8** bad IDs prevented on the pack snapshot.  
- Uncertain rows (e.g. **R018**) are not auto-contacted.  
- Coordinator + tiered techs + lanes + capped AI drafts in **one** daily pipeline (dry-run).  
- Customers get **structured** receipt feedback (OK / not OK / under review) in JSON + trace — simulated send only.

## What Product 1 does not claim

Production deployment, measured time savings, live LLM, or real customer delivery. See **`../HANDOVER.md`** → *Not proven*.

## Module map

See **`MANIFEST.json`** in this folder.
