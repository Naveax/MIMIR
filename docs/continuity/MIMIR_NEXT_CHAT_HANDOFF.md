# MIMIR — Next Chat Handoff

Canonical production remains **R3.18BA** at `5d2bca711f528ab1bb607104379af503ff175697` / `6b5140e228c882efea8b3f5ec0b0f6abf2f49a3a`.

R3.18BB is now **Outcome A / CLOSED**. Evidence head `91595db2970ad395ec048ebd9326cfa97b01b38a`, authority `33104207616/98629573433` SUCCESS, same-head CI `33104207621/98629573926` SUCCESS, artifact `9659874105` / 9295 bytes / `sha256:0e5bc329e1fc89068243ad0846356ed4dbfc2ade245623385b8e84d21b4f138e`, internal manifest 11/11 PASS. Published BA and AY prerequisite are exact 40/40; false=37 / true=3; mismatch/reselection 0/0; adjacent stream/header/payload/second-control 0/0/0/0; mutation 0/0/0/0/0; privacy PASS.

The first BB helper head `a8ed349204d2a72f404ade717aba58fdbdfde815` / run `33103836525` is non-authority. Its science passed but Rust 1.85 lacked the `rustfmt` component; it was not rerun. v2 corrected only toolchain components on a fresh sibling SHA.

The active pass is **R3.18BC — one following-property-header evidence after published BA mixed control**. Preserve all 40 BB witnesses. Exactly 37 false rows terminate at BA. Only these three true rows may enter the header lane: `external_fixtures/sample_002.replay` (BA stop 11224), `external_fixtures/sample_003.replay` (7808), and `test_corpus/largest_100/079_1f838b01-66b5-4963-b62e-64f3d7dbd545.replay` (3160). Observe one header through `payload_start`, compare with pinned Boxcars, discover exact contexts/tags, and decode no following payload or second control.

Before any dispatch/rerun inspect queued/waiting/in-progress equivalent runs and reuse an existing exact run. Rerun is never polling.
