# MIMIR R3.18L — Following-Property Control-Bit Evidence Decision

**Date:** 2026-08-17  
**Outcome:** **A — ADMITTED / READ-ONLY EVIDENCE CLOSED**  
**Production mutation:** **NONE**  
**Production authority remains:** `330ab01890a7c09eff1805e437584fb3be0a1134`

## Decision

R3.18L is admitted. Exactly the 47 R3.18K continuation rows were reused with zero witness reselection. Every row first reproduced the published R3.18J second-property payload result through its frozen stop. Pinned Boxcars and an independent one-bit evidence read then agreed exactly on the next `property_present` start, value and end.

The observed distribution is `false=0 / true=47`. Native/oracle mismatch is zero. No following stream, header or payload bit was consumed. Truncation before the bit, post-control poison invariance, repeatability and prior-stop mismatch controls all passed 47/47. Privacy passed and production/Cargo/fixture/corpus/support mutation remained `0/0/0/0/0`.

## Immutable authority

```text
pre-pass canonical main             1b39cf1abb8b84100349bfe2540296425ef1baed
production SHA/tree                 330ab01890a7c09eff1805e437584fb3be0a1134 / 5540b6a86e53d243dabbabea223a5afa8657521c
evidence head                       9205ac1616e686589938f952782a32f03d0d1488
evidence workflow run/job           31978791346 / 95242213413 SUCCESS
same-head normal CI run/job         31978791304 / 95242213357 SUCCESS
artifact                            9271817700 / 20906 bytes
artifact digest                     sha256:db5d2db96429a4f2b699dca5176fc4d218f9eb9e4faa8dee813b766896f70c1c
frozen rows                         47/47
R3.18J reconstruction               47/47 exact
control false / true                0 / 47
native/oracle mismatch              0
control truncation                  47/47 PASS
repeatability                       47/47 PASS
post-control poison                 47/47 PASS
prior-stop mismatch negative        47/47 PASS
following stream/header/payload     0/0/0 bits consumed
witness reselection                 0
production/Cargo/fixture/corpus/support mutation 0/0/0/0/0
```

### Evidence file SHA-256

```text
7cbfc2e36b116ba9aac9f3daee29e7652a723e5ceb96a96e270118151e16fd7b  r3_18l_source_scope.txt
b02488b13cd6374219bbb89f884b03f8356f3744f930e39b2279df34859015cf  r3_18l_replay_identity.tsv
99461d2c2bf2f17dc41336d6efcd9321ce7ad6fabd2da663d8ddc3509231fdd7  r3_18l_frozen_witnesses.json
0fc4681b94749991a226a07af58709d0074bde3ecf4eae67575512a242f44f99  r3_18l_r318k_authority_sha256.txt
107778cbfc4971ad883c53d4dd8e33d5bd0ebe5a1aadb054b42b83810cb1ca4f  r3_18l_source_summary.json
73afd57f43a2656c5d98f6c97b4c24015283c688a1e343494139ea3ba16d8950  r3_18l_targets.tsv
e607f40bdffe9a9a6df2a3546f33a22811624b6efc5ba073a2b954dd84ecb4cf  r3_18l_boxcars_instrumentation_sha256.txt
f94693fe6ae4babe7fc951013de16fc32c0279e40f1d4957943776d3f3d81381  r3_18l_control_rows.json
f30d66d3b6e5fca1525dc01d1154179cadee58747fdb5bf4dbfdaeb4bd4b59c3  r3_18l_negative_controls.txt
ad1d3b129e34a97f46d0bc3ea879a723e3e46e8d7624e2c9eb8945800b15ee19  r3_18l_aggregate.txt
28f4df430ef84149cdd33a1efc7124fb232d69abd3cb94e6d2196957268985c8  r3_18l_artifact_sha256.txt
```

## Tooling-attempt note

R3.18L v1 and v2 are non-authoritative. v1 stopped on an evidence-probe type mismatch (`u32` versus production `u8` `prop_id_bits`). v2 corrected that but incorrectly forced Rust 1.85 onto the external Boxcars dependency graph; current Boxcars transitive dependencies require a newer compiler. v3 isolates the exact pinned Boxcars source build to stable rustc 1.90.0 while all MIMIR validation remains on rustc 1.85.0. This does not add or change a production dependency.

## Admission boundary

R3.18L proves only the observed true after-second-payload control context. It does **not** prove a false after-second-payload control context because the frozen lane contains no false example. It does not admit the following stream/header/payload or a repeated property loop.

## Next exact pass

`R3.18M — bounded native after-second-payload control-bit composition` may productionize exactly one following control bit from a valid R3.18J result. Success is admitted only when that bit is `true`; false fails closed. The API must stop one bit later and may not resolve or decode anything following it.
