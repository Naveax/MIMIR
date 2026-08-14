# MIMIR R3.17I — K3 Spatial/Physics Wire-Format Evidence Execution Spec

**Pass type:** read-only evidence
**Production implementation:** forbidden
**Production authority:** R3.17G Outcome A, confirmed by R3.17H Outcome A
**Oracle:** pinned Boxcars only

## Goal

Characterize the exact observed wire shapes for the roadmap K3 spatial/physics attribute family across the frozen 47-replay supported lane, without admitting or implementing a native K3 decoder.

```text
Location
RigidBody
ReplicatedBoost
PickupNew
```

## Frozen identities

```text
continuity base              2d338d4244ce07122bb97097c516193f68ff73b7
native production SHA        9bfa837c69c4751f70ca63a17c65f0f89877ff32
native source blob           7288238cfb5338653552435be6af41f0dd7a4e85
R3.17H authority head        9b8e8fe82ab5bdc663eecc3f5d3cd1e3b8ee38ac
R3.17H artifact              9222624242
R3.17H artifact digest       sha256:d6c773d593c3c50957507a19056e85aef8b769fdc03fd88c6d693b1258c0af28
pinned Boxcars SHA           c70e77df7af81b436cb545d070bb90c82f562d0b
supported replay lane        47
```

## Evidence method

1. Verify fresh main and the exact frozen native source blob before instrumentation.
2. Reuse the exact 47 replay identities already admitted by R3.17E/R3.17H; do not widen the corpus in this pass.
3. Instrument pinned Boxcars at the already-resolved attribute payload boundary and decode all four K3 tags while recording exact payload start/end/width and version/context.
4. Record field-boundary evidence sufficient to distinguish observed wire shapes:
   - `Location`: vector codec/context and exact component/payload boundaries.
   - `RigidBody`: sleeping flag, location, rotation representation/context, velocity presence branches and exact subfield boundaries.
   - `ReplicatedBoost`: exact field order/width for grant count, boost amount and the two remaining bytes.
   - `PickupNew`: optional instigator/reference branch, picked-up byte and exact branch boundaries.
5. Classify every observed occurrence into a deterministic shape identifier derived from actual wire structure, not from debug formatting alone.
6. Produce frequency distributions by tag, shape, version/net-version/context and payload width.
7. Select deterministic privacy-safe witnesses covering every observed shape/context family. Persist structural identities, bounded numeric/spatial values where safe, packed-payload hashes and exact bit ranges; do not persist unrelated player/account identity material.
8. Cross-check cursor monotonicity, packed-bit shape and exact replay identity. Production Rust, manifests, fixtures and corpus stay unchanged.

## Required evidence gates

```text
replay identity verification             47 / 47
oracle replay decode                     47 / 47
K3 occurrence accounting                 exact / deterministic
Location occurrences                     > 0 or Outcome B targeted evidence
RigidBody occurrences                    > 0 or Outcome B targeted evidence
ReplicatedBoost occurrences              > 0 or Outcome B targeted evidence
PickupNew occurrences                    > 0 or Outcome B targeted evidence
observed shape classification            100%
shape mismatch / unclassified            0
bit monotonicity failures                0
raw packed-payload shape failures        0
privacy scan                             PASS
production mutation                      0
Cargo mutation                           0
corpus / fixture mutation                0
```

If any tag has zero supported-lane occurrences, or an observed branch cannot be classified without guessing, use Outcome B and request only the targeted missing evidence. Boxcars source code alone is not enough to admit an unobserved branch.

## Evidence fields

Every durable occurrence/witness identity should be reproducible from a structural key including at least:

```text
replay identity
frame / actor ordinal
actor context
stream/property identity
attribute tag
version + net_version + relevant context gates
payload start bit
payload end bit
payload width
shape id
packed payload SHA256
```

Field-specific structural summaries may be stored only when they are required to prove the wire shape and are privacy-safe.

## Outcome rules

- **Outcome A:** all four tags are observed, every K3 occurrence is deterministically classified, cursor/raw-payload checks are clean, privacy passes and production/Cargo/corpus mutation is zero.
- **Outcome B:** supported evidence is insufficient for one or more tags/branches; request targeted evidence without widening production.
- **Outcome C:** oracle instrumentation or existing structural assumptions contradict reproducible replay evidence; stop and repair the evidence model before any contract pass.

## Hard stop

R3.17I must not change production Rust, Cargo manifests/lockfiles, fixtures, supported replay policy or downstream capability. It does not admit K3 decoding, second-property continuation, actor/frame iteration, lifecycle mutation, K4, raw state, events, replay slicing, skills, runtime or export.

## Next pass

Only on Outcome A open `R3.17J — K3 contract admission for evidence-supported shapes only`. R3.17J is contract-only; native K3 implementation must remain a later separate pass.
