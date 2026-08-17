# MIMIR R3.18U — Published R3.18T Following-Payload Differential

**Status:** ACTIVE
**Pass type:** read-only published-API differential
**Production authority:** R3.18T `c2765ab9f04f9c981a6868cb6503bdf0e339ce1b`
**Production tree:** `a6f27fe606cd3446da02ef1cb8cf53fff071e383`
**Production mutation:** forbidden
**Later property control:** forbidden

## 1. Goal

Validate the published R3.18T bounded following-payload production API against the exact immutable R3.18S 47-row authority lane. Prove that the published composition reproduces the already-admitted R3.18Q header plus exactly one R3.18S payload, with exact boundary and semantic identity, and stops before another property-control bit.

## 2. Frozen authority

```text
production SHA/tree                 c2765ab9f04f9c981a6868cb6503bdf0e339ce1b / a6f27fe606cd3446da02ef1cb8cf53fff071e383
lib/test blobs                      cf992670b461e9d923e773ed375bef2b42aea20d / 430676ec118fa0755a9c64abc0067bf5c5c88d05
R3.18T implementation authority     32049639448 / 95445637593 SUCCESS
R3.18T candidate CI                 32049893219 / 95446478223 SUCCESS
R3.18T PR CI                        32050205389 / 95447503058 SUCCESS
R3.18T published CI                 32050650336 / 95448937493 SUCCESS
R3.18P contract SHA256              0dc2474a368a765c19cc49099fc61822954e9e29d1ce4ba8ad8fe21fe1fa181b
R3.18S artifact                     9293436309 / sha256:dac07647e288bfc3b177000e1bfa6b9cfd892b80fd77d46c2f4974a3832cf422
R3.18S frozen rows                  47/47
R3.18S exact contexts               18/18
R3.18S payload classes              Boolean=39×1 bit / ActiveActor=8×33 bits
```

Any production-source, contract, witness or artifact drift stops the pass.

## 3. Exact lane and comparison

Reuse exactly the 47 frozen R3.18S witnesses with zero reselection. For every row:

1. reconstruct the exact prior R3.18J second-payload result and required lookup/version context;
2. call the published R3.18T API once;
3. require the embedded R3.18Q control/header identity to match the frozen prior evidence;
4. require tag, payload start, payload end, payload width and typed semantic value to match R3.18S exactly;
5. require final `stop_bit` to equal the frozen payload end;
6. repeat the exact invocation and require byte/semantic equality;
7. stop. Do not read another property-control bit.

Expected immutable class counts are Boolean=39 and ActiveActor=8. They are not permission to widen to new structural/version contexts.

## 4. Required negative controls

At minimum:

- truncation through every required payload boundary -> atomic reject;
- wrong actor / unresolved lookup / wrong exact replay context -> reject through the existing fail-closed chain;
- fabricated or widened R3.18P context -> reject;
- wrong lower-decoder/tag pairing remains rejected by the admitted primitive/K2 boundaries;
- bits beginning exactly at the published R3.18T `stop_bit`, including the potential next control, may be poisoned without changing the one-payload result;
- repeated identical invocation -> exact identical result.

Both admitted payload forms have total fixed-width value domains. Do not invent a nonexistent invalid full-width bit pattern; truncation is the structural malformed-payload control.

## 5. Evidence artifact

Produce one privacy-safe immutable artifact containing:

- exact production/source/test/CI authorities;
- exact R3.18P and R3.18S receipts;
- replay identity + frozen witness identity and zero-reselection proof;
- per-row published T versus frozen S comparison;
- class/context aggregates;
- negative-control results;
- another-control consumption counter;
- production/Cargo/fixture/corpus/support mutation counters;
- SHA-256 manifest for all evidence payload files.

No private raw payload windows or user-identifying replay metadata may be emitted beyond the approved privacy-safe identity scheme.

## 6. Validation

Require:

- exact 47/47 frozen identity set and exact 18-context membership;
- published T versus frozen S mismatch `0`;
- Boolean rows `39` at width `1`;
- ActiveActor rows `8` at width `33`;
- deterministic double-run equality;
- all negatives PASS;
- another-control bits consumed `0`;
- production/Cargo/fixture/corpus/support mutation `0/0/0/0/0`;
- focused R3.18T tests PASS;
- full `mimir-replay`, workspace check/test/clippy and repository verifier PASS;
- same exact evidence-head normal CI SUCCESS;
- privacy scan PASS.

## 7. Hard stop

R3.18U may not mutate production or publish another control/header/payload. It may not create a generalized property loop/cursor, widen R3.18P contexts or payload tags, iterate another actor/frame, mutate lifecycle state, materialize raw state/events, slice replays, mine skills, execute counterfactual rollouts or widen runtime/export behavior.

## 8. Outcome gate

### Outcome A
Published R3.18T is exact on all 47 frozen rows with mismatch 0, all negative/mutation/privacy gates pass and another-control consumption remains zero. Admit only the published differential. A later separate pass may investigate exactly one next property-control bit.

### Outcome B
A bounded mismatch is isolated. Admit only supported facts and keep every later property-control boundary closed.

### Outcome C
Authority/witness drift, production mutation, privacy failure, context/tag widening or another-control access. Stop without widening.
