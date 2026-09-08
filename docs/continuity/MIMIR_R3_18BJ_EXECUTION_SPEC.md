# MIMIR R3.18BJ — Published R3.18BI One-Following-Payload Differential

**Status:** ACTIVE
**Pass type:** read-only published-production differential
**Production authority:** R3.18BI `def8e959239106e25d95091fcfcf468fec59e228` / `61ca1c3cdf504f4c1eaef3001cbe81984414c537`
**Production mutation:** forbidden
**Direct payload authority:** immutable R3.18BG artifact `10015405999`
**Next-control authority:** immutable R3.18BH artifact `10023482583` (observation only; production remains closed)
**Witness reselection:** forbidden

## 1. Goal

Validate published R3.18BI against exactly the immutable R3.18BG payload rows while preserving the surrounding false-terminator boundaries.

- Exactly the three BG authority rows must compose one production payload with bit semantics identical to BG and stop at exact `payload_end_bit`.
- The thirty-seven published R3.18BE false rows must reject before primitive payload decoding.
- The seven upstream R3.18AU false terminators remain outside the BE/BI success lane.
- The R3.18BH next `property_present` bit must remain unread. Changing that bit must not change the published BI result.
- No following stream ID, property header, payload, second later control, actor/frame state, or generalized cursor may be consumed.

## 2. Frozen authority

```text
published BI SHA/tree                 def8e959239106e25d95091fcfcf468fec59e228 / 61ca1c3cdf504f4c1eaef3001cbe81984414c537
BI parent                             2d8a2a28413467690b076bd08e6f750843af5c33
BI lib/test blobs                     2307ea008176d27208e2354c9706f09dc447fd5f / 16b15e1fa5dc71d295837578dff861635679ffc9
BI execution spec blob                e70e45a8a256d633c516895bbc28b61413af4b97
BI builder                            34158571800/101855439564 SUCCESS
BI validation PR                      #213 closed unmerged
BI exact-head PR CI                   34159120199/101857049780 SUCCESS
BI published-main CI                  34159530318/101858247592 SUCCESS
BG artifact                           10015405999 / sha256:a43a528a49fa6d07ef1c92266c6dc9ed4ef2a3e87e7f69f65f2f40d39f3fa15a
BG manifest                           sha256:b06097e08cc276e80e17543f36a3ab05ac184b335ec12ded0fd460e2129d5e46
BG exact rows                         3
BG tags                               Boolean=2 / Float=1
BG widths                             1 / 1 / 32 bits
BH head/tree                          c728658ac237a45f34b3af002c27f704f5293fb5 / 9761d42cd55d3152fe19653ea5be67efd826f2fa
BH evidence                           34132181073/101774645567 SUCCESS
BH artifact                           10023482583 / sha256:26e2bf42abe3d174949bc37b2e3e5e7e02a6caff2fa0490cbc9f3fa30626822d
BH manifest                           sha256:9eba3e774500eccf0fa1df06d98588ea945b237683594ebd0a8e89c3bad671aa
BH observed distribution              false=1 / true=2
pinned Boxcars                        c70e77df7af81b436cb545d070bb90c82f562d0b
```

R3.18BG and R3.18BH are immutable authorities. R3.18BJ may not reselect witnesses, infer a wider payload/tag/context set, or promote any false terminator into a successful production result.

## 3. Exact differential lane

For each exact BG authority row:

1. reconstruct the published prerequisites through R3.18BE;
2. call published R3.18BI exactly once;
3. require the embedded BE composition to equal the recomputed published BE result;
4. require the BI payload start/tag/value/width/end/stop to equal immutable BG authority exactly;
5. require a direct call to the existing primitive scalar decoder at the frozen BG start/tag to return the identical payload object;
6. require `BI.stop_bit == payload_end_bit`;
7. repeat and require bit-exact identical output;
8. flip the exact R3.18BH control bit at `payload_end_bit` and require the BI result unchanged;
9. truncate inside the payload and require atomic rejection;
10. stop without reading the BH bit or any later structure.

For surrounding negative lanes:

- all 37 BE-false rows must reject before payload decode;
- all 7 upstream AU-false rows remain outside BI success;
- no witness or context may be substituted to manufacture another true row.

Expected totals:

```text
published BI exact successes          3/3
Boolean / Float                       2 / 1
payload widths                        1 / 1 / 32
BG semantic/boundary mismatch         0
witness reselection                   0
BE false rejected                     37/37
upstream AU false excluded            7/7
BH control bits consumed              0
following stream/header/payload       0/0/0 bits
second later control                  0 bits
production mutation                   0
```

## 4. Required negative controls

At minimum:
- mutate/corrupt the supplied BE prior -> reject;
- wrong actor object -> reject;
- unresolved lookup -> reject;
- wrong exact K3 context or RL223 flip -> reject unless the complete resulting header tuple is independently admitted;
- wrong/fabricated payload tag -> reject;
- truncate each of the three payloads before exact end -> reject;
- poison only the exact BH bit at BI stop -> result unchanged 3/3;
- fabricated fourth BG row/context -> reject;
- all 37 BE false terminators -> no payload decode;
- all 7 upstream AU false terminators -> no BI success;
- source-scope guard -> one published-BE recomputation plus one primitive scalar decode, zero next-control reads, zero later stream/header/payload reads, no generalized/repeated loop.

## 5. Evidence artifact

Produce one privacy-safe immutable artifact containing exact BI SHA/tree/blob/spec and CI receipts, exact BG/BH authority receipts and artifact hashes, the three frozen successful witness identities and 37+7 negative-lane identities, per-row published-BI vs BG/direct-primitive comparison, tag/width/value/start/end/stop summaries, repeatability and negative controls, BH/later-consumption counters, production/Cargo/fixture/corpus/support mutation counters, same-head normal-CI receipt, privacy result and SHA-256 manifest.

## 6. Validation

Require exact witness identity 3/3; published BI exact 3/3; Boolean=2 / Float=1 and widths 1/1/32; BG semantic/boundary mismatch 0; direct primitive equality 3/3; repeatability PASS; all negative controls PASS; 37 BE-false rejected and 7 AU-false excluded; BH control / following stream / following header / following payload / second control consumption all zero; focused BI and prerequisite regressions PASS; full `mimir-replay` plus workspace fmt/check/test/clippy and repository verifier PASS; same-head normal CI SUCCESS; production/Cargo/fixture/corpus/support mutation 0/0/0/0/0; privacy scan PASS.

Before dispatch or rerun, inspect queued/waiting/in-progress equivalent runs and reuse an existing exact run. Rerun is never polling.

## 7. Hard stop

No R3.18BH control production, no next stream/header/payload, no second later control, no wider payload tag/context membership, no repeated/generalized property cursor, no next actor/frame/lifecycle mutation, and no raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.

## 8. Outcome gate

### Outcome A
Published R3.18BI matches immutable BG payload authority exactly on 3/3 rows, all surrounding false lanes remain closed, mismatch/reselection are 0/0, all validations pass, and BH/later consumption remains zero. A later separate bounded production pass may then consider exactly one R3.18BH-observed next control bit.

### Outcome B/C
Any narrower safe subset, authority drift, payload mismatch, false-lane payload access, BH-bit consumption, context widening, unrelated mutation or privacy failure keeps control production closed.
