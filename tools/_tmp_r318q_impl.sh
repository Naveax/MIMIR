#!/usr/bin/env bash
set -euxo pipefail

BASE_MAIN='1a3f89e7256c7c7ff4bf6b747a434504f1f2e572'
PRODUCTION_BASE='fd74ba8c520ab83b808730572c41e45d6dc616e6'
CONTRACT_SHA256='0dc2474a368a765c19cc49099fc61822954e9e29d1ce4ba8ad8fe21fe1fa181b'
CANDIDATE_BRANCH='candidate/r318q-following-header-v1'
ROOT="$PWD"
ART="$(mktemp -d)"
WORK="$(mktemp -d)"
TMP="$(mktemp -d)"
trap 'rm -rf "$ART" "$WORK" "$TMP"' EXIT

git fetch origin main evidence/r318o-following-property-header-v1 --force
test "$(git rev-parse origin/main)" = "$BASE_MAIN"
test "$(git rev-parse "$BASE_MAIN:crates/mimir-replay/src/lib.rs")" = '029c48e38ea0257f8cdb3fa8715bde5a789213e7'
test "$(git rev-parse "$PRODUCTION_BASE:crates/mimir-replay/src/lib.rs")" = '029c48e38ea0257f8cdb3fa8715bde5a789213e7'
test "$(git show "$BASE_MAIN:docs/continuity/MIMIR_R3_18P_ADMITTED_HEADER_CONTEXTS.json" | sha256sum | awk '{print $1}')" = "$CONTRACT_SHA256"

test "$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/9284144768" --jq .workflow_run.id)" = '32017369100'
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/9284144768" --jq .workflow_run.head_sha)" = '5046e1594b87ce2828db5faa48aceba456c3166f'
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/9284144768" --jq .size_in_bytes)" = '25129'
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/9284144768" --jq .digest)" = 'sha256:e6dc02f08ad025e816d772227a8c21a595902e45a9d71b5a9eb07c28fab4b94d'
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/9284144768" --jq .expired)" = 'false'
gh run download 32017369100 -n r318o-following-property-header-evidence -D "$ART"
test "$(wc -l < "$ART/r3_18o_artifact_sha256.txt")" -eq 11
(cd "$ART" && sha256sum -c r3_18o_artifact_sha256.txt)
python3 - "$ART/r3_18o_source_summary.json" <<'PY'
import json,sys
d=json.load(open(sys.argv[1],encoding='utf-8'))
assert d['rows']==47
assert d['distinct_exact_header_context_tuples']==18
assert d['witness_reselection']==0
assert d['observer_following_payload_bits_consumed']==0
assert d['observer_another_control_bits_consumed']==0
print('R3_18Q_O_AUTHORITY=PASS rows=47 contexts=18')
PY

git show f3e2ad006413e1357102697d7eb0e5cc24e3cefd:tools/_tmp_r318o_native_probe.rs > "$TMP/r318o_probe.rs"
git worktree add --detach "$WORK" "$BASE_MAIN"
cd "$WORK"

cat >> crates/mimir-replay/src/lib.rs <<'RS'

/// One R3.18P-admitted following property header composed after a valid R3.18M true control.
///
/// This result stops exactly at the following header's payload boundary. It does not decode the
/// following payload, consume another property-control bit, or expose a repeatable property cursor.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingHeaderV1 {
    pub control: ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingControlV1,
    pub following_header: ReplayNetworkExistingActorFirstPropertyHeaderV1,
    pub stop_bit: u64,
}

fn network_existing_actor_after_second_payload_following_header_error(
    category: &str,
    detail: impl Into<String>,
) -> MimirError {
    MimirError::message(format!(
        "replay network after-second-payload following-header error: {category}: {}",
        detail.into()
    ))
}

