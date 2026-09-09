# MIMIR R3.18BQ — One Following Payload Evidence

**Status:** ACTIVE
**Pass type:** read-only exactly-one-payload boundary evidence
**Production authority:** R3.18BO `cbb823ce7d3fc871c35a83afc5ee21ae71945821` / `146cb78edfb434fd43e532593efce8e35ee97111`
**Direct row authority:** admitted R3.18BP artifact `10105612793` / `sha256:ffa6613fc7703f148d388650466f164068e5d454cfeb0a926c548caacda47240`
**Contract authority:** R3.18BN `sha256:904a6c69d716964f756000d71e9b36c10400176057003dc5b811b1d8eb87040`**Production mutation:** forbidden
**Next property-control bit:** forbidden
**Witness reselection:** forbidden

## 1. Goal

On exactly the two R3.18BP true rows, reconstruct published prerequisites through R3.18BO, require exact equality with the admitted BP header row, decode exactly one payload beginning at the proven `payload_start_bit`, independently measure the same payload with pinned Boxcars, require exact equality, and stop at payload end. The one BP false terminator, 37 BE exclusions and 7 Au exclusions never invoke a payload decoder.

## 2. Frozen authority

```text
production SHA/tree                    cbb823ce7d3fc871c35a83afc5ee21ae71945821 / 146cb78edfb434fd43e532593efce8e35ee97111
continuity base SHA/tree               bd7310eb8ba96f0bd8ebcd59ed3b1806e856ae52 / 17ad3834dc36c5e9e6ddd1f62d5147c16dd93946
BP evidence head/tree                  319d2b910ac23008bcc5338f04a5f95a0ae5ac5b / 1fc7223296b71256681a885de7e20161114532a9
BP run/job                               34355148349/102477806191 SUCCESS
BP same-head CI                           34355148286/102477834627 SUCCESS
BP artifact                             10105612793 / 7008 / sha256:ffa6613fc7703f148d388650466f164068e5d454cfeb0a926c548caacda47240
BP inner manifest                     sha256:2e8fbf0b4a9c2d29d4fdb440dba54eabcd860c91bc25c49d486c969052bef174
BP row split                           false=1 / true=2
BP exact BN contexts / multiplicity    2 / 2
BP tags                                Boolean=1 / ActiveActor=1
BN contract                            sha256:904a6c69d716964f756000d71e9b36c10400176057003dc5b811b1d8eb87040c
pinned Boxcars                        c70e77df7af81b436cb545d070bb90c82f562d0b
```

## 3. No historical value inheritance

BQ must not inherit payload value, start/end coordinate or target selection from older payload passes. The admitted BP row identity and current pre-payload coordinates are the only selectors.

## 4. Exact payload layouts

- Boolean row: `decode_replay_network_primitive_scalar_v1`, exact width 1 bit.
- ActiveActor row: `decode_replay_network_k2_v1` under exact net10/non-RL223 context, semantic layout `active: bool + i32 actor_id`, exact width 33 bits.
- Require payload end = start + width and stop there.
- Preserve signed actor id losslessly.

## 5. Independent Boxcars oracle

Pin Boxcars at `c70e77df7af81b436cb545d070bb90c82f562d0b`. Selection may use only replay/frame/actor identity and current header/property coordinates known before payload interpretation. Payload value/end are oracle outputs.

## 6. Expected equality

```text
targets                       2
Boolean rows / width          1 / 1
ActiveActor rows / width      1 / 33
native/oracle mismatch        0
witness reselection           0
next-control consumption      0
```

Per row require exact identity, tag, payload start/end/width and lossless semantic value equality.

## 7. Negative controls

False-row payload access absent; repeat decode 2/2; truncate inside payload rejects; wrong tag/start rejects before payload read; payload-end poison leaves result unchanged; corrupt BO/header prerequisite rejects; wrong actor, unresolved lookup, RL223/version drift and BN widening remain rejected; source-scope proves one payload decode only and zero next-control/generalized-loop access.

## 8. Validation

Require BP artifact identity/digest/manifest; frozen rows 3/3; false excluded 1/1; true targets 2/2; exact BN contexts 2/2; native and Boxcars rows 2/2; Boolean width1 and ActiveActor width33; mismatch/reselection 0/0; negatives PASS; next-control=0; full fmt/check/test/clippy/repository verifier; unique same-head CI SUCCESS; mutation 0/0/0/0/0; privacy PASS.

## 9. Hard stop

No next property-control bit, second payload/header, payload on the false row, generalized cursor, actor/frame/lifecycle/raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.

## 10. Outcome gate

### Outcome A
Both exact BP-true rows produce one payload exactly matching pinned Boxcars; all gates pass; next-control consumption is zero. Only then may a later pass inspect exactly one next property-control bit.

### Outcome B
A narrower exact subset is isolated without witness reselection or historical inheritance; keep next control closed.

### Outcome C
Authority drift, false-row payload access, header mismatch, native/oracle mismatch, unsupported layout, over-read, next-control access, production mutation, generic chaining or privacy failure. Stop without widening.
