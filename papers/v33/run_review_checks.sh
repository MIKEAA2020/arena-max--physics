#!/usr/bin/env bash
# Run only the A-1 paper-specific suites, not the unrelated time-framework suites.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
cd "$ROOT/v2.2/verify"
python3 replica_checks.py
python3 v33_checks.py
python3 transfer_checks.py
