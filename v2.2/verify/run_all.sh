#!/usr/bin/env bash
# run_all.sh — one command for the v2.2 verification suite (added 15 Oct 2026, tenth amendment; §23.2 item 105; replica_checks.py added by the eleventh, item 107 — ~70 s, L <= 12 only).
# v33_checks.py added 16 Oct 2026 by the twelfth amendment, items 109–112 (35 extension checks).
# Usage:  cd /home/user/v2.2/verify && bash run_all.sh [--fast]
#   --fast   skips r7_check.py (≈1–2 min) and sector_probe.py (≈10 s per stratum; a probe, no pass/fail count).
# Each suite prints "N/N checks passed"; this script collects those lines and exits non-zero if any suite
# fails, is missing, or does not report a pass count. q_kernel.py needs the z3-solver package; it is installed
# on demand (sandbox packages do not persist across sessions).
set -u
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
cd "$(dirname "$0")"
FAST=0; [ "${1:-}" = "--fast" ] && FAST=1
python3 -c "import z3" 2>/dev/null || pip install -q z3-solver >/dev/null 2>&1 || echo "WARN: could not install z3-solver; q_kernel.py will fail"

# transfer_checks.py: thirteenth amendment / half-row and fourth-Clifford extension.
SUITES="opfibration_checks.py q_kernel.py primon_checks.py adelic_checks.py bst_checks.py clock_checks.py replica_checks.py v33_checks.py transfer_checks.py"
[ $FAST -eq 0 ] && SUITES="$SUITES r7_check.py"
status=0; total_pass=0; total_all=0
printf "%-26s %-12s %s\n" "suite" "result" "note"
for f in $SUITES; do
  if [ ! -f "$f" ]; then printf "%-26s %-12s %s\n" "$f" "MISSING" ""; status=1; continue; fi
  out=$(timeout 900 python3 "$f" 2>&1); rc=$?
  line=$(printf "%s\n" "$out" | grep -Eo '[0-9]+/[0-9]+ checks passed' | tail -1)
  if [ -z "$line" ]; then
    printf "%-26s %-12s %s\n" "$f" "NO-REPORT" "exit $rc: $(printf "%s\n" "$out" | tail -1 | cut -c1-80)"; status=1; continue
  fi
  p=${line%%/*}; a=$(printf "%s" "$line" | sed -E 's#^[0-9]+/([0-9]+).*#\1#')
  total_pass=$((total_pass+p)); total_all=$((total_all+a))
  if [ "$p" = "$a" ] && [ $rc -eq 0 ]; then printf "%-26s %-12s %s\n" "$f" "$p/$a" "ok"; else printf "%-26s %-12s %s\n" "$f" "$p/$a" "FAIL (exit $rc)"; status=1; fi
  printf "%s\n" "$out" > "${f%.py}.log"
done
if [ $FAST -eq 0 ] && [ -f sector_probe.py ]; then
  printf "%-26s %-12s %s\n" "sector_probe.py" "probe" "numerical probe, no pass/fail count; output in sector_probe.log"
  timeout 900 python3 sector_probe.py > sector_probe.log 2>&1 || true
fi
printf "%-26s %-12s %s\n" "quran corpus" "present" "$(ls quran 2>/dev/null | wc -l | tr -d ' ') files; q.py lookups used by §4.1 and §5 (no pass/fail count)"
echo "TOTAL ${total_pass}/${total_all} checks passed across $(echo $SUITES | wc -w | tr -d ' ') suites"
exit $status
