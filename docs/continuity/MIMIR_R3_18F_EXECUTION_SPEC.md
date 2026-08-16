# MIMIR R3.18F — Second-Property-Header Real-Replay Evidence

**Status:** ACTIVE
**Pass type:** read-only boundary evidence
**Production mutation:** forbidden
**Second-property payload decode:** forbidden
**Third property / repeated loop:** forbidden

## 1. Goal

Establish whether the already-admitted property-header primitive matches pinned Boxcars at the second-property boundary exposed by R3.18D, without publishing a new production composition and without consuming the second payload.

## 2. Frozen authority

```text
canonical continuity base            dd7d9550910a0ad08cd5f1a171d782b5dd4e954a
production SHA/tree                  4adadd185783954c7fb6ad67db14b77b377cdde5 / 67b1969eaff49d2913b88b3921f27b1bd7fe8193
production lib blob                  42bc3fd3e8ea6bd1d15df82e4c6d8809b8443662
R3.18D focused test blob             2f5b188cc5b3ce8200c9961d964f1dc66b3ab49b
R3.18E evidence head                 aae03a7fdec85e30be3954d14ffdc8cd1d86121e
R3.18E authority run/job             31949407736 / 95170443262 SUCCESS
R3.18E same-head normal CI           31949407685 / 95170443059 SUCCESS
R3.18E artifact                      9264243765
R3.18E artifact SHA256               005afc3c97bd6bdb9aef69be993538fd813e30481923c59beefcf37e71cdfc9b
pinned Boxcars                       c70e77df7af81b436cb545d070bb90c82f562d0b
supported replay lane                47
frozen source witness classes        47 terminator + 47 continuation
```

Before evidence work, fetch fresh `main`, prove every commit after `4adadd185783954c7fb6ad67db14b77b377cdde5` is continuity-only, verify source/test blobs and the R3.18E receipts, and reconstruct the exact replay identity lane.

## 3. Witness policy

Reproduce the deterministic R3.18E witness classes without changing their replay identity or first-property/control coordinates.

- Positive second-header lane: exactly one continuation witness per replay when the frozen lane reproduces, target 47.
- Terminator negative lane: exactly one terminator witness per replay, target 47.
- If either class count drifts, stop and classify the drift before changing any target.

Record only privacy-safe relative replay identity/hash and structural bit/object/tag facts.

## 4. Native evidence path — continuation rows

For every continuation witness:

1. build the existing production lookup plan;
2. run the published R3.18B single-K1-property decoder at the frozen first-property start;
3. run the published R3.18D control API and require `next_property_present == true`;
4. require the R3.18D control start equals the oracle second `property_present` start;
5. independently invoke `decode_replay_network_existing_actor_first_property_header_v1` at that same second `property_present` start using the same actor object and lookup plan;
6. require `property_present == true`;
7. compare stream-ID start/end/value, resolved property object, resolved attribute tag, payload-start and stop exactly with pinned Boxcars;
8. stop at `payload_start`. Do not decode or interpret any second-property payload bit.

The existing function name contains `first_property`; R3.18F uses it only as a stateless header primitive at an explicit bit start for evidence. This pass does not redefine its production role or publish a repeated loop.

## 5. Terminator negative lane

For every terminator witness, invoke the same header primitive at the false control-bit start and require:

```text
property_present == false
property_present_end == R3.18D control end
stop_bit == property_present_end
stream-id fields == None
resolved object/tag == None
payload_start == None
```

No lookup-derived or payload boundary may appear after a false terminator.

## 6. Required aggregate gates

```text
replay identity / oracle parse          47/47
R3.18E witness reconstruction           94/94
continuation rows                       47
terminator rows                         47
continuation header native success      47/47
second property_present exact           47/47
second stream start/end/value exact     47/47
resolved property object exact          47/47
resolved attribute tag exact            47/47
second payload_start/stop exact         47/47
terminator one-bit stop exact           47/47
terminator optional header fields None  47/47
native/oracle mismatch                  0
second payload bits consumed            0
third-property bits consumed            0
privacy                                 PASS
production/Cargo/fixture/corpus/
support mutation                        0/0/0/0/0
```

## 7. Negative controls

At minimum prove:

- truncate within the required second stream-ID/header bits for a deterministic continuation witness: fail closed;
- mutate bits strictly after the second-header stop/payload-start: header result unchanged;
- repeat the same continuation header observation: exact;
- mutate an otherwise-resolved second stream ID to an unresolved value in an isolated synthetic copy: fail closed;
- terminator rows never attempt stream/header resolution after the false bit.

No negative may decode the second payload.

## 8. Evidence artifact

Emit an immutable privacy-safe artifact containing source/production/R3.18E receipts, replay identity manifest, pinned Boxcars instrumentation receipt, reproduced source witnesses, continuation second-header rows, terminator negatives, aggregate summary, negative controls and file hashes. Record artifact ID and digest.

## 9. Outcome gate

### Outcome A

All frozen continuation second-header boundaries match exactly, all terminator negatives stop after one bit, mismatch is zero, and second-payload/third-property consumption remains zero. Close R3.18F. Only then may a separate contract/production admission pass be defined.

### Outcome B

A bounded native/oracle discrepancy exists. Record the exact stream/header class and keep production second-property admission closed.

### Outcome C

Authority drift, corpus drift, privacy failure, production mutation, scope widening, second-payload consumption, or any third-property/repeated-loop observation. Stop without admission.

## 10. Hard stop

R3.18F does not publish a second-property decoder, decode a second payload, observe a third property, generalize a property loop, widen K2/K3/K4 wrapper composition, iterate actors/frames, mutate lifecycle state, extract raw-state/events, slice replays, or widen skill/runtime/export/dependency behavior.
