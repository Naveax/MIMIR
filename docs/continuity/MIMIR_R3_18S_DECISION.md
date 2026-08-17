# MIMIR R3.18S — Following-Property Payload Contract / Evidence Decision

**Date:** 2026-08-17
**Outcome:** **A — ADMITTED / READ-ONLY PAYLOAD CONTRACT EVIDENCE**
**Production SHA:** `f41c59d26ed6c810a640b4fa8cd76129decb32aa`
**Production tree:** `606db4b5778e5218f2bd0117cc5dd72d7f3e37a5`

## Decision

R3.18S is admitted Outcome A. On the exact immutable 47-row R3.18O/R3.18R following-header lane, an independently pinned Boxcars oracle and existing MIMIR lower-level decoders agreed exactly through one following payload end on all 47 rows with zero witness reselection and zero native/oracle mismatch.

The admitted payload classes are exactly the observed and validated forms:

```text
Boolean      39 rows / exactly 1 payload bit
ActiveActor   8 rows / exactly 33 payload bits = active:1 + actor:32
```

This evidence admits only the narrow payload contract for those exact R3.18P structural/version contexts. It does not by itself publish a production following-payload composition API and does not admit another property-control bit.

## Exact authority

```text
canonical pre-admission main        f2b644389b9d18c95fa13fd1ba5a32ce32d1145e
canonical pre-admission tree        efd0b7f5cae288a11a2ff9f0a9bca301d664a3c0
production SHA/tree                 f41c59d26ed6c810a640b4fa8cd76129decb32aa / 606db4b5778e5218f2bd0117cc5dd72d7f3e37a5
evidence head/tree                  7fed9a90d2cb1e356b2a388503650b434d7f3f87 / c552e5ef2cb8e7d1cb3b4022b3ff1ec6dc763989
authority run/job                   32047433925 / 95438466699 SUCCESS
exact-head normal CI                32047433876 / 95438466663 SUCCESS
artifact                            9293436309 / 18955 bytes
artifact name                       r318s-following-property-payload-evidence
artifact digest / ZIP SHA256        sha256:dac07647e288bfc3b177000e1bfa6b9cfd892b80fd77d46c2f4974a3832cf422
R3.18P contract SHA256              0dc2474a368a765c19cc49099fc61822954e9e29d1ce4ba8ad8fe21fe1fa181b
R3.18R source artifact              9292549978 / sha256:142a2480f38a7ddc4f74e73dd9ce84ed70ccd740645f05d2e90579825927220f
continuity admission authority      32047947277 / 95440106710
```

The downloaded final artifact ZIP SHA-256 equals the GitHub Actions artifact digest exactly. It contains ten files; `r3_18s_artifact_sha256.txt` covers the other nine and all nine entries verified exactly.

## Frozen result

```text
frozen following payloads           47/47
exact R3.18P contexts               18/18
Boolean rows / width                39 / 1 bit
ActiveActor rows / width             8 / 33 bits
native/oracle mismatch              0
witness reselection                 0
repeatability                       47/47
truncation negative                 47/47
wrong decoder negative              47/47
wrong exact context negative        47/47
post-payload/next-control poison    47/47 invariant
another control bits consumed       0
production/Cargo/fixture/corpus/support mutation 0/0/0/0/0
privacy scan                        PASS
```

For both admitted classes the full fixed-width bit domain is valid, so there is no fabricated invalid full-width bit pattern. Structural malformed evidence is therefore the truncation class, which rejected 47/47. This is an explicit negative fact, not a missing test disguised as one.

## Semantic identity

- `Boolean`: exact one-bit boolean semantic value matched Boxcars and `decode_replay_network_primitive_scalar_v1`.
- `ActiveActor`: exact `active: bool` plus signed 32-bit actor identifier matched Boxcars and `decode_replay_network_k2_v1`, total width 33 bits.
- payload start equals the already-proven R3.18Q following-header `payload_start` on every row;
- the pass stops exactly at the one payload end and reads zero bits of another property control.

## Hard stop

Production remains R3.18Q at `f41c59d26ed6c810a640b4fa8cd76129decb32aa`. Another `property_present` bit, another property header/payload, repeated/generalized property loops or generic cursors, context widening beyond exact R3.18P membership, next actor/frame iteration, lifecycle mutation, raw-state/event extraction, replay slicing, skill mining, counterfactual runtime and export widening remain closed.

## Next gate

R3.18T is a separate production implementation pass. It may compose exactly one following payload after the already-published R3.18Q following header, using only the admitted `Boolean | ActiveActor` lower-level decoders and exact R3.18P context. It must stop at that payload end and must not read another property-control bit. A successful R3.18T publication still requires a later separate real-replay differential audit.
