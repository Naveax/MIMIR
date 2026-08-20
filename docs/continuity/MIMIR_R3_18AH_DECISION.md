# MIMIR R3.18AH — Published R3.18AG True-Control Differential Decision

**Date:** 2026-08-20
**Outcome:** **A — ADMITTED / PUBLISHED DIFFERENTIAL EXACT**
**Production mutation:** none
**Canonical production:** `2d351e8ceb601e2fbe515d2977b2103a4b2c7976`

## Decision

R3.18AH closes Outcome A. On exactly the immutable 47 R3.18AF witnesses, the published R3.18AG API accepted the reconstructed valid R3.18AD prior, read exactly the frozen one `property_present` bit and returned identical start/value/end/stop on all 47 rows. The distribution remains **false=0 / true=47** and published/frozen/native mismatch is zero.

This admits only the published differential. It does not admit false success semantics, a generalized property cursor, the following payload, a second later control, alternate UniqueId layouts, next actor/frame iteration or semantic/runtime widening.

## Exact authority

```text
canonical main before admission      0e48eebffbd7f54238835e23c177e732cbeb7978
canonical main tree                  627d02ca39ff732e9dd7137d061432c6a67fafd8
production SHA/tree                  2d351e8ceb601e2fbe515d2977b2103a4b2c7976 / 4123820ce6537f2d4942cd0b5f72b52e43b96c1d
production lib / AG test blobs       db923ebcb419d278f4ab0144fe7ed15b298b60fa / 3f3e1c8f3f6deb7f2558862a1032f8a102131443
AH execution spec blob               94aec628115f43db549ffec2d52338372a6a7459
evidence head/tree                   7389831c626c078d60178c94461ac39e5f427bd5 / 6121bd7d0fab5a5a338a75343d92f11876f71c8b
authority run/job                    32405516670 / 96543562860 SUCCESS
validation PR                        #57 closed unmerged
same-head normal CI                  32406901661 / 96547992406 SUCCESS
artifact                             9420166543 / 11686 bytes
artifact digest / ZIP SHA-256        sha256:b7b9100489a7ae20a959450d0d80fbcda281aee288a00d0c7edd18930cc60df1
continuity builder                   32407844469 / 96551057302
```

The downloaded artifact contains nine evidence payload files plus their SHA-256 manifest. All nine manifest entries verified and the downloaded ZIP SHA-256 equals the GitHub artifact digest exactly.

## Admitted evidence

```text
frozen rows                          47/47
published R3.18AG exact              47/47
published/frozen/native mismatch     0
control false                        0
control true                         47
witness reselection                  0
repeatability                        PASS 47/47
false mutation                       PASS 47/47
truncation before control            PASS 47/47
post-stop poison                     PASS 47/47
prior-stop mismatch                  PASS 47/47
wrong K3 context                     PASS 47/47
next stream bits consumed            0
next header bits consumed            0
next payload bits consumed           0
second later control bits consumed   0
production/Cargo/fixture/corpus/support mutation 0/0/0/0/0
privacy scan                         PASS
```

## Superseded attempts

- `32404962614` reached the scientific lane and regressions but failed only `cargo fmt --check` on the temporary evidence probe. It is not final authority.
- `ffea098d178de21c2542afef05b3535cb99b688e` / `32405211961` failed before science because the runner still froze the pre-rustfmt probe blob. It is not scientific authority.

## Next gate

R3.18AI is a separate read-only structural evidence pass. It may begin exactly at the valid published R3.18AG `stop_bit`, investigate exactly one following property header on the same frozen 47 witnesses and stop exactly at that header's `payload_start`. It may not consume the following payload or another control bit, and it may not generalize into a property loop/cursor.
