include!("r3_18bo_post_bk_following_header.rs");

#[derive(Debug, Clone)]
struct R318BpFrozenControlRow {
    label: String,
    frame_index: u32,
    actor_ordinal: u32,
    actor_context_object_id: u32,
    payload_end_bit: u64,
    control_start_bit: u64,
    control_end_bit: u64,
    property_present: bool,
}

fn r318bp_normalize_label(path: &str) -> &str {
    path.strip_prefix("../../").unwrap_or(path)
}

fn r318bp_frozen_control_rows() -> Vec<R318BpFrozenControlRow> {
    let path = std::env::var("R318BP_BM_CONTROL_ROWS")
        .expect("R318BP_BM_CONTROL_ROWS must point at immutable BM control rows");
    let text = std::fs::read_to_string(path).expect("read immutable BM control rows");
    let mut lines = text.lines();
    assert_eq!(
        lines.next(),
        Some("label\tframe_index\tactor_ordinal\tactor_context_object_id\tpayload_end_bit\tnext_property_present_start_bit\tnext_property_present_end_bit\tnext_property_present"),
        "BM control-row schema drift",
    );
    let mut rows = Vec::new();
    for line in lines.filter(|line| !line.is_empty()) {
        let fields = line.split('\t').collect::<Vec<_>>();
        assert_eq!(fields.len(), 8, "BM control-row field-count drift: {line}");
        rows.push(R318BpFrozenControlRow {
            label: fields[0].to_owned(),
            frame_index: fields[1].parse().expect("frame_index"),
            actor_ordinal: fields[2].parse().expect("actor_ordinal"),
            actor_context_object_id: fields[3].parse().expect("actor_context_object_id"),
            payload_end_bit: fields[4].parse().expect("payload_end_bit"),
            control_start_bit: fields[5].parse().expect("control_start_bit"),
            control_end_bit: fields[6].parse().expect("control_end_bit"),
            property_present: match fields[7] {
                "0" => false,
                "1" => true,
                other => panic!("invalid property_present {other}"),
            },
        });
    }
    assert_eq!(rows.len(), 3, "R3.18BP must freeze exactly three BM rows");
    rows
}

fn r318bp_opt_u64(value: Option<u64>) -> String {
    value.map_or_else(|| "-".to_owned(), |value| value.to_string())
}

fn r318bp_opt_u32(value: Option<u32>) -> String {
    value.map_or_else(|| "-".to_owned(), |value| value.to_string())
}

fn r318bp_opt_u8(value: Option<u8>) -> String {
    value.map_or_else(|| "-".to_owned(), |value| value.to_string())
}

