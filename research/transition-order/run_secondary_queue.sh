#!/usr/bin/env bash
# One worker/core. Verification failure stops this queue before numerical pilots.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT/v2.2/verify/replica"
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
python3 -u ../transfer_checks.py > ../transfer_checks.log 2>&1
STAGE_SECONDS=120 CORR_RMAX=100 python3 -u secondary_campaign.py d3-mps > n3_d3_mps_pilot.log 2>&1
STAGE_SECONDS=120 CORR_RMAX=100 python3 -u secondary_campaign.py n4-mps > n4_haar_half_pilot.log 2>&1
L8_SECTOR_SECONDS=120 python3 -u secondary_campaign.py clifford8 > clifford4_L8_budgeted.log 2>&1
STAGE_SECONDS=900 MAXITER=400 CORR_RMAX=240 \
RESUME_STATE=checkpoints/n3_disordered_latest.npz \
CASE_FILE="$ROOT/research/transition-order/cases-disordered-critical.json" \
python3 -u order_campaign.py disordered > order_disordered_critical.log 2>&1
