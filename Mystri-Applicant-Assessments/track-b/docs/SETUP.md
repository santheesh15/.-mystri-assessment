# Setup — Product 1 (DICM Core)

## Prerequisites

| Requirement | Version / note |
| --- | --- |
| **Python** | 3.10 or newer (`python --version`) |
| **pip packages** | **None** — stdlib only |
| **Internet** | Not required to run (after clone/download) |
| **OS** | Windows 10+, macOS, Linux |
| **Disk** | ~5 MB project + generated `output/` |

---

## Get the code

**Repository:** `https://github.com/santheesh15/.-mystri-assessment`  
**Branch (use exactly):** **`cursor/track-b-submission-edb7`**

### Option A — Git (private repo; sign in to GitHub)

```powershell
git clone https://github.com/santheesh15/.-mystri-assessment.git
cd .-mystri-assessment
git checkout cursor/track-b-submission-edb7
cd Mystri-Applicant-Assessments\track-b
```

(or on macOS/Linux: paths with `/` and `python3`)

### Option B — ZIP

1. GitHub → branch **`cursor/track-b-submission-edb7`**
2. **Code → Download ZIP**
3. Extract; **`cd`** to `...\Mystri-Applicant-Assessments\track-b` (folder with **`experiment.py`**)

### Reviewer `cd` template (Windows)

**`<REPO_ROOT>`** = parent of **`Mystri-Applicant-Assessments`** (where you cloned or unzipped).

```powershell
cd "<REPO_ROOT>\Mystri-Applicant-Assessments\track-b"
dir experiment.py
```

---

## Setup steps

1. Install Python 3.10+ and ensure it is on `PATH`.
2. `cd` into **`track-b`** (folder containing `experiment.py`).
3. Do **not** modify Mystri **`data/*.csv`**.
4. Run verification (creates `output/` automatically).

---

## Setup commands

### Windows (PowerShell)

```powershell
cd "C:\path\to\...\Mystri-Applicant-Assessments\track-b"
python --version
python starter.py
python product1\verify_product1.py
```

If Unicode error on older zip: replace arrows in `integrated_model.py` or use updated branch; or:

```powershell
python -X utf8 product1\verify_product1.py
```

### macOS / Linux

```bash
cd Mystri-Applicant-Assessments/track-b
python3 --version
python3 starter.py
python3 product1/verify_product1.py
```

---

## Commands to generate outputs

All default outputs are written to **`track-b/output/`** in **one folder**.

### One command — verify + generate everything (recommended)

Creates/refreshes all outputs and runs tests.

**Windows:**

```powershell
cd "C:\path\to\...\Mystri-Applicant-Assessments\track-b"
python product1\verify_product1.py
```

**macOS / Linux:**

```bash
cd Mystri-Applicant-Assessments/track-b
python3 product1/verify_product1.py
```

**Produces:**

| File | Description |
| --- | --- |
| `output\integrated_report.json` | Full DICM JSON report |
| `output\dicm_pipeline_trace.log` | Unified audit trace |
| `output\customer_structured_responses.json` | Structured OK / not-OK receipts |

---

### Step-by-step — same outputs without full test gate

**Windows:**

```powershell
cd "C:\path\to\...\Mystri-Applicant-Assessments\track-b"
python starter.py
python experiment.py
```

**macOS / Linux:**

```bash
cd Mystri-Applicant-Assessments/track-b
python3 starter.py
python3 experiment.py
```

Terminal prints summary lines ending with:

```text
Wrote output/integrated_report.json
Wrote trace output/dicm_pipeline_trace.log
Wrote structured customer responses output/customer_structured_responses.json
```

---

### Explicit output paths (default flags)

**Windows:**

```powershell
python experiment.py `
  --write output\integrated_report.json `
  --trace output\dicm_pipeline_trace.log `
  --acks output\customer_structured_responses.json
```

**macOS / Linux:**

```bash
python3 experiment.py \
  --write output/integrated_report.json \
  --trace output/dicm_pipeline_trace.log \
  --acks output/customer_structured_responses.json
```

---

### Reviewer checklist (Windows — run in order)

**Branch:** **`cursor/track-b-submission-edb7`**. From PowerShell, after **`cd`** into **`track-b`**:

```powershell
cd "<REPO_ROOT>\Mystri-Applicant-Assessments\track-b"
python product1\verify_product1.py
notepad output\dicm_pipeline_trace.log
notepad output\customer_structured_responses.json
notepad output\integrated_report.json
notepad DECISION.md
notepad HANDOVER.md
```

Replace **`<REPO_ROOT>`** with your clone/ZIP folder (must contain **`Mystri-Applicant-Assessments`**). Run **`dir experiment.py`** to confirm.

1. First command must print **`PRODUCT 1 PASS`**.
2. **`notepad`** lines open the saved proof files (not opened by verify itself).
3. Do **not** change files in **`data/`** before step 1.

Optional: `explorer output` to open the folder in File Explorer.

### Open outputs after run (Windows)

```powershell
explorer output
notepad output\dicm_pipeline_trace.log
notepad output\customer_structured_responses.json
notepad output\integrated_report.json
```

**macOS:**

```bash
open output/
open -a TextEdit output/dicm_pipeline_trace.log
```

---

### Run unit tests only (does not replace output files)

```powershell
python -m unittest discover -s tests -v
```

```bash
python3 -m unittest discover -s tests -v
```

---

### Custom output folder (optional — e.g. Desktop)

See section below; **`verify_product1.py`** still requires default **`output/`** for **PRODUCT 1 PASS**.

---

Default: **`track-b/output/`**. To write elsewhere (e.g. Desktop):

**Windows:**

```powershell
$out = "$HOME\Desktop\daybreak-output"
New-Item -ItemType Directory -Force -Path $out | Out-Null
python experiment.py --write "$out\integrated_report.json" --trace "$out\dicm_pipeline_trace.log" --acks "$out\customer_structured_responses.json"
```

Official **`product1/verify_product1.py`** still expects default paths under **`output/`**.

---

## Environment variables

| Variable | Used? |
| --- | --- |
| None required | Product 1 has no secrets or API keys |

`verify_product1.py` may set `PYTHONUTF8=1` on Windows subprocesses (internal).

---

## Troubleshooting

| Symptom | Fix |
| --- | --- |
| `python` not found | Install Python; use `py` (Windows) or `python3` |
| `PRODUCT 1 FAIL` Unicode | Update from branch or `-X utf8`; see `console_io.py` |
| Wrong results | Check `data/` unchanged; snapshot in `scenario.json` |
| No `product1/` | Wrong branch/ZIP — use `cursor/track-b-submission-edb7` |

---

## Success criteria

```text
PRODUCT 1 PASS — DICM Core ready for Track B submission.
```

Plus 38 unit tests via verify subprocess.