#[test]
fn r3_18bp_emit_published_bo_differential_rows() {
    let out_dir = std::path::PathBuf::from(
        std::env::var("R318BP_OUT_DIR").expect("R318BP_OUT_DIR must be set"),
    );
    std::fs::create_dir_all(&out_dir).expect("create R3.18BP output directory");

    let frozen = r318bp_frozen_control_rows();
    let mut seen = std::collections::BTreeSet::new();
    let (mut excluded_au, mut excluded_be, mut bk_rows, mut false_rows, mut true_rows) =
        (0usize, 0usize, 0usize, 0usize, 0usize);
    let mut tsv = String::from(
        "label\tframe_index\tactor_ordinal\tactor_context_object_id\tbk_payload_end_bit\tbk_control_start_bit\tbk_control_end_bit\tbk_property_present\tbk_stop_bit\tbo_stop_bit\theader_present\theader_actor_object_index\theader_property_present_start_bit\theader_property_present_end_bit\tstream_id_start_bit\tstream_id\tstream_id_bound\tprop_id_bits\tproperty_object_index\tattribute_tag\tpayload_start_bit\theader_stop_bit\tversion_major\tversion_minor\tnet_version\tis_rl_223\n",
    );

    for (index, (path, first_start, actor_object, _)) in au_cases().into_iter().enumerate() {
        let (network, plan) = frozen_network_and_plan(path, &format!("r318bp_{index}"));
        let (prior, control, an) = aq_from_frozen(&network, &plan, first_start, actor_object);
        let aq = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_v1(
            &network, &prior, &control, &plan, k3_context(), &an,
        ).unwrap_or_else(|error| panic!("AQ prerequisite row {index} {path}: {error}"));
        let au = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_following_header_v1(
            &network, &prior, &control, &plan, k3_context(), &an, &aq,
        ).unwrap_or_else(|error| panic!("AU prerequisite row {index} {path}: {error}"));
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
        bk_rows += 1;

        let label = r318bp_normalize_label(path);
        let authority = frozen
            .iter()
            .find(|row| row.label == label)
            .unwrap_or_else(|| panic!("R3.18BP witness reselection: {label}"));
        assert!(seen.insert(label.to_owned()), "duplicate R3.18BP witness {label}");
        assert_eq!(authority.frame_index, 0, "{label}");
        assert_eq!(authority.actor_context_object_id, actor_object, "{label}");
        assert_eq!(authority.payload_end_bit, bi.stop_bit, "{label}");
        assert_eq!(authority.control_start_bit, bk.property_present_start_bit, "{label}");
        assert_eq!(authority.control_end_bit, bk.property_present_end_bit, "{label}");
        assert_eq!(authority.property_present, bk.property_present, "{label}");
        assert_eq!(bk.stop_bit, authority.control_end_bit, "{label}");

        let got: ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderV1 = decode_bo(
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
        ).unwrap_or_else(|error| panic!("published BO row {index} {label}: {error}"));
        assert_eq!(got.control, bk, "{label}");
        assert_eq!(got.context, k3_context(), "{label}");

        let repeated = decode_bo(
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
        .expect("repeat published BO");
        assert_eq!(repeated, got, "repeatability {label}");

        let mut poisoned = network.clone();
        let poison_bit = usize::try_from(got.stop_bit).expect("BO stop fits usize");
        assert!(poison_bit / 8 < poisoned.len(), "{label}");
        let old = raw_lsb(&poisoned, got.stop_bit);
        set_bit(&mut poisoned, poison_bit, !old);
        let after_poison = decode_bo(
            &poisoned,
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
        .expect("published BO must ignore bits at/after returned stop");
        assert_eq!(after_poison, got, "post-stop poison {label}");

        let context = got.context;
        if !bk.property_present {
            false_rows += 1;
            assert!(got.following_header.is_none(), "{label}");
            assert_eq!(got.stop_bit, bk.stop_bit, "{label}");
            tsv.push_str(&format!(
                "{}\t{}\t{}\t{}\t{}\t{}\t{}\t0\t{}\t{}\t0\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t{}\t{}\t{}\t{}\n",
                label,
                authority.frame_index,
                authority.actor_ordinal,
                authority.actor_context_object_id,
                authority.payload_end_bit,
                authority.control_start_bit,
                authority.control_end_bit,
                bk.stop_bit,
                got.stop_bit,
                context.version_major,
                context.version_minor,
                context.net_version,
                u8::from(context.is_rl_223),
            ));
            continue;
        }

        true_rows += 1;
        let header = got
            .following_header
            .as_ref()
            .expect("published BO true row must expose one header");
        let tag = header
            .resolved_attribute_tag
            .map(|tag| format!("{tag:?}"))
            .unwrap_or_else(|| "-".to_owned());
        tsv.push_str(&format!(
            "{}\t{}\t{}\t{}\t{}\t{}\t{}\t1\t{}\t{}\t1\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n",
            label,
            authority.frame_index,
            authority.actor_ordinal,
            authority.actor_context_object_id,
            authority.payload_end_bit,
            authority.control_start_bit,
            authority.control_end_bit,
            bk.stop_bit,
            got.stop_bit,
            header.actor_object_index,
            header.property_present_start_bit,
            header.property_present_end_bit,
            r318bp_opt_u64(header.stream_id_start_bit),
            r318bp_opt_u32(header.stream_id),
            r318bp_opt_u32(header.stream_id_bound),
            r318bp_opt_u8(header.prop_id_bits),
            r318bp_opt_u32(header.resolved_property_object_index),
            tag,
            r318bp_opt_u64(header.payload_start_bit),
            header.stop_bit,
            context.version_major,
            context.version_minor,
            context.net_version,
            u8::from(context.is_rl_223),
        ));
    }

    assert_eq!(excluded_au, 7, "AU exclusion drift");
    assert_eq!(excluded_be, 37, "BE exclusion drift");
    assert_eq!(bk_rows, 3, "BK witness-count drift");
    assert_eq!(false_rows, 1, "false terminator drift");
    assert_eq!(true_rows, 2, "true header drift");
    assert_eq!(seen.len(), 3, "witness reselection or omission");
    for authority in &frozen {
        assert!(seen.contains(&authority.label), "missing frozen witness {}", authority.label);
    }

    std::fs::write(out_dir.join("r3_18bp_published_bo.tsv"), tsv)
        .expect("write R3.18BP published BO rows");
    std::fs::write(
        out_dir.join("r3_18bp_probe_summary.txt"),
        format!(
            "R3_18BP_PROBE=PASS\nR3_18BP_ROWS=3/3\nR3_18BP_FALSE=1\nR3_18BP_TRUE=2\nR3_18BP_AU_EXCLUDED=7\nR3_18BP_BE_EXCLUDED=37\nR3_18BP_REPEATABILITY=PASS 3/3\nR3_18BP_POST_STOP_POISON=PASS 3/3\nR3_18BP_WITNESS_RESELECTION=0\n"
        ),
    )
    .expect("write R3.18BP probe summary");
}
