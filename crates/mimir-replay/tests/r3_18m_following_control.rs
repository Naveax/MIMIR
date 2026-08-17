use mimir_replay::{
    MinimalReplayNetworkLookupPlanReader, ReplayInput, ReplayNetworkAttributeTagV1,
    ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadV1,
    ReplayNetworkExistingActorSecondPropertyPayloadV1, ReplayNetworkK2DecodeContextV1,
    ReplayNetworkLookupPlanReader, ReplayNetworkLookupPlanV1,
    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_control_v1,
    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_v1,
    decode_replay_network_existing_actor_single_primitive_property_v1,
};
use std::path::PathBuf;

fn plan() -> ReplayNetworkLookupPlanV1 {
    let p =
        PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("../../external_fixtures/sample_001.replay");
    let bytes = std::fs::read(p).unwrap();
    MinimalReplayNetworkLookupPlanReader
        .read_network_lookup_plan(&ReplayInput::Memory {
            label: "r318m".into(),
            bytes,
        })
        .unwrap()
}
fn ctx() -> ReplayNetworkK2DecodeContextV1 {
    ReplayNetworkK2DecodeContextV1 {
        net_version: 10,
        is_rl_223: false,
    }
}
fn bit(bytes: &mut Vec<u8>, p: usize, v: bool) {
    let n = p / 8 + 1;
    if bytes.len() < n {
        bytes.resize(n, 0)
    };
    if v {
        bytes[p / 8] |= 1 << (p % 8)
    } else {
        bytes[p / 8] &= !(1 << (p % 8))
    }
}
fn bits(bytes: &mut Vec<u8>, p: usize, w: usize, v: u64) {
    for i in 0..w {
        bit(bytes, p + i, ((v >> i) & 1) != 0)
    }
}
fn retag(p: &mut ReplayNetworkLookupPlanV1, t: ReplayNetworkAttributeTagV1) {
    p.object_lookups[47]
        .as_mut()
        .unwrap()
        .properties
        .iter_mut()
        .find(|x| x.stream_id == 30)
        .unwrap()
        .tag = t;
}
fn int_packet(start: usize, following: bool, trail: usize) -> Vec<u8> {
    let a = start + 6;
    let e = a + 32;
    let s = e + 6;
    let mut b = vec![];
    bit(&mut b, start, true);
    bits(&mut b, start + 1, 5, 30);
    bits(&mut b, a, 32, 62);
    bit(&mut b, e, true);
    bits(&mut b, e + 1, 5, 30);
    bits(&mut b, s, 32, 0x12345678);
    let end = s + 32;
    bit(&mut b, end, following);
    if trail > 0 {
        bit(&mut b, end + trail, false)
    }
    b
}
fn string_packet(following: bool) -> Vec<u8> {
    let start = 0;
    let a = 6;
    let e = a + 32;
    let s = e + 6;
    let mut b = vec![];
    bit(&mut b, start, true);
    bits(&mut b, 1, 5, 30);
    bits(&mut b, a, 32, 62);
    bit(&mut b, e, true);
    bits(&mut b, e + 1, 5, 30);
    bits(&mut b, s, 32, 7);
    let mut p = s + 32;
    for c in b"ABCDEF" {
        bits(&mut b, p, 8, u64::from(*c));
        p += 8
    }
    bits(&mut b, p, 8, 0x7f);
    p += 8;
    bit(&mut b, p, following);
    b
}
fn prior_int(
    bytes: &[u8],
    start: usize,
    p: &ReplayNetworkLookupPlanV1,
) -> ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadV1 {
    let first = decode_replay_network_existing_actor_single_primitive_property_v1(
        bytes,
        start as u64,
        47,
        p,
    )
    .unwrap();
    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_v1(
        bytes,
        &first,
        p,
        ctx(),
    )
    .unwrap()
}

