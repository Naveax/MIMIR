# MIMIR — Next Chat Handoff

Canonical production is **R3.18BA** at `5d2bca711f528ab1bb607104379af503ff175697` / `6b5140e228c882efea8b3f5ec0b0f6abf2f49a3a`, parent `109bad258d43963fd5432317503f99a7e1b8aa1b`. The clean production commit changes only `crates/mimir-replay/src/lib.rs` and `crates/mimir-replay/tests/r3_18ba_post_ay_payload_control.rs`.

R3.18BA validates/recomputes one exact R3.18AY payload, begins at AY `stop_bit`, consumes exactly one R3.18AX-admitted LSB-first `property_present` bit, accepts both observed classes (**false=37 / true=3**), and stops exactly one bit later. All seven upstream AU false terminators remain outside BA. Adjacent stream/header/payload/second-control consumption is 0/0/0/0.

Validation: builder `33091339939/98584661482` SUCCESS; PR #208 closed unmerged with CI `33091594385/98585555551` SUCCESS; exact candidate push CI `33091611038/98585614713` SUCCESS; published-main CI `33092084628/98587299347` SUCCESS; publication force=false.

The active pass is **R3.18BB published R3.18BA mixed following-control differential**. Use exactly the immutable R3.18AX forty-row artifact `9644869549` / `sha256:32f8b8056791280805da023e18ba73931f7caf4e2cf9e816411d4a0094bf97d9`. Require published BA and AY prerequisite exact 40/40, false=37 / true=3, mismatch/reselection 0/0, repeatability/negatives PASS and adjacent consumption 0/0/0/0. BB is read-only and must not decode a following header.

Before any dispatch/rerun inspect queued/waiting/in-progress equivalent runs and reuse an existing exact run. Rerun is never polling.
