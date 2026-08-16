# MIMIR R3.18C — Existing-Actor Property-Loop Terminator / Continuation Evidence

**Status:** ACTIVE
**Pass type:** read-only real-replay evidence
**Production mutation:** forbidden
**Second property payload:** forbidden

## 1. Goal

Prove the first loop-control edge immediately after the published R3.18B one-property composition.

For deterministic real existing-actor updates whose first property resolves to an R3.18B-admitted K1 scalar, prove that:

```text
native R3.18B stop_bit
== pinned Boxcars first-property payload end
== pinned Boxcars next property_present start bit
```

Then an evidence-only native probe may read exactly that one next `property_present` bit and must stop immediately afterward.

This is evidence for loop control, not implementation of a production property loop.

## 2. Frozen authority

```text
canonical main / production  de7a2ba40663bb619ca7bd8654846ce87670d023
production tree              d1889038ca2eaeb8bb0f05e44b811d906f84cf6e
parent                       f12365b43029f19f3ab1dd889e651f9781b0655e
lib.rs blob                  478ae5b70514fcff79117b834733849517c48500
R3.18B focused test blob     927e9a2c834115d1c918fa96fb6d0690bd03965e
R3.18B exact validation      31942696817 / 95154052998 SUCCESS
R3.18B published main CI     31942870294 / 95154460239 SUCCESS
R3.18B published validator   31942896666 / 95154519828 SUCCESS
R3.18A oracle authority      12ee215fd843260d5ece14f27aa1171cb862f49e
R3.18A evidence run/job      31941400273 / 95151024131 SUCCESS
pinned Boxcars               c70e77df7af81b436cb545d070bb90c82f562d0b
supported replay lane        exact 47-replay identity lane
```

Before evidence work, re-read fresh `main` and verify the production SHA/tree/source blobs above. Any drift requires a new ancestry/source audit before continuing.

## 3. Witness selection

Regenerate or reuse the exact 47-replay identity lane under immutable SHA checks. With pinned Boxcars instrumentation, enumerate real existing-actor updates where:

1. the first property is present;
2. its resolved tag is one of `Boolean`, `Byte`, `Enum`, `Float`, `Int`, `Int64`;
3. Boxcars reaches the first payload end cleanly;
4. the following `property_present` bit exists.

Deterministically select:

- at least one **terminator** witness with next `property_present = false`;
- at least one **continuation** witness with next `property_present = true`;

if both classes exist in the frozen lane. If one class does not exist, do not manufacture a synthetic admission claim; record the evidence gap and choose Outcome B/C as appropriate.

Selection order must be deterministic, for example lexicographic replay label then frame index then actor ordinal/ID.

## 4. Required comparisons

For each selected witness, prove:

```text
replay identity                          exact
frame / actor identity                   exact
first property stream/property/tag       exact
first property semantic value            exact for the admitted K1 type
native first payload start               == oracle start
native first payload end / stop_bit      == oracle end
oracle next property_present start       == native stop_bit
native evidence bit value                == oracle next property_present value
native evidence stop                     == native stop_bit + 1
```

For a **terminator** witness additionally prove:

```text
next property_present = false
loop-control end = start + 1 bit
second stream bits consumed = 0
second payload bits consumed = 0
```

For a **continuation** witness prove only:

```text
next property_present = true
continuation exists
native probe stops immediately after that one bit
```

The native probe must not decode the second stream ID, resolve the second property header, or decode the second payload.

## 5. Negative and boundary controls

Required evidence controls:

- truncate exactly before the next `property_present` bit and require failure without cursor advance;
- mutate bits after the one-bit evidence stop and require identical result;
- invalid first-property/non-K1 inputs must remain rejected through the production R3.18B boundary;
- repeated runs over the same witness must be bit-exact and receipt-exact.

## 6. Privacy and artifact policy

Durable artifacts may contain replay identity hashes, frame/actor/property coordinates, bit ranges, decoded K1 semantic values where already non-sensitive, booleans, counts, mismatch summaries, and payload hashes.

Do not persist raw replay payload windows, player/account names, free-form title text, or other unnecessary cleartext replay content.

## 7. Mutation gate

This pass must leave unchanged:

```text
crates/mimir-replay/src/**
crates/mimir-replay/tests/**
Cargo.toml
Cargo.lock
external_fixtures/**
test_corpus/**
scripts/**
```

Disposable workflows/tools on an evidence branch are allowed but must never enter the clean production history.

## 8. Hard stop

R3.18C does **not** admit:

- any production Rust change;
- a production `property_present` loop;
- a second property stream/header/payload native decode;
- K2/K3/K4 composition through the R3.18B wrapper;
- next actor or next frame iteration;
- actor lifecycle table mutation;
- new attribute family/shape/context;
- raw-state/event/replay-slice/skill/runtime/export widening.

## 9. Outcome gate

### Outcome A

Both real terminator and continuation classes are proven when available, all native/oracle coordinates and one-bit values match exactly, negative controls pass, privacy/mutation gates pass, and same-head normal CI is green. Then continuity may open a separately specified minimal production loop-control pass. A generalized property loop is still not automatically admitted.

### Outcome B

The supported lane proves only part of the loop-control surface or lacks one required witness class. Record the bounded evidence and keep production at R3.18B.

### Outcome C

Any native/oracle coordinate mismatch, one-bit disagreement, source drift, privacy failure, unexpected mutation, or cursor ambiguity. Stop without production widening.
