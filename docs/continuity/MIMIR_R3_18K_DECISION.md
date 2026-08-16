# MIMIR R3.18K — Published Second-Property Payload Differential Decision

**Date:** 2026-08-17  
**Outcome:** **A — ADMITTED / READ-ONLY EVIDENCE CLOSED**  
**Production mutation:** **NONE**  
**Production authority remains:** `330ab01890a7c09eff1805e437584fb3be0a1134`

## Decision

R3.18K is admitted. The published R3.18J bounded second-property payload composition was differentially exercised on the exact immutable R3.18I 94-row lane with no witness reselection. All 47 terminators and all 47 continuations matched their frozen structural and payload boundaries. Continuation tags remained exactly `Int=46 / String=1`; native/oracle mismatch was zero; the following `property_present` bit was never consumed.

All 47 terminator no-post-control-lookup controls and all 47 real payload truncation controls passed. The exact String wrong-context control, a tag-outside-`Int|String` control, deterministic repeatability and post-payload poison invariance also passed. Privacy passed and production/Cargo/fixture/corpus/support mutation was `0/0/0/0/0`.

## Immutable authority

```text
pre-pass canonical main             0a9bdab3717aacf320459d738a322ce00415fec7
production SHA/tree                 330ab01890a7c09eff1805e437584fb3be0a1134 / 5540b6a86e53d243dabbabea223a5afa8657521c
evidence head                       926ddd88331ef0372b17b495cb06502010ab39ac
evidence workflow run/job           31977860600 / 95239932737 SUCCESS
same-head normal CI run/job         31977860563 / 95239932564 SUCCESS
artifact                            9271561853 / 18744 bytes
artifact digest                     sha256:a455984c1149cb8f186eedb34d3e148fe45b8592c928cd9246d36cd52843262f
frozen rows                         94/94
terminator / continuation           47 / 47
continuation tags                   Int=46 / String=1
terminator no-lookup                47/47
real payload truncation             47/47
native/oracle mismatch              0
following-property bits consumed    0
witness reselection                 0
production/Cargo/fixture/corpus/support mutation 0/0/0/0/0
```

### Evidence file SHA-256

```text
64ed5ce376813534cdc196e35421092db62b6d84dc244950aa51872def38151f  r3_18k_source_scope.txt
b02488b13cd6374219bbb89f884b03f8356f3744f930e39b2279df34859015cf  r3_18k_replay_identity.tsv
99461d2c2bf2f17dc41336d6efcd9321ce7ad6fabd2da663d8ddc3509231fdd7  r3_18k_frozen_witnesses.json
9cf75f074c46a15823556e6f0de32f727d10845382e9631537483dbd952c388e  r3_18k_r318i_authority_sha256.txt
40854122f5c39981514077f66fbf0e51b54d0a07997dc262bb5a6b37fe309f70  r3_18k_authority_summary.json
8ca0503a453550c82fccf500834b79b25cafa6c100fda71b67aa5cb7ee0558ac  r3_18k_comparison.json
f6186113fbbcde35c7670e1415dc967eaa549ffde934625e613893cf04e7b9c9  r3_18k_negative_controls.txt
a746fe172d11d55cd274df105c6a1f65b69b114c0951df0c7c7aa5d0859418bd  r3_18k_aggregate.txt
```

## Hard stop retained

R3.18K does not admit production consumption of the following property control bit. It does not admit a following stream/header/payload, a repeated/general property loop, a generic property cursor, next actor/frame iteration, lifecycle state, raw state, events, replay slices, skills, teacher/runtime/export widening, or dependency/support-lane expansion.

## Next exact pass

`R3.18L — following-property control-bit evidence after one published second payload` may inspect exactly one `property_present` bit at the R3.18J stop on the frozen 47 continuation rows and must stop one bit later.
