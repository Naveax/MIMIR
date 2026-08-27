include!("r3_18au_post_aq_following_header.rs");
use mimir_replay::decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_v1 as decode_ay;

#[test]
fn r3_18ay_exact_aw_lane_and_hard_stop() {
    let (mut t, mut f, mut low) = (0usize, 0usize, 0usize);
    for (i, (path, first, actor, control_start)) in au_cases().into_iter().enumerate() {
        let (network, plan) = frozen_network_and_plan(path, &format!("r318ay_{i}"));
        let (prior, control, an) = aq_from_frozen(&network, &plan, first, actor);
        assert_eq!(an.stop_bit, control_start, "{path}");
        let aq=decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_v1(&network,&prior,&control,&plan,k3_context(),&an).unwrap();
        let au=decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_following_header_v1(&network,&prior,&control,&plan,k3_context(),&an,&aq).unwrap();
        if au.following_header.is_none() {
            f += 1;
            assert!(decode_ay(&network, &prior, &control, &plan, k3_context(), &an, &au).is_err());
            continue;
        }
        t += 1;
        let got = decode_ay(&network, &prior, &control, &plan, k3_context(), &an, &au).unwrap();
        let h = au.following_header.as_ref().unwrap();
        let start = h.payload_start_bit.unwrap();
        let end = start + 32;
        let expected = if path.contains("079_1f838b01-66b5-4963-b62e-64f3d7dbd545") {
            low += 1;
            5
        } else {
            300
        };
        assert_eq!(got.header_composition, au, "{path}");
        assert_eq!(
            got.following_payload.attribute_tag,
            ReplayNetworkAttributeTagV1::Int,
            "{path}"
        );
        assert_eq!(
            (
                got.following_payload.payload_start_bit,
                got.following_payload.payload_end_bit,
                got.following_payload.payload_width,
                got.following_payload.stop_bit,
                got.stop_bit
            ),
            (start, end, 32, end, end),
            "{path}"
        );
        assert_eq!(
            got.following_payload.value,
            ReplayNetworkPrimitiveScalarValueV1::Int(expected),
            "{path}"
        );
        let direct = decode_replay_network_primitive_scalar_v1(
            &network,
            start,
            ReplayNetworkAttributeTagV1::Int,
        )
        .unwrap();
        assert_eq!(got.following_payload, direct, "{path}");
        assert_eq!(
            decode_ay(&network, &prior, &control, &plan, k3_context(), &an, &au).unwrap(),
            got,
            "{path}"
        );
        let mut poisoned = network.clone();
        let bit = usize::try_from(got.stop_bit).unwrap();
        if bit < poisoned.len() * 8 {
            let old = ((poisoned[bit / 8] >> (bit % 8)) & 1) != 0;
            set_bit(&mut poisoned, bit, !old);
            assert_eq!(
                decode_ay(&poisoned, &prior, &control, &plan, k3_context(), &an, &au).unwrap(),
                got,
                "{path}"
            );
        }
    }
    assert_eq!((t, f, low), (40, 7, 1));
}

#[test]
fn r3_18ay_negative_authority_and_truncation_controls() {
    let (network, plan) =
        frozen_network_and_plan("../../external_fixtures/sample_001.replay", "r318ay_neg");
    let (prior, control, an) = aq_from_frozen(&network, &plan, 10227, 98);
    let aq=decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_v1(&network,&prior,&control,&plan,k3_context(),&an).unwrap();
    let au=decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_following_header_v1(&network,&prior,&control,&plan,k3_context(),&an,&aq).unwrap();
    let base = decode_ay(&network, &prior, &control, &plan, k3_context(), &an, &au).unwrap();
    let n = usize::try_from((base.stop_bit - 1) / 8).unwrap();
    assert!(n * 8 >= usize::try_from(au.stop_bit).unwrap());
    assert!(
        decode_ay(
            &network[..n],
            &prior,
            &control,
            &plan,
            k3_context(),
            &an,
            &au
        )
        .is_err()
    );
    let mut bad = au.clone();
    bad.stop_bit += 1;
    assert!(decode_ay(&network, &prior, &control, &plan, k3_context(), &an, &bad).is_err());
    bad = au.clone();
    bad.following_header
        .as_mut()
        .unwrap()
        .resolved_attribute_tag = Some(ReplayNetworkAttributeTagV1::Boolean);
    assert!(decode_ay(&network, &prior, &control, &plan, k3_context(), &an, &bad).is_err());
    bad = au.clone();
    bad.following_header.as_mut().unwrap().payload_start_bit = Some(au.stop_bit + 1);
    assert!(decode_ay(&network, &prior, &control, &plan, k3_context(), &an, &bad).is_err());
    bad = au.clone();
    bad.following_header.as_mut().unwrap().stream_id_bound = Some(60);
    assert!(decode_ay(&network, &prior, &control, &plan, k3_context(), &an, &bad).is_err());
    let mut bad_an = an.clone();
    bad_an
        .header_composition
        .following_header
        .actor_object_index = u32::MAX;
    assert!(
        decode_ay(
            &network,
            &prior,
            &control,
            &plan,
            k3_context(),
            &bad_an,
            &au
        )
        .is_err()
    );
    let mut bad_plan = plan.clone();
    let h = au.following_header.as_ref().unwrap();
    let ai = usize::try_from(h.actor_object_index).unwrap();
    let sid = h.stream_id.unwrap();
    if let Some(l) = bad_plan.object_lookups.get_mut(ai).and_then(Option::as_mut) {
        l.properties.retain(|p| p.stream_id != sid);
    }
    assert!(
        decode_ay(
            &network,
            &prior,
            &control,
            &bad_plan,
            k3_context(),
            &an,
            &au
        )
        .is_err()
    );
    let mut ctx = k3_context();
    ctx.version_minor -= 1;
    assert!(decode_ay(&network, &prior, &control, &plan, ctx, &an, &au).is_err());
    let mut ctx = k3_context();
    ctx.is_rl_223 = true;
    assert!(decode_ay(&network, &prior, &control, &plan, ctx, &an, &au).is_err());
}

#[test]
fn r3_18ay_source_scope_is_one_payload_and_no_later_control_loop() {
    let s = include_str!("../src/lib.rs");
    let b = s
        .split_once("// R3.18AY PRE-ADMISSION BEGIN bounded post-AU one-following-payload")
        .unwrap()
        .1
        .split_once("// R3.18AY PRE-ADMISSION END bounded post-AU one-following-payload")
        .unwrap()
        .0;
    assert_eq!(
        b.matches("decode_replay_network_primitive_scalar_v1(")
            .count(),
        1
    );
    assert_eq!(b.matches("decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_following_header_v1(").count(),1);
    assert!(
        b.find("unadmitted-false-terminator").unwrap()
            < b.find("decode_replay_network_primitive_scalar_v1(")
                .unwrap()
    );
    for x in [
        "NetworkBitCursor",
        ".read_bit(",
        "decode_replay_network_k2_v1(",
        "loop {",
        "while ",
    ] {
        assert_eq!(b.matches(x).count(), 0, "forbidden AY token: {x}");
    }
}
