use mimir_replay::{
    ReplayNetworkAttributeTagV1, ReplayNetworkK2DecodeContextV1, ReplayNetworkK2ValueV1,
    ReplayNetworkTextEncodingV1, ReplayNetworkTextV1, ReplayNetworkUniqueIdRemoteV1,
    decode_replay_network_k2_v1,
};

fn push_bits(bytes: &mut Vec<u8>, bit: &mut usize, value: u64, width: usize) {
    for offset in 0..width {
        let position = *bit + offset;
        let byte_index = position / 8;
        let bit_index = position % 8;
        while bytes.len() <= byte_index {
            bytes.push(0);
        }
        if ((value >> offset) & 1) != 0 {
            bytes[byte_index] |= 1 << bit_index;
        }
    }
    *bit += width;
}

fn push_u8(bytes: &mut Vec<u8>, bit: &mut usize, value: u8) {
    push_bits(bytes, bit, u64::from(value), 8);
}

fn push_u16(bytes: &mut Vec<u8>, bit: &mut usize, value: u16) {
    push_bits(bytes, bit, u64::from(value), 16);
}

fn push_i32(bytes: &mut Vec<u8>, bit: &mut usize, value: i32) {
    push_bits(bytes, bit, u64::from(value as u32), 32);
}

fn push_u64(bytes: &mut Vec<u8>, bit: &mut usize, value: u64) {
    push_bits(bytes, bit, value, 64);
}

fn push_windows_text(bytes: &mut Vec<u8>, bit: &mut usize, content: &[u8], terminator: u8) {
    push_i32(bytes, bit, i32::try_from(content.len() + 1).unwrap());
    for value in content {
        push_u8(bytes, bit, *value);
    }
    push_u8(bytes, bit, terminator);
}

fn push_utf16_text(bytes: &mut Vec<u8>, bit: &mut usize, content: &[u16], terminator: u16) {
    let declared = -i32::try_from(content.len() + 1).unwrap();
    push_i32(bytes, bit, declared);
    for value in content {
        push_u16(bytes, bit, *value);
    }
    push_u16(bytes, bit, terminator);
}

fn new_bits(start: usize) -> (Vec<u8>, usize) {
    (vec![0; start.div_ceil(8)], start)
}

fn ctx(net_version: i32, is_rl_223: bool) -> ReplayNetworkK2DecodeContextV1 {
    ReplayNetworkK2DecodeContextV1 {
        net_version,
        is_rl_223,
    }
}

fn assert_error_contains(error: mimir_core::MimirError, needle: &str) {
    let text = error.to_string();
    assert!(text.contains(needle), "expected {needle:?} in {text:?}");
}

#[test]
fn active_actor_decodes_exact_33_bits_at_unaligned_starts() {
    let cases = [
        (1usize, false, 0i32),
        (3usize, true, 42i32),
        (5usize, false, -1i32),
        (7usize, true, -123_456i32),
    ];
    for (start, active, actor) in cases {
        let (mut bytes, mut bit) = new_bits(start);
        push_bits(&mut bytes, &mut bit, u64::from(active), 1);
        push_i32(&mut bytes, &mut bit, actor);
        let decoded = decode_replay_network_k2_v1(
            &bytes,
            start as u64,
            ReplayNetworkAttributeTagV1::ActiveActor,
            ctx(10, true),
        )
        .unwrap();
        assert_eq!(decoded.payload_end_bit, bit as u64);
        assert_eq!(decoded.payload_width, 33);
        assert_eq!(
            decoded.value,
            ReplayNetworkK2ValueV1::ActiveActor { active, actor }
        );
    }

    let error = decode_replay_network_k2_v1(
        &[0; 4],
        0,
        ReplayNetworkAttributeTagV1::ActiveActor,
        ctx(10, false),
    )
    .unwrap_err();
    assert_error_contains(error, "insufficient-bits");
}

