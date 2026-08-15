# MIMIR R3.17N Decision — K4 Evidence-Supported Contract Admission

**Outcome:** A — ADMITTED / COMPLETE
**Pass type:** contract-only
**Production Rust:** unchanged / forbidden in this pass

## Frozen authority

```text
continuity base / published contract main  c8ebb872e510574bb69ab28c719f415ece8b7665
production SHA                             7390e3b145372252caaa8fa1fe3e0cd13b83336c
contract authority branch head             086ec251aea4eea9881cfc224bfac2d09596269f
contract authority run/job                 31883205829 / 95008550716 SUCCESS
clean contract commit                      c8ebb872e510574bb69ab28c719f415ece8b7665
clean contract tree                        61e36d40e6af3853a887e840b22f759dda26ed75
exact clean-candidate CI                   31883438754 / 95009080782 SUCCESS
published-main Knowledge Archive           31883625387 / 95009532717 SUCCESS
published-main normal CI                   31883625362 / 95009532734 SUCCESS
admitted-group SHA256                      80c50783d70951bf125ccdadb818750a7ce35012891997f9b396241d84a9ae2b
admitted-group git blob                    b5fa6aaa729772ab3d113703952effe2346c9866
contract git blob                          76deabf8241b419ca224645106d2a19b041e20f8
```

## Result

R3.17N admitted exactly the R3.17M evidence surface and nothing more.

```text
R3.17M evidence groups                     161
R3.17N admitted groups                     161
byte-for-byte evidence equality            161/161 PASS
cross-product widening                     0
positive-vector plan                       PASS
negative/malformed vector plan             PASS
atomic failure semantics                   PASS
exact one-value end semantics              PASS
production mutation                        0
Cargo / fixture / corpus / support         0 / 0 / 0 / 0
outcome                                    A
```

The canonical admitted-group artifact is `docs/continuity/MIMIR_R3_17N_ADMITTED_GROUPS.jsonl`. Its SHA-256 is `80c50783d70951bf125ccdadb818750a7ce35012891997f9b396241d84a9ae2b` and it is byte-for-byte identical to the R3.17M evidence groups.

## Exact contract boundary

Admission identity is the exact tuple `(attribute_tag, shape, version_major, version_minor, net_version, is_rl_223, payload_width)`. The 161 rows contain 132 unique shapes because context remains part of admission. `Reservation` remains 46 exact group rows / 35 shapes, `DemolishFx` 19 / 12, `DemolishExtended` 5 / 5 and `LoadoutsOnline` 79 / 73. No Cartesian recombination of observed subfields is legal.

The contract freezes LSB-first unaligned decoding, checked arithmetic, atomic failure, exact one-value end, explicit rejection of unobserved version/context/shape combinations, and preservation of trailing bits. It does not authorize a second property.

## What remains closed

- native K4 production implementation,
- any K4 group outside the exact 161-row artifact,
- second-property / property-loop continuation,
- next actor/frame iteration or lifecycle mutation,
- raw-state/event extraction,
- replay slicing, skill mining, runtime or export widening.

## Next pass

Open `R3.17O — Direct Native Exact-Contract K4 Decoder Implementation`. R3.17O may implement only the exact 161-group R3.17N contract. A later separate R3.17P real-replay differential audit remains mandatory before any R3.18 property-loop reopening.
