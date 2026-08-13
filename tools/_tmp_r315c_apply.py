from pathlib import Path

SOURCE = Path("crates/mimir-replay/src/lib.rs")
EXPECTED_BLOB = "67752868807c0b7169e46f22762c7a0ea9efce40"


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected exactly one match, found {count}")
    return text.replace(old, new, 1)


text = SOURCE.read_text(encoding="utf-8")
if "ReplayNetworkFirstNewActorEnvelopeV1" in text:
    raise SystemExit("R3.15C surface already exists; refusing to patch twice")

public_marker = "/// Conservative network attribute wire-tag registry admitted from the supported replay lane.\n"
public_insert = r'''/// Signed integer vector decoded from one admitted NewActor spawn trajectory.
#[derive(Debug, Clone, Copy, Serialize, Deserialize, PartialEq, Eq)]
pub struct ReplayNetworkVector3iV1 {
    pub x: i32,
    pub y: i32,
    pub z: i32,
}

/// Optional yaw/pitch/roll components decoded from one admitted NewActor spawn trajectory.
#[derive(Debug, Clone, Copy, Serialize, Deserialize, PartialEq, Eq)]
pub struct ReplayNetworkRotationV1 {
    pub yaw: Option<i8>,
    pub pitch: Option<i8>,
    pub roll: Option<i8>,
}

/// First admitted NewActor payload, ending exactly at its spawn trajectory endpoint.
#[derive(Debug, Clone, Copy, Serialize, Deserialize, PartialEq, Eq)]
pub struct ReplayNetworkNewActorV1 {
    pub name_id: i32,
    pub opaque_post_name_bit: bool,
    pub object_id: i32,
    pub spawn_kind: ReplayNetworkSpawnTrajectoryV1,
    pub location: Option<ReplayNetworkVector3iV1>,
    pub rotation: Option<ReplayNetworkRotationV1>,
    pub stop_bit: u64,
}

/// Additive first-actor result that extends only a `new == true` branch through spawn trajectory.
///
/// `envelope` preserves the independently admitted R3.14D result. When the first actor is absent,
/// dead, or not new, `new_actor` is `None` and no bits after `envelope.stop_bit` are consumed.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub struct ReplayNetworkFirstNewActorEnvelopeV1 {
    pub envelope: ReplayNetworkFirstActorEnvelopeV1,
    pub new_actor: Option<ReplayNetworkNewActorV1>,
}

pub trait ReplayNetworkFirstNewActorEnvelopeReader {
    fn read_network_first_new_actor_envelope(
        &self,
        input: &ReplayInput,
    ) -> Result<ReplayNetworkFirstNewActorEnvelopeV1>;
}

#[derive(Debug, Default, Clone, Copy)]
pub struct MinimalReplayNetworkFirstNewActorEnvelopeReader;

impl ReplayNetworkFirstNewActorEnvelopeReader for MinimalReplayNetworkFirstNewActorEnvelopeReader {
    fn read_network_first_new_actor_envelope(
        &self,
        input: &ReplayInput,
    ) -> Result<ReplayNetworkFirstNewActorEnvelopeV1> {
        match input {
            ReplayInput::Memory { label, bytes } => {
                parse_replay_network_first_new_actor_envelope_from_memory(label, bytes)
            }
            ReplayInput::File(path) => Err(network_first_new_actor_error(
                "unsupported-input",
                format!(
                    "ReplayInput::File is outside the first NewActor envelope reader: {}",
                    path.display()
                ),
            )),
        }
    }
}

'''
text = replace_once(text, public_marker, public_insert + public_marker, "public R3.15C insertion")

