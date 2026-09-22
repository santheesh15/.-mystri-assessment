# Decision note — missing-information follow-ups at Daybreak Repairs

## Problem and user

**Users:** **one coordinator** (customer email, reminders, data cleanup) and **four technicians** (technical clearance—not bulk customer chasing).  
**Workflow:** after intake, cases need photos, access, or serial numbers before quoting. Industry-style improvement: **parallel lanes** so technicians prep quotes/review photo quality while the coordinator only handles eligible customer contact.  
**Problem chosen:** speed up missing-information flow **without** wrong reminders (opt-outs, already-sent photos, 48-hour gap) and route **messy/uncertain rows to humans** (coordinator inbox sync or technician visual photo check—not AI vision).

The export supports this focus: 24 cases include six still `waiting_info`, and 24 of 30 requests are `fault_photo` rows. Interview notes match the pain (duplicate reminders, photos arriving off-thread, incomplete logging). The data is weak on true calendar waiting time, technician effort, and whether quote value converts to profit—so I do not treat the owner’s “eight hours a week” as measured fact.

## Calculations (with data treatment)

1. **Logged coordinator effort:** `events.csv` has duplicate `event_id` deliveries; I counted each `event_id` once. Unique events = 124; summed `active_minutes` where present = **400 minutes** over the observation window (24 Aug–6 Sep 2026). That is ~**29 minutes per calendar day**, or ~**2.4 hours per five-day week** of *logged* admin time—not 8 hours. Many calls are unlogged per the coordinator note.
2. **Pending vs actionable:** At snapshot, **15** requests are `pending`. A naive spreadsheet rule (“remind every pending row with `followup_allowed=1`”) would target **13** rows. The rules engine in `experiment.py` proposes **5** dry-run drafts and flags **2** uncertain rows (e.g. R018: `pending` but `received_at` set).
3. **Mistake prevention on this snapshot:** The same naive baseline would include **8** request IDs that the rules engine rejects (closed cases, opt-out, 48-hour gap, or conflicting fields). Example: **R012** (`followup_allowed=0` on a case the customer asked not to chase) and **R029** (only ~46 hours since last request—below the 48-hour policy).

Duplicates in `events.csv` are ignored for counts. Blank `active_minutes` are treated as unknown, not zero. Conflicting `status` vs `received_at` are routed to **uncertain**, not auto-contact.

## Alternatives

| Option | Fit | Constraint |
| --- | --- | --- |
| **Microsoft OneDrive file request** | Customers can upload a photo without an account; helps *collection* | Does not reconcile inbox threads with request status or enforce 48-hour spacing (see SOURCES.md) |
| **Process-only: weekly stale-request review** | Uses existing inbox + spreadsheet; coordinator already works there | Relies on human discipline; easy to repeat reminders when status lags |
| **Custom rules queue (my experiment)** | Encodes published constraints; dry-run drafts only | Needs maintained rules and clean exports; not a messaging product |

## Technical claim investigated

**Claim:** A hosted “file request” product can replace the coordinator’s follow-up discipline for missing photos.  
**Check:** Microsoft’s OneDrive file-request documentation describes collecting files via a link and optional password/expiry—it does **not** describe case-level cooldowns, opt-out flags, or cross-thread matching to a request row.  
**Implication:** File-request tools address **upload friction**, not **eligibility to nudge**. That gap must be filled by process logic (human or deterministic code), not assumed away by “AI.”

## Recommendation

**Pilot a five-person operating model + small rules workboard (not an AI assistant):** coordinator owns **approved** customer drafts; technicians own **parallel prep and photo-quality checks** assigned by case (`T1`–`T4`). This is the optimistic industry pattern—**narrow automation where rules are clear, humans where judgment is required**—to shorten queue time without blasting customers. Defer paid workflow products until metrics exist. **What would change my mind:** measured cycle-time from `waiting_info` to quote with error rate on reminders unchanged or lower.

## Net value estimate (selected workflow: rules-assisted follow-up)

| Item | Assumption | Minutes/week |
| --- | --- | --- |
| Time saved triaging 15 pending rows | 2 min/row → 30 min saved vs manual scan | +30 |
| Review uncertain/excluded rows | 6 rows × 3 min | −18 |
| Tool cost | INR 1,500/month ≈ negligible vs labor in scenario | — |
| **Net (scenario)** | | **+12 min/week** (~0.2 h) |

This is **not** proof of the owner’s 8-hour claim; it is a narrow, honest band. Missing measurements: reminders actually sent, customer churn from bad nudges, and coordinator hourly cost.

## Next experiment with a real operator

**Question:** “When you sent a reminder you regretted, which rule would have stopped it?”  
**Continue if:** in a two-week pilot, ≥50% of proposed drafts are approved without edit and mistaken reminders do not increase. **Stop if:** uncertain queue grows faster than proposals or coordinators bypass the tool.
