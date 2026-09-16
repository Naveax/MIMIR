# MIMIR R3.18CA — One Following-Payload Evidence Decision

**Date:** 2026-09-16
**Outcome:** **A — CLOSED / READ-ONLY EVIDENCE**
**Canonical entry main:** `6ab5ee3423f74a34fbaacef32b98e5f3fd560b16` / `9afa6362ecd0613a9bda06c2261a704cde2847b8`
**Production authority:** R3.18BY `3b07e223fdf326e8100412fad9410bb1b66d2cb9` / `68b32f61d61c863b25e393cfa77575bac55217d7`
**Evidence authority:** `01ebdf5a8c7b192ef19a280711b3b0947f373647` / `116d2ef967bdbcd04d2af855be16fb865500854b`
**Evidence run/job:** `34989130467/104448878632` SUCCESS
**Same-head CI:** `34989130481` SUCCESS
**Artifact:** `10405136702` / `sha256:7e5e94df57fe51513ead7b7ed973bcce81c983f51603892fa9022227c8a05876` / 3602 bytes
**Artifact manifest SHA-256:** `a4670cdd141a2c12242542cf3788c01af331267c526b6d612c633ded01708341`
**Pinned Boxcars:** `c70e77df7af81b436cb545d070bb90c82f562d0b`

## Decision

R3.18CA satisfies Outcome A exactly. The immutable R3.18BY true continuation exposes one `LoadoutsOnline` payload at bit 3245; pinned Boxcars and the already-published R3.17O K4 decoder agree on the complete structural and semantic result. Existing K4 membership accepts the exact observed representation. No decoder/allowlist or production capability was widened during CA.

The BU=false `external_fixtures/sample_002.replay` row remains a terminator at bit 11240 and performs zero payload access.

## Exact admitted evidence

```text
true replay                         test_corpus/largest_100/079_1f838b01-66b5-4963-b62e-64f3d7dbd545.replay
true header context                 (110,6,67,LoadoutsOnline,868,32,10,false)
payload                             [3245,4227)
payload width                       982 bits
semantic SHA-256                    7641391ebd59828550db4ee24036b07a47a0bf40057c9c34024e5461787eb142
existing K4 membership              accepted
oracle repeat                       2/2
native repeat                       2/2
native/oracle structural match      true
native/oracle semantic match        true
truncation atomic rejection         3/3
post-payload poison                 PASS
false-row payload access            0
next property-control bits          0
second payloads                     0
witness reselection                 0
production/Cargo/fixture/corpus/support mutation 0/0/0/0/0
```

Exact structural shape:

```text
LoadoutsOnline:blue:outer28[g0:0();g1:0();g2:0();g3:1(Paint:new31);g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:1(Paint:new31);g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:0();g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]:orange:outer28[g0:0();g1:0();g2:0();g3:1(Paint:new31);g4:0();g5:0();g6:0();g7:0();g8:0();g9:0();g10:0();g11:0();g12:0();g13:0();g14:0();g15:1(Paint:new31);g16:1(UserColor:new32);g17:0();g18:0();g19:0();g20:1(UserColor:new32);g21:0();g22:0();g23:0();g24:0();g25:0();g26:0();g27:0()]
```

Witness multiplicity (`133` target-property witnesses; `75` same-shape witnesses) is evidence context only and is not a runtime-frequency promise.

The oracle build used Rust 1.86.0 solely to keep the pinned external Boxcars instrumentation buildable after registry dependency drift. MIMIR production remains on the repository Rust 1.85 floor; no production dependency or toolchain changed.

## Boundary consequence

Open R3.18CB as a separate bounded-production pass. It may compose exactly the one CA-observed `LoadoutsOnline` K4 payload after the already-valid R3.18BY true header, using only the existing R3.17O K4 decoder and exact existing membership. The false BY/BU row terminates unchanged.

## Hard stop

No K4 decoder/allowlist widening, no other header context/tag/shape, no false-row payload access, no next property-control bit after 4227, no second payload/following header, no generalized/repeated property cursor, and no actor/frame/lifecycle/raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.
