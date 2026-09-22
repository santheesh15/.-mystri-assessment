#!/usr/bin/env python3
"""Product 1 (DICM Core) submission gate — run from track-b root or this folder."""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

TRACK_B = Path(__file__).resolve().parent.parent


def _subprocess_env() -> dict[str, str]:
    env = os.environ.copy()
    if sys.platform == 'win32':
        env['PYTHONUTF8'] = '1'
        env['PYTHONIOENCODING'] = 'utf-8'
    return env


def _fail(msg: str) -> None:
    print(f'PRODUCT 1 FAIL: {msg}', file=sys.stderr)
    sys.exit(1)


def main() -> None:
    print('=== Product 1 — DICM Core verification ===')
    print('Root:', TRACK_B)

    manifest_path = TRACK_B / 'product1' / 'MANIFEST.json'
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))

    for rel in manifest['required_docs']:
        if not (TRACK_B / rel).is_file():
            _fail(f'missing required doc: {rel}')
    for rel in manifest['python_modules']:
        if not (TRACK_B / rel).is_file():
            _fail(f'missing module: {rel}')

    print('Manifest files: OK')

    starter = subprocess.run(
        [sys.executable, 'starter.py'],
        cwd=TRACK_B,
        capture_output=True,
        text=True,
        env=_subprocess_env(),
    )
    if starter.returncode != 0:
        _fail(f'starter.py failed:\n{starter.stderr}')

    experiment = subprocess.run(
        [sys.executable, 'experiment.py'],
        cwd=TRACK_B,
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='replace',
        env=_subprocess_env(),
    )
    if experiment.returncode != 0:
        _fail(f'experiment.py failed:\n{experiment.stderr}')
    if 'Wrote trace' not in experiment.stdout:
        _fail('experiment.py did not write trace (stdout missing confirmation)')

    for rel in manifest['outputs']:
        out = TRACK_B / rel
        if not out.is_file() or out.stat().st_size < 10:
            _fail(f'missing or empty output: {rel}')

    trace = (TRACK_B / 'output/dicm_pipeline_trace.log').read_text(encoding='utf-8')
    for needle in ('phase=START', 'CUSTOMER_ACK', 'DRY-RUN delivery simulated', 'phase=END'):
        if needle not in trace:
            _fail(f'trace missing: {needle}')

    acks = json.loads((TRACK_B / 'output/customer_structured_responses.json').read_text(encoding='utf-8'))
    if not acks.get('submission_receipts'):
        _fail('customer_structured_responses.json has no submission_receipts')

    report = json.loads((TRACK_B / 'output/integrated_report.json').read_text(encoding='utf-8'))
    model = report.get('integrated_model', {})
    comp = model.get('comparison', {})
    if comp.get('naive_pending_reminders', 0) <= comp.get('rules_based_drafts', 0):
        _fail('expected naive pending count > rules-based drafts on pack data')
    if not comp.get('prevented_bad_reminders'):
        _fail('expected prevented_bad_reminders non-empty')

    print('Outputs + trace + baseline check: OK')

    tests = subprocess.run(
        [sys.executable, '-m', 'unittest', 'discover', '-s', 'tests'],
        cwd=TRACK_B,
        capture_output=True,
        text=True,
        env=_subprocess_env(),
    )
    if tests.returncode != 0:
        print(tests.stdout, tests.stderr, sep='')
        _fail('unit tests failed (see output above)')
    ran_line = [ln for ln in tests.stdout.splitlines() if ln.startswith('Ran ')]
    print('Unit tests:', ran_line[-1] if ran_line else 'OK')

    print('')
    print('PRODUCT 1 PASS — DICM Core ready for Track B submission.')
    print('Grade this product only; Product 2/3 are not included yet (see ../PRODUCTS.md).')


if __name__ == '__main__':
    main()
