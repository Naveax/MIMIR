# MIMIR R3.18AC — Post-AA Ordinal-3 Following-Property Payload Decision

**Date:** 2026-08-19
**Outcome:** **A — ADMITTED / READ-ONLY EVIDENCE**
**Production SHA:** `9392240c49f95766c214afee9865fed4155a87a4`
**Production tree:** `968520d480f78c528086e4e31b2ce307f4f8d232`

## Decision

R3.18AC is admitted Outcome A. On the exact immutable 47-row R3.18AB/Y lane, pinned Boxcars ordinal 3 and the narrow existing native payload decoders matched exactly through one payload end on 47/47 rows with zero witness reselection and zero another-control consumption.

The observed boundary-specific payload shapes are exactly:

- `ActiveActor`: 39/47, exact width 33 bits;
- `Int`: 7/47, exact width 32 bits;
- `UniqueId`: 1/47, exact width 80 bits, actual `system_id=1`, remote kind `Steam`.

No generic `UniqueId` width or alternate system/layout is admitted. R3.18AC is evidence only and changes no production source.

## Exact authority

```text
continuity base main/tree            f34413e00518b73cf3768cd1914eda8c728306df / cce54b2040c2a83ebbcce3b31250df5bc82102ca
production SHA/tree                  9392240c49f95766c214afee9865fed4155a87a4 / 968520d480f78c528086e4e31b2ce307f4f8d232
production lib/test blobs            46523f47f94231362b60f8aee038e943e41c7972 / 7df8f84af37d771b12da1334bd195634e4cc6a54
R3.18Z contract SHA256               81f3072628ef78bcd71dacc1e31b5211aa0de9c32e922e01112b20f4df1425d9
R3.18AB evidence head/tree           b2f4b73600165b2d83389b6ce43709b64beba52a / 8d36c8c7118db8c6f0d28c4ae88e0400cf4a3cd1
R3.18AB authority / same-head CI     32230919566/96000311036 / 32230919652/96000311479
R3.18AB artifact                     9357559410 / sha256:4b6d72b154440ee2b819f5a5ecb6fa3768e086b7ec4ba0d0c53d0e8e3ad23d99
R3.18AC evidence head/tree           62bc43dd12dbde48fb503cccd4da46dfcf6ae252 / 9d5b550b4bb93688db9f3a67583067adb32425f6
R3.18AC authority run/job            32237834815 / 96021661994 SUCCESS
R3.18AC same-head normal CI          32237834813 / 96021661894 SUCCESS
R3.18AC artifact                     9359697636 / 12010 bytes
R3.18AC artifact digest / ZIP SHA256 sha256:a6914044dfd8991d74b95caeb3507fb2469175c4458c5b50b55395b8ea67b9df
R3.18AC receipt helper               32238679393 / 96024251802 SUCCESS
pinned Boxcars                       c70e77df7af81b436cb545d070bb90c82f562d0b
```

The downloaded final artifact ZIP SHA-256 equals the GitHub Actions artifact digest exactly. The internal SHA-256 manifest verifies 10/10 payload files.

## Frozen result

```text
frozen rows                         47/47
oracle/native mismatch              0
ActiveActor                         39 x 33 bits
Int                                 7 x 32 bits
UniqueId                            1 x 80 bits
UniqueId actual layout              system_id=1 / Steam / 80 bits
witness reselection                 0
repeatability                       47/47 PASS
truncation                          47/47 PASS
wrong tag                           47/47 PASS
wrong context or N/A                47/47 PASS
post-payload poison                 47/47 PASS
another-control bits consumed       0
production/Cargo/fixture/corpus/support mutation 0/0/0/0/0
privacy                             PASS
```

## Superseded evidence attempt

Initial evidence head `4207ffdcbc9a032dfd3c6f36cc05703861c2067f` was not admitted. Its temporary native probe contained two harness defects: the `Int` branch moved `got.value` before reuse, and the context-negative gate incorrectly required context-insensitive `ActiveActor` decoding to reject a wrong K2 context. The corrected head `62bc43dd12dbde48fb503cccd4da46dfcf6ae252` changed only the temporary probe; production remained unchanged.

The first receipt-helper run `32238312740 / 96023121111` also was not authority. Its authority-resolution step succeeded but artifact download failed because the helper had not checked out a repository before invoking `gh run download`. Corrected helper `32238679393 / 96024251802` passed and independently bound the exact evidence run, exact-head CI, artifact digest and 10/10 internal manifest.

## Hard stop

Production remains R3.18AA at `9392240c49f95766c214afee9865fed4155a87a4`. R3.18AC admits no post-AA payload production API, no alternate UniqueId system/layout, no another `property_present` bit, no repeated/generalized property loop or cursor, no next actor/frame iteration, no lifecycle mutation, no raw-state/event extraction, no replay slicing, no skill mining, no counterfactual execution, and no runtime/export widening.

## Next gate

R3.18AD is a separate bounded production implementation. Starting only from a valid published R3.18AA result whose complete header context remains admitted by R3.18Z, it may decode exactly one ordinal-3 payload using only the AC-observed payload shapes: ActiveActor 33 bits, Int 32 bits, or UniqueId system 1 / Steam / 80 bits. It must stop exactly at that payload end and consume zero bits of another property-control boundary.
