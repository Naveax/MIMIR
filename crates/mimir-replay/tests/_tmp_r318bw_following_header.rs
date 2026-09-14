include!("r3_18bu_post_bs_following_control.rs");

fn r3_18bw_boxcars_bounded_u32_at(
    bytes: &[u8],
    start_bit: u64,
    low_width: u8,
    max_exclusive: u32,
) -> (u32, u64) {
    assert!(max_exclusive > 0);
    let mut pos = usize::try_from(start_bit).expect("start bit fits usize");
    let mut low = 0u64;
    for out in 0..usize::from(low_width) {
        let bit = (bytes[pos / 8] >> (pos % 8)) & 1;
        low |= u64::from(bit) << out;
        pos += 1;
    }
    let range = 1u64 << low_width;
    let up = low + range;
    let max = u64::from(max_exclusive);
    let value = if up >= max {
        low
    } else {
        let discriminator = ((bytes[pos / 8] >> (pos % 8)) & 1) != 0;
        pos += 1;
        if discriminator { up } else { low }
    };
    assert!(value < max);
    (
        u32::try_from(value).expect("bounded value fits u32"),
        u64::try_from(pos).expect("end bit fits u64"),
    )
}

#[test]
fn r3_18bw_exact_bv_lane_observes_one_header_on_true_row_only() {
    let (mut false_rows, mut true_rows, mut header_rows) = (0usize, 0usize, 0usize);

    for (index, (path, first_start, actor_object, _)) in au_cases().into_iter().enumerate() {
        let (network, plan) = frozen_network_and_plan(path, &format!("r318bw_{index}"));
        let (prior, control, an) = aq_from_frozen(&network, &plan, first_start, actor_object);
        let aq = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_v1(
            &network, &prior, &control, &plan, k3_context(), &an,
        ).unwrap_or_else(|error| panic!("AQ prerequisite row {index} {path}: {error}"));
        let au = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_following_header_v1(
            &network, &prior, &control, &plan, k3_context(), &an, &aq,
        ).unwrap_or_else(|error| panic!("AU prerequisite row {index} {path}: {error}"));
        if au.following_header.is_none() { continue; }
        let ay = decode_ay(&network, &prior, &control, &plan, k3_context(), &an, &au)
            .unwrap_or_else(|error| panic!("AY prerequisite row {index} {path}: {error}"));
        let ba = decode_ba(&network, &prior, &control, &plan, k3_context(), &an, &ay)
            .unwrap_or_else(|error| panic!("BA prerequisite row {index} {path}: {error}"));
        let be = decode_be(&network, &prior, &control, &plan, k3_context(), &an, &ay, &ba)
            .unwrap_or_else(|error| panic!("BE prerequisite row {index} {path}: {error}"));
        if be.following_header.is_none() { continue; }
        let bi = decode_bi(&network, &prior, &control, &plan, k3_context(), &an, &ay, &ba, &be)
            .unwrap_or_else(|error| panic!("BI prerequisite row {index} {path}: {error}"));
        let bk = decode_bk(&network, &prior, &control, &plan, k3_context(), &an, &ay, &ba, &be, &bi)
            .unwrap_or_else(|error| panic!("BK prerequisite row {index} {path}: {error}"));
        let bo = decode_bo(&network, &prior, &control, &plan, k3_context(), &an, &ay, &ba, &be, &bi, &bk)
            .unwrap_or_else(|error| panic!("BO prerequisite row {index} {path}: {error}"));
        if bo.following_header.is_none() { continue; }
        let bs = decode_bs(&network, &prior, &control, &plan, k3_context(), &an, &ay, &ba, &be, &bi, &bk, &bo)
            .unwrap_or_else(|error| panic!("BS prerequisite row {index} {path}: {error}"));
        let bu = decode_bu(&network, &prior, &control, &plan, k3_context(), &an, &ay, &ba, &be, &bi, &bk, &bo, &bs)
            .unwrap_or_else(|error| panic!("BU prerequisite row {index} {path}: {error}"));

        let expected = expected_bu_control(path).expect("only exact BV/BU authority rows reach BW");
        assert_eq!(bu.property_control, expected, "{path}");
        if !bu.property_control {
            false_rows += 1;
            assert!(path.ends_with("external_fixtures/sample_002.replay"));
            assert_eq!(bu.control_start_bit, 11239);
            assert_eq!(bu.stop_bit, 11240);
            continue;
        }

        true_rows += 1;
        assert!(path.ends_with("test_corpus/largest_100/079_1f838b01-66b5-4963-b62e-64f3d7dbd545.replay"));
        assert_eq!(bu.control_start_bit, 3238);
        assert_eq!(bu.stop_bit, 3239);

        let header = mimir_replay::decode_replay_network_existing_actor_first_property_header_v1(
            &network,
            bu.control_start_bit,
            actor_object,
            &plan,
        ).unwrap_or_else(|error| panic!("BW one-header row {path}: {error}"));

        assert!(header.property_present, "{path}");
        assert_eq!(header.property_present_start_bit, bu.control_start_bit, "{path}");
        assert_eq!(header.property_present_end_bit, bu.control_end_bit, "{path}");
        assert_eq!(header.stream_id_start_bit, Some(bu.stop_bit), "{path}");
        assert_eq!(header.stream_id_bound, Some(110), "{path}");
        assert_eq!(header.prop_id_bits, Some(6), "{path}");

        // Pinned Boxcars c70e77d... uses peek_bits_max_computed: low 6 bits plus
        // exactly one discriminator bit iff low + 64 < max. Reproduce that rule
        // independently at the exact BU stop and require native structural equality.
        let (oracle_stream, oracle_end) =
            r3_18bw_boxcars_bounded_u32_at(&network, bu.stop_bit, 6, 110);
        assert_eq!(header.stream_id, Some(oracle_stream), "{path}");
        assert_eq!(header.stream_id_end_bit, Some(oracle_end), "{path}");
        assert_eq!(header.payload_start_bit, Some(oracle_end), "{path}");
        assert_eq!(header.stop_bit, oracle_end, "{path}");
        assert!(header.resolved_property_object_index.is_some(), "{path}");
        assert!(header.resolved_property_object_name.is_some(), "{path}");
        assert!(header.resolved_attribute_tag.is_some(), "{path}");

        let repeated = mimir_replay::decode_replay_network_existing_actor_first_property_header_v1(
            &network,
            bu.control_start_bit,
            actor_object,
            &plan,
        ).expect("repeat BW one-header observation");
        assert_eq!(repeated, header, "{path}");

        let mut poisoned = network.clone();
        let poison_bit = usize::try_from(header.stop_bit).expect("payload-start poison fits usize");
        assert!(poison_bit / 8 < poisoned.len());
        let old = raw_lsb(&poisoned, header.stop_bit);
        set_bit(&mut poisoned, poison_bit, !old);
        let after_poison = mimir_replay::decode_replay_network_existing_actor_first_property_header_v1(
            &poisoned,
            bu.control_start_bit,
            actor_object,
            &plan,
        ).expect("payload poison must not affect BW header");
        assert_eq!(after_poison, header, "{path}");

        let control_carrier = usize::try_from(bu.control_start_bit / 8).expect("carrier cut fits usize");
        assert!(mimir_replay::decode_replay_network_existing_actor_first_property_header_v1(
            &network[..control_carrier],
            bu.control_start_bit,
            actor_object,
            &plan,
        ).is_err(), "truncation before BW header must fail");

        let mut missing_lookup = plan.clone();
        let actor_slot = usize::try_from(actor_object).expect("actor object fits usize");
        missing_lookup.object_lookups[actor_slot] = None;
        assert!(mimir_replay::decode_replay_network_existing_actor_first_property_header_v1(
            &network,
            bu.control_start_bit,
            actor_object,
            &missing_lookup,
        ).is_err(), "missing actor lookup must fail");

        println!(
            "R3_18BW_HEADER\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{:?}\t{}\t{}",
            path.trim_start_matches("../../"),
            bu.control_start_bit,
            bu.control_end_bit,
            bu.stop_bit,
            oracle_end,
            oracle_stream,
            110,
            6,
            header.resolved_property_object_index.expect("object"),
            header.resolved_attribute_tag.as_ref().expect("tag"),
            header.resolved_property_object_name.as_deref().expect("object name"),
            header.stop_bit,
        );
        header_rows += 1;
    }

    assert_eq!(false_rows, 1, "BV false terminator drift");
    assert_eq!(true_rows, 1, "BV true continuation drift");
    assert_eq!(header_rows, 1, "BW one-header row drift");
    println!("R3_18BW_BV_ROWS=2/2");
    println!("R3_18BW_FALSE_TERMINATOR=1/1");
    println!("R3_18BW_TRUE_ROWS=1/1");
    println!("R3_18BW_ONE_FOLLOWING_HEADER_EXACT=1/1");
    println!("R3_18BW_NATIVE_BOXCARS_BOUNDED_MISMATCH=0");
    println!("R3_18BW_WITNESS_RESELECTION=0");
    println!("R3_18BW_REPEATABILITY=1/1");
    println!("R3_18BW_POST_PAYLOAD_START_POISON=1/1");
    println!("R3_18BW_FOLLOWING_PAYLOAD_SECOND_CONTROL=0/0");
}
