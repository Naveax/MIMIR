# MIMIR — Next Chat Handoff

Canonical production is **R3.18BE** at `1d717d3e82179edd85b197968f46b8f951a3e828` / `72cf2b907437a1ba62cc9deebd7608f7d0372f81`, parent `3fa88f27201ee91c51a3bb7a623c00b46204c1e0`. The clean production commit changes only `crates/mimir-replay/src/lib.rs` and `crates/mimir-replay/tests/r3_18be_post_ba_following_header.rs`.

R3.18BE validates/recomputes one exact published R3.18BA mixed control. False rows (**37**) terminate successfully with no following-header access. True rows (**3**) compose exactly one stateless existing-actor header under exact R3.18BD membership and stop at `payload_start`; observed true tags are Boolean=2 / Float=1. Seven upstream AU false terminators remain outside the BA/BE lane. Following payload / second later control consumption is 0/0.

Validation: builder `33129018318/98713908063` SUCCESS; PR #209 closed unmerged with exact-head CI `34094630343/101655343287` SUCCESS; published-main CI `34095061141/101656732728` SUCCESS; publication force=false.

The active pass is **R3.18BF published R3.18BE mixed following-header differential**. Use exactly the immutable forty-row BC/BD-backed lane. Require published BE exact 40/40, false=37 / true=3, true headers exact 3/3, exact BD contexts 3/3, Boolean=2 / Float=1, mismatch/reselection 0/0, repeatability/negatives PASS and payload/second-control 0/0. BF is read-only and must not decode a following payload.

Before any dispatch/rerun inspect queued/waiting/in-progress equivalent runs and reuse an existing exact run. Rerun is never polling.
