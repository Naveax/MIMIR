# MIMIR — Next Chat Handoff

Canonical production is **R3.18BK** at `f4a56d53d11a0c3d59f4bd57e58688bdd9d192bf` / `07656c7a43c1afb97903ef33c1109b764fbf8b7d`.

**R3.18BK is CLOSED / Outcome A.** It validates/recomputes the published BI prerequisite and consumes exactly one immutable BH `property_present` bit on only three authority rows. Exact distribution false=1 / true=2; start is BI payload end; end/stop is start+1. The 37 BE-false and 7 upstream AU-false rows remain excluded. Following stream/header/payload/second-control consumption is 0/0/0/0.

Production receipts: builder `34211911298/102014640422` SUCCESS; validation-only PR #216 closed unmerged; exact-head PR CI `34212312983/102015924320` SUCCESS; published-main CI `34212774993/102017408925` SUCCESS. Clean production scope is exactly `crates/mimir-replay/src/lib.rs` plus `crates/mimir-replay/tests/r3_18bk_post_bi_following_control.rs`.

Active pass: **R3.18BL — Published R3.18BK Mixed Next-Control Differential**. Revalidate published BK against immutable BH on exact 3/3 rows, preserve false=1 / true=2, prove exact BI prerequisite and exact start/value/end/stop, repeatability and negatives, and keep following stream/header/payload/second-control consumption plus production mutation at zero. Do not decode a following header during BL.

Only after BL Outcome A may a separate later pass inspect one following header on exactly the two BK-true continuation rows. The BK-false row is a terminator.

Before dispatch or rerun inspect queued/waiting/in-progress equivalent runs and reuse an existing exact run. CI waiting is not a reason to duplicate the same SHA/workflow/input.
