# MIMIR R3.18S — Following-Property Payload Contract / Evidence Discovery

**Status:** ACTIVE
**Pass type:** read-only evidence / payload-boundary and semantic contract discovery
**Production authority:** R3.18Q `f41c59d26ed6c810a640b4fa8cd76129decb32aa`
**Prior differential authority:** R3.18R `47bf441f2c795702e4ee75c66b4dbe710ccc9a9c` / `32044430149`
**Production mutation:** forbidden
**Another property control / repeated loop:** forbidden

## 1. Goal

Characterize exactly one following-property payload beginning at the already-proven R3.18Q `payload_start` over the same immutable 47-row lane. Establish exact payload end and, only where independently supported, semantic agreement for the observed `Boolean=39` and `ActiveActor=8` classes. Do not compose this payload into production.

## 2. Frozen authority

```text
canonical main before admission     196771bfc4193a9abf40f50577fbcebd37d0f131 / cbd655c600252c82ceb9d9d0db8a0c4942e7d45b
production SHA/tree                 f41c59d26ed6c810a640b4fa8cd76129decb32aa / 606db4b5778e5218f2bd0117cc5dd72d7f3e37a5
R3.18P contract SHA256              0dc2474a368a765c19cc49099fc61822954e9e29d1ce4ba8ad8fe21fe1fa181b
R3.18O artifact                     9284144768 / sha256:e6dc02f08ad025e816d772227a8c21a595902e45a9d71b5a9eb07c28fab4b94d
R3.18R evidence head/tree           47bf441f2c795702e4ee75c66b4dbe710ccc9a9c / 0dd95a0f8d4e8729191176d1e2614cbafd75d80e
R3.18R run/job                      32044430149 / 95429267025 SUCCESS
R3.18R same-head CI                 32044430126 / 95429266690 SUCCESS
R3.18R artifact                     9292549978 / 18820 bytes / sha256:142a2480f38a7ddc4f74e73dd9ce84ed70ccd740645f05d2e90579825927220f
```

Fresh-read all authorities before evidence. Any source drift, witness reselection or contract widening stops the pass.

## 3. Exact source lane

Reuse exactly the frozen 47 R3.18O/R3.18R rows and their exact R3.18Q following headers. Do not reselect easier rows or rebuild a broader Cartesian context set.

```text
following headers                   47
exact R3.18P contexts               18
Boolean payload candidates          39
ActiveActor payload candidates      8
version                             868.32 / net10 on all 47
witness reselection                 0
```

The observed tag counts are starting evidence only. They do not by themselves admit payload width, payload semantics or a production decoder.

## 4. Payload evidence procedure

For every frozen row:

1. reconstruct the already-admitted R3.18J prior, R3.18M true control and published R3.18Q following header exactly;
2. begin payload work only at that header's proven `payload_start`;
3. obtain an independently auditable native/oracle payload boundary and privacy-safe semantic result without consuming another `property_present` bit;
4. audit candidate lower-level decoder/model behavior separately for `Boolean` and `ActiveActor`; use an existing decoder only when its exact admitted context applies;
5. compare payload start, payload end, width and semantic value under that decoder's established comparison rules;
6. preserve the full R3.18P structural/version context of each witness; no tag-only or component-only widening;
7. stop exactly at the one following payload end and record zero another-control bits consumed.

`Boolean` and `ActiveActor` are independent evidence classes. Neither class may borrow width or semantics from the other, and repeated observations of one exact tuple do not widen any unobserved tuple.

## 5. Required negative controls

At minimum:

- truncation at every required payload boundary -> atomic reject;
- wrong tag/native-decoder pairing -> reject;
- wrong or unadmitted structural/version context -> reject;
- malformed payload encoding appropriate to the candidate class -> reject;
- repeated identical invocation -> exact identical result;
- bits after the proven payload end may be poisoned without changing the one-payload result;
- the next `property_present` bit may be poisoned or removed without affecting the one-payload result because R3.18S may not read it.

Real frozen rows must carry the core boundary evidence. Synthetic negatives may supplement but may not replace the 47-row lane.

## 6. Evidence artifact

Produce a privacy-safe immutable artifact containing at least:

- exact production/main/R3.18P/R3.18O/R3.18R authorities and receipts;
- exact frozen replay/witness identity and zero-reselection proof;
- per-row tag, exact seven-field context, payload start/end/width and semantic-comparison result;
- separate Boolean and ActiveActor aggregates;
- negative-control results;
- another-control consumption counter;
- production/Cargo/fixture/corpus/support mutation counters;
- SHA-256 for every evidence payload file.

Do not emit private raw payload windows or user-identifying replay metadata outside the already-approved privacy-safe identity scheme.

## 7. Validation

Require:

- exact 47-row frozen identity set and exact 18-context membership;
- deterministic double-run equality;
- all applicable independently justified native/oracle payload comparisons exact;
- focused existing decoder tests PASS;
- full `mimir-replay` PASS;
- workspace check/test/clippy PASS;
- full repository verifier PASS;
- same exact evidence head normal CI SUCCESS;
- privacy scan PASS;
- production/Cargo/fixture/corpus/support mutation `0/0/0/0/0`;
- another-control bits consumed `0`.

## 8. Hard stop

R3.18S may not change production Rust/Cargo/lockfile/fixtures/corpus/support lanes. It may not publish following-payload composition, read another property control/header/payload, create a repeated/generalized property loop or public cursor, widen R3.18P contexts, iterate the next actor/frame, mutate lifecycle state, materialize raw state/events, slice replays, mine skills, execute counterfactual rollouts or widen runtime/export behavior.

## 9. Outcome gate

### Outcome A

All 47 frozen following payloads are exactly characterized through one payload end under independently justified class/context rules, all applicable native/oracle comparisons are exact, negatives pass, witness reselection remains zero, another-control consumption is zero and mutation/privacy gates pass. Admit only the narrow payload evidence/contract. A later separate pass may propose bounded production composition.

### Outcome B

One tag/context subset is exact while another remains unresolved or outside an already-admitted decoder contract. Admit only the supported evidence facts and open a narrower follow-up contract/evidence pass. Production following-payload composition remains closed.

### Outcome C

Authority drift, witness reselection, native/oracle contradiction inside an admitted decoder context, privacy failure, production mutation, context widening or any another-control access. Stop without widening.
