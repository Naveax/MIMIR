include!("r3_18bu_post_bs_following_control.rs");

#[test]
fn r3_18bv_published_bu_exact_differential() {
    let (mut excluded_au, mut excluded_be, mut false_terminators, mut exact_rows) =
        (0usize, 0usize, 0usize, 0usize);
    let (mut false_controls, mut true_controls) = (0usize, 0usize);

    for (index, (path, first_start, actor_object, _)) in au_cases().into_iter().enumerate() {
        let (network, plan) = frozen_network_and_plan(path, &format!("r318bv_{index}"));
        let (prior, control, an) = aq_from_frozen(&network, &plan, first_start, actor_object);
        let aq = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_v1(
            &network, &prior, &control, &plan, k3_context(), &an,
        )
        .unwrap_or_else(|error| panic!("AQ prerequisite row {index} {path}: {error}"));
        let au = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_following_header_v1(
            &network, &prior, &control, &plan, k3_context(), &an, &aq,
        )
        .unwrap_or_else(|error| panic!("AU prerequisite row {index} {path}: {error}"));

        if au.following_header.is_none() {
            excluded_au += 1;
            continue;
        }

        let ay = decode_ay(&network, &prior, &control, &plan, k3_context(), &an, &au)
            .unwrap_or_else(|error| panic!("AY prerequisite row {index} {path}: {error}"));
        let ba = decode_ba(&network, &prior, &control, &plan, k3_context(), &an, &ay)
            .unwrap_or_else(|error| panic!("BA prerequisite row {index} {path}: {error}"));
        let be = decode_be(
            &network,
            &prior,
            &control,
            &plan,
            k3_context(),
            &an,
            &ay,
            &ba,
        )
        .unwrap_or_else(|error| panic!("BE prerequisite row {index} {path}: {error}"));

        if be.following_header.is_none() {
            excluded_be += 1;
            continue;
        }

        let bi = decode_bi(
            &network,
            &prior,
            &control,
            &plan,
            k3_context(),
            &an,
            &ay,
            &ba,
            &be,
        )
        .unwrap_or_else(|error| panic!("BI prerequisite row {index} {path}: {error}"));
        let bk = decode_bk(
            &network,
            &prior,
            &control,
            &plan,
            k3_context(),
            &an,
            &ay,
            &ba,
            &be,
            &bi,
        )
        .unwrap_or_else(|error| panic!("BK prerequisite row {index} {path}: {error}"));
        let bo = decode_bo(
            &network,
            &prior,
            &control,
            &plan,
            k3_context(),
            &an,
            &ay,
            &ba,
            &be,
            &bi,
            &bk,
        )
        .unwrap_or_else(|error| panic!("BO prerequisite row {index} {path}: {error}"));

        if bo.following_header.is_none() {
            false_terminators += 1;
            assert!(
                path.ends_with("external_fixtures/sample_003.replay"),
                "{path}"
            );
            continue;
        }

        let expected = expected_bu_control(path)
            .unwrap_or_else(|| panic!("unexpected BV authority row {path}"));
        let bs = decode_bs(
            &network,
            &prior,
            &control,
            &plan,
            k3_context(),
            &an,
            &ay,
            &ba,
            &be,
            &bi,
            &bk,
            &bo,
        )
        .unwrap_or_else(|error| panic!("BS prerequisite row {index} {path}: {error}"));
        let got = decode_bu(
            &network,
            &prior,
            &control,
            &plan,
            k3_context(),
            &an,
            &ay,
            &ba,
            &be,
            &bi,
            &bk,
            &bo,
            &bs,
        )
        .unwrap_or_else(|error| panic!("BU differential row {index} {path}: {error}"));

        assert_eq!(got.payload_composition, bs, "{path}");
        assert_eq!(got.control_start_bit, bs.stop_bit, "{path}");
        assert_eq!(got.control_end_bit, got.control_start_bit + 1, "{path}");
        assert_eq!(got.stop_bit, got.control_end_bit, "{path}");
        assert_eq!(got.property_control, expected, "{path}");
        assert_eq!(raw_lsb(&network, got.control_start_bit), expected, "{path}");

        let expected_start = if path.ends_with("external_fixtures/sample_002.replay") {
            11239
        } else {
            3238
        };
        let expected_end = expected_start + 1;
        assert_eq!(got.control_start_bit, expected_start, "{path}");
        assert_eq!(got.control_end_bit, expected_end, "{path}");
        assert_eq!(got.stop_bit, expected_end, "{path}");

        let repeated = decode_bu(
            &network,
            &prior,
            &control,
            &plan,
            k3_context(),
            &an,
            &ay,
            &ba,
            &be,
            &bi,
            &bk,
            &bo,
            &bs,
        )
        .expect("repeat BV published BU decode");
        assert_eq!(repeated, got, "{path}");

        let mut poison = network.clone();
        let poison_bit = usize::try_from(got.stop_bit).expect("BV poison bit fits usize");
        assert!(poison_bit / 8 < poison.len(), "{path}");
        let current = raw_lsb(&poison, got.stop_bit);
        set_bit(&mut poison, poison_bit, !current);
        let poisoned = decode_bu(
            &poison,
            &prior,
            &control,
            &plan,
            k3_context(),
            &an,
            &ay,
            &ba,
            &be,
            &bi,
            &bk,
            &bo,
            &bs,
        )
        .expect("post-BU stop poison must not alter BV result");
        assert_eq!(poisoned, got, "{path}");

        exact_rows += 1;
        if got.property_control {
            true_controls += 1;
        } else {
            false_controls += 1;
        }
        println!(
            "R3_18BV_ROW\t{}\t{}\t{}\t{}\t{}\t{}",
            path,
            got.control_start_bit,
            got.control_end_bit,
            got.stop_bit,
            got.property_control,
            bs.stop_bit
        );
    }

    assert_eq!(excluded_au, 7);
    assert_eq!(excluded_be, 37);
    assert_eq!(false_terminators, 1);
    assert_eq!(exact_rows, 2);
    assert_eq!(false_controls, 1);
    assert_eq!(true_controls, 1);
    assert_eq!(
        excluded_au + excluded_be + false_terminators + exact_rows,
        47
    );
    println!("R3_18BV_EXACT=2/2");
    println!("R3_18BV_FALSE_TRUE=1/1");
    println!("R3_18BV_BP_FALSE_EXCLUDED=1/1");
    println!("R3_18BV_REPEATABILITY=2/2");
    println!("R3_18BV_POST_STOP_POISON=2/2");
    println!("R3_18BV_ADJACENT_CONSUMPTION=0/0/0/0");
}
