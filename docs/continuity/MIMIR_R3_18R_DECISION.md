# MIMIR R3.18R — Published Following-Property Header Differential Decision

**Date:** 2026-08-17
**Outcome:** **A — ADMITTED / READ-ONLY EVIDENCE**
**Production SHA:** `f41c59d26ed6c810a640b4fa8cd76129decb32aa`
**Production tree:** `606db4b5778e5218f2bd0117cc5dd72d7f3e37a5`

## Decision

R3.18R is admitted Outcome A. The published R3.18Q production API was differentially validated on the exact immutable R3.18O 47-row lane with zero witness reselection. R3.18Q's embedded R3.18M control matched the frozen control on 47/47 rows, its following header matched the direct stateless native header on 47/47 rows, the exact R3.18P seven-field contract reconstructed 18/18 contexts and 47/47 multiplicities, and native/oracle mismatch was zero.

R3.18R consumed zero following-payload bits and zero another-control bits. It admits no payload decoder, no later property control, no loop/cursor and no production source widening.

## Exact authority

```text
canonical pre-admission main        196771bfc4193a9abf40f50577fbcebd37d0f131
canonical pre-admission tree        cbd655c600252c82ceb9d9d0db8a0c4942e7d45b
production SHA/tree                 f41c59d26ed6c810a640b4fa8cd76129decb32aa / 606db4b5778e5218f2bd0117cc5dd72d7f3e37a5
evidence head/tree                  47bf441f2c795702e4ee75c66b4dbe710ccc9a9c / 0dd95a0f8d4e8729191176d1e2614cbafd75d80e
authority run/job                   32044430149 / 95429267025 SUCCESS
exact-head normal CI                32044430126 / 95429266690 SUCCESS
artifact                            9292549978 / 18820 bytes
artifact name                       r318r-published-following-header-differential-evidence
artifact digest / ZIP SHA256        sha256:142a2480f38a7ddc4f74e73dd9ce84ed70ccd740645f05d2e90579825927220f
R3.18P contract SHA256              0dc2474a368a765c19cc49099fc61822954e9e29d1ce4ba8ad8fe21fe1fa181b
R3.18O source artifact              9284144768 / sha256:e6dc02f08ad025e816d772227a8c21a595902e45a9d71b5a9eb07c28fab4b94d
continuity admission authority      32045289930 / 95431702360
```

The downloaded final artifact ZIP SHA-256 equals the GitHub Actions artifact digest exactly. The artifact contains nine files; `r3_18r_artifact_sha256.txt` covers the other eight evidence files and all eight entries verified exactly.

## Frozen result

```text
published R3.18Q rows               47/47
R3.18P exact contexts               18/18
R3.18P exact multiplicities         47/47
R3.18M control equality             47/47
stateless-header equality           47/47
native/oracle mismatch              0
Boolean rows                        39
ActiveActor rows                    8
version                             868.32 / net10
witness reselection                 0
following payload bits consumed     0
another control bits consumed       0
production/Cargo/fixture/corpus/support mutation 0/0/0/0/0
privacy scan                        PASS
```

## Negative controls

All frozen production-Q rows passed truncation, wrong-actor, unresolved-lookup, wrong-version, repeatability and post-payload-poison invariance: 47/47 in every class. Permanent R3.18Q focused tests also retained fabricated-Cartesian and component/tag/version widening rejection.

The evidence helper enforced an exact two-file disposable branch scope: `.github/workflows/_tmp_r318r_evidence.yml` and `tools/_tmp_r318r_run.sh`. Production, Cargo, fixture, corpus, support, docs and canonical source lanes were unchanged.

## Hard stop

Production remains R3.18Q at `f41c59d26ed6c810a640b4fa8cd76129decb32aa`. Following-property payload composition, another `property_present` bit, repeated/generalized property loops or public cursors, next actor/frame iteration, lifecycle mutation, raw-state/event extraction, replay slicing, skill mining, counterfactual rollout execution, runtime bridge and export widening remain closed.

## Next gate

R3.18S is a separate read-only following-property-payload contract/evidence discovery pass. It must reuse the exact same 47 following headers with zero witness reselection, characterize payload boundaries independently for the observed Boolean=39 and ActiveActor=8 classes, and stop at one payload end without reading another property-control bit. R3.18S may admit evidence/contract facts only; production payload composition requires a later separate pass.
