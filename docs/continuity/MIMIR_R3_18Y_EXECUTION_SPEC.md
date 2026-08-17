# MIMIR R3.18Y — One Following Property Header Evidence After Published R3.18W

**Status:** ACTIVE
**Pass type:** read-only structural evidence / one header only
**Production authority:** R3.18W `58872e94f00ef094807f21ab2ff984ac66b97d91`
**Evidence authority:** R3.18X Outcome A
**Production mutation:** forbidden
**Following payload:** forbidden
**Another property-control bit:** forbidden
**General property loop/cursor:** forbidden

## 1. Goal

On exactly the immutable 47 R3.18X/R3.18V witnesses, start at the published R3.18W `stop_bit`, independently identify and validate exactly one following existing-actor property header, and stop exactly at that header's `payload_start`. This pass characterizes the new structural contexts at this later boundary. It does not decode the payload.

## 2. Frozen authority

```text
canonical main before Y              continuity parent containing this spec
production SHA/tree                  58872e94f00ef094807f21ab2ff984ac66b97d91 / d6965d77903ea99dad0465bb350b6a673ee7dd00
production lib/W-test blobs          d997ae8c3ad2d201b3f43c6ccca7ded2ef03b73b / ac176135c2e6ed56f0b91bdde8c7548f17641cf0
R3.18X evidence head/tree            75259a9b3705b16b21d89b975ee584a7765e8134 / fe90b38c98039cd1dde05b96613645d0ab69a8a9
R3.18X authority                     32065498170 / 95496521378 SUCCESS
R3.18X same-head CI                  32065498109 / 95496518762 SUCCESS
R3.18X artifact                      9299790869 / 19761 bytes / sha256:ac32daa92d88f1753da34123d074dcd8f3c98c58fdeb0b91f89cb837ea02ebff
R3.18V source artifact               9297068554 / sha256:e17426aad6d476eba17bb471dc92cd24b4b4d8727ad427ad15fa6e9c1dda9eb2
frozen lane                          47 rows / true control 47 / false 0
```

Before evidence, fetch fresh `main`, prove production source/test identities remain exact, verify every X/V receipt and artifact digest/manifest, and prove witness identity with zero reselection.

## 3. Important non-inheritance rule

R3.18Y must **not assume** that the earlier R3.18P seven-field header contract applies at this later boundary. The prior P contract may be used only as historical methodology. Every stream bound, prop-id width, property object, attribute tag and version tuple at the Y boundary must be measured from the immutable Y witnesses and independently cross-validated.

No Cartesian expansion, same-name analogy or tag-only widening is allowed.

## 4. Required per-row evidence

For every frozen witness:

1. reconstruct exact published R3.18T through payload end;
2. invoke published R3.18W and require its true control start/value/end/stop to equal frozen X;
3. require the next header `property_present_start_bit` to equal the W control start and its `property_present_end_bit` to equal W stop;
4. independently establish the one-header oracle using pinned Boxcars observation-only instrumentation;
5. decode/measure exactly one header's:
   - stream-id start/end/value,
   - stream-id bound,
   - prop-id bit width,
   - resolved property object index,
   - resolved attribute tag,
   - version major/minor/net version,
   - payload-start bit;
6. require native/evidence-oracle equality for every recorded field and bit boundary;
7. stop exactly at `payload_start`.

The evidence must report exact unique structural tuples and multiplicities discovered on the 47 rows. Do not predeclare a context count or tag distribution.

## 5. Required negative controls

At minimum:

- truncation at each observed header sub-boundary;
- prior published-W stop mismatch;
- wrong actor context;
- unresolved/wrong stream lookup context;
- wrong version/context where applicable;
- repeat identical header observation -> exact equality;
- poison all bits beginning at `payload_start` -> header result unchanged;
- prove following payload bits consumed `0`;
- prove another property-control bit consumed `0`.

Synthetic cases may exercise surgical negatives, but admission requires the immutable real 47-row lane.

## 6. Artifact

Produce one privacy-safe immutable artifact with:

- exact main/production/lib/test/spec identities;
- exact X/V authority receipts and artifact digests;
- replay/witness identity hashes;
- pinned Boxcars SHA and evidence instrumentation hash;
- all 47 privacy-safe header rows;
- exact structural tuple/multiplicity summary;
- all negative results and adjacency-consumption counters;
- production/Cargo/fixture/corpus/support mutation counters;
- SHA-256 manifest for all evidence payload files.

## 7. Validation

Require:

- frozen identities 47/47; witness reselection `0`;
- published W reconstruction exact 47/47 before header observation;
- native/oracle header mismatch `0` for Outcome A;
- deterministic double-run equality;
- all required truncation/context/poison negatives PASS;
- following payload / another-control bits consumed `0/0`;
- focused W tests, full `mimir-replay`, workspace check/test/clippy and repository verifier PASS;
- same exact evidence-head normal CI SUCCESS;
- privacy PASS;
- production/Cargo/fixture/corpus/support mutation `0/0/0/0/0`.

## 8. Hard stop

R3.18Y may not decode the following payload, read another property-control bit, construct a repeatable/general property cursor or loop, iterate next actor/frame, mutate lifecycle state, materialize raw state/events, slice replays, mine skills, execute counterfactuals or widen runtime/export behavior.

## 9. Outcome gate

### Outcome A
All 47 one-header rows are exact, structural tuples are fully enumerable, all negatives/privacy/mutation gates pass, and the decoder stops at `payload_start`. Admit Y as read-only evidence only. A later separate pass may formalize an exact context contract if the observed tuple set is safely contractable.

### Outcome B
A reproducible mismatch or heterogeneous/unbounded context is isolated. Record the narrowed boundary and keep later composition closed.

### Outcome C
Authority drift, witness reselection, production mutation, payload/another-control access, privacy failure or loop/generalization. Stop without admission.