fn r3_18p_following_header_context_is_admitted(
    stream_id_bound: u32,
    prop_id_bits: u8,
    property_object_index: u32,
    attribute_tag: ReplayNetworkAttributeTagV1,
    context: ReplayNetworkK3DecodeContextV1,
) -> bool {
    matches!(
        (
            stream_id_bound,
            prop_id_bits,
            property_object_index,
            attribute_tag,
            context.version_major,
            context.version_minor,
            context.net_version,
        ),
        (60, 5, 32, ReplayNetworkAttributeTagV1::Boolean, 868, 32, 10)
            | (60, 5, 41, ReplayNetworkAttributeTagV1::Boolean, 868, 32, 10)
            | (60, 5, 78, ReplayNetworkAttributeTagV1::Boolean, 868, 32, 10)
            | (60, 5, 79, ReplayNetworkAttributeTagV1::Boolean, 868, 32, 10)
            | (60, 5, 80, ReplayNetworkAttributeTagV1::ActiveActor, 868, 32, 10)
            | (60, 5, 83, ReplayNetworkAttributeTagV1::ActiveActor, 868, 32, 10)
            | (60, 5, 85, ReplayNetworkAttributeTagV1::Boolean, 868, 32, 10)
            | (60, 5, 87, ReplayNetworkAttributeTagV1::Boolean, 868, 32, 10)
            | (60, 5, 89, ReplayNetworkAttributeTagV1::Boolean, 868, 32, 10)
            | (60, 5, 94, ReplayNetworkAttributeTagV1::Boolean, 868, 32, 10)
            | (60, 5, 102, ReplayNetworkAttributeTagV1::Boolean, 868, 32, 10)
            | (60, 5, 103, ReplayNetworkAttributeTagV1::Boolean, 868, 32, 10)
            | (60, 5, 106, ReplayNetworkAttributeTagV1::Boolean, 868, 32, 10)
            | (60, 5, 116, ReplayNetworkAttributeTagV1::Boolean, 868, 32, 10)
            | (67, 6, 61, ReplayNetworkAttributeTagV1::Boolean, 868, 32, 10)
            | (72, 6, 62, ReplayNetworkAttributeTagV1::Boolean, 868, 32, 10)
            | (72, 6, 65, ReplayNetworkAttributeTagV1::Boolean, 868, 32, 10)
            | (110, 6, 36, ReplayNetworkAttributeTagV1::ActiveActor, 868, 32, 10)
    )
}

