# MIMIR — Current Canonical State

**Continuity date:** 2026-08-16
**Repository:** `Naveax/MIMIR`
**Canonical production SHA:** `de7a2ba40663bb619ca7bd8654846ce87670d023`
**Production milestone:** `R3.18B — minimal native existing-actor single-property K1 composition`
**Completed single-property evidence:** `R3.18A — Outcome A / exact one-property boundary / 0 next-property bits`
**Current exact pass:** `R3.18C — existing-actor property-loop terminator/continuation evidence`

## 1. Truthful production boundary

Production now includes R3.18B. MIMIR can start at an existing actor's first `property_present` bit, reuse the R3.16B header decoder, and compose exactly one property only when the resolved tag is one of the six already-admitted K1 primitive scalar tags. The composition stops exactly at that scalar payload end. It does not read the next `property_present` bit and it does not dispatch K2/K3/K4 through this wrapper.

Separate one-value K2/K3/K4 decoders remain production-authoritative at their previously admitted boundaries; R3.18B deliberately does not combine them into the property wrapper.

```text
production SHA               de7a2ba40663bb619ca7bd8654846ce87670d023
production tree              d1889038ca2eaeb8bb0f05e44b811d906f84cf6e
parent                       f12365b43029f19f3ab1dd889e651f9781b0655e
lib.rs blob                  478ae5b70514fcff79117b834733849517c48500
R3.18B focused test blob     927e9a2c834115d1c918fa96fb6d0690bd03965e
```

## 2. R3.18B production closure

```text
implementation run/job       31942254523 / 95153021330 SUCCESS
exact candidate validation   31942696817 / 95154052998 SUCCESS
published main CI            31942870294 / 95154460239 SUCCESS
published-main validator     31942896666 / 95154519828 SUCCESS
clean production files       2
focused R3.18B tests          8/8 PASS
K1 tags                       Boolean Byte Enum Float Int Int64
R3.18A-shaped Int=62          PASS
property absent               reject
non-K1 tag                    reject before payload read
header/payload truncation     reject
trailing poison bits          no effect
header stop == payload start  true
composition stop == end       true
next property bits consumed   0
Cargo/fixture/corpus/support/
workflow/continuity mutation  0/0/0/0/0/0/0
```

## 3. R3.18C exact next pass

R3.18C is evidence-only. On deterministic real existing-actor witnesses whose first property is R3.18B-admitted K1, compare the native one-property `stop_bit` to the pinned Boxcars oracle's next `property_present` start. Then consume **exactly one bit** at that location in the evidence probe.

Required witness classes, if both exist in the frozen supported lane:

```text
terminator     next property_present = false
continuation   next property_present = true
```

For the terminator case, prove the actor's property sequence ends exactly after that one bit and no stream/payload bits are consumed. For the continuation case, prove only that continuation is true and stop immediately after the bit. A second stream ID, property header, or payload remains outside the native evidence boundary.

## 4. Still closed

```text
production property_present loop
second property stream/header/payload
K2/K3/K4 dispatch through the R3.18B wrapper
next actor / next frame iteration
actor lifecycle mutation
new attribute family/shape/context admission
raw-state extraction
native event extraction
replay slicing
skill/runtime/export widening
Cargo/fixture/corpus/support-lane expansion
```
