#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TRACK_A="${ROOT}/Mystri-Applicant-Assessments/track-a"

cd "${TRACK_A}"
python3 -m unittest discover -s tests -q
python3 app.py reset-demo