/// Compose exactly one following existing-actor property header after a valid R3.18J payload.
///
/// The published R3.18M true-only control is reused as the boundary authority. The stateless
/// property-header primitive is then replayed from that same present-bit coordinate, and the
/// resolved structural tuple must match one of the exact 18 R3.18P contexts including replay
/// version. The function stops at `payload_start` and consumes no following payload or later bit.
pub fn decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_header_v1(
    network_bytes: &[u8],
    prior: &ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadV1,
    lookup_plan: &ReplayNetworkLookupPlanV1,
    context: ReplayNetworkK3DecodeContextV1,
) -> Result<ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingHeaderV1> {
    let control =
        decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_control_v1(
            network_bytes,
            prior,
        )?;
    if !control.following_property_present {
        return Err(network_existing_actor_after_second_payload_following_header_error(
            "invalid-following-control",
            "R3.18Q requires the R3.18M admitted true following control",
        ));
    }

    let second_header = prior
        .header_composition
        .second_header
        .as_ref()
        .ok_or_else(|| {
            network_existing_actor_after_second_payload_following_header_error(
                "missing-second-header",
                "R3.18J prior has no second header",
            )
        })?;
    let actor_object_index = second_header.actor_object_index;
    let following_header = decode_replay_network_existing_actor_first_property_header_v1(
        network_bytes,
        control.property_present_start_bit,
        actor_object_index,
        lookup_plan,
    )?;

    if !following_header.property_present {
        return Err(network_existing_actor_after_second_payload_following_header_error(
            "control-header-mismatch",
            "R3.18M reported a present following property but the header primitive did not",
        ));
    }
    if following_header.property_present_start_bit != control.property_present_start_bit
        || following_header.property_present_end_bit != control.property_present_end_bit
        || control.stop_bit != following_header.property_present_end_bit
    {
        return Err(network_existing_actor_after_second_payload_following_header_error(
            "control-header-boundary-mismatch",
            format!(
                "control bits [{}, {}) stop {}, header bits [{}, {})",
                control.property_present_start_bit,
                control.property_present_end_bit,
                control.stop_bit,
                following_header.property_present_start_bit,
                following_header.property_present_end_bit
            ),
        ));
    }
    if following_header.actor_object_index != actor_object_index {
        return Err(network_existing_actor_after_second_payload_following_header_error(
            "actor-mismatch",
            format!(
                "prior actor {actor_object_index} differs from following header actor {}",
                following_header.actor_object_index
            ),
        ));
    }

    let payload_start_bit = following_header.payload_start_bit.ok_or_else(|| {
        network_existing_actor_after_second_payload_following_header_error(
            "missing-payload-start",
            "present following header has no payload start",
        )
    })?;
    if following_header.stop_bit != payload_start_bit {
        return Err(network_existing_actor_after_second_payload_following_header_error(
            "payload-boundary-mismatch",
            format!(
                "following header stop {} differs from payload start {payload_start_bit}",
                following_header.stop_bit
            ),
        ));
    }

    let (
        Some(stream_id_bound),
        Some(prop_id_bits),
        Some(property_object_index),
        Some(attribute_tag),
    ) = (
        following_header.stream_id_bound,
        following_header.prop_id_bits,
        following_header.resolved_property_object_index,
        following_header.resolved_attribute_tag,
    )
    else {
        return Err(network_existing_actor_after_second_payload_following_header_error(
            "incomplete-header-context",
            "following header is missing one or more R3.18P tuple fields",
        ));
    };

    if !r3_18p_following_header_context_is_admitted(
        stream_id_bound,
        prop_id_bits,
        property_object_index,
        attribute_tag,
        context,
    ) {
        return Err(network_existing_actor_after_second_payload_following_header_error(
            "unadmitted-following-header-context",
            format!(
                "R3.18P exact tuple rejected bound={stream_id_bound} bits={prop_id_bits} object={property_object_index} tag={attribute_tag:?} version={}.{} net{}",
                context.version_major, context.version_minor, context.net_version
            ),
        ));
    }

    Ok(
        ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingHeaderV1 {
            control,
            stop_bit: payload_start_bit,
            following_header,
        },
    )
}

#[cfg(test)]
mod r3_18q_following_header_contract_tests {
    use super::*;

    fn context(major: i32, minor: i32, net: i32) -> ReplayNetworkK3DecodeContextV1 {
        ReplayNetworkK3DecodeContextV1 {
            version_major: major,
            version_minor: minor,
            net_version: net,
            is_rl_223: false,
        }
    }

    #[test]
    fn r3_18q_all_eighteen_exact_r3_18p_tuple_identities_are_admitted() {
        let admitted = [
            (60, 5, 32, ReplayNetworkAttributeTagV1::Boolean),
            (60, 5, 41, ReplayNetworkAttributeTagV1::Boolean),
            (60, 5, 78, ReplayNetworkAttributeTagV1::Boolean),
            (60, 5, 79, ReplayNetworkAttributeTagV1::Boolean),
            (60, 5, 80, ReplayNetworkAttributeTagV1::ActiveActor),
            (60, 5, 83, ReplayNetworkAttributeTagV1::ActiveActor),
            (60, 5, 85, ReplayNetworkAttributeTagV1::Boolean),
            (60, 5, 87, ReplayNetworkAttributeTagV1::Boolean),
            (60, 5, 89, ReplayNetworkAttributeTagV1::Boolean),
            (60, 5, 94, ReplayNetworkAttributeTagV1::Boolean),
            (60, 5, 102, ReplayNetworkAttributeTagV1::Boolean),
            (60, 5, 103, ReplayNetworkAttributeTagV1::Boolean),
            (60, 5, 106, ReplayNetworkAttributeTagV1::Boolean),
            (60, 5, 116, ReplayNetworkAttributeTagV1::Boolean),
            (67, 6, 61, ReplayNetworkAttributeTagV1::Boolean),
            (72, 6, 62, ReplayNetworkAttributeTagV1::Boolean),
            (72, 6, 65, ReplayNetworkAttributeTagV1::Boolean),
            (110, 6, 36, ReplayNetworkAttributeTagV1::ActiveActor),
        ];
        assert_eq!(admitted.len(), 18);
        for (bound, bits, object, tag) in admitted {
            assert!(r3_18p_following_header_context_is_admitted(
                bound,
                bits,
                object,
                tag,
                context(868, 32, 10)
            ));
        }
    }