#[test]
fn string_decodes_empty_windows1252_and_utf16_with_exact_shape_identity() {
    let start = 3usize;
    let (mut empty_bytes, mut empty_bit) = new_bits(start);
    push_i32(&mut empty_bytes, &mut empty_bit, 0);
    let empty = decode_replay_network_k2_v1(
        &empty_bytes,
        start as u64,
        ReplayNetworkAttributeTagV1::String,
        ctx(10, false),
    )
    .unwrap();
    assert_eq!(empty.payload_end_bit, empty_bit as u64);
    assert_eq!(
        empty.value,
        ReplayNetworkK2ValueV1::String(ReplayNetworkTextV1 {
            value: String::new(),
            declared_length: 0,
            encoding: ReplayNetworkTextEncodingV1::Empty,
        })
    );

    let (mut windows_bytes, mut windows_bit) = new_bits(5);
    push_windows_text(
        &mut windows_bytes,
        &mut windows_bit,
        &[b'A', 0x80, b'Z'],
        0x7f,
    );
    let windows = decode_replay_network_k2_v1(
        &windows_bytes,
        5,
        ReplayNetworkAttributeTagV1::String,
        ctx(10, true),
    )
    .unwrap();
    assert_eq!(windows.payload_end_bit, windows_bit as u64);
    assert_eq!(
        windows.value,
        ReplayNetworkK2ValueV1::String(ReplayNetworkTextV1 {
            value: "A€Z".to_owned(),
            declared_length: 4,
            encoding: ReplayNetworkTextEncodingV1::Windows1252,
        })
    );

    let (mut utf16_bytes, mut utf16_bit) = new_bits(7);
    push_utf16_text(
        &mut utf16_bytes,
        &mut utf16_bit,
        &[0x0041, 0xd800, 0x0042],
        0x1234,
    );
    let utf16 = decode_replay_network_k2_v1(
        &utf16_bytes,
        7,
        ReplayNetworkAttributeTagV1::String,
        ctx(10, false),
    )
    .unwrap();
    assert_eq!(utf16.payload_end_bit, utf16_bit as u64);
    assert_eq!(
        utf16.value,
        ReplayNetworkK2ValueV1::String(ReplayNetworkTextV1 {
            value: "A�B".to_owned(),
            declared_length: -4,
            encoding: ReplayNetworkTextEncodingV1::Utf16Le,
        })
    );
}

#[test]
fn string_rejects_invalid_length_and_truncation() {
    let (mut min_bytes, mut min_bit) = new_bits(0);
    push_i32(&mut min_bytes, &mut min_bit, i32::MIN);
    let error = decode_replay_network_k2_v1(
        &min_bytes,
        0,
        ReplayNetworkAttributeTagV1::String,
        ctx(10, false),
    )
    .unwrap_err();
    assert_error_contains(error, "invalid-text-length");

    let error = decode_replay_network_k2_v1(
        &[0; 3],
        0,
        ReplayNetworkAttributeTagV1::String,
        ctx(10, false),
    )
    .unwrap_err();
    assert_error_contains(error, "insufficient-bits");

    let mut truncated = vec![0; 7];
    let mut bit = 0usize;
    push_i32(&mut truncated, &mut bit, 4);
    let error = decode_replay_network_k2_v1(
        &truncated,
        0,
        ReplayNetworkAttributeTagV1::String,
        ctx(10, false),
    )
    .unwrap_err();
    assert_error_contains(error, "insufficient-bits");
}

#[test]
fn qword_string_obeys_rl223_gate() {
    let (mut legacy_bytes, mut legacy_bit) = new_bits(3);
    push_u64(&mut legacy_bytes, &mut legacy_bit, 0x0123_4567_89ab_cdef);
    let legacy = decode_replay_network_k2_v1(
        &legacy_bytes,
        3,
        ReplayNetworkAttributeTagV1::QWordString,
        ctx(10, false),
    )
    .unwrap();
    assert_eq!(legacy.payload_end_bit, legacy_bit as u64);
    assert_eq!(
        legacy.value,
        ReplayNetworkK2ValueV1::QWordStringQWord(0x0123_4567_89ab_cdef)
    );

    let (mut text_bytes, mut text_bit) = new_bits(1);
    push_windows_text(&mut text_bytes, &mut text_bit, b"rl223", 0xff);
    let text = decode_replay_network_k2_v1(
        &text_bytes,
        1,
        ReplayNetworkAttributeTagV1::QWordString,
        ctx(10, true),
    )
    .unwrap();
    assert_eq!(text.payload_end_bit, text_bit as u64);
    assert!(matches!(
        text.value,
        ReplayNetworkK2ValueV1::QWordStringText(ReplayNetworkTextV1 {
            encoding: ReplayNetworkTextEncodingV1::Windows1252,
            declared_length: 6,
            ..
        })
    ));

    let (mut empty_bytes, mut empty_bit) = new_bits(0);
    push_i32(&mut empty_bytes, &mut empty_bit, 0);
    let error = decode_replay_network_k2_v1(
        &empty_bytes,
        0,
        ReplayNetworkAttributeTagV1::QWordString,
        ctx(10, true),
    )
    .unwrap_err();
    assert_error_contains(error, "unadmitted-k2-shape");

    let (mut utf16_bytes, mut utf16_bit) = new_bits(0);
    push_utf16_text(&mut utf16_bytes, &mut utf16_bit, &[0x41], 0);
    let error = decode_replay_network_k2_v1(
        &utf16_bytes,
        0,
        ReplayNetworkAttributeTagV1::QWordString,
        ctx(10, true),
    )
    .unwrap_err();
    assert_error_contains(error, "unadmitted-k2-shape");
}

