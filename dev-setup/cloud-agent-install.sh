#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TRACK_B="${ROOT}/Mystri-Applicant-Assessments/track-b"

cd "${TRACK_B}"
python3 starter.py >/dev/null
python3 -V
echo "Track B data loader OK"
