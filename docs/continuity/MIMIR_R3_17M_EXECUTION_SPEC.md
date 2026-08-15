# MIMIR R3.17M Execution Spec — K4 Gameplay Structured Wire-Format Evidence

**Pass type:** read-only evidence
**Production implementation:** forbidden
**Production authority:** R3.17K, confirmed by R3.17L
**Continuity base:** `6b73a7e8f8639f8078dff0e656fc0fb9ea0bbc18`
**Production SHA:** `7390e3b145372252caaa8fa1fe3e0cd13b83336c`
**Pinned Boxcars:** `c70e77df7af81b436cb545d070bb90c82f562d0b`

## 1. Goal

Characterize the exact observed wire formats and context families for the R3.17 roadmap K4 gameplay-structured tags across the same frozen 47-replay supported lane:

```text
CamSettings
TeamPaint
TeamLoadout
ClubColors
Reservation
StatEvent
PlayerHistoryKey
DemolishFx
DemolishExtended
ExtendedExplosion
LoadoutsOnline
```

This pass gathers evidence only. It does not admit a K4 contract and does not add a native K4 decoder.

## 2. Frozen inputs

- supported replay lane: exact same 47 replay identities used by R3.17I/L
- replay identity SHA256: `b02488b13cd6374219bbb89f884b03f8356f3744f930e39b2279df34859015cf`
- R3.17L authority head: `0febcde7b312b6724e86ba156c700b41cf0562b7`
- R3.17L run/job: `31871353806 / 94980384463` SUCCESS
- R3.17L artifact: `9243555556`
- R3.17L artifact digest: `sha256:514580727df642ebde04d69824402db46ed48ff66755d4b17c0db6e69ac5eb3d`
- native K3 production SHA: `7390e3b145372252caaa8fa1fe3e0cd13b83336c`
- no support-lane widening

## 3. Evidence method

1. Verify fresh `main`, production SHA/tree/blobs, exact 47 replay identities and pinned Boxcars SHA before instrumentation.
2. Instrument pinned Boxcars at the already-resolved attribute payload boundary. Production MIMIR code remains untouched.
3. For every K4 occurrence, record exact payload start/end/width, replay version/net-version/RL223 context, tag, structural branch choices and exact subfield boundaries.
4. Build deterministic shape IDs from wire structure and branch choices, never from debug-string formatting.
5. Record frequency distributions by tag, shape, version/context and payload width.
6. Persist privacy-safe deterministic witnesses covering every observed shape/context family. Raw payload bytes may be used ephemerally for validation but must not enter durable public evidence.
7. Validate cursor monotonicity, packed-bit shape, replay identity and deterministic rerun accounting.
8. Keep production/Cargo/fixture/corpus/support-lane mutation at zero.

## 4. Per-tag evidence requirements

The instrumentation must expose enough internal cursor markers to reconstruct the exact read order and branch shape for each observed tag. Source-code inspection may guide marker placement, but **source code alone is not admission evidence**. A tag or branch with zero supported-lane occurrences remains unadmitted.

At minimum, capture every version/context-gated optional branch, collection count/length, nested identifier/reference choice, primitive field width/order, and exact subfield bit range needed to make a later contract deterministic. Do not flatten structurally distinct branches into one shape merely because their decoded values happen to match.

## 5. Required gates

```text
replay identity                         47/47
Boxcars oracle decode                   47/47
K4 occurrence accounting               exact + deterministic
observed shape classification          100%
unclassified/mismatch                  0
bit monotonicity failures               0
raw packed-payload shape failures       0
privacy                                 PASS
production mutation                     0
Cargo mutation                          0
fixture/corpus/support-lane mutation    0/0/0
```

For each of the 11 target tags, occurrence count must be reported explicitly. Zero occurrence is valid evidence of insufficiency, not permission to infer a contract from Boxcars source.

## 6. Outcome rules

**Outcome A:** every K4 tag/branch intended for the next contract is observed sufficiently, all observed occurrences are deterministically classified, cursor/raw-payload gates are clean, privacy passes, and all mutation counters are zero. Only then may the next pass admit evidence-supported K4 shapes.

**Outcome B:** one or more tags or material branches lack supported-lane evidence. Keep production closed and perform only targeted evidence work or explicitly narrow the future K4 contract to evidence-supported tags.

**Outcome C:** instrumentation or structural assumptions are contradicted. Stop and repair the evidence model before any K4 contract pass.

## 7. Hard stop

No production Rust, Cargo, fixture, corpus or support-lane changes. No K4 contract or native K4 implementation. No second property/property loop, next actor/frame, lifecycle mutation, raw-state extraction, events, replay slicing, skill mining, runtime or export widening.

If R3.17M closes with Outcome A, the next pass is a **separate K4 contract admission pass**. R3.18 remains closed until the R3.17 attribute-family dependency is explicitly satisfied.