fn push_epic(bytes: &mut Vec<u8>, bit: &mut usize, local_id: u8) {
    push_u8(bytes, bit, 11);
    push_windows_text(bytes, bit, &[b'E'; 32], 0x55);
    push_u8(bytes, bit, local_id);
}

#[test]
fn unique_id_decodes_all_admitted_systems() {
    let (mut steam_bytes, mut steam_bit) = new_bits(1);
    push_u8(&mut steam_bytes, &mut steam_bit, 1);
    push_u64(&mut steam_bytes, &mut steam_bit, 0x1111_2222_3333_4444);
    push_u8(&mut steam_bytes, &mut steam_bit, 7);
    for rl223 in [false, true] {
        let steam = decode_replay_network_k2_v1(
            &steam_bytes,
            1,
            ReplayNetworkAttributeTagV1::UniqueId,
            ctx(10, rl223),
        )
        .unwrap();
        assert_eq!(steam.payload_end_bit, steam_bit as u64);
        assert!(matches!(
            steam.value,
            ReplayNetworkK2ValueV1::UniqueId(mimir_replay::ReplayNetworkUniqueIdV1 {
                system_id: 1,
                remote_id: ReplayNetworkUniqueIdRemoteV1::Steam {
                    online_id: 0x1111_2222_3333_4444
                },
                local_id: 7,
            })
        ));
    }

    let (mut ps_bytes, mut ps_bit) = new_bits(3);
    push_u8(&mut ps_bytes, &mut ps_bit, 2);
    let mut name = [0u8; 16];
    name[..6].copy_from_slice(b"Player");
    for value in name {
        push_u8(&mut ps_bytes, &mut ps_bit, value);
    }
    for _ in 0..16 {
        push_u8(&mut ps_bytes, &mut ps_bit, 0xa5);
    }
    push_u64(&mut ps_bytes, &mut ps_bit, 0x1234);
    push_u8(&mut ps_bytes, &mut ps_bit, 9);
    let ps = decode_replay_network_k2_v1(
        &ps_bytes,
        3,
        ReplayNetworkAttributeTagV1::UniqueId,
        ctx(10, true),
    )
    .unwrap();
    assert_eq!(ps.payload_width, 336);
    assert_eq!(ps.payload_end_bit, ps_bit as u64);
    assert!(matches!(
        ps.value,
        ReplayNetworkK2ValueV1::UniqueId(mimir_replay::ReplayNetworkUniqueIdV1 {
            system_id: 2,
            remote_id: ReplayNetworkUniqueIdRemoteV1::PlayStation { ref name, ref unknown, online_id: 0x1234 },
            local_id: 9,
        }) if name == "Player" && unknown == &vec![0xa5; 16]
    ));

    let (mut psy_bytes, mut psy_bit) = new_bits(5);
    push_u8(&mut psy_bytes, &mut psy_bit, 7);
    push_u64(&mut psy_bytes, &mut psy_bit, 0xaabb_ccdd_eeff_0011);
    push_u8(&mut psy_bytes, &mut psy_bit, 3);
    let psy = decode_replay_network_k2_v1(
        &psy_bytes,
        5,
        ReplayNetworkAttributeTagV1::UniqueId,
        ctx(10, true),
    )
    .unwrap();
    assert_eq!(psy.payload_width, 80);
    assert_eq!(psy.payload_end_bit, psy_bit as u64);
    assert!(matches!(
        psy.value,
        ReplayNetworkK2ValueV1::UniqueId(mimir_replay::ReplayNetworkUniqueIdV1 {
            system_id: 7,
            remote_id: ReplayNetworkUniqueIdRemoteV1::PsyNet {
                online_id: 0xaabb_ccdd_eeff_0011
            },
            local_id: 3,
        })
    ));

    let (mut epic_bytes, mut epic_bit) = new_bits(7);
    push_epic(&mut epic_bytes, &mut epic_bit, 4);
    for rl223 in [false, true] {
        let epic = decode_replay_network_k2_v1(
            &epic_bytes,
            7,
            ReplayNetworkAttributeTagV1::UniqueId,
            ctx(10, rl223),
        )
        .unwrap();
        assert_eq!(epic.payload_width, 312);
        assert_eq!(epic.payload_end_bit, epic_bit as u64);
        assert!(matches!(
            epic.value,
            ReplayNetworkK2ValueV1::UniqueId(mimir_replay::ReplayNetworkUniqueIdV1 {
                system_id: 11,
                remote_id: ReplayNetworkUniqueIdRemoteV1::Epic {
                    account_id: ReplayNetworkTextV1 {
                        declared_length: 33,
                        encoding: ReplayNetworkTextEncodingV1::Windows1252,
                        ..
                    }
                },
                local_id: 4,
            })
        ));
    }
}

