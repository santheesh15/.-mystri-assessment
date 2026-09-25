# Tool-use summary — Santheesh S — Mystri Track B

**Product 1 (DICM Core)** · **3 hours 50 minutes (230 min)** · **sivasandy509@gmail.com**

---

## 1. Why I document tool use

Mystri asks for transparency on how I produced the submission. I treat **AI assistants as accelerators**, not authors of record. My **evidence** is what runs on the Mystri pack (`python product1\verify_product1.py` → **PRODUCT 1 PASS**, 39 unit tests) and what I wrote in **DECISION.md** / **SOURCES.md**. This note explains **which tools I used**, **why**, and **how I verified or overruled** their output.

---

## 2. My working theory (how I use AI on a timed assessment)

1. **Human owns the decision; AI owns drafts.** Business recommendation, rule semantics, and scope live in my decision note and code review—not in unchecked model text.
2. **Verify before trust.** Any AI-generated code path must pass the same gate a reviewer would use: integrated verify script + unit tests on **unchanged `data/`**.
3. **Separate “collection” from “policy.”** I used external docs to test whether file-request products replace *follow-up discipline*; I concluded they help **upload**, not **cooldowns, opt-outs, or row reconciliation**—that theory shaped DICM.
4. **Fail closed on ambiguity.** Conflicting CSV fields (e.g. **R018**: `pending` + `received_at`) go to **uncertain**, not auto-contact—whether the suggestion came from me or from the assistant.
5. **Credit and limits.** I state what is **not proven** (live savings, LLM necessity, owner 8 h/week) so the submission stays honest under time pressure.

---

## 3. Tools I used (mandatory disclosure)

### 3.1 Cursor — Composer (AI coding assistant)

| | |
| --- | --- |
| **What it is** | IDE-embedded agent (Composer) in **Cursor**; I used it as the primary AI pair-programmer for this repo. |
| **Model / settings** | Composer model as provided by Cursor at time of work; I did not tune custom temperature or run a separate paid API key for this submission. |
| **What I used it for** | Scaffolding **`queue_engine.py`**, parts of **`integrated_model.py`**, unit-test stubs, and first-pass documentation structure. |
| **What I did not use it for** | Final say on rule dispositions, evidence numbers in **DECISION.md**, or declaring success without **PRODUCT 1 PASS**. |
| **How I checked output** | Re-ran **`python product1\verify_product1.py`** and **`python -m unittest discover -s tests -v`** after substantive edits; read behaviour against **`DATA_DICTIONARY.md`**. |
| **How I corrected / rejected** | When generated code disagreed with dictionary rules or tests failed, I edited manually or reverted—see §5. |

### 3.2 Python 3.10+ (stdlib only)

| | |
| --- | --- |
| **What I used it for** | **`starter.py`**, **`experiment.py`**, integrated pipeline, **`product1/verify_product1.py`**, 39 tests, dry-run outputs. |
| **How I checked output** | Verify gate on pack data; baseline **13** vs rules **5** locked in **`test_pack_snapshot_baseline_thirteen_rules_five`**. |
| **Theory** | Deterministic rules on a fixed snapshot (**`scenario.json`**) give reviewers reproducible proof without cloud spend or credentials. |

### 3.3 Manual analysis (spreadsheet-style reasoning in code)

| | |
| --- | --- |
| **What I used it for** | Deduplicated **`event_id`** in **`events.csv`** before summing minutes; reconciled naive vs rules counts for **DECISION.md**. |
| **How I checked output** | Cross-checked CSVs, test output, and integrated report JSON. |
| **How I rejected a premise** | I did **not** treat the owner’s “8 hours/week” as measured fact—logged minutes in the window are far lower. |

### 3.4 Web / vendor documentation

| | |
| --- | --- |
| **What I used it for** | Microsoft OneDrive file-request, Dropbox file-request, Microsoft Learn share-files, Jotform Approvals (weak fit for photo chase). |
| **How I checked output** | Logged in **SOURCES.md** with access dates, supported claims, and explicit limitations. |
| **Theory** | I tested the brief’s implicit claim: “a buy tool fixes chasing.” Docs support **file collection**, not **Daybreak’s follow-up policy** in the export. |

---

## 4. What I deliberately did not use

- Paid **LLM API** keys or external inference for grading runs  
- **Deployment**, containers, or production messaging (email/SMS/WhatsApp)  
- **Customer interviews** or live CRM writes  
- Edits to Mystri **`data/*.csv`** for graded results  

This matches Track B constraints and keeps the experiment runnable offline after clone.

---

## 5. Concrete example — issue I caught and fixed

**Situation:** While implementing queue logic, Composer produced an **invalid dataclass update pattern**.

**Signal:** **Unit tests failed** immediately—not a cosmetic lint issue.

**My decision:** I **rejected** the assistant’s version rather than patching around failing tests.

**Fix:** Rewrote the update using **`dataclasses.replace`**, consistent with Python dataclass semantics.

**Verification:** Full **`unittest`** run, then **`python product1\verify_product1.py`** until **PRODUCT 1 PASS**.

**Lesson I apply:** AI output is a **draft** until verify + tests pass on the pack snapshot.

---

## 6. AI vs my judgment (summary)

| AI (Composer) | Me |
| --- | --- |
| Boilerplate modules and test skeletons | Rule semantics, uncertain routing, baseline interpretation |
| First-pass doc structure | Final numbers, word budget, scope (Product 1 only) |
| Speed on repetitive code | **Reject rule:** failing verify/tests → fix or revert, no narrative excuse |

---

## 7. Repository pointer (for reviewers)

**Repo:** `https://github.com/santheesh15/.-mystri-assessment`  
**Branch:** `cursor/track-b-submission-edb7`  
**Handover / evidence:** `Mystri-Applicant-Assessments/track-b/HANDOVER.md`, `DECISION.md`, `SOURCES.md`

---

*Santheesh S · Track B · Mystri applicant challenge*
