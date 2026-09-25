# Tool-use summary — Santheesh S — Mystri Track B

**Product 1 · 3 hours 50 minutes · sivasandy509@gmail.com**

I used AI and local tools under Mystri’s transparency requirement. My submission stands on what a reviewer can replay: **`python product1\verify_product1.py`** → **PRODUCT 1 PASS**, 39 unit tests on unchanged pack **`data/`**, and **`DECISION.md`** / **`SOURCES.md`**. I treat Composer as a fast draft layer; I own the decision, the rules, and the pass/fail gate.

I work with five habits on a timed build: keep the **human decision** and let AI handle drafts; **verify before trust** on every substantive code change; separate **file collection from follow-up policy**; **fail closed** on ambiguous rows such as R018; and state **honest limits** rather than overstating ROI or the owner’s eight-hour claim.

## Tools and how I governed their output

| Tool | What I used it for | How I checked / corrected / rejected |
| --- | --- | --- |
| **Cursor — Composer** | Scaffolding `queue_engine.py`, parts of `integrated_model.py`, test stubs, doc structure. No paid LLM API for graded runs. | `verify_product1.py` + full `unittest`; matched `DATA_DICTIONARY.md`; conflicts → **uncertain**. |
| **Python 3.10+** | Loader, `experiment.py`, verify gate, 39 tests, dry-run outputs. | **PRODUCT 1 PASS**; baseline **13** vs rules **5** in `test_pack_snapshot_baseline_thirteen_rules_five`. |
| **Manual analysis** | Deduped `event_id`; counts for `DECISION.md`. | Cross-checked CSVs/tests; did not treat owner 8 h/week as measured. |
| **Vendor documentation** | OneDrive/Dropbox file-request; Microsoft Learn share-files; Jotform for context. | `SOURCES.md` with dates, claims, limits. |

## Division of responsibility

| Role | Responsibility |
| --- | --- |
| **Composer** | Boilerplate, test skeletons, first-pass documentation. |
| **Me** | Rule semantics, evidence, Product 1 scope, SOURCES claims, pass/fail criteria. |
| **Reject rule** | Verify or tests fail → fix or revert; no failing AI output shipped. |

## Excluded from this submission

| Category | Reason |
| --- | --- |
| Paid LLM APIs | Graded proof uses stdlib + local verify. |
| Deployment / hosting | Dry-run assessment scope. |
| Live messaging | Simulated in trace/JSON only. |
| Editing pack `data/` | Verify assumes original Mystri CSVs. |

## Example I caught during implementation

Composer once emitted an invalid dataclass update in queue code. Unit tests failed immediately. I rejected that version, rewrote with **`dataclasses.replace`**, and re-ran the full suite and verify until **PRODUCT 1 PASS**.

| Step | Outcome |
| --- | --- |
| Problem | Invalid dataclass update in generated code. |
| Signal | Unit tests failed. |
| Action | Rejected assistant output; fixed with `dataclasses.replace`. |
| Proof | Full unittest + verify → **PRODUCT 1 PASS**. |

## Where this lives in the repo

| Artifact | Role |
| --- | --- |
| `DECISION.md` | Decision note with claim, alternatives, counterargument. |
| `HANDOVER.md` | Run steps, evidence, tool judgment. |
| `SOURCES.md` | External references and limitations. |
| `product1/verify_product1.py` | Single reviewer gate. |

**Repository:** `https://github.com/santheesh15/.-mystri-assessment` · **Branch:** `cursor/track-b-submission-edb7`

*Santheesh S · Track B*
