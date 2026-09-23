# Setup — Product 1 (DICM Core)

## Prerequisites

| Requirement | Version / note |
| --- | --- |
| **Python** | 3.10 or newer (`python --version`) |
| **pip packages** | **None** — stdlib only |
| **Internet** | Not required to run (after clone/download) |
| **OS** | Windows 10+, macOS, Linux |
| **Disk** | ~5 MB project + generated `output/` |

Optional: Git (clone from GitHub) or ZIP download from branch `cursor/track-b-submission-edb7`.

---

## Get the code

### Option A — Git (private repo; sign in to GitHub)

```bash
git clone -b cursor/track-b-submission-edb7 https://github.com/santheesh15/.-mystri-assessment.git
cd .-mystri-assessment/Mystri-Applicant-Assessments/track-b
```

### Option B — ZIP

1. GitHub → branch **`cursor/track-b-submission-edb7`**
2. **Code → Download ZIP**
3. Extract; open `.../Mystri-Applicant-Assessments/track-b`

---

## Setup steps

1. Install Python 3.10+ and ensure it is on `PATH`.
2. `cd` into **`track-b`** (folder containing `experiment.py`).
3. Do **not** modify Mystri **`data/*.csv`** for baseline grading (tests assume pack snapshot).
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

## Custom output folder (optional)

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
