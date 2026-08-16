# MIMIR R3.17P — Native K4 Real-Replay Differential Audit Decision

**Date:** 2026-08-16
**Pass:** R3.17P
**Outcome:** **A — ADMITTED / COMPLETE**
**Pass type:** read-only real-replay differential audit
**Production mutation:** none

## Frozen authority

```text
pre-audit canonical main     19e3f558bd343372c7fe863822ab961fb10976ad
production SHA               492cc8218be7abc6db8f75acaea33d009ab2f175
production tree              a66c47d7fb58da508188e64d42141987a0021a07
authority audit head         f2d87b732ad3103d50e2c047351f1017d4f3613f
authority run/job            31937527114 / 95141677175 SUCCESS
exact-head normal CI         31937527123 / 95141677140 SUCCESS
artifact                     9261118033
artifact digest              sha256:bc366b75e003531ba17351e880f259457ceba7cda702d912580c686990ba1beb
pinned Boxcars               c70e77df7af81b436cb545d070bb90c82f562d0b
R3.17N group SHA256          80c50783d70951bf125ccdadb818750a7ce35012891997f9b396241d84a9ae2b
```

The fresh-main audit before execution proved that `19e3f558bd343372c7fe863822ab961fb10976ad` differed from production only by the R3.17O continuity publication. The production Rust blobs remained exactly frozen.

## Admitted result

```text
replay identity              47/47
Boxcars oracle decode        47/47
exact group reconstruction   161/161
real witness group coverage  161/161
native decode success        161/161
tag variant match            161/161
context match                161/161
payload range match          161/161
structural shape match       161/161
semantic value match         161/161
mismatch count               0
bit monotonicity failures    0
packed payload failures      0
negative controls            PASS
privacy                      PASS
production mutation          0
Cargo mutation               0
fixture mutation             0
corpus mutation              0
support-lane mutation        0
```

The durable witness manifest, match rows and summary are privacy-safe. Account/player/title clear text was permitted only ephemerally inside the runner for semantic comparison.

## Numeric equality rule

The comparison rule was frozen before witness evaluation:

- `CamSettings`: exact raw IEEE-754 f32 bit identity for all compared fields;
- `DemolishFx`, `DemolishExtended`, `ExtendedExplosion` vectors: exact selected vector size, component width, raw X/Y/Z values and reconstructed f32 bit identity;
- integers, booleans, actor/object IDs, counts and version gates: exact equality;
- tolerance: **0**.

`LoadoutsOnline` used the exact caller-resolved object table materialized from the same replay as each witness. Product meaning was not inferred from the production branch being tested.

## Durable receipt hashes

```text
witness manifest SHA256      82e86cbbf03092f96484199d950587f52b061a2414eb9bc7cdf54abab57b083a
match rows SHA256            b87bf50cf3db618bda35fb90bd26230cfcfa77803812c81701b925a1af1d8201
summary SHA256               45fbe1de3b8b2b4c317ccbd15260d03ea1ddfb37fe07e25c0d11627741b66251
negative controls SHA256     b591f70c39092d179edcf60354c42b1808f0f4f8ac0e1ff8fb54ee84533f90d7
```

## Non-authority harness incident

The first disposable run `31937199601 / 95140880625` reached authority freeze, exact group reconstruction, semantic oracle rescan and 161/161 witness selection, then failed while compiling the external comparison harness because of a `serde_json::json!` expression syntax error. No production mismatch was observed. The corrected exact-head authority run `31937527114` repeated the substantive gates and is the only R3.17P authority.

## Boundary consequence

R3.17P certifies R3.17O's exact K4 one-value decoder against real replay evidence. It does **not** admit a second property or property loop.

The execution roadmap was re-read after Outcome A. The first dependency-valid unfinished step is R3.18: one complete existing-actor property update and exact end cursor before loop continuation. MIMIR therefore opens **R3.18A**, a read-only evidence pass for exactly one complete existing-actor single-property boundary.
