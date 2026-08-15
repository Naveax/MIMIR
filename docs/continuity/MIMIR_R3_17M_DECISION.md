# MIMIR R3.17M Decision — K4 Gameplay Structured Wire-Format Evidence

**Outcome:** A — ADMITTED / COMPLETE
**Pass type:** read-only evidence
**Production implementation:** unchanged / forbidden in this pass

## Frozen authority

```text
continuity base              b1a4ad1a04623e3c8b002a7ea60817120b5fb551
production SHA               7390e3b145372252caaa8fa1fe3e0cd13b83336c
evidence authority head      a50f09857f36ac52cec30b4bf3efbde9e15bb564
authority run/job            31881779861 / 95005282281 SUCCESS
exact-head normal CI         31881779862 / 95005282149 SUCCESS
artifact                     9246249473
artifact digest              sha256:50839ba19f65feb92a2e79be30d36bf78fc4cc2e3280049cd591faf6846e2987
pinned Boxcars               c70e77df7af81b436cb545d070bb90c82f562d0b
replay identity SHA256       b02488b13cd6374219bbb89f884b03f8356f3744f930e39b2279df34859015cf
```

## Result

The frozen 47-replay lane was scanned twice with the same pinned Boxcars instrumentation. Both raw oracle logs were byte-identical and every durable analysis output was hash-identical.

```text
replay identity                         47/47 PASS
Boxcars oracle decode                   47/47 PASS
K4 occurrences                          39463
exact structural/context groups         161
privacy-safe witness rows               617
zero-occurrence target tags             0
unclassified occurrences                0
bit monotonicity failures               0
raw packed-payload shape failures       0
privacy                                 PASS
production/Cargo/fixture/corpus/support 0/0/0/0/0
outcome                                 A
```

## Target-tag coverage

- `CamSettings`: 6314 occurrences / 47 replay(s) / 1 observed shape(s)
- `TeamPaint`: 6498 occurrences / 47 replay(s) / 1 observed shape(s)
- `TeamLoadout`: 6443 occurrences / 47 replay(s) / 1 observed shape(s)
- `ClubColors`: 208 occurrences / 1 replay(s) / 1 observed shape(s)
- `Reservation`: 6392 occurrences / 47 replay(s) / 35 observed shape(s)
- `StatEvent`: 2279 occurrences / 47 replay(s) / 1 observed shape(s)
- `PlayerHistoryKey`: 3840 occurrences / 1 replay(s) / 1 observed shape(s)
- `DemolishFx`: 131 occurrences / 36 replay(s) / 12 observed shape(s)
- `DemolishExtended`: 16 occurrences / 2 replay(s) / 5 observed shape(s)
- `ExtendedExplosion`: 701 occurrences / 47 replay(s) / 1 observed shape(s)
- `LoadoutsOnline`: 6641 occurrences / 47 replay(s) / 73 observed shape(s)

The sparse tags are still real supported-lane evidence: `ClubColors` and `PlayerHistoryKey` occur in one replay each, and `DemolishExtended` occurs in two. Their admission may therefore cover only the exact observed structural/context groups, never inferred neighboring branches.

## Determinism and durable receipt

```text
first raw oracle log SHA256     ace53c1413c39da7afefa6ab73324e129bc8c1e660ceea2273e283ade0c73cb4
rerun raw oracle log SHA256     ace53c1413c39da7afefa6ab73324e129bc8c1e660ceea2273e283ade0c73cb4
raw oracle logs identical       true
analysis outputs identical      true
K4 groups JSONL SHA256          80c50783d70951bf125ccdadb818750a7ce35012891997f9b396241d84a9ae2b
K4 witnesses JSONL SHA256       acd66e4b1fc6f8c13228c7c67c24855760d55569957177915521d685949f80c3
summary SHA256                  0ae05ee497f27bf159ba3ca8b4d1ec59a8b3a131713883e72592024bf2ca59f8
aggregate SHA256                f6ff0d70d81afbd1db4f84cb3eaf47c8a6325aeca5bb0294071b678da352f82a
artifact ZIP SHA256             50839ba19f65feb92a2e79be30d36bf78fc4cc2e3280049cd591faf6846e2987
```

The downloaded artifact ZIP was independently re-hashed against GitHub's digest and all 12 receipt-listed durable files matched their recorded SHA-256 values. The durable witness surface contains structural replay/property identities, exact bit ranges, context, shape and structural witness hashes; it contains no raw payload field and no player/account identifier field.

## Admission boundary

R3.17M proves only the 161 exact observed structural/context groups represented by `r3_17m_k4_groups.jsonl`. It does **not** admit:

- Cartesian products assembled from independently observed subfields,
- zero-occurrence branches or version contexts,
- source-code-only Boxcars branches,
- a native K4 decoder,
- a second property, actor, frame or lifecycle transition.

`Reservation` contributes 35 observed shapes and `LoadoutsOnline` 73; those families especially require exact tuple/group membership rather than convenient field-union widening.

## Next pass

Open `R3.17N — K4 Evidence-Supported Contract Admission`. R3.17N is contract-only. Production Rust remains frozen at `7390e3b145372252caaa8fa1fe3e0cd13b83336c` until a later implementation pass is separately admitted.
