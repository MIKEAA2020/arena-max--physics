# Active closer-point experiment — inspect before restarting

Registered parent: `128-closer-common-rate-b2884612`. Check registered process liveness, OS PIDs, `n3_branch128_mid.json`, raw per-history JSON and actual NPZ checkpoints before any restart. Do not duplicate active/completed work or reset deadlines silently.

User selected `closer_point`: exactly p=.304825, chi128, both actual accepted .30480 states as warm sources, 60-minute overall cap, at most two single-thread CPU workers, unchanged external gates. The sources are NOT the small-order .30485 endpoints. Internal driver goal is 5e-8 for the same safety margin; no phase/pinning constraint. No extra rate, chi192 or stability campaign is authorized.

Original grid, original failed 3/4 pilot and separately accepted same-point refinement remain unchanged. The prior .30485 calculation ended with two small-order approximants; its arithmetic ranking sign flip is not a retained two-family bracket. Do not relabel history as phase or infer a physical spinodal/window width.

Current inputs/protocol/code hashes are `branch128-mid-protocol.json`; outcomes in `BRANCH128-MID-RESULTS.md`, `branch128-mid-report.docx`, CSV and raw `n3_branch128_mid.json`. All actual MPS states stay in the full Git checkout/workspace. To avoid duplicate high-chi arrays exhausting the 128 MiB snapshot budget, the compact review ZIP now includes code/observations/reports/control and low-chi fixtures, not chi>=96 states. No scientific checkpoint file was changed/deleted by that packaging policy. A fresh isolated ZIP extraction actually passed 17+35+49=101 checks.

Private PAT remains only at `.private/github-repository.pat`, mode 0600, outside publication inputs. Never echo or publish it. Helper repairs modes/askpass and restores an absent public clone when needed.

Mathematical blocks (65), protected framework sources (8) and the Qur'anic/Lighthouse real creator–creation distinction remain unchanged. v34 is author-review; original figure/SM, author approval and analytic audit remain outstanding.
