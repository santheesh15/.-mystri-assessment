# Handover

- Name: *[Your full name — fill before sending]*
- Email used for this application: *[fill]*
- Chosen track: **B**
- Why this track: I prefer scoping a business/technical decision, checking a concrete claim against documentation, and proving it with a small runnable experiment rather than repairing an existing app.
- Approximate total time, including setup and handover: *[fill honestly, ≤4 hours]*

## Run and verify

Prerequisites: Python 3.10+, no third-party packages.

```text
cd Mystri-Applicant-Assessments/track-b
python3 starter.py
python3 experiment.py --write output/queue_report.json
python3 -m unittest discover -s tests -v
```

Expected: starter prints 24/128/30 rows; experiment reports **5** proposed dry-run drafts, **23** excluded, **2** uncertain; tests **6/6 OK**. Report JSON at `output/queue_report.json`.

## What I delivered

**Problem:** coordinator follow-ups for missing photos/info without violating Daybreak constraints.  
**Result:** `queue_engine.py` + `experiment.py` implement a **rules queue** and compare it to a **naive “all pending” baseline** on the supplied CSVs. See `DECISION.md` for recommendation and net-value sketch; `SOURCES.md` for citations.

## Evidence and limits

| Check | Command / artifact | Result |
| --- | --- | --- |
| Technical claim (file request ≠ follow-up policy) | `SOURCES.md` + `DECISION.md` | Documented gap |
| Baseline comparison | `experiment.py` | Baseline 13 vs rules 5; 8 IDs prevented |
| No-action input | `tests/test_queue.py` `test_no_action_when_all_requests_received` | 0 proposals |
| Changed input | `test_changed_input_blocks_recent_request` | R009 blocked when last request moved to 1h before snapshot |
| Edge case | `test_conflicting_pending_and_received_is_uncertain` | R018 → uncertain |

**Changed-input expectation:** Setting R009’s `last_requested_at` to one hour before snapshot should block a draft; observed `exclude` with “need 48h” reason.

**Not proven:** real-world time savings, customer satisfaction, or LLM necessity—only that deterministic rules fit this snapshot better than a naive list.

**Next step:** pilot with coordinator labeling false positives on the uncertain queue.

## Tools and judgment

1. **AI coding assistant (Cursor / Composer)** — scaffolded `queue_engine.py` and tests; I verified logic against `DATA_DICTIONARY.md` and adjusted handling for conflicting `pending` + `received_at`.
2. **Manual calculation** — deduplicated `event_id` before summing minutes; caught that owner “8h/week” is not supported by logged minutes.
3. **Example catch:** Assistant initially used an invalid dataclass API; tests failed until replaced with `dataclasses.replace`—re-ran `unittest` before submitting.

Credit: Mystri starter `starter.py` and CSVs unchanged.
