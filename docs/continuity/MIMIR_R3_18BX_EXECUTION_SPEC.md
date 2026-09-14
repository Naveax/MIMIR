# MIMIR R3.18BX — Exact Following-Header Context Contract After R3.18BW

**Status:** PREPARED / NOT ADMITTED
**Pass type:** contract-only admission
**Evidence authority:** R3.18BW Outcome A candidate evidence
**Production authority:** R3.18BU `43c5d6248e2ea606b2eb0fd95f5c50758c372356` / `d1b7b40ed4e361d9c047e0494fb821688ef7d7b4`
**Production mutation:** forbidden
**Following payload decode:** forbidden
**Second later property-control bit:** forbidden
**Admission gate still open:** R3.18BW same-head natural CI `34843377045` must complete SUCCESS on evidence head `778b12988046da4d186248877bd577eb2a533a58`

## Goal

Freeze the narrowest exact-context contract supported by the immutable R3.18BW two-row lane.

The lane contains exactly two published R3.18BU control rows:

- `external_fixtures/sample_002.replay`: BU=false at `[11239,11240)`, terminates with zero following-header access.
- `test_corpus/largest_100/079_1f838b01-66b5-4963-b62e-64f3d7dbd545.replay`: BU=true at `[3238,3239)`, exposes exactly one following property header and stops at `payload_start=3245`.

R3.18BX does not compose a following header in production. It admits membership only after the R3.18BW same-head CI gate is successful.

## Frozen candidate authority

```text
canonical continuity base             64f81e106338493476954f207a997a2bc7c25c9a / 3f023aa0fb0f4d1c695b5d1e3eaab7b3321ff797
production SHA/tree                   43c5d6248e2ea606b2eb0fd95f5c50758c372356 / d1b7b40ed4e361d9c047e0494fb821688ef7d7b4
BW evidence head/tree                 778b12988046da4d186248877bd577eb2a533a58 / 5a6e7bd95c95f3e38db34a543b396aec747db985
BW evidence run/job                   34843377101/103973337631 SUCCESS
BW artifact                           10346819501 / 3582 / sha256:ee8a1878241b45765a7fa57c64c179c40090836096055fc5626a58724b5796fd
BW header rows                        sha256:003d956cd7b4a8eb266c51d4514f9533a3c147eb4923f3113e08673323fb3a38
BW aggregate                          sha256:12abc510fe9821c6fe3ef21e1ecdc3dc53a9b4235b75ca318a6ba77cd574fa4d
BW negatives                          sha256:f47d318ecfdf47098a697ea2f94e2fdd4a37221925dd260496107ac133858edc
BW validation                         sha256:8dd144e6f69992f8c8a31ac0c196c04a59a2ecea199164fe4860f2e50479f445
BW source scope                       sha256:d91a11794cabcb5e001fe59e66c8b5fcd75ea70a73ce7bf4d925c6af723a8582
BW same-head natural CI               34843377045 / PENDING at candidate preparation
pinned Boxcars                        c70e77df7af81b436cb545d070bb90c82f562d0b
source control rows                   2
false terminators / true headers      1 / 1
unique exact contexts                 1
property ordinal                      8 on 1/1
native/oracle mismatch                0
witness reselection                   0
following payload / second control    0 / 0
```

## Exact candidate membership

```text
(110, 6, 67, LoadoutsOnline, 868, 32, 10, false) x1
```

Tuple field order:

```text
stream_id_bound, prop_id_bits, property_object_index, attribute_tag,
version_major, version_minor, net_version, is_rl_223
```

Membership is complete eight-field equality only. `LoadoutsOnline` alone, property object `67` alone, ordinal `8` alone, version-only matching, or any tuple inherited from R3.18BN/BD/AT is insufficient.

## Required validation and negatives

Admission requires all of the following:

1. R3.18BW evidence run/job remains SUCCESS at the exact frozen evidence head.
2. R3.18BW same-head natural CI `34843377045` completes SUCCESS on that same head. Do not rerun while queued/waiting/in-progress.
3. artifact metadata remains exact and unexpired.
4. downloaded artifact digest matches GitHub metadata.
5. all eight manifest-listed non-self files match the artifact hash list.
6. exact source control partition remains 2 = 1 false terminator + 1 true header.
7. exact context equality is 1/1 and multiplicity sum is 1.
8. false terminator remains outside header membership.
9. tag-only, object-only, ordinal-only, versionless, RL223-dropped/flipped and fabricated tuple membership reject.
10. R3.18BN tuple `(110,6,66,ActiveActor,868,32,10,false)` rejects at this boundary.
11. production/Cargo/fixture/corpus/support mutation remains `0/0/0/0/0`.
12. repository and knowledge archive verification pass.

## Clean scope

Contract/continuity documents only. No Rust source, test, Cargo, fixture, corpus, workflow, support helper, payload decoder, runtime bridge or export change belongs in the eventual clean R3.18BX admission commit.

## Outcome gate

### Outcome A

After the same-head CI gate closes SUCCESS, admit exactly the one eight-field context above with observed multiplicity one, preserve the one BU=false terminator outside membership, and open a separate R3.18BY bounded-production pass.

### Outcome B

A bounded authority, tuple, multiplicity or artifact discrepancy is found. Admit only the supported subset and rewrite the later production spec.

### Outcome C

Same-head CI failure, authority drift, false-row header access, historical-contract inheritance, tuple/RL223 widening, payload/later-control access, production mutation or generalized chaining. Stop without admission.

## Hard stop

No production following-header composition, no following payload, no second later property-control bit, no false-terminator header synthesis, no repeated/generalized property cursor, and no actor/frame/lifecycle/raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.
