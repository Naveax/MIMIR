# MIMIR — Current Canonical State

**Continuity date:** 2026-08-27
**Repository:** `Naveax/MIMIR`
**Canonical production SHA:** `5d2bca711f528ab1bb607104379af503ff175697`
**Production tree:** `6b5140e228c882efea8b3f5ec0b0f6abf2f49a3a`
**Production milestone:** `R3.18BA — bounded post-AY mixed following-control production`
**Last read-only evidence/audit:** `R3.18AZ — Outcome A / published AY exact 40/40 / mismatch 0 / reselection 0 / artifact 9652520412`
**Current exact pass:** `R3.18BB — published-R3.18BA mixed following-control differential`

## Truthful boundary

R3.18BA is now canonical production. It validates/recomputes one exact R3.18AY Int/32 payload composition, starts exactly at the validated AY stop, consumes exactly one LSB-first following `property_present` bit, accepts both immutable R3.18AX-observed classes, and stops one bit later. The exact frozen distribution is false=37 / true=3 on forty valid payload rows; all seven upstream AU false terminators remain outside the BA lane.

```text
production SHA/tree                    5d2bca711f528ab1bb607104379af503ff175697 / 6b5140e228c882efea8b3f5ec0b0f6abf2f49a3a
production parent                      109bad258d43963fd5432317503f99a7e1b8aa1b
fixed builder                          ce5e27641cb0240e7440b93092be69a8fc5b7a11
builder run/job                        33091339939/98584661482 SUCCESS
builder helper-head CI                 33091339935 SUCCESS
validation-only PR                     #208 closed unmerged
exact-candidate PR CI                  33091594385/98585555551 SUCCESS
validation-branch CI                   33091611038 SUCCESS
published-main CI                      33092084628/98587299347 SUCCESS
frozen BA rows                         40/40
upstream AU false terminators          7/7 excluded
BA false / true                        37 / 3
AY recomputation per BA call           exactly 1
new control reads per BA call          exactly 1
next stream/header/payload/second      0/0/0/0
production files                       exactly 2
```

The superseded first builder run `33090827273` is not authority: focused behavior passed, but Clippy rejected the redundant eight-argument API (`too_many_arguments 8/7`). It was not rerun. The corrected API removes the redundant AU authority parameter and derives that authority through `ay_prior.header_composition`.

## Current gate

R3.18BB is read-only. It must replay exactly the immutable forty R3.18AX control witnesses against published R3.18BA and require exact start/value/end/stop equality, false=37 / true=3, mismatch 0 and witness reselection 0. The 37 false rows are terminators. Only the exact three true rows may be candidates for a later, separate following-header evidence pass.

R3.18AX already carries the exact bit-level `TRUNCATION_BEFORE_CONTROL=PASS 40/40` authority. All forty control starts are non-byte-aligned, so the production `&[u8]` API must not pretend it can represent a partial-byte EOF that preserves AY while deleting only the following bit. BA's carrier truncation negative remains fail-closed; the exact-before-bit claim remains AX evidence authority.

## Hard stop

R3.18BB decodes no following stream ID, header or payload and no second later control. No generic/repeated property cursor, next actor/frame/lifecycle mutation, raw-state/event/replay-slice/skill/counterfactual/runtime/export widening is open.
