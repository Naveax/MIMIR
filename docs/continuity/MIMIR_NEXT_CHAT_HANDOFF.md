# MIMIR — Next Chat Handoff

Canonical production is **R3.18AQ** at `e1ccbef95c8424b689dee7d77fd8fde2af3e0204` / `4e7100625096594bcc5c5b4c6a8054c283643b13`, parent `ec2d6c29f90863d9e312856043d01fb98a0c2d2d`.

AQ authority: builder `32860339919/97842469079` SUCCESS on helper `4fee8974780fa2f8897bf0fea14ce13333a2dac4`; receipt artifact `9568109670` / `1183` bytes / `sha256:1d865740559cb0748f840b3cca3d4ab9c627ac251bc15f6f99dbabb20c2e3afe`; validation-only PR #197 closed unmerged after exact-head CI `32861522922/97846413853` SUCCESS; published-main CI `32861924684/97847764026` SUCCESS. Clean production scope is exactly `crates/mimir-replay/src/lib.rs` plus `crates/mimir-replay/tests/r3_18aq_post_an_payload_control.rs`.

Published behavior: immutable rows 47; false=7; true=40; both values succeed; exactly one new `property_present` bit is consumed; next stream/header/payload/second-control consumption 0/0/0/0. Wrong actor, unresolved lookup, truncation, corrupt AN prior, wrong context, repeatability and post-stop poison negatives PASS.

The active pass is **R3.18AR**, a read-only published-production differential. Reuse exactly the immutable R3.18AP 47 witnesses and require published AQ value/start/end/stop equality 47/47, false=7, true=40, mismatch 0, witness reselection 0, production mutation 0 and adjacent consumption 0/0/0/0.

Do not decode the following header in AR. The 7 false rows are terminators. Only after AR Outcome A may a separate later pass investigate one following header on the exact 40 true continuation rows.

Before any workflow dispatch/rerun, inspect queued/waiting/in-progress equivalent runs and reuse an existing exact run if present. Rerun is never polling.