    #[test]
    fn r3_18q_exact_membership_rejects_component_cartesian_tag_and_version_widening() {
        let ctx = context(868, 32, 10);
        assert!(!r3_18p_following_header_context_is_admitted(
            60,
            5,
            32,
            ReplayNetworkAttributeTagV1::ActiveActor,
            ctx
        ));
        assert!(!r3_18p_following_header_context_is_admitted(
            60,
            5,
            33,
            ReplayNetworkAttributeTagV1::Boolean,
            ctx
        ));
        assert!(!r3_18p_following_header_context_is_admitted(
            67,
            6,
            62,
            ReplayNetworkAttributeTagV1::Boolean,
            ctx
        ));
        assert!(!r3_18p_following_header_context_is_admitted(
            60,
            5,
            32,
            ReplayNetworkAttributeTagV1::Boolean,
            context(868, 31, 10)
        ));
        assert!(!r3_18p_following_header_context_is_admitted(
            60,
            5,
            32,
            ReplayNetworkAttributeTagV1::Boolean,
            context(868, 32, 9)
        ));
        assert!(!r3_18p_following_header_context_is_admitted(
            999,
            9,
            999,
            ReplayNetworkAttributeTagV1::Boolean,
            ctx
        ));
    }
}
RS

cat > crates/mimir-replay/tests/r3_18q_following_header.rs <<'RS'
use mimir_replay::{
    MinimalReplayContentScaffoldReader, MinimalReplayNetworkLookupPlanReader,
    ReplayContentScaffoldReader, ReplayInput, ReplayNetworkAttributeTagV1,
    ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadV1,
    ReplayNetworkK2DecodeContextV1, ReplayNetworkK3DecodeContextV1,
    ReplayNetworkLookupPlanReader, ReplayNetworkLookupPlanV1,
    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_control_v1,
    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_header_v1,
    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_v1,
    decode_replay_network_existing_actor_single_primitive_property_v1,
};
use std::path::PathBuf;

fn sample_network_and_plan() -> (Vec<u8>, ReplayNetworkLookupPlanV1) {
    let path =
        PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("../../external_fixtures/sample_001.replay");
    let replay_bytes = std::fs::read(path).expect("read sample_001.replay");
    let input = ReplayInput::Memory {
        label: "r318q_sample_001".to_owned(),
        bytes: replay_bytes.clone(),
    };
    let scaffold = MinimalReplayContentScaffoldReader
        .read_content_scaffold(&input)
        .expect("content scaffold");
    let network = replay_bytes[usize::try_from(scaffold.network_start).unwrap()
        ..usize::try_from(scaffold.network_end).unwrap()]
        .to_vec();
    let plan = MinimalReplayNetworkLookupPlanReader
        .read_network_lookup_plan(&input)
        .expect("lookup plan");
    (network, plan)
}

fn r3_18j_prior(
    network: &[u8],
    plan: &ReplayNetworkLookupPlanV1,
) -> ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadV1 {
    let first = decode_replay_network_existing_actor_single_primitive_property_v1(
        network, 10227, 98, plan,
    )
    .expect("R3.18B first property");
    assert_eq!(first.stop_bit, 10266);
    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_v1(
        network,
        &first,
        plan,
        ReplayNetworkK2DecodeContextV1 {
            net_version: 10,
            is_rl_223: false,
        },
    )
    .expect("R3.18J second payload")
}

