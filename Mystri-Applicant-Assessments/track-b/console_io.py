"""Windows-safe console output for Track B CLI entrypoints."""
from __future__ import annotations

import sys


def configure_utf8_stdout() -> None:
    """Avoid UnicodeEncodeError on Windows cp1252 consoles (e.g. arrow in summaries)."""
    if sys.platform != 'win32':
        return
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, 'reconfigure', None)
        if reconfigure is None:
            continue
        try:
            reconfigure(encoding='utf-8', errors='replace')
        except (OSError, ValueError):
            pass
