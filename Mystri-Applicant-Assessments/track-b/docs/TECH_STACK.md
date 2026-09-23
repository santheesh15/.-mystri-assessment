# Tech stack — Product 1

## Summary

| Layer | Choice |
| --- | --- |
| Language | **Python 3.10+** |
| Dependencies | **Standard library only** |
| Data | **CSV + JSON** (Mystri pack) |
| Persistence | **File-based** (`output/`); no database |
| UI | **CLI** (terminal); no web framework |
| Messaging | **Simulated** (log + JSON); no SMTP/API |
| AI | **In-process templates** (`ai_assist.py`); no LLM API |

---

## Standard library modules (by area)

| Area | Modules |
| --- | --- |
| Data I/O | `csv`, `json`, `pathlib` |
| Time / rules | `datetime` |
| Types | `dataclasses`, `typing` |
| Media sniffing | `struct`, `base64`, `re` |
| Testing | `unittest` |
| Subprocess (verify gate) | `subprocess`, `os`, `sys` |
| Console (Windows) | `console_io` → `sys.stdout.reconfigure` |

---

## External services

**None** in Product 1. References to OneDrive/Dropbox appear in **draft text** and **`SOURCES.md`** only (claim check), not as live integrations.

---

## Supported platforms

| OS | Command | Notes |
| --- | --- | --- |
| Windows | `python` | cp1252 console: use UTF-8 fix in `console_io.py` / branch update |
| macOS | `python3` | |
| Linux | `python3` | |

---

## Version pinning

No `requirements.txt` — by design (Mystri pack). Minimum **Python 3.10** for type syntax used in codebase.

---

## Build / deploy

No build step. No Docker required. No CI config in Product 1 (run tests locally or via verify script).