fn context() -> ReplayNetworkK3DecodeContextV1 {
    ReplayNetworkK3DecodeContextV1 {
        version_major: 868,
        version_minor: 32,
        net_version: 10,
        is_rl_223: false,
    }
}

fn set_bit(bytes: &mut [u8], position: usize, value: bool) {
    if value {
        bytes[position / 8] |= 1 << (position % 8);
    } else {
        bytes[position / 8] &= !(1 << (position % 8));
    }
}

#[test]
fn r3_18q_sample_001_composes_exact_admitted_header_and_preserves_r3_18m_control() {
    let (network, plan) = sample_network_and_plan();
    let prior = r3_18j_prior(&network, &plan);
    assert_eq!(prior.stop_bit, 10305);
    let m = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_control_v1(
        &network, &prior,
    )
    .expect("R3.18M control");
    let q = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_header_v1(
        &network, &prior, &plan, context(),
    )
    .expect("R3.18Q following header");

    assert_eq!(q.control, m);
    assert_eq!(q.control.property_present_start_bit, 10305);
    assert_eq!(q.control.stop_bit, 10306);
    assert!(q.following_header.property_present);
    assert_eq!(q.following_header.stream_id, Some(33));
    assert_eq!(q.following_header.stream_id_bound, Some(67));
    assert_eq!(q.following_header.prop_id_bits, Some(6));
    assert_eq!(q.following_header.resolved_property_object_index, Some(61));
    assert_eq!(
        q.following_header.resolved_attribute_tag,
        Some(ReplayNetworkAttributeTagV1::Boolean)
    );
    assert_eq!(q.following_header.payload_start_bit, Some(10312));
    assert_eq!(q.following_header.stop_bit, 10312);
    assert_eq!(q.stop_bit, 10312);
}

#[test]
fn r3_18q_post_payload_poison_cannot_change_header_result() {
    let (network, plan) = sample_network_and_plan();
    let prior = r3_18j_prior(&network, &plan);
    let clean = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_header_v1(
        &network, &prior, &plan, context(),
    )
    .unwrap();
    let mut poisoned = network.clone();
    for offset in 0..16usize {
        set_bit(&mut poisoned, 10312 + offset, offset % 2 == 0);
    }
    let got = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_header_v1(
        &poisoned, &prior, &plan, context(),
    )
    .unwrap();
    assert_eq!(got, clean);
}

#[test]
fn r3_18q_truncation_and_wrong_actor_fail_closed() {
    let (network, plan) = sample_network_and_plan();
    let prior = r3_18j_prior(&network, &plan);
    let truncated = &network[..1288];
    assert!(
        decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_header_v1(
            truncated, &prior, &plan, context(),
        )
        .is_err()
    );

    let mut wrong_actor = prior.clone();
    wrong_actor
        .header_composition
        .second_header
        .as_mut()
        .unwrap()
        .actor_object_index = u32::MAX;
    assert!(
        decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_header_v1(
            &network, &wrong_actor, &plan, context(),
        )
        .is_err()
    );
}

#[test]
fn r3_18q_fabricated_cartesian_tuple_and_wrong_version_are_rejected() {
    let (network, plan) = sample_network_and_plan();
    let prior = r3_18j_prior(&network, &plan);

    let mut fabricated_plan = plan.clone();
    let property = fabricated_plan.object_lookups[98]
        .as_mut()
        .unwrap()
        .properties
        .iter_mut()
        .find(|property| property.stream_id == 33)
        .unwrap();
    assert_eq!(property.object_index, 61);
    property.object_index = 62;
    let fabricated = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_header_v1(
        &network, &prior, &fabricated_plan, context(),
    )
    .unwrap_err();
    assert!(fabricated
        .to_string()
        .contains("unadmitted-following-header-context"));

    let wrong_version = ReplayNetworkK3DecodeContextV1 {
        version_major: 868,
        version_minor: 31,
        net_version: 10,
        is_rl_223: false,
    };
    let error = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_header_v1(
        &network, &prior, &plan, wrong_version,
    )
    .unwrap_err();
    assert!(error
        .to_string()
        .contains("unadmitted-following-header-context"));
}
RS

