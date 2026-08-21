# MIMIR R3.18AO / AP / AQ — Consolidated Preparatory Index V2

**Status:** PREPARATORY / NON-CANONICAL / DEPENDENCY-GATED
**Preparation parent:** canonical main `fec9dca3cb8366108245788fc9a2b24a0c99fe94` / tree `3bf5f68ec7df5565f78f89fd4bc2254f2a64e010`
**Canonical production at preparation time:** R3.18AK `f20f529e3ada6e9a671ea91e5676a17a00770145`
**Canonical continuity at preparation time:** R3.18AL CLOSED; R3.18AM evidence authority proven but canonical AM continuity admission still pending.

This index consolidates the already-reviewed AO/AP/AQ preparatory specifications onto one fresh-main descendant. The three imported specifications remain planning material only. Their historical `Preparation base` fields describe their source provenance and are not upgraded into authority by copying them here.

## Frozen facts already known

- R3.18AL is canonically CLOSED on main.
- R3.18AM evidence authority is `842b94ed4c4e57323433585fea48116ecf18989b` / tree `486d0a0f3833dcb8872f062ae1927c9aefde87ba`.
- R3.18AM evidence run/job is `32473716883 / 96745647750` SUCCESS.
- R3.18AM same-head CI is `32474038136 / 96746590106` SUCCESS.
- R3.18AM artifact is `9443581172`, 14827 bytes, digest `sha256:2f65de5207bd96787fd7d1527a55991f08d5da614a0ddfce22a7aa267968e3c8`.
- R3.18AM observed exactly 47/47 `Int` payloads, width 32 on 47/47, semantic range 1..415, native/oracle mismatch 0, witness reselection 0 and another-control consumption 0.
- These facts do not authorize R3.18AN production until AM continuity is canonically admitted.

## Dependency gates

```text
R3.18AL CLOSED
  -> R3.18AM canonical continuity admission
  -> R3.18AN bounded payload production publication
  -> R3.18AO published-AN differential
  -> R3.18AP exactly-one-next-control evidence
  -> R3.18AQ bounded next-control production
```

### R3.18AO

AO remains read-only. It must be reconstructed from the then-published AN authority and the immutable AM lane. It must stop exactly at AN payload end and consume zero next-control bits. No payload distribution may be inferred from historical analogues.

### R3.18AP

AP remains evidence-only. It begins exactly at the AO/AN payload stop, reads exactly one `property_present` bit, independently measures the actual false/true distribution and stops one bit later. Earlier true-only control lanes are not evidence for this boundary.

### R3.18AQ

AQ remains production-gated by final AP evidence. Its accepted false/true semantics must be derived only from AP. It must validate/recompute the AN prior, consume exactly one next control bit and stop before any stream/header/payload/second-control access.

## Revalidation rule

When each dependency opens, discard this consolidated branch as authority, fetch fresh canonical main, re-read all newly admitted decisions/specs/receipts and reconstruct the real pass from that parent. Do not cherry-pick these preparatory documents into a canonical production or evidence candidate.

No production, Cargo/dependency, fixture/corpus, workflow, runtime, skill or export behavior is changed by this preparation.