#[test]
fn unique_id_rejects_unadmitted_contexts_systems_and_epic_shape() {
    let error = decode_replay_network_k2_v1(
        &[1; 16],
        0,
        ReplayNetworkAttributeTagV1::UniqueId,
        ctx(9, true),
    )
    .unwrap_err();
    assert_error_contains(error, "unadmitted-context");

    for system_id in [0u8, 4, 5, 6, 99] {
        let (mut bytes, mut bit) = new_bits(0);
        push_u8(&mut bytes, &mut bit, system_id);
        let error = decode_replay_network_k2_v1(
            &bytes,
            0,
            ReplayNetworkAttributeTagV1::UniqueId,
            ctx(10, true),
        )
        .unwrap_err();
        assert_error_contains(error, "unadmitted-k2-shape");
    }

    for system_id in [2u8, 7] {
        let (mut bytes, mut bit) = new_bits(0);
        push_u8(&mut bytes, &mut bit, system_id);
        let error = decode_replay_network_k2_v1(
            &bytes,
            0,
            ReplayNetworkAttributeTagV1::UniqueId,
            ctx(10, false),
        )
        .unwrap_err();
        assert_error_contains(error, "unadmitted-context");
    }

    let (mut epic_bytes, mut epic_bit) = new_bits(0);
    push_u8(&mut epic_bytes, &mut epic_bit, 11);
    push_windows_text(&mut epic_bytes, &mut epic_bit, &[b'X'; 31], 0);
    let error = decode_replay_network_k2_v1(
        &epic_bytes,
        0,
        ReplayNetworkAttributeTagV1::UniqueId,
        ctx(10, true),
    )
    .unwrap_err();
    assert_error_contains(error, "unadmitted-k2-shape");
}

#[test]
fn party_leader_admits_only_rl223_epic_declared_33() {
    let (mut epic_bytes, mut epic_bit) = new_bits(3);
    push_epic(&mut epic_bytes, &mut epic_bit, 8);
    let decoded = decode_replay_network_k2_v1(
        &epic_bytes,
        3,
        ReplayNetworkAttributeTagV1::PartyLeader,
        ctx(10, true),
    )
    .unwrap();
    assert_eq!(decoded.payload_width, 312);
    assert_eq!(decoded.payload_end_bit, epic_bit as u64);
    assert!(matches!(
        decoded.value,
        ReplayNetworkK2ValueV1::PartyLeader(mimir_replay::ReplayNetworkUniqueIdV1 {
            system_id: 11,
            remote_id: ReplayNetworkUniqueIdRemoteV1::Epic { .. },
            local_id: 8,
        })
    ));

    let error = decode_replay_network_k2_v1(
        &[0],
        0,
        ReplayNetworkAttributeTagV1::PartyLeader,
        ctx(10, true),
    )
    .unwrap_err();
    assert_error_contains(error, "unadmitted-k2-shape");

    let (mut steam_bytes, mut steam_bit) = new_bits(0);
    push_u8(&mut steam_bytes, &mut steam_bit, 1);
    push_u64(&mut steam_bytes, &mut steam_bit, 7);
    push_u8(&mut steam_bytes, &mut steam_bit, 1);
    let error = decode_replay_network_k2_v1(
        &steam_bytes,
        0,
        ReplayNetworkAttributeTagV1::PartyLeader,
        ctx(10, true),
    )
    .unwrap_err();
    assert_error_contains(error, "unadmitted-k2-shape");

    for context in [ctx(10, false), ctx(9, true)] {
        let error = decode_replay_network_k2_v1(
            &epic_bytes,
            3,
            ReplayNetworkAttributeTagV1::PartyLeader,
            context,
        )
        .unwrap_err();
        assert_error_contains(error, "unadmitted-context");
    }
}

#[test]
fn k2_decoder_rejects_non_k2_tag_and_invalid_start() {
    let error = decode_replay_network_k2_v1(
        &[0xff; 8],
        0,
        ReplayNetworkAttributeTagV1::Boolean,
        ctx(10, true),
    )
    .unwrap_err();
    assert_error_contains(error, "unsupported-k2-tag");

    let error = decode_replay_network_k2_v1(
        &[0xff],
        9,
        ReplayNetworkAttributeTagV1::ActiveActor,
        ctx(10, true),
    )
    .unwrap_err();
    assert_error_contains(error, "invalid-start");
}
