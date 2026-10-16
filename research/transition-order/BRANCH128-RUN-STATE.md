# Pilot stopped at declared validation gate

Parent `128-branch-following-pilot-acaecab5` exited 0, but only 3/4 continuation steps passed. At common .30480 the small-order history reached the primary tolerance; its right compatibility residual was 1.0001650127505745e-7, above the 1e-7 ceiling. It was not accepted, and full-period evaluation was not run on that rejected step. Do not relabel or round it into acceptance. All tensors and earlier source states are preserved. No crossing or stability certificate.

Full regression `branch-pilot-release-verificatio-39b4e39c` exited 0 (246/246); data audit separately confirms the accepted states and the rejected gate. Any same-point refinement is a separately recorded convergence-safety amendment, not an unnoticed restart or threshold relaxation. No new rate or chi192 is authorized.

Private PAT remains only in `.private/github-repository.pat`, mode 0600, excluded from public inputs. Never echo it.