git add -N crates/mimir-replay/tests/r3_18q_following_header.rs
cargo +1.85.0 fmt --all
git diff --check
cargo +1.85.0 test --locked -p mimir-replay r3_18q -- --nocapture

mkdir -p crates/mimir-replay/examples
cp "$TMP/r318o_probe.rs" crates/mimir-replay/examples/_tmp_r318q_probe.rs
python3 - crates/mimir-replay/examples/_tmp_r318q_probe.rs <<'PY'
from pathlib import Path
import sys
p=Path(sys.argv[1])
s=p.read_text(encoding='utf-8')
old='ReplayNetworkK2DecodeContextV1, ReplayNetworkLookupPlanReader,'
new='ReplayNetworkK2DecodeContextV1, ReplayNetworkK3DecodeContextV1, ReplayNetworkLookupPlanReader,'
assert s.count(old)==1
s=s.replace(old,new,1)
old='    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_control_v1,\n'
new=old+'    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_header_v1,\n'
assert s.count(old)==1
s=s.replace(old,new,1)
old='    let mut header_count = 0usize;\n'
assert s.count(old)==1
s=s.replace(old,old+'    let mut q_count = 0usize;\n',1)
for old,new in [
    ('        let _version_major: u32 = f[36].parse()?;','        let version_major: i32 = f[36].parse()?;'),
    ('        let _version_minor: u32 = f[37].parse()?;','        let version_minor: i32 = f[37].parse()?;'),
    ('        let _net_version: u32 = f[38].parse()?;','        let net_version: i32 = f[38].parse()?;'),
]:
    assert s.count(old)==1,(old,s.count(old))
    s=s.replace(old,new,1)
needle='''        header_count += 1;\n\n        let repeated = decode_replay_network_existing_actor_first_property_header_v1('''
insert='''        header_count += 1;\n\n        let q = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_header_v1(\n            &network,\n            &decoded,\n            &plan,\n            ReplayNetworkK3DecodeContextV1 {\n                version_major,\n                version_minor,\n                net_version,\n                is_rl_223: false,\n            },\n        )?;\n        if q.control != control || q.following_header != following || q.stop_bit != expected_payload_start {\n            return Err(format!("{label}: R3.18Q composition mismatch").into());\n        }\n        q_count += 1;\n\n        let repeated = decode_replay_network_existing_actor_first_property_header_v1('''
assert s.count(needle)==1
s=s.replace(needle,insert,1)
old='''    if rows != 47 || r3_18j_count != 47 || r3_18m_count != 47 || header_count != 47\n        || trunc_property_count != 47 || trunc_stream_count != 47 || stop_negative_count != 47'''
new='''    if rows != 47 || r3_18j_count != 47 || r3_18m_count != 47 || header_count != 47 || q_count != 47\n        || trunc_property_count != 47 || trunc_stream_count != 47 || stop_negative_count != 47'''
assert s.count(old)==1,s.count(old)
s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8',newline='\n')
PY
cargo +1.85.0 fmt --all
cargo +1.85.0 build --locked -p mimir-replay --example _tmp_r318q_probe
./target/debug/examples/_tmp_r318q_probe "$ART/r3_18o_targets.tsv" | tee "$TMP/native1.log"
./target/debug/examples/_tmp_r318q_probe "$ART/r3_18o_targets.tsv" > "$TMP/native2.log"
cmp "$TMP/native1.log" "$TMP/native2.log"
test "$(grep -c '^R3_18O_NATIVE' "$TMP/native1.log")" -eq 47
rm -f crates/mimir-replay/examples/_tmp_r318q_probe.rs
rmdir crates/mimir-replay/examples 2>/dev/null || true
cargo +1.85.0 fmt --all -- --check

