# MIMIR R3.18BJ — Published R3.18BI One-Following-Payload Differential Decision

**Date:** 2026-09-08
**Outcome:** **A — ADMITTED / READ-ONLY DIFFERENTIAL CLOSED**
**Canonical production remains:** `def8e959239106e25d95091fcfcf468fec59e228` / `61ca1c3cdf504f4c1eaef3001cbe81984414c537`
**Evidence authority:** `fa75bb265eed9909047076d4a35e55e65dd27838` / `877f783c665215a56f43a71aec0abfe23acb99ce`

## Decision

R3.18BJ closes Outcome A. Published R3.18BI matches immutable R3.18BG payload authority exactly on all three admitted rows while preserving every surrounding false terminator and stopping before the R3.18BH next-control bit.

The exact payload lane remains Boolean=2 / Float=1 with widths 1/1/32. Published BI, the immutable BG authority and a direct primitive decode agree 3/3. Repeatability is exact 3/3, poisoning only the BH bit does not change BI 3/3, all 37 R3.18BE false terminators reject before payload decoding, all 7 upstream R3.18AU false terminators stay outside BI success, and witness reselection is zero.

No R3.18BH bit or later stream/header/payload/second-control bit was consumed. Production, Cargo, fixture, corpus and support mutation are all zero.

## Exact authority

```text
published continuity base             910b88b66cf896893ff86620944111c723c5ab5d
BJ evidence SHA/tree                  fa75bb265eed9909047076d4a35e55e65dd27838 / 877f783c665215a56f43a71aec0abfe23acb99ce
BJ evidence run/job                   34191528993/101950417302 SUCCESS
BJ same-head natural CI               34191528959/101950417219 SUCCESS
same-head CI count                    1
artifact                              10042480960 / 7131 bytes
artifact ZIP sha256                   e9ec49453dc69c384042b67ee6e459881999478f4ab5e6fe978ce171299ff24d
artifact manifest sha256              ac1ec9da8053f21e54bb4ff4e42d63c46058a281374412a9e31a87e6228012c4
curated authority files               13 + manifest
published BI SHA/tree                 def8e959239106e25d95091fcfcf468fec59e228 / 61ca1c3cdf504f4c1eaef3001cbe81984414c537
BI lib/test blobs                     2307ea008176d27208e2354c9706f09dc447fd5f / 16b15e1fa5dc71d295837578dff861635679ffc9
BG artifact                           10015405999 / sha256:a43a528a49fa6d07ef1c92266c6dc9ed4ef2a3e87e7f69f65f2f40d39f3fa15a
BH artifact                           10023482583 / sha256:26e2bf42abe3d174949bc37b2e3e5e7e02a6caff2fa0490cbc9f3fa30626822d
pinned Boxcars                        c70e77df7af81b436cb545d070bb90c82f562d0b
```

## Frozen differential result

```text
published BI exact                    3/3
direct primitive exact                3/3
Boolean / Float                       2 / 1
width 1 / width 32                    2 / 1
native-authority mismatch             0
repeatability                         PASS 3/3
BH poison unchanged                   PASS 3/3
BE false rejected                     37/37
AU false excluded                     7/7
witness reselection                   0
BH control bits consumed              0
following stream/header/payload       0/0/0
second later control                  0
full validation                       PASS
production/Cargo/fixture/corpus/support mutation 0/0/0/0/0
privacy                               PASS
```

## Sequencing consequence

R3.18BJ does not itself widen production. It closes the publication differential required by the R3.18BI decision. The next exact pass is **R3.18BK — Bounded Post-BI Next Property-Control Production**.

R3.18BK may consider exactly the one R3.18BH-observed `property_present` bit at BI `payload_end_bit` on the same three immutable authority rows. Both observed boolean classes are valid: false=1 / true=2. Earlier true-only production semantics must not be inherited.

## Hard stop

No following stream ID, header, payload, second later control, wider tag/context membership, generalized/repeated property cursor, actor/frame/lifecycle mutation, raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.
