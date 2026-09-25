# Sources

| Source | Accessed | Supports | Limitation |
| --- | --- | --- | --- |
| [Microsoft — Create a file request (OneDrive)](https://support.microsoft.com/en-us/onedrive/create-a-file-request) | 2026-09-22 | Customers can upload files via a link without a Microsoft account; optional password/expiry | Describes collection only—not reminder cadence, opt-outs, or CRM/request-row sync |
| [Dropbox — Create a file request](https://help.dropbox.com/share/create-file-request) | 2026-09-22 | Similar file-collection pattern for “buy” alternative | Same gap vs Daybreak’s follow-up rules; price/plan not verified for INR budget |
| [Jotform — Approvals product overview](https://www.jotform.com/products/approvals/) | 2026-09-22 | Hosted approval workflows exist for quote-style decisions | Geared to form approvals, not appliance photo chase; adoption by email-only customers unproven |
| Mystri pack — `DATA_DICTIONARY.md` | 2026-09-22 | 48h gap, dry-run, excluded case statuses, uncertain handling | Synthetic snapshot; not production telemetry |
| Mystri pack — `USER_NOTES.md` | 2026-09-22 | Coordinator pain: duplicate reminders, off-thread photos | Fictional interviews—not market validation |
| [Microsoft Learn — Share files from OneDrive](https://learn.microsoft.com/en-us/onedrive/share-files) | 2026-09-25 | Upload/share links deliver files to a folder; permission-based access | Describes sharing mechanics—not reminder policy, opt-outs, or per-request row rules in Daybreak’s export |

**Unverified assumptions:** coordinator fully adopts a new queue; CSV exports stay as clean as the sample; customers accept email-only follow-ups.

## How I used these sources

- I used the **Microsoft OneDrive file-request** and **Microsoft Learn share-files** pages to test the owner’s “upload link fixes chasing” idea. I concluded they support **collection only**; they do **not** replace follow-up discipline in **`DECISION.md`**.
- I used **Dropbox file request** as a second “buy” pattern with the same limitation, to show the gap is not vendor-specific.
- I included **Jotform Approvals** because the brief allows quote-approval workflows; I judged it a weak fit for **fault_photo** chase but useful as an alternative for **quote_approval** rows later.
- I used **`DATA_DICTIONARY.md`** to implement **48h**, **uncertain**, and dry-run rules in code; I used **`USER_NOTES.md`** as fictional context only—not as market proof.
