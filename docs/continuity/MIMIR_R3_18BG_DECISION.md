# MIMIR R3.18BG — One Following Primitive Payload Evidence Decision

**Status:** CLOSED — Outcome A
**Pass type:** read-only one-payload differential evidence
**Production authority:** R3.18BE `1d717d3e82179edd85b197968f46b8f951a3e828` / `72cf2b907437a1ba62cc9deebd7608f7d0372f81`
**Direct row authority:** R3.18BF three true rows
**Pinned oracle:** Boxcars `c70e77df7af81b436cb545d070bb90c82f562d0b`

## Authority

- evidence head: `02e1799001b670db24f1e0076f2afd6c05f5afdf`
- evidence run/job: `34112731371/101715102551` — SUCCESS
- same-head CI: `34112731358/101712578621` — SUCCESS
- artifact: `10015405999` / `sha256:a43a528a49fa6d07ef1c92266c6dc9ed4ef2a3e87e7f69f65f2f40d39f3fa15a`
- inner manifest: `sha256:b06097e08cc276e80e17543f36a3ab05ac184b335ec12ded0fd460e2129d5e46` — 17/17 files verified

## Outcome A

Exactly the three immutable BF-true rows reached payload decoding and all three matched pinned Boxcars at both payload boundary and value identity.

```text
target rows                    3/3
Boolean                        2
Float                          1
width=1                        2
width=32                       1
Float identity                 raw IEEE754 u32
native/oracle mismatch         0
witness reselection            0
BF false rows excluded         37/37
upstream AU false excluded     7/7
next-control bits consumed     0
full validation                PASS
privacy scan                   PASS
```

Historical R3.18AW/R3.18AM/R3.18AN payload coordinates or values were not used as authority.

## Admission

BG closes as evidence only. It does **not** add production payload composition. Production remains R3.18BE.

The only newly opened boundary is R3.18BH: from each exact BG `payload_end_bit`, observe exactly one next `property_present` bit and stop one bit later.

## Hard stop

No production composition of the BG payload, no following stream/header/payload after the BH observation, no second later property-control bit, no repeated/generalized property cursor, no actor/frame/lifecycle mutation, and no raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.
