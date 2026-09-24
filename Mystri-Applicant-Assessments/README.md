# Mystri Track B submission

**Full reviewer guide (start → verify → read docs):** [`../README.md`](../README.md) at the **repository root** on branch **`cursor/track-b-submission-edb7`**.

This folder contains **Track B only** (summary below; detailed steps are in the root README).

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

Sign in to GitHub (inviter must grant access).

### Switch branch on GitHub (default is `main`)

The repo opens on **`main`** by default. **You must switch** before download or review:

1. Open `https://github.com/santheesh15/.-mystri-assessment`
2. Click the **branch** dropdown (left of the file list; it may say **`main`**).
3. Type or select: **`cursor/track-b-submission-edb7`**
4. Confirm the URL contains:  
   `.../tree/cursor/track-b-submission-edb7/...`  
   and you see **`Mystri-Applicant-Assessments`** (not an empty/old tree).

Then clone, ZIP, or browse files on **this** branch only.

### 2) Get files on your computer

**Option A — Git**

```powershell
git clone https://github.com/santheesh15/.-mystri-assessment.git
cd .-mystri-assessment
git checkout cursor/track-b-submission-edb7
```

**If you already cloned on `main`**, switch locally:

```powershell
cd .-mystri-assessment
git fetch origin
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
