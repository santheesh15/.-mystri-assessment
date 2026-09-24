# Handover

| Field | Your answer |
| --- | --- |
| **Name** | Santheesh S |
| **Email** | sivasandy509@gmail.com |
| **Total time** (setup + research + coding + tests + handover) | 4 hours and 35 minutes (275 min) |
| **Chosen track** | **B** |

- Name: Santheesh S
- Email: sivasandy509@gmail.com
- Approximate total time, including setup and handover: 4 hours and 35 minutes (275 min)
- Chosen track: **B**

## Time budget

| Activity | Minutes |
| --- | ---: |
| Read the scenario and inspect the data | 40 |
| Targeted external research | 55 |
| Analyze, compare and choose an approach | 40 |
| Build and check the experiment | 95 |
| Decision note, docs, verification, and handover | 45 |
| **Total, including setup and choosing Track B** | **275** |

Mystri’s brief targets **4 hours (240 min)**; this submission records **4 h 35 min** hours.

**Why this track:** I prefer scoping a business/technical decision, checking a concrete claim against documentation, and proving it with a small runnable experiment rather than repairing an existing app.

**Submission product:** **Product 1 — DICM Core** (`product1/README.md`, `PRODUCTS.md`).

## Run and verify (reviewer — copy all steps)

Prerequisites: Python 3.10+, no third-party packages. **Do not edit `data/`**.

**Step 1 — verify (creates `output/` files):**

```powershell
cd "C:\Users\SantheeshS\Documents\.-mystri-assessment-cursor-track-b-submission-edb7\Mystri-Applicant-Assessments\track-b"
python product1\verify_product1.py
```

*(Replace the path above if your folder is elsewhere.)*

Expected terminal line: **`PRODUCT 1 PASS`**.

![Example: PRODUCT 1 PASS then opening output and docs in Notepad](docs/assets/verify-product1-pass-windows.png)

**Step 2 — open saved outputs:**

```powershell
notepad output\dicm_pipeline_trace.log
notepad output\customer_structured_responses.json
notepad output\integrated_report.json
```

**Step 3 — read submission narrative (required):**

```powershell
notepad DECISION.md
notepad HANDOVER.md
```

For macOS/Linux Users: after verify, open the same paths under `output/` and the two Markdown files in any text editor (`docs/SETUP.md` has `open` examples).

Rules and limits: **`docs\RULES_AND_LIMITATIONS.md`**. Full command reference: **`docs\SETUP.md`**.

Or step by step (optional, without the Product 1 gate):

```text
cd Mystri-Applicant-Assessments/track-b
python3 starter.py
python3 experiment.py
python3 -m unittest discover -s tests -v
```

Expected: **`experiment.py`** prints the DICM collaboration summary; writes **`output/`** files. **`verify_product1.py`** prints **`PRODUCT 1 PASS`**. Full project guide: **`PROJECT_README.md`** and **`docs/`**. Tests **38/38 OK**. Primary narrative: **`INTEGRATED_MODEL.md`**, **`DECISION.md`**.

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

**Next step:** pilot with coordinator labeling false positives on the uncertain queue. **Future enhancements (Product 2/3):** **`docs/FUTURE_SCOPE.md`** (HTML report, generic verify, live LLM/messaging plan, tech stack).

## Tools and judgment

1. **AI coding assistant (Cursor / Composer)** — scaffolded `queue_engine.py` and tests; I verified logic against `DATA_DICTIONARY.md` and adjusted handling for conflicting `pending` + `received_at`.
2. **Manual calculation** — deduplicated `event_id` before summing minutes; caught that owner “8h/week” is not supported by logged minutes.
3. **Example catch:** Assistant initially used an invalid dataclass API; tests failed until replaced with `dataclasses.replace`—re-ran `unittest` before submitting.

Credit: Mystri starter `starter.py` and CSVs unchanged.
