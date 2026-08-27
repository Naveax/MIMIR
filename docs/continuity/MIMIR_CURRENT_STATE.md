# MIMIR — Current Canonical State

**Continuity date:** 2026-08-27
**Repository:** `Naveax/MIMIR`
**Canonical production SHA:** `5d2bca711f528ab1bb607104379af503ff175697`
**Production tree:** `6b5140e228c882efea8b3f5ec0b0f6abf2f49a3a`
**Production milestone:** `R3.18BA — bounded post-AY mixed following-control production`
**Last read-only evidence/audit:** `R3.18AZ — Outcome A / published AY exact 40/40 / mismatch 0 / reselection 0 / artifact 9652520412`
**Last completed contract:** `R3.18AT — exact_tuple_only / 16 eight-field contexts / multiplicity 40 / 7 false terminators outside membership`
**Current exact pass:** `R3.18BB — published R3.18BA mixed following-control differential`

## Truthful boundary

R3.18BA is canonical production. Exactly forty valid R3.18AY payload rows may enter BA; seven upstream R3.18AU false terminators remain outside the lane. BA recomputes AY, begins at AY payload end, consumes exactly one R3.18AX-admitted LSB-first `property_present` bit, accepts both false and true, and stops one bit later. The frozen distribution is false=37 / true=3. Production consumes no following stream/header/payload or second later control bit.

```text
production SHA/tree                    5d2bca711f528ab1bb607104379af503ff175697 / 6b5140e228c882efea8b3f5ec0b0f6abf2f49a3a
parent                                 109bad258d43963fd5432317503f99a7e1b8aa1b
lib/test blobs                         fe232760e63c3c1b46711084c70049f456ef345b / 41ef1c2c087cc52bf2bcf0fa65c911a31a6ffc13
builder                                33091339939/98584661482 SUCCESS
validation PR                          #208 CLOSED UNMERGED
PR CI                                  33091594385/98585555551 SUCCESS
candidate push CI                      33091611038/98585614713 SUCCESS
published-main CI                      33092084628/98587299347 SUCCESS
valid BA rows                          40/40
upstream false terminators excluded    7/7
control distribution                   false=37 / true=3
adjacent stream/header/payload/second  0/0/0/0
```

## Current gate

R3.18BB is read-only. It must validate published BA against exactly the immutable R3.18AX forty-row authority with mismatch/reselection zero and no adjacent consumption. It may not decode a following header, including on the three true rows.

## Hard stop

No following stream/header/payload, second later control, generalized property cursor, actor/frame/lifecycle/raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.
