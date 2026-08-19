# MIMIR R3.18AB — Published R3.18AA Post-W Following-Header Differential Decision

**Date:** 2026-08-19
**Outcome:** **A — ADMITTED / READ-ONLY EVIDENCE**
**Production SHA:** `9392240c49f95766c214afee9865fed4155a87a4`
**Production tree:** `968520d480f78c528086e4e31b2ce307f4f8d232`

## Decision

R3.18AB is admitted Outcome A. The published R3.18AA production API was differentially validated on the exact immutable R3.18Y 47-row lane with zero witness reselection. For every row, the published AA result matched the frozen Y header and the direct stateless native header through `payload_start`; complete R3.18Z tuple membership and multiplicity reconstructed exactly; mismatch was zero.

R3.18AB consumed zero following-payload bits and zero another-control bits. It admits no payload decoder, later control, property loop/cursor or production source widening.

## Exact authority

```text
continuity base main/tree            713298a04bbb5491286e7f4ee5bf47a5d201b28c / 5cca2c6c15013895e01ab4acf083fed59f8023da
production SHA/tree                  9392240c49f95766c214afee9865fed4155a87a4 / 968520d480f78c528086e4e31b2ce307f4f8d232
production lib/test blobs            46523f47f94231362b60f8aee038e943e41c7972 / 7df8f84af37d771b12da1334bd195634e4cc6a54
R3.18Z contract SHA256               81f3072628ef78bcd71dacc1e31b5211aa0de9c32e922e01112b20f4df1425d9
R3.18Y authority                     32076198677 / 95529856476 SUCCESS
R3.18Y artifact                      9303584468 / sha256:46f3253cd50c95cfc05a39f2b45ed647b3d45d3951b0af78da3cf03803fcfd29
evidence head/tree                   __AB_HEAD__ / __AB_TREE__
authority run/job                    __AB_RUN__ / __AB_JOB__ SUCCESS
same-head normal CI                  __AB_CI_RUN__ / __AB_CI_JOB__ SUCCESS
artifact                             __AB_ARTIFACT__ / __AB_ARTIFACT_SIZE__ bytes
artifact digest / ZIP SHA256         __AB_ARTIFACT_DIGEST__
```

The downloaded final artifact ZIP SHA-256 must equal the GitHub Actions artifact digest exactly. The internal SHA-256 manifest covers every other evidence payload file and must verify exactly.

## Frozen result

```text
published R3.18AA rows               47/47
frozen-Y equality                    47/47
direct stateless-header equality     47/47
R3.18Z exact contexts                18/18
R3.18Z exact multiplicities          47/47
ActiveActor / Int / UniqueId         39 / 7 / 1
published/frozen/direct mismatch     0
witness reselection                  0
following payload bits consumed      0
another control bits consumed        0
production/Cargo/fixture/corpus/support mutation 0/0/0/0/0
privacy scan                         PASS
```

## Negative controls

Repeatability, prefix truncation before the post-W control/header boundary, wrong actor, unresolved lookup, wrong replay version/context and post-payload poison invariance pass on 47/47 frozen rows. The permanent R3.18AA focused suite retains fabricated-Cartesian and R3.18P-valid/Z-absent rejection. Focused R3.18AA tests pass 5/5 on the evidence head.

## Superseded evidence attempt

Initial evidence head `f2f79e47fefbe7ee95ea5df84c78a86868f57bb3`, run/job `32229955227 / 95997443235`, was not admitted. All positive/equality checks and every negative except truncation already passed 47/47; the byte-prefix truncation harness used `payload_start / 8`, which left complete header bytes available on 8 unaligned rows and therefore produced 39/47 rejection. The corrected authority cuts the byte prefix before the post-W control/header byte and separately removes an impossible same-head Knowledge Archive expectation because the evidence diff does not match that workflow's path filter. No production source change was involved.

## Hard stop

Production remains R3.18AA at `9392240c49f95766c214afee9865fed4155a87a4`. Post-AA following-payload composition, another `property_present` bit, repeated/generalized property loops or public cursors, next actor/frame iteration, lifecycle mutation, raw-state/event extraction, replay slicing, skill mining, counterfactual execution, runtime bridge and export widening remain closed.

## Next gate

R3.18AC is a separate read-only ordinal-3 following-property-payload evidence pass on the exact same 47 rows. It starts at AA `payload_start`, discovers payload width/subshape and semantic identity independently for the observed ActiveActor=39, Int=7 and UniqueId=1 classes against pinned Boxcars, and stops at one payload end without reading another property-control bit. UniqueId width/layout must be proven from its actual system id; no generic UniqueId width is inherited by assumption.
