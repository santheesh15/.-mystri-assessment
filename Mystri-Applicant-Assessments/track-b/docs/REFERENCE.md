# Reference — modules, helpers, constants, tests

## Entry points

| Script | Purpose |
| --- | --- |
| `starter.py` | Load CSV/JSON; smoke print row counts |
| `experiment.py` | Product 1 main run → report + trace + acks |
| `product1/verify_product1.py` | Submission gate (manifest + run + tests) |

---

## Python modules

| Module | Responsibility | Key exports |
| --- | --- | --- |
| `starter.py` | Data loader | `load_inputs()`, `load_csv()`, `DATA` |
| `experiment.py` | CLI orchestration | `main()` |
| `integrated_model.py` | DICM pipeline | `run_integrated_pipeline()`, `run_and_write_trace()`, `format_executive_summary()` |
| `queue_engine.py` | Follow-up rules | `triage_all()`, `triage_request()`, `RowResult`, `baseline_naive_pending()`, `proposed_ids()` |
| `data_policy.py` | Validation | `validate_all()`, `summarize_validation()` |
| `customer_registry.py` | Spam / contact match | `verify_customers()`, `summarize_customer_verification()` |
| `media_intake.py` | File sniff / QC | `assess_attachment()`, `assess_demo_pack()` |
| `customer_acknowledgment.py` | Receipt JSON | `build_all_submission_acknowledgments()`, `StructuredCustomerResponse`, outcome constants |
| `lane_model.py` | Lanes + board | `classify_case_lane()`, `prioritized_board()`, `duty_lead_for_snapshot()` |
| `team_workboard.py` | Tiered tasks | `build_team_board()`, `TECH_ROSTER`, `TASK_WORK_LEVEL` |
| `ai_assist.py` | Mock AI | `draft_reminder_email()`, `enrich_coordinator_tasks()`, `AiSuggestion` |
| `cost_model.py` | Scenario economics | `build_cost_structure()` |
| `approaches.py` | Hybrid ranking | `rank_approaches_for_daybreak()`, `hybrid_incorporation_summary()` |
| `pipeline_trace.py` | Audit log | `PipelineTrace`, `build_customer_deliveries()` |
| `console_io.py` | Windows UTF-8 | `configure_utf8_stdout()` |

---

## Helpers & utilities

| Helper | File | Notes |
| --- | --- | --- |
| `load_inputs()` | `starter.py` | Single dict: cases, requests, events, scenario |
| `configure_utf8_stdout()` | `console_io.py` | Call at start of `experiment.main()` |
| `_ascii_safe()` | `integrated_model.py` | Strip/replace Unicode for Windows console in summary |
| `_subprocess_env()` | `product1/verify_product1.py` | Windows UTF-8 for verify subprocesses |
| `_parse_ts()` | `queue_engine.py` | ISO datetime parse for rules |
| `sniff_format()` | `media_intake.py` | Magic-byte format detection |

No separate `utils/` package — helpers live next to domain modules (stdlib-only layout).

---

## Constants (by module)

### `queue_engine.py`

| Name | Value / role |
| --- | --- |
| `CLOSED_CASE_STATUSES` | completed, cancelled, scheduled |
| `INFO_ITEMS` | fault_photo, serial_number, site_access |
| `APPROVAL_ITEMS` | quote_approval |

### `data_policy.py`

| Name | Role |
| --- | --- |
| `CASE_STATUSES` | Allowed case status strings |
| `REQUEST_ITEMS` | Allowed request item types |
| `REQUEST_STATUSES` | pending, received |
| `FOLLOWUP_FLAGS` | 0, 1 |
| `CONTACT_RE` | `@example.invalid` pattern |

### `customer_registry.py`

| Name | Role |
| --- | --- |
| `FAKE_DOMAINS` | Spam domain set |
| `VALID_DOMAIN` | example.invalid |
| `SPAM_LOCAL_PART` | Regex for junk local parts |

### `media_intake.py`

| Name | Role |
| --- | --- |
| `SUPPORTED_IMAGE` | jpeg, png, webp, gif |
| `SUPPORTED_DOCUMENT` | pdf, plain_text, csv |
| `CONVERT_BY_HUMAN` | heic, unknown, etc. |

### `customer_acknowledgment.py`

| Name | Value |
| --- | --- |
| `SCHEMA_VERSION` | daybreak.customer_ack.v1 |
| `RECEIVED_OK` | received_ok |
| `RECEIVED_NOT_OK` | received_not_ok |
| `UNDER_REVIEW` | under_review |

### `team_workboard.py`

| Name | Role |
| --- | --- |
| `TECH_ROSTER` | T1–T4 metadata |
| `TASK_WORK_LEVEL` | Task → level mapping |

### `starter.py`

| Name | Role |
| --- | --- |
| `DATA` | Path to `data/` directory |

---

## Tests (`tests/`)

| File | Focus |
| --- | --- |
| `test_queue.py` | Rules, baseline, changed input, R018 uncertain |
| `test_integrated.py` | Pipeline report shape |
| `test_data_policy.py` | Validation |
| `test_customer_registry.py` | Spam / mismatch |
| `test_media_intake.py` | PNG/HEIC/unknown |
| `test_lanes.py` | Lanes, duty lead |
| `test_hierarchy.py` | Tiered board |
| `test_ai_assist.py` | Human gates |
| `test_customer_acknowledgment.py` | Structured receipts |
| `test_pipeline_trace.py` | Trace file end-to-end |
| `test_product1_gate.py` | Manifest / Product 1 files |

Run:

```bash
python -m unittest discover -s tests -v
```

**38 tests** when run from `track-b`.

---

## Documentation index

| Doc | Path |
| --- | --- |
| Project overview | `PROJECT_README.md` |
| Mystri brief | `README.md` |
| Products | `PRODUCTS.md` |
| Setup | `docs/SETUP.md` |
| Tech stack | `docs/TECH_STACK.md` |
| Architecture | `docs/ARCHITECTURE.md` |
| Configuration | `docs/CONFIGURATION.md` |
| Decision / handover | `DECISION.md`, `HANDOVER.md` |
| Sources | `SOURCES.md` |
| Data dictionary | `DATA_DICTIONARY.md` |

---

## External references

See **`SOURCES.md`** (OneDrive, Dropbox, Jotform, pack dictionary).

---

## JSON report shape (top level)

`integrated_report.json`:

| Key | Content |
| --- | --- |
| `integrated_model` | Full DICM dict from pipeline |
| `approach_ranking_top5` | From `approaches.py` |
| `pipeline_trace_file` | Path string |
| `customer_structured_responses` | Ack bundle |

Nested: `comparison.naive_pending_reminders`, `comparison.rules_based_drafts`, `triage_rows`, etc.
