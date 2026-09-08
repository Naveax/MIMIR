# MIMIR R3.18BI — Bounded Post-BE One-Following-Payload Production Decision

**Date:** 2026-09-08
**Outcome:** **A — ADMITTED / PRODUCTION CLOSED**
**Canonical production:** `def8e959239106e25d95091fcfcf468fec59e228` / `61ca1c3cdf504f4c1eaef3001cbe81984414c537`
**Parent authority:** `2d8a2a28413467690b076bd08e6f750843af5c33`

## Decision

R3.18BI closes Outcome A. Production now composes exactly one already-admitted R3.18BG primitive payload after a valid published R3.18BE true-path following header, on exactly the three immutable BG authority rows.

The admitted payload set remains **Boolean=2 / Float=1** with exact widths **1 / 1 / 32 bits**. Each production result starts at the exact R3.18BE `payload_start_bit`, preserves the BG semantic value and raw Float identity, and stops exactly at the primitive `payload_end_bit`.

The separately evidenced R3.18BH next `property_present` bit is not consumed. Poisoning that bit leaves the BI result unchanged. The thirty-seven R3.18BE false terminators and seven upstream R3.18AU false terminators cannot enter payload production.

## Exact authority

```text
production SHA/tree                   def8e959239106e25d95091fcfcf468fec59e228 / 61ca1c3cdf504f4c1eaef3001cbe81984414c537
parent                                2d8a2a28413467690b076bd08e6f750843af5c33
lib blob                              2307ea008176d27208e2354c9706f09dc447fd5f
focused BI test blob                  16b15e1fa5dc71d295837578dff861635679ffc9
BI execution spec blob                e70e45a8a256d633c516895bbc28b61413af4b97
BI production builder                 34158571800/101855439564 SUCCESS
BI helper exact-head CI               34158571745/101855439521 SUCCESS
BI validation PR                      #213 closed unmerged
BI exact-head PR CI                   34159120199/101857049780 SUCCESS
BI published-main CI                  34159530318/101858247592 SUCCESS
BG artifact                           10015405999 / sha256:a43a528a49fa6d07ef1c92266c6dc9ed4ef2a3e87e7f69f65f2f40d39f3fa15a
BG manifest                           sha256:b06097e08cc276e80e17543f36a3ab05ac184b335ec12ded0fd460e2129d5e46
BH evidence head/tree                 c728658ac237a45f34b3af002c27f704f5293fb5 / 9761d42cd55d3152fe19653ea5be67efd826f2fa
BH evidence run/job                   34132181073/101774645567 SUCCESS
BH same-head CI                       34132181159/101775846915 SUCCESS
BH artifact                           10023482583 / sha256:26e2bf42abe3d174949bc37b2e3e5e7e02a6caff2fa0490cbc9f3fa30626822d
BH manifest                           sha256:9eba3e774500eccf0fa1df06d98588ea945b237683594ebd0a8e89c3bad671aa
pinned Boxcars                        c70e77df7af81b436cb545d070bb90c82f562d0b
```

## Frozen production result

```text
target BG payload rows                3/3
Boolean                               2
Float                                 1
payload widths                        1 / 1 / 32 bits
payload semantic/boundary exact       3/3
repeatability                         3/3
BE false terminators excluded         37/37
upstream AU false excluded            7/7
BH control bits consumed              0
following stream/header/payload       0/0/0 bits
second later control                  0 bits
production scope                      2 files
```

## Sequencing consequence

R3.18BI makes the BG payload a production capability, but it does **not** admit the BH control bit. The next pass is **R3.18BJ — Published R3.18BI One-Following-Payload Differential**, a separate read-only differential against immutable BG/BH authority.

Only an R3.18BJ Outcome A may allow a later bounded production pass to consider the one R3.18BH-observed control bit.

## Hard stop

No BH control production during R3.18BJ, no following stream/header/payload after that bit, no second later control, no new tag/context membership, no generalized/repeated property cursor, and no actor/frame/lifecycle/raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.