#[test]
fn true_control_stops_exactly_one_bit_later_aligned_and_unaligned() {
    for start in [0usize, 4, 7] {
        let mut p = plan();
        retag(&mut p, ReplayNetworkAttributeTagV1::Int);
        let b = int_packet(start, true, 12);
        let prior = prior_int(&b, start, &p);
        let got=decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_control_v1(&b,&prior).unwrap();
        assert!(got.following_property_present);
        assert_eq!(got.property_present_start_bit, prior.stop_bit);
        assert_eq!(got.property_present_end_bit, prior.stop_bit + 1);
        assert_eq!(got.stop_bit, prior.stop_bit + 1);
    }
}
#[test]
fn repeatability_and_post_control_poison_are_invariant() {
    let mut p = plan();
    retag(&mut p, ReplayNetworkAttributeTagV1::Int);
    let b = int_packet(4, true, 32);
    let prior = prior_int(&b, 4, &p);
    let one=decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_control_v1(&b,&prior).unwrap();
    let two=decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_control_v1(&b,&prior).unwrap();
    assert_eq!(one, two);
    let mut poisoned = b.clone();
    for i in 0..16 {
        bit(&mut poisoned, one.stop_bit as usize + i, i % 2 == 0)
    }
    let got=decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_control_v1(&poisoned,&prior).unwrap();
    assert_eq!(got, one);
}
#[test]
fn false_control_is_evidence_unadmitted_and_rejected() {
    let mut p = plan();
    retag(&mut p, ReplayNetworkAttributeTagV1::Int);
    let b = int_packet(4, false, 0);
    let prior = prior_int(&b, 4, &p);
    let e=decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_control_v1(&b,&prior).unwrap_err();
    assert!(e.to_string().contains("unadmitted-false-following-control"));
}
#[test]
fn missing_bit_and_inconsistent_prior_fail_closed() {
    let mut p = plan();
    retag(&mut p, ReplayNetworkAttributeTagV1::Int);
    let full = int_packet(4, true, 0);
    let prior = prior_int(&full, 4, &p);
    assert_eq!(prior.stop_bit % 8, 0);
    let truncated = full[..(prior.stop_bit / 8) as usize].to_vec();
    assert!(decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_control_v1(&truncated,&prior).is_err());
    let mut bad = prior.clone();
    bad.stop_bit += 1;
    let e=decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_control_v1(&[],&bad).unwrap_err();
    assert!(e.to_string().contains("prior-stop-mismatch"));
}
#[test]
fn missing_second_payload_or_header_rejects_before_read() {
    let mut p = plan();
    retag(&mut p, ReplayNetworkAttributeTagV1::Int);
    let b = int_packet(4, true, 0);
    let prior = prior_int(&b, 4, &p);
    let mut no_payload = prior.clone();
    no_payload.second_payload = None;
    assert!(decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_control_v1(&[],&no_payload).unwrap_err().to_string().contains("missing-second-payload"));
    let mut no_header = prior.clone();
    no_header.header_composition.second_header = None;
    assert!(decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_control_v1(&[],&no_header).unwrap_err().to_string().contains("missing-second-header"));
}
#[test]
fn exact_context_string_prior_uses_same_true_only_control() {
    let mut p = plan();
    retag(&mut p, ReplayNetworkAttributeTagV1::Int);
    let b = string_packet(true);
    let first =
        decode_replay_network_existing_actor_single_primitive_property_v1(&b, 0, 47, &p).unwrap();
    retag(&mut p, ReplayNetworkAttributeTagV1::String);
    let prior =
        decode_replay_network_existing_actor_after_first_primitive_second_property_payload_v1(
            &b,
            &first,
            &p,
            ctx(),
        )
        .unwrap();
    assert!(matches!(
        &prior.second_payload,
        Some(ReplayNetworkExistingActorSecondPropertyPayloadV1::String(_))
    ));
    let got=decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_control_v1(&b,&prior).unwrap();
    assert!(got.following_property_present);
    assert_eq!(got.stop_bit, prior.stop_bit + 1);
}
