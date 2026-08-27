# MIMIR R3.18AZ — Published R3.18AY One-Following-Payload Differential

**Status:** ACTIVE
**Pass type:** read-only published-production differential
**Production authority:** R3.18AY `2558cc0559422a3e6695e1501f20d96d83b23e6d` / `93198ad2a4f929ac62b87beddbc9d5b5665f08d1`
**Payload evidence authority:** R3.18AW `5f1d983a7b67f84293f337f23b7e7c25fee48795` / artifact `9643254651` / `sha256:9bf954cbb161a6ab37e72d04243e6b4aff5495e5d49799dbbbd71e32d0380fbc`
**Header contract:** R3.18AT `sha256:3c412a5fdf5ed647fbe2b2e4db1f3adf4e4f578ae07c58a302c261f6abafd0a5` / 16 exact eight-field tuples / multiplicity 40
**Later-control evidence:** R3.18AX false=37 / true=3 / artifact `9644869549` (evidence only; consumption forbidden)
**Production mutation:** forbidden
**Following control:** forbidden

## 1. Goal

Differentially validate the published R3.18AY bounded post-AU payload API against exactly the immutable forty-row R3.18AW payload authority. Prove the published composition itself reproduces the exact admitted Int/32 tag, start, end, width and lossless signed value and stops exactly at payload end.

The seven R3.18AU false terminators are not payload witnesses and must not be widened into the differential lane. They may be exercised only as fail-closed negative controls. The R3.18AX next `property_present` bit must remain unread.

## 2. Frozen authority

```text
R3.18AY production SHA/tree            2558cc0559422a3e6695e1501f20d96d83b23e6d / 93198ad2a4f929ac62b87beddbc9d5b5665f08d1
parent                                  dae58bc2d27aef2daac02b626ae37dbd309706bc / 06f5cb02daa94be784e7ab31aac101493bc8e959
lib / focused-test blobs                3742a0e856f51e50fd56ea963bb0bd6bac2d4b50 / f78956a22d0b2bb83e621cce24d88bce9484788b
AY execution spec blob                  d636344a63854b25f2be89540cf3dbf672a28b5c
AY clean-candidate CI                   33075136792/98527244393 SUCCESS
AY published-main CI                    33075583682/98528794945 SUCCESS
R3.18AT contract                        sha256:3c412a5fdf5ed647fbe2b2e4db1f3adf4e4f578ae07c58a302c261f6abafd0a5
R3.18AW evidence head                   5f1d983a7b67f84293f337f23b7e7c25fee48795
R3.18AW artifact                        9643254651 / sha256:9bf954cbb161a6ab37e72d04243e6b4aff5495e5d49799dbbbd71e32d0380fbc
R3.18AW payload identity                Int=40 / width32=40 / semantic range 5..300
R3.18AX evidence head                   465a3f2fc71e5eed6f00c16a04738031bef8d82c
R3.18AX artifact                        9644869549 / sha256:32f8b8056791280805da023e18ba73931f7caf4e2cf9e816411d4a0094bf97d9
R3.18AX control distribution            false=37 / true=3
pinned Boxcars                          c70e77df7af81b436cb545d070bb90c82f562d0b
witness reselection                     0
```

R3.18AW is the immutable payload authority. Historical R3.18AM/R3.18AN payload ordinal/value/boundary facts are not membership and may not be inherited.

## 3. Exact differential lane

For each of the exact forty AW payload witnesses:

1. reconstruct the exact valid published prerequisites through R3.18AU from the same witness;
2. invoke published R3.18AY exactly once;
3. require its retained/recomputed AU header authority to equal the frozen current authority;
4. require payload tag `Int`;
5. require payload start/end/width and final `stop_bit` to equal the R3.18AW row exactly;
6. require the privacy-safe lossless signed value to equal R3.18AW plus independent direct-native/oracle observation;
7. repeat and require bit-exact deterministic equality;
8. poison beginning exactly at AY `stop_bit`, including the AX control bit, and require the AY result to remain unchanged;
9. prove zero following-control and adjacent stream/header/payload consumption.

Expected totals:

```text
payload rows                    40/40
Int                             40
width32                         40
semantic range                  5..300
mismatch                        0
witness reselection             0
following-control consumption   0 bits
production mutation             0
```

## 4. Required negative controls

At minimum:
- all seven AU false terminators reject before payload decode;
- truncate any true row inside its 32-bit payload -> reject atomically;
- wrong actor -> reject;
- unresolved lookup -> reject;
- wrong exact version/context -> reject;
- corrupt/mismatched AU prior -> reject;
- wrong resolved tag -> reject;
- payload-start/header-stop mismatch -> reject;
- fabricated or historical-only header context -> reject;
- poison at exact payload end, including the AX bit, must not alter the valid result;
- source-scope guard proves one scalar payload primitive, zero control reads and no generalized/repeated cursor.

## 5. Evidence artifact

Produce one privacy-safe immutable R3.18AZ artifact containing exact AY SHA/tree/blob/CI receipts, exact AW/AT/AX authorities, forty frozen witness identities, per-row published-AY/AW/direct-native/oracle comparison, exact payload boundaries/widths/privacy-safe signed values, repeatability and negative-control results, following-control/adjacent-consumption counters, production/Cargo/fixture/corpus/support mutation counters, and a SHA-256 manifest/privacy result.

## 6. Validation

Require frozen witness identity 40/40, published AY exact 40/40, AW/direct-native/oracle exact 40/40, Int=40/width32=40, mismatch 0/witness reselection 0, all negatives and repeatability PASS, following-control consumption 0, focused AY/prerequisite regressions PASS, workspace fmt/check/test/clippy and repository verifier PASS, same exact evidence-head normal CI SUCCESS, production/Cargo/fixture/corpus/support mutation 0/0/0/0/0, and privacy scan PASS.

Before any dispatch or rerun, inspect queued/waiting/in-progress equivalent runs and reuse an existing exact run. Rerun is never polling. Use at most one validation-only PR for the exact evidence head if a natural CI cannot otherwise be obtained, and close it unmerged after SUCCESS.

## 7. Hard stop

No R3.18AX control consumption, no payload success on false terminators, no next stream/header/payload, no second later control, no generalized/repeated property loop/cursor, no next actor/frame/lifecycle mutation, and no raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.

## 8. Outcome gate

### Outcome A
Published R3.18AY matches all forty immutable AW payload witnesses exactly through payload end; mismatch 0; witness reselection 0; all negative/full validations PASS; following-control consumption 0; production mutation 0. Only then may a separate later pass consider production composition of exactly one AX-admitted next control bit.

### Outcome B
A reproducible bounded published-AY versus AW/direct-native/oracle mismatch or narrower safe subset exists. Record only the exact supported subset and keep control production closed.

### Outcome C
Authority drift, witness reselection, false-terminator widening, payload/context widening, R3.18AX control access, production mutation, generic chaining, privacy failure or validation contradiction. Stop without admission.
