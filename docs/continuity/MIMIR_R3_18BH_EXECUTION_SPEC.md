# MIMIR R3.18BH — Next Property-Control Bit Evidence After Exact BG Payload End

**Status:** ACTIVE
**Pass type:** read-only exactly-one-control-bit differential evidence
**Production authority:** R3.18BE `1d717d3e82179edd85b197968f46b8f951a3e828` / `72cf2b907437a1ba62cc9deebd7608f7d0372f81`
**Direct authority:** R3.18BG Outcome A artifact `10015405999`
**Pinned oracle:** Boxcars `c70e77df7af81b436cb545d070bb90c82f562d0b`

## 1. Goal

On exactly the three immutable BG authority rows, rematerialize the exact published BE header and exact BG payload, require the native cursor to equal the authoritative `payload_end_bit`, then read **exactly one** next `property_present` bit natively and through pinned Boxcars.

The false/true distribution is an output of BH. It must not be guessed or inherited from an older ordinal.

## 2. Entry requirements

For every target row:

1. identity matches the BG authority row;
2. published R3.18BE header reconstruction matches;
3. exact BG payload tag/value/width/end boundary matches;
4. cursor equals BG `payload_end_bit` before BH reads anything.

The 37 BF-false rows and seven upstream AU-false terminators are excluded before BH entry.

## 3. Allowed read

```text
start = exact BG payload_end_bit
read exactly one property_present bit
end = start + 1 bit
```

Record native bit, oracle bit, start boundary, end boundary, and row identity.

## 4. Required differential assertions

- target rows: exactly 3/3;
- native/oracle control bit: exact 3/3;
- native/oracle one-bit end boundary: exact 3/3;
- witness reselection: 0;
- excluded false-row access: 0;
- following stream bits consumed: 0;
- following header bits consumed: 0;
- following payload bits consumed: 0;
- second later control bits consumed: 0.

## 5. Negative tests

Reject or fail closed on:

- cursor not equal to exact BG payload end;
- row not in the three-row BG authority set;
- altered replay identity or witness reselection;
- any attempt to read stream/header/payload after the one bit;
- any attempt to consume a second later property-control bit;
- historical ordinal/value assumptions used as authority.

## 6. Validation

Run focused evidence tests, full workspace validation, privacy scan, artifact manifest verification, and exact-SHA CI. Reuse an already queued/in-progress identical run instead of dispatching duplicates.

## 7. Outcome gate

### Outcome A
All 3/3 rows match pinned Boxcars for the one control bit and exact one-bit boundary, with zero reselection and zero adjacent consumption. Record the observed false/true distribution. A later production pass may then be specified for exactly this control boundary.

### Outcome B
Any mismatch, unexpected cursor movement, authority drift, or adjacent read keeps the boundary closed. Diagnose before widening.

## 8. Hard stop

BH does not decode a following stream ID, header, payload, or second later control. It does not create a generalized/repeated property cursor and does not advance actor/frame/lifecycle state or open raw-state/event/replay-slice/skill/counterfactual/runtime/export boundaries.