function_marker = "fn network_first_actor_envelope_error(category: &str, detail: impl Into<String>) -> MimirError {\n"
function_insert = r'''fn parse_replay_network_first_new_actor_envelope_from_memory(
    label: &str,
    bytes: &[u8],
) -> Result<ReplayNetworkFirstNewActorEnvelopeV1> {
    // Preserve the exact admitted timing/header/content lane and first-envelope decoder.
    let timing = parse_replay_network_timing_preamble_from_memory(label, bytes)?;
    let network_start = usize::try_from(timing.content.network_start).map_err(|_| {
        network_first_new_actor_error("malformed", "network_start cannot fit usize")
    })?;
    let network_size = usize::try_from(timing.content.network_size).map_err(|_| {
        network_first_new_actor_error("malformed", "network_size cannot fit usize")
    })?;
    let network_end = network_start.checked_add(network_size).ok_or_else(|| {
        network_first_new_actor_error("malformed", "network byte range overflows usize")
    })?;
    if network_end > bytes.len() {
        return Err(network_first_new_actor_error(
            "insufficient",
            "network payload extends beyond replay bytes",
        ));
    }
    let network = &bytes[network_start..network_end];

    let decoded = decode_network_first_actor_header(
        network,
        timing.max_channels,
        timing.channel_bits,
        timing.first_frame_time.to_bits(),
        timing.first_frame_delta.to_bits(),
    )?;
    let envelope_stop_bit = u64::try_from(decoded.stop_bit).map_err(|_| {
        network_first_new_actor_error("mapping", "first-envelope stop bit cannot fit u64")
    })?;
    let envelope = ReplayNetworkFirstActorEnvelopeV1 {
        timing,
        first_frame_time_raw_u32: decoded.time_raw_u32,
        first_frame_delta_raw_u32: decoded.delta_raw_u32,
        actor_present: decoded.actor_present,
        actor_id: decoded.actor_id,
        alive: decoded.alive,
        is_new: decoded.is_new,
        stop_bit: envelope_stop_bit,
    };

    if decoded.is_new != Some(true) {
        return Ok(ReplayNetworkFirstNewActorEnvelopeV1 {
            envelope,
            new_actor: None,
        });
    }

    // Static spawn dispatch is admitted separately from network bits. Build it only for a new
    // branch so absent/dead/not-new branches gain no extra structural precondition.
    let lookup_plan = parse_replay_network_lookup_plan_from_memory(label, bytes)?;
    let new_actor = decode_network_new_actor_after_header_v1(
        network,
        &decoded,
        &lookup_plan.spawn_trajectories,
    )?;

    Ok(ReplayNetworkFirstNewActorEnvelopeV1 {
        envelope,
        new_actor,
    })
}

fn decode_network_new_actor_after_header_v1(
    network: &[u8],
    header: &DecodedNetworkFirstActorHeaderV1,
    spawn_trajectories: &[ReplayNetworkSpawnTrajectoryV1],
) -> Result<Option<ReplayNetworkNewActorV1>> {
    if header.is_new != Some(true) {
        return Ok(None);
    }

    let total_bits = network.len().checked_mul(8).ok_or_else(|| {
        network_first_new_actor_error("malformed", "network bit length overflows usize")
    })?;
    if header.stop_bit > total_bits {
        return Err(network_first_new_actor_error(
            "malformed",
            format!(
                "first-envelope stop bit {} exceeds network bit length {total_bits}",
                header.stop_bit
            ),
        ));
    }

    let mut cursor = NetworkBitCursor::new(network);
    cursor.bit_position = header.stop_bit;
    decode_network_new_actor_v1(&mut cursor, spawn_trajectories).map(Some)
}

fn decode_network_new_actor_v1(
    cursor: &mut NetworkBitCursor<'_>,
    spawn_trajectories: &[ReplayNetworkSpawnTrajectoryV1],
) -> Result<ReplayNetworkNewActorV1> {
    // Commit the caller cursor only when the complete NewActor payload succeeds.
    let mut probe = cursor.clone();

    let name_id = read_network_i32_v1(&mut probe, "name-id")?;
    let opaque_post_name_bit = probe.read_bit().map_err(|error| {
        network_first_new_actor_error(
            "opaque-post-name-bit",
            format!("cannot read opaque post-name bit: {error}"),
        )
    })?;
    let object_id = read_network_i32_v1(&mut probe, "object-id")?;
    if object_id < 0 {
        return Err(network_first_new_actor_error(
            "object-id",
            format!("negative object_id {object_id} is outside the admitted spawn table"),
        ));
    }
    let object_index = usize::try_from(object_id).map_err(|_| {
        network_first_new_actor_error(
            "object-id",
            format!("object_id {object_id} cannot fit usize"),
        )
    })?;
    let spawn_kind = *spawn_trajectories.get(object_index).ok_or_else(|| {
        network_first_new_actor_error(
            "object-id",
            format!(
                "object_id {object_id} is outside spawn table length {}",
                spawn_trajectories.len()
            ),
        )
    })?;

    let (location, rotation) = match spawn_kind {
        ReplayNetworkSpawnTrajectoryV1::None => (None, None),
        ReplayNetworkSpawnTrajectoryV1::Location => {
            (Some(decode_network_vector3i_v1(&mut probe)?), None)
        }
        ReplayNetworkSpawnTrajectoryV1::LocationAndRotation => {
            let location = decode_network_vector3i_v1(&mut probe)?;
            let rotation = decode_network_rotation_v1(&mut probe)?;
            (Some(location), Some(rotation))
        }
    };

    let stop_bit = u64::try_from(probe.position_bits()).map_err(|_| {
        network_first_new_actor_error("mapping", "NewActor stop bit cannot fit u64")
    })?;
    let result = ReplayNetworkNewActorV1 {
        name_id,
        opaque_post_name_bit,
        object_id,
        spawn_kind,
        location,
        rotation,
        stop_bit,
    };
    *cursor = probe;
    Ok(result)
}

fn read_network_i32_v1(cursor: &mut NetworkBitCursor<'_>, field: &str) -> Result<i32> {
    let raw = cursor.read_bits_le(32).map_err(|error| {
        network_first_new_actor_error(field, format!("cannot read signed i32 bits: {error}"))
    })?;
    let raw = u32::try_from(raw).map_err(|_| {
        network_first_new_actor_error(field, format!("32-bit value {raw} cannot fit u32"))
    })?;
    Ok(i32::from_le_bytes(raw.to_le_bytes()))
}

fn decode_network_vector3i_v1(
    cursor: &mut NetworkBitCursor<'_>,
) -> Result<ReplayNetworkVector3iV1> {
    let mut probe = cursor.clone();
    let size_bits = probe.read_bounded_u32(22, 4).map_err(|error| {
        network_first_new_actor_error(
            "spawn-location-size",
            format!("cannot read Vector3i size prefix: {error}"),
        )
    })?;
    let component_width_u32 = size_bits.checked_add(2).ok_or_else(|| {
        network_first_new_actor_error("spawn-location", "Vector3i component width overflows u32")
    })?;
    let component_width = usize::try_from(component_width_u32).map_err(|_| {
        network_first_new_actor_error(
            "spawn-location",
            format!("Vector3i component width {component_width_u32} cannot fit usize"),
        )
    })?;
    let bias_shift = size_bits.checked_add(1).ok_or_else(|| {
        network_first_new_actor_error("spawn-location", "Vector3i bias shift overflows u32")
    })?;
    let bias = 1i64.checked_shl(bias_shift).ok_or_else(|| {
        network_first_new_actor_error(
            "spawn-location",
            format!("Vector3i bias shift {bias_shift} is invalid"),
        )
    })?;

    let x = decode_network_vector_component_v1(&mut probe, component_width, bias, "x")?;
    let y = decode_network_vector_component_v1(&mut probe, component_width, bias, "y")?;
    let z = decode_network_vector_component_v1(&mut probe, component_width, bias, "z")?;
    let result = ReplayNetworkVector3iV1 { x, y, z };
    *cursor = probe;
    Ok(result)
}

fn decode_network_vector_component_v1(
    cursor: &mut NetworkBitCursor<'_>,
    width: usize,
    bias: i64,
    component: &str,
) -> Result<i32> {
    let raw = cursor.read_bits_le(width).map_err(|error| {
        network_first_new_actor_error(
            "spawn-location",
            format!("cannot read Vector3i {component} component: {error}"),
        )
    })?;
    let raw = i64::try_from(raw).map_err(|_| {
        network_first_new_actor_error(
            "spawn-location",
            format!("Vector3i {component} raw value {raw} cannot fit i64"),
        )
    })?;
    let signed = raw.checked_sub(bias).ok_or_else(|| {
        network_first_new_actor_error(
            "spawn-location",
            format!("Vector3i {component} subtraction underflows"),
        )
    })?;
    i32::try_from(signed).map_err(|_| {
        network_first_new_actor_error(
            "spawn-location",
            format!("Vector3i {component} value {signed} cannot fit i32"),
        )
    })
}

fn decode_network_rotation_v1(
    cursor: &mut NetworkBitCursor<'_>,
) -> Result<ReplayNetworkRotationV1> {
    let mut probe = cursor.clone();
    let yaw = decode_network_rotation_component_v1(&mut probe, "yaw")?;
    let pitch = decode_network_rotation_component_v1(&mut probe, "pitch")?;
    let roll = decode_network_rotation_component_v1(&mut probe, "roll")?;
    let result = ReplayNetworkRotationV1 { yaw, pitch, roll };
    *cursor = probe;
    Ok(result)
}

fn decode_network_rotation_component_v1(
    cursor: &mut NetworkBitCursor<'_>,
    component: &str,
) -> Result<Option<i8>> {
    let present = cursor.read_bit().map_err(|error| {
        network_first_new_actor_error(
            "spawn-rotation",
            format!("cannot read {component} presence bit: {error}"),
        )
    })?;
    if !present {
        return Ok(None);
    }
    let raw = cursor.read_bits_le(8).map_err(|error| {
        network_first_new_actor_error(
            "spawn-rotation",
            format!("cannot read {component} signed i8 payload: {error}"),
        )
    })?;
    let raw = u8::try_from(raw).map_err(|_| {
        network_first_new_actor_error(
            "spawn-rotation",
            format!("{component} payload {raw} cannot fit u8"),
        )
    })?;
    Ok(Some(i8::from_le_bytes([raw])))
}

fn network_first_new_actor_error(category: &str, detail: impl Into<String>) -> MimirError {
    MimirError::message(format!(
        "replay network first NewActor envelope error: {category}: {}",
        detail.into()
    ))
}

'''
text = replace_once(text, function_marker, function_insert + function_marker, "R3.15C decoder insertion")

