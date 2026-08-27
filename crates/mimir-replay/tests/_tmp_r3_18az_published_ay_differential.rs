include!("r3_18ay_post_au_payload.rs");

#[derive(Debug, Clone)]
struct AwExpected {
    start: u64,
    end: u64,
    width: u8,
    value: i32,
}

fn aw_expected_rows() -> BTreeMap<String, AwExpected> {
    let path = std::env::var("R318AZ_AW_COMPARE").expect("R318AZ_AW_COMPARE");
    let text = std::fs::read_to_string(path).expect("read AW compare");
    let mut out = BTreeMap::new();
    for line in text.lines().filter(|line| !line.trim().is_empty()) {
        let mut fields = BTreeMap::<String, String>::new();
        for field in line.split('\t').skip(1) {
            let (key, value) = field.split_once('=').expect("key=value");
            fields.insert(key.to_owned(), value.to_owned());
        }
        let label = fields.remove("label").expect("label");
        assert_eq!(fields.get("mismatch").map(String::as_str), Some("0"));
        let row = AwExpected {
            start: fields["payload_start"].parse().unwrap(),
            end: fields["payload_end"].parse().unwrap(),
            width: fields["width"].parse().unwrap(),
            value: fields["semantic_int"].parse().unwrap(),
        };
        assert!(out.insert(label, row).is_none());
    }
    assert_eq!(out.len(), 40);
    out
}

#[test]
fn r3_18az_published_ay_matches_frozen_aw_rows_exactly() {
    let expected = aw_expected_rows();
    let mut published_rows = Vec::new();
    let mut true_rows = 0usize;
    let mut false_rows = 0usize;

    for (i, (path, first, actor, control_start)) in au_cases().into_iter().enumerate() {
        let label = path.strip_prefix("../../").unwrap_or(path);
        let (network, plan) = frozen_network_and_plan(path, &format!("r318az_{i}"));
        let (prior, control, an) = aq_from_frozen(&network, &plan, first, actor);
        assert_eq!(an.stop_bit, control_start, "{label}");

        let aq = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_v1(
            &network, &prior, &control, &plan, k3_context(), &an
        ).unwrap();
        let au = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_following_header_v1(
            &network, &prior, &control, &plan, k3_context(), &an, &aq
        ).unwrap();

        if au.following_header.is_none() {
            false_rows += 1;
            assert!(!expected.contains_key(label), "false terminator widened: {label}");
            assert!(decode_ay(&network, &prior, &control, &plan, k3_context(), &an, &au).is_err());
            continue;
        }

        true_rows += 1;
        let exp = expected.get(label).unwrap_or_else(|| panic!("missing frozen AW row: {label}"));
        let got = decode_ay(&network, &prior, &control, &plan, k3_context(), &an, &au).unwrap();
        let direct = decode_replay_network_primitive_scalar_v1(
            &network,
            exp.start,
            ReplayNetworkAttributeTagV1::Int,
        ).unwrap();

        assert_eq!(got.header_composition, au, "{label}");
        assert_eq!(au.stop_bit, exp.start, "{label}");
        assert_eq!(got.following_payload.attribute_tag, ReplayNetworkAttributeTagV1::Int, "{label}");
        assert_eq!(
            (
                got.following_payload.payload_start_bit,
                got.following_payload.payload_end_bit,
                got.following_payload.payload_width,
                got.following_payload.stop_bit,
                got.stop_bit,
            ),
            (exp.start, exp.end, exp.width, exp.end, exp.end),
            "{label}"
        );
        assert_eq!(got.following_payload, direct, "{label}");
        let value = match got.following_payload.value {
            ReplayNetworkPrimitiveScalarValueV1::Int(value) => value,
            ref other => panic!("unexpected value for {label}: {other:?}"),
        };
        assert_eq!(value, exp.value, "{label}");

        let repeat = decode_ay(&network, &prior, &control, &plan, k3_context(), &an, &au).unwrap();
        assert_eq!(repeat, got, "{label}");

        let cut_bytes = usize::try_from((exp.end - 1) / 8).unwrap();
        assert!(cut_bytes * 8 >= usize::try_from(exp.start).unwrap(), "{label}");
        assert!(
            decode_ay(&network[..cut_bytes], &prior, &control, &plan, k3_context(), &an, &au).is_err(),
            "{label}"
        );

        let mut poisoned = network.clone();
        let bit = usize::try_from(got.stop_bit).unwrap();
        if bit < poisoned.len() * 8 {
            let old = ((poisoned[bit / 8] >> (bit % 8)) & 1) != 0;
            set_bit(&mut poisoned, bit, !old);
            assert_eq!(
                decode_ay(&poisoned, &prior, &control, &plan, k3_context(), &an, &au).unwrap(),
                got,
                "{label}"
            );
        }

        published_rows.push(format!(
            "{label}\t{}\t{}\t{}\t{}\tPASS",
            exp.start, exp.end, exp.width, value
        ));
    }

    assert_eq!((true_rows, false_rows), (40, 7));
    assert_eq!(published_rows.len(), 40);
    let out = std::env::var("R318AZ_PUBLISHED_OUT").expect("R318AZ_PUBLISHED_OUT");
    std::fs::write(
        out,
        format!(
            "label\tpayload_start_bit\tpayload_end_bit\tpayload_width\tsemantic_int\tstatus\n{}\n",
            published_rows.join("\n")
        ),
    ).unwrap();
    println!("R3_18AZ_PUBLISHED_ROWS=40/40 false_terminators=7/7 mismatch=0 reselection=0 following_control_bits=0");
}
