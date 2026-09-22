# Handover

- Name: *[Your full name — fill before sending]*
- Email used for this application: *[fill]*
- Chosen track: **B**
- Why this track: I prefer scoping a business/technical decision, checking a concrete claim against documentation, and proving it with a small runnable experiment rather than repairing an existing app.
- Approximate total time, including setup and handover: *[fill honestly]*

**Submission product:** **Product 1 — DICM Core** (`product1/README.md`, `PRODUCTS.md`). Products 2 and 3 are not included in this handover.

## Run and verify

Prerequisites: Python 3.10+, no third-party packages.

```text
cd Mystri-Applicant-Assessments/track-b
python3 product1/verify_product1.py
```

Or step by step:

```text
cd Mystri-Applicant-Assessments/track-b
python3 starter.py
python3 experiment.py
python3 -m unittest discover -s tests -v
```

Expected: **`experiment.py`** prints the **DICM collaboration summary**; writes **`output/integrated_report.json`**, **`output/dicm_pipeline_trace.log`**, and **`output/customer_structured_responses.json`**. **`verify_product1.py`** prints **`PRODUCT 1 PASS`**. Tests **38/38 OK**. Primary doc: **`INTEGRATED_MODEL.md`**.

## What I delivered

**Problem:** missing-info follow-ups using **one integrated model (DICM)** — coordinator + tiered technicians + rules + lanes + AI assist + existing tools.  
**Result:** **Product 1 (DICM Core)** — `integrated_model.py` orchestrates all in-scope pieces; see **`product1/README.md`**, **`INTEGRATED_MODEL.md`**, `DECISION.md`, `OPERATING_REPORT.md`.

## Evidence and limits

| Check | Command / artifact | Result |
| --- | --- | --- |
| Technical claim (file request ≠ follow-up policy) | `SOURCES.md` + `DECISION.md` | Documented gap |
| Baseline comparison | `experiment.py` | Baseline 13 vs rules 5; 8 IDs prevented |
| No-action input | `tests/test_queue.py` `test_no_action_when_all_requests_received` | 0 proposals |
| Changed input | `test_changed_input_blocks_recent_request` | R009 blocked when last request moved to 1h before snapshot |
| Edge case | `test_conflicting_pending_and_received_is_uncertain` | R018 → uncertain |
| End-to-end audit log | `output/dicm_pipeline_trace.log` + `tests/test_pipeline_trace.py` | START → CUSTOMER dry-run → END |
| Structured receipt OK/not-OK | `output/customer_structured_responses.json` + `tests/test_customer_acknowledgment.py` | JSON `receipt_outcome` + trace `CUSTOMER_ACK` |

**Changed-input expectation:** Setting R009’s `last_requested_at` to one hour before snapshot should block a draft; observed `exclude` with “need 48h” reason.

**Not proven:** real-world time savings, customer satisfaction, or LLM necessity—only that deterministic rules fit this snapshot better than a naive list.

**Next step:** pilot with coordinator labeling false positives on the uncertain queue.

## Tools and judgment

1. **AI coding assistant (Cursor / Composer)** — scaffolded `queue_engine.py` and tests; I verified logic against `DATA_DICTIONARY.md` and adjusted handling for conflicting `pending` + `received_at`.
2. **Manual calculation** — deduplicated `event_id` before summing minutes; caught that owner “8h/week” is not supported by logged minutes.
3. **Example catch:** Assistant initially used an invalid dataclass API; tests failed until replaced with `dataclasses.replace`—re-ran `unittest` before submitting.

Credit: Mystri starter `starter.py` and CSVs unchanged.