expected=(
  crates/mimir-replay/src/lib.rs
  crates/mimir-replay/tests/r3_18q_following_header.rs
)
mapfile -t changed < <(git status --short | sed -E 's/^.. //' | sort)
mapfile -t want < <(printf '%s\n' "${expected[@]}" | sort)
test "${#changed[@]}" -eq 2
test "$(printf '%s\n' "${changed[@]}")" = "$(printf '%s\n' "${want[@]}")"
git diff --exit-code "$BASE_MAIN" -- Cargo.toml Cargo.lock external_fixtures test_corpus scripts docs .github MIMIR_CONTINUE_HERE.md MIMIR_KNOWLEDGE_GRAPH.md

git diff "$BASE_MAIN" -- crates/mimir-replay/src/lib.rs > "$TMP/lib.diff"
sed -n 's/^+//p' "$TMP/lib.diff" > "$TMP/lib.added"
test "$(grep -c 'decode_replay_network_existing_actor_first_property_header_v1(' "$TMP/lib.added")" -eq 1
test "$(grep -c 'decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_control_v1(' "$TMP/lib.added")" -eq 1
! grep -Eq 'NetworkBitCursor::new|\.read_bit\(|\.read_bits_le\(' "$TMP/lib.added"
! grep -Eq 'decode_replay_network_existing_actor_after_first_primitive_second_property_payload_v1\(' "$TMP/lib.added"

pwsh -NoProfile -File scripts/verify_repo.ps1
git diff --check

git config user.name 'MIMIR Admission Bot'
git config user.email 'actions@users.noreply.github.com'
git add -- "${expected[@]}"
git commit -m 'Implement R3.18Q bounded following header'
SHA="$(git rev-parse HEAD)"
TREE="$(git rev-parse HEAD^{tree})"
LIB_BLOB="$(git rev-parse HEAD:crates/mimir-replay/src/lib.rs)"
TEST_BLOB="$(git rev-parse HEAD:crates/mimir-replay/tests/r3_18q_following_header.rs)"
test "$(git rev-parse HEAD^)" = "$BASE_MAIN"
test "$(git diff --name-only "$BASE_MAIN" HEAD | sort)" = "$(printf '%s\n' "${want[@]}")"
git diff --exit-code "$BASE_MAIN" HEAD -- Cargo.toml Cargo.lock external_fixtures test_corpus scripts docs .github MIMIR_CONTINUE_HERE.md MIMIR_KNOWLEDGE_GRAPH.md
pwsh -NoProfile -File scripts/verify_repo.ps1

if git ls-remote --exit-code --heads origin "$CANDIDATE_BRANCH" >/dev/null 2>&1; then
  echo "candidate branch already exists" >&2
  exit 1
fi
git push origin "HEAD:refs/heads/$CANDIDATE_BRANCH"
test "$(git ls-remote origin "refs/heads/$CANDIDATE_BRANCH" | awk '{print $1}')" = "$SHA"

mkdir -p "$ROOT/r3_18q_authority"
cp "$TMP/native1.log" "$ROOT/r3_18q_authority/r3_18q_native_47.log"
printf 'R3_18Q_OUTCOME=A\nR3_18Q_CLEAN_SHA=%s\nR3_18Q_CLEAN_TREE=%s\nR3_18Q_PARENT=%s\nR3_18Q_LIB_BLOB=%s\nR3_18Q_TEST_BLOB=%s\nR3_18Q_SCOPE=2_PRODUCTION_FILES\nR3_18Q_CONTRACT_SHA256=%s\nR3_18Q_CONTEXTS=18\nR3_18Q_NATIVE_ROWS=47/47\nR3_18Q_R318M_CONTROL_EQUAL=47/47\nR3_18Q_PAYLOAD_BITS_CONSUMED=0\nR3_18Q_ANOTHER_CONTROL_BITS_CONSUMED=0\n' \
  "$SHA" "$TREE" "$BASE_MAIN" "$LIB_BLOB" "$TEST_BLOB" "$CONTRACT_SHA256" > "$ROOT/r3_18q_authority/receipt.txt"
