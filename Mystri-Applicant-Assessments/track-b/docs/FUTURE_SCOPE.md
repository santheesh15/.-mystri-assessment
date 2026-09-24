# Future scope — Product 2 / 3 

**Product 1 (DICM Core) is complete and submitted.** Everything below is a **planned roadmap** — not built, not verified by `product1/verify_product1.py`.

Applicant: **Santheesh S** · Total effort on Product 1: **3 hours 50 minutes (230 min)** · See **`HANDOVER.md`**.

---

## Why a phased plan

Daybreak needs **fewer wrong reminders** and **clear human lanes** before adding AI or messaging. Product 1 proves **rules + dry-run pipeline** on the Mystri CSV snapshot. Next phases add **pilot tooling**, then **production integrations** — only if pilot metrics in **`DECISION.md`** are met (draft approval rate, uncertain queue size, no increase in bad reminders).

---

## Product lines (summary)

| Phase | Name | Goal |
| --- | --- | --- |
| **1** | DICM Core | Decision + rules experiment + dry-run evidence |
| **2** | DICM Pilot | Coordinator-facing tools on real folders; optional HTML report; flex verify |
| **3** | DICM Vision | Live messaging, CRM/Graph, production LLM, optional web app + DB |

Detail checklist: **`../PRODUCTS.md`**.

---

## Product 2 — DICM Pilot (planned enhancements)

**Intent:** Same rules engine as Product 1, but easier for a coordinator to **see, approve, and export** work — still **human-in-the-loop**, no autonomous send by default.

| Feature | Description | Tech (planned) |
| --- | --- | --- |
| **HTML / dashboard report** | One page summarizing triage, lanes, drafts, uncertain queue (instead of scrolling terminal) | Static HTML generated from JSON (`integrated_report.json` shape); optional small **Jinja2** or stdlib string templates |
| **Coordinator approval queue** | UI or structured file listing `propose` + `uncertain` rows for approve/reject/skip | JSON or SQLite queue; CLI or minimal **Flask/FastAPI** read-only UI |
| **Local intake folder** | Drop customer photos into `--intake-dir`; link to `media_intake.py` checks | **pathlib** watcher or manual folder scan; extend **`media_intake.py`** |
| **Generic dataset verify** | `verify_product1.py --generic` — run on changed CSVs without Mystri pack checks | Same stdlib stack; split **strict** (submit) vs **generic** (experiments) in verify script |
| **Richer media QC** | Blur/glare hints, HEIC → JPEG | **Pillow**; optional **Tesseract** OCR for serial numbers (technician still signs off) |
| **Export for reviewer** | Zip `output/` + trace + decision one-click | **zipfile** (stdlib) CLI flag on `experiment.py` |
| **Versioned AI prompts** | Replace inline templates with reviewed prompt files + audit log | Text files under `prompts/`; **`ai_assist.py`** loads file; log prompt hash in trace |

**Pilot success criteria (from decision note):** ≥50% of proposed drafts approved with little edit; mistaken reminders do not rise; uncertain queue does not grow faster than proposals.

**Estimated stack addition:** optional `requirements-pilot.txt` (Pillow, maybe Flask) — Product 1 stays stdlib-only.

---

## Product 3 — DICM Vision (production direction)

**Intent:** Connect to real Daybreak tools **after** rules and pilot behavior are trusted.

| Area | Planned capability | Tech (planned) |
| --- | --- | --- |
| **Email send** | Send only after coordinator approval | **SMTP** or **Microsoft Graph** sendMail; dry-run flag retained |
| **File collection** | OneDrive / Dropbox file-request links in live drafts | Graph API or vendor SDK; secrets in env / Key Vault |
| **Inbox triage** | Classify replies; suggest CRM status | **LLM API** (e.g. Azure OpenAI) with retrieval over case history; default **uncertain** |
| **Draft wording** | LLM drafts reminders; coordinator edits | Same LLM + **prompts/** versioning; cost cap (% of INR 1,500/month in **`cost_model.py`**) |
| **CRM / requests** | Sync request rows with spreadsheet or CRM | CSV export import first; later **REST** to CRM |
| **WhatsApp / SMS** | Optional channel per `requests.channel` | WhatsApp Business API — **opt-in only**, same rules gate |
| **Web app** | Technician + coordinator dashboards | **FastAPI** or **Django** backend; **React** or server-rendered templates |
| **Database** | Audit trail, approvals, send history | **PostgreSQL** or **SQLite** for pilot scale |
| **Observability** | Trace sends, LLM calls, rule overrides | Structured logs; optional **OpenTelemetry** |

**Explicit non-goals until metrics exist:** autonomous send, replacing 48h/opt-out rules with LLM judgment, claiming 8 h/week savings without measurement.

---

## Tech used today (Product 1) vs planned

| Layer | Product 1 (now) | Product 2 (pilot) | Product 3 (vision) |
| --- | --- | --- | --- |
| Language | Python 3.10+ | Same | Same |
| Dependencies | **Stdlib only** | + Pillow; optional Flask | + Graph/LLM SDKs, DB driver, web framework |
| Data | Mystri CSV + JSON | CSV + optional SQLite | DB + API sync |
| UI | CLI + `output/` files | HTML report + optional small web UI | Full web app |
| AI | Template functions in **`ai_assist.py`** | File-based prompts | Hosted LLM + audit |
| Messaging | Simulated in trace | Still dry-run default | SMTP / Graph / WhatsApp behind flags |
| Verify | **`product1/verify_product1.py`** strict on pack | Add **`--generic`** mode | CI + staging environment |

Full current stack: **`TECH_STACK.md`**. Architecture hooks: **`ARCHITECTURE.md`** → Extension points.

---

## How I plan to build it (order of work)

1. **Keep Product 1 frozen** — **`data/`**.
2. **Product 2a — visibility** — HTML report from existing JSON; document in README; no new business rules.
3. **Product 2b — pilot ops** — approval queue file format; coordinator records approve/reject; measure pilot KPIs.
4. **Product 2c — flex verify + intake folder** — support changed datasets and local photo drops without breaking strict verify.
5. **Product 3 — one integration at a time** — e.g. Graph file request + dry-run send log first; then LLM drafts with human gate; never skip **`queue_engine.py`** dispositions.
6. **Stop / continue** — use **`DECISION.md`** continue/stop rules; if coordinators bypass the tool, fix UX before adding AI.

---

## Where this is referenced in the repo

| Doc | Role |
| --- | --- |
| **`PRODUCTS.md`** | Product 1 vs 2 vs 3 boundary |
| **`DECISION.md`** | Business recommendation + pilot question |
| **`OPERATING_REPORT.md`** | Risks, maintainability, synthesis |
| **`INTEGRATED_MODEL.md`** | Daily pipeline narrative |
| **`RULES_AND_LIMITATIONS.md`** | What Product 1 does not claim |
