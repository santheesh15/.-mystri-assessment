# Product 1 — DICM Core (Track B submission)

This folder marks the **official scoped product** for Mystri Track B. All code lives in the parent `track-b/` directory; Product 1 is the **default behavior** of `experiment.py` (no extra flags required).

## Reviewer quick path (5 minutes)

1. Read **`../DECISION.md`** (recommendation + baseline math).  
2. Read **`../PROJECT_README.md`** and **`../docs/SETUP.md`** (prerequisites + commands).  
3. Run:

```text
cd Mystri-Applicant-Assessments/track-b
python3 product1/verify_product1.py
```

4. Open **`../output/dicm_pipeline_trace.log`** (tail: `CUSTOMER_ACK`, `CUSTOMER`, `END`).  
5. Skim **`../output/customer_structured_responses.json`** for `receipt_outcome` / `ok`.

## What Product 1 proves

- Rules-based drafts (**5**) vs naive pending chase (**13**); **8** bad IDs prevented on the pack snapshot.  
- Uncertain rows (e.g. **R018**) are not auto-contacted.  
- Coordinator + tiered techs + lanes + capped AI drafts in **one** daily pipeline (dry-run).  
- Customers get **structured** receipt feedback (OK / not OK / under review) in JSON + trace — simulated send only.

## What Product 1 does not claim

Production deployment, measured time savings, live LLM, or real customer delivery. See **`../HANDOVER.md`** → *Not proven*.

## Module map

See **`MANIFEST.json`** in this folder.
