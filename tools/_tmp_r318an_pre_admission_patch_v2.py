from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LIB = ROOT / "crates/mimir-replay/src/lib.rs"
TEST = ROOT / "crates/mimir-replay/tests/r3_18an_post_ak_payload.rs"

lib_text = LIB.read_text(encoding="utf-8")
old_match = """        || !matches!(
            following_payload.value,
            ReplayNetworkPrimitiveScalarValueV1::Int(_)
        )
"""
new_match = """        || !matches!(
            &following_payload.value,
            ReplayNetworkPrimitiveScalarValueV1::Int(_)
        )
"""
if lib_text.count(old_match) != 1:
    raise SystemExit(f"expected one primitive-value ownership match, got {lib_text.count(old_match)}")
LIB.write_text(lib_text.replace(old_match, new_match, 1), encoding="utf-8", newline="\n")

test_text = TEST.read_text(encoding="utf-8")
if "r3_18an_all_47_frozen_am_rows_are_exact_and_stop_before_next_control" in test_text:
    raise SystemExit("47-row R3.18AN regression already present")

append = r'''

fn frozen_network_and_plan(path: &str, label: &str) -> (Vec<u8>, ReplayNetworkLookupPlanV1) {
    let path = PathBuf::from(env!("CARGO_MANIFEST_DIR")).join(path);
    let replay_bytes = std::fs::read(&path)
        .unwrap_or_else(|error| panic!("read frozen R3.18AM replay {}: {error}", path.display()));
    let input = ReplayInput::Memory {
        label: label.to_owned(),
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

fn frozen_ad_prior(
    network: &[u8],
    plan: &ReplayNetworkLookupPlanV1,
    first_start: u64,
    actor_object: u32,
) -> ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadV1 {
    let first = decode_replay_network_existing_actor_single_primitive_property_v1(
        network,
        first_start,
        actor_object,
        plan,
    )
    .expect("R3.18B frozen first property");
    let second = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_v1(
        network,
        &first,
        plan,
        k2_context(),
    )
    .expect("R3.18J frozen second payload");
    let following = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_v1(
        network,
        &second,
        plan,
        k3_context(),
    )
    .expect("R3.18T frozen following payload");
    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_v1(
        network,
        &following,
        plan,
        k3_context(),
    )
    .expect("R3.18AD frozen payload")
}

#[test]
fn r3_18an_all_47_frozen_am_rows_are_exact_and_stop_before_next_control() {
    let cases: [(&str, u64, u32, u64, u64, i32); 47] = [
        ("../../external_fixtures/sample_001.replay", 10227, 98, 10360, 10392, 3),
        ("../../external_fixtures/sample_002.replay", 11019, 106, 11152, 11184, 3),
        ("../../external_fixtures/sample_003.replay", 7603, 103, 7736, 7768, 2),
        ("../../test_corpus/largest_100/003_d137eaa3-af41-4803-8fe7-1eb87d304e2c.replay", 2848, 112, 2980, 3012, 1),
        ("../../test_corpus/largest_100/010_27f8a623-4388-41da-9473-5f59df5fa93b.replay", 3006, 112, 3138, 3170, 1),
        ("../../test_corpus/largest_100/011_39aa142a-baf8-4af3-8b67-6fbca93f23a6.replay", 3164, 114, 3328, 3360, 300),
        ("../../test_corpus/largest_100/012_0c83fe49-b7f6-427a-ae97-b1a4f53d6117.replay", 3042, 112, 3174, 3206, 1),
        ("../../test_corpus/largest_100/016_b473f51b-abdd-4896-872f-26fb7d8bd939.replay", 3006, 112, 3138, 3170, 1),
        ("../../test_corpus/largest_100/019_bd1a83e2-5ac0-4a79-beba-df8547515782.replay", 3006, 111, 3170, 3202, 300),
        ("../../test_corpus/largest_100/023_d9186df1-af02-4ab1-ba1b-b2c3b6fb1a67.replay", 3006, 112, 3138, 3170, 1),
        ("../../test_corpus/largest_100/027_abfd6c12-e5e0-46a3-aaee-4d086a4d6ee5.replay", 3006, 112, 3138, 3170, 1),
        ("../../test_corpus/largest_100/033_e8ab232b-24e4-401c-b5ac-db2d5587cfcf.replay", 3168, 127, 3300, 3332, 1),
        ("../../test_corpus/largest_100/035_6b90776b-1784-4d30-a8ff-d37b66ae4a38.replay", 3006, 112, 3138, 3170, 1),
        ("../../test_corpus/largest_100/036_88b815c9-bc3d-498a-8fa3-80638cfa8709.replay", 3243, 120, 3375, 3407, 1),
        ("../../test_corpus/largest_100/038_c44e3655-bcc9-41fb-9548-808ee70c66e7.replay", 2892, 74, 3024, 3056, 1),
        ("../../test_corpus/largest_100/039_4c5e5ad8-c72f-49b2-890c-d936e172160c.replay", 3006, 111, 3170, 3202, 300),
        ("../../test_corpus/largest_100/040_0a38f81b-862d-4776-9d27-3c221355f839.replay", 3006, 111, 3138, 3170, 1),
        ("../../test_corpus/largest_100/042_be1e76bd-258a-4067-8d06-57481459f946.replay", 3042, 112, 3174, 3206, 1),
        ("../../test_corpus/largest_100/049_6c45a00b-d14b-4eba-86b8-4a3e99faf545.replay", 3164, 111, 3296, 3328, 1),
        ("../../test_corpus/largest_100/050_6e301fcc-239b-4a29-863b-8c2561e56042.replay", 2970, 135, 3102, 3134, 1),
        ("../../test_corpus/largest_100/054_9ed418f3-9eaf-4a18-a591-633db1120790.replay", 3006, 112, 3138, 3170, 1),
        ("../../test_corpus/largest_100/057_4fab5b3d-17de-4a7b-86d7-432ba973c524.replay", 3042, 111, 3174, 3206, 1),
        ("../../test_corpus/largest_100/059_d86eb20b-396c-49bc-80bb-71bec6949f94.replay", 3243, 120, 3375, 3407, 1),
        ("../../test_corpus/largest_100/060_6bc2e5f5-e243-4db0-b6f9-1b8173472c29.replay", 3006, 112, 3138, 3170, 1),
        ("../../test_corpus/largest_100/061_2b7d3c05-ff84-44fd-ae1b-9e745b9a9350.replay", 3164, 135, 3296, 3328, 1),
        ("../../test_corpus/largest_100/065_62d26477-6502-49ba-b48e-1990a4ea3e2b.replay", 3217, 122, 3349, 3381, 1),
        ("../../test_corpus/largest_100/066_0e3f475c-ab4e-45b3-8857-f0f5583da70b.replay", 3032, 65, 3164, 3196, 1),
        ("../../test_corpus/largest_100/068_fdb826bc-63a7-4aba-b6b9-70327ccd9af9.replay", 3042, 112, 3174, 3206, 1),
        ("../../test_corpus/largest_100/069_2ee7342c-a8cd-47cf-bc6e-536150bc2e2f.replay", 3006, 112, 3138, 3170, 1),
        ("../../test_corpus/largest_100/072_60e8a19d-6782-4599-b2c7-13194b1719f6.replay", 2892, 74, 3024, 3056, 1),
        ("../../test_corpus/largest_100/073_e435deab-aaed-4848-bdd0-c49858bce7e4.replay", 3006, 111, 3170, 3202, 300),
        ("../../test_corpus/largest_100/074_a6e89dc6-09ca-4c1a-b2da-c7383009ce8c.replay", 3489, 149, 3621, 3653, 1),
        ("../../test_corpus/largest_100/075_2533649e-b2d9-4438-9261-0e6eea032525.replay", 3006, 112, 3138, 3170, 1),
        ("../../test_corpus/largest_100/078_e4841be3-229e-410c-8a67-b88e76f46ade.replay", 3006, 111, 3170, 3202, 300),
        ("../../test_corpus/largest_100/079_1f838b01-66b5-4963-b62e-64f3d7dbd545.replay", 2838, 117, 3087, 3119, 415),
        ("../../test_corpus/largest_100/082_ca9dcc03-e630-464a-a76d-8edb8fc78d0f.replay", 3006, 111, 3138, 3170, 1),
        ("../../test_corpus/largest_100/083_0d530715-6b10-421c-8af2-9b5b1feff4f6.replay", 2848, 111, 3012, 3044, 300),
        ("../../test_corpus/largest_100/085_24c94755-bf07-44ff-a745-17ec46fdf0dd.replay", 3060, 118, 3192, 3224, 1),
        ("../../test_corpus/largest_100/086_12e3b253-fa87-45b0-973b-307aafc0a41f.replay", 3006, 111, 3170, 3202, 300),
        ("../../test_corpus/largest_100/089_927d8bb2-1999-4a4d-aaf3-482dae6348c4.replay", 3006, 112, 3138, 3170, 1),
        ("../../test_corpus/largest_100/093_893c8162-4390-4fc3-bd87-5eba4b2b5065.replay", 3200, 112, 3332, 3364, 1),
        ("../../test_corpus/largest_100/094_5ca1d62e-ede6-4829-95cd-ac1f3b462750.replay", 3006, 112, 3138, 3170, 1),
        ("../../test_corpus/largest_100/095_544eb235-f537-4e93-955e-77c4a1ed3380.replay", 2848, 112, 2980, 3012, 1),
        ("../../test_corpus/largest_100/096_898e1ab6-2fe4-4446-8086-a5963a3b7b0c.replay", 3006, 112, 3138, 3170, 1),
        ("../../test_corpus/largest_100/097_ab8382c3-d2f8-4481-a0c0-5ea2d5b5653e.replay", 3006, 112, 3138, 3170, 1),
        ("../../test_corpus/largest_100/098_be5b3375-17ec-42f2-b58b-e2fca2e61ce4.replay", 3218, 139, 3350, 3382, 1),
        ("../../test_corpus/largest_100/100_1f669eef-b24a-45d8-9d67-bb5abf46b553.replay", 3152, 136, 3284, 3316, 1),
    ];

    for (index, (path, first_start, actor_object, expected_start, expected_end, expected_value))
        in cases.into_iter().enumerate()
    {
        let (network, plan) = frozen_network_and_plan(path, &format!("r318an_frozen_{index}"));
        let prior = frozen_ad_prior(&network, &plan, first_start, actor_object);
        let control = ag_control(&network, &prior);
        let got = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_v1(
            &network,
            &prior,
            &control,
            &plan,
            k3_context(),
        )
        .unwrap_or_else(|error| panic!("frozen row {index} {path}: {error}"));

        assert_eq!(got.header_composition.stop_bit, expected_start, "{path}");
        assert_eq!(got.following_payload.payload_start_bit, expected_start, "{path}");
        assert_eq!(got.following_payload.payload_end_bit, expected_end, "{path}");
        assert_eq!(got.following_payload.payload_width, 32, "{path}");
        assert_eq!(got.stop_bit, expected_end, "{path}");
        assert_eq!(
            got.following_payload.value,
            ReplayNetworkPrimitiveScalarValueV1::Int(expected_value),
            "{path}"
        );

        let direct = decode_replay_network_primitive_scalar_v1(
            &network,
            expected_start,
            ReplayNetworkAttributeTagV1::Int,
        )
        .expect("direct frozen Int primitive");
        assert_eq!(got.following_payload, direct, "{path}");

        let repeated = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_v1(
            &network,
            &prior,
            &control,
            &plan,
            k3_context(),
        )
        .expect("repeat frozen R3.18AN");
        assert_eq!(repeated, got, "{path}");

        let trunc_bytes = usize::try_from(expected_end.saturating_sub(1) / 8).unwrap();
        assert!(trunc_bytes < network.len(), "{path}");
        assert!(
            decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_v1(
                &network[..trunc_bytes],
                &prior,
                &control,
                &plan,
                k3_context(),
            )
            .is_err(),
            "truncation unexpectedly admitted {path}"
        );

        let mut poisoned = network.clone();
        let stop = usize::try_from(expected_end).unwrap();
        assert!(stop / 8 < poisoned.len(), "{path}");
        let original = ((poisoned[stop / 8] >> (stop % 8)) & 1) != 0;
        set_bit(&mut poisoned, stop, !original);
        let after_poison = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_v1(
            &poisoned,
            &prior,
            &control,
            &plan,
            k3_context(),
        )
        .expect("post-payload poison must not affect R3.18AN");
        assert_eq!(after_poison, got, "post-stop poison changed {path}");
    }
}
'''

TEST.write_text(test_text.rstrip() + append + "\n", encoding="utf-8", newline="\n")
print("R3_18AN_PRE_ADMISSION_V2_PATCH=PASS rows=47 ownership_fix=1")
