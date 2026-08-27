# MIMIR R3.18AZ — Published R3.18AY One-Following-Payload Differential Decision

**Date:** 2026-08-27
**Outcome:** **A — ADMITTED / READ-ONLY PUBLISHED-PRODUCTION DIFFERENTIAL**
**Production mutation:** none
**Canonical production remains:** `2558cc0559422a3e6695e1501f20d96d83b23e6d` / `93198ad2a4f929ac62b87beddbc9d5b5665f08d1`

## Decision

R3.18AZ closes Outcome A. Exactly the immutable forty R3.18AW payload witnesses were rematerialized without witness reselection and compared against published R3.18AY plus the admitted AW direct-native/Boxcars payload identities. Published R3.18AY matched tag, payload start, payload end, width and signed Int value on 40/40 rows with mismatch zero. All seven upstream AU false terminators remained outside the AY/AZ payload lane and were rejected before payload decode.

Every admitted payload is `Int/32`; the observed semantic range is 5..300, with one value 5 and thirty-nine values 300. Deterministic repeatability, truncation, post-stop poison isolation and prerequisite/context negatives pass. R3.18AZ consumed zero R3.18AX following-control bits and changed no production source, Cargo metadata, fixtures, corpus or support code.

## Exact authority

```text
canonical main/tree                    d12b7662a61571ecb43109ebbc753b790d37b6ad / b90fb38e7e16bfd3948219856eef29f9ac1bb8f2
canonical production/tree              2558cc0559422a3e6695e1501f20d96d83b23e6d / 93198ad2a4f929ac62b87beddbc9d5b5665f08d1
evidence head/tree                     f46479faa2b230f7fde474f7f7696a1024420879 / 0d022d27fda2275de9512d96231979e1d016491e
authority run/job                      33086674062 / 98568084290 SUCCESS
same-head natural CI                   33086674797 / 98568087263 SUCCESS
artifact                               9652520412 / 18151 bytes
artifact digest / downloaded ZIP       sha256:558c709e242d74150755565d07c7968853abad0a1de6c5f49cd8f5920e7f9fc4
inner manifest                         13/13 PASS
R3.18AW artifact                       9643254651 / sha256:9bf954cbb161a6ab37e72d04243e6b4aff5495e5d49799dbbbd71e32d0380fbc
R3.18AX artifact                       9644869549 / sha256:32f8b8056791280805da023e18ba73931f7caf4e2cf9e816411d4a0094bf97d9
R3.18AT contract                       sha256:3c412a5fdf5ed647fbe2b2e4db1f3adf4e4f578ae07c58a302c261f6abafd0a5
```

The downloaded artifact ZIP SHA-256 equals GitHub's artifact digest exactly. The ZIP contains 14 files; its SHA-256 manifest covers and verifies all 13 payload files.

## Frozen result

```text
frozen AW payload rows                 40/40
published AY exact                     40/40
AW native/oracle exact                 40/40
AU false terminators rejected          7/7
payload tag                            Int=40
payload width                          32 bits on 40/40
semantic range                         5..300
mismatch                               0
witness reselection                    0
following AX control bits consumed     0
production/Cargo/fixture/corpus/support mutation 0/0/0/0/0
privacy                                PASS
```

## Required negatives

```text
payload truncation                     PASS 40/40
repeatability                          PASS 40/40
post-stop AX-bit poison                PASS 40/40
wrong actor                            PASS
unresolved lookup                      PASS
wrong exact version context            PASS
wrong tag                              PASS
payload-start mismatch                 PASS
fabricated/historical context          PASS
source scope: one scalar / zero control-loop widening PASS
```

## Superseded scaffolding attempts

Earlier evidence SHAs were not scientific authority: `8d9043e7...` failed harness compilation; `7bd7e434...` reached the full 40/40 scientific differential but failed formatting; `2c5357e0...` exposed shallow-checkout ancestry and normal-CI evidence-environment isolation defects. None was rerun. The immutable authority is `f46479faa2b230f7fde474f7f7696a1024420879` and the success receipts above.

## Hard stop

R3.18AZ does not produce the R3.18AX-observed following control bit. It does not permit payload/control access on the seven false terminators, next stream/header/payload consumption, a second later control, a generalized/repeated property cursor, actor/frame/lifecycle advance, raw-state/event/replay-slice/skill/counterfactual/runtime/export widening, or historical boundary/value inheritance.

## Next gate

R3.18BA is a separate bounded production pass. It may validate/recompute exactly one valid published R3.18AY payload composition, begin exactly at that payload end, consume exactly one R3.18AX-admitted `property_present` bit, preserve the mixed false=37 / true=3 semantics, and stop exactly one bit later. It may not resolve a following stream, header or payload, read a second later control bit, or create a generalized property loop/cursor.
