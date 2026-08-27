# MIMIR — Next Chat Handoff

Canonical production is now **R3.18BA** at `5d2bca711f528ab1bb607104379af503ff175697` / `6b5140e228c882efea8b3f5ec0b0f6abf2f49a3a`. R3.18BA closed **Outcome A / PRODUCTION**: fixed builder `ce5e27641cb0240e7440b93092be69a8fc5b7a11`, builder `33091339939/98584661482` SUCCESS, validation-only PR #208 exact-head CI `33091594385/98585555551` SUCCESS and closed unmerged, and published-main CI `33092084628/98587299347` SUCCESS.

The production boundary recomputes one exact R3.18AY payload, consumes exactly one following `property_present` bit and stops one bit later. Frozen immutable R3.18AX semantics are false=37 / true=3 across forty valid rows; seven upstream AU false terminators remain outside. Adjacent stream/header/payload/second-control consumption remains 0/0/0/0.

The active pass is **R3.18BB — published-R3.18BA mixed following-control differential**. It is read-only: replay exactly the immutable forty AX witnesses, require published BA exact 40/40 for start/value/end/stop, false=37 / true=3, mismatch 0, witness reselection 0, deterministic repeatability and all bounded negatives. The 37 false rows terminate. Only the exact three true rows may become candidates for a later separate header-evidence pass; BB itself consumes no header or payload.

R3.18AX is the exact bit-level truncation authority (`TRUNCATION_BEFORE_CONTROL=PASS 40/40`). The BA carrier API is byte-slice based and all forty frozen control starts are non-byte-aligned, so do not widen BA with a bit-length transport parameter merely to simulate a partial-byte EOF.

Before any dispatch/rerun inspect queued/waiting/in-progress equivalent runs and reuse an existing exact run. Rerun is never polling.
