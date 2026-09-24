# Mystri Track B submission

This repository folder contains **Track B only**.

| Path | Purpose |
| --- | --- |
| **`track-b/`** | All code, data, docs — **start here** |
| **`track-b/output/`** | Generated proof files (after verify or `experiment.py`) |
| **`briefs/`** | Track B assignment PDF only |

**Applicant total time:** 4 hours 35 minutes (275 min) — **`track-b/HANDOVER.md`**.

---

## Reviewers — GitHub login to verify

### 1) Repository and branch (use exactly)

| Item | Value |
| --- | --- |
| **Repository** | `https://github.com/santheesh15/.-mystri-assessment` |
| **Branch** | **`cursor/track-b-submission-edb7`** |

Sign in to GitHub (inviter must grant access). Open the repo → branch dropdown → select **`cursor/track-b-submission-edb7`**.

### 2) Get files on your computer

**Option A — Git**

```powershell
git clone https://github.com/santheesh15/.-mystri-assessment.git
cd .-mystri-assessment
git checkout cursor/track-b-submission-edb7
```

**Option B — ZIP**

On branch **`cursor/track-b-submission-edb7`**: **Code → Download ZIP** → extract.

### 3) `cd` syntax (replace with your path)

**`<REPO_ROOT>`** = the folder that **contains** `Mystri-Applicant-Assessments`  
(not `C:\Users\YourName` alone unless the repo is there).

```powershell
cd "<REPO_ROOT>\Mystri-Applicant-Assessments\track-b"
dir experiment.py
python product1\verify_product1.py
```

**Examples of `<REPO_ROOT>`:**

| How you got the code | Typical `<REPO_ROOT>` |
| --- | --- |
| `git clone` | `...\-.-mystri-assessment` |
| ZIP extract | `...\Downloads\<unzip-folder>` |

Expect terminal: **`PRODUCT 1 PASS`**. Do **not** edit **`track-b\data\`**.

### 4) Open proof (after PASS)

```powershell
notepad output\dicm_pipeline_trace.log
notepad output\integrated_report.json
notepad DECISION.md
notepad HANDOVER.md
```

Optional: `explorer output`

Full steps, macOS/Linux, screenshots: **`track-b/HANDOVER.md`**, **`track-b/docs/SETUP.md`**, **`track-b/PROJECT_README.md`**.

**Future scope (not graded):** **`track-b/docs/FUTURE_SCOPE.md`**.
