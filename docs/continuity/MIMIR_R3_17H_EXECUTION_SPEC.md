# MIMIR R3.17H — Native K2 Differential Audit Execution Spec

**Pass type:** read-only differential audit
**Production implementation:** forbidden
**Native authority:** R3.17G production Outcome A
**Evidence authority:** R3.17E Outcome A

## Goal

Prove that the direct native R3.17G K2 decoder agrees with the pinned Boxcars oracle on the exact privacy-safe witness occurrences selected by immutable R3.17E evidence, without widening production capability.

## Frozen identities

```text
native production SHA        9bfa837c69c4751f70ca63a17c65f0f89877ff32
native source blob           7288238cfb5338653552435be6af41f0dd7a4e85
R3.17E evidence head         19db534a3668f84f1c5ce36ef1252c52841d890f
R3.17E artifact              9219554878
R3.17E artifact digest       sha256:210a9138e7027672b27c2e557741625abba2af4836286ea2e4aa722fa613a0cc
R3.17E witnesses SHA256      7db56e75d6754767d95a11af269ea2c31978a35e83be808bb6c9100eca71cb9b
R3.17E witness rows          469
pinned Boxcars SHA           c70e77df7af81b436cb545d070bb90c82f562d0b
supported replay lane        47
```

## Audit method

1. Verify fresh main and the exact native source blob before doing any evidence work.
2. Verify the 47 replay identities used by R3.17E.
3. Recreate the pinned Boxcars instrumentation from the canonical R3.17E evidence tooling or an exactly equivalent reviewed patch.
4. Decode the 47 replay lane and regenerate raw K2 payload bits plus oracle semantic values only in ephemeral runner storage.
5. Select exactly the 469 witness occurrence identities from immutable `r3_17e_k2_witnesses.jsonl` using structural keys such as replay path, frame, actor ordinal, stream/property identity, tag, context, start/end/width and packed-payload SHA256.
6. Feed each selected packed payload to `decode_replay_network_k2_v1` under the witness context. A temporary audit harness may normalize the witness payload start to bit zero only if it proves the packed bit sequence is identical.
7. Compare native vs oracle in memory for tag/variant, context acceptance, exact consumed width/end, text encoding/declared length, reference/system fields and decoded semantic value.
8. Persist only privacy-safe aggregate rows, structural identifiers, match flags and cryptographic hashes. Do not persist clear player names, account ids, remote ids or replay-private text.

## Required audit gates

```text
witness rows selected                 469 / 469
native decode success                 469 / 469
attribute tag / semantic variant      469 / 469 exact
payload width                         469 / 469 exact
payload end / consumed bits           469 / 469 exact
context gate                          469 / 469 exact
semantic value                        469 / 469 exact in-memory
privacy scan                          PASS
production mutation                   0
Cargo mutation                        0
corpus/fixture mutation               0
```

If a witness cannot be regenerated or matched unambiguously, do not silently replace it. Outcome B must request targeted evidence for the missing identity.

## Required negative controls

The audit harness must also prove that selected nearby unadmitted variants remain rejected, using synthetic privacy-safe payloads only. At minimum cover PartyLeader None, a non-Epic PartyLeader, an unadmitted UniqueId system, wrong net version, RL223 QWordString Empty/UTF16, and wrong Epic declared length.

These negative controls are audit-only and do not widen the production contract.

## Outcome rules

- **Outcome A:** all 469 immutable witnesses match exactly, all negative controls fail closed as contracted, privacy scan passes, and production/Cargo/corpus mutation is zero.
- **Outcome B:** a bounded witness/evidence ambiguity exists; request targeted evidence only.
- **Outcome C:** a native/oracle semantic contradiction or reproducible decoder defect exists; stop widening and open a corrective implementation pass.

## Hard stop

R3.17H must not change production Rust, manifests, fixtures, supported replay policy or downstream capability. It does not admit second-property continuation, actor/frame iteration, lifecycle mutation, K3/K4, raw state, events, replay slicing, skills, runtime or export.

## Next pass

Do not pre-commit the next attribute family. On Outcome A, inspect the remaining canonical roadmap and evidence gaps, then open the first still-unfinished evidence pass under the same evidence -> contract -> implementation -> audit discipline.