tests = r'''

    fn r3_15c_append_i32(bytes: &mut Vec<u8>, bit_position: &mut usize, value: i32) {
        r3_14d_append_bits(bytes, bit_position, u64::from(value as u32), 32);
    }

    fn r3_15c_append_vector(
        bytes: &mut Vec<u8>,
        bit_position: &mut usize,
        size_bits: u32,
        value: ReplayNetworkVector3iV1,
    ) {
        r3_14d_append_bounded(bytes, bit_position, size_bits, 22, 4);
        let width = usize::try_from(size_bits + 2).unwrap();
        let bias = 1i64 << (size_bits + 1);
        for component in [value.x, value.y, value.z] {
            let raw = i64::from(component) + bias;
            assert!(raw >= 0);
            r3_14d_append_bits(bytes, bit_position, raw as u64, width);
        }
    }

    fn r3_15c_append_rotation_component(
        bytes: &mut Vec<u8>,
        bit_position: &mut usize,
        value: Option<i8>,
    ) {
        match value {
            None => r3_14d_append_bit(bytes, bit_position, false),
            Some(value) => {
                r3_14d_append_bit(bytes, bit_position, true);
                r3_14d_append_bits(bytes, bit_position, u64::from(value as u8), 8);
            }
        }
    }

    fn r3_15c_append_rotation(
        bytes: &mut Vec<u8>,
        bit_position: &mut usize,
        value: ReplayNetworkRotationV1,
    ) {
        r3_15c_append_rotation_component(bytes, bit_position, value.yaw);
        r3_15c_append_rotation_component(bytes, bit_position, value.pitch);
        r3_15c_append_rotation_component(bytes, bit_position, value.roll);
    }

    fn r3_15c_spawn_table(
        len: usize,
        object_index: usize,
        kind: ReplayNetworkSpawnTrajectoryV1,
    ) -> Vec<ReplayNetworkSpawnTrajectoryV1> {
        let mut table = vec![ReplayNetworkSpawnTrajectoryV1::None; len];
        table[object_index] = kind;
        table
    }

    #[test]
    fn r3_15c_non_byte_aligned_signed_fields_and_none_spawn() {
        let mut bytes = Vec::new();
        let mut bit = 0usize;
        r3_14d_append_bits(&mut bytes, &mut bit, 0b101, 3);
        let start = bit;
        r3_15c_append_i32(&mut bytes, &mut bit, -123_456);
        r3_14d_append_bit(&mut bytes, &mut bit, true);
        r3_15c_append_i32(&mut bytes, &mut bit, 1);
        let expected_stop = bit;
        let mut cursor = NetworkBitCursor::new(&bytes);
        cursor.bit_position = start;
        let table = r3_15c_spawn_table(2, 1, ReplayNetworkSpawnTrajectoryV1::None);
        let actor = decode_network_new_actor_v1(&mut cursor, &table).expect("None spawn");
        assert_eq!(actor.name_id, -123_456);
        assert!(actor.opaque_post_name_bit);
        assert_eq!(actor.object_id, 1);
        assert_eq!(actor.spawn_kind, ReplayNetworkSpawnTrajectoryV1::None);
        assert_eq!(actor.location, None);
        assert_eq!(actor.rotation, None);
        assert_eq!(actor.stop_bit, expected_stop as u64);
        assert_eq!(cursor.position_bits(), expected_stop);
    }

    #[test]
    fn r3_15c_negative_object_id_fails_atomically() {
        let mut bytes = Vec::new();
        let mut bit = 0usize;
        r3_15c_append_i32(&mut bytes, &mut bit, 7);
        r3_14d_append_bit(&mut bytes, &mut bit, false);
        r3_15c_append_i32(&mut bytes, &mut bit, -1);
        let mut cursor = NetworkBitCursor::new(&bytes);
        let error = decode_network_new_actor_v1(&mut cursor, &[ReplayNetworkSpawnTrajectoryV1::None])
            .expect_err("negative object id must fail");
        assert_eq!(cursor.position_bits(), 0);
        assert_error_contains(error, "first NewActor envelope error: object-id");
    }

    #[test]
    fn r3_15c_out_of_range_object_id_fails_atomically() {
        let mut bytes = Vec::new();
        let mut bit = 0usize;
        r3_15c_append_i32(&mut bytes, &mut bit, 7);
        r3_14d_append_bit(&mut bytes, &mut bit, false);
        r3_15c_append_i32(&mut bytes, &mut bit, 2);
        let mut cursor = NetworkBitCursor::new(&bytes);
        let table = vec![ReplayNetworkSpawnTrajectoryV1::None; 2];
        let error = decode_network_new_actor_v1(&mut cursor, &table)
            .expect_err("out-of-range object id must fail");
        assert_eq!(cursor.position_bits(), 0);
        assert_error_contains(error, "first NewActor envelope error: object-id");
    }

    #[test]
    fn r3_15c_vector_discriminator_zero_and_signed_bias() {
        let expected = ReplayNetworkVector3iV1 { x: -8, y: 0, z: 7 };
        let mut bytes = Vec::new();
        let mut bit = 0usize;
        r3_15c_append_vector(&mut bytes, &mut bit, 2, expected);
        let expected_stop = bit;
        let mut cursor = NetworkBitCursor::new(&bytes);
        let decoded = decode_network_vector3i_v1(&mut cursor).expect("Vector3i discriminator zero");
        assert_eq!(decoded, expected);
        assert_eq!(cursor.position_bits(), expected_stop);
    }

    #[test]
    fn r3_15c_vector_discriminator_one_path() {
        let expected = ReplayNetworkVector3iV1 { x: -123, y: 456, z: 0 };
        let mut bytes = Vec::new();
        let mut bit = 0usize;
        r3_15c_append_vector(&mut bytes, &mut bit, 18, expected);
        let expected_stop = bit;
        let mut cursor = NetworkBitCursor::new(&bytes);
        let decoded = decode_network_vector3i_v1(&mut cursor).expect("Vector3i discriminator one");
        assert_eq!(decoded, expected);
        assert_eq!(cursor.position_bits(), expected_stop);
    }

    #[test]
    fn r3_15c_vector_truncation_is_atomic() {
        let mut bytes = Vec::new();
        let mut bit = 0usize;
        r3_14d_append_bounded(&mut bytes, &mut bit, 2, 22, 4);
        r3_14d_append_bits(&mut bytes, &mut bit, 0, 4);
        let mut cursor = NetworkBitCursor::new(&bytes);
        let error = decode_network_vector3i_v1(&mut cursor).expect_err("truncated vector");
        assert_eq!(cursor.position_bits(), 0);
        assert_error_contains(error, "first NewActor envelope error: spawn-location");
    }

    #[test]
    fn r3_15c_rotation_all_absent_consumes_three_bits() {
        let expected = ReplayNetworkRotationV1 { yaw: None, pitch: None, roll: None };
        let mut bytes = Vec::new();
        let mut bit = 0usize;
        r3_15c_append_rotation(&mut bytes, &mut bit, expected);
        assert_eq!(bit, 3);
        let mut cursor = NetworkBitCursor::new(&bytes);
        let decoded = decode_network_rotation_v1(&mut cursor).expect("all absent rotation");
        assert_eq!(decoded, expected);
        assert_eq!(cursor.position_bits(), 3);
    }

    #[test]
    fn r3_15c_rotation_all_present_consumes_twenty_seven_bits() {
        let expected = ReplayNetworkRotationV1 {
            yaw: Some(-128),
            pitch: Some(0),
            roll: Some(127),
        };
        let mut bytes = Vec::new();
        let mut bit = 0usize;
        r3_15c_append_rotation(&mut bytes, &mut bit, expected);
        assert_eq!(bit, 27);
        let mut cursor = NetworkBitCursor::new(&bytes);
        let decoded = decode_network_rotation_v1(&mut cursor).expect("all present rotation");
        assert_eq!(decoded, expected);
        assert_eq!(cursor.position_bits(), 27);
    }

    #[test]
    fn r3_15c_rotation_mixed_presence_preserves_order() {
        let expected = ReplayNetworkRotationV1 { yaw: Some(-5), pitch: None, roll: Some(9) };
        let mut bytes = Vec::new();
        let mut bit = 0usize;
        r3_15c_append_rotation(&mut bytes, &mut bit, expected);
        let expected_stop = bit;
        let mut cursor = NetworkBitCursor::new(&bytes);
        assert_eq!(decode_network_rotation_v1(&mut cursor).unwrap(), expected);
        assert_eq!(cursor.position_bits(), expected_stop);
    }

    #[test]
    fn r3_15c_rotation_truncation_is_atomic() {
        let mut bytes = Vec::new();
        let mut bit = 0usize;
        r3_14d_append_bit(&mut bytes, &mut bit, true);
        r3_14d_append_bits(&mut bytes, &mut bit, 0x55, 4);
        let mut cursor = NetworkBitCursor::new(&bytes);
        let error = decode_network_rotation_v1(&mut cursor).expect_err("truncated rotation");
        assert_eq!(cursor.position_bits(), 0);
        assert_error_contains(error, "first NewActor envelope error: spawn-rotation");
    }

    #[test]
    fn r3_15c_location_spawn_stops_at_vector_endpoint() {
        let vector = ReplayNetworkVector3iV1 { x: -4, y: 5, z: 6 };
        let mut bytes = Vec::new();
        let mut bit = 0usize;
        r3_15c_append_i32(&mut bytes, &mut bit, 11);
        r3_14d_append_bit(&mut bytes, &mut bit, false);
        r3_15c_append_i32(&mut bytes, &mut bit, 1);
        r3_15c_append_vector(&mut bytes, &mut bit, 3, vector);
        let expected_stop = bit;
        let table = r3_15c_spawn_table(2, 1, ReplayNetworkSpawnTrajectoryV1::Location);
        let mut cursor = NetworkBitCursor::new(&bytes);
        let actor = decode_network_new_actor_v1(&mut cursor, &table).unwrap();
        assert_eq!(actor.location, Some(vector));
        assert_eq!(actor.rotation, None);
        assert_eq!(actor.stop_bit, expected_stop as u64);
    }

    #[test]
    fn r3_15c_location_rotation_spawn_stops_at_rotation_endpoint() {
        let vector = ReplayNetworkVector3iV1 { x: 1, y: -2, z: 3 };
        let rotation = ReplayNetworkRotationV1 { yaw: Some(-7), pitch: None, roll: Some(12) };
        let mut bytes = Vec::new();
        let mut bit = 0usize;
        r3_15c_append_i32(&mut bytes, &mut bit, -42);
        r3_14d_append_bit(&mut bytes, &mut bit, true);
        r3_15c_append_i32(&mut bytes, &mut bit, 1);
        r3_15c_append_vector(&mut bytes, &mut bit, 3, vector);
        r3_15c_append_rotation(&mut bytes, &mut bit, rotation);
        let expected_stop = bit;
        let table = r3_15c_spawn_table(2, 1, ReplayNetworkSpawnTrajectoryV1::LocationAndRotation);
        let mut cursor = NetworkBitCursor::new(&bytes);
        let actor = decode_network_new_actor_v1(&mut cursor, &table).unwrap();
        assert_eq!(actor.location, Some(vector));
        assert_eq!(actor.rotation, Some(rotation));
        assert_eq!(actor.stop_bit, expected_stop as u64);
    }

    #[test]
    fn r3_15c_absent_dead_and_non_new_headers_do_not_decode_payload() {
        let cases = [
            (false, None, None),
            (true, Some(false), None),
            (true, Some(true), Some(false)),
        ];
        for (actor_present, alive, is_new) in cases {
            let header = DecodedNetworkFirstActorHeaderV1 {
                time_raw_u32: 1.0f32.to_bits(),
                delta_raw_u32: 0.01f32.to_bits(),
                actor_present,
                actor_id: actor_present.then_some(0),
                alive,
                is_new,
                stop_bit: 0,
            };
            let decoded = decode_network_new_actor_after_header_v1(&[], &header, &[])
                .expect("non-new branch must not require spawn table or payload bits");
            assert_eq!(decoded, None);
        }
    }

    #[test]
    fn r3_15c_first_envelope_fields_are_preserved_on_checked_fixtures() {
        for (path, label) in [
            (FIXTURE_001_PATH, FIXTURE_001_LABEL),
            (FIXTURE_002_PATH, FIXTURE_002_LABEL),
            (FIXTURE_003_PATH, FIXTURE_003_LABEL),
        ] {
            let Some(bytes) = load_fixture_bytes_or_skip(path, label) else {
                return;
            };
            let input = ReplayInput::Memory { label: label.to_string(), bytes };
            let old = MinimalReplayNetworkFirstActorEnvelopeReader
                .read_network_first_actor_envelope(&input)
                .expect("admitted R3.14D envelope");
            let extended = MinimalReplayNetworkFirstNewActorEnvelopeReader
                .read_network_first_new_actor_envelope(&input)
                .expect("R3.15C additive envelope");
            assert_eq!(extended.envelope, old);
            let actor = extended.new_actor.expect("first actor is new in admitted fixture lane");
            assert!(actor.stop_bit >= old.stop_bit);
        }
    }

    #[test]
    fn r3_15c_reader_rejects_file_input() {
        let error = MinimalReplayNetworkFirstNewActorEnvelopeReader
            .read_network_first_new_actor_envelope(&ReplayInput::file("sample.replay"))
            .expect_err("File input remains outside R3.15C");
        assert_error_contains(error, "first NewActor envelope error: unsupported-input");
    }
'''

last_close = text.rfind("\n}")
if last_close < 0:
    raise SystemExit("cannot locate final test-module close")
text = text[:last_close] + tests + text[last_close:]
SOURCE.write_text(text, encoding="utf-8")
print("R3_15C_PATCH=APPLIED")
