use mimir_core::{MimirError, Result};
use mimir_types::{FieldValue, Metadata, ReplayId};
use serde::{Deserialize, Serialize};
use std::collections::{BTreeMap, BTreeSet};
use std::path::PathBuf;

mod k3_admitted_groups;
mod k4_admitted_groups;
mod k4_native;
pub use k4_admitted_groups::{R3_17N_K4_ADMITTED_GROUPS_V1, ReplayNetworkK4AdmittedGroupV1};
pub use k4_native::*;

/// Private LSB-first cursor for Rocket League replay network payload bits.
///
/// R3.14C deliberately keeps this primitive internal. Replay-envelope semantics
/// remain closed until R3.14D.
#[cfg_attr(not(test), allow(dead_code))]
#[derive(Debug, Clone)]
struct NetworkBitCursor<'a> {
    bytes: &'a [u8],
    bit_position: usize,
}

#[cfg_attr(not(test), allow(dead_code))]
impl<'a> NetworkBitCursor<'a> {
    fn new(bytes: &'a [u8]) -> Self {
        Self {
            bytes,
            bit_position: 0,
        }
    }

    fn position_bits(&self) -> usize {
        self.bit_position
    }

    fn remaining_bits(&self) -> usize {
        self.bytes
            .len()
            .saturating_mul(8)
            .saturating_sub(self.bit_position)
    }

    fn read_bit(&mut self) -> Result<bool> {
        let total_bits = self.bytes.len().checked_mul(8).ok_or_else(|| {
            network_bit_error("invalid-length", "network bit length overflows usize")
        })?;
        if self.bit_position >= total_bits {
            return Err(network_bit_error(
                "insufficient-bits",
                format!(
                    "need 1 bit at position {}, but no bits remain",
                    self.bit_position
                ),
            ));
        }

        let position = self.bit_position;
        let byte_index = position / 8;
        let bit_index = position % 8;
        let bit = ((self.bytes[byte_index] >> bit_index) & 1) != 0;
        self.bit_position = position + 1;
        Ok(bit)
    }

    fn read_bits_le(&mut self, width: usize) -> Result<u64> {
        if width > 64 {
            return Err(network_bit_error(
                "invalid-width",
                format!("bit width {width} exceeds 64"),
            ));
        }

        let start = self.bit_position;
        let end = start.checked_add(width).ok_or_else(|| {
            network_bit_error("invalid-position", "bit position addition overflows usize")
        })?;
        let total_bits = self.bytes.len().checked_mul(8).ok_or_else(|| {
            network_bit_error("invalid-length", "network bit length overflows usize")
        })?;
        if end > total_bits {
            return Err(network_bit_error(
                "insufficient-bits",
                format!(
                    "need {width} bits at position {start}, but only {} remain",
                    total_bits.saturating_sub(start)
                ),
            ));
        }

        let mut value = 0u64;
        for output_bit in 0..width {
            let position = start + output_bit;
            let byte = self.bytes[position / 8];
            let bit = (byte >> (position % 8)) & 1;
            value |= u64::from(bit) << output_bit;
        }

        self.bit_position = end;
        Ok(value)
    }

    fn read_bounded_u32(&mut self, max_exclusive: u32, low_width: u8) -> Result<u32> {
        if max_exclusive == 0 {
            return Err(network_bit_error(
                "invalid-maximum",
                "bounded integer maximum must be greater than zero",
            ));
        }
        if low_width > 32 {
            return Err(network_bit_error(
                "invalid-low-width",
                format!("bounded integer low width {low_width} exceeds 32"),
            ));
        }

        let range = 1u64 << low_width;
        let max_exclusive_u64 = u64::from(max_exclusive);
        if range > max_exclusive_u64 {
            return Err(network_bit_error(
                "invalid-configuration",
                format!(
                    "bounded integer range {range} from low width {low_width} exceeds maximum {max_exclusive}"
                ),
            ));
        }

        let start = self.bit_position;
        let low = self.read_bits_le(usize::from(low_width))?;
        let up = low + range;
        let value = if up < max_exclusive_u64 {
            match self.read_bit() {
                Ok(true) => up,
                Ok(false) => low,
                Err(error) => {
                    self.bit_position = start;
                    return Err(error);
                }
            }
        } else {
            low
        };

        if value >= max_exclusive_u64 {
            self.bit_position = start;
            return Err(network_bit_error(
                "invalid-bounded-result",
                format!("decoded value {value} is outside maximum {max_exclusive}"),
            ));
        }

        match u32::try_from(value) {
            Ok(value) => Ok(value),
            Err(_) => {
                self.bit_position = start;
                Err(network_bit_error(
                    "invalid-bounded-result",
                    format!("decoded value {value} does not fit in u32"),
                ))
            }
        }
    }
}

fn network_bit_error(category: &str, detail: impl Into<String>) -> MimirError {
    MimirError::message(format!(
        "replay network bit error: {category}: {}",
        detail.into()
    ))
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub enum ReplayInput {
    File(PathBuf),
    Memory { label: String, bytes: Vec<u8> },
}

impl ReplayInput {
    pub fn file(path: impl Into<PathBuf>) -> Self {
        Self::File(path.into())
    }

    pub fn label(&self) -> String {
        match self {
            Self::File(path) => path
                .file_name()
                .map(|value| value.to_string_lossy().into_owned())
                .unwrap_or_else(|| path.display().to_string()),
            Self::Memory { label, .. } => label.clone(),
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub struct ReplayHeader {
    pub replay_id: ReplayId,
    pub source_label: String,
    pub total_frames: Option<u32>,
    pub metadata: Metadata,
}

pub trait ReplayReader {
    fn read_header(&self, input: &ReplayInput) -> Result<ReplayHeader>;
}

/// Structural framing facts immediately after the replay header.
///
/// This type does not imply supported ReplayHeader semantics, CRC validity,
/// replay-body semantic validity, frame decoding, raw-state extraction, or events.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct ReplayBodyBoundaryV1 {
    pub source_label: String,
    pub header_size: u32,
    pub header_end: u64,
    pub content_size: u32,
    /// Stored content CRC field. MinimalReplayBodyBoundaryReader does not validate it.
    pub content_crc: u32,
    pub content_start: u64,
    pub content_end: u64,
    pub input_len: u64,
}

pub trait ReplayBodyBoundaryReader {
    fn read_body_boundary(&self, input: &ReplayInput) -> Result<ReplayBodyBoundaryV1>;
}

#[derive(Debug, Default, Clone, Copy)]
pub struct MinimalReplayBodyBoundaryReader;

impl ReplayBodyBoundaryReader for MinimalReplayBodyBoundaryReader {
    fn read_body_boundary(&self, input: &ReplayInput) -> Result<ReplayBodyBoundaryV1> {
        match input {
            ReplayInput::Memory { label, bytes } => {
                parse_replay_body_boundary_from_memory(label, bytes)
            }
            ReplayInput::File(path) => Err(body_boundary_error(
                "unsupported-input",
                format!(
                    "ReplayInput::File is outside the minimal body-boundary reader: {}",
                    path.display()
                ),
            )),
        }
    }
}

/// Structural body scaffold through the raw network payload boundary.
///
/// Levels are skipped only far enough to locate later sections. Keyframe tuples,
/// network bytes, and footer bytes are not semantically decoded by this type.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct ReplayContentScaffoldV1 {
    pub boundary: ReplayBodyBoundaryV1,
    pub levels_count_offset: u64,
    pub levels_count: u32,
    pub levels_data_start: u64,
    pub levels_end: u64,
    pub keyframes_count_offset: u64,
    pub keyframes_count: u32,
    pub keyframes_data_start: u64,
    pub keyframes_end: u64,
    pub network_size_offset: u64,
    pub network_size: u32,
    pub network_start: u64,
    pub network_end: u64,
    pub footer_start: u64,
    pub footer_size: u64,
}

pub trait ReplayContentScaffoldReader {
    fn read_content_scaffold(&self, input: &ReplayInput) -> Result<ReplayContentScaffoldV1>;
}

#[derive(Debug, Default, Clone, Copy)]
pub struct MinimalReplayContentScaffoldReader;

impl ReplayContentScaffoldReader for MinimalReplayContentScaffoldReader {
    fn read_content_scaffold(&self, input: &ReplayInput) -> Result<ReplayContentScaffoldV1> {
        match input {
            ReplayInput::Memory { label, bytes } => {
                parse_replay_content_scaffold_from_memory(label, bytes)
            }
            ReplayInput::File(path) => Err(content_scaffold_error(
                "unsupported-input",
                format!(
                    "ReplayInput::File is outside the minimal content-scaffold reader: {}",
                    path.display()
                ),
            )),
        }
    }
}

/// Structural footer scaffold after the raw replay network payload.
///
/// This type records bounded offsets and counts only. It does not decode network bits,
/// interpret footer strings, build object/name/net-cache lookup semantics, validate CRCs,
/// extract frames/raw states/events, or assign meaning to the optional opaque tail bytes.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct ReplayFooterScaffoldV1 {
    pub content: ReplayContentScaffoldV1,
    pub debug_info_count_offset: u64,
    pub debug_info_count: u32,
    pub debug_info_data_start: u64,
    pub debug_info_end: u64,
    pub tickmarks_count_offset: u64,
    pub tickmarks_count: u32,
    pub tickmarks_data_start: u64,
    pub tickmarks_end: u64,
    pub packages_count_offset: u64,
    pub packages_count: u32,
    pub packages_data_start: u64,
    pub packages_end: u64,
    pub objects_count_offset: u64,
    pub objects_count: u32,
    pub objects_data_start: u64,
    pub objects_end: u64,
    pub names_count_offset: u64,
    pub names_count: u32,
    pub names_data_start: u64,
    pub names_end: u64,
    pub class_indices_count_offset: u64,
    pub class_indices_count: u32,
    pub class_indices_data_start: u64,
    pub class_indices_end: u64,
    pub net_cache_count_offset: u64,
    pub net_cache_count: u32,
    pub net_cache_data_start: u64,
    pub net_cache_properties_count: u32,
    pub net_cache_end: u64,
    /// First byte after the structurally known footer fields.
    pub opaque_tail_start: u64,
    /// Admitted observed forms are zero bytes or exactly four zero bytes.
    /// No semantic meaning is assigned to either form.
    pub opaque_tail_size: u32,
    pub footer_end: u64,
}

pub trait ReplayFooterScaffoldReader {
    fn read_footer_scaffold(&self, input: &ReplayInput) -> Result<ReplayFooterScaffoldV1>;
}

#[derive(Debug, Default, Clone, Copy)]
pub struct MinimalReplayFooterScaffoldReader;

impl ReplayFooterScaffoldReader for MinimalReplayFooterScaffoldReader {
    fn read_footer_scaffold(&self, input: &ReplayInput) -> Result<ReplayFooterScaffoldV1> {
        match input {
            ReplayInput::Memory { label, bytes } => {
                parse_replay_footer_scaffold_from_memory(label, bytes)
            }
            ReplayInput::File(path) => Err(footer_scaffold_error(
                "unsupported-input",
                format!(
                    "ReplayInput::File is outside the minimal footer-scaffold reader: {}",
                    path.display()
                ),
            )),
        }
    }
}

/// Raw class-index row materialized from the replay footer.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct ReplayClassIndexV1 {
    pub class_name: String,
    pub object_index: u32,
}

/// Raw network-cache property row materialized from the replay footer.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct ReplayNetCachePropertyV1 {
    pub object_index: u32,
    pub stream_id: u32,
}

/// Raw network-cache row materialized from the replay footer.
///
/// `parent_id` and `cache_id` are intentionally preserved as opaque signed values.
/// This pass does not treat them as hierarchy identifiers or uniqueness predicates.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct ReplayNetCacheEntryV1 {
    pub object_index: u32,
    pub parent_id: i32,
    pub cache_id: i32,
    pub properties: Vec<ReplayNetCachePropertyV1>,
}

/// Typed raw lookup tables from the replay footer.
///
/// This is not a network decoder and not an inheritance/attribute resolver. It materializes
/// only the raw object/name/class-index/net-cache tables proven by the checked-in evidence.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct ReplayFooterLookupMaterializationV1 {
    pub scaffold: ReplayFooterScaffoldV1,
    pub objects: Vec<String>,
    pub names: Vec<String>,
    pub class_indices: Vec<ReplayClassIndexV1>,
    pub net_cache: Vec<ReplayNetCacheEntryV1>,
}

pub trait ReplayFooterLookupMaterializationReader {
    fn read_footer_lookup_materialization(
        &self,
        input: &ReplayInput,
    ) -> Result<ReplayFooterLookupMaterializationV1>;
}

#[derive(Debug, Default, Clone, Copy)]
pub struct MinimalReplayFooterLookupMaterializationReader;

impl ReplayFooterLookupMaterializationReader for MinimalReplayFooterLookupMaterializationReader {
    fn read_footer_lookup_materialization(
        &self,
        input: &ReplayInput,
    ) -> Result<ReplayFooterLookupMaterializationV1> {
        match input {
            ReplayInput::Memory { label, bytes } => {
                parse_replay_footer_lookup_materialization_from_memory(label, bytes)
            }
            ReplayInput::File(path) => Err(footer_lookup_error(
                "unsupported-input",
                format!(
                    "ReplayInput::File is outside the footer lookup materializer: {}",
                    path.display()
                ),
            )),
        }
    }
}

/// Byte-aligned timing preamble and decoder prerequisites for the first admitted network frame.
///
/// This type deliberately stops after the first 8 network bytes (`f32 time`, `f32 delta`).
/// It does not consume actor bits, iterate frames, resolve attributes, extract raw state/events,
/// or validate replay CRC fields.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub struct ReplayNetworkTimingPreambleV1 {
    pub header: ReplayHeader,
    pub content: ReplayContentScaffoldV1,
    pub num_frames: u32,
    pub max_channels: u32,
    pub channel_bits: u8,
    pub first_frame_time: f32,
    pub first_frame_delta: f32,
}

pub trait ReplayNetworkTimingPreambleReader {
    fn read_network_timing_preamble(
        &self,
        input: &ReplayInput,
    ) -> Result<ReplayNetworkTimingPreambleV1>;
}

#[derive(Debug, Default, Clone, Copy)]
pub struct MinimalReplayNetworkTimingPreambleReader;

impl ReplayNetworkTimingPreambleReader for MinimalReplayNetworkTimingPreambleReader {
    fn read_network_timing_preamble(
        &self,
        input: &ReplayInput,
    ) -> Result<ReplayNetworkTimingPreambleV1> {
        match input {
            ReplayInput::Memory { label, bytes } => {
                parse_replay_network_timing_preamble_from_memory(label, bytes)
            }
            ReplayInput::File(path) => Err(network_timing_error(
                "unsupported-input",
                format!(
                    "ReplayInput::File is outside the network timing preamble reader: {}",
                    path.display()
                ),
            )),
        }
    }
}

/// First native replay-network frame / actor-envelope header admitted through the `new` bit.
///
/// This type deliberately stops before `name_id`, object/spawn payloads, property payloads,
/// additional actors, or additional frames.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub struct ReplayNetworkFirstActorEnvelopeV1 {
    pub timing: ReplayNetworkTimingPreambleV1,
    pub first_frame_time_raw_u32: u32,
    pub first_frame_delta_raw_u32: u32,
    pub actor_present: bool,
    pub actor_id: Option<u32>,
    pub alive: Option<bool>,
    pub is_new: Option<bool>,
    pub stop_bit: u64,
}

pub trait ReplayNetworkFirstActorEnvelopeReader {
    fn read_network_first_actor_envelope(
        &self,
        input: &ReplayInput,
    ) -> Result<ReplayNetworkFirstActorEnvelopeV1>;
}

#[derive(Debug, Default, Clone, Copy)]
pub struct MinimalReplayNetworkFirstActorEnvelopeReader;

impl ReplayNetworkFirstActorEnvelopeReader for MinimalReplayNetworkFirstActorEnvelopeReader {
    fn read_network_first_actor_envelope(
        &self,
        input: &ReplayInput,
    ) -> Result<ReplayNetworkFirstActorEnvelopeV1> {
        match input {
            ReplayInput::Memory { label, bytes } => {
                parse_replay_network_first_actor_envelope_from_memory(label, bytes)
            }
            ReplayInput::File(path) => Err(network_first_actor_envelope_error(
                "unsupported-input",
                format!(
                    "ReplayInput::File is outside the first actor-envelope reader: {}",
                    path.display()
                ),
            )),
        }
    }
}

/// Signed integer vector decoded from one admitted NewActor spawn trajectory.
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

/// Conservative network attribute wire-tag registry admitted from the supported replay lane.
///
/// Only the 102 attribute names observed in successfully decoded updates are explicitly admitted.
/// Every other name maps to `NotImplemented`, even if a broader external registry knows it.
/// This layer performs lookup only; it does not consume network bits or decode payload values.
#[derive(Debug, Clone, Copy, Serialize, Deserialize, PartialEq, Eq, PartialOrd, Ord, Hash)]
#[serde(rename_all = "snake_case")]
pub enum ReplayNetworkAttributeTagV1 {
    ActiveActor,
    Boolean,
    Byte,
    CamSettings,
    ClubColors,
    DemolishExtended,
    DemolishFx,
    Enum,
    ExtendedExplosion,
    Float,
    Int,
    Int64,
    LoadoutsOnline,
    Location,
    PartyLeader,
    PickupNew,
    PlayerHistoryKey,
    QWordString,
    ReplicatedBoost,
    Reservation,
    RigidBody,
    StatEvent,
    String,
    TeamLoadout,
    TeamPaint,
    UniqueId,
    NotImplemented,
}

#[derive(Debug, Clone, Copy, Serialize, Deserialize, PartialEq, Eq, PartialOrd, Ord, Hash)]
#[serde(rename_all = "snake_case")]
pub enum ReplayNetworkSpawnTrajectoryV1 {
    None,
    Location,
    LocationAndRotation,
}

const OBSERVED_NETWORK_ATTRIBUTE_TAGS_V1: [(&str, ReplayNetworkAttributeTagV1); 102] = [
    ("Engine.Actor:DrawScale", ReplayNetworkAttributeTagV1::Float),
    ("Engine.Actor:RemoteRole", ReplayNetworkAttributeTagV1::Enum),
    (
        "Engine.Actor:bBlockActors",
        ReplayNetworkAttributeTagV1::Boolean,
    ),
    (
        "Engine.Actor:bCollideActors",
        ReplayNetworkAttributeTagV1::Boolean,
    ),
    ("Engine.Actor:bHidden", ReplayNetworkAttributeTagV1::Boolean),
    (
        "Engine.GameReplicationInfo:GameClass",
        ReplayNetworkAttributeTagV1::ActiveActor,
    ),
    (
        "Engine.GameReplicationInfo:ServerName",
        ReplayNetworkAttributeTagV1::String,
    ),
    (
        "Engine.Pawn:PlayerReplicationInfo",
        ReplayNetworkAttributeTagV1::ActiveActor,
    ),
    (
        "Engine.PlayerReplicationInfo:Ping",
        ReplayNetworkAttributeTagV1::Byte,
    ),
    (
        "Engine.PlayerReplicationInfo:PlayerID",
        ReplayNetworkAttributeTagV1::Int,
    ),
    (
        "Engine.PlayerReplicationInfo:PlayerName",
        ReplayNetworkAttributeTagV1::String,
    ),
    (
        "Engine.PlayerReplicationInfo:Score",
        ReplayNetworkAttributeTagV1::Int,
    ),
    (
        "Engine.PlayerReplicationInfo:Team",
        ReplayNetworkAttributeTagV1::ActiveActor,
    ),
    (
        "Engine.PlayerReplicationInfo:UniqueId",
        ReplayNetworkAttributeTagV1::UniqueId,
    ),
    (
        "Engine.PlayerReplicationInfo:bTimedOut",
        ReplayNetworkAttributeTagV1::Boolean,
    ),
    ("Engine.TeamInfo:Score", ReplayNetworkAttributeTagV1::Int),
    (
        "ProjectX.GRI_X:GameServerID",
        ReplayNetworkAttributeTagV1::QWordString,
    ),
    (
        "ProjectX.GRI_X:MatchGUID",
        ReplayNetworkAttributeTagV1::String,
    ),
    (
        "ProjectX.GRI_X:MatchGuid",
        ReplayNetworkAttributeTagV1::String,
    ),
    (
        "ProjectX.GRI_X:ReplicatedGamePlaylist",
        ReplayNetworkAttributeTagV1::Int,
    ),
    (
        "ProjectX.GRI_X:ReplicatedServerRegion",
        ReplayNetworkAttributeTagV1::String,
    ),
    (
        "ProjectX.GRI_X:Reservations",
        ReplayNetworkAttributeTagV1::Reservation,
    ),
    (
        "ProjectX.GRI_X:bGameStarted",
        ReplayNetworkAttributeTagV1::Boolean,
    ),
    (
        "TAGame.Ball_TA:GameEvent",
        ReplayNetworkAttributeTagV1::ActiveActor,
    ),
    (
        "TAGame.Ball_TA:HitTeamNum",
        ReplayNetworkAttributeTagV1::Byte,
    ),
    (
        "TAGame.Ball_TA:ReplicatedExplosionDataExtended",
        ReplayNetworkAttributeTagV1::ExtendedExplosion,
    ),
    (
        "TAGame.Ball_TA:ReplicatedWorldBounceScale",
        ReplayNetworkAttributeTagV1::Float,
    ),
    (
        "TAGame.CameraSettingsActor_TA:CameraPitch",
        ReplayNetworkAttributeTagV1::Byte,
    ),
    (
        "TAGame.CameraSettingsActor_TA:CameraYaw",
        ReplayNetworkAttributeTagV1::Byte,
    ),
    (
        "TAGame.CameraSettingsActor_TA:PRI",
        ReplayNetworkAttributeTagV1::ActiveActor,
    ),
    (
        "TAGame.CameraSettingsActor_TA:ProfileSettings",
        ReplayNetworkAttributeTagV1::CamSettings,
    ),
    (
        "TAGame.CameraSettingsActor_TA:bMouseCameraToggleEnabled",
        ReplayNetworkAttributeTagV1::Boolean,
    ),
    (
        "TAGame.CameraSettingsActor_TA:bUsingBehindView",
        ReplayNetworkAttributeTagV1::Boolean,
    ),
    (
        "TAGame.CameraSettingsActor_TA:bUsingSecondaryCamera",
        ReplayNetworkAttributeTagV1::Boolean,
    ),
    (
        "TAGame.CameraSettingsActor_TA:bUsingSwivel",
        ReplayNetworkAttributeTagV1::Boolean,
    ),
    (
        "TAGame.CarComponent_AirActivate_TA:AirActivateCount",
        ReplayNetworkAttributeTagV1::Int,
    ),
    (
        "TAGame.CarComponent_Boost_TA:ReplicatedBoost",
        ReplayNetworkAttributeTagV1::ReplicatedBoost,
    ),
    (
        "TAGame.CarComponent_Boost_TA:ReplicatedBoostAmount",
        ReplayNetworkAttributeTagV1::Byte,
    ),
    (
        "TAGame.CarComponent_Dodge_TA:DodgeImpulse",
        ReplayNetworkAttributeTagV1::Location,
    ),
    (
        "TAGame.CarComponent_Dodge_TA:DodgeTorque",
        ReplayNetworkAttributeTagV1::Location,
    ),
    (
        "TAGame.CarComponent_DoubleJump_TA:DoubleJumpImpulse",
        ReplayNetworkAttributeTagV1::Location,
    ),
    (
        "TAGame.CarComponent_FlipCar_TA:FlipCarTime",
        ReplayNetworkAttributeTagV1::Float,
    ),
    (
        "TAGame.CarComponent_FlipCar_TA:bFlipRight",
        ReplayNetworkAttributeTagV1::Boolean,
    ),
    (
        "TAGame.CarComponent_TA:ReplicatedActive",
        ReplayNetworkAttributeTagV1::Byte,
    ),
    (
        "TAGame.CarComponent_TA:Vehicle",
        ReplayNetworkAttributeTagV1::ActiveActor,
    ),
    (
        "TAGame.Car_TA:ClubColors",
        ReplayNetworkAttributeTagV1::ClubColors,
    ),
    (
        "TAGame.Car_TA:ReplicatedDemolishExtended",
        ReplayNetworkAttributeTagV1::DemolishExtended,
    ),
    (
        "TAGame.Car_TA:ReplicatedDemolishGoalExplosion",
        ReplayNetworkAttributeTagV1::DemolishFx,
    ),
    (
        "TAGame.Car_TA:RumblePickups",
        ReplayNetworkAttributeTagV1::ActiveActor,
    ),
    (
        "TAGame.Car_TA:TeamPaint",
        ReplayNetworkAttributeTagV1::TeamPaint,
    ),
    (
        "TAGame.GameEvent_Soccar_TA:ReplicatedScoredOnTeam",
        ReplayNetworkAttributeTagV1::Byte,
    ),
    (
        "TAGame.GameEvent_Soccar_TA:ReplicatedStatEvent",
        ReplayNetworkAttributeTagV1::StatEvent,
    ),
    (
        "TAGame.GameEvent_Soccar_TA:RoundNum",
        ReplayNetworkAttributeTagV1::Int,
    ),
    (
        "TAGame.GameEvent_Soccar_TA:SecondsRemaining",
        ReplayNetworkAttributeTagV1::Int,
    ),
    (
        "TAGame.GameEvent_Soccar_TA:bBallHasBeenHit",
        ReplayNetworkAttributeTagV1::Boolean,
    ),
    (
        "TAGame.GameEvent_Soccar_TA:bClubMatch",
        ReplayNetworkAttributeTagV1::Boolean,
    ),
    (
        "TAGame.GameEvent_Soccar_TA:bOverTime",
        ReplayNetworkAttributeTagV1::Boolean,
    ),
    (
        "TAGame.GameEvent_Soccar_TA:bReadyToStartGame",
        ReplayNetworkAttributeTagV1::Boolean,
    ),
    (
        "TAGame.GameEvent_TA:BotSkill",
        ReplayNetworkAttributeTagV1::Int,
    ),
    (
        "TAGame.GameEvent_TA:MatchStartEpoch",
        ReplayNetworkAttributeTagV1::Int64,
    ),
    (
        "TAGame.GameEvent_TA:MatchTypeClass",
        ReplayNetworkAttributeTagV1::ActiveActor,
    ),
    (
        "TAGame.GameEvent_TA:ReplicatedGameStateTimeRemaining",
        ReplayNetworkAttributeTagV1::Int,
    ),
    (
        "TAGame.GameEvent_TA:ReplicatedRoundCountDownNumber",
        ReplayNetworkAttributeTagV1::Int,
    ),
    (
        "TAGame.GameEvent_TA:ReplicatedStateName",
        ReplayNetworkAttributeTagV1::Int,
    ),
    (
        "TAGame.GameEvent_TA:bCanVoteToForfeit",
        ReplayNetworkAttributeTagV1::Boolean,
    ),
    (
        "TAGame.GameEvent_TA:bHasLeaveMatchPenalty",
        ReplayNetworkAttributeTagV1::Boolean,
    ),
    (
        "TAGame.GameEvent_Team_TA:MaxTeamSize",
        ReplayNetworkAttributeTagV1::Int,
    ),
    (
        "TAGame.GameEvent_Team_TA:bForfeit",
        ReplayNetworkAttributeTagV1::Boolean,
    ),
    (
        "TAGame.PRI_TA:CarDemolitions",
        ReplayNetworkAttributeTagV1::Int,
    ),
    (
        "TAGame.PRI_TA:ClientLoadouts",
        ReplayNetworkAttributeTagV1::TeamLoadout,
    ),
    (
        "TAGame.PRI_TA:ClientLoadoutsOnline",
        ReplayNetworkAttributeTagV1::LoadoutsOnline,
    ),
    ("TAGame.PRI_TA:ClubID", ReplayNetworkAttributeTagV1::Int64),
    (
        "TAGame.PRI_TA:CurrentVoiceRoom",
        ReplayNetworkAttributeTagV1::String,
    ),
    (
        "TAGame.PRI_TA:MatchAssists",
        ReplayNetworkAttributeTagV1::Int,
    ),
    ("TAGame.PRI_TA:MatchGoals", ReplayNetworkAttributeTagV1::Int),
    ("TAGame.PRI_TA:MatchSaves", ReplayNetworkAttributeTagV1::Int),
    ("TAGame.PRI_TA:MatchScore", ReplayNetworkAttributeTagV1::Int),
    ("TAGame.PRI_TA:MatchShots", ReplayNetworkAttributeTagV1::Int),
    (
        "TAGame.PRI_TA:PartyLeader",
        ReplayNetworkAttributeTagV1::PartyLeader,
    ),
    (
        "TAGame.PRI_TA:PersistentCamera",
        ReplayNetworkAttributeTagV1::ActiveActor,
    ),
    (
        "TAGame.PRI_TA:PlayerHistoryKey",
        ReplayNetworkAttributeTagV1::PlayerHistoryKey,
    ),
    (
        "TAGame.PRI_TA:PlayerHistoryValid",
        ReplayNetworkAttributeTagV1::Boolean,
    ),
    (
        "TAGame.PRI_TA:ReplicatedGameEvent",
        ReplayNetworkAttributeTagV1::ActiveActor,
    ),
    (
        "TAGame.PRI_TA:ReplicatedWorstNetQualityBeyondLatency",
        ReplayNetworkAttributeTagV1::Byte,
    ),
    (
        "TAGame.PRI_TA:SelfDemolitions",
        ReplayNetworkAttributeTagV1::Int,
    ),
    (
        "TAGame.PRI_TA:SpectatorShortcut",
        ReplayNetworkAttributeTagV1::Int,
    ),
    (
        "TAGame.PRI_TA:SteeringSensitivity",
        ReplayNetworkAttributeTagV1::Float,
    ),
    ("TAGame.PRI_TA:Title", ReplayNetworkAttributeTagV1::Int),
    (
        "TAGame.PRI_TA:TotalGameTimePlayed",
        ReplayNetworkAttributeTagV1::Float,
    ),
    (
        "TAGame.PRI_TA:ViralItemActor",
        ReplayNetworkAttributeTagV1::ActiveActor,
    ),
    (
        "TAGame.PRI_TA:bIsDistracted",
        ReplayNetworkAttributeTagV1::Boolean,
    ),
    ("TAGame.PRI_TA:bReady", ReplayNetworkAttributeTagV1::Boolean),
    (
        "TAGame.RBActor_TA:ReplicatedRBState",
        ReplayNetworkAttributeTagV1::RigidBody,
    ),
    (
        "TAGame.RBActor_TA:bReplayActor",
        ReplayNetworkAttributeTagV1::Boolean,
    ),
    (
        "TAGame.Team_TA:ClubColors",
        ReplayNetworkAttributeTagV1::ClubColors,
    ),
    ("TAGame.Team_TA:ClubID", ReplayNetworkAttributeTagV1::Int64),
    (
        "TAGame.Team_TA:GameEvent",
        ReplayNetworkAttributeTagV1::ActiveActor,
    ),
    (
        "TAGame.VehiclePickup_TA:NewReplicatedPickupData",
        ReplayNetworkAttributeTagV1::PickupNew,
    ),
    (
        "TAGame.Vehicle_TA:ReplicatedSteer",
        ReplayNetworkAttributeTagV1::Byte,
    ),
    (
        "TAGame.Vehicle_TA:ReplicatedThrottle",
        ReplayNetworkAttributeTagV1::Byte,
    ),
    (
        "TAGame.Vehicle_TA:bDriving",
        ReplayNetworkAttributeTagV1::Boolean,
    ),
    (
        "TAGame.Vehicle_TA:bReplicatedHandbrake",
        ReplayNetworkAttributeTagV1::Boolean,
    ),
];

const OBSERVED_NETWORK_PARENT_CLASSES_V1: [(&str, &str); 65] = [
    ("Engine.Actor", "Core.Object"),
    ("Engine.GameReplicationInfo", "Engine.ReplicationInfo"),
    ("Engine.Info", "Engine.Actor"),
    ("Engine.Pawn", "Engine.Actor"),
    ("Engine.PlayerReplicationInfo", "Engine.ReplicationInfo"),
    ("Engine.ReplicationInfo", "Engine.Info"),
    ("Engine.TeamInfo", "Engine.Info"),
    ("ProjectX.GRI_X", "Engine.GameReplicationInfo"),
    ("ProjectX.NetModeReplicator_X", "Engine.ReplicationInfo"),
    ("ProjectX.PRI_X", "Engine.PlayerReplicationInfo"),
    ("ProjectX.Pawn_X", "Engine.Pawn"),
    ("TAGame.Ball_TA", "TAGame.RBActor_TA"),
    ("TAGame.CameraSettingsActor_TA", "Engine.ReplicationInfo"),
    (
        "TAGame.CarComponent_AirActivate_TA",
        "TAGame.CarComponent_TA",
    ),
    (
        "TAGame.CarComponent_Boost_TA",
        "TAGame.CarComponent_AirActivate_TA",
    ),
    (
        "TAGame.CarComponent_Dodge_TA",
        "TAGame.CarComponent_AirActivate_TA",
    ),
    (
        "TAGame.CarComponent_DoubleJump_TA",
        "TAGame.CarComponent_AirActivate_TA",
    ),
    ("TAGame.CarComponent_FlipCar_TA", "TAGame.CarComponent_TA"),
    ("TAGame.CarComponent_Jump_TA", "TAGame.CarComponent_TA"),
    ("TAGame.CarComponent_TA", "Engine.ReplicationInfo"),
    ("TAGame.Car_TA", "TAGame.Vehicle_TA"),
    ("TAGame.CrowdActor_TA", "Engine.ReplicationInfo"),
    ("TAGame.CrowdManager_TA", "Engine.ReplicationInfo"),
    ("TAGame.GRI_TA", "ProjectX.GRI_X"),
    ("TAGame.GameEvent_Soccar_TA", "TAGame.GameEvent_Team_TA"),
    ("TAGame.GameEvent_TA", "Engine.ReplicationInfo"),
    ("TAGame.GameEvent_Team_TA", "TAGame.GameEvent_TA"),
    ("TAGame.InMapScoreboard_TA", "Engine.Actor"),
    ("TAGame.PRI_TA", "ProjectX.PRI_X"),
    ("TAGame.RBActor_TA", "ProjectX.Pawn_X"),
    ("TAGame.RumblePickups_TA", "Engine.Actor"),
    ("TAGame.Team_Soccar_TA", "TAGame.Team_TA"),
    ("TAGame.Team_TA", "Engine.TeamInfo"),
    ("TAGame.VehiclePickup_Boost_TA", "TAGame.VehiclePickup_TA"),
    ("TAGame.VehiclePickup_TA", "Engine.ReplicationInfo"),
    ("TAGame.Vehicle_TA", "TAGame.RBActor_TA"),
    ("TAGame.ViralItemActor_TA", "Engine.Actor"),
    ("Archetypes.Ball.Ball_Default", "TAGame.Ball_TA"),
    ("Archetypes.Ball.Ball_Puck", "TAGame.Ball_TA"),
    ("Archetypes.Car.Car_Default", "TAGame.Car_TA"),
    (
        "Archetypes.CarComponents.CarComponent_Boost",
        "TAGame.CarComponent_Boost_TA",
    ),
    (
        "Archetypes.CarComponents.CarComponent_Dodge",
        "TAGame.CarComponent_Dodge_TA",
    ),
    (
        "Archetypes.CarComponents.CarComponent_DoubleJump",
        "TAGame.CarComponent_DoubleJump_TA",
    ),
    (
        "Archetypes.CarComponents.CarComponent_FlipCar",
        "TAGame.CarComponent_FlipCar_TA",
    ),
    (
        "Archetypes.CarComponents.CarComponent_Jump",
        "TAGame.CarComponent_Jump_TA",
    ),
    (
        "Archetypes.GameEvent.GameEvent_Soccar",
        "TAGame.GameEvent_Soccar_TA",
    ),
    ("Archetypes.Teams.Team0", "TAGame.Team_Soccar_TA"),
    ("Archetypes.Teams.Team1", "TAGame.Team_Soccar_TA"),
    (
        "GameInfo_Soccar.GameInfo.GameInfo_Soccar:GameReplicationInfoArchetype",
        "TAGame.GRI_TA",
    ),
    (
        "Gameinfo_Hockey.GameInfo.Gameinfo_Hockey:Archetype",
        "TAGame.GameEvent_Soccar_TA",
    ),
    (
        "Gameinfo_Hockey.GameInfo.Gameinfo_Hockey:GameReplicationInfoArchetype",
        "TAGame.GRI_TA",
    ),
    (
        "ProjectX.Default__NetModeReplicator_X",
        "ProjectX.NetModeReplicator_X",
    ),
    (
        "TAGame.Default__CameraSettingsActor_TA",
        "TAGame.CameraSettingsActor_TA",
    ),
    ("TAGame.Default__PRI_TA", "TAGame.PRI_TA"),
    (
        "TAGame.Default__RumblePickups_TA",
        "TAGame.RumblePickups_TA",
    ),
    (
        "TAGame.Default__ViralItemActor_TA",
        "TAGame.ViralItemActor_TA",
    ),
    (
        "TAGame.ProductAttribute_Painted_TA",
        "TAGame.ProductAttribute_TA",
    ),
    ("TAGame.ProductAttribute_TA", "Core.Object"),
    (
        "TAGame.ProductAttribute_TeamEdition_TA",
        "TAGame.ProductAttribute_TA",
    ),
    (
        "TAGame.ProductAttribute_TitleID_TA",
        "TAGame.ProductAttribute_TA",
    ),
    (
        "TAGame.ProductAttribute_UserColor_TA",
        "TAGame.ProductAttribute_TA",
    ),
    (
        "TheWorld:PersistentLevel.CrowdActor_TA",
        "TAGame.CrowdActor_TA",
    ),
    (
        "TheWorld:PersistentLevel.CrowdManager_TA",
        "TAGame.CrowdManager_TA",
    ),
    (
        "TheWorld:PersistentLevel.InMapScoreboard_TA",
        "TAGame.InMapScoreboard_TA",
    ),
    (
        "TheWorld:PersistentLevel.VehiclePickup_Boost_TA",
        "TAGame.VehiclePickup_Boost_TA",
    ),
];

const PINNED_NETWORK_SPAWN_STATS_V1: [(&str, ReplayNetworkSpawnTrajectoryV1); 11] = [
    ("Engine.Actor", ReplayNetworkSpawnTrajectoryV1::Location),
    ("Engine.ZoneInfo", ReplayNetworkSpawnTrajectoryV1::None),
    (
        "TAGame.BreakOutActor_Platform_TA",
        ReplayNetworkSpawnTrajectoryV1::None,
    ),
    ("TAGame.CrowdActor_TA", ReplayNetworkSpawnTrajectoryV1::None),
    (
        "TAGame.CrowdManager_TA",
        ReplayNetworkSpawnTrajectoryV1::None,
    ),
    (
        "TAGame.HauntedBallTrapTrigger_TA",
        ReplayNetworkSpawnTrajectoryV1::None,
    ),
    (
        "TAGame.InMapScoreboard_TA",
        ReplayNetworkSpawnTrajectoryV1::None,
    ),
    (
        "TAGame.PlayerStart_Platform_TA",
        ReplayNetworkSpawnTrajectoryV1::None,
    ),
    (
        "TAGame.RBActor_TA",
        ReplayNetworkSpawnTrajectoryV1::LocationAndRotation,
    ),
    (
        "TAGame.VehiclePickup_Boost_TA",
        ReplayNetworkSpawnTrajectoryV1::None,
    ),
    (
        "TAGame.KeepUpIndicator_TA",
        ReplayNetworkSpawnTrajectoryV1::LocationAndRotation,
    ),
];

const NETWORK_INSTANCE_NORMALIZATION_KINDS_V1: [&str; 6] = [
    "CrowdActor_TA",
    "CrowdManager_TA",
    "VehiclePickup_Boost_TA",
    "InMapScoreboard_TA",
    "BreakOutActor_Platform_TA",
    "PlayerStart_Platform_TA",
];

const RL_223_BUILD_VERSION_THRESHOLD_V1: &str = "221120.42953.406184";

pub fn replay_network_attribute_tag_v1(name: &str) -> ReplayNetworkAttributeTagV1 {
    OBSERVED_NETWORK_ATTRIBUTE_TAGS_V1
        .iter()
        .find_map(|(candidate, tag)| (*candidate == name).then_some(*tag))
        .unwrap_or(ReplayNetworkAttributeTagV1::NotImplemented)
}

pub fn replay_network_object_name_v1(name: &str) -> String {
    const PERSISTENT_LEVEL_PREFIX: &str = "TheWorld:PersistentLevel.";

    let persistent_tail = if let Some(rest) = name.strip_prefix(PERSISTENT_LEVEL_PREFIX) {
        Some(rest)
    } else if let Some((_, suffix)) = name.split_once('.') {
        suffix.strip_prefix(PERSISTENT_LEVEL_PREFIX)
    } else {
        None
    };

    if let Some(rest) = persistent_tail {
        for kind in NETWORK_INSTANCE_NORMALIZATION_KINDS_V1 {
            if rest.starts_with(kind) {
                return format!("{PERSISTENT_LEVEL_PREFIX}{kind}");
            }
        }
    }

    name.to_string()
}

pub fn replay_network_parent_class_v1(name: &str) -> Option<&'static str> {
    let normalized = replay_network_object_name_v1(name);
    OBSERVED_NETWORK_PARENT_CLASSES_V1
        .iter()
        .find_map(|(child, parent)| (*child == normalized.as_str()).then_some(*parent))
}

pub fn replay_network_spawn_trajectory_class_v1(
    class_name: &str,
) -> Option<ReplayNetworkSpawnTrajectoryV1> {
    PINNED_NETWORK_SPAWN_STATS_V1
        .iter()
        .find_map(|(candidate, trajectory)| (*candidate == class_name).then_some(*trajectory))
}

pub fn replay_network_qword_string_uses_text_v1(build_version: &str) -> bool {
    build_version >= RL_223_BUILD_VERSION_THRESHOLD_V1
}

/// One inherited network property available to an actor class in the admitted lookup plan.
///
/// The tag may be `NotImplemented`. That is an explicit fail-closed decoder boundary, not
/// permission to consume an unknown payload.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct ReplayNetworkResolvedPropertyV1 {
    pub stream_id: u32,
    pub object_index: u32,
    pub tag: ReplayNetworkAttributeTagV1,
}

/// Effective inherited property lookup for one replay object index.
///
/// `max_prop_id` is the exclusive upper bound used by Rocket League's bounded integer decoder.
/// `prop_id_bits` is the corresponding precomputed bit width parameter. This type does not read
/// network payload bits.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct ReplayNetworkObjectLookupV1 {
    pub object_index: u32,
    pub max_prop_id: u32,
    pub prop_id_bits: u8,
    pub properties: Vec<ReplayNetworkResolvedPropertyV1>,
}

/// Static network-decoder lookup plan derived entirely from admitted header/footer structure.
///
/// The plan deliberately stops before actor/frame bits. `object_lookups[index] == None` preserves
/// the upstream `MissingCache` distinction for object names that do not participate in the
/// admitted inheritance surface. Spawn trajectories are kept as a separate object-index table
/// because spawn semantics and cache availability are independent.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub struct ReplayNetworkLookupPlanV1 {
    pub header: ReplayHeader,
    pub footer_lookup: ReplayFooterLookupMaterializationV1,
    pub num_frames: u32,
    pub max_channels: u32,
    pub channel_bits: u8,
    pub is_lan: bool,
    pub qword_string_uses_text: bool,
    pub spawn_trajectories: Vec<ReplayNetworkSpawnTrajectoryV1>,
    pub object_lookups: Vec<Option<ReplayNetworkObjectLookupV1>>,
}

pub trait ReplayNetworkLookupPlanReader {
    fn read_network_lookup_plan(&self, input: &ReplayInput) -> Result<ReplayNetworkLookupPlanV1>;
}

#[derive(Debug, Default, Clone, Copy)]
pub struct MinimalReplayNetworkLookupPlanReader;

impl ReplayNetworkLookupPlanReader for MinimalReplayNetworkLookupPlanReader {
    fn read_network_lookup_plan(&self, input: &ReplayInput) -> Result<ReplayNetworkLookupPlanV1> {
        match input {
            ReplayInput::Memory { label, bytes } => {
                parse_replay_network_lookup_plan_from_memory(label, bytes)
            }
            ReplayInput::File(path) => Err(network_lookup_plan_error(
                "unsupported-input",
                format!(
                    "ReplayInput::File is outside the network lookup-plan reader: {}",
                    path.display()
                ),
            )),
        }
    }
}

/// Native existing-actor first-property envelope header admitted by R3.16A.
///
/// This result stops exactly at the selected property's payload boundary. It never decodes or
/// consumes the attribute payload, never iterates to a second property, and never mutates actor
/// state. `payload_start_bit` is present only when `property_present == true` and resolution
/// succeeds.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct ReplayNetworkExistingActorFirstPropertyHeaderV1 {
    pub actor_object_index: u32,
    pub property_present: bool,
    pub property_present_start_bit: u64,
    pub property_present_end_bit: u64,
    pub stream_id: Option<u32>,
    pub stream_id_bound: Option<u32>,
    pub prop_id_bits: Option<u8>,
    pub stream_id_start_bit: Option<u64>,
    pub stream_id_end_bit: Option<u64>,
    pub resolved_property_object_index: Option<u32>,
    pub resolved_property_object_name: Option<String>,
    pub resolved_attribute_tag: Option<ReplayNetworkAttributeTagV1>,
    pub payload_start_bit: Option<u64>,
    pub stop_bit: u64,
}

/// Decode exactly one existing-actor property envelope header from an already admitted cursor.
///
/// `property_start_bit` must identify the first property-present bit after an alive existing
/// actor (`new == false`). The caller supplies the already materialized static/inherited lookup
/// plan. This function consumes no attribute payload bits and performs no actor/frame iteration.
pub fn decode_replay_network_existing_actor_first_property_header_v1(
    network_bytes: &[u8],
    property_start_bit: u64,
    actor_object_index: u32,
    lookup_plan: &ReplayNetworkLookupPlanV1,
) -> Result<ReplayNetworkExistingActorFirstPropertyHeaderV1> {
    let start = usize::try_from(property_start_bit).map_err(|_| {
        network_existing_actor_property_error(
            "invalid-position",
            format!("property start bit {property_start_bit} does not fit usize"),
        )
    })?;
    let total_bits = network_bytes.len().checked_mul(8).ok_or_else(|| {
        network_existing_actor_property_error(
            "invalid-length",
            "network bit length overflows usize",
        )
    })?;
    if start > total_bits {
        return Err(network_existing_actor_property_error(
            "invalid-position",
            format!(
                "property start bit {property_start_bit} exceeds network bit length {total_bits}"
            ),
        ));
    }

    let mut cursor = NetworkBitCursor::new(network_bytes);
    cursor.bit_position = start;

    let property_present_start_bit = network_position_to_u64(cursor.position_bits())?;
    let property_present = cursor.read_bit()?;
    let property_present_end_bit = network_position_to_u64(cursor.position_bits())?;

    if !property_present {
        return Ok(ReplayNetworkExistingActorFirstPropertyHeaderV1 {
            actor_object_index,
            property_present,
            property_present_start_bit,
            property_present_end_bit,
            stream_id: None,
            stream_id_bound: None,
            prop_id_bits: None,
            stream_id_start_bit: None,
            stream_id_end_bit: None,
            resolved_property_object_index: None,
            resolved_property_object_name: None,
            resolved_attribute_tag: None,
            payload_start_bit: None,
            stop_bit: property_present_end_bit,
        });
    }

    let actor_slot = usize::try_from(actor_object_index).map_err(|_| {
        network_existing_actor_property_error(
            "invalid-actor-object",
            format!("actor object index {actor_object_index} does not fit usize"),
        )
    })?;
    let object_lookup = lookup_plan
        .object_lookups
        .get(actor_slot)
        .and_then(Option::as_ref)
        .ok_or_else(|| {
            network_existing_actor_property_error(
                "missing-actor-lookup",
                format!("no admitted object lookup for actor object {actor_object_index}"),
            )
        })?;
    if object_lookup.object_index != actor_object_index {
        return Err(network_existing_actor_property_error(
            "actor-lookup-identity-mismatch",
            format!(
                "actor object {actor_object_index} resolved to lookup object {}",
                object_lookup.object_index
            ),
        ));
    }

    let stream_id_start_bit = network_position_to_u64(cursor.position_bits())?;
    let stream_id =
        cursor.read_bounded_u32(object_lookup.max_prop_id, object_lookup.prop_id_bits)?;
    let stream_id_end_bit = network_position_to_u64(cursor.position_bits())?;

    let property = object_lookup
        .properties
        .iter()
        .find(|property| property.stream_id == stream_id)
        .ok_or_else(|| {
            network_existing_actor_property_error(
                "unresolved-stream-id",
                format!(
                    "stream id {stream_id} is not resolved for actor object {actor_object_index}"
                ),
            )
        })?;
    let property_slot = usize::try_from(property.object_index).map_err(|_| {
        network_existing_actor_property_error(
            "invalid-property-object",
            format!(
                "property object index {} does not fit usize",
                property.object_index
            ),
        )
    })?;
    let property_name = lookup_plan
        .footer_lookup
        .objects
        .get(property_slot)
        .cloned()
        .ok_or_else(|| {
            network_existing_actor_property_error(
                "invalid-property-object",
                format!(
                    "property object index {} is outside object table length {}",
                    property.object_index,
                    lookup_plan.footer_lookup.objects.len()
                ),
            )
        })?;

    Ok(ReplayNetworkExistingActorFirstPropertyHeaderV1 {
        actor_object_index,
        property_present,
        property_present_start_bit,
        property_present_end_bit,
        stream_id: Some(stream_id),
        stream_id_bound: Some(object_lookup.max_prop_id),
        prop_id_bits: Some(object_lookup.prop_id_bits),
        stream_id_start_bit: Some(stream_id_start_bit),
        stream_id_end_bit: Some(stream_id_end_bit),
        resolved_property_object_index: Some(property.object_index),
        resolved_property_object_name: Some(property_name),
        resolved_attribute_tag: Some(property.tag),
        payload_start_bit: Some(stream_id_end_bit),
        stop_bit: stream_id_end_bit,
    })
}

/// One R3.17B-admitted primitive scalar attribute value.
///
/// Float identity preserves both the exact raw IEEE-754 bit pattern and its `f32`
/// interpretation. Equality is bit-exact for Float so NaN payloads and signed zero
/// remain deterministic evidence identities.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum ReplayNetworkPrimitiveScalarValueV1 {
    Boolean(bool),
    Byte(u8),
    Enum(u16),
    Float { raw_bits: u32, value: f32 },
    Int(i32),
    Int64(i64),
}

impl PartialEq for ReplayNetworkPrimitiveScalarValueV1 {
    fn eq(&self, other: &Self) -> bool {
        match (self, other) {
            (Self::Boolean(left), Self::Boolean(right)) => left == right,
            (Self::Byte(left), Self::Byte(right)) => left == right,
            (Self::Enum(left), Self::Enum(right)) => left == right,
            (
                Self::Float {
                    raw_bits: left_raw,
                    value: left_value,
                },
                Self::Float {
                    raw_bits: right_raw,
                    value: right_value,
                },
            ) => left_raw == right_raw && left_value.to_bits() == right_value.to_bits(),
            (Self::Int(left), Self::Int(right)) => left == right,
            (Self::Int64(left), Self::Int64(right)) => left == right,
            _ => false,
        }
    }
}

impl Eq for ReplayNetworkPrimitiveScalarValueV1 {}

/// Exact result of decoding one admitted primitive scalar payload.
/// Caller-resolved context for one evidence-admitted K2 payload decode.
#[derive(Debug, Clone, Copy, Serialize, Deserialize, PartialEq, Eq)]
pub struct ReplayNetworkK2DecodeContextV1 {
    pub net_version: i32,
    pub is_rl_223: bool,
}

/// Wire encoding identity retained for an admitted length-prefixed network string.
#[derive(Debug, Clone, Copy, Serialize, Deserialize, PartialEq, Eq)]
#[serde(rename_all = "snake_case")]
pub enum ReplayNetworkTextEncodingV1 {
    Empty,
    Windows1252,
    Utf16Le,
}

/// One decoded network text value plus the signed length that selected its wire branch.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct ReplayNetworkTextV1 {
    pub value: String,
    pub declared_length: i32,
    pub encoding: ReplayNetworkTextEncodingV1,
}

/// Evidence-admitted remote identity variants for one direct K2 value.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub enum ReplayNetworkUniqueIdRemoteV1 {
    Steam {
        online_id: u64,
    },
    PlayStation {
        name: String,
        unknown: Vec<u8>,
        online_id: u64,
    },
    PsyNet {
        online_id: u64,
    },
    Epic {
        account_id: ReplayNetworkTextV1,
    },
}

/// One evidence-admitted network unique id.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct ReplayNetworkUniqueIdV1 {
    pub system_id: u8,
    pub remote_id: ReplayNetworkUniqueIdRemoteV1,
    pub local_id: u8,
}

/// Semantic value returned by the direct one-value K2 decoder.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub enum ReplayNetworkK2ValueV1 {
    ActiveActor { active: bool, actor: i32 },
    String(ReplayNetworkTextV1),
    QWordStringQWord(u64),
    QWordStringText(ReplayNetworkTextV1),
    UniqueId(ReplayNetworkUniqueIdV1),
    PartyLeader(ReplayNetworkUniqueIdV1),
}

/// Exactly one already-resolved evidence-admitted K2 payload decode.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct ReplayNetworkK2DecodeV1 {
    pub attribute_tag: ReplayNetworkAttributeTagV1,
    pub payload_start_bit: u64,
    pub payload_end_bit: u64,
    pub payload_width: u64,
    pub value: ReplayNetworkK2ValueV1,
}

fn network_k2_reset_cursor(cursor: &mut NetworkBitCursor<'_>, start: usize) {
    cursor.bit_position = start;
    debug_assert_eq!(cursor.position_bits(), start);
}

fn replay_network_k2_error(category: &str, detail: impl Into<String>) -> MimirError {
    MimirError::message(format!(
        "replay network k2 error: {category}: {}",
        detail.into()
    ))
}

fn network_k2_read_u8(cursor: &mut NetworkBitCursor<'_>) -> Result<u8> {
    cursor.read_bits_le(8).map(|value| value as u8)
}

fn network_k2_read_u64(cursor: &mut NetworkBitCursor<'_>) -> Result<u64> {
    cursor.read_bits_le(64)
}

fn network_k2_read_bytes(cursor: &mut NetworkBitCursor<'_>, count: usize) -> Result<Vec<u8>> {
    let required_bits = count.checked_mul(8).ok_or_else(|| {
        replay_network_k2_error("invalid-text-length", "byte length overflows bit width")
    })?;
    if cursor.remaining_bits() < required_bits {
        return Err(replay_network_k2_error(
            "insufficient-bits",
            format!(
                "need {required_bits} content bits at position {}, but only {} remain",
                cursor.position_bits(),
                cursor.remaining_bits()
            ),
        ));
    }

    let mut output = Vec::new();
    output.try_reserve_exact(count).map_err(|_| {
        replay_network_k2_error(
            "invalid-text-length",
            format!("unable to reserve {count} decoded bytes"),
        )
    })?;
    for _ in 0..count {
        output.push(network_k2_read_u8(cursor)?);
    }
    Ok(output)
}

fn decode_network_windows1252(bytes: &[u8]) -> String {
    let mut output = String::with_capacity(bytes.len());
    for byte in bytes {
        let character = match *byte {
            0x80 => '\u{20ac}',
            0x81 => '\u{0081}',
            0x82 => '\u{201a}',
            0x83 => '\u{0192}',
            0x84 => '\u{201e}',
            0x85 => '\u{2026}',
            0x86 => '\u{2020}',
            0x87 => '\u{2021}',
            0x88 => '\u{02c6}',
            0x89 => '\u{2030}',
            0x8a => '\u{0160}',
            0x8b => '\u{2039}',
            0x8c => '\u{0152}',
            0x8d => '\u{008d}',
            0x8e => '\u{017d}',
            0x8f => '\u{008f}',
            0x90 => '\u{0090}',
            0x91 => '\u{2018}',
            0x92 => '\u{2019}',
            0x93 => '\u{201c}',
            0x94 => '\u{201d}',
            0x95 => '\u{2022}',
            0x96 => '\u{2013}',
            0x97 => '\u{2014}',
            0x98 => '\u{02dc}',
            0x99 => '\u{2122}',
            0x9a => '\u{0161}',
            0x9b => '\u{203a}',
            0x9c => '\u{0153}',
            0x9d => '\u{009d}',
            0x9e => '\u{017e}',
            0x9f => '\u{0178}',
            value => char::from_u32(u32::from(value)).expect("u8 is always a Unicode scalar"),
        };
        output.push(character);
    }
    output
}

fn decode_network_text_v1(cursor: &mut NetworkBitCursor<'_>) -> Result<ReplayNetworkTextV1> {
    let declared_length = cursor.read_bits_le(32)? as u32 as i32;
    if declared_length == 0 {
        return Ok(ReplayNetworkTextV1 {
            value: String::new(),
            declared_length,
            encoding: ReplayNetworkTextEncodingV1::Empty,
        });
    }

    if declared_length > 0 {
        let byte_count = usize::try_from(declared_length).map_err(|_| {
            replay_network_k2_error(
                "invalid-text-length",
                format!("positive text length {declared_length} does not fit usize"),
            )
        })?;
        let bytes = network_k2_read_bytes(cursor, byte_count)?;
        let content = &bytes[..byte_count - 1];
        return Ok(ReplayNetworkTextV1 {
            value: decode_network_windows1252(content),
            declared_length,
            encoding: ReplayNetworkTextEncodingV1::Windows1252,
        });
    }

    if declared_length == i32::MIN {
        return Err(replay_network_k2_error(
            "invalid-text-length",
            "i32::MIN cannot be negated for UTF-16 byte length",
        ));
    }

    let code_unit_count = usize::try_from(-declared_length).map_err(|_| {
        replay_network_k2_error(
            "invalid-text-length",
            format!("UTF-16 code-unit length {declared_length} does not fit usize"),
        )
    })?;
    let byte_count = code_unit_count.checked_mul(2).ok_or_else(|| {
        replay_network_k2_error(
            "invalid-text-length",
            format!("UTF-16 byte length overflows for {declared_length}"),
        )
    })?;
    let bytes = network_k2_read_bytes(cursor, byte_count)?;
    let content = &bytes[..byte_count - 2];
    let mut units = Vec::new();
    units.try_reserve_exact(content.len() / 2).map_err(|_| {
        replay_network_k2_error(
            "invalid-text-length",
            format!("unable to reserve {} UTF-16 code units", content.len() / 2),
        )
    })?;
    for chunk in content.chunks_exact(2) {
        units.push(u16::from_le_bytes([chunk[0], chunk[1]]));
    }

    Ok(ReplayNetworkTextV1 {
        value: String::from_utf16_lossy(&units),
        declared_length,
        encoding: ReplayNetworkTextEncodingV1::Utf16Le,
    })
}

fn decode_network_unique_id_v1(
    cursor: &mut NetworkBitCursor<'_>,
    context: ReplayNetworkK2DecodeContextV1,
) -> Result<ReplayNetworkUniqueIdV1> {
    if context.net_version != 10 {
        return Err(replay_network_k2_error(
            "unadmitted-context",
            format!(
                "UniqueId requires net_version 10, got {}",
                context.net_version
            ),
        ));
    }

    let system_id = network_k2_read_u8(cursor)?;
    let remote_id = match system_id {
        1 => ReplayNetworkUniqueIdRemoteV1::Steam {
            online_id: network_k2_read_u64(cursor)?,
        },
        2 => {
            if !context.is_rl_223 {
                return Err(replay_network_k2_error(
                    "unadmitted-context",
                    "PlayStation UniqueId was observed only in RL223 context",
                ));
            }
            let name_bytes = network_k2_read_bytes(cursor, 16)?;
            let name_end = name_bytes
                .iter()
                .position(|byte| *byte == 0)
                .unwrap_or(name_bytes.len());
            let name = decode_network_windows1252(&name_bytes[..name_end]);
            let unknown = network_k2_read_bytes(cursor, 16)?;
            let online_id = network_k2_read_u64(cursor)?;
            ReplayNetworkUniqueIdRemoteV1::PlayStation {
                name,
                unknown,
                online_id,
            }
        }
        7 => {
            if !context.is_rl_223 {
                return Err(replay_network_k2_error(
                    "unadmitted-context",
                    "PsyNet UniqueId was observed only in RL223 context",
                ));
            }
            ReplayNetworkUniqueIdRemoteV1::PsyNet {
                online_id: network_k2_read_u64(cursor)?,
            }
        }
        11 => {
            let account_id = decode_network_text_v1(cursor)?;
            if account_id.encoding != ReplayNetworkTextEncodingV1::Windows1252
                || account_id.declared_length != 33
            {
                return Err(replay_network_k2_error(
                    "unadmitted-k2-shape",
                    format!(
                        "Epic UniqueId requires Windows-1252 declared length 33, got {:?} / {}",
                        account_id.encoding, account_id.declared_length
                    ),
                ));
            }
            ReplayNetworkUniqueIdRemoteV1::Epic { account_id }
        }
        value => {
            return Err(replay_network_k2_error(
                "unadmitted-k2-shape",
                format!("UniqueId system id {value} is not admitted by R3.17F"),
            ));
        }
    };
    let local_id = network_k2_read_u8(cursor)?;
    Ok(ReplayNetworkUniqueIdV1 {
        system_id,
        remote_id,
        local_id,
    })
}

/// Decode exactly one already-resolved R3.17F-admitted K2 payload.
///
/// This API is intentionally stateless: it receives the exact payload start and returns
/// the first bit after one K2 value. It does not continue a property loop or mutate actor state.
pub fn decode_replay_network_k2_v1(
    network_bytes: &[u8],
    payload_start_bit: u64,
    attribute_tag: ReplayNetworkAttributeTagV1,
    context: ReplayNetworkK2DecodeContextV1,
) -> Result<ReplayNetworkK2DecodeV1> {
    let total_bits = network_bytes.len().checked_mul(8).ok_or_else(|| {
        replay_network_k2_error("invalid-start", "network bit length overflows usize")
    })?;
    let total_bits_u64 = u64::try_from(total_bits).map_err(|_| {
        replay_network_k2_error("invalid-start", "network bit length does not fit u64")
    })?;
    if payload_start_bit > total_bits_u64 {
        return Err(replay_network_k2_error(
            "invalid-start",
            format!(
                "payload start {payload_start_bit} exceeds network length {total_bits_u64} bits"
            ),
        ));
    }
    let start = usize::try_from(payload_start_bit).map_err(|_| {
        replay_network_k2_error(
            "invalid-start",
            format!("payload start {payload_start_bit} does not fit usize"),
        )
    })?;

    let mut cursor = NetworkBitCursor::new(network_bytes);
    network_k2_reset_cursor(&mut cursor, start);
    let decoded = (|| -> Result<ReplayNetworkK2ValueV1> {
        match attribute_tag {
            ReplayNetworkAttributeTagV1::ActiveActor => {
                let active = cursor.read_bit()?;
                let actor = cursor.read_bits_le(32)? as u32 as i32;
                Ok(ReplayNetworkK2ValueV1::ActiveActor { active, actor })
            }
            ReplayNetworkAttributeTagV1::String => {
                decode_network_text_v1(&mut cursor).map(ReplayNetworkK2ValueV1::String)
            }
            ReplayNetworkAttributeTagV1::QWordString => {
                if context.is_rl_223 {
                    let value = decode_network_text_v1(&mut cursor)?;
                    if value.encoding != ReplayNetworkTextEncodingV1::Windows1252
                        || value.declared_length <= 0
                    {
                        return Err(replay_network_k2_error(
                            "unadmitted-k2-shape",
                            format!(
                                "RL223 QWordString requires positive Windows-1252 text, got {:?} / {}",
                                value.encoding, value.declared_length
                            ),
                        ));
                    }
                    Ok(ReplayNetworkK2ValueV1::QWordStringText(value))
                } else {
                    network_k2_read_u64(&mut cursor).map(ReplayNetworkK2ValueV1::QWordStringQWord)
                }
            }
            ReplayNetworkAttributeTagV1::UniqueId => {
                decode_network_unique_id_v1(&mut cursor, context)
                    .map(ReplayNetworkK2ValueV1::UniqueId)
            }
            ReplayNetworkAttributeTagV1::PartyLeader => {
                if context.net_version != 10 || !context.is_rl_223 {
                    return Err(replay_network_k2_error(
                        "unadmitted-context",
                        format!(
                            "PartyLeader requires net_version 10 and RL223 context, got {} / {}",
                            context.net_version, context.is_rl_223
                        ),
                    ));
                }
                let unique = decode_network_unique_id_v1(&mut cursor, context)?;
                if !matches!(unique.remote_id, ReplayNetworkUniqueIdRemoteV1::Epic { .. }) {
                    return Err(replay_network_k2_error(
                        "unadmitted-k2-shape",
                        "PartyLeader admits only Some(Epic declared=33)",
                    ));
                }
                Ok(ReplayNetworkK2ValueV1::PartyLeader(unique))
            }
            _ => Err(replay_network_k2_error(
                "unsupported-k2-tag",
                format!("attribute tag {attribute_tag:?} is not an admitted K2 tag"),
            )),
        }
    })();

    let value = match decoded {
        Ok(value) => value,
        Err(error) => {
            network_k2_reset_cursor(&mut cursor, start);
            return Err(error);
        }
    };
    let payload_end_bit = u64::try_from(cursor.position_bits()).map_err(|_| {
        network_k2_reset_cursor(&mut cursor, start);
        replay_network_k2_error("invalid-start", "decoded end bit does not fit u64")
    })?;
    let payload_width = payload_end_bit
        .checked_sub(payload_start_bit)
        .ok_or_else(|| {
            network_k2_reset_cursor(&mut cursor, start);
            replay_network_k2_error("invalid-start", "decoded end bit precedes payload start")
        })?;

    Ok(ReplayNetworkK2DecodeV1 {
        attribute_tag,
        payload_start_bit,
        payload_end_bit,
        payload_width,
        value,
    })
}

/// Caller-resolved context for one R3.17J-admitted K3 payload decode.
#[derive(Debug, Clone, Copy, Serialize, Deserialize, PartialEq, Eq)]
pub struct ReplayNetworkK3DecodeContextV1 {
    pub version_major: i32,
    pub version_minor: i32,
    pub net_version: i32,
    pub is_rl_223: bool,
}

/// One decoded net10 vector plus exact structural codec metadata.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub struct ReplayNetworkVector3V1 {
    pub selected_size_bits: u8,
    pub component_width: u8,
    pub raw_x: u32,
    pub raw_y: u32,
    pub raw_z: u32,
    pub x: f32,
    pub y: f32,
    pub z: f32,
}

/// One exact 56-bit quaternion decode used by the admitted net10 RigidBody lane.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub struct ReplayNetworkQuaternion56V1 {
    pub largest: u8,
    pub raw_a: u32,
    pub raw_b: u32,
    pub raw_c: u32,
    pub x: f32,
    pub y: f32,
    pub z: f32,
    pub w: f32,
}

/// One evidence-admitted RigidBody value.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub struct ReplayNetworkRigidBodyV1 {
    pub sleeping: bool,
    pub location: ReplayNetworkVector3V1,
    pub rotation: ReplayNetworkQuaternion56V1,
    pub linear_velocity: Option<ReplayNetworkVector3V1>,
    pub angular_velocity: Option<ReplayNetworkVector3V1>,
}

/// One evidence-admitted ReplicatedBoost value.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct ReplayNetworkReplicatedBoostV1 {
    pub grant_count: u8,
    pub boost_amount: u8,
    pub unused1: u8,
    pub unused2: u8,
}

/// One evidence-admitted PickupNew value.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct ReplayNetworkPickupNewV1 {
    pub instigator: Option<i32>,
    pub picked_up: u8,
}

/// Semantic value returned by the direct one-value K3 decoder.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub enum ReplayNetworkK3ValueV1 {
    Location(ReplayNetworkVector3V1),
    RigidBody(ReplayNetworkRigidBodyV1),
    ReplicatedBoost(ReplayNetworkReplicatedBoostV1),
    PickupNew(ReplayNetworkPickupNewV1),
}

/// Exactly one already-resolved evidence-admitted K3 payload decode.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub struct ReplayNetworkK3DecodeV1 {
    pub attribute_tag: ReplayNetworkAttributeTagV1,
    pub payload_start_bit: u64,
    pub payload_end_bit: u64,
    pub payload_width: u64,
    pub value: ReplayNetworkK3ValueV1,
}

fn replay_network_k3_error(category: &str, detail: impl Into<String>) -> MimirError {
    MimirError::message(format!(
        "replay network k3 error: {category}: {}",
        detail.into()
    ))
}

fn network_k3_reset_cursor(cursor: &mut NetworkBitCursor<'_>, start: usize) {
    cursor.bit_position = start;
    debug_assert_eq!(cursor.position_bits(), start);
}

fn network_k3_read_bits(cursor: &mut NetworkBitCursor<'_>, width: usize) -> Result<u64> {
    if cursor.remaining_bits() < width {
        return Err(replay_network_k3_error(
            "insufficient-bits",
            format!(
                "need {width} bits at position {}, but only {} remain",
                cursor.position_bits(),
                cursor.remaining_bits()
            ),
        ));
    }
    cursor.read_bits_le(width).map_err(|error| {
        replay_network_k3_error(
            "insufficient-bits",
            format!("bounded K3 bit read failed unexpectedly: {error}"),
        )
    })
}

fn validate_network_k3_context(context: ReplayNetworkK3DecodeContextV1) -> Result<()> {
    if context.version_major != 868 || context.version_minor != 32 || context.net_version != 10 {
        return Err(replay_network_k3_error(
            "unadmitted-context",
            format!(
                "K3 requires replay version 868.32 / net10, got {}.{} / net{}",
                context.version_major, context.version_minor, context.net_version
            ),
        ));
    }
    Ok(())
}

fn decode_network_vector3_v1(cursor: &mut NetworkBitCursor<'_>) -> Result<ReplayNetworkVector3V1> {
    let low = network_k3_read_bits(cursor, 4)? as u8;
    let candidate = low.checked_add(16).ok_or_else(|| {
        replay_network_k3_error("invalid-k3-value", "vector size candidate overflows u8")
    })?;
    let selected_size_bits = if candidate < 22 {
        if network_k3_read_bits(cursor, 1)? != 0 {
            candidate
        } else {
            low
        }
    } else {
        low
    };

    if selected_size_bits >= 20 {
        return Err(replay_network_k3_error(
            "unadmitted-k3-shape",
            format!("vector selected size {selected_size_bits} is not admitted"),
        ));
    }

    let component_width = selected_size_bits.checked_add(2).ok_or_else(|| {
        replay_network_k3_error("invalid-k3-value", "vector component width overflows u8")
    })?;
    let bias_shift = selected_size_bits.checked_add(1).ok_or_else(|| {
        replay_network_k3_error("invalid-k3-value", "vector bias shift overflows u8")
    })?;
    let bias = 1u64.checked_shl(u32::from(bias_shift)).ok_or_else(|| {
        replay_network_k3_error("invalid-k3-value", "vector bias shift exceeds u64")
    })?;
    let width = usize::from(component_width);
    let raw_x = network_k3_read_bits(cursor, width)?;
    let raw_y = network_k3_read_bits(cursor, width)?;
    let raw_z = network_k3_read_bits(cursor, width)?;

    let to_semantic = |raw: u64| -> Result<f32> {
        let signed = i64::try_from(raw)
            .map_err(|_| replay_network_k3_error("invalid-k3-value", "vector raw exceeds i64"))?
            .checked_sub(i64::try_from(bias).map_err(|_| {
                replay_network_k3_error("invalid-k3-value", "vector bias exceeds i64")
            })?)
            .ok_or_else(|| {
                replay_network_k3_error("invalid-k3-value", "vector signed subtraction overflow")
            })?;
        Ok((signed as f32) / 100.0)
    };

    Ok(ReplayNetworkVector3V1 {
        selected_size_bits,
        component_width,
        raw_x: u32::try_from(raw_x).map_err(|_| {
            replay_network_k3_error("invalid-k3-value", "vector x raw does not fit u32")
        })?,
        raw_y: u32::try_from(raw_y).map_err(|_| {
            replay_network_k3_error("invalid-k3-value", "vector y raw does not fit u32")
        })?,
        raw_z: u32::try_from(raw_z).map_err(|_| {
            replay_network_k3_error("invalid-k3-value", "vector z raw does not fit u32")
        })?,
        x: to_semantic(raw_x)?,
        y: to_semantic(raw_y)?,
        z: to_semantic(raw_z)?,
    })
}

fn decode_network_quaternion56_v1(
    cursor: &mut NetworkBitCursor<'_>,
) -> Result<ReplayNetworkQuaternion56V1> {
    let largest = network_k3_read_bits(cursor, 2)? as u8;
    let raw_a = network_k3_read_bits(cursor, 18)? as u32;
    let raw_b = network_k3_read_bits(cursor, 18)? as u32;
    let raw_c = network_k3_read_bits(cursor, 18)? as u32;

    let unpack = |raw: u32| -> f32 {
        let pos_range = (raw as f32) / 262_143.0_f32;
        let range = (pos_range - 0.5_f32) * 2.0_f32;
        range * std::f32::consts::FRAC_1_SQRT_2
    };
    let a = unpack(raw_a);
    let b = unpack(raw_b);
    let c = unpack(raw_c);
    if !a.is_finite() || !b.is_finite() || !c.is_finite() {
        return Err(replay_network_k3_error(
            "invalid-k3-value",
            "quaternion unpack produced a non-finite component",
        ));
    }

    let radicand = 1.0_f32 - a * a - b * b - c * c;
    if !radicand.is_finite() || radicand < 0.0 {
        return Err(replay_network_k3_error(
            "invalid-k3-value",
            format!("quaternion reconstruction radicand is invalid: {radicand}"),
        ));
    }
    let extra = radicand.sqrt();
    let (x, y, z, w) = match largest {
        0 => (extra, a, b, c),
        1 => (a, extra, b, c),
        2 => (a, b, extra, c),
        3 => (a, b, c, extra),
        _ => unreachable!("two bits cannot decode outside 0..=3"),
    };
    if !x.is_finite() || !y.is_finite() || !z.is_finite() || !w.is_finite() {
        return Err(replay_network_k3_error(
            "invalid-k3-value",
            "quaternion reconstruction produced a non-finite component",
        ));
    }

    Ok(ReplayNetworkQuaternion56V1 {
        largest,
        raw_a,
        raw_b,
        raw_c,
        x,
        y,
        z,
        w,
    })
}

fn network_k3_location_code(context: ReplayNetworkK3DecodeContextV1, size: u8) -> u32 {
    ((context.is_rl_223 as u32) << 5) | u32::from(size)
}

fn network_k3_rigid_body_code(
    context: ReplayNetworkK3DecodeContextV1,
    sleeping: bool,
    location_size: u8,
    linear_size: Option<u8>,
    angular_size: Option<u8>,
) -> u32 {
    let linear = u32::from(linear_size.unwrap_or(31));
    let angular = u32::from(angular_size.unwrap_or(31));
    ((context.is_rl_223 as u32) << 16)
        | ((sleeping as u32) << 15)
        | (u32::from(location_size) << 10)
        | (linear << 5)
        | angular
}

fn network_k3_pickup_new_code(context: ReplayNetworkK3DecodeContextV1, some_i32: bool) -> u32 {
    ((context.is_rl_223 as u32) << 1) | (some_i32 as u32)
}

/// Decode exactly one already-resolved R3.17J-admitted K3 payload.
///
/// The decoder is intentionally stateless and one-value only. It never advances into a
/// second property, actor or frame. Every failure discards the partial value and resets
/// the internal cursor to the supplied payload start.
pub fn decode_replay_network_k3_v1(
    network_bytes: &[u8],
    payload_start_bit: u64,
    attribute_tag: ReplayNetworkAttributeTagV1,
    context: ReplayNetworkK3DecodeContextV1,
) -> Result<ReplayNetworkK3DecodeV1> {
    let total_bits = network_bytes.len().checked_mul(8).ok_or_else(|| {
        replay_network_k3_error("invalid-start", "network bit length overflows usize")
    })?;
    let total_bits_u64 = u64::try_from(total_bits).map_err(|_| {
        replay_network_k3_error("invalid-start", "network bit length does not fit u64")
    })?;
    if payload_start_bit > total_bits_u64 {
        return Err(replay_network_k3_error(
            "invalid-start",
            format!(
                "payload start {payload_start_bit} exceeds network length {total_bits_u64} bits"
            ),
        ));
    }
    let start = usize::try_from(payload_start_bit).map_err(|_| {
        replay_network_k3_error(
            "invalid-start",
            format!("payload start {payload_start_bit} does not fit usize"),
        )
    })?;
    validate_network_k3_context(context)?;

    let mut cursor = NetworkBitCursor::new(network_bytes);
    network_k3_reset_cursor(&mut cursor, start);
    let decoded = (|| -> Result<ReplayNetworkK3ValueV1> {
        match attribute_tag {
            ReplayNetworkAttributeTagV1::Location => {
                let value = decode_network_vector3_v1(&mut cursor)?;
                let code = network_k3_location_code(context, value.selected_size_bits);
                if !k3_admitted_groups::location_contains(code) {
                    return Err(replay_network_k3_error(
                        "unadmitted-k3-shape",
                        format!("Location structural code {code} is absent from R3.17J"),
                    ));
                }
                Ok(ReplayNetworkK3ValueV1::Location(value))
            }
            ReplayNetworkAttributeTagV1::RigidBody => {
                let sleeping = network_k3_read_bits(&mut cursor, 1)? != 0;
                let location = decode_network_vector3_v1(&mut cursor)?;
                let rotation = decode_network_quaternion56_v1(&mut cursor)?;
                let (linear_velocity, angular_velocity) = if sleeping {
                    (None, None)
                } else {
                    (
                        Some(decode_network_vector3_v1(&mut cursor)?),
                        Some(decode_network_vector3_v1(&mut cursor)?),
                    )
                };
                let code = network_k3_rigid_body_code(
                    context,
                    sleeping,
                    location.selected_size_bits,
                    linear_velocity
                        .as_ref()
                        .map(|value| value.selected_size_bits),
                    angular_velocity
                        .as_ref()
                        .map(|value| value.selected_size_bits),
                );
                if !k3_admitted_groups::rigid_body_contains(code) {
                    return Err(replay_network_k3_error(
                        "unadmitted-k3-shape",
                        format!("RigidBody structural code {code} is absent from R3.17J"),
                    ));
                }
                Ok(ReplayNetworkK3ValueV1::RigidBody(
                    ReplayNetworkRigidBodyV1 {
                        sleeping,
                        location,
                        rotation,
                        linear_velocity,
                        angular_velocity,
                    },
                ))
            }
            ReplayNetworkAttributeTagV1::ReplicatedBoost => {
                let code = context.is_rl_223 as u32;
                if !k3_admitted_groups::replicated_boost_contains(code) {
                    return Err(replay_network_k3_error(
                        "unadmitted-k3-shape",
                        format!("ReplicatedBoost structural code {code} is absent from R3.17J"),
                    ));
                }
                let grant_count = network_k3_read_bits(&mut cursor, 8)? as u8;
                let boost_amount = network_k3_read_bits(&mut cursor, 8)? as u8;
                let unused1 = network_k3_read_bits(&mut cursor, 8)? as u8;
                let unused2 = network_k3_read_bits(&mut cursor, 8)? as u8;
                Ok(ReplayNetworkK3ValueV1::ReplicatedBoost(
                    ReplayNetworkReplicatedBoostV1 {
                        grant_count,
                        boost_amount,
                        unused1,
                        unused2,
                    },
                ))
            }
            ReplayNetworkAttributeTagV1::PickupNew => {
                let some_i32 = network_k3_read_bits(&mut cursor, 1)? != 0;
                let instigator = if some_i32 {
                    Some(network_k3_read_bits(&mut cursor, 32)? as u32 as i32)
                } else {
                    None
                };
                let picked_up = network_k3_read_bits(&mut cursor, 8)? as u8;
                let code = network_k3_pickup_new_code(context, some_i32);
                if !k3_admitted_groups::pickup_new_contains(code) {
                    return Err(replay_network_k3_error(
                        "unadmitted-k3-shape",
                        format!("PickupNew structural code {code} is absent from R3.17J"),
                    ));
                }
                Ok(ReplayNetworkK3ValueV1::PickupNew(
                    ReplayNetworkPickupNewV1 {
                        instigator,
                        picked_up,
                    },
                ))
            }
            _ => Err(replay_network_k3_error(
                "unsupported-k3-tag",
                format!("attribute tag {attribute_tag:?} is not an admitted K3 tag"),
            )),
        }
    })();

    let value = match decoded {
        Ok(value) => value,
        Err(error) => {
            network_k3_reset_cursor(&mut cursor, start);
            return Err(error);
        }
    };
    let payload_end_bit = u64::try_from(cursor.position_bits()).map_err(|_| {
        network_k3_reset_cursor(&mut cursor, start);
        replay_network_k3_error("invalid-start", "decoded end bit does not fit u64")
    })?;
    let payload_width = payload_end_bit
        .checked_sub(payload_start_bit)
        .ok_or_else(|| {
            network_k3_reset_cursor(&mut cursor, start);
            replay_network_k3_error("invalid-start", "decoded end bit precedes payload start")
        })?;

    Ok(ReplayNetworkK3DecodeV1 {
        attribute_tag,
        payload_start_bit,
        payload_end_bit,
        payload_width,
        value,
    })
}

/// This result is deliberately one-value only. `stop_bit` is exactly the first bit
/// after the scalar and does not imply permission to read another property, actor,
/// frame, or compound/spatial attribute.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct ReplayNetworkPrimitiveScalarDecodeV1 {
    pub attribute_tag: ReplayNetworkAttributeTagV1,
    pub payload_start_bit: u64,
    pub payload_end_bit: u64,
    pub payload_width: u8,
    pub value: ReplayNetworkPrimitiveScalarValueV1,
    pub stop_bit: u64,
}

/// One complete existing-actor first property composed from the already-published
/// property-header boundary and primitive K1 scalar decoder.
///
/// This type is deliberately one-property only. `stop_bit` is exactly the first bit after the
/// primitive scalar payload. It does not authorize or consume the next `property_present` bit.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct ReplayNetworkExistingActorSinglePrimitivePropertyV1 {
    pub header: ReplayNetworkExistingActorFirstPropertyHeaderV1,
    pub scalar: ReplayNetworkPrimitiveScalarDecodeV1,
    pub stop_bit: u64,
}

/// Decode exactly one existing-actor property when its resolved tag is an admitted K1 scalar.
///
/// The existing R3.16B header decoder remains the sole authority for `property_present`, bounded
/// stream decoding, inherited lookup resolution, and `payload_start_bit`. The existing R3.17C
/// primitive scalar decoder remains the sole authority for Boolean/Byte/Enum/Float/Int/Int64 wire
/// decoding. This composition stops at the scalar end and never reads the next property bit.
pub fn decode_replay_network_existing_actor_single_primitive_property_v1(
    network_bytes: &[u8],
    property_start_bit: u64,
    actor_object_index: u32,
    lookup_plan: &ReplayNetworkLookupPlanV1,
) -> Result<ReplayNetworkExistingActorSinglePrimitivePropertyV1> {
    let header = decode_replay_network_existing_actor_first_property_header_v1(
        network_bytes,
        property_start_bit,
        actor_object_index,
        lookup_plan,
    )?;

    if !header.property_present {
        return Err(network_existing_actor_single_property_error(
            "property-absent",
            "the selected first property is absent; no payload may be composed",
        ));
    }

    let attribute_tag = header.resolved_attribute_tag.ok_or_else(|| {
        network_existing_actor_single_property_error(
            "missing-tag",
            "resolved property header did not contain an attribute tag",
        )
    })?;
    let payload_start_bit = header.payload_start_bit.ok_or_else(|| {
        network_existing_actor_single_property_error(
            "missing-payload-start",
            "resolved property header did not contain a payload start bit",
        )
    })?;

    if header.stop_bit != payload_start_bit {
        return Err(network_existing_actor_single_property_error(
            "header-stop-mismatch",
            format!(
                "property header stop bit {} differs from payload start bit {payload_start_bit}",
                header.stop_bit
            ),
        ));
    }

    match attribute_tag {
        ReplayNetworkAttributeTagV1::Boolean
        | ReplayNetworkAttributeTagV1::Byte
        | ReplayNetworkAttributeTagV1::Enum
        | ReplayNetworkAttributeTagV1::Float
        | ReplayNetworkAttributeTagV1::Int
        | ReplayNetworkAttributeTagV1::Int64 => {}
        _ => {
            return Err(network_existing_actor_single_property_error(
                "unsupported-tag",
                format!(
                    "attribute tag {attribute_tag:?} is outside the R3.18B primitive K1 composition"
                ),
            ));
        }
    }

    let scalar =
        decode_replay_network_primitive_scalar_v1(network_bytes, payload_start_bit, attribute_tag)?;
    if scalar.payload_start_bit != payload_start_bit || scalar.stop_bit != scalar.payload_end_bit {
        return Err(network_existing_actor_single_property_error(
            "scalar-boundary-mismatch",
            format!(
                "scalar boundary start/end/stop = {}/{}/{} but expected start {payload_start_bit}",
                scalar.payload_start_bit, scalar.payload_end_bit, scalar.stop_bit
            ),
        ));
    }

    let stop_bit = scalar.stop_bit;
    Ok(ReplayNetworkExistingActorSinglePrimitivePropertyV1 {
        header,
        scalar,
        stop_bit,
    })
}

/// Exactly one loop-control bit immediately after an already-decoded R3.18B first K1 property.
///
/// This result is deliberately not a reusable property-loop cursor. `stop_bit` is exactly one bit
/// after `first_property.stop_bit` and does not authorize a second stream/header/payload decode.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct ReplayNetworkExistingActorAfterFirstPrimitivePropertyControlV1 {
    pub next_property_present: bool,
    pub property_present_start_bit: u64,
    pub property_present_end_bit: u64,
    pub stop_bit: u64,
}

/// Read exactly the next `property_present` bit after one valid R3.18B first K1 property.
///
/// The caller must supply the already-decoded first-property result. This function validates that
/// result's published boundary invariants, reuses the private LSB-first network cursor for one bit,
/// and stops immediately. It never decodes a second stream id, property header, or payload.
pub fn decode_replay_network_existing_actor_after_first_primitive_property_control_v1(
    network_bytes: &[u8],
    first_property: &ReplayNetworkExistingActorSinglePrimitivePropertyV1,
) -> Result<ReplayNetworkExistingActorAfterFirstPrimitivePropertyControlV1> {
    if !first_property.header.property_present {
        return Err(network_existing_actor_after_first_property_control_error(
            "invalid-first-property",
            "first property result is not present",
        ));
    }

    let payload_start_bit = first_property.header.payload_start_bit.ok_or_else(|| {
        network_existing_actor_after_first_property_control_error(
            "invalid-first-property",
            "first property header is missing payload_start_bit",
        )
    })?;
    if first_property.header.stop_bit != payload_start_bit
        || first_property.scalar.payload_start_bit != payload_start_bit
        || first_property.scalar.stop_bit != first_property.scalar.payload_end_bit
        || first_property.stop_bit != first_property.scalar.payload_end_bit
    {
        return Err(network_existing_actor_after_first_property_control_error(
            "boundary-mismatch",
            format!(
                "header_stop={} header_payload_start={} scalar_start={} scalar_end={} scalar_stop={} first_stop={}",
                first_property.header.stop_bit,
                payload_start_bit,
                first_property.scalar.payload_start_bit,
                first_property.scalar.payload_end_bit,
                first_property.scalar.stop_bit,
                first_property.stop_bit,
            ),
        ));
    }

    if first_property.header.resolved_attribute_tag != Some(first_property.scalar.attribute_tag) {
        return Err(network_existing_actor_after_first_property_control_error(
            "tag-mismatch",
            format!(
                "header tag {:?} differs from scalar tag {:?}",
                first_property.header.resolved_attribute_tag, first_property.scalar.attribute_tag
            ),
        ));
    }

    let decoded_width = first_property
        .scalar
        .payload_end_bit
        .checked_sub(first_property.scalar.payload_start_bit)
        .ok_or_else(|| {
            network_existing_actor_after_first_property_control_error(
                "boundary-mismatch",
                "scalar payload end precedes payload start",
            )
        })?;
    if decoded_width != u64::from(first_property.scalar.payload_width) {
        return Err(network_existing_actor_after_first_property_control_error(
            "width-mismatch",
            format!(
                "scalar range width {decoded_width} differs from declared width {}",
                first_property.scalar.payload_width
            ),
        ));
    }

    let property_present_start_bit = first_property.stop_bit;
    let property_present_end_bit = property_present_start_bit.checked_add(1).ok_or_else(|| {
        network_existing_actor_after_first_property_control_error(
            "invalid-position",
            "next property_present end bit overflows u64",
        )
    })?;
    let start = usize::try_from(property_present_start_bit).map_err(|_| {
        network_existing_actor_after_first_property_control_error(
            "invalid-position",
            format!(
                "next property_present start bit {property_present_start_bit} does not fit usize"
            ),
        )
    })?;
    let end = usize::try_from(property_present_end_bit).map_err(|_| {
        network_existing_actor_after_first_property_control_error(
            "invalid-position",
            format!("next property_present end bit {property_present_end_bit} does not fit usize"),
        )
    })?;
    let total_bits = network_bytes.len().checked_mul(8).ok_or_else(|| {
        network_existing_actor_after_first_property_control_error(
            "invalid-length",
            "network bit length overflows usize",
        )
    })?;
    if end > total_bits {
        return Err(network_existing_actor_after_first_property_control_error(
            "insufficient-bits",
            format!(
                "need one property_present bit at position {start}, but network bit length is {total_bits}"
            ),
        ));
    }

    let mut cursor = NetworkBitCursor::new(network_bytes);
    cursor.bit_position = start;
    let next_property_present = cursor.read_bit()?;
    let stop_bit = u64::try_from(cursor.position_bits()).map_err(|_| {
        network_existing_actor_after_first_property_control_error(
            "invalid-position",
            "one-bit control stop does not fit u64",
        )
    })?;
    if stop_bit != property_present_end_bit {
        return Err(network_existing_actor_after_first_property_control_error(
            "control-stop-mismatch",
            format!("one-bit control stopped at {stop_bit}, expected {property_present_end_bit}"),
        ));
    }

    Ok(
        ReplayNetworkExistingActorAfterFirstPrimitivePropertyControlV1 {
            next_property_present,
            property_present_start_bit,
            property_present_end_bit,
            stop_bit,
        },
    )
}

/// Decode exactly one R3.17B-admitted primitive scalar payload.
///
/// The caller supplies an already resolved attribute tag and the exact
/// `payload_start_bit` returned by the existing property-header boundary. Reads use
/// the existing LSB-first network cursor, require no byte alignment, and stop after
/// exactly one scalar. Unsupported/compound tags are rejected before any payload read.
pub fn decode_replay_network_primitive_scalar_v1(
    network_bytes: &[u8],
    payload_start_bit: u64,
    attribute_tag: ReplayNetworkAttributeTagV1,
) -> Result<ReplayNetworkPrimitiveScalarDecodeV1> {
    let payload_width = match attribute_tag {
        ReplayNetworkAttributeTagV1::Boolean => 1,
        ReplayNetworkAttributeTagV1::Byte => 8,
        ReplayNetworkAttributeTagV1::Enum => 11,
        ReplayNetworkAttributeTagV1::Float | ReplayNetworkAttributeTagV1::Int => 32,
        ReplayNetworkAttributeTagV1::Int64 => 64,
        _ => {
            return Err(network_primitive_scalar_error(
                "unsupported-tag",
                format!("attribute tag {attribute_tag:?} is not an admitted primitive scalar"),
            ));
        }
    };

    let start = usize::try_from(payload_start_bit).map_err(|_| {
        network_primitive_scalar_error(
            "invalid-position",
            format!("payload start bit {payload_start_bit} does not fit usize"),
        )
    })?;
    let total_bits = network_bytes.len().checked_mul(8).ok_or_else(|| {
        network_primitive_scalar_error("invalid-length", "network bit length overflows usize")
    })?;
    if start > total_bits {
        return Err(network_primitive_scalar_error(
            "invalid-position",
            format!(
                "payload start bit {payload_start_bit} exceeds network bit length {total_bits}"
            ),
        ));
    }

    let mut cursor = NetworkBitCursor::new(network_bytes);
    cursor.bit_position = start;
    let raw = cursor.read_bits_le(usize::from(payload_width))?;

    let value = match attribute_tag {
        ReplayNetworkAttributeTagV1::Boolean => {
            ReplayNetworkPrimitiveScalarValueV1::Boolean(raw != 0)
        }
        ReplayNetworkAttributeTagV1::Byte => {
            ReplayNetworkPrimitiveScalarValueV1::Byte(u8::try_from(raw).map_err(|_| {
                network_primitive_scalar_error(
                    "invalid-value",
                    format!("8-bit scalar value {raw} does not fit u8"),
                )
            })?)
        }
        ReplayNetworkAttributeTagV1::Enum => {
            ReplayNetworkPrimitiveScalarValueV1::Enum(u16::try_from(raw).map_err(|_| {
                network_primitive_scalar_error(
                    "invalid-value",
                    format!("11-bit scalar value {raw} does not fit u16"),
                )
            })?)
        }
        ReplayNetworkAttributeTagV1::Float => {
            let raw_bits = u32::try_from(raw).map_err(|_| {
                network_primitive_scalar_error(
                    "invalid-value",
                    format!("32-bit float value {raw} does not fit u32"),
                )
            })?;
            ReplayNetworkPrimitiveScalarValueV1::Float {
                raw_bits,
                value: f32::from_bits(raw_bits),
            }
        }
        ReplayNetworkAttributeTagV1::Int => {
            let raw_bits = u32::try_from(raw).map_err(|_| {
                network_primitive_scalar_error(
                    "invalid-value",
                    format!("32-bit integer value {raw} does not fit u32"),
                )
            })?;
            ReplayNetworkPrimitiveScalarValueV1::Int(raw_bits as i32)
        }
        ReplayNetworkAttributeTagV1::Int64 => {
            ReplayNetworkPrimitiveScalarValueV1::Int64(raw as i64)
        }
        _ => unreachable!("unsupported tags return before payload read"),
    };

    let payload_end_bit = u64::try_from(cursor.position_bits()).map_err(|_| {
        network_primitive_scalar_error(
            "invalid-position",
            format!(
                "payload end bit {} does not fit u64",
                cursor.position_bits()
            ),
        )
    })?;

    Ok(ReplayNetworkPrimitiveScalarDecodeV1 {
        attribute_tag,
        payload_start_bit,
        payload_end_bit,
        payload_width,
        value,
        stop_bit: payload_end_bit,
    })
}

fn network_primitive_scalar_error(category: &str, detail: impl Into<String>) -> MimirError {
    MimirError::message(format!(
        "replay primitive scalar attribute error: {category}: {}",
        detail.into()
    ))
}

// R3.18G BEGIN bounded second-property header composition
/// One bounded optional second-property header after an already-valid R3.18B first primitive
/// property.
///
/// This result is deliberately not a generic property cursor. A present second property stops
/// exactly at its payload start; the payload itself, a third property and repeated iteration are
/// outside this API.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyHeaderV1 {
    pub control: ReplayNetworkExistingActorAfterFirstPrimitivePropertyControlV1,
    pub second_header: Option<ReplayNetworkExistingActorFirstPropertyHeaderV1>,
    pub stop_bit: u64,
}

/// Compose exactly one optional second-property header after an admitted R3.18B first primitive
/// property.
///
/// The existing R3.18D control decoder owns the next `property_present` bit. A false bit returns
/// immediately without consulting the lookup plan. A true bit reuses the existing property-header
/// primitive at that same bit, admits only the R3.18F-observed `Int`/`String` header contexts and
/// stops at `payload_start`. No second payload decoder is called.
pub fn decode_replay_network_existing_actor_after_first_primitive_second_property_header_v1(
    network_bytes: &[u8],
    first_property: &ReplayNetworkExistingActorSinglePrimitivePropertyV1,
    lookup_plan: &ReplayNetworkLookupPlanV1,
) -> Result<ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyHeaderV1> {
    let control = decode_replay_network_existing_actor_after_first_primitive_property_control_v1(
        network_bytes,
        first_property,
    )?;

    if !control.next_property_present {
        let stop_bit = control.stop_bit;
        return Ok(
            ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyHeaderV1 {
                control,
                second_header: None,
                stop_bit,
            },
        );
    }

    let header = decode_replay_network_existing_actor_first_property_header_v1(
        network_bytes,
        control.property_present_start_bit,
        first_property.header.actor_object_index,
        lookup_plan,
    )?;

    if !header.property_present {
        return Err(
            network_existing_actor_after_first_primitive_second_property_header_error(
                "control-header-mismatch",
                "R3.18D control reported a present second property but the header primitive did not",
            ),
        );
    }
    if header.property_present_start_bit != control.property_present_start_bit
        || header.property_present_end_bit != control.property_present_end_bit
        || control.stop_bit != control.property_present_end_bit
    {
        return Err(
            network_existing_actor_after_first_primitive_second_property_header_error(
                "control-header-boundary-mismatch",
                format!(
                    "control present bits [{}, {}) stop {}, header present bits [{}, {})",
                    control.property_present_start_bit,
                    control.property_present_end_bit,
                    control.stop_bit,
                    header.property_present_start_bit,
                    header.property_present_end_bit
                ),
            ),
        );
    }
    if header.actor_object_index != first_property.header.actor_object_index {
        return Err(
            network_existing_actor_after_first_primitive_second_property_header_error(
                "actor-mismatch",
                format!(
                    "first property actor {} does not match second header actor {}",
                    first_property.header.actor_object_index, header.actor_object_index
                ),
            ),
        );
    }

    match header.resolved_attribute_tag {
        Some(ReplayNetworkAttributeTagV1::Int | ReplayNetworkAttributeTagV1::String) => {}
        Some(tag) => {
            return Err(
                network_existing_actor_after_first_primitive_second_property_header_error(
                    "unsupported-second-header-tag",
                    format!("R3.18G admits only Int/String second-header contexts, got {tag:?}"),
                ),
            );
        }
        None => {
            return Err(
                network_existing_actor_after_first_primitive_second_property_header_error(
                    "missing-second-header-tag",
                    "present second header has no resolved attribute tag",
                ),
            );
        }
    }

    let payload_start_bit = header.payload_start_bit.ok_or_else(|| {
        network_existing_actor_after_first_primitive_second_property_header_error(
            "missing-payload-start",
            "present second header has no payload start",
        )
    })?;
    if header.stop_bit != payload_start_bit {
        return Err(
            network_existing_actor_after_first_primitive_second_property_header_error(
                "payload-boundary-mismatch",
                format!(
                    "second header stop {} does not equal payload start {}",
                    header.stop_bit, payload_start_bit
                ),
            ),
        );
    }
    if header.stop_bit < control.stop_bit {
        return Err(
            network_existing_actor_after_first_primitive_second_property_header_error(
                "non-monotonic-stop",
                format!(
                    "second header stop {} precedes control stop {}",
                    header.stop_bit, control.stop_bit
                ),
            ),
        );
    }

    let stop_bit = header.stop_bit;
    Ok(
        ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyHeaderV1 {
            control,
            second_header: Some(header),
            stop_bit,
        },
    )
}

fn network_existing_actor_after_first_primitive_second_property_header_error(
    category: &str,
    detail: impl Into<String>,
) -> MimirError {
    MimirError::message(format!(
        "replay existing actor after first primitive second property header error: {category}: {}",
        detail.into()
    ))
}
// R3.18G END bounded second-property header composition

fn network_existing_actor_after_first_property_control_error(
    category: &str,
    detail: impl Into<String>,
) -> MimirError {
    MimirError::message(format!(
        "replay existing actor after first primitive property control error: {category}: {}",
        detail.into()
    ))
}

fn network_existing_actor_single_property_error(
    category: &str,
    detail: impl Into<String>,
) -> MimirError {
    MimirError::message(format!(
        "replay existing actor single primitive property error: {category}: {}",
        detail.into()
    ))
}

fn network_existing_actor_property_error(category: &str, detail: impl Into<String>) -> MimirError {
    MimirError::message(format!(
        "replay existing actor property header error: {category}: {}",
        detail.into()
    ))
}

fn network_position_to_u64(position: usize) -> Result<u64> {
    u64::try_from(position).map_err(|_| {
        network_existing_actor_property_error(
            "invalid-position",
            format!("network bit position {position} does not fit u64"),
        )
    })
}

fn network_lookup_plan_error(category: &str, detail: impl Into<String>) -> MimirError {
    MimirError::message(format!(
        "replay network lookup plan error: {category}: {}",
        detail.into()
    ))
}

fn parse_replay_network_lookup_plan_from_memory(
    label: &str,
    bytes: &[u8],
) -> Result<ReplayNetworkLookupPlanV1> {
    // Reuse the exact production header admission lane. R3.13 does not widen version/build support.
    let header = parse_replay_header_from_memory(label, bytes)?;
    let footer_lookup = parse_replay_footer_lookup_materialization_from_memory(label, bytes)?;

    let num_frames = header.total_frames.ok_or_else(|| {
        network_lookup_plan_error(
            "missing-header-field",
            "NumFrames is required for the admitted network lookup plan",
        )
    })?;

    let max_channels_i64 = match header.metadata.get("MaxChannels") {
        Some(FieldValue::Integer(value)) => *value,
        Some(other) => {
            return Err(network_lookup_plan_error(
                "mapping",
                format!("MaxChannels must be integer metadata, got {other:?}"),
            ));
        }
        None => {
            return Err(network_lookup_plan_error(
                "missing-header-field",
                "MaxChannels is required for the admitted network lookup plan",
            ));
        }
    };
    let max_channels = u32::try_from(max_channels_i64).map_err(|_| {
        network_lookup_plan_error(
            "mapping",
            format!("MaxChannels {max_channels_i64} cannot fit non-negative u32"),
        )
    })?;
    if max_channels == 0 {
        return Err(network_lookup_plan_error(
            "mapping",
            "MaxChannels must be positive for the admitted network lookup plan",
        ));
    }

    if u64::from(num_frames) > u64::from(footer_lookup.scaffold.content.network_size) {
        return Err(network_lookup_plan_error(
            "precondition",
            format!(
                "NumFrames {num_frames} exceeds network byte count {}",
                footer_lookup.scaffold.content.network_size
            ),
        ));
    }

    let match_type = match header.metadata.get("MatchType") {
        Some(FieldValue::Text(value)) => value.as_str(),
        Some(other) => {
            return Err(network_lookup_plan_error(
                "mapping",
                format!("MatchType must be text metadata, got {other:?}"),
            ));
        }
        None => {
            return Err(network_lookup_plan_error(
                "missing-header-field",
                "MatchType is required for the admitted network lookup plan",
            ));
        }
    };
    let build_version = match header.metadata.get("BuildVersion") {
        Some(FieldValue::Text(value)) => value.as_str(),
        Some(other) => {
            return Err(network_lookup_plan_error(
                "mapping",
                format!("BuildVersion must be text metadata, got {other:?}"),
            ));
        }
        None => {
            return Err(network_lookup_plan_error(
                "missing-header-field",
                "BuildVersion is required for the admitted network lookup plan",
            ));
        }
    };

    let is_lan = match_type == "Lan";
    let qword_string_uses_text = replay_network_qword_string_uses_text_v1(build_version);

    let channel_width = u32::BITS - max_channels.leading_zeros();
    let channel_bits_u32 = channel_width.saturating_sub(1);
    let channel_bits = u8::try_from(channel_bits_u32).map_err(|_| {
        network_lookup_plan_error(
            "mapping",
            format!("derived channel bit width {channel_bits_u32} cannot fit u8"),
        )
    })?;

    let (spawn_trajectories, object_lookups) =
        build_replay_network_lookup_tables_v1(&footer_lookup.objects, &footer_lookup.net_cache)?;

    Ok(ReplayNetworkLookupPlanV1 {
        header,
        footer_lookup,
        num_frames,
        max_channels,
        channel_bits,
        is_lan,
        qword_string_uses_text,
        spawn_trajectories,
        object_lookups,
    })
}

fn build_replay_network_lookup_tables_v1(
    objects: &[String],
    net_cache: &[ReplayNetCacheEntryV1],
) -> Result<(
    Vec<ReplayNetworkSpawnTrajectoryV1>,
    Vec<Option<ReplayNetworkObjectLookupV1>>,
)> {
    let mut name_index = BTreeMap::<String, u32>::new();
    for (index, name) in objects.iter().enumerate() {
        let index = u32::try_from(index)
            .map_err(|_| network_lookup_plan_error("mapping", "object index cannot fit u32"))?;
        if name_index.insert(name.clone(), index).is_some() {
            return Err(network_lookup_plan_error(
                "malformed",
                format!("duplicate object name is outside admitted lookup evidence: {name}"),
            ));
        }
    }

    let mut local_properties = BTreeMap::<u32, BTreeMap<u32, u32>>::new();
    let mut seen_cache_objects = BTreeSet::new();
    for cache in net_cache {
        if cache.object_index as usize >= objects.len() {
            return Err(network_lookup_plan_error(
                "malformed",
                format!(
                    "net-cache object index {} is outside {} objects",
                    cache.object_index,
                    objects.len()
                ),
            ));
        }
        if !seen_cache_objects.insert(cache.object_index) {
            return Err(network_lookup_plan_error(
                "malformed",
                format!(
                    "duplicate net-cache object index {} is outside admitted lookup evidence",
                    cache.object_index
                ),
            ));
        }

        let target = local_properties.entry(cache.object_index).or_default();
        for property in &cache.properties {
            if property.object_index as usize >= objects.len() {
                return Err(network_lookup_plan_error(
                    "malformed",
                    format!(
                        "net-cache property object index {} is outside {} objects",
                        property.object_index,
                        objects.len()
                    ),
                ));
            }
            if target
                .insert(property.stream_id, property.object_index)
                .is_some()
            {
                return Err(network_lookup_plan_error(
                    "malformed",
                    format!(
                        "duplicate stream id {} for net-cache object {}",
                        property.stream_id, cache.object_index
                    ),
                ));
            }
        }
    }

    let mut hierarchy_by_object = Vec::with_capacity(objects.len());
    for object_name in objects {
        hierarchy_by_object.push(replay_network_hierarchy_object_indices_v1(
            object_name,
            &name_index,
        )?);
    }

    // Match the upstream two-stage spawn table: direct class entries first, then inherited
    // values cached while walking the same object hierarchy used by the attribute lookup.
    let mut spawn_cache = objects
        .iter()
        .map(|name| replay_network_spawn_trajectory_class_v1(name))
        .collect::<Vec<_>>();
    for hierarchy in &hierarchy_by_object {
        let mut unresolved = Vec::new();
        let mut resolved = ReplayNetworkSpawnTrajectoryV1::None;
        for object_index in hierarchy {
            match spawn_cache[*object_index as usize] {
                Some(trajectory) => {
                    resolved = trajectory;
                    break;
                }
                None => unresolved.push(*object_index),
            }
        }
        for object_index in unresolved {
            spawn_cache[object_index as usize] = Some(resolved);
        }
    }
    let spawn_trajectories = spawn_cache
        .into_iter()
        .map(|value| value.unwrap_or(ReplayNetworkSpawnTrajectoryV1::None))
        .collect::<Vec<_>>();

    let mut object_lookups = Vec::with_capacity(objects.len());
    for (object_index, hierarchy) in hierarchy_by_object.into_iter().enumerate() {
        if hierarchy.is_empty() {
            object_lookups.push(None);
            continue;
        }

        let mut effective = BTreeMap::<u32, u32>::new();
        for hierarchy_object_index in hierarchy.iter().rev() {
            if let Some(local) = local_properties.get(hierarchy_object_index) {
                for (stream_id, property_object_index) in local {
                    effective.insert(*stream_id, *property_object_index);
                }
            }
        }

        let max_prop_id = effective
            .keys()
            .next_back()
            .copied()
            .unwrap_or(2)
            .saturating_add(1);
        let max_bit_width = u32::BITS - max_prop_id.leading_zeros();
        let prop_id_bits_u32 = max_bit_width.max(1) - 1;
        let prop_id_bits = u8::try_from(prop_id_bits_u32).map_err(|_| {
            network_lookup_plan_error(
                "mapping",
                format!("derived property bit width {prop_id_bits_u32} cannot fit u8"),
            )
        })?;

        let properties = effective
            .into_iter()
            .map(
                |(stream_id, property_object_index)| ReplayNetworkResolvedPropertyV1 {
                    stream_id,
                    object_index: property_object_index,
                    tag: replay_network_attribute_tag_v1(&objects[property_object_index as usize]),
                },
            )
            .collect::<Vec<_>>();

        object_lookups.push(Some(ReplayNetworkObjectLookupV1 {
            object_index: u32::try_from(object_index).map_err(|_| {
                network_lookup_plan_error("mapping", "object lookup index cannot fit u32")
            })?,
            max_prop_id,
            prop_id_bits,
            properties,
        }));
    }

    Ok((spawn_trajectories, object_lookups))
}

fn replay_network_hierarchy_object_indices_v1(
    object_name: &str,
    name_index: &BTreeMap<String, u32>,
) -> Result<Vec<u32>> {
    let mut current = object_name.to_string();
    let mut seen = BTreeSet::new();
    let mut child_to_parent = Vec::new();

    while let Some(parent) = replay_network_parent_class_v1(&current) {
        if !seen.insert(current.clone()) {
            return Err(network_lookup_plan_error(
                "malformed",
                format!("network parent cycle while resolving {object_name}: {current}"),
            ));
        }
        if let Some(index) = name_index.get(&current) {
            child_to_parent.push(*index);
        }
        current = parent.to_string();
        if seen.len() > OBSERVED_NETWORK_PARENT_CLASSES_V1.len() {
            return Err(network_lookup_plan_error(
                "malformed",
                format!("network parent depth escaped admitted surface for {object_name}"),
            ));
        }
    }

    Ok(child_to_parent)
}

#[derive(Debug, Default, Clone, Copy)]
pub struct MinimalReplayHeaderReader;

impl ReplayReader for MinimalReplayHeaderReader {
    fn read_header(&self, input: &ReplayInput) -> Result<ReplayHeader> {
        match input {
            ReplayInput::Memory { label, bytes } => parse_replay_header_from_memory(label, bytes),
            ReplayInput::File(path) => Err(parse_error(
                "unsupported-input",
                format!(
                    "ReplayInput::File is outside the first minimal parser boundary: {}",
                    path.display()
                ),
            )),
        }
    }
}

#[derive(Debug, Default, Clone, Copy)]
pub struct UnsupportedReplayReader;

impl ReplayReader for UnsupportedReplayReader {
    fn read_header(&self, input: &ReplayInput) -> Result<ReplayHeader> {
        Err(MimirError::message(format!(
            "no replay parser is bundled in this scaffold for {}",
            input.label()
        )))
    }
}

const SUPPORTED_MAJOR_VERSION: i32 = 868;
const SUPPORTED_MINOR_VERSION: i32 = 32;
const SUPPORTED_NET_VERSION: i32 = 10;
const SUPPORTED_GAME_TYPE: &str = "TAGame.Replay_Soccar_TA";
const SUPPORTED_REPLAY_VERSION: i32 = 8;
const SUPPORTED_BUILD_VERSION_FIXTURE_001: &str = "241206.55345.468477";
const SUPPORTED_BUILD_VERSION_FIXTURE_002: &str = "250811.43331.492665";
const SUPPORTED_BUILD_VERSION_FIXTURE_003: &str = "251020.62592.500294";
const SUPPORTED_BUILD_VERSION_CORPUS_RANK_001: &str = "220826.56130.393105";
const SUPPORTED_BUILD_VERSION_CORPUS_RANK_002: &str = "230224.54624.415510";
const SUPPORTED_BUILD_VERSION_CORPUS_RANK_003: &str = "230823.66121.430366";
const SUPPORTED_BUILD_VERSION_CORPUS_RANK_004: &str = "231010.63095.433650";
const SUPPORTED_BUILD_VERSION_CORPUS_RANK_005: &str = "211110.58467.353926";
const SUPPORTED_BUILD_VERSION_CORPUS_RANK_006: &str = "211123.48895.355454";
const SUPPORTED_BUILD_VERSION_CORPUS_RANK_007: &str = "230113.44243.411503";
const SUPPORTED_BUILD_VERSION_CORPUS_RANK_008: &str = "230413.76047.419576";
const SUPPORTED_BUILD_VERSION_CORPUS_RANK_009: &str = "240425.56865.448852";
const SUPPORTED_BUILD_VERSION_CORPUS_RANK_010: &str = "240717.49861.454952";
const SUPPORTED_BUILD_VERSIONS_V1: [&str; 13] = [
    SUPPORTED_BUILD_VERSION_FIXTURE_001,
    SUPPORTED_BUILD_VERSION_FIXTURE_002,
    SUPPORTED_BUILD_VERSION_FIXTURE_003,
    SUPPORTED_BUILD_VERSION_CORPUS_RANK_001,
    SUPPORTED_BUILD_VERSION_CORPUS_RANK_002,
    SUPPORTED_BUILD_VERSION_CORPUS_RANK_003,
    SUPPORTED_BUILD_VERSION_CORPUS_RANK_004,
    SUPPORTED_BUILD_VERSION_CORPUS_RANK_005,
    SUPPORTED_BUILD_VERSION_CORPUS_RANK_006,
    SUPPORTED_BUILD_VERSION_CORPUS_RANK_007,
    SUPPORTED_BUILD_VERSION_CORPUS_RANK_008,
    SUPPORTED_BUILD_VERSION_CORPUS_RANK_009,
    SUPPORTED_BUILD_VERSION_CORPUS_RANK_010,
];
const MAX_ADMITTED_TEXT_BYTES: i32 = 10_000;
const MAX_CONTENT_SCAFFOLD_LIST_ITEMS: i32 = 25_000;
const MAX_CONTENT_SCAFFOLD_TEXT_UNITS: i32 = 10_000;

const KIND_ARRAY: &str = "ArrayProperty";
const KIND_BOOL: &str = "BoolProperty";
const KIND_FLOAT: &str = "FloatProperty";
const KIND_INT: &str = "IntProperty";
const KIND_NAME: &str = "NameProperty";
const KIND_QWORD: &str = "QWordProperty";
const KIND_STR: &str = "StrProperty";

fn is_supported_replay_header_tuple_v1(
    major_version: i32,
    minor_version: i32,
    net_version: i32,
    game_type: &str,
    replay_version: i32,
    build_version: &str,
) -> bool {
    if major_version != SUPPORTED_MAJOR_VERSION
        || minor_version != SUPPORTED_MINOR_VERSION
        || net_version != SUPPORTED_NET_VERSION
        || game_type != SUPPORTED_GAME_TYPE
        || replay_version != SUPPORTED_REPLAY_VERSION
    {
        return false;
    }

    SUPPORTED_BUILD_VERSIONS_V1.contains(&build_version)
}
struct HeaderCursor<'a> {
    bytes: &'a [u8],
    offset: usize,
}

impl<'a> HeaderCursor<'a> {
    fn new(bytes: &'a [u8]) -> Self {
        Self { bytes, offset: 0 }
    }

    fn remaining(&self) -> usize {
        self.bytes.len().saturating_sub(self.offset)
    }

    fn position(&self) -> usize {
        self.offset
    }

    fn read_exact(&mut self, len: usize, context: impl AsRef<str>) -> Result<&'a [u8]> {
        if len > self.remaining() {
            return Err(parse_error(
                "insufficient",
                format!(
                    "{} needs {} bytes at offset {}, only {} remain",
                    context.as_ref(),
                    len,
                    self.offset,
                    self.remaining()
                ),
            ));
        }

        let start = self.offset;
        self.offset += len;
        Ok(&self.bytes[start..self.offset])
    }

    fn read_i32_le(&mut self, context: impl AsRef<str>) -> Result<i32> {
        let raw = self.read_exact(4, context)?;
        Ok(i32::from_le_bytes(
            raw.try_into().expect("read_exact returned 4 bytes"),
        ))
    }

    fn read_u32_le(&mut self, context: impl AsRef<str>) -> Result<u32> {
        let raw = self.read_exact(4, context)?;
        Ok(u32::from_le_bytes(
            raw.try_into().expect("read_exact returned 4 bytes"),
        ))
    }

    fn read_f32_le(&mut self, context: impl AsRef<str>) -> Result<f32> {
        let raw = self.read_exact(4, context)?;
        Ok(f32::from_le_bytes(
            raw.try_into().expect("read_exact returned 4 bytes"),
        ))
    }

    fn read_parse_str_utf8_nul(&mut self, context: impl AsRef<str>) -> Result<String> {
        let context = context.as_ref();
        let bytes = self.read_len_prefixed_nul_bytes(context)?;
        std::str::from_utf8(bytes)
            .map(str::to_owned)
            .map_err(|error| malformed(format!("{context} is not UTF-8: {error}")))
    }

    fn read_parse_text_windows1252_nul(&mut self, context: impl AsRef<str>) -> Result<String> {
        let context = context.as_ref();
        let bytes = self.read_len_prefixed_nul_bytes(context)?;
        decode_windows1252(bytes, context)
    }

    fn read_len_prefixed_nul_bytes(&mut self, context: &str) -> Result<&'a [u8]> {
        let len = self.read_i32_le(format!("{context} length"))?;
        if len < 0 {
            return Err(parse_error(
                "unsupported-text",
                format!("{context} uses negative-length UTF-16 text, which is unsupported"),
            ));
        }
        if len > MAX_ADMITTED_TEXT_BYTES {
            return Err(malformed(format!(
                "{context} length {len} exceeds admitted bound {MAX_ADMITTED_TEXT_BYTES}"
            )));
        }

        let len = usize::try_from(len)
            .map_err(|_| malformed(format!("{context} length cannot fit usize")))?;
        if len == 0 {
            return Err(malformed(format!(
                "{context} has zero length and no trailing NUL"
            )));
        }

        let raw = self.read_exact(len, context)?;
        if raw.last() != Some(&0) {
            return Err(malformed(format!("{context} is missing trailing NUL")));
        }

        Ok(&raw[..raw.len() - 1])
    }

    fn skip_bounded(&mut self, len: usize, context: impl AsRef<str>) -> Result<()> {
        self.read_exact(len, context)?;
        Ok(())
    }
}

#[derive(Default)]
struct ParsedHeaderProperties {
    replay_id: Option<String>,
    total_frames: Option<u32>,
    replay_version: Option<i32>,
    build_version: Option<String>,
    metadata: Metadata,
}

fn parse_replay_body_boundary_from_memory(
    label: &str,
    bytes: &[u8],
) -> Result<ReplayBodyBoundaryV1> {
    if label.is_empty() {
        return Err(body_boundary_error(
            "mapping",
            "ReplayInput::Memory.label must be non-empty for ReplayBodyBoundaryV1.source_label",
        ));
    }

    if bytes.len() < 8 {
        return Err(body_boundary_error(
            "insufficient",
            format!(
                "body-boundary framing needs the 8-byte replay preamble, input has {} bytes",
                bytes.len()
            ),
        ));
    }

    let header_size_i32 =
        i32::from_le_bytes(bytes[0..4].try_into().expect("slice is exactly four bytes"));
    if header_size_i32 < 0 {
        return Err(body_boundary_error(
            "malformed",
            format!("header_size {header_size_i32} is negative"),
        ));
    }

    let header_size = usize::try_from(header_size_i32).map_err(|_| {
        body_boundary_error(
            "malformed",
            format!("header_size {header_size_i32} cannot fit usize"),
        )
    })?;
    let header_end = 8usize.checked_add(header_size).ok_or_else(|| {
        body_boundary_error(
            "malformed",
            format!("header_size {header_size_i32} overflows header_end"),
        )
    })?;
    let framing_end = header_end
        .checked_add(8)
        .ok_or_else(|| body_boundary_error("malformed", "content framing end overflows usize"))?;

    if framing_end > bytes.len() {
        return Err(body_boundary_error(
            "insufficient",
            format!(
                "header_end {header_end} requires 8 content-framing bytes through {framing_end}, input has {} bytes",
                bytes.len()
            ),
        ));
    }

    let content_size_i32 = i32::from_le_bytes(
        bytes[header_end..header_end + 4]
            .try_into()
            .expect("slice is exactly four bytes"),
    );
    if content_size_i32 < 0 {
        return Err(body_boundary_error(
            "malformed",
            format!("content_size {content_size_i32} is negative"),
        ));
    }
    let content_crc = u32::from_le_bytes(
        bytes[header_end + 4..header_end + 8]
            .try_into()
            .expect("slice is exactly four bytes"),
    );
    let content_size = usize::try_from(content_size_i32).map_err(|_| {
        body_boundary_error(
            "malformed",
            format!("content_size {content_size_i32} cannot fit usize"),
        )
    })?;
    let content_start = framing_end;
    let content_end = content_start.checked_add(content_size).ok_or_else(|| {
        body_boundary_error(
            "malformed",
            format!("content_size {content_size_i32} overflows content_end"),
        )
    })?;

    if content_end > bytes.len() {
        return Err(body_boundary_error(
            "insufficient",
            format!(
                "content_size {content_size_i32} requires content_end {content_end}, input has {} bytes",
                bytes.len()
            ),
        ));
    }
    if content_end < bytes.len() {
        return Err(body_boundary_error(
            "malformed",
            format!(
                "content_size {content_size_i32} leaves {} trailing bytes after content_end {content_end}",
                bytes.len() - content_end
            ),
        ));
    }

    let header_size = u32::try_from(header_size_i32)
        .map_err(|_| body_boundary_error("malformed", "non-negative header_size cannot fit u32"))?;
    let content_size = u32::try_from(content_size_i32).map_err(|_| {
        body_boundary_error("malformed", "non-negative content_size cannot fit u32")
    })?;
    let header_end = u64::try_from(header_end)
        .map_err(|_| body_boundary_error("malformed", "header_end cannot fit u64"))?;
    let content_start = u64::try_from(content_start)
        .map_err(|_| body_boundary_error("malformed", "content_start cannot fit u64"))?;
    let content_end = u64::try_from(content_end)
        .map_err(|_| body_boundary_error("malformed", "content_end cannot fit u64"))?;
    let input_len = u64::try_from(bytes.len())
        .map_err(|_| body_boundary_error("malformed", "input length cannot fit u64"))?;

    Ok(ReplayBodyBoundaryV1 {
        source_label: label.to_string(),
        header_size,
        header_end,
        content_size,
        content_crc,
        content_start,
        content_end,
        input_len,
    })
}

fn parse_replay_content_scaffold_from_memory(
    label: &str,
    bytes: &[u8],
) -> Result<ReplayContentScaffoldV1> {
    let boundary = parse_replay_body_boundary_from_memory(label, bytes)?;
    let content_start = usize::try_from(boundary.content_start)
        .map_err(|_| content_scaffold_error("malformed", "content_start cannot fit usize"))?;
    let content_end = usize::try_from(boundary.content_end)
        .map_err(|_| content_scaffold_error("malformed", "content_end cannot fit usize"))?;
    let mut cursor = content_start;

    let levels_count_offset = cursor;
    let levels_count_i32 =
        read_content_scaffold_i32(bytes, &mut cursor, content_end, "levels count")?;
    let levels_count = admitted_content_scaffold_count(levels_count_i32, "levels")?;
    let levels_data_start = cursor;
    for index in 0..levels_count {
        skip_content_scaffold_unreal_text(
            bytes,
            &mut cursor,
            content_end,
            &format!("levels[{index}]"),
        )?;
    }
    let levels_end = cursor;

    let keyframes_count_offset = cursor;
    let keyframes_count_i32 =
        read_content_scaffold_i32(bytes, &mut cursor, content_end, "keyframes count")?;
    let keyframes_count = admitted_content_scaffold_count(keyframes_count_i32, "keyframes")?;
    let keyframes_data_start = cursor;
    let keyframes_len = keyframes_count.checked_mul(12).ok_or_else(|| {
        content_scaffold_error("malformed", "keyframe byte length overflows usize")
    })?;
    skip_content_scaffold_bytes(
        bytes,
        &mut cursor,
        content_end,
        keyframes_len,
        "keyframe tuples",
    )?;
    let keyframes_end = cursor;

    let network_size_offset = cursor;
    let network_size_i32 =
        read_content_scaffold_i32(bytes, &mut cursor, content_end, "network size")?;
    if network_size_i32 < 0 {
        return Err(content_scaffold_error(
            "malformed",
            format!("network size {network_size_i32} is negative"),
        ));
    }
    let network_size = usize::try_from(network_size_i32).map_err(|_| {
        content_scaffold_error(
            "malformed",
            format!("network size {network_size_i32} cannot fit usize"),
        )
    })?;
    let network_start = cursor;
    skip_content_scaffold_bytes(
        bytes,
        &mut cursor,
        content_end,
        network_size,
        "network data",
    )?;
    let network_end = cursor;
    let footer_start = network_end;
    let footer_size = content_end.saturating_sub(footer_start);

    Ok(ReplayContentScaffoldV1 {
        boundary,
        levels_count_offset: scaffold_offset_u64(levels_count_offset, "levels_count_offset")?,
        levels_count: u32::try_from(levels_count)
            .map_err(|_| content_scaffold_error("malformed", "levels count cannot fit u32"))?,
        levels_data_start: scaffold_offset_u64(levels_data_start, "levels_data_start")?,
        levels_end: scaffold_offset_u64(levels_end, "levels_end")?,
        keyframes_count_offset: scaffold_offset_u64(
            keyframes_count_offset,
            "keyframes_count_offset",
        )?,
        keyframes_count: u32::try_from(keyframes_count)
            .map_err(|_| content_scaffold_error("malformed", "keyframes count cannot fit u32"))?,
        keyframes_data_start: scaffold_offset_u64(keyframes_data_start, "keyframes_data_start")?,
        keyframes_end: scaffold_offset_u64(keyframes_end, "keyframes_end")?,
        network_size_offset: scaffold_offset_u64(network_size_offset, "network_size_offset")?,
        network_size: u32::try_from(network_size)
            .map_err(|_| content_scaffold_error("malformed", "network size cannot fit u32"))?,
        network_start: scaffold_offset_u64(network_start, "network_start")?,
        network_end: scaffold_offset_u64(network_end, "network_end")?,
        footer_start: scaffold_offset_u64(footer_start, "footer_start")?,
        footer_size: scaffold_offset_u64(footer_size, "footer_size")?,
    })
}

fn admitted_content_scaffold_count(value: i32, context: &str) -> Result<usize> {
    if value < 0 {
        return Err(content_scaffold_error(
            "malformed",
            format!("{context} count {value} is negative"),
        ));
    }
    if value > MAX_CONTENT_SCAFFOLD_LIST_ITEMS {
        return Err(content_scaffold_error(
            "malformed",
            format!(
                "{context} count {value} exceeds structural bound {MAX_CONTENT_SCAFFOLD_LIST_ITEMS}"
            ),
        ));
    }
    usize::try_from(value).map_err(|_| {
        content_scaffold_error(
            "malformed",
            format!("{context} count {value} cannot fit usize"),
        )
    })
}

fn read_content_scaffold_i32(
    bytes: &[u8],
    cursor: &mut usize,
    content_end: usize,
    context: &str,
) -> Result<i32> {
    let raw = take_content_scaffold_bytes(bytes, cursor, content_end, 4, context)?;
    Ok(i32::from_le_bytes(
        raw.try_into()
            .expect("content scaffold read exactly four bytes"),
    ))
}

fn skip_content_scaffold_unreal_text(
    bytes: &[u8],
    cursor: &mut usize,
    content_end: usize,
    context: &str,
) -> Result<()> {
    let units =
        read_content_scaffold_i32(bytes, cursor, content_end, &format!("{context} length"))?;
    if !(-MAX_CONTENT_SCAFFOLD_TEXT_UNITS..=MAX_CONTENT_SCAFFOLD_TEXT_UNITS).contains(&units) {
        return Err(content_scaffold_error(
            "malformed",
            format!(
                "{context} text length {units} exceeds structural bound {MAX_CONTENT_SCAFFOLD_TEXT_UNITS}"
            ),
        ));
    }
    let unit_count = usize::try_from(units.unsigned_abs()).map_err(|_| {
        content_scaffold_error(
            "malformed",
            format!("{context} text length {units} cannot fit usize"),
        )
    })?;
    let byte_len = if units < 0 {
        unit_count.checked_mul(2).ok_or_else(|| {
            content_scaffold_error(
                "malformed",
                format!("{context} UTF-16 byte length overflows"),
            )
        })?
    } else {
        unit_count
    };
    skip_content_scaffold_bytes(bytes, cursor, content_end, byte_len, context)
}

fn skip_content_scaffold_bytes(
    bytes: &[u8],
    cursor: &mut usize,
    content_end: usize,
    len: usize,
    context: &str,
) -> Result<()> {
    take_content_scaffold_bytes(bytes, cursor, content_end, len, context)?;
    Ok(())
}

fn take_content_scaffold_bytes<'a>(
    bytes: &'a [u8],
    cursor: &mut usize,
    content_end: usize,
    len: usize,
    context: &str,
) -> Result<&'a [u8]> {
    let end = cursor.checked_add(len).ok_or_else(|| {
        content_scaffold_error(
            "malformed",
            format!("{context} length {len} overflows cursor"),
        )
    })?;
    if end > content_end || end > bytes.len() {
        return Err(content_scaffold_error(
            "insufficient",
            format!(
                "{context} needs {len} bytes at offset {}, content ends at {content_end}",
                *cursor
            ),
        ));
    }
    let start = *cursor;
    *cursor = end;
    Ok(&bytes[start..end])
}

fn scaffold_offset_u64(value: usize, context: &str) -> Result<u64> {
    u64::try_from(value)
        .map_err(|_| content_scaffold_error("malformed", format!("{context} cannot fit u64")))
}

fn parse_replay_footer_scaffold_from_memory(
    label: &str,
    bytes: &[u8],
) -> Result<ReplayFooterScaffoldV1> {
    let content = parse_replay_content_scaffold_from_memory(label, bytes)?;
    let content_end = usize::try_from(content.boundary.content_end)
        .map_err(|_| footer_scaffold_error("malformed", "content_end cannot fit usize"))?;
    let mut cursor = usize::try_from(content.footer_start)
        .map_err(|_| footer_scaffold_error("malformed", "footer_start cannot fit usize"))?;

    let debug_info_count_offset = cursor;
    let debug_info_count =
        read_footer_scaffold_count(bytes, &mut cursor, content_end, "debug info")?;
    let debug_info_data_start = cursor;
    for index in 0..debug_info_count {
        skip_footer_scaffold_bytes(
            bytes,
            &mut cursor,
            content_end,
            4,
            &format!("debug_info[{index}].frame"),
        )?;
        skip_footer_scaffold_unreal_text(
            bytes,
            &mut cursor,
            content_end,
            &format!("debug_info[{index}].user"),
        )?;
        skip_footer_scaffold_unreal_text(
            bytes,
            &mut cursor,
            content_end,
            &format!("debug_info[{index}].text"),
        )?;
    }
    let debug_info_end = cursor;

    let tickmarks_count_offset = cursor;
    let tickmarks_count = read_footer_scaffold_count(bytes, &mut cursor, content_end, "tickmarks")?;
    let tickmarks_data_start = cursor;
    for index in 0..tickmarks_count {
        skip_footer_scaffold_unreal_text(
            bytes,
            &mut cursor,
            content_end,
            &format!("tickmarks[{index}].description"),
        )?;
        skip_footer_scaffold_bytes(
            bytes,
            &mut cursor,
            content_end,
            4,
            &format!("tickmarks[{index}].frame"),
        )?;
    }
    let tickmarks_end = cursor;

    let packages_count_offset = cursor;
    let packages_count = read_footer_scaffold_count(bytes, &mut cursor, content_end, "packages")?;
    let packages_data_start = cursor;
    for index in 0..packages_count {
        skip_footer_scaffold_unreal_text(
            bytes,
            &mut cursor,
            content_end,
            &format!("packages[{index}]"),
        )?;
    }
    let packages_end = cursor;

    let objects_count_offset = cursor;
    let objects_count = read_footer_scaffold_count(bytes, &mut cursor, content_end, "objects")?;
    let objects_data_start = cursor;
    for index in 0..objects_count {
        skip_footer_scaffold_unreal_text(
            bytes,
            &mut cursor,
            content_end,
            &format!("objects[{index}]"),
        )?;
    }
    let objects_end = cursor;

    let names_count_offset = cursor;
    let names_count = read_footer_scaffold_count(bytes, &mut cursor, content_end, "names")?;
    let names_data_start = cursor;
    for index in 0..names_count {
        skip_footer_scaffold_unreal_text(
            bytes,
            &mut cursor,
            content_end,
            &format!("names[{index}]"),
        )?;
    }
    let names_end = cursor;

    let class_indices_count_offset = cursor;
    let class_indices_count =
        read_footer_scaffold_count(bytes, &mut cursor, content_end, "class indices")?;
    let class_indices_data_start = cursor;
    for index in 0..class_indices_count {
        skip_footer_scaffold_raw_string(
            bytes,
            &mut cursor,
            content_end,
            &format!("class_indices[{index}].class"),
        )?;
        skip_footer_scaffold_bytes(
            bytes,
            &mut cursor,
            content_end,
            4,
            &format!("class_indices[{index}].index"),
        )?;
    }
    let class_indices_end = cursor;

    let net_cache_count_offset = cursor;
    let net_cache_count = read_footer_scaffold_count(bytes, &mut cursor, content_end, "net cache")?;
    let net_cache_data_start = cursor;
    let mut net_cache_properties_count = 0usize;
    for index in 0..net_cache_count {
        skip_footer_scaffold_bytes(
            bytes,
            &mut cursor,
            content_end,
            12,
            &format!("net_cache[{index}] identity tuple"),
        )?;
        let property_count = read_footer_scaffold_count(
            bytes,
            &mut cursor,
            content_end,
            &format!("net_cache[{index}].properties"),
        )?;
        net_cache_properties_count = net_cache_properties_count
            .checked_add(property_count)
            .ok_or_else(|| {
                footer_scaffold_error("malformed", "net-cache property total overflows usize")
            })?;
        let property_bytes = property_count.checked_mul(8).ok_or_else(|| {
            footer_scaffold_error(
                "malformed",
                "net-cache property byte length overflows usize",
            )
        })?;
        skip_footer_scaffold_bytes(
            bytes,
            &mut cursor,
            content_end,
            property_bytes,
            &format!("net_cache[{index}].properties"),
        )?;
    }
    let net_cache_end = cursor;
    let opaque_tail_start = cursor;
    let opaque_tail_size = content_end.saturating_sub(cursor);
    match opaque_tail_size {
        0 => {}
        4 => {
            let tail = take_footer_scaffold_bytes(
                bytes,
                &mut cursor,
                content_end,
                4,
                "opaque footer tail",
            )?;
            if tail != [0, 0, 0, 0] {
                return Err(footer_scaffold_error(
                    "unsupported-layout",
                    format!("observed four-byte opaque tail is non-zero: {tail:02X?}"),
                ));
            }
        }
        other => {
            return Err(footer_scaffold_error(
                "unsupported-layout",
                format!(
                    "known footer fields leave {other} opaque tail bytes; admitted observed forms are 0 or four zero bytes"
                ),
            ));
        }
    }
    if cursor != content_end {
        return Err(footer_scaffold_error(
            "malformed",
            "footer cursor did not reach content_end after admitted opaque tail",
        ));
    }

    Ok(ReplayFooterScaffoldV1 {
        content,
        debug_info_count_offset: footer_offset_u64(
            debug_info_count_offset,
            "debug_info_count_offset",
        )?,
        debug_info_count: footer_count_u32(debug_info_count, "debug_info_count")?,
        debug_info_data_start: footer_offset_u64(debug_info_data_start, "debug_info_data_start")?,
        debug_info_end: footer_offset_u64(debug_info_end, "debug_info_end")?,
        tickmarks_count_offset: footer_offset_u64(
            tickmarks_count_offset,
            "tickmarks_count_offset",
        )?,
        tickmarks_count: footer_count_u32(tickmarks_count, "tickmarks_count")?,
        tickmarks_data_start: footer_offset_u64(tickmarks_data_start, "tickmarks_data_start")?,
        tickmarks_end: footer_offset_u64(tickmarks_end, "tickmarks_end")?,
        packages_count_offset: footer_offset_u64(packages_count_offset, "packages_count_offset")?,
        packages_count: footer_count_u32(packages_count, "packages_count")?,
        packages_data_start: footer_offset_u64(packages_data_start, "packages_data_start")?,
        packages_end: footer_offset_u64(packages_end, "packages_end")?,
        objects_count_offset: footer_offset_u64(objects_count_offset, "objects_count_offset")?,
        objects_count: footer_count_u32(objects_count, "objects_count")?,
        objects_data_start: footer_offset_u64(objects_data_start, "objects_data_start")?,
        objects_end: footer_offset_u64(objects_end, "objects_end")?,
        names_count_offset: footer_offset_u64(names_count_offset, "names_count_offset")?,
        names_count: footer_count_u32(names_count, "names_count")?,
        names_data_start: footer_offset_u64(names_data_start, "names_data_start")?,
        names_end: footer_offset_u64(names_end, "names_end")?,
        class_indices_count_offset: footer_offset_u64(
            class_indices_count_offset,
            "class_indices_count_offset",
        )?,
        class_indices_count: footer_count_u32(class_indices_count, "class_indices_count")?,
        class_indices_data_start: footer_offset_u64(
            class_indices_data_start,
            "class_indices_data_start",
        )?,
        class_indices_end: footer_offset_u64(class_indices_end, "class_indices_end")?,
        net_cache_count_offset: footer_offset_u64(
            net_cache_count_offset,
            "net_cache_count_offset",
        )?,
        net_cache_count: footer_count_u32(net_cache_count, "net_cache_count")?,
        net_cache_data_start: footer_offset_u64(net_cache_data_start, "net_cache_data_start")?,
        net_cache_properties_count: footer_count_u32(
            net_cache_properties_count,
            "net_cache_properties_count",
        )?,
        net_cache_end: footer_offset_u64(net_cache_end, "net_cache_end")?,
        opaque_tail_start: footer_offset_u64(opaque_tail_start, "opaque_tail_start")?,
        opaque_tail_size: footer_count_u32(opaque_tail_size, "opaque_tail_size")?,
        footer_end: footer_offset_u64(content_end, "footer_end")?,
    })
}

fn read_footer_scaffold_count(
    bytes: &[u8],
    cursor: &mut usize,
    content_end: usize,
    context: &str,
) -> Result<usize> {
    let value = read_footer_scaffold_i32(bytes, cursor, content_end, &format!("{context} count"))?;
    if value < 0 {
        return Err(footer_scaffold_error(
            "malformed",
            format!("{context} count {value} is negative"),
        ));
    }
    if value > MAX_CONTENT_SCAFFOLD_LIST_ITEMS {
        return Err(footer_scaffold_error(
            "malformed",
            format!(
                "{context} count {value} exceeds structural bound {MAX_CONTENT_SCAFFOLD_LIST_ITEMS}"
            ),
        ));
    }
    usize::try_from(value).map_err(|_| {
        footer_scaffold_error(
            "malformed",
            format!("{context} count {value} cannot fit usize"),
        )
    })
}

fn read_footer_scaffold_i32(
    bytes: &[u8],
    cursor: &mut usize,
    content_end: usize,
    context: &str,
) -> Result<i32> {
    let raw = take_footer_scaffold_bytes(bytes, cursor, content_end, 4, context)?;
    Ok(i32::from_le_bytes(
        raw.try_into()
            .expect("footer scaffold read exactly four bytes"),
    ))
}

fn skip_footer_scaffold_unreal_text(
    bytes: &[u8],
    cursor: &mut usize,
    content_end: usize,
    context: &str,
) -> Result<()> {
    let units = read_footer_scaffold_i32(bytes, cursor, content_end, &format!("{context} length"))?;
    if !(-MAX_CONTENT_SCAFFOLD_TEXT_UNITS..=MAX_CONTENT_SCAFFOLD_TEXT_UNITS).contains(&units) {
        return Err(footer_scaffold_error(
            "malformed",
            format!(
                "{context} text length {units} exceeds structural bound {MAX_CONTENT_SCAFFOLD_TEXT_UNITS}"
            ),
        ));
    }
    let unit_count = usize::try_from(units.unsigned_abs()).map_err(|_| {
        footer_scaffold_error(
            "malformed",
            format!("{context} text length {units} cannot fit usize"),
        )
    })?;
    let byte_len = if units < 0 {
        unit_count.checked_mul(2).ok_or_else(|| {
            footer_scaffold_error(
                "malformed",
                format!("{context} UTF-16 byte length overflows"),
            )
        })?
    } else {
        unit_count
    };
    skip_footer_scaffold_bytes(bytes, cursor, content_end, byte_len, context)
}

fn skip_footer_scaffold_raw_string(
    bytes: &[u8],
    cursor: &mut usize,
    content_end: usize,
    context: &str,
) -> Result<()> {
    let byte_len_i32 =
        read_footer_scaffold_i32(bytes, cursor, content_end, &format!("{context} length"))?;
    if byte_len_i32 < 0 {
        return Err(footer_scaffold_error(
            "malformed",
            format!("{context} raw string length {byte_len_i32} is negative"),
        ));
    }
    if byte_len_i32 > MAX_CONTENT_SCAFFOLD_TEXT_UNITS {
        return Err(footer_scaffold_error(
            "malformed",
            format!(
                "{context} raw string length {byte_len_i32} exceeds structural bound {MAX_CONTENT_SCAFFOLD_TEXT_UNITS}"
            ),
        ));
    }
    let byte_len = usize::try_from(byte_len_i32).map_err(|_| {
        footer_scaffold_error(
            "malformed",
            format!("{context} raw string length cannot fit usize"),
        )
    })?;
    skip_footer_scaffold_bytes(bytes, cursor, content_end, byte_len, context)
}

fn skip_footer_scaffold_bytes(
    bytes: &[u8],
    cursor: &mut usize,
    content_end: usize,
    len: usize,
    context: &str,
) -> Result<()> {
    take_footer_scaffold_bytes(bytes, cursor, content_end, len, context)?;
    Ok(())
}

fn take_footer_scaffold_bytes<'a>(
    bytes: &'a [u8],
    cursor: &mut usize,
    content_end: usize,
    len: usize,
    context: &str,
) -> Result<&'a [u8]> {
    let end = cursor.checked_add(len).ok_or_else(|| {
        footer_scaffold_error(
            "malformed",
            format!("{context} length {len} overflows cursor"),
        )
    })?;
    if end > content_end || end > bytes.len() {
        return Err(footer_scaffold_error(
            "insufficient",
            format!(
                "{context} needs {len} bytes at offset {}, content ends at {content_end}",
                *cursor
            ),
        ));
    }
    let start = *cursor;
    *cursor = end;
    Ok(&bytes[start..end])
}

fn footer_offset_u64(value: usize, context: &str) -> Result<u64> {
    u64::try_from(value)
        .map_err(|_| footer_scaffold_error("malformed", format!("{context} cannot fit u64")))
}

fn footer_count_u32(value: usize, context: &str) -> Result<u32> {
    u32::try_from(value)
        .map_err(|_| footer_scaffold_error("malformed", format!("{context} cannot fit u32")))
}

fn parse_replay_footer_lookup_materialization_from_memory(
    label: &str,
    bytes: &[u8],
) -> Result<ReplayFooterLookupMaterializationV1> {
    let scaffold = parse_replay_footer_scaffold_from_memory(label, bytes)?;
    let content_end = lookup_offset_usize(scaffold.content.boundary.content_end, "content_end")?;

    let mut objects_cursor =
        lookup_offset_usize(scaffold.objects_count_offset, "objects_count_offset")?;
    let objects_count =
        read_footer_lookup_count(bytes, &mut objects_cursor, content_end, "objects")?;
    require_lookup_count(objects_count, scaffold.objects_count, "objects")?;
    let mut objects = Vec::with_capacity(objects_count);
    for index in 0..objects_count {
        objects.push(read_footer_lookup_unreal_text(
            bytes,
            &mut objects_cursor,
            content_end,
            &format!("objects[{index}]"),
        )?);
    }
    require_lookup_cursor(objects_cursor, scaffold.objects_end, "objects_end")?;

    let mut names_cursor = lookup_offset_usize(scaffold.names_count_offset, "names_count_offset")?;
    let names_count = read_footer_lookup_count(bytes, &mut names_cursor, content_end, "names")?;
    require_lookup_count(names_count, scaffold.names_count, "names")?;
    let mut names = Vec::with_capacity(names_count);
    for index in 0..names_count {
        names.push(read_footer_lookup_unreal_text(
            bytes,
            &mut names_cursor,
            content_end,
            &format!("names[{index}]"),
        )?);
    }
    require_lookup_cursor(names_cursor, scaffold.names_end, "names_end")?;

    let mut class_cursor = lookup_offset_usize(
        scaffold.class_indices_count_offset,
        "class_indices_count_offset",
    )?;
    let class_count =
        read_footer_lookup_count(bytes, &mut class_cursor, content_end, "class indices")?;
    require_lookup_count(class_count, scaffold.class_indices_count, "class indices")?;
    let mut class_indices = Vec::with_capacity(class_count);
    for index in 0..class_count {
        let class_name = read_footer_lookup_raw_utf8_string(
            bytes,
            &mut class_cursor,
            content_end,
            &format!("class_indices[{index}].class"),
        )?;
        let object_index_i32 = read_footer_lookup_i32(
            bytes,
            &mut class_cursor,
            content_end,
            &format!("class_indices[{index}].index"),
        )?;
        let object_index = lookup_index_u32(
            object_index_i32,
            objects.len(),
            &format!("class_indices[{index}].index"),
        )?;
        let object_name = &objects[object_index as usize];
        if object_name != &class_name {
            return Err(footer_lookup_error(
                "mapping",
                format!(
                    "class_indices[{index}] class {class_name:?} does not match objects[{object_index}] {object_name:?}"
                ),
            ));
        }
        class_indices.push(ReplayClassIndexV1 {
            class_name,
            object_index,
        });
    }
    require_lookup_cursor(
        class_cursor,
        scaffold.class_indices_end,
        "class_indices_end",
    )?;

    let mut cache_cursor =
        lookup_offset_usize(scaffold.net_cache_count_offset, "net_cache_count_offset")?;
    let cache_count = read_footer_lookup_count(bytes, &mut cache_cursor, content_end, "net cache")?;
    require_lookup_count(cache_count, scaffold.net_cache_count, "net cache")?;
    let mut net_cache = Vec::with_capacity(cache_count);
    let mut total_properties = 0usize;
    for index in 0..cache_count {
        let object_index_i32 = read_footer_lookup_i32(
            bytes,
            &mut cache_cursor,
            content_end,
            &format!("net_cache[{index}].object_ind"),
        )?;
        let object_index = lookup_index_u32(
            object_index_i32,
            objects.len(),
            &format!("net_cache[{index}].object_ind"),
        )?;
        let parent_id = read_footer_lookup_i32(
            bytes,
            &mut cache_cursor,
            content_end,
            &format!("net_cache[{index}].parent_id"),
        )?;
        let cache_id = read_footer_lookup_i32(
            bytes,
            &mut cache_cursor,
            content_end,
            &format!("net_cache[{index}].cache_id"),
        )?;
        let property_count = read_footer_lookup_count(
            bytes,
            &mut cache_cursor,
            content_end,
            &format!("net_cache[{index}].properties"),
        )?;
        total_properties = total_properties
            .checked_add(property_count)
            .ok_or_else(|| {
                footer_lookup_error("malformed", "net-cache property total overflows usize")
            })?;
        let mut properties = Vec::with_capacity(property_count);
        for property_index in 0..property_count {
            let property_object_i32 = read_footer_lookup_i32(
                bytes,
                &mut cache_cursor,
                content_end,
                &format!("net_cache[{index}].properties[{property_index}].object_ind"),
            )?;
            let property_object_index = lookup_index_u32(
                property_object_i32,
                objects.len(),
                &format!("net_cache[{index}].properties[{property_index}].object_ind"),
            )?;
            let stream_id_i32 = read_footer_lookup_i32(
                bytes,
                &mut cache_cursor,
                content_end,
                &format!("net_cache[{index}].properties[{property_index}].stream_id"),
            )?;
            if stream_id_i32 < 0 {
                return Err(footer_lookup_error(
                    "mapping",
                    format!(
                        "net_cache[{index}].properties[{property_index}].stream_id {stream_id_i32} is negative"
                    ),
                ));
            }
            let stream_id = u32::try_from(stream_id_i32).map_err(|_| {
                footer_lookup_error(
                    "mapping",
                    format!(
                        "net_cache[{index}].properties[{property_index}].stream_id {stream_id_i32} cannot fit u32"
                    ),
                )
            })?;
            properties.push(ReplayNetCachePropertyV1 {
                object_index: property_object_index,
                stream_id,
            });
        }
        net_cache.push(ReplayNetCacheEntryV1 {
            object_index,
            parent_id,
            cache_id,
            properties,
        });
    }
    require_lookup_count(
        total_properties,
        scaffold.net_cache_properties_count,
        "net-cache properties total",
    )?;
    require_lookup_cursor(cache_cursor, scaffold.net_cache_end, "net_cache_end")?;

    Ok(ReplayFooterLookupMaterializationV1 {
        scaffold,
        objects,
        names,
        class_indices,
        net_cache,
    })
}

fn read_footer_lookup_count(
    bytes: &[u8],
    cursor: &mut usize,
    content_end: usize,
    context: &str,
) -> Result<usize> {
    let value = read_footer_lookup_i32(bytes, cursor, content_end, &format!("{context} count"))?;
    if value < 0 {
        return Err(footer_lookup_error(
            "malformed",
            format!("{context} count {value} is negative"),
        ));
    }
    if value > MAX_CONTENT_SCAFFOLD_LIST_ITEMS {
        return Err(footer_lookup_error(
            "malformed",
            format!(
                "{context} count {value} exceeds structural bound {MAX_CONTENT_SCAFFOLD_LIST_ITEMS}"
            ),
        ));
    }
    usize::try_from(value).map_err(|_| {
        footer_lookup_error(
            "malformed",
            format!("{context} count {value} cannot fit usize"),
        )
    })
}

fn read_footer_lookup_i32(
    bytes: &[u8],
    cursor: &mut usize,
    content_end: usize,
    context: &str,
) -> Result<i32> {
    let raw = take_footer_lookup_bytes(bytes, cursor, content_end, 4, context)?;
    Ok(i32::from_le_bytes(
        raw.try_into()
            .expect("footer lookup read exactly four bytes"),
    ))
}

fn read_footer_lookup_unreal_text(
    bytes: &[u8],
    cursor: &mut usize,
    content_end: usize,
    context: &str,
) -> Result<String> {
    let units = read_footer_lookup_i32(bytes, cursor, content_end, &format!("{context} length"))?;
    if units < 0 {
        return Err(footer_lookup_error(
            "unsupported-text",
            format!(
                "{context} uses negative-length UTF-16 text; R3.8 lookup admission covers only observed non-negative Windows-1252 text"
            ),
        ));
    }
    if units > MAX_CONTENT_SCAFFOLD_TEXT_UNITS {
        return Err(footer_lookup_error(
            "malformed",
            format!(
                "{context} length {units} exceeds structural bound {MAX_CONTENT_SCAFFOLD_TEXT_UNITS}"
            ),
        ));
    }
    let byte_len = usize::try_from(units).map_err(|_| {
        footer_lookup_error(
            "malformed",
            format!("{context} length {units} cannot fit usize"),
        )
    })?;
    if byte_len == 0 {
        return Ok(String::new());
    }
    let raw = take_footer_lookup_bytes(bytes, cursor, content_end, byte_len, context)?;
    if raw.last() != Some(&0) {
        return Err(footer_lookup_error(
            "malformed",
            format!("{context} is missing trailing NUL"),
        ));
    }
    decode_footer_lookup_windows1252(&raw[..raw.len() - 1], context)
}

fn read_footer_lookup_raw_utf8_string(
    bytes: &[u8],
    cursor: &mut usize,
    content_end: usize,
    context: &str,
) -> Result<String> {
    let byte_len_i32 =
        read_footer_lookup_i32(bytes, cursor, content_end, &format!("{context} length"))?;
    if byte_len_i32 <= 0 {
        return Err(footer_lookup_error(
            "malformed",
            format!("{context} raw string length {byte_len_i32} must be positive"),
        ));
    }
    if byte_len_i32 > MAX_CONTENT_SCAFFOLD_TEXT_UNITS {
        return Err(footer_lookup_error(
            "malformed",
            format!(
                "{context} raw string length {byte_len_i32} exceeds structural bound {MAX_CONTENT_SCAFFOLD_TEXT_UNITS}"
            ),
        ));
    }
    let byte_len = usize::try_from(byte_len_i32).map_err(|_| {
        footer_lookup_error(
            "malformed",
            format!("{context} raw string length cannot fit usize"),
        )
    })?;
    let raw = take_footer_lookup_bytes(bytes, cursor, content_end, byte_len, context)?;
    if raw.last() != Some(&0) {
        return Err(footer_lookup_error(
            "malformed",
            format!("{context} raw string is missing trailing NUL"),
        ));
    }
    std::str::from_utf8(&raw[..raw.len() - 1])
        .map(str::to_owned)
        .map_err(|error| {
            footer_lookup_error(
                "malformed",
                format!("{context} raw string is not UTF-8: {error}"),
            )
        })
}

fn decode_footer_lookup_windows1252(bytes: &[u8], context: &str) -> Result<String> {
    let mut decoded = String::with_capacity(bytes.len());
    for &byte in bytes {
        let character = match byte {
            0x00..=0x7F => char::from(byte),
            0x80 => '\u{20AC}',
            0x82 => '\u{201A}',
            0x83 => '\u{0192}',
            0x84 => '\u{201E}',
            0x85 => '\u{2026}',
            0x86 => '\u{2020}',
            0x87 => '\u{2021}',
            0x88 => '\u{02C6}',
            0x89 => '\u{2030}',
            0x8A => '\u{0160}',
            0x8B => '\u{2039}',
            0x8C => '\u{0152}',
            0x8E => '\u{017D}',
            0x91 => '\u{2018}',
            0x92 => '\u{2019}',
            0x93 => '\u{201C}',
            0x94 => '\u{201D}',
            0x95 => '\u{2022}',
            0x96 => '\u{2013}',
            0x97 => '\u{2014}',
            0x98 => '\u{02DC}',
            0x99 => '\u{2122}',
            0x9A => '\u{0161}',
            0x9B => '\u{203A}',
            0x9C => '\u{0153}',
            0x9E => '\u{017E}',
            0x9F => '\u{0178}',
            0x81 | 0x8D | 0x8F | 0x90 | 0x9D => {
                return Err(footer_lookup_error(
                    "malformed",
                    format!("{context} contains undefined Windows-1252 byte 0x{byte:02X}"),
                ));
            }
            _ => char::from(byte),
        };
        decoded.push(character);
    }
    Ok(decoded)
}

fn take_footer_lookup_bytes<'a>(
    bytes: &'a [u8],
    cursor: &mut usize,
    content_end: usize,
    len: usize,
    context: &str,
) -> Result<&'a [u8]> {
    let end = cursor.checked_add(len).ok_or_else(|| {
        footer_lookup_error(
            "malformed",
            format!("{context} length {len} overflows cursor"),
        )
    })?;
    if end > content_end || end > bytes.len() {
        return Err(footer_lookup_error(
            "insufficient",
            format!(
                "{context} needs {len} bytes at offset {}, content ends at {content_end}",
                *cursor
            ),
        ));
    }
    let start = *cursor;
    *cursor = end;
    Ok(&bytes[start..end])
}

fn lookup_index_u32(value: i32, object_count: usize, context: &str) -> Result<u32> {
    if value < 0 {
        return Err(footer_lookup_error(
            "mapping",
            format!("{context} {value} is negative"),
        ));
    }
    let index = usize::try_from(value).map_err(|_| {
        footer_lookup_error("mapping", format!("{context} {value} cannot fit usize"))
    })?;
    if index >= object_count {
        return Err(footer_lookup_error(
            "mapping",
            format!("{context} {value} is outside objects length {object_count}"),
        ));
    }
    u32::try_from(index)
        .map_err(|_| footer_lookup_error("mapping", format!("{context} {value} cannot fit u32")))
}

fn lookup_offset_usize(value: u64, context: &str) -> Result<usize> {
    usize::try_from(value).map_err(|_| {
        footer_lookup_error("malformed", format!("{context} {value} cannot fit usize"))
    })
}

fn require_lookup_count(actual: usize, expected: u32, context: &str) -> Result<()> {
    let expected = usize::try_from(expected).map_err(|_| {
        footer_lookup_error(
            "malformed",
            format!("{context} scaffold count {expected} cannot fit usize"),
        )
    })?;
    if actual == expected {
        Ok(())
    } else {
        Err(footer_lookup_error(
            "mapping",
            format!(
                "{context} materialized count {actual} does not match scaffold count {expected}"
            ),
        ))
    }
}

fn require_lookup_cursor(actual: usize, expected: u64, context: &str) -> Result<()> {
    let expected = lookup_offset_usize(expected, context)?;
    if actual == expected {
        Ok(())
    } else {
        Err(footer_lookup_error(
            "mapping",
            format!(
                "{context} materialization cursor {actual} does not match scaffold boundary {expected}"
            ),
        ))
    }
}

fn parse_replay_network_timing_preamble_from_memory(
    label: &str,
    bytes: &[u8],
) -> Result<ReplayNetworkTimingPreambleV1> {
    // Reuse the exact admitted header lane. R3.9 must not widen BuildVersion/version support.
    let header = parse_replay_header_from_memory(label, bytes)?;
    let content = parse_replay_content_scaffold_from_memory(label, bytes)?;

    let num_frames = header.total_frames.ok_or_else(|| {
        network_timing_error(
            "missing-header-field",
            "NumFrames is required for the admitted network timing preamble",
        )
    })?;

    let max_channels_i64 = match header.metadata.get("MaxChannels") {
        Some(FieldValue::Integer(value)) => *value,
        Some(other) => {
            return Err(network_timing_error(
                "mapping",
                format!("MaxChannels must be integer metadata, got {other:?}"),
            ));
        }
        None => {
            return Err(network_timing_error(
                "missing-header-field",
                "MaxChannels is required for the admitted network timing preamble",
            ));
        }
    };
    let max_channels = u32::try_from(max_channels_i64).map_err(|_| {
        network_timing_error(
            "mapping",
            format!("MaxChannels {max_channels_i64} cannot fit non-negative u32"),
        )
    })?;
    if max_channels == 0 {
        return Err(network_timing_error(
            "mapping",
            "MaxChannels must be positive for the admitted network timing preamble",
        ));
    }

    let network_size = usize::try_from(content.network_size)
        .map_err(|_| network_timing_error("malformed", "network_size cannot fit usize"))?;
    if network_size < 8 {
        return Err(network_timing_error(
            "insufficient",
            format!("network payload has {network_size} bytes; first timing pair needs 8"),
        ));
    }
    if usize::try_from(num_frames)
        .map_err(|_| network_timing_error("mapping", "NumFrames cannot fit usize"))?
        > network_size
    {
        return Err(network_timing_error(
            "precondition",
            format!("NumFrames {num_frames} exceeds network payload byte length {network_size}"),
        ));
    }

    let network_start = usize::try_from(content.network_start)
        .map_err(|_| network_timing_error("malformed", "network_start cannot fit usize"))?;
    let timing_end = network_start.checked_add(8).ok_or_else(|| {
        network_timing_error("malformed", "first timing byte range overflows usize")
    })?;
    if timing_end > bytes.len() {
        return Err(network_timing_error(
            "insufficient",
            "first network timing pair extends beyond replay bytes",
        ));
    }

    let first_frame_time = f32::from_le_bytes(
        bytes[network_start..network_start + 4]
            .try_into()
            .expect("timing range checked for four bytes"),
    );
    let first_frame_delta = f32::from_le_bytes(
        bytes[network_start + 4..timing_end]
            .try_into()
            .expect("timing range checked for four bytes"),
    );
    validate_network_timing_component("time", first_frame_time)?;
    validate_network_timing_component("delta", first_frame_delta)?;
    if first_frame_time == 0.0 && first_frame_delta == 0.0 {
        return Err(network_timing_error(
            "terminal-first-frame",
            "first network timing pair is the 0/0 terminal marker",
        ));
    }

    let bit_width = u32::BITS - max_channels.leading_zeros();
    let channel_bits_u32 = bit_width.saturating_sub(1);
    let channel_bits = u8::try_from(channel_bits_u32).map_err(|_| {
        network_timing_error(
            "mapping",
            format!("derived channel bit width {channel_bits_u32} cannot fit u8"),
        )
    })?;

    Ok(ReplayNetworkTimingPreambleV1 {
        header,
        content,
        num_frames,
        max_channels,
        channel_bits,
        first_frame_time,
        first_frame_delta,
    })
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
struct DecodedNetworkFirstActorHeaderV1 {
    time_raw_u32: u32,
    delta_raw_u32: u32,
    actor_present: bool,
    actor_id: Option<u32>,
    alive: Option<bool>,
    is_new: Option<bool>,
    stop_bit: usize,
}

fn parse_replay_network_first_actor_envelope_from_memory(
    label: &str,
    bytes: &[u8],
) -> Result<ReplayNetworkFirstActorEnvelopeV1> {
    // Reuse the exact admitted timing/header/content lane. R3.14D must not widen support.
    let timing = parse_replay_network_timing_preamble_from_memory(label, bytes)?;

    let network_start = usize::try_from(timing.content.network_start).map_err(|_| {
        network_first_actor_envelope_error("malformed", "network_start cannot fit usize")
    })?;
    let network_size = usize::try_from(timing.content.network_size).map_err(|_| {
        network_first_actor_envelope_error("malformed", "network_size cannot fit usize")
    })?;
    let network_end = network_start.checked_add(network_size).ok_or_else(|| {
        network_first_actor_envelope_error("malformed", "network byte range overflows usize")
    })?;
    if network_end > bytes.len() {
        return Err(network_first_actor_envelope_error(
            "insufficient",
            "network payload extends beyond replay bytes",
        ));
    }

    let decoded = decode_network_first_actor_header(
        &bytes[network_start..network_end],
        timing.max_channels,
        timing.channel_bits,
        timing.first_frame_time.to_bits(),
        timing.first_frame_delta.to_bits(),
    )?;
    let stop_bit = u64::try_from(decoded.stop_bit)
        .map_err(|_| network_first_actor_envelope_error("mapping", "stop bit cannot fit u64"))?;

    Ok(ReplayNetworkFirstActorEnvelopeV1 {
        timing,
        first_frame_time_raw_u32: decoded.time_raw_u32,
        first_frame_delta_raw_u32: decoded.delta_raw_u32,
        actor_present: decoded.actor_present,
        actor_id: decoded.actor_id,
        alive: decoded.alive,
        is_new: decoded.is_new,
        stop_bit,
    })
}

fn decode_network_first_actor_header(
    network: &[u8],
    max_channels: u32,
    channel_bits: u8,
    expected_time_raw_u32: u32,
    expected_delta_raw_u32: u32,
) -> Result<DecodedNetworkFirstActorHeaderV1> {
    let mut cursor = NetworkBitCursor::new(network);

    let time_raw_u32 = u32::try_from(cursor.read_bits_le(32)?).map_err(|_| {
        network_first_actor_envelope_error("mapping", "time raw bits cannot fit u32")
    })?;
    let delta_raw_u32 = u32::try_from(cursor.read_bits_le(32)?).map_err(|_| {
        network_first_actor_envelope_error("mapping", "delta raw bits cannot fit u32")
    })?;

    if time_raw_u32 != expected_time_raw_u32 {
        return Err(network_first_actor_envelope_error(
            "timing-mismatch",
            format!(
                "cursor time raw bits {time_raw_u32:#010x} differ from admitted timing preamble {expected_time_raw_u32:#010x}"
            ),
        ));
    }
    if delta_raw_u32 != expected_delta_raw_u32 {
        return Err(network_first_actor_envelope_error(
            "timing-mismatch",
            format!(
                "cursor delta raw bits {delta_raw_u32:#010x} differ from admitted timing preamble {expected_delta_raw_u32:#010x}"
            ),
        ));
    }

    // The preamble has already validated these values. Re-materialize them from cursor bits so
    // the reader cannot silently skip the first 64 network bits.
    let _time = f32::from_bits(time_raw_u32);
    let _delta = f32::from_bits(delta_raw_u32);

    let actor_present = cursor.read_bit().map_err(|error| {
        network_first_actor_envelope_error(
            "actor-present",
            format!("cannot read first actor_present bit: {error}"),
        )
    })?;
    if !actor_present {
        return Ok(DecodedNetworkFirstActorHeaderV1 {
            time_raw_u32,
            delta_raw_u32,
            actor_present,
            actor_id: None,
            alive: None,
            is_new: None,
            stop_bit: cursor.position_bits(),
        });
    }

    let actor_id = cursor
        .read_bounded_u32(max_channels, channel_bits)
        .map_err(|error| {
            network_first_actor_envelope_error(
                "actor-id",
                format!("cannot read first bounded actor_id: {error}"),
            )
        })?;

    let alive = cursor.read_bit().map_err(|error| {
        network_first_actor_envelope_error(
            "alive",
            format!("cannot read first actor alive bit: {error}"),
        )
    })?;
    if !alive {
        return Ok(DecodedNetworkFirstActorHeaderV1 {
            time_raw_u32,
            delta_raw_u32,
            actor_present,
            actor_id: Some(actor_id),
            alive: Some(false),
            is_new: None,
            stop_bit: cursor.position_bits(),
        });
    }

    let is_new = cursor.read_bit().map_err(|error| {
        network_first_actor_envelope_error(
            "new",
            format!("cannot read first actor new bit: {error}"),
        )
    })?;

    Ok(DecodedNetworkFirstActorHeaderV1 {
        time_raw_u32,
        delta_raw_u32,
        actor_present,
        actor_id: Some(actor_id),
        alive: Some(true),
        is_new: Some(is_new),
        stop_bit: cursor.position_bits(),
    })
}

fn parse_replay_network_first_new_actor_envelope_from_memory(
    label: &str,
    bytes: &[u8],
) -> Result<ReplayNetworkFirstNewActorEnvelopeV1> {
    // Preserve the exact admitted timing/header/content lane and first-envelope decoder.
    let timing = parse_replay_network_timing_preamble_from_memory(label, bytes)?;
    let network_start = usize::try_from(timing.content.network_start).map_err(|_| {
        network_first_new_actor_error("malformed", "network_start cannot fit usize")
    })?;
    let network_size = usize::try_from(timing.content.network_size)
        .map_err(|_| network_first_new_actor_error("malformed", "network_size cannot fit usize"))?;
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

fn network_first_actor_envelope_error(category: &str, detail: impl Into<String>) -> MimirError {
    MimirError::message(format!(
        "replay network first actor envelope error: {category}: {}",
        detail.into()
    ))
}

fn validate_network_timing_component(name: &str, value: f32) -> Result<()> {
    if !value.is_finite() || value < 0.0 || (value > 0.0 && value < 1.0e-10) {
        return Err(network_timing_error(
            "malformed",
            format!("first frame {name} is outside admitted finite timing bounds: {value:?}"),
        ));
    }
    Ok(())
}

fn parse_replay_header_from_memory(label: &str, bytes: &[u8]) -> Result<ReplayHeader> {
    if label.is_empty() {
        return Err(mapping_error(
            "ReplayInput::Memory.label must be non-empty for ReplayHeader.source_label",
        ));
    }

    let mut outer = HeaderCursor::new(bytes);
    let header_size = outer.read_i32_le("header_size")?;
    let _header_crc = outer.read_u32_le("header_crc")?;

    if header_size < 0 {
        return Err(malformed(format!("header_size {header_size} is negative")));
    }

    let header_len = usize::try_from(header_size)
        .map_err(|_| malformed(format!("header_size {header_size} cannot fit usize")))?;
    let header_end = 8usize
        .checked_add(header_len)
        .ok_or_else(|| malformed(format!("header_size {header_size} overflows header_end")))?;

    if header_end > bytes.len() {
        return Err(parse_error(
            "insufficient",
            format!(
                "header_size {header_size} requires header_end {header_end}, input has {} bytes",
                bytes.len()
            ),
        ));
    }

    let header_bytes = &bytes[8..header_end];
    let mut header = HeaderCursor::new(header_bytes);
    let major_version = header.read_i32_le("major_version")?;
    let minor_version = header.read_i32_le("minor_version")?;
    let net_version = header.read_i32_le("net_version")?;
    let game_type = header.read_parse_text_windows1252_nul("game_type")?;

    let parsed = parse_top_level_properties(&mut header)?;

    if header.position() != header_bytes.len() {
        return Err(malformed(format!(
            "header terminator ended at {}, expected {}",
            header.position(),
            header_bytes.len()
        )));
    }

    let replay_version = parsed.replay_version.ok_or_else(|| {
        mapping_error("missing required ReplayVersion for supported-version tuple")
    })?;
    let build_version = parsed.build_version.as_deref().ok_or_else(|| {
        mapping_error("missing required BuildVersion for supported-version tuple")
    })?;

    if !is_supported_replay_header_tuple_v1(
        major_version,
        minor_version,
        net_version,
        &game_type,
        replay_version,
        build_version,
    ) {
        return Err(parse_error(
            "unsupported-version",
            format!(
                "unsupported tuple major={major_version}, minor={minor_version}, net={net_version}, game_type={game_type}, ReplayVersion={replay_version}, BuildVersion={build_version}"
            ),
        ));
    }
    let replay_id = parsed
        .replay_id
        .ok_or_else(|| mapping_error("missing required Id property for ReplayHeader.replay_id"))?;

    Ok(ReplayHeader {
        replay_id: ReplayId::new(replay_id),
        source_label: label.to_string(),
        total_frames: parsed.total_frames,
        metadata: parsed.metadata,
    })
}

fn parse_top_level_properties(cursor: &mut HeaderCursor<'_>) -> Result<ParsedHeaderProperties> {
    let mut seen = BTreeSet::new();
    let mut parsed = ParsedHeaderProperties::default();
    let mut terminated = false;

    while cursor.position() < cursor.bytes.len() {
        let key_offset = cursor.position();
        let key = cursor.read_parse_str_utf8_nul("property key")?;
        if key == "None" {
            terminated = true;
            break;
        }

        if !seen.insert(key.clone()) {
            if is_selected_property(&key) {
                return Err(mapping_error(format!("duplicate selected property {key}")));
            }
            return Err(malformed(format!(
                "duplicate top-level property {key} at header offset {key_offset}"
            )));
        }

        let kind = cursor.read_parse_str_utf8_nul(format!("property {key} kind"))?;
        let property_size = cursor.read_u32_le(format!("property {key} size"))?;
        let _ignored = cursor.read_u32_le(format!("property {key} ignored field"))?;
        let value_len = usize::try_from(property_size).map_err(|_| {
            malformed(format!(
                "property {key} size {property_size} cannot fit usize"
            ))
        })?;

        if value_len > cursor.remaining() {
            return Err(malformed(format!(
                "property {key} size {property_size} exceeds header boundary at offset {}",
                cursor.position()
            )));
        }

        if is_selected_property(&key) {
            parse_selected_property(&mut parsed, &key, &kind, cursor, value_len)?;
        } else {
            skip_non_selected_property(&key, &kind, cursor, value_len)?;
        }
    }

    if !terminated {
        return Err(malformed("missing top-level property terminator None"));
    }

    Ok(parsed)
}

fn parse_selected_property(
    parsed: &mut ParsedHeaderProperties,
    key: &str,
    kind: &str,
    cursor: &mut HeaderCursor<'_>,
    value_len: usize,
) -> Result<()> {
    let value_bytes = cursor.read_exact(value_len, format!("property {key} value"))?;
    let mut value = HeaderCursor::new(value_bytes);

    match key {
        "Id" => {
            require_kind(key, kind, KIND_STR)?;
            let id = value.read_parse_text_windows1252_nul("Id value")?;
            ensure_consumed(&value, key)?;
            if !is_admitted_replay_id(&id) {
                return Err(mapping_error(
                    "Id must be exactly 32 ASCII hexadecimal digits",
                ));
            }
            parsed.replay_id = Some(id);
        }
        "NumFrames" => {
            require_kind(key, kind, KIND_INT)?;
            require_value_len(key, value_len, 4)?;
            let frames = value.read_i32_le("NumFrames value")?;
            ensure_consumed(&value, key)?;
            if frames < 0 {
                return Err(mapping_error(format!("NumFrames {frames} is negative")));
            }
            parsed.total_frames = Some(frames as u32);
        }
        "ReplayName" | "Date" | "BuildVersion" => {
            require_kind(key, kind, KIND_STR)?;
            let text = value.read_parse_text_windows1252_nul(format!("{key} value"))?;
            ensure_consumed(&value, key)?;
            if key == "BuildVersion" {
                parsed.build_version = Some(text.clone());
            }
            parsed.metadata.insert(key, FieldValue::Text(text));
        }
        "MapName" | "MatchType" => {
            require_kind(key, kind, KIND_NAME)?;
            let text = value.read_parse_text_windows1252_nul(format!("{key} value"))?;
            ensure_consumed(&value, key)?;
            parsed.metadata.insert(key, FieldValue::Text(text));
        }
        "ReplayVersion" | "MaxChannels" | "TeamSize" => {
            require_kind(key, kind, KIND_INT)?;
            require_value_len(key, value_len, 4)?;
            let number = value.read_i32_le(format!("{key} value"))?;
            ensure_consumed(&value, key)?;
            if key == "ReplayVersion" {
                parsed.replay_version = Some(number);
            }
            parsed
                .metadata
                .insert(key, FieldValue::Integer(i64::from(number)));
        }
        "RecordFPS" => {
            require_kind(key, kind, KIND_FLOAT)?;
            require_value_len(key, value_len, 4)?;
            let number = value.read_f32_le("RecordFPS value")?;
            ensure_consumed(&value, key)?;
            if !number.is_finite() {
                return Err(mapping_error("RecordFPS must be finite"));
            }
            parsed
                .metadata
                .insert(key, FieldValue::Float(f64::from(number)));
        }
        _ => unreachable!("is_selected_property and parse_selected_property are out of sync"),
    }

    Ok(())
}

fn skip_non_selected_property(
    key: &str,
    kind: &str,
    cursor: &mut HeaderCursor<'_>,
    value_len: usize,
) -> Result<()> {
    match kind {
        KIND_BOOL => skip_non_selected_bool_property(key, cursor, value_len),
        KIND_ARRAY | KIND_FLOAT | KIND_INT | KIND_NAME | KIND_QWORD | KIND_STR => {
            cursor.skip_bounded(value_len, format!("property {key} value"))
        }
        _ => Err(parse_error(
            "unsupported-property",
            format!("property {key} uses unsupported kind {kind}"),
        )),
    }
}

fn skip_non_selected_bool_property(
    key: &str,
    cursor: &mut HeaderCursor<'_>,
    value_len: usize,
) -> Result<()> {
    if value_len != 0 {
        return Err(malformed(format!(
            "property {key} BoolProperty has declared size {value_len}, expected 0"
        )));
    }

    let value = cursor.read_exact(1, format!("property {key} BoolProperty value"))?[0];
    match value {
        0 | 1 => Ok(()),
        _ => Err(malformed(format!(
            "property {key} BoolProperty value must be 0 or 1, got {value}"
        ))),
    }
}

fn require_kind(key: &str, actual: &str, expected: &str) -> Result<()> {
    if actual == expected {
        return Ok(());
    }

    if is_admitted_property_kind(actual) {
        return Err(mapping_error(format!(
            "selected property {key} has kind {actual}, expected {expected}"
        )));
    }

    Err(parse_error(
        "unsupported-property",
        format!("selected property {key} uses unsupported kind {actual}"),
    ))
}

fn require_value_len(key: &str, actual: usize, expected: usize) -> Result<()> {
    if actual == expected {
        Ok(())
    } else {
        Err(malformed(format!(
            "selected property {key} has value length {actual}, expected {expected}"
        )))
    }
}

fn ensure_consumed(cursor: &HeaderCursor<'_>, key: &str) -> Result<()> {
    if cursor.remaining() == 0 {
        Ok(())
    } else {
        Err(malformed(format!(
            "selected property {key} left {} trailing value bytes",
            cursor.remaining()
        )))
    }
}

fn is_selected_property(key: &str) -> bool {
    matches!(
        key,
        "Id" | "NumFrames"
            | "ReplayName"
            | "Date"
            | "MapName"
            | "ReplayVersion"
            | "BuildVersion"
            | "MaxChannels"
            | "MatchType"
            | "TeamSize"
            | "RecordFPS"
    )
}

fn is_admitted_property_kind(kind: &str) -> bool {
    matches!(
        kind,
        KIND_ARRAY | KIND_FLOAT | KIND_INT | KIND_NAME | KIND_QWORD | KIND_STR
    )
}

fn is_admitted_replay_id(value: &str) -> bool {
    value.len() == 32 && value.bytes().all(|byte| byte.is_ascii_hexdigit())
}

fn decode_windows1252(bytes: &[u8], context: &str) -> Result<String> {
    let mut decoded = String::with_capacity(bytes.len());
    for &byte in bytes {
        let character = match byte {
            0x00..=0x7F => char::from(byte),
            0x80 => '\u{20AC}',
            0x82 => '\u{201A}',
            0x83 => '\u{0192}',
            0x84 => '\u{201E}',
            0x85 => '\u{2026}',
            0x86 => '\u{2020}',
            0x87 => '\u{2021}',
            0x88 => '\u{02C6}',
            0x89 => '\u{2030}',
            0x8A => '\u{0160}',
            0x8B => '\u{2039}',
            0x8C => '\u{0152}',
            0x8E => '\u{017D}',
            0x91 => '\u{2018}',
            0x92 => '\u{2019}',
            0x93 => '\u{201C}',
            0x94 => '\u{201D}',
            0x95 => '\u{2022}',
            0x96 => '\u{2013}',
            0x97 => '\u{2014}',
            0x98 => '\u{02DC}',
            0x99 => '\u{2122}',
            0x9A => '\u{0161}',
            0x9B => '\u{203A}',
            0x9C => '\u{0153}',
            0x9E => '\u{017E}',
            0x9F => '\u{0178}',
            0x81 | 0x8D | 0x8F | 0x90 | 0x9D => {
                return Err(malformed(format!(
                    "{context} contains undefined Windows-1252 byte 0x{byte:02X}"
                )));
            }
            _ => char::from(byte),
        };
        decoded.push(character);
    }
    Ok(decoded)
}

fn network_timing_error(category: &str, detail: impl Into<String>) -> MimirError {
    MimirError::message(format!(
        "replay network timing error: {category}: {}",
        detail.into()
    ))
}

fn footer_lookup_error(category: &str, detail: impl Into<String>) -> MimirError {
    MimirError::message(format!(
        "replay footer lookup error: {category}: {}",
        detail.into()
    ))
}

fn footer_scaffold_error(category: &str, detail: impl Into<String>) -> MimirError {
    MimirError::message(format!(
        "replay footer scaffold error: {category}: {}",
        detail.into()
    ))
}

fn content_scaffold_error(category: &str, detail: impl Into<String>) -> MimirError {
    MimirError::message(format!(
        "replay content scaffold error: {category}: {}",
        detail.into()
    ))
}

fn body_boundary_error(category: &str, detail: impl Into<String>) -> MimirError {
    MimirError::message(format!(
        "replay body boundary error: {category}: {}",
        detail.into()
    ))
}

fn parse_error(category: &str, detail: impl Into<String>) -> MimirError {
    MimirError::message(format!(
        "replay header parse error: {category}: {}",
        detail.into()
    ))
}

fn malformed(detail: impl Into<String>) -> MimirError {
    parse_error("malformed", detail)
}

fn mapping_error(detail: impl Into<String>) -> MimirError {
    MimirError::message(format!("replay header mapping error: {}", detail.into()))
}

// R3.18AK BEGIN bounded post-AG following-header composition
const R3_18AJ_POST_AG_HEADER_CONTEXTS_V1: [(
    u32,
    u8,
    u32,
    ReplayNetworkAttributeTagV1,
    i32,
    i32,
    i32,
); 17] = [
    (60, 5, 38, ReplayNetworkAttributeTagV1::Int, 868, 32, 10),
    (60, 5, 47, ReplayNetworkAttributeTagV1::Int, 868, 32, 10),
    (60, 5, 84, ReplayNetworkAttributeTagV1::Int, 868, 32, 10),
    (60, 5, 85, ReplayNetworkAttributeTagV1::Int, 868, 32, 10),
    (60, 5, 91, ReplayNetworkAttributeTagV1::Int, 868, 32, 10),
    (60, 5, 93, ReplayNetworkAttributeTagV1::Int, 868, 32, 10),
    (60, 5, 95, ReplayNetworkAttributeTagV1::Int, 868, 32, 10),
    (60, 5, 100, ReplayNetworkAttributeTagV1::Int, 868, 32, 10),
    (60, 5, 106, ReplayNetworkAttributeTagV1::Int, 868, 32, 10),
    (60, 5, 108, ReplayNetworkAttributeTagV1::Int, 868, 32, 10),
    (60, 5, 109, ReplayNetworkAttributeTagV1::Int, 868, 32, 10),
    (60, 5, 112, ReplayNetworkAttributeTagV1::Int, 868, 32, 10),
    (60, 5, 122, ReplayNetworkAttributeTagV1::Int, 868, 32, 10),
    (67, 6, 68, ReplayNetworkAttributeTagV1::Int, 868, 32, 10),
    (72, 6, 70, ReplayNetworkAttributeTagV1::Int, 868, 32, 10),
    (72, 6, 73, ReplayNetworkAttributeTagV1::Int, 868, 32, 10),
    (110, 6, 37, ReplayNetworkAttributeTagV1::Int, 868, 32, 10),
];

fn r3_18aj_post_ag_header_context_contains_v1(
    stream_id_bound: u32,
    prop_id_bits: u8,
    property_object_index: u32,
    attribute_tag: ReplayNetworkAttributeTagV1,
    context: ReplayNetworkK3DecodeContextV1,
) -> bool {
    R3_18AJ_POST_AG_HEADER_CONTEXTS_V1.contains(&(
        stream_id_bound,
        prop_id_bits,
        property_object_index,
        attribute_tag,
        context.version_major,
        context.version_minor,
        context.net_version,
    ))
}

/// Exactly one R3.18AJ-admitted property header after a valid published R3.18AG true control.
///
/// The supplied R3.18AG control is recomputed from the R3.18AD payload prior and must match
/// exactly. The existing stateless property-header primitive is then replayed from the same
/// property-present coordinate. This result stops at `payload_start` and consumes no payload or
/// later property-control bit.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderV1 {
    pub control: ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlV1,
    pub following_header: ReplayNetworkExistingActorFirstPropertyHeaderV1,
    pub stop_bit: u64,
}

fn network_existing_actor_post_ag_following_header_error(
    category: &str,
    detail: impl Into<String>,
) -> MimirError {
    MimirError::message(format!(
        "replay network post-AG following-header error: {category}: {}",
        detail.into()
    ))
}

/// Compose exactly one R3.18AJ-admitted post-AG following header through `payload_start`.
///
/// This function is deliberately boundary-specific. It validates the supplied R3.18AG result by
/// recomputing it from the exact R3.18AD prior, reuses the existing stateless header primitive,
/// requires full seven-field R3.18AJ tuple membership, and exposes no payload decoder, later
/// control bit, property iterator, or reusable cursor.
pub fn decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_v1(
    network_bytes: &[u8],
    prior: &ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadV1,
    control: &ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlV1,
    lookup_plan: &ReplayNetworkLookupPlanV1,
    context: ReplayNetworkK3DecodeContextV1,
) -> Result<ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderV1>{
    let expected_control = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_v1(
        network_bytes,
        prior,
        context,
    )?;
    if expected_control != *control {
        return Err(network_existing_actor_post_ag_following_header_error(
            "invalid-r3-18ag-control",
            format!(
                "supplied R3.18AG control {:?} differs from recomputed {:?}",
                control, expected_control
            ),
        ));
    }
    if !control.following_property_present {
        return Err(network_existing_actor_post_ag_following_header_error(
            "invalid-r3-18ag-control",
            "R3.18AK requires the published R3.18AG admitted true control",
        ));
    }
    if control.property_present_start_bit != prior.stop_bit
        || control.property_present_end_bit != control.stop_bit
        || control.property_present_end_bit != control.property_present_start_bit + 1
    {
        return Err(network_existing_actor_post_ag_following_header_error(
            "control-boundary-mismatch",
            format!(
                "prior stop {}, control [{}, {}) stop {}",
                prior.stop_bit,
                control.property_present_start_bit,
                control.property_present_end_bit,
                control.stop_bit,
            ),
        ));
    }

    let actor_object_index = prior.header_composition.following_header.actor_object_index;
    let following_header = decode_replay_network_existing_actor_first_property_header_v1(
        network_bytes,
        control.property_present_start_bit,
        actor_object_index,
        lookup_plan,
    )?;
    if !following_header.property_present {
        return Err(network_existing_actor_post_ag_following_header_error(
            "control-header-mismatch",
            "R3.18AG reported a present property but the post-AG header primitive did not",
        ));
    }
    if following_header.property_present_start_bit != control.property_present_start_bit
        || following_header.property_present_end_bit != control.property_present_end_bit
        || control.stop_bit != following_header.property_present_end_bit
    {
        return Err(network_existing_actor_post_ag_following_header_error(
            "control-header-boundary-mismatch",
            format!(
                "control bits [{}, {}) stop {}, header bits [{}, {})",
                control.property_present_start_bit,
                control.property_present_end_bit,
                control.stop_bit,
                following_header.property_present_start_bit,
                following_header.property_present_end_bit,
            ),
        ));
    }
    if following_header.actor_object_index != actor_object_index {
        return Err(network_existing_actor_post_ag_following_header_error(
            "actor-mismatch",
            format!(
                "prior actor {actor_object_index} differs from post-AG header actor {}",
                following_header.actor_object_index,
            ),
        ));
    }

    let payload_start_bit = following_header.payload_start_bit.ok_or_else(|| {
        network_existing_actor_post_ag_following_header_error(
            "missing-payload-start",
            "present post-AG header has no payload start",
        )
    })?;
    if following_header.stop_bit != payload_start_bit {
        return Err(network_existing_actor_post_ag_following_header_error(
            "payload-boundary-mismatch",
            format!(
                "post-AG header stop {} differs from payload start {payload_start_bit}",
                following_header.stop_bit,
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
        return Err(network_existing_actor_post_ag_following_header_error(
            "incomplete-r3-18aj-header-context",
            "post-AG header is missing one or more R3.18AJ tuple fields",
        ));
    };
    if !r3_18aj_post_ag_header_context_contains_v1(
        stream_id_bound,
        prop_id_bits,
        property_object_index,
        attribute_tag,
        context,
    ) {
        return Err(network_existing_actor_post_ag_following_header_error(
            "unadmitted-r3-18aj-header-context",
            format!(
                "R3.18AJ exact tuple rejected bound={stream_id_bound} bits={prop_id_bits} object={property_object_index} tag={attribute_tag:?} version={}.{} net{}",
                context.version_major, context.version_minor, context.net_version,
            ),
        ));
    }

    Ok(ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderV1 {
        control: control.clone(),
        following_header,
        stop_bit: payload_start_bit,
    })
}
// R3.18AK END bounded post-AG following-header composition

#[cfg(test)]
mod tests {
    use super::*;

    fn r3_14d_append_bit(bytes: &mut Vec<u8>, bit_position: &mut usize, value: bool) {
        let byte_index = *bit_position / 8;
        let bit_index = *bit_position % 8;
        if byte_index == bytes.len() {
            bytes.push(0);
        }
        if value {
            bytes[byte_index] |= 1 << bit_index;
        }
        *bit_position += 1;
    }

    fn r3_14d_append_bits(bytes: &mut Vec<u8>, bit_position: &mut usize, value: u64, width: usize) {
        for bit in 0..width {
            r3_14d_append_bit(bytes, bit_position, ((value >> bit) & 1) != 0);
        }
    }

    fn r3_14d_append_bounded(
        bytes: &mut Vec<u8>,
        bit_position: &mut usize,
        value: u32,
        max_exclusive: u32,
        low_width: u8,
    ) {
        let range = 1u64 << low_width;
        let low = u64::from(value) & (range - 1);
        r3_14d_append_bits(bytes, bit_position, low, usize::from(low_width));
        if low + range < u64::from(max_exclusive) {
            r3_14d_append_bit(bytes, bit_position, u64::from(value) >= range);
        }
    }

    fn r3_14d_network_prefix(time: f32, delta: f32) -> (Vec<u8>, usize) {
        let mut bytes = Vec::with_capacity(16);
        bytes.extend_from_slice(&time.to_bits().to_le_bytes());
        bytes.extend_from_slice(&delta.to_bits().to_le_bytes());
        (bytes, 64)
    }

    #[test]
    fn r3_14d_consumes_timing_raw_bits_through_native_cursor() {
        let time = 1.25f32;
        let delta = 0.008f32;
        let (mut network, mut bit) = r3_14d_network_prefix(time, delta);
        r3_14d_append_bit(&mut network, &mut bit, false);

        let decoded =
            decode_network_first_actor_header(&network, 2047, 10, time.to_bits(), delta.to_bits())
                .expect("timing + absent actor envelope should decode");
        assert_eq!(decoded.time_raw_u32, time.to_bits());
        assert_eq!(decoded.delta_raw_u32, delta.to_bits());
        assert_eq!(decoded.stop_bit, 65);
    }

    #[test]
    fn r3_14d_rejects_timing_raw_bit_mismatch() {
        let time = 1.25f32;
        let delta = 0.008f32;
        let (mut network, mut bit) = r3_14d_network_prefix(time, delta);
        r3_14d_append_bit(&mut network, &mut bit, false);
        let error = decode_network_first_actor_header(
            &network,
            2047,
            10,
            2.0f32.to_bits(),
            delta.to_bits(),
        )
        .expect_err("timing raw mismatch must fail closed");
        assert_error_contains(
            error,
            "replay network first actor envelope error: timing-mismatch",
        );
    }

    #[test]
    fn r3_14d_actor_absent_branch_stops_at_65_and_preserves_none_fields() {
        let (mut network, mut bit) = r3_14d_network_prefix(1.0, 0.01);
        r3_14d_append_bit(&mut network, &mut bit, false);
        let decoded = decode_network_first_actor_header(
            &network,
            2047,
            10,
            1.0f32.to_bits(),
            0.01f32.to_bits(),
        )
        .expect("actor absent branch");
        assert!(!decoded.actor_present);
        assert_eq!(decoded.actor_id, None);
        assert_eq!(decoded.alive, None);
        assert_eq!(decoded.is_new, None);
        assert_eq!(decoded.stop_bit, 65);
    }

    #[test]
    fn r3_14d_alive_false_branch_stops_before_new() {
        let (mut network, mut bit) = r3_14d_network_prefix(1.0, 0.01);
        r3_14d_append_bit(&mut network, &mut bit, true);
        r3_14d_append_bounded(&mut network, &mut bit, 0, 2047, 10);
        r3_14d_append_bit(&mut network, &mut bit, false);
        let decoded = decode_network_first_actor_header(
            &network,
            2047,
            10,
            1.0f32.to_bits(),
            0.01f32.to_bits(),
        )
        .expect("alive false branch");
        assert_eq!(decoded.actor_id, Some(0));
        assert_eq!(decoded.alive, Some(false));
        assert_eq!(decoded.is_new, None);
        assert_eq!(decoded.stop_bit, 77);
    }

    #[test]
    fn r3_14d_alive_true_new_false_branch_stops_after_new() {
        let (mut network, mut bit) = r3_14d_network_prefix(1.0, 0.01);
        r3_14d_append_bit(&mut network, &mut bit, true);
        r3_14d_append_bounded(&mut network, &mut bit, 0, 2047, 10);
        r3_14d_append_bit(&mut network, &mut bit, true);
        r3_14d_append_bit(&mut network, &mut bit, false);
        let decoded = decode_network_first_actor_header(
            &network,
            2047,
            10,
            1.0f32.to_bits(),
            0.01f32.to_bits(),
        )
        .expect("new false branch");
        assert_eq!(decoded.actor_id, Some(0));
        assert_eq!(decoded.alive, Some(true));
        assert_eq!(decoded.is_new, Some(false));
        assert_eq!(decoded.stop_bit, 78);
    }

    #[test]
    fn r3_14d_alive_true_new_true_branch_stops_at_r3_14a_boundary() {
        let (mut network, mut bit) = r3_14d_network_prefix(1.0, 0.01);
        r3_14d_append_bit(&mut network, &mut bit, true);
        r3_14d_append_bounded(&mut network, &mut bit, 0, 2047, 10);
        r3_14d_append_bit(&mut network, &mut bit, true);
        r3_14d_append_bit(&mut network, &mut bit, true);
        r3_14d_append_bits(&mut network, &mut bit, 0b11_1111, 6);
        let decoded = decode_network_first_actor_header(
            &network,
            2047,
            10,
            1.0f32.to_bits(),
            0.01f32.to_bits(),
        )
        .expect("new true branch");
        assert_eq!(decoded.actor_id, Some(0));
        assert_eq!(decoded.alive, Some(true));
        assert_eq!(decoded.is_new, Some(true));
        assert_eq!(decoded.stop_bit, 78);
    }

    #[test]
    fn r3_14d_bounded_actor_id_discriminator_zero_path() {
        let (mut network, mut bit) = r3_14d_network_prefix(1.0, 0.01);
        r3_14d_append_bit(&mut network, &mut bit, true);
        r3_14d_append_bounded(&mut network, &mut bit, 0, 2047, 10);
        r3_14d_append_bit(&mut network, &mut bit, false);
        let decoded = decode_network_first_actor_header(
            &network,
            2047,
            10,
            1.0f32.to_bits(),
            0.01f32.to_bits(),
        )
        .expect("discriminator zero path");
        assert_eq!(decoded.actor_id, Some(0));
        assert_eq!(decoded.stop_bit, 77);
    }

    #[test]
    fn r3_14d_bounded_actor_id_discriminator_one_path() {
        let (mut network, mut bit) = r3_14d_network_prefix(1.0, 0.01);
        r3_14d_append_bit(&mut network, &mut bit, true);
        r3_14d_append_bounded(&mut network, &mut bit, 1024, 2047, 10);
        r3_14d_append_bit(&mut network, &mut bit, false);
        let decoded = decode_network_first_actor_header(
            &network,
            2047,
            10,
            1.0f32.to_bits(),
            0.01f32.to_bits(),
        )
        .expect("discriminator one path");
        assert_eq!(decoded.actor_id, Some(1024));
        assert_eq!(decoded.stop_bit, 77);
    }

    #[test]
    fn r3_14d_bounded_actor_id_threshold_skips_discriminator() {
        let (mut network, mut bit) = r3_14d_network_prefix(1.0, 0.01);
        r3_14d_append_bit(&mut network, &mut bit, true);
        r3_14d_append_bounded(&mut network, &mut bit, 1023, 2047, 10);
        r3_14d_append_bit(&mut network, &mut bit, false);
        let decoded = decode_network_first_actor_header(
            &network,
            2047,
            10,
            1.0f32.to_bits(),
            0.01f32.to_bits(),
        )
        .expect("threshold path");
        assert_eq!(decoded.actor_id, Some(1023));
        assert_eq!(decoded.stop_bit, 76);
    }

    #[test]
    fn r3_14d_missing_actor_present_fails() {
        let (network, _) = r3_14d_network_prefix(1.0, 0.01);
        let error = decode_network_first_actor_header(
            &network,
            2047,
            10,
            1.0f32.to_bits(),
            0.01f32.to_bits(),
        )
        .expect_err("actor_present is required after timing");
        assert_error_contains(
            error,
            "replay network first actor envelope error: actor-present",
        );
    }

    #[test]
    fn r3_14d_truncated_actor_id_low_bits_fail() {
        let (mut network, mut bit) = r3_14d_network_prefix(1.0, 0.01);
        r3_14d_append_bit(&mut network, &mut bit, true);
        // One extra byte provides only seven bits after actor_present, fewer than low_width=10.
        while network.len() < 9 {
            network.push(0);
        }
        let error = decode_network_first_actor_header(
            &network,
            2047,
            10,
            1.0f32.to_bits(),
            0.01f32.to_bits(),
        )
        .expect_err("actor id low bits are truncated");
        assert_error_contains(error, "replay network first actor envelope error: actor-id");
    }

    #[test]
    fn r3_14d_missing_required_actor_id_discriminator_fails() {
        let (mut network, mut bit) = r3_14d_network_prefix(1.0, 0.01);
        r3_14d_append_bit(&mut network, &mut bit, true);
        r3_14d_append_bits(&mut network, &mut bit, 0, 7);
        assert_eq!(bit, 72);
        let error = decode_network_first_actor_header(
            &network,
            255,
            7,
            1.0f32.to_bits(),
            0.01f32.to_bits(),
        )
        .expect_err("required bounded discriminator is truncated at byte end");
        assert_error_contains(error, "replay network first actor envelope error: actor-id");
    }

    #[test]
    fn r3_14d_missing_alive_fails() {
        let (mut network, mut bit) = r3_14d_network_prefix(1.0, 0.01);
        r3_14d_append_bit(&mut network, &mut bit, true);
        r3_14d_append_bits(&mut network, &mut bit, 0, 7);
        assert_eq!(bit, 72);
        let error = decode_network_first_actor_header(
            &network,
            128,
            7,
            1.0f32.to_bits(),
            0.01f32.to_bits(),
        )
        .expect_err("alive bit is truncated at byte end");
        assert_error_contains(error, "replay network first actor envelope error: alive");
    }

    #[test]
    fn r3_14d_missing_new_when_alive_true_fails() {
        let (mut network, mut bit) = r3_14d_network_prefix(1.0, 0.01);
        r3_14d_append_bit(&mut network, &mut bit, true);
        r3_14d_append_bits(&mut network, &mut bit, 0, 6);
        r3_14d_append_bit(&mut network, &mut bit, true);
        assert_eq!(bit, 72);
        let error =
            decode_network_first_actor_header(&network, 64, 6, 1.0f32.to_bits(), 0.01f32.to_bits())
                .expect_err("new bit is truncated at byte end");
        assert_error_contains(error, "replay network first actor envelope error: new");
    }

    #[test]
    fn r3_14d_public_reader_rejects_file_input() {
        let error = MinimalReplayNetworkFirstActorEnvelopeReader
            .read_network_first_actor_envelope(&ReplayInput::file("sample.replay"))
            .expect_err("file input remains outside first actor-envelope reader");
        assert_error_contains(
            error,
            "replay network first actor envelope error: unsupported-input",
        );
    }

    #[test]
    fn r3_14d_public_reader_preserves_terminal_first_frame_rejection() {
        let Some(mut bytes) = load_fixture_bytes_or_skip(FIXTURE_001_PATH, FIXTURE_001_LABEL)
        else {
            return;
        };
        mutate_first_network_timing(&mut bytes, 0.0, 0.0);
        let error = MinimalReplayNetworkFirstActorEnvelopeReader
            .read_network_first_actor_envelope(&ReplayInput::Memory {
                label: FIXTURE_001_LABEL.to_string(),
                bytes,
            })
            .expect_err("terminal first frame must fail before actor parsing");
        assert_error_contains(error, "replay network timing error: terminal-first-frame");
    }

    #[test]
    fn r3_14d_public_reader_matches_three_historical_fixtures_through_new_only() {
        for (path, label) in [
            (FIXTURE_001_PATH, FIXTURE_001_LABEL),
            (FIXTURE_002_PATH, FIXTURE_002_LABEL),
            (FIXTURE_003_PATH, FIXTURE_003_LABEL),
        ] {
            let Some(bytes) = load_fixture_bytes_or_skip(path, label) else {
                return;
            };
            let envelope = MinimalReplayNetworkFirstActorEnvelopeReader
                .read_network_first_actor_envelope(&ReplayInput::Memory {
                    label: label.to_string(),
                    bytes,
                })
                .expect("historical admitted fixture should expose first actor envelope");
            assert_eq!(
                envelope.first_frame_time_raw_u32,
                envelope.timing.first_frame_time.to_bits()
            );
            assert_eq!(
                envelope.first_frame_delta_raw_u32,
                envelope.timing.first_frame_delta.to_bits()
            );
            assert!(envelope.actor_present);
            assert_eq!(envelope.actor_id, Some(0));
            assert_eq!(envelope.alive, Some(true));
            assert_eq!(envelope.is_new, Some(true));
            assert_eq!(envelope.stop_bit, 78);
        }
    }

    #[test]
    fn r3_14c_bit_cursor_reads_lsb_first_within_byte() {
        let mut cursor = NetworkBitCursor::new(&[0b1010_0110]);
        let observed = [
            cursor.read_bit().expect("bit 0"),
            cursor.read_bit().expect("bit 1"),
            cursor.read_bit().expect("bit 2"),
            cursor.read_bit().expect("bit 3"),
            cursor.read_bit().expect("bit 4"),
            cursor.read_bit().expect("bit 5"),
            cursor.read_bit().expect("bit 6"),
            cursor.read_bit().expect("bit 7"),
        ];
        assert_eq!(
            observed,
            [false, true, true, false, false, true, false, true]
        );
        assert_eq!(cursor.position_bits(), 8);
        assert_eq!(cursor.remaining_bits(), 0);
    }

    #[test]
    fn r3_14c_bit_cursor_reads_across_byte_boundary() {
        let mut cursor = NetworkBitCursor::new(&[0b1111_0000, 0b0000_0011]);
        assert_eq!(cursor.read_bits_le(4).expect("prefix"), 0);
        assert_eq!(cursor.read_bits_le(8).expect("cross-byte value"), 0x3f);
        assert_eq!(cursor.position_bits(), 12);
        assert_eq!(cursor.remaining_bits(), 4);
    }

    #[test]
    fn r3_14c_bit_cursor_tracks_mixed_width_positions() {
        let mut cursor = NetworkBitCursor::new(&[0b1101_0110, 0b0000_0001]);
        assert_eq!(cursor.read_bits_le(3).expect("first"), 6);
        assert_eq!(cursor.position_bits(), 3);
        assert_eq!(cursor.read_bits_le(2).expect("second"), 2);
        assert_eq!(cursor.position_bits(), 5);
        assert_eq!(cursor.read_bits_le(4).expect("third"), 14);
        assert_eq!(cursor.position_bits(), 9);
        assert_eq!(cursor.remaining_bits(), 7);
    }

    #[test]
    fn r3_14c_bit_cursor_zero_width_is_noop() {
        let mut cursor = NetworkBitCursor::new(&[0xff]);
        assert_eq!(cursor.read_bits_le(0).expect("zero width"), 0);
        assert_eq!(cursor.position_bits(), 0);
        assert_eq!(cursor.remaining_bits(), 8);
    }

    #[test]
    fn r3_14c_bit_cursor_width_64_consumes_exactly_64_bits() {
        let bytes = [0xff; 8];
        let mut cursor = NetworkBitCursor::new(&bytes);
        assert_eq!(cursor.read_bits_le(64).expect("64-bit read"), u64::MAX);
        assert_eq!(cursor.position_bits(), 64);
        assert_eq!(cursor.remaining_bits(), 0);
    }

    #[test]
    fn r3_14c_bit_cursor_width_above_64_fails_atomically() {
        let mut cursor = NetworkBitCursor::new(&[0xff; 9]);
        let before = cursor.position_bits();
        let error = cursor
            .read_bits_le(65)
            .expect_err("width 65 must be rejected");
        assert_eq!(cursor.position_bits(), before);
        assert!(error.to_string().contains("invalid-width"));
    }

    #[test]
    fn r3_14c_bit_cursor_empty_read_bit_fails_atomically() {
        let mut cursor = NetworkBitCursor::new(&[]);
        let before = cursor.position_bits();
        let error = cursor.read_bit().expect_err("empty cursor must fail");
        assert_eq!(cursor.position_bits(), before);
        assert!(error.to_string().contains("insufficient-bits"));
    }

    #[test]
    fn r3_14c_bit_cursor_insufficient_multibit_read_fails_atomically() {
        let mut cursor = NetworkBitCursor::new(&[0xff]);
        let before = cursor.position_bits();
        let error = cursor
            .read_bits_le(9)
            .expect_err("nine bits from one byte must fail");
        assert_eq!(cursor.position_bits(), before);
        assert!(error.to_string().contains("insufficient-bits"));
    }

    #[test]
    fn r3_14c_bounded_u32_zero_maximum_fails_atomically() {
        let mut cursor = NetworkBitCursor::new(&[0xff]);
        let before = cursor.position_bits();
        let error = cursor
            .read_bounded_u32(0, 0)
            .expect_err("zero maximum must fail");
        assert_eq!(cursor.position_bits(), before);
        assert!(error.to_string().contains("invalid-maximum"));
    }

    #[test]
    fn r3_14c_bounded_u32_maximum_one_returns_zero_without_reading() {
        let mut cursor = NetworkBitCursor::new(&[]);
        assert_eq!(
            cursor.read_bounded_u32(1, 0).expect("only zero is valid"),
            0
        );
        assert_eq!(cursor.position_bits(), 0);
        assert_eq!(cursor.remaining_bits(), 0);
    }

    #[test]
    fn r3_14c_bounded_u32_r3_14a_vector_discriminator_zero() {
        let mut cursor = NetworkBitCursor::new(&[0x00, 0x00]);
        assert_eq!(
            cursor
                .read_bounded_u32(2047, 10)
                .expect("R3.14A actor-id vector"),
            0
        );
        assert_eq!(cursor.position_bits(), 11);
    }

    #[test]
    fn r3_14c_bounded_u32_matches_all_47_r3_14a_actor_id_vectors() {
        for row_index in 0..47 {
            let mut cursor = NetworkBitCursor::new(&[0x00, 0x00]);
            let value = cursor
                .read_bounded_u32(2047, 10)
                .unwrap_or_else(|error| panic!("R3.14A row {row_index} failed: {error}"));
            assert_eq!(value, 0, "R3.14A row {row_index} value drift");
            assert_eq!(
                cursor.position_bits(),
                11,
                "R3.14A row {row_index} end-bit drift"
            );
        }
    }

    #[test]
    fn r3_14c_bounded_u32_discriminator_one_selects_upper_value() {
        let mut cursor = NetworkBitCursor::new(&[0x00, 0x04]);
        assert_eq!(
            cursor
                .read_bounded_u32(2047, 10)
                .expect("upper actor-id branch"),
            1024
        );
        assert_eq!(cursor.position_bits(), 11);
    }

    #[test]
    fn r3_14c_bounded_u32_threshold_skips_discriminator() {
        let mut cursor = NetworkBitCursor::new(&[0xff, 0x03]);
        assert_eq!(
            cursor
                .read_bounded_u32(2047, 10)
                .expect("threshold low value"),
            1023
        );
        assert_eq!(cursor.position_bits(), 10);
        assert_eq!(cursor.remaining_bits(), 6);
    }

    #[test]
    fn r3_14c_bounded_u32_missing_discriminator_fails_atomically() {
        let mut cursor = NetworkBitCursor::new(&[0x00, 0x00]);
        assert_eq!(cursor.read_bits_le(6).expect("prefix"), 0);
        let before = cursor.position_bits();
        let error = cursor
            .read_bounded_u32(2047, 10)
            .expect_err("required discriminator is missing");
        assert_eq!(cursor.position_bits(), before);
        assert!(error.to_string().contains("insufficient-bits"));
    }

    #[test]
    fn r3_14c_bounded_u32_back_to_back_reads_stay_aligned() {
        let mut cursor = NetworkBitCursor::new(&[0b0000_0110]);
        assert_eq!(cursor.read_bounded_u32(3, 1).expect("first"), 2);
        assert_eq!(cursor.position_bits(), 2);
        assert_eq!(cursor.read_bounded_u32(3, 1).expect("second"), 1);
        assert_eq!(cursor.position_bits(), 3);
    }

    #[test]
    fn r3_14c_bounded_u32_admitted_synthetic_outputs_stay_below_maximum() {
        let cases = [
            ([0x00, 0x00], 0u32),
            ([0x00, 0x04], 1024u32),
            ([0xff, 0x03], 1023u32),
        ];
        for (bytes, expected) in cases {
            let mut cursor = NetworkBitCursor::new(&bytes);
            let value = cursor
                .read_bounded_u32(2047, 10)
                .expect("synthetic bounded value");
            assert_eq!(value, expected);
            assert!(value < 2047);
        }
    }

    #[test]
    fn r3_14c_bounded_u32_low_width_above_32_fails_atomically() {
        let mut cursor = NetworkBitCursor::new(&[0xff; 8]);
        let before = cursor.position_bits();
        let error = cursor
            .read_bounded_u32(u32::MAX, 33)
            .expect_err("low width above 32 must fail");
        assert_eq!(cursor.position_bits(), before);
        assert!(error.to_string().contains("invalid-low-width"));
    }

    #[test]
    fn r3_14c_bounded_u32_impossible_range_fails_atomically() {
        let mut cursor = NetworkBitCursor::new(&[0xff]);
        let before = cursor.position_bits();
        let error = cursor
            .read_bounded_u32(3, 2)
            .expect_err("range larger than maximum must fail");
        assert_eq!(cursor.position_bits(), before);
        assert!(error.to_string().contains("invalid-configuration"));
    }
    use std::fs;
    use std::path::PathBuf;

    const FIXTURE_001_LABEL: &str = "rl_replay_header_fixture_001";
    const FIXTURE_001_PATH: &str = concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../external_fixtures/sample_001.replay"
    );
    const FIXTURE_002_LABEL: &str = "rl_replay_header_fixture_002";
    const FIXTURE_002_PATH: &str = concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../external_fixtures/sample_002.replay"
    );
    const FIXTURE_003_LABEL: &str = "rl_replay_header_fixture_003";
    const FIXTURE_003_PATH: &str = concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../external_fixtures/sample_003.replay"
    );

    #[test]
    fn supported_build_version_registry_v1_contains_only_expected_exact_entries() {
        assert_eq!(
            SUPPORTED_BUILD_VERSIONS_V1,
            [
                SUPPORTED_BUILD_VERSION_FIXTURE_001,
                SUPPORTED_BUILD_VERSION_FIXTURE_002,
                SUPPORTED_BUILD_VERSION_FIXTURE_003,
                SUPPORTED_BUILD_VERSION_CORPUS_RANK_001,
                SUPPORTED_BUILD_VERSION_CORPUS_RANK_002,
                SUPPORTED_BUILD_VERSION_CORPUS_RANK_003,
                SUPPORTED_BUILD_VERSION_CORPUS_RANK_004,
                SUPPORTED_BUILD_VERSION_CORPUS_RANK_005,
                SUPPORTED_BUILD_VERSION_CORPUS_RANK_006,
                SUPPORTED_BUILD_VERSION_CORPUS_RANK_007,
                SUPPORTED_BUILD_VERSION_CORPUS_RANK_008,
                SUPPORTED_BUILD_VERSION_CORPUS_RANK_009,
                SUPPORTED_BUILD_VERSION_CORPUS_RANK_010,
            ]
        );
    }

    #[test]
    fn supported_build_version_registry_v1_has_no_duplicates() {
        let unique: BTreeSet<_> = SUPPORTED_BUILD_VERSIONS_V1.iter().copied().collect();
        assert_eq!(unique.len(), SUPPORTED_BUILD_VERSIONS_V1.len());
    }
    #[test]
    fn minimal_body_boundary_reader_matches_three_historical_fixtures() {
        let cases = [
            (
                FIXTURE_001_PATH,
                FIXTURE_001_LABEL,
                13_200u32,
                13_208u64,
                2_987_805u32,
                2_323_044_833u32,
                13_216u64,
                3_001_021u64,
            ),
            (
                FIXTURE_002_PATH,
                FIXTURE_002_LABEL,
                11_273u32,
                11_281u64,
                2_621_614u32,
                3_734_167_123u32,
                11_289u64,
                2_632_903u64,
            ),
            (
                FIXTURE_003_PATH,
                FIXTURE_003_LABEL,
                11_190u32,
                11_198u64,
                1_627_332u32,
                3_991_282_011u32,
                11_206u64,
                1_638_538u64,
            ),
        ];

        for (
            path,
            label,
            header_size,
            header_end,
            content_size,
            content_crc,
            content_start,
            input_len,
        ) in cases
        {
            let Some(bytes) = load_fixture_bytes_or_skip(path, label) else {
                return;
            };
            let boundary = MinimalReplayBodyBoundaryReader
                .read_body_boundary(&ReplayInput::Memory {
                    label: label.to_string(),
                    bytes,
                })
                .expect("historical fixture body boundary should be structurally valid");

            assert_eq!(boundary.source_label, label);
            assert_eq!(boundary.header_size, header_size);
            assert_eq!(boundary.header_end, header_end);
            assert_eq!(boundary.content_size, content_size);
            assert_eq!(boundary.content_crc, content_crc);
            assert_eq!(boundary.content_start, content_start);
            assert_eq!(boundary.content_end, input_len);
            assert_eq!(boundary.input_len, input_len);
        }
    }

    #[test]
    fn minimal_body_boundary_reader_exactly_frames_checked_in_largest_100_corpus() {
        let root = PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("../../test_corpus/largest_100");
        if !root.is_dir() {
            eprintln!("skipping largest_100 body-boundary regression; corpus root is absent");
            return;
        }

        let mut replay_paths = fs::read_dir(&root)
            .expect("largest_100 corpus directory should be readable")
            .map(|entry| {
                entry
                    .expect("corpus directory entry should be readable")
                    .path()
            })
            .filter(|path| path.extension().and_then(|value| value.to_str()) == Some("replay"))
            .collect::<Vec<_>>();
        replay_paths.sort();
        assert_eq!(replay_paths.len(), 100);

        for path in replay_paths {
            let bytes = fs::read(&path).expect("checked-in corpus replay should be readable");
            let label = path
                .file_name()
                .expect("corpus replay should have a file name")
                .to_string_lossy()
                .into_owned();
            let boundary = MinimalReplayBodyBoundaryReader
                .read_body_boundary(&ReplayInput::Memory {
                    label: label.clone(),
                    bytes,
                })
                .unwrap_or_else(|error| panic!("body boundary failed for {label}: {error}"));
            assert_eq!(boundary.source_label, label);
            assert_eq!(boundary.content_end, boundary.input_len);
        }
    }

    #[test]
    fn minimal_body_boundary_reader_rejects_file_input() {
        let error = MinimalReplayBodyBoundaryReader
            .read_body_boundary(&ReplayInput::file("sample.replay"))
            .expect_err("file input remains outside the body-boundary reader");
        assert_error_contains(error, "replay body boundary error: unsupported-input");
    }

    #[test]
    fn minimal_body_boundary_reader_rejects_empty_memory_label() {
        let bytes = build_body_boundary_bytes(&[], 0, 0, &[]);
        let error = MinimalReplayBodyBoundaryReader
            .read_body_boundary(&ReplayInput::Memory {
                label: String::new(),
                bytes,
            })
            .expect_err("empty source labels are not admitted");
        assert_error_contains(error, "replay body boundary error: mapping");
    }

    #[test]
    fn minimal_body_boundary_reader_rejects_truncated_preamble() {
        let error = MinimalReplayBodyBoundaryReader
            .read_body_boundary(&ReplayInput::Memory {
                label: "synthetic".to_string(),
                bytes: vec![0; 7],
            })
            .expect_err("an eight-byte replay preamble is required");
        assert_error_contains(error, "replay body boundary error: insufficient");
    }

    #[test]
    fn minimal_body_boundary_reader_rejects_negative_header_size() {
        let mut bytes = Vec::new();
        bytes.extend_from_slice(&(-1i32).to_le_bytes());
        bytes.extend_from_slice(&0u32.to_le_bytes());
        let error = MinimalReplayBodyBoundaryReader
            .read_body_boundary(&ReplayInput::Memory {
                label: "synthetic".to_string(),
                bytes,
            })
            .expect_err("negative header_size is malformed");
        assert_error_contains(error, "replay body boundary error: malformed");
    }

    #[test]
    fn minimal_body_boundary_reader_rejects_truncated_content_framing() {
        let mut bytes = Vec::new();
        bytes.extend_from_slice(&0i32.to_le_bytes());
        bytes.extend_from_slice(&0u32.to_le_bytes());
        bytes.extend_from_slice(&0i32.to_le_bytes());
        let error = MinimalReplayBodyBoundaryReader
            .read_body_boundary(&ReplayInput::Memory {
                label: "synthetic".to_string(),
                bytes,
            })
            .expect_err("content_size without content_crc is truncated framing");
        assert_error_contains(error, "replay body boundary error: insufficient");
    }

    #[test]
    fn minimal_body_boundary_reader_rejects_negative_content_size() {
        let bytes = build_body_boundary_bytes(&[], 0, -1, &[]);
        let error = MinimalReplayBodyBoundaryReader
            .read_body_boundary(&ReplayInput::Memory {
                label: "synthetic".to_string(),
                bytes,
            })
            .expect_err("negative content_size is malformed");
        assert_error_contains(error, "replay body boundary error: malformed");
    }

    #[test]
    fn minimal_body_boundary_reader_rejects_content_size_beyond_input() {
        let bytes = build_body_boundary_bytes(&[1, 2, 3], 0, 4, &[9, 8, 7]);
        let error = MinimalReplayBodyBoundaryReader
            .read_body_boundary(&ReplayInput::Memory {
                label: "synthetic".to_string(),
                bytes,
            })
            .expect_err("declared content beyond input is insufficient");
        assert_error_contains(error, "replay body boundary error: insufficient");
    }

    #[test]
    fn minimal_body_boundary_reader_rejects_trailing_bytes_after_content() {
        let mut bytes = build_body_boundary_bytes(&[1, 2], 0, 2, &[3, 4]);
        bytes.push(5);
        let error = MinimalReplayBodyBoundaryReader
            .read_body_boundary(&ReplayInput::Memory {
                label: "synthetic".to_string(),
                bytes,
            })
            .expect_err("bytes after declared content are malformed framing");
        assert_error_contains(error, "replay body boundary error: malformed");
    }

    #[test]
    fn minimal_body_boundary_reader_reports_crc_without_validating_it() {
        let bytes = build_body_boundary_bytes(&[0xAA; 12], 0xDEADBEEF, 3, &[1, 2, 3]);
        let boundary = MinimalReplayBodyBoundaryReader
            .read_body_boundary(&ReplayInput::Memory {
                label: "synthetic".to_string(),
                bytes,
            })
            .expect("arbitrary stored CRC must not be validated in this pass");
        assert_eq!(boundary.content_crc, 0xDEADBEEF);
        assert_eq!(boundary.content_size, 3);
        assert_eq!(boundary.content_end, boundary.input_len);
    }

    #[test]
    fn minimal_content_scaffold_reader_matches_three_historical_fixtures() {
        let cases = [
            (
                FIXTURE_001_PATH,
                FIXTURE_001_LABEL,
                13_216u64,
                1u32,
                13_246u64,
                64u32,
                14_018u64,
                2_954_240u32,
                14_022u64,
                2_968_262u64,
                32_759u64,
            ),
            (
                FIXTURE_002_PATH,
                FIXTURE_002_LABEL,
                11_289u64,
                4u32,
                11_378u64,
                51u32,
                11_994u64,
                2_588_160u32,
                11_998u64,
                2_600_158u64,
                32_745u64,
            ),
            (
                FIXTURE_003_PATH,
                FIXTURE_003_LABEL,
                11_206u64,
                6u32,
                11_310u64,
                41u32,
                11_806u64,
                1_593_856u32,
                11_810u64,
                1_605_666u64,
                32_872u64,
            ),
        ];

        for (
            path,
            label,
            content_start,
            levels_count,
            levels_end,
            keyframes_count,
            keyframes_end,
            network_size,
            network_start,
            network_end,
            footer_size,
        ) in cases
        {
            let Some(bytes) = load_fixture_bytes_or_skip(path, label) else {
                return;
            };
            let scaffold = MinimalReplayContentScaffoldReader
                .read_content_scaffold(&ReplayInput::Memory {
                    label: label.to_string(),
                    bytes,
                })
                .expect("historical fixture content scaffold should be structurally valid");
            assert_eq!(scaffold.boundary.content_start, content_start);
            assert_eq!(scaffold.levels_count_offset, content_start);
            assert_eq!(scaffold.levels_count, levels_count);
            assert_eq!(scaffold.levels_end, levels_end);
            assert_eq!(scaffold.keyframes_count_offset, levels_end);
            assert_eq!(scaffold.keyframes_count, keyframes_count);
            assert_eq!(scaffold.keyframes_end, keyframes_end);
            assert_eq!(scaffold.network_size_offset, keyframes_end);
            assert_eq!(scaffold.network_size, network_size);
            assert_eq!(scaffold.network_start, network_start);
            assert_eq!(scaffold.network_end, network_end);
            assert_eq!(scaffold.footer_start, network_end);
            assert_eq!(scaffold.footer_size, footer_size);
            assert_eq!(
                scaffold.footer_start + scaffold.footer_size,
                scaffold.boundary.content_end
            );
        }
    }

    #[test]
    fn minimal_content_scaffold_reader_frames_checked_in_largest_100_corpus() {
        let root = PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("../../test_corpus/largest_100");
        if !root.is_dir() {
            eprintln!("skipping largest_100 content-scaffold regression; corpus root is absent");
            return;
        }
        let mut replay_paths = fs::read_dir(&root)
            .expect("largest_100 corpus directory should be readable")
            .map(|entry| {
                entry
                    .expect("corpus directory entry should be readable")
                    .path()
            })
            .filter(|path| path.extension().and_then(|value| value.to_str()) == Some("replay"))
            .collect::<Vec<_>>();
        replay_paths.sort();
        assert_eq!(replay_paths.len(), 100);
        for path in replay_paths {
            let bytes = fs::read(&path).expect("checked-in corpus replay should be readable");
            let label = path
                .file_name()
                .expect("corpus replay should have a file name")
                .to_string_lossy()
                .into_owned();
            let scaffold = MinimalReplayContentScaffoldReader
                .read_content_scaffold(&ReplayInput::Memory {
                    label: label.clone(),
                    bytes,
                })
                .unwrap_or_else(|error| panic!("content scaffold failed for {label}: {error}"));
            assert!(scaffold.levels_count > 0);
            assert!(scaffold.keyframes_count > 0);
            assert!(scaffold.network_size > 0);
            assert_eq!(scaffold.footer_start, scaffold.network_end);
            assert_eq!(
                scaffold.footer_start + scaffold.footer_size,
                scaffold.boundary.content_end
            );
        }
    }

    #[test]
    fn minimal_content_scaffold_reader_rejects_file_input() {
        let error = MinimalReplayContentScaffoldReader
            .read_content_scaffold(&ReplayInput::file("sample.replay"))
            .expect_err("file input remains outside the content-scaffold reader");
        assert_error_contains(error, "replay content scaffold error: unsupported-input");
    }

    #[test]
    fn minimal_content_scaffold_reader_keeps_network_and_footer_opaque() {
        let mut content = Vec::new();
        content.extend_from_slice(&0i32.to_le_bytes());
        content.extend_from_slice(&0i32.to_le_bytes());
        content.extend_from_slice(&3i32.to_le_bytes());
        content.extend_from_slice(&[0xFF, 0x00, 0x7A]);
        content.extend_from_slice(&[0xDE, 0xAD, 0xBE, 0xEF]);
        let bytes = build_body_boundary_bytes(
            &[],
            0x12345678,
            i32::try_from(content.len()).unwrap(),
            &content,
        );
        let scaffold = MinimalReplayContentScaffoldReader
            .read_content_scaffold(&ReplayInput::Memory {
                label: "synthetic".to_string(),
                bytes,
            })
            .expect("opaque network and footer bytes should only be bounded");
        assert_eq!(scaffold.network_size, 3);
        assert_eq!(scaffold.footer_size, 4);
        assert_eq!(scaffold.boundary.content_crc, 0x12345678);
    }

    #[test]
    fn minimal_content_scaffold_reader_structurally_skips_bounded_utf16_level_text() {
        let mut content = Vec::new();
        content.extend_from_slice(&1i32.to_le_bytes());
        content.extend_from_slice(&(-2i32).to_le_bytes());
        content.extend_from_slice(&[b'A', 0, 0, 0]);
        content.extend_from_slice(&0i32.to_le_bytes());
        content.extend_from_slice(&0i32.to_le_bytes());
        let bytes =
            build_body_boundary_bytes(&[], 0, i32::try_from(content.len()).unwrap(), &content);
        let scaffold = MinimalReplayContentScaffoldReader
            .read_content_scaffold(&ReplayInput::Memory {
                label: "synthetic".to_string(),
                bytes,
            })
            .expect("bounded negative Unreal text length should be structurally skippable");
        assert_eq!(scaffold.levels_count, 1);
        assert_eq!(scaffold.keyframes_count, 0);
        assert_eq!(scaffold.network_size, 0);
        assert_eq!(scaffold.footer_size, 0);
    }

    #[test]
    fn minimal_content_scaffold_reader_rejects_negative_levels_count() {
        let content = (-1i32).to_le_bytes();
        let bytes = build_body_boundary_bytes(&[], 0, 4, &content);
        let error = MinimalReplayContentScaffoldReader
            .read_content_scaffold(&ReplayInput::Memory {
                label: "synthetic".to_string(),
                bytes,
            })
            .expect_err("negative levels count is malformed");
        assert_error_contains(error, "replay content scaffold error: malformed");
    }

    #[test]
    fn minimal_content_scaffold_reader_rejects_truncated_level_text() {
        let mut content = Vec::new();
        content.extend_from_slice(&1i32.to_le_bytes());
        content.extend_from_slice(&5i32.to_le_bytes());
        content.extend_from_slice(&[1, 2]);
        let bytes =
            build_body_boundary_bytes(&[], 0, i32::try_from(content.len()).unwrap(), &content);
        let error = MinimalReplayContentScaffoldReader
            .read_content_scaffold(&ReplayInput::Memory {
                label: "synthetic".to_string(),
                bytes,
            })
            .expect_err("truncated level text is insufficient");
        assert_error_contains(error, "replay content scaffold error: insufficient");
    }

    #[test]
    fn minimal_content_scaffold_reader_rejects_negative_keyframes_count() {
        let mut content = Vec::new();
        content.extend_from_slice(&0i32.to_le_bytes());
        content.extend_from_slice(&(-1i32).to_le_bytes());
        let bytes =
            build_body_boundary_bytes(&[], 0, i32::try_from(content.len()).unwrap(), &content);
        let error = MinimalReplayContentScaffoldReader
            .read_content_scaffold(&ReplayInput::Memory {
                label: "synthetic".to_string(),
                bytes,
            })
            .expect_err("negative keyframes count is malformed");
        assert_error_contains(error, "replay content scaffold error: malformed");
    }

    #[test]
    fn minimal_content_scaffold_reader_rejects_truncated_keyframe_tuples() {
        let mut content = Vec::new();
        content.extend_from_slice(&0i32.to_le_bytes());
        content.extend_from_slice(&1i32.to_le_bytes());
        content.extend_from_slice(&[0; 8]);
        let bytes =
            build_body_boundary_bytes(&[], 0, i32::try_from(content.len()).unwrap(), &content);
        let error = MinimalReplayContentScaffoldReader
            .read_content_scaffold(&ReplayInput::Memory {
                label: "synthetic".to_string(),
                bytes,
            })
            .expect_err("keyframe tuple must be twelve bytes");
        assert_error_contains(error, "replay content scaffold error: insufficient");
    }

    #[test]
    fn minimal_content_scaffold_reader_rejects_negative_network_size() {
        let mut content = Vec::new();
        content.extend_from_slice(&0i32.to_le_bytes());
        content.extend_from_slice(&0i32.to_le_bytes());
        content.extend_from_slice(&(-1i32).to_le_bytes());
        let bytes =
            build_body_boundary_bytes(&[], 0, i32::try_from(content.len()).unwrap(), &content);
        let error = MinimalReplayContentScaffoldReader
            .read_content_scaffold(&ReplayInput::Memory {
                label: "synthetic".to_string(),
                bytes,
            })
            .expect_err("negative network size is malformed");
        assert_error_contains(error, "replay content scaffold error: malformed");
    }

    #[test]
    fn minimal_content_scaffold_reader_rejects_network_beyond_content() {
        let mut content = Vec::new();
        content.extend_from_slice(&0i32.to_le_bytes());
        content.extend_from_slice(&0i32.to_le_bytes());
        content.extend_from_slice(&4i32.to_le_bytes());
        content.extend_from_slice(&[1, 2, 3]);
        let bytes =
            build_body_boundary_bytes(&[], 0, i32::try_from(content.len()).unwrap(), &content);
        let error = MinimalReplayContentScaffoldReader
            .read_content_scaffold(&ReplayInput::Memory {
                label: "synthetic".to_string(),
                bytes,
            })
            .expect_err("network payload beyond content is insufficient");
        assert_error_contains(error, "replay content scaffold error: insufficient");
    }

    fn build_minimal_footer_content(tail: &[u8]) -> Vec<u8> {
        let mut content = Vec::new();
        content.extend_from_slice(&0i32.to_le_bytes()); // levels
        content.extend_from_slice(&0i32.to_le_bytes()); // keyframes
        content.extend_from_slice(&0i32.to_le_bytes()); // network size
        content.extend_from_slice(&0i32.to_le_bytes()); // debug info
        content.extend_from_slice(&0i32.to_le_bytes()); // tickmarks
        content.extend_from_slice(&0i32.to_le_bytes()); // packages
        content.extend_from_slice(&0i32.to_le_bytes()); // objects
        content.extend_from_slice(&0i32.to_le_bytes()); // names
        content.extend_from_slice(&0i32.to_le_bytes()); // class indices
        content.extend_from_slice(&0i32.to_le_bytes()); // net cache
        content.extend_from_slice(tail);
        content
    }

    fn build_footer_replay(content: Vec<u8>) -> ReplayInput {
        let content_size = i32::try_from(content.len()).expect("synthetic footer content fits i32");
        ReplayInput::Memory {
            label: "synthetic-footer".to_string(),
            bytes: build_body_boundary_bytes(&[], 0xA1B2C3D4, content_size, &content),
        }
    }

    #[test]
    fn minimal_footer_scaffold_reader_matches_three_historical_fixtures() {
        let cases = [
            (
                FIXTURE_001_PATH,
                FIXTURE_001_LABEL,
                0u32,
                16u32,
                3u32,
                398u32,
                416u32,
                41u32,
                36u32,
                301u32,
                3_001_017u64,
                4u32,
                3_001_021u64,
            ),
            (
                FIXTURE_002_PATH,
                FIXTURE_002_LABEL,
                0u32,
                8u32,
                6u32,
                429u32,
                344u32,
                43u32,
                38u32,
                327u32,
                2_632_899u64,
                4u32,
                2_632_903u64,
            ),
            (
                FIXTURE_003_PATH,
                FIXTURE_003_LABEL,
                0u32,
                16u32,
                8u32,
                433u32,
                351u32,
                42u32,
                37u32,
                335u32,
                1_638_534u64,
                4u32,
                1_638_538u64,
            ),
        ];

        for (
            path,
            label,
            debug_info_count,
            tickmarks_count,
            packages_count,
            objects_count,
            names_count,
            class_indices_count,
            net_cache_count,
            net_cache_properties_count,
            known_footer_end,
            opaque_tail_size,
            footer_end,
        ) in cases
        {
            let Some(bytes) = load_fixture_bytes_or_skip(path, label) else {
                return;
            };
            let scaffold = MinimalReplayFooterScaffoldReader
                .read_footer_scaffold(&ReplayInput::Memory {
                    label: label.to_string(),
                    bytes,
                })
                .expect("historical fixture footer scaffold should be structurally valid");

            assert_eq!(scaffold.debug_info_count, debug_info_count);
            assert_eq!(scaffold.tickmarks_count, tickmarks_count);
            assert_eq!(scaffold.packages_count, packages_count);
            assert_eq!(scaffold.objects_count, objects_count);
            assert_eq!(scaffold.names_count, names_count);
            assert_eq!(scaffold.class_indices_count, class_indices_count);
            assert_eq!(scaffold.net_cache_count, net_cache_count);
            assert_eq!(
                scaffold.net_cache_properties_count,
                net_cache_properties_count
            );
            assert_eq!(scaffold.net_cache_end, known_footer_end);
            assert_eq!(scaffold.opaque_tail_start, known_footer_end);
            assert_eq!(scaffold.opaque_tail_size, opaque_tail_size);
            assert_eq!(scaffold.footer_end, footer_end);
            assert_eq!(scaffold.footer_end, scaffold.content.boundary.content_end);
        }
    }

    #[test]
    fn minimal_footer_scaffold_reader_frames_checked_in_largest_100_corpus() {
        let root = PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("../../test_corpus/largest_100");
        if !root.is_dir() {
            eprintln!("skipping largest_100 footer-scaffold regression; corpus root is absent");
            return;
        }
        let mut replay_paths = fs::read_dir(&root)
            .expect("largest_100 corpus directory should be readable")
            .map(|entry| {
                entry
                    .expect("corpus directory entry should be readable")
                    .path()
            })
            .filter(|path| path.extension().and_then(|value| value.to_str()) == Some("replay"))
            .collect::<Vec<_>>();
        replay_paths.sort();
        assert_eq!(replay_paths.len(), 100);

        let mut empty_tail = 0usize;
        let mut zero_word_tail = 0usize;
        for path in replay_paths {
            let bytes = fs::read(&path).expect("checked-in corpus replay should be readable");
            let label = path
                .file_name()
                .expect("corpus replay should have a file name")
                .to_string_lossy()
                .into_owned();
            let scaffold = MinimalReplayFooterScaffoldReader
                .read_footer_scaffold(&ReplayInput::Memory {
                    label: label.clone(),
                    bytes,
                })
                .unwrap_or_else(|error| panic!("footer scaffold failed for {label}: {error}"));
            assert_eq!(scaffold.footer_end, scaffold.content.boundary.content_end);
            assert_eq!(scaffold.opaque_tail_start, scaffold.net_cache_end);
            match scaffold.opaque_tail_size {
                0 => empty_tail += 1,
                4 => zero_word_tail += 1,
                other => panic!("unexpected admitted opaque tail size {other} for {label}"),
            }
        }
        assert_eq!(empty_tail, 1);
        assert_eq!(zero_word_tail, 99);
    }

    #[test]
    fn minimal_footer_scaffold_reader_accepts_observed_empty_tail() {
        let content = build_minimal_footer_content(&[]);
        let scaffold = MinimalReplayFooterScaffoldReader
            .read_footer_scaffold(&build_footer_replay(content))
            .expect("empty opaque footer tail is an observed admitted form");
        assert_eq!(scaffold.opaque_tail_size, 0);
        assert_eq!(scaffold.net_cache_end, scaffold.footer_end);
        assert_eq!(scaffold.content.boundary.content_crc, 0xA1B2C3D4);
    }

    #[test]
    fn minimal_footer_scaffold_reader_accepts_observed_zero_word_tail() {
        let content = build_minimal_footer_content(&[0, 0, 0, 0]);
        let scaffold = MinimalReplayFooterScaffoldReader
            .read_footer_scaffold(&build_footer_replay(content))
            .expect("four zero opaque footer bytes are an observed admitted form");
        assert_eq!(scaffold.opaque_tail_size, 4);
        assert_eq!(scaffold.opaque_tail_start + 4, scaffold.footer_end);
    }

    #[test]
    fn minimal_footer_scaffold_reader_rejects_nonzero_four_byte_tail() {
        let content = build_minimal_footer_content(&[1, 0, 0, 0]);
        let error = MinimalReplayFooterScaffoldReader
            .read_footer_scaffold(&build_footer_replay(content))
            .expect_err("non-zero four-byte footer tail is outside observed layout admission");
        assert_error_contains(error, "replay footer scaffold error: unsupported-layout");
    }

    #[test]
    fn minimal_footer_scaffold_reader_rejects_unobserved_tail_length() {
        let content = build_minimal_footer_content(&[0]);
        let error = MinimalReplayFooterScaffoldReader
            .read_footer_scaffold(&build_footer_replay(content))
            .expect_err("one-byte footer tail is outside observed layout admission");
        assert_error_contains(error, "replay footer scaffold error: unsupported-layout");
    }

    #[test]
    fn minimal_footer_scaffold_reader_rejects_file_input() {
        let error = MinimalReplayFooterScaffoldReader
            .read_footer_scaffold(&ReplayInput::file("sample.replay"))
            .expect_err("file input remains outside the footer-scaffold reader");
        assert_error_contains(error, "replay footer scaffold error: unsupported-input");
    }

    #[test]
    fn minimal_footer_scaffold_reader_rejects_negative_debug_info_count() {
        let mut content = Vec::new();
        content.extend_from_slice(&0i32.to_le_bytes());
        content.extend_from_slice(&0i32.to_le_bytes());
        content.extend_from_slice(&0i32.to_le_bytes());
        content.extend_from_slice(&(-1i32).to_le_bytes());
        let error = MinimalReplayFooterScaffoldReader
            .read_footer_scaffold(&build_footer_replay(content))
            .expect_err("negative footer list counts are malformed");
        assert_error_contains(error, "replay footer scaffold error: malformed");
    }

    #[test]
    fn minimal_footer_scaffold_reader_rejects_truncated_debug_info_entry() {
        let mut content = Vec::new();
        content.extend_from_slice(&0i32.to_le_bytes());
        content.extend_from_slice(&0i32.to_le_bytes());
        content.extend_from_slice(&0i32.to_le_bytes());
        content.extend_from_slice(&1i32.to_le_bytes());
        content.extend_from_slice(&7i32.to_le_bytes());
        let error = MinimalReplayFooterScaffoldReader
            .read_footer_scaffold(&build_footer_replay(content))
            .expect_err("debug-info entry without user text length is truncated");
        assert_error_contains(error, "replay footer scaffold error: insufficient");
    }

    #[test]
    fn minimal_footer_scaffold_reader_rejects_negative_class_index_string_length() {
        let mut content = build_minimal_footer_content(&[]);
        content.truncate(12 + 5 * 4);
        content.extend_from_slice(&1i32.to_le_bytes());
        content.extend_from_slice(&(-1i32).to_le_bytes());
        let error = MinimalReplayFooterScaffoldReader
            .read_footer_scaffold(&build_footer_replay(content))
            .expect_err("negative class-index raw string length is malformed");
        assert_error_contains(error, "replay footer scaffold error: malformed");
    }

    #[test]
    fn minimal_footer_scaffold_reader_rejects_negative_net_cache_property_count() {
        let mut content = build_minimal_footer_content(&[]);
        content.truncate(12 + 6 * 4);
        content.extend_from_slice(&1i32.to_le_bytes());
        content.extend_from_slice(&0i32.to_le_bytes());
        content.extend_from_slice(&0i32.to_le_bytes());
        content.extend_from_slice(&0i32.to_le_bytes());
        content.extend_from_slice(&(-1i32).to_le_bytes());
        let error = MinimalReplayFooterScaffoldReader
            .read_footer_scaffold(&build_footer_replay(content))
            .expect_err("negative net-cache property count is malformed");
        assert_error_contains(error, "replay footer scaffold error: malformed");
    }

    fn push_lookup_unreal_text(content: &mut Vec<u8>, payload_without_nul: &[u8]) {
        let len = i32::try_from(payload_without_nul.len() + 1).expect("synthetic text fits i32");
        content.extend_from_slice(&len.to_le_bytes());
        content.extend_from_slice(payload_without_nul);
        content.push(0);
    }

    fn push_lookup_raw_utf8(content: &mut Vec<u8>, value: &str) {
        let len = i32::try_from(value.len() + 1).expect("synthetic raw string fits i32");
        content.extend_from_slice(&len.to_le_bytes());
        content.extend_from_slice(value.as_bytes());
        content.push(0);
    }

    fn build_lookup_footer_content() -> Vec<u8> {
        let mut content = Vec::new();
        content.extend_from_slice(&0i32.to_le_bytes()); // levels
        content.extend_from_slice(&0i32.to_le_bytes()); // keyframes
        content.extend_from_slice(&0i32.to_le_bytes()); // network size
        content.extend_from_slice(&0i32.to_le_bytes()); // debug info
        content.extend_from_slice(&0i32.to_le_bytes()); // tickmarks
        content.extend_from_slice(&0i32.to_le_bytes()); // packages

        content.extend_from_slice(&2i32.to_le_bytes()); // objects
        push_lookup_unreal_text(&mut content, b"Core.Object");
        push_lookup_unreal_text(&mut content, b"TAGame.Vehicle_TA");

        content.extend_from_slice(&1i32.to_le_bytes()); // names
        push_lookup_unreal_text(&mut content, &[b'E', 0x80]);

        content.extend_from_slice(&1i32.to_le_bytes()); // class indices
        push_lookup_raw_utf8(&mut content, "Core.Object");
        content.extend_from_slice(&0i32.to_le_bytes());

        content.extend_from_slice(&2i32.to_le_bytes()); // net cache
        content.extend_from_slice(&0i32.to_le_bytes()); // object_ind
        content.extend_from_slice(&40i32.to_le_bytes()); // opaque unresolved parent_id
        content.extend_from_slice(&23i32.to_le_bytes()); // duplicate cache_id admitted
        content.extend_from_slice(&1i32.to_le_bytes()); // properties
        content.extend_from_slice(&1i32.to_le_bytes()); // property object_ind
        content.extend_from_slice(&5i32.to_le_bytes()); // stream_id

        content.extend_from_slice(&1i32.to_le_bytes()); // object_ind
        content.extend_from_slice(&40i32.to_le_bytes()); // same unresolved parent_id
        content.extend_from_slice(&23i32.to_le_bytes()); // same cache_id
        content.extend_from_slice(&0i32.to_le_bytes()); // properties
        content.extend_from_slice(&[0, 0, 0, 0]); // observed opaque tail
        content
    }

    #[test]
    fn minimal_footer_lookup_materializer_matches_three_historical_fixtures() {
        for (path, label) in [
            (FIXTURE_001_PATH, FIXTURE_001_LABEL),
            (FIXTURE_002_PATH, FIXTURE_002_LABEL),
            (FIXTURE_003_PATH, FIXTURE_003_LABEL),
        ] {
            let Some(bytes) = load_fixture_bytes_or_skip(path, label) else {
                return;
            };
            let lookup = MinimalReplayFooterLookupMaterializationReader
                .read_footer_lookup_materialization(&ReplayInput::Memory {
                    label: label.to_string(),
                    bytes,
                })
                .expect("historical footer lookup tables should materialize");
            assert_eq!(lookup.objects.len(), lookup.scaffold.objects_count as usize);
            assert_eq!(lookup.names.len(), lookup.scaffold.names_count as usize);
            assert_eq!(
                lookup.class_indices.len(),
                lookup.scaffold.class_indices_count as usize
            );
            assert_eq!(
                lookup.net_cache.len(),
                lookup.scaffold.net_cache_count as usize
            );
            let property_total: usize = lookup
                .net_cache
                .iter()
                .map(|entry| entry.properties.len())
                .sum();
            assert_eq!(
                property_total,
                lookup.scaffold.net_cache_properties_count as usize
            );
            for class_index in &lookup.class_indices {
                assert_eq!(
                    class_index.class_name,
                    lookup.objects[class_index.object_index as usize]
                );
            }
            for entry in &lookup.net_cache {
                assert!((entry.object_index as usize) < lookup.objects.len());
                for property in &entry.properties {
                    assert!((property.object_index as usize) < lookup.objects.len());
                }
            }
        }
    }

    #[test]
    fn minimal_footer_lookup_materializer_matches_checked_in_largest_100_corpus() {
        let root = PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("../../test_corpus/largest_100");
        if !root.is_dir() {
            eprintln!("skipping largest_100 footer-lookup regression; corpus root is absent");
            return;
        }
        let mut replay_paths = fs::read_dir(&root)
            .expect("largest_100 corpus directory should be readable")
            .map(|entry| {
                entry
                    .expect("corpus directory entry should be readable")
                    .path()
            })
            .filter(|path| path.extension().and_then(|value| value.to_str()) == Some("replay"))
            .collect::<Vec<_>>();
        replay_paths.sort();
        assert_eq!(replay_paths.len(), 100);

        for path in replay_paths {
            let bytes = fs::read(&path).expect("checked-in corpus replay should be readable");
            let label = path
                .file_name()
                .expect("corpus replay should have a file name")
                .to_string_lossy()
                .into_owned();
            let lookup = MinimalReplayFooterLookupMaterializationReader
                .read_footer_lookup_materialization(&ReplayInput::Memory {
                    label: label.clone(),
                    bytes,
                })
                .unwrap_or_else(|error| panic!("footer lookup failed for {label}: {error}"));
            assert_eq!(lookup.objects.len(), lookup.scaffold.objects_count as usize);
            assert_eq!(lookup.names.len(), lookup.scaffold.names_count as usize);
            assert_eq!(
                lookup.class_indices.len(),
                lookup.scaffold.class_indices_count as usize
            );
            assert_eq!(
                lookup.net_cache.len(),
                lookup.scaffold.net_cache_count as usize
            );
            for class_index in &lookup.class_indices {
                assert_eq!(
                    class_index.class_name,
                    lookup.objects[class_index.object_index as usize]
                );
            }
            for entry in &lookup.net_cache {
                assert!((entry.object_index as usize) < lookup.objects.len());
                for property in &entry.properties {
                    assert!((property.object_index as usize) < lookup.objects.len());
                }
            }
        }
    }

    #[test]
    fn minimal_footer_lookup_materializer_preserves_opaque_cache_and_parent_ids() {
        let lookup = MinimalReplayFooterLookupMaterializationReader
            .read_footer_lookup_materialization(&build_footer_replay(build_lookup_footer_content()))
            .expect("duplicate cache_id and unresolved parent_id are raw fields, not rejection predicates");
        assert_eq!(lookup.objects, ["Core.Object", "TAGame.Vehicle_TA"]);
        assert_eq!(lookup.names, ["E€"]);
        assert_eq!(lookup.net_cache.len(), 2);
        assert_eq!(lookup.net_cache[0].parent_id, 40);
        assert_eq!(lookup.net_cache[1].parent_id, 40);
        assert_eq!(lookup.net_cache[0].cache_id, 23);
        assert_eq!(lookup.net_cache[1].cache_id, 23);
        assert_eq!(lookup.net_cache[0].properties[0].stream_id, 5);
    }

    #[test]
    fn minimal_footer_lookup_materializer_rejects_file_input() {
        let error = MinimalReplayFooterLookupMaterializationReader
            .read_footer_lookup_materialization(&ReplayInput::file("sample.replay"))
            .expect_err("file input remains outside footer lookup materialization");
        assert_error_contains(error, "replay footer lookup error: unsupported-input");
    }

    #[test]
    fn minimal_footer_lookup_materializer_rejects_utf16_object_text() {
        let mut content = build_lookup_footer_content();
        let objects_count_offset = 24usize;
        let object_text_offset = objects_count_offset + 4;
        // Core.Object + trailing NUL occupies 12 bytes; -6 keeps the scaffold byte width at 12.
        content[object_text_offset..object_text_offset + 4].copy_from_slice(&(-6i32).to_le_bytes());
        let error = MinimalReplayFooterLookupMaterializationReader
            .read_footer_lookup_materialization(&build_footer_replay(content))
            .expect_err("R3.8 lookup admission does not claim UTF-16 object text");
        assert_error_contains(error, "replay footer lookup error: unsupported-text");
    }

    #[test]
    fn minimal_footer_lookup_materializer_rejects_missing_object_nul() {
        let mut content = build_lookup_footer_content();
        let objects_count_offset = 24usize;
        let object_text_offset = objects_count_offset + 4;
        let object_len = i32::from_le_bytes(
            content[object_text_offset..object_text_offset + 4]
                .try_into()
                .unwrap(),
        ) as usize;
        let last = object_text_offset + 4 + object_len - 1;
        content[last] = b'X';
        let error = MinimalReplayFooterLookupMaterializationReader
            .read_footer_lookup_materialization(&build_footer_replay(content))
            .expect_err("lookup Unreal text requires trailing NUL");
        assert_error_contains(error, "replay footer lookup error: malformed");
    }

    #[test]
    fn minimal_footer_lookup_materializer_rejects_undefined_windows1252_byte() {
        let mut content = build_lookup_footer_content();
        let objects_count_offset = 24usize;
        let object_text_offset = objects_count_offset + 4;
        content[object_text_offset + 4] = 0x81;
        let error = MinimalReplayFooterLookupMaterializationReader
            .read_footer_lookup_materialization(&build_footer_replay(content))
            .expect_err("undefined Windows-1252 bytes are malformed lookup text");
        assert_error_contains(error, "replay footer lookup error: malformed");
    }

    #[test]
    fn minimal_footer_lookup_materializer_rejects_class_index_name_mismatch() {
        let mut content = build_lookup_footer_content();
        let needle = b"Core.Object\0";
        let positions = content
            .windows(needle.len())
            .enumerate()
            .filter_map(|(index, window)| (window == needle).then_some(index))
            .collect::<Vec<_>>();
        assert_eq!(positions.len(), 2);
        let class_name_start = positions[1];
        content[class_name_start] = b'X';
        let error = MinimalReplayFooterLookupMaterializationReader
            .read_footer_lookup_materialization(&build_footer_replay(content))
            .expect_err("class-index class names must match objects[index]");
        assert_error_contains(error, "replay footer lookup error: mapping");
    }

    #[test]
    fn minimal_footer_lookup_materializer_rejects_negative_class_index() {
        let mut content = build_lookup_footer_content();
        let needle = b"Core.Object\0";
        let positions = content
            .windows(needle.len())
            .enumerate()
            .filter_map(|(index, window)| (window == needle).then_some(index))
            .collect::<Vec<_>>();
        let class_name_start = positions[1];
        let index_offset = class_name_start + needle.len();
        content[index_offset..index_offset + 4].copy_from_slice(&(-1i32).to_le_bytes());
        let error = MinimalReplayFooterLookupMaterializationReader
            .read_footer_lookup_materialization(&build_footer_replay(content))
            .expect_err("negative class-index object indices are invalid mappings");
        assert_error_contains(error, "replay footer lookup error: mapping");
    }

    #[test]
    fn minimal_footer_lookup_materializer_rejects_out_of_bounds_net_cache_object() {
        let mut content = build_lookup_footer_content();
        let tail_start = content.len() - 4;
        let second_entry_size = 16usize;
        let first_entry_size = 24usize;
        let net_cache_start = tail_start - second_entry_size - first_entry_size - 4;
        let first_object_offset = net_cache_start + 4;
        content[first_object_offset..first_object_offset + 4].copy_from_slice(&99i32.to_le_bytes());
        let error = MinimalReplayFooterLookupMaterializationReader
            .read_footer_lookup_materialization(&build_footer_replay(content))
            .expect_err("net-cache object indices must resolve into objects");
        assert_error_contains(error, "replay footer lookup error: mapping");
    }

    #[test]
    fn minimal_footer_lookup_materializer_rejects_negative_stream_id() {
        let mut content = build_lookup_footer_content();
        let tail_start = content.len() - 4;
        let second_entry_size = 16usize;
        let first_entry_size = 24usize;
        let net_cache_start = tail_start - second_entry_size - first_entry_size - 4;
        let first_stream_id_offset = net_cache_start + 4 + 16 + 4;
        content[first_stream_id_offset..first_stream_id_offset + 4]
            .copy_from_slice(&(-1i32).to_le_bytes());
        let error = MinimalReplayFooterLookupMaterializationReader
            .read_footer_lookup_materialization(&build_footer_replay(content))
            .expect_err("negative stream ids are outside raw lookup admission");
        assert_error_contains(error, "replay footer lookup error: mapping");
    }

    fn mutate_first_network_timing(
        bytes: &mut [u8],
        time: f32,
        delta: f32,
    ) -> ReplayContentScaffoldV1 {
        let input = ReplayInput::Memory {
            label: "timing-mutation-source".to_string(),
            bytes: bytes.to_vec(),
        };
        let scaffold = MinimalReplayContentScaffoldReader
            .read_content_scaffold(&input)
            .expect("fixture content scaffold should be valid before timing mutation");
        let start = scaffold.network_start as usize;
        bytes[start..start + 4].copy_from_slice(&time.to_le_bytes());
        bytes[start + 4..start + 8].copy_from_slice(&delta.to_le_bytes());
        scaffold
    }

    fn rename_unique_ascii_property(bytes: &mut [u8], needle: &[u8]) {
        let positions = bytes
            .windows(needle.len())
            .enumerate()
            .filter_map(|(index, window)| (window == needle).then_some(index))
            .collect::<Vec<_>>();
        assert_eq!(positions.len(), 1, "property marker must be unique");
        bytes[positions[0]] = b'X';
    }

    #[test]
    fn minimal_network_timing_preamble_reader_matches_three_historical_fixtures() {
        for (path, label) in [
            (FIXTURE_001_PATH, FIXTURE_001_LABEL),
            (FIXTURE_002_PATH, FIXTURE_002_LABEL),
            (FIXTURE_003_PATH, FIXTURE_003_LABEL),
        ] {
            let Some(bytes) = load_fixture_bytes_or_skip(path, label) else {
                return;
            };
            let timing = MinimalReplayNetworkTimingPreambleReader
                .read_network_timing_preamble(&ReplayInput::Memory {
                    label: label.to_string(),
                    bytes,
                })
                .expect("historical exact-admitted fixture should expose first timing preamble");
            assert!(timing.first_frame_time.is_finite());
            assert!(timing.first_frame_time > 0.0);
            assert_eq!(timing.first_frame_delta, 0.0);
            assert_eq!(timing.channel_bits, 10);
            assert_eq!(timing.num_frames, timing.header.total_frames.unwrap());
            assert!(timing.max_channels > 0);
            assert!(timing.content.network_size >= 8);
        }
    }

    #[test]
    fn minimal_network_timing_preamble_reader_preserves_44_56_header_admission_gate() {
        let root = PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("../../test_corpus/largest_100");
        if !root.is_dir() {
            eprintln!("skipping largest_100 timing-preamble regression; corpus root is absent");
            return;
        }
        let mut replay_paths = fs::read_dir(&root)
            .expect("largest_100 corpus directory should be readable")
            .map(|entry| {
                entry
                    .expect("corpus directory entry should be readable")
                    .path()
            })
            .filter(|path| path.extension().and_then(|value| value.to_str()) == Some("replay"))
            .collect::<Vec<_>>();
        replay_paths.sort();
        assert_eq!(replay_paths.len(), 100);

        let mut supported = 0usize;
        let mut unsupported = 0usize;
        for path in replay_paths {
            let bytes = fs::read(&path).expect("checked-in corpus replay should be readable");
            let label = path.file_name().unwrap().to_string_lossy().into_owned();
            let input = ReplayInput::Memory { label, bytes };
            let header_result = MinimalReplayHeaderReader.read_header(&input);
            let timing_result =
                MinimalReplayNetworkTimingPreambleReader.read_network_timing_preamble(&input);
            match header_result {
                Ok(_) => {
                    supported += 1;
                    let timing = timing_result.expect(
                        "every currently admitted header row must satisfy R3.9 timing evidence",
                    );
                    assert!(timing.first_frame_time > 0.0);
                    assert_eq!(timing.first_frame_delta, 0.0);
                    assert_eq!(timing.channel_bits, 10);
                }
                Err(_) => {
                    unsupported += 1;
                    assert!(
                        timing_result.is_err(),
                        "timing reader must not bypass exact header admission"
                    );
                }
            }
        }
        assert_eq!(supported, 44);
        assert_eq!(unsupported, 56);
    }

    #[test]
    fn minimal_network_timing_preamble_reader_rejects_file_input() {
        let error = MinimalReplayNetworkTimingPreambleReader
            .read_network_timing_preamble(&ReplayInput::file("sample.replay"))
            .expect_err("file input remains outside timing preamble reader");
        assert_error_contains(error, "replay network timing error: unsupported-input");
    }

    #[test]
    fn minimal_network_timing_preamble_reader_rejects_invalid_timing_components() {
        let Some(original) = load_fixture_bytes_or_skip(FIXTURE_001_PATH, FIXTURE_001_LABEL) else {
            return;
        };
        for (time, delta) in [
            (f32::NAN, 0.0),
            (-1.0, 0.0),
            (1.0e-20, 0.0),
            (1.0, -0.01),
            (1.0, 1.0e-20),
        ] {
            let mut bytes = original.clone();
            mutate_first_network_timing(&mut bytes, time, delta);
            let error = MinimalReplayNetworkTimingPreambleReader
                .read_network_timing_preamble(&ReplayInput::Memory {
                    label: FIXTURE_001_LABEL.to_string(),
                    bytes,
                })
                .expect_err("invalid first timing component must fail closed");
            assert_error_contains(error, "replay network timing error: malformed");
        }
    }

    #[test]
    fn minimal_network_timing_preamble_reader_rejects_terminal_zero_zero_pair() {
        let Some(mut bytes) = load_fixture_bytes_or_skip(FIXTURE_001_PATH, FIXTURE_001_LABEL)
        else {
            return;
        };
        mutate_first_network_timing(&mut bytes, 0.0, 0.0);
        let error = MinimalReplayNetworkTimingPreambleReader
            .read_network_timing_preamble(&ReplayInput::Memory {
                label: FIXTURE_001_LABEL.to_string(),
                bytes,
            })
            .expect_err("0/0 first timing pair is the terminal marker");
        assert_error_contains(error, "replay network timing error: terminal-first-frame");
    }

    #[test]
    fn minimal_network_timing_preamble_reader_rejects_network_shorter_than_eight_bytes() {
        let Some(mut bytes) = load_fixture_bytes_or_skip(FIXTURE_001_PATH, FIXTURE_001_LABEL)
        else {
            return;
        };
        let input = ReplayInput::Memory {
            label: FIXTURE_001_LABEL.to_string(),
            bytes: bytes.clone(),
        };
        let scaffold = MinimalReplayContentScaffoldReader
            .read_content_scaffold(&input)
            .expect("fixture scaffold should be valid");
        let offset = scaffold.network_size_offset as usize;
        bytes[offset..offset + 4].copy_from_slice(&7i32.to_le_bytes());
        let error = MinimalReplayNetworkTimingPreambleReader
            .read_network_timing_preamble(&ReplayInput::Memory {
                label: FIXTURE_001_LABEL.to_string(),
                bytes,
            })
            .expect_err("network payload shorter than one timing pair must fail");
        assert_error_contains(error, "replay network timing error: insufficient");
    }

    #[test]
    fn minimal_network_timing_preamble_reader_rejects_num_frames_over_network_bytes() {
        let Some(mut bytes) = load_fixture_bytes_or_skip(FIXTURE_001_PATH, FIXTURE_001_LABEL)
        else {
            return;
        };
        let input = ReplayInput::Memory {
            label: FIXTURE_001_LABEL.to_string(),
            bytes: bytes.clone(),
        };
        let scaffold = MinimalReplayContentScaffoldReader
            .read_content_scaffold(&input)
            .expect("fixture scaffold should be valid");
        let offset = scaffold.network_size_offset as usize;
        bytes[offset..offset + 4].copy_from_slice(&8i32.to_le_bytes());
        let error = MinimalReplayNetworkTimingPreambleReader
            .read_network_timing_preamble(&ReplayInput::Memory {
                label: FIXTURE_001_LABEL.to_string(),
                bytes,
            })
            .expect_err("NumFrames above network byte count violates decoder precondition");
        assert_error_contains(error, "replay network timing error: precondition");
    }

    #[test]
    fn minimal_network_timing_preamble_reader_requires_max_channels_metadata() {
        let Some(mut bytes) = load_fixture_bytes_or_skip(FIXTURE_001_PATH, FIXTURE_001_LABEL)
        else {
            return;
        };
        rename_unique_ascii_property(&mut bytes, b"MaxChannels\0");
        let error = MinimalReplayNetworkTimingPreambleReader
            .read_network_timing_preamble(&ReplayInput::Memory {
                label: FIXTURE_001_LABEL.to_string(),
                bytes,
            })
            .expect_err("R3.9 admission requires observed MaxChannels instead of fallback");
        assert_error_contains(error, "replay network timing error: missing-header-field");
    }

    #[test]
    fn minimal_network_timing_preamble_reader_requires_num_frames_header_mapping() {
        let Some(mut bytes) = load_fixture_bytes_or_skip(FIXTURE_001_PATH, FIXTURE_001_LABEL)
        else {
            return;
        };
        rename_unique_ascii_property(&mut bytes, b"NumFrames\0");
        let error = MinimalReplayNetworkTimingPreambleReader
            .read_network_timing_preamble(&ReplayInput::Memory {
                label: FIXTURE_001_LABEL.to_string(),
                bytes,
            })
            .expect_err("R3.9 admission requires NumFrames mapping");
        assert_error_contains(error, "replay network timing error: missing-header-field");
    }

    #[test]
    fn unsupported_reader_fails_explicitly() {
        let reader = UnsupportedReplayReader;
        let error = reader
            .read_header(&ReplayInput::file("sample.replay"))
            .expect_err("reader should be unavailable");

        assert!(
            error
                .to_string()
                .contains("no replay parser is bundled in this scaffold")
        );
    }

    #[test]
    fn minimal_reader_parses_rl_replay_header_fixture_001_and_header_only_slice() {
        let Some(bytes) = load_fixture_bytes_or_skip(FIXTURE_001_PATH, FIXTURE_001_LABEL) else {
            return;
        };

        let reader = MinimalReplayHeaderReader;
        let input = ReplayInput::Memory {
            label: FIXTURE_001_LABEL.to_string(),
            bytes: bytes.clone(),
        };

        let header = reader
            .read_header(&input)
            .expect("fixture header should parse");
        assert_fixture_001_header(&header);

        let header_size = i32::from_le_bytes(
            bytes[0..4]
                .try_into()
                .expect("fixture should contain header_size"),
        );
        assert_eq!(header_size, 13_200);
        let header_end =
            8 + usize::try_from(header_size).expect("fixture header_size should fit usize");
        assert_eq!(header_end, 13_208);
        let header_only = bytes[..header_end].to_vec();
        let header_only_input = ReplayInput::Memory {
            label: FIXTURE_001_LABEL.to_string(),
            bytes: header_only,
        };
        let header_from_header_only = reader
            .read_header(&header_only_input)
            .expect("complete header-only slice should parse without body bytes");

        assert_eq!(header_from_header_only, header);
    }

    #[test]
    fn minimal_reader_parses_rl_replay_header_fixture_002_exact_happy_path() {
        let Some(bytes) = load_fixture_bytes_or_skip(FIXTURE_002_PATH, FIXTURE_002_LABEL) else {
            return;
        };

        let header = MinimalReplayHeaderReader
            .read_header(&ReplayInput::Memory {
                label: FIXTURE_002_LABEL.to_string(),
                bytes,
            })
            .expect("fixture_002 exact header should parse");

        assert_fixture_002_header(&header);
    }

    #[test]
    fn minimal_reader_parses_rl_replay_header_fixture_002_header_only_slice() {
        let Some(bytes) = load_fixture_bytes_or_skip(FIXTURE_002_PATH, FIXTURE_002_LABEL) else {
            return;
        };

        let header_size = i32::from_le_bytes(
            bytes[0..4]
                .try_into()
                .expect("fixture should contain header_size"),
        );
        assert_eq!(header_size, 11_273);
        let header_end =
            8 + usize::try_from(header_size).expect("fixture header_size should fit usize");
        assert_eq!(header_end, 11_281);

        let full_header = MinimalReplayHeaderReader
            .read_header(&ReplayInput::Memory {
                label: FIXTURE_002_LABEL.to_string(),
                bytes: bytes.clone(),
            })
            .expect("fixture_002 full bytes should parse");
        let header_only = MinimalReplayHeaderReader
            .read_header(&ReplayInput::Memory {
                label: FIXTURE_002_LABEL.to_string(),
                bytes: bytes[..header_end].to_vec(),
            })
            .expect("fixture_002 complete header-only slice should parse without body bytes");

        assert_fixture_002_header(&header_only);
        assert_eq!(header_only, full_header);
    }

    #[test]
    fn minimal_reader_parses_rl_replay_header_fixture_003_exact_happy_path() {
        let Some(bytes) = load_fixture_bytes_or_skip(FIXTURE_003_PATH, FIXTURE_003_LABEL) else {
            return;
        };

        let header = MinimalReplayHeaderReader
            .read_header(&ReplayInput::Memory {
                label: FIXTURE_003_LABEL.to_string(),
                bytes,
            })
            .expect("fixture_003 exact header should parse");

        assert_fixture_003_header(&header);
        assert!(header.metadata.get("bForfeit").is_none());
    }

    #[test]
    fn minimal_reader_parses_rl_replay_header_fixture_003_header_only_slice() {
        let Some(bytes) = load_fixture_bytes_or_skip(FIXTURE_003_PATH, FIXTURE_003_LABEL) else {
            return;
        };

        let header_size = i32::from_le_bytes(
            bytes[0..4]
                .try_into()
                .expect("fixture should contain header_size"),
        );
        assert_eq!(header_size, 11_190);
        let header_end =
            8 + usize::try_from(header_size).expect("fixture header_size should fit usize");
        assert_eq!(header_end, 11_198);

        let full_header = MinimalReplayHeaderReader
            .read_header(&ReplayInput::Memory {
                label: FIXTURE_003_LABEL.to_string(),
                bytes: bytes.clone(),
            })
            .expect("fixture_003 full bytes should parse");
        let header_only = MinimalReplayHeaderReader
            .read_header(&ReplayInput::Memory {
                label: FIXTURE_003_LABEL.to_string(),
                bytes: bytes[..header_end].to_vec(),
            })
            .expect("fixture_003 complete header-only slice should parse without body bytes");

        assert_fixture_003_header(&header_only);
        assert!(header_only.metadata.get("bForfeit").is_none());
        assert_eq!(header_only, full_header);
    }

    #[test]
    fn minimal_reader_rejects_file_input() {
        let error = MinimalReplayHeaderReader
            .read_header(&ReplayInput::file("sample.replay"))
            .expect_err("file input is outside the first minimal parser boundary");

        assert_error_contains(error, "replay header parse error: unsupported-input");
    }

    #[test]
    fn minimal_reader_rejects_empty_memory_label() {
        let error = MinimalReplayHeaderReader
            .read_header(&ReplayInput::Memory {
                label: String::new(),
                bytes: minimal_valid_replay_bytes(),
            })
            .expect_err("empty labels are not admitted source_label values");

        assert_error_contains(error, "replay header mapping error");
    }

    #[test]
    fn minimal_reader_rejects_fewer_than_4_bytes() {
        let error = read_synthetic(vec![1, 2, 3]).expect_err("header_size is truncated");

        assert_error_contains(error, "replay header parse error: insufficient");
    }

    #[test]
    fn minimal_reader_rejects_fewer_than_8_bytes() {
        let error =
            read_synthetic(0i32.to_le_bytes().to_vec()).expect_err("header_crc is truncated");

        assert_error_contains(error, "replay header parse error: insufficient");
    }

    #[test]
    fn minimal_reader_rejects_negative_header_size() {
        let mut bytes = Vec::new();
        bytes.extend_from_slice(&(-1i32).to_le_bytes());
        bytes.extend_from_slice(&0u32.to_le_bytes());

        let error = read_synthetic(bytes).expect_err("negative header_size is malformed");

        assert_error_contains(error, "replay header parse error: malformed");
    }

    #[test]
    fn minimal_reader_rejects_header_size_larger_than_bytes() {
        let mut bytes = Vec::new();
        bytes.extend_from_slice(&100i32.to_le_bytes());
        bytes.extend_from_slice(&0u32.to_le_bytes());

        let error = read_synthetic(bytes).expect_err("header region is truncated");

        assert_error_contains(error, "replay header parse error: insufficient");
    }

    #[test]
    fn minimal_reader_rejects_unsupported_version_tuple() {
        let bytes = build_replay_bytes(build_header(HeaderSpec {
            major_version: SUPPORTED_MAJOR_VERSION - 1,
            ..HeaderSpec::minimal()
        }));

        let error = read_synthetic(bytes).expect_err("only the admitted exact tuple is supported");

        assert_error_contains(error, "replay header parse error: unsupported-version");
    }

    #[test]
    fn minimal_reader_admits_top_ranked_corpus_build_exact_tuple() {
        let bytes = build_replay_bytes(build_header(HeaderSpec {
            build_version: SUPPORTED_BUILD_VERSION_CORPUS_RANK_001.to_string(),
            ..HeaderSpec::minimal()
        }));

        let header = read_synthetic(bytes)
            .expect("top-ranked corpus BuildVersion exact tuple should be admitted");

        assert_eq!(
            header.metadata.get("BuildVersion"),
            Some(&FieldValue::Text(
                SUPPORTED_BUILD_VERSION_CORPUS_RANK_001.to_string()
            ))
        );
    }

    #[test]
    fn minimal_reader_admits_second_ranked_corpus_build_exact_tuple() {
        let bytes = build_replay_bytes(build_header(HeaderSpec {
            build_version: SUPPORTED_BUILD_VERSION_CORPUS_RANK_002.to_string(),
            ..HeaderSpec::minimal()
        }));

        let header = read_synthetic(bytes)
            .expect("second-ranked corpus BuildVersion exact tuple should be admitted");

        assert_eq!(
            header.metadata.get("BuildVersion"),
            Some(&FieldValue::Text(
                SUPPORTED_BUILD_VERSION_CORPUS_RANK_002.to_string()
            ))
        );
    }

    #[test]
    fn minimal_reader_admits_third_ranked_corpus_build_exact_tuple() {
        let bytes = build_replay_bytes(build_header(HeaderSpec {
            build_version: SUPPORTED_BUILD_VERSION_CORPUS_RANK_003.to_string(),
            ..HeaderSpec::minimal()
        }));

        let header = read_synthetic(bytes)
            .expect("third-ranked corpus BuildVersion exact tuple should be admitted");

        assert_eq!(
            header.metadata.get("BuildVersion"),
            Some(&FieldValue::Text(
                SUPPORTED_BUILD_VERSION_CORPUS_RANK_003.to_string()
            ))
        );
    }

    #[test]
    fn minimal_reader_admits_fourth_ranked_corpus_build_exact_tuple() {
        let bytes = build_replay_bytes(build_header(HeaderSpec {
            build_version: SUPPORTED_BUILD_VERSION_CORPUS_RANK_004.to_string(),
            ..HeaderSpec::minimal()
        }));

        let header = read_synthetic(bytes)
            .expect("fourth-ranked corpus BuildVersion exact tuple should be admitted");

        assert_eq!(
            header.metadata.get("BuildVersion"),
            Some(&FieldValue::Text(
                SUPPORTED_BUILD_VERSION_CORPUS_RANK_004.to_string()
            ))
        );
    }

    #[test]
    fn minimal_reader_admits_fifth_ranked_corpus_build_exact_tuple() {
        let bytes = build_replay_bytes(build_header(HeaderSpec {
            build_version: SUPPORTED_BUILD_VERSION_CORPUS_RANK_005.to_string(),
            ..HeaderSpec::minimal()
        }));

        let header = read_synthetic(bytes)
            .expect("fifth-ranked corpus BuildVersion exact tuple should be admitted");

        assert_eq!(
            header.metadata.get("BuildVersion"),
            Some(&FieldValue::Text(
                SUPPORTED_BUILD_VERSION_CORPUS_RANK_005.to_string()
            ))
        );
    }

    #[test]
    fn minimal_reader_admits_sixth_ranked_corpus_build_exact_tuple() {
        let bytes = build_replay_bytes(build_header(HeaderSpec {
            build_version: SUPPORTED_BUILD_VERSION_CORPUS_RANK_006.to_string(),
            ..HeaderSpec::minimal()
        }));

        let header = read_synthetic(bytes)
            .expect("sixth-ranked corpus BuildVersion exact tuple should be admitted");

        assert_eq!(
            header.metadata.get("BuildVersion"),
            Some(&FieldValue::Text(
                SUPPORTED_BUILD_VERSION_CORPUS_RANK_006.to_string()
            ))
        );
    }

    #[test]
    fn minimal_reader_admits_seventh_ranked_corpus_build_exact_tuple() {
        let bytes = build_replay_bytes(build_header(HeaderSpec {
            build_version: SUPPORTED_BUILD_VERSION_CORPUS_RANK_007.to_string(),
            ..HeaderSpec::minimal()
        }));

        let header = read_synthetic(bytes)
            .expect("seventh-ranked corpus BuildVersion exact tuple should be admitted");

        assert_eq!(
            header.metadata.get("BuildVersion"),
            Some(&FieldValue::Text(
                SUPPORTED_BUILD_VERSION_CORPUS_RANK_007.to_string()
            ))
        );
    }

    #[test]
    fn minimal_reader_admits_eighth_ranked_corpus_build_exact_tuple() {
        let bytes = build_replay_bytes(build_header(HeaderSpec {
            build_version: SUPPORTED_BUILD_VERSION_CORPUS_RANK_008.to_string(),
            ..HeaderSpec::minimal()
        }));

        let header = read_synthetic(bytes)
            .expect("eighth-ranked corpus BuildVersion exact tuple should be admitted");

        assert_eq!(
            header.metadata.get("BuildVersion"),
            Some(&FieldValue::Text(
                SUPPORTED_BUILD_VERSION_CORPUS_RANK_008.to_string()
            ))
        );
    }

    #[test]
    fn minimal_reader_admits_ninth_ranked_corpus_build_exact_tuple() {
        let bytes = build_replay_bytes(build_header(HeaderSpec {
            build_version: SUPPORTED_BUILD_VERSION_CORPUS_RANK_009.to_string(),
            ..HeaderSpec::minimal()
        }));

        let header = read_synthetic(bytes)
            .expect("ninth-ranked corpus BuildVersion exact tuple should be admitted");

        assert_eq!(
            header.metadata.get("BuildVersion"),
            Some(&FieldValue::Text(
                SUPPORTED_BUILD_VERSION_CORPUS_RANK_009.to_string()
            ))
        );
    }

    #[test]
    fn minimal_reader_admits_tenth_ranked_corpus_build_exact_tuple() {
        let bytes = build_replay_bytes(build_header(HeaderSpec {
            build_version: SUPPORTED_BUILD_VERSION_CORPUS_RANK_010.to_string(),
            ..HeaderSpec::minimal()
        }));

        let header = read_synthetic(bytes)
            .expect("tenth-ranked corpus BuildVersion exact tuple should be admitted");

        assert_eq!(
            header.metadata.get("BuildVersion"),
            Some(&FieldValue::Text(
                SUPPORTED_BUILD_VERSION_CORPUS_RANK_010.to_string()
            ))
        );
    }

    #[test]
    fn minimal_reader_rejects_unknown_build_version_for_otherwise_supported_tuple() {
        let bytes = build_replay_bytes(build_header(HeaderSpec {
            build_version: "251020.62592.500295".to_string(),
            ..HeaderSpec::minimal()
        }));

        let error = read_synthetic(bytes).expect_err(
            "unknown BuildVersion near fixture_003 must not be accepted by wildcard policy",
        );

        assert_error_contains(error, "replay header parse error: unsupported-version");
    }

    #[test]
    fn minimal_reader_rejects_missing_terminator() {
        let bytes = build_replay_bytes(build_header(HeaderSpec {
            include_terminator: false,
            ..HeaderSpec::minimal()
        }));

        let error = read_synthetic(bytes).expect_err("top-level None terminator is required");

        assert_error_contains(error, "replay header parse error: malformed");
    }

    #[test]
    fn minimal_reader_rejects_duplicate_selected_property() {
        let mut spec = HeaderSpec::minimal();
        spec.extra_properties
            .push(PropertySpec::str("Id", "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"));
        let bytes = build_replay_bytes(build_header(spec));

        let error = read_synthetic(bytes).expect_err("duplicate selected properties are forbidden");

        assert_error_contains(error, "replay header mapping error");
    }

    #[test]
    fn minimal_reader_rejects_duplicate_top_level_property() {
        let mut spec = HeaderSpec::minimal();
        spec.extra_properties
            .push(PropertySpec::int("Team0Score", 1));
        spec.extra_properties
            .push(PropertySpec::int("Team0Score", 2));
        let bytes = build_replay_bytes(build_header(spec));

        let error =
            read_synthetic(bytes).expect_err("top-level duplicate properties are forbidden");

        assert_error_contains(error, "replay header parse error: malformed");
    }

    #[test]
    fn minimal_reader_skips_non_selected_bool_property_false_without_metadata() {
        let bytes =
            build_replay_with_bool_property(HeaderSpec::minimal(), "bForfeit", 0, &[0], true);

        let header =
            read_synthetic(bytes).expect("non-selected false BoolProperty should be skipped");

        assert!(header.metadata.get("bForfeit").is_none());
    }

    #[test]
    fn minimal_reader_skips_non_selected_bool_property_true_without_metadata() {
        let bytes =
            build_replay_with_bool_property(HeaderSpec::minimal(), "bForfeit", 0, &[1], true);

        let header =
            read_synthetic(bytes).expect("non-selected true BoolProperty should be skipped");

        assert!(header.metadata.get("bForfeit").is_none());
    }

    #[test]
    fn minimal_reader_rejects_selected_bool_property() {
        let bytes =
            build_replay_with_bool_property(HeaderSpec::minimal_without_id(), "Id", 0, &[1], true);

        let error =
            read_synthetic(bytes).expect_err("selected BoolProperty must remain unsupported");

        assert_error_contains(error, "replay header parse error: unsupported-property");
    }

    #[test]
    fn minimal_reader_rejects_non_selected_bool_property_nonzero_declared_size() {
        let bytes =
            build_replay_with_bool_property(HeaderSpec::minimal(), "bForfeit", 1, &[1], true);

        let error = read_synthetic(bytes)
            .expect_err("BoolProperty declared size other than zero must be malformed");

        assert_error_contains(error, "replay header parse error: malformed");
    }

    #[test]
    fn minimal_reader_rejects_truncated_non_selected_bool_property_value() {
        let bytes =
            build_replay_with_bool_property(HeaderSpec::minimal(), "bForfeit", 0, &[], false);

        let error = read_synthetic(bytes)
            .expect_err("BoolProperty missing its separate one-byte value must be insufficient");

        assert_error_contains(error, "replay header parse error: insufficient");
    }

    #[test]
    fn minimal_reader_rejects_invalid_non_selected_bool_property_value() {
        let bytes =
            build_replay_with_bool_property(HeaderSpec::minimal(), "bForfeit", 0, &[2], true);

        let error =
            read_synthetic(bytes).expect_err("BoolProperty values other than 0 or 1 are malformed");

        assert_error_contains(error, "replay header parse error: malformed");
    }

    #[test]
    fn minimal_reader_rejects_unknown_property_kind() {
        let mut spec = HeaderSpec::minimal();
        spec.extra_properties.push(PropertySpec {
            key: "Unselected".to_string(),
            kind: "ByteProperty".to_string(),
            value: vec![1],
        });
        let bytes = build_replay_bytes(build_header(spec));

        let error = read_synthetic(bytes).expect_err("unknown property kinds are unsupported");

        assert_error_contains(error, "replay header parse error: unsupported-property");
    }

    #[test]
    fn minimal_reader_rejects_negative_length_text() {
        let mut header = Vec::new();
        header.extend_from_slice(&SUPPORTED_MAJOR_VERSION.to_le_bytes());
        header.extend_from_slice(&SUPPORTED_MINOR_VERSION.to_le_bytes());
        header.extend_from_slice(&SUPPORTED_NET_VERSION.to_le_bytes());
        header.extend_from_slice(&(-1i32).to_le_bytes());
        let bytes = build_replay_bytes(header);

        let error = read_synthetic(bytes).expect_err("UTF-16 negative-length text is unsupported");

        assert_error_contains(error, "replay header parse error: unsupported-text");
    }

    #[test]
    fn minimal_reader_rejects_selected_array_property() {
        let mut spec = HeaderSpec::minimal_without_id();
        spec.extra_properties.push(PropertySpec {
            key: "Id".to_string(),
            kind: KIND_ARRAY.to_string(),
            value: 0i32.to_le_bytes().to_vec(),
        });
        let bytes = build_replay_bytes(build_header(spec));

        let error = read_synthetic(bytes).expect_err("selected arrays are unsupported");

        assert_error_contains(error, "replay header mapping error");
    }

    #[test]
    fn minimal_reader_rejects_selected_non_finite_float() {
        let mut spec = HeaderSpec::minimal();
        spec.extra_properties
            .push(PropertySpec::float("RecordFPS", f32::INFINITY));
        let bytes = build_replay_bytes(build_header(spec));

        let error = read_synthetic(bytes).expect_err("selected floats must be finite");

        assert_error_contains(error, "replay header mapping error");
    }

    #[test]
    fn minimal_reader_does_not_validate_header_crc() {
        let reader = MinimalReplayHeaderReader;
        let original = minimal_valid_replay_bytes();
        let original_header =
            read_synthetic(original.clone()).expect("baseline header should parse");

        let mut changed_crc = original;
        changed_crc[4..8].copy_from_slice(&0xA5A5_A5A5u32.to_le_bytes());
        let changed_header = reader
            .read_header(&ReplayInput::Memory {
                label: "synthetic".to_string(),
                bytes: changed_crc,
            })
            .expect("header_crc is read as layout only, not validated");

        assert_eq!(changed_header, original_header);
    }

    fn load_fixture_bytes_or_skip(default_path: &str, fixture_id: &str) -> Option<Vec<u8>> {
        let path = PathBuf::from(default_path);

        match fs::read(&path) {
            Ok(bytes) => Some(bytes),
            Err(error) => {
                eprintln!(
                    "fixture missing or unreadable at {}; skipping {fixture_id} fixture-specific test: {}",
                    path.display(),
                    error
                );
                None
            }
        }
    }

    fn assert_fixture_001_header(header: &ReplayHeader) {
        assert_eq!(
            header.replay_id,
            ReplayId::new("7F59297811EFD8B19C444A81FB07660C")
        );
        assert_eq!(header.source_label, FIXTURE_001_LABEL);
        assert_eq!(header.total_frames, Some(13_555));
        assert_eq!(
            header.metadata.get("ReplayName"),
            Some(&FieldValue::Text(
                "Frestyle double touch but not ball".to_string()
            ))
        );
        assert_eq!(
            header.metadata.get("Date"),
            Some(&FieldValue::Text("2025-01-22 11-10-32".to_string()))
        );
        assert_eq!(
            header.metadata.get("MapName"),
            Some(&FieldValue::Text("Stadium_Winter_P".to_string()))
        );
        assert_eq!(
            header.metadata.get("ReplayVersion"),
            Some(&FieldValue::Integer(8))
        );
        assert_eq!(
            header.metadata.get("BuildVersion"),
            Some(&FieldValue::Text(
                SUPPORTED_BUILD_VERSION_FIXTURE_001.to_string()
            ))
        );
        assert_eq!(
            header.metadata.get("MaxChannels"),
            Some(&FieldValue::Integer(2047))
        );
        assert_eq!(
            header.metadata.get("MatchType"),
            Some(&FieldValue::Text("Online".to_string()))
        );
        assert_eq!(
            header.metadata.get("TeamSize"),
            Some(&FieldValue::Integer(3))
        );
        assert_eq!(
            header.metadata.get("RecordFPS"),
            Some(&FieldValue::Float(30.0))
        );
    }

    fn assert_fixture_002_header(header: &ReplayHeader) {
        assert_eq!(
            header.replay_id,
            ReplayId::new("D9DA34DA11F0811EAC139A94CBF30AF2")
        );
        assert_eq!(header.source_label, FIXTURE_002_LABEL);
        assert_eq!(header.total_frames, Some(10_351));
        assert_eq!(
            header.metadata.get("ReplayName"),
            Some(&FieldValue::Text("asdasd".to_string()))
        );
        assert_eq!(
            header.metadata.get("Date"),
            Some(&FieldValue::Text("2025-08-24 19-16-35".to_string()))
        );
        assert_eq!(
            header.metadata.get("MapName"),
            Some(&FieldValue::Text("NeoTokyo_Standard_P".to_string()))
        );
        assert_eq!(
            header.metadata.get("ReplayVersion"),
            Some(&FieldValue::Integer(8))
        );
        assert_eq!(
            header.metadata.get("BuildVersion"),
            Some(&FieldValue::Text(
                SUPPORTED_BUILD_VERSION_FIXTURE_002.to_string()
            ))
        );
        assert_eq!(
            header.metadata.get("MaxChannels"),
            Some(&FieldValue::Integer(2047))
        );
        assert_eq!(
            header.metadata.get("MatchType"),
            Some(&FieldValue::Text("Online".to_string()))
        );
        assert_eq!(
            header.metadata.get("TeamSize"),
            Some(&FieldValue::Integer(3))
        );
        assert_eq!(
            header.metadata.get("RecordFPS"),
            Some(&FieldValue::Float(30.0))
        );
    }

    fn assert_fixture_003_header(header: &ReplayHeader) {
        assert_eq!(
            header.replay_id,
            ReplayId::new("DF72482811F0B757082C458D84251EFF")
        );
        assert_eq!(header.source_label, FIXTURE_003_LABEL);
        assert_eq!(header.total_frames, Some(8_288));
        assert_eq!(
            header.metadata.get("ReplayName"),
            Some(&FieldValue::Text("asdasd".to_string()))
        );
        assert_eq!(
            header.metadata.get("Date"),
            Some(&FieldValue::Text("2025-11-01 19-20-48".to_string()))
        );
        assert_eq!(
            header.metadata.get("MapName"),
            Some(&FieldValue::Text("cs_day_p".to_string()))
        );
        assert_eq!(
            header.metadata.get("ReplayVersion"),
            Some(&FieldValue::Integer(8))
        );
        assert_eq!(
            header.metadata.get("BuildVersion"),
            Some(&FieldValue::Text(
                SUPPORTED_BUILD_VERSION_FIXTURE_003.to_string()
            ))
        );
        assert_eq!(
            header.metadata.get("MaxChannels"),
            Some(&FieldValue::Integer(2047))
        );
        assert_eq!(
            header.metadata.get("MatchType"),
            Some(&FieldValue::Text("Online".to_string()))
        );
        assert_eq!(
            header.metadata.get("TeamSize"),
            Some(&FieldValue::Integer(2))
        );
        assert_eq!(
            header.metadata.get("RecordFPS"),
            Some(&FieldValue::Float(30.0))
        );
        assert!(header.metadata.get("bForfeit").is_none());
    }

    fn read_synthetic(bytes: Vec<u8>) -> Result<ReplayHeader> {
        MinimalReplayHeaderReader.read_header(&ReplayInput::Memory {
            label: "synthetic".to_string(),
            bytes,
        })
    }

    fn assert_error_contains(error: MimirError, expected: &str) {
        let message = error.to_string();
        assert!(
            message.contains(expected),
            "expected error to contain {expected:?}, got {message:?}"
        );
    }

    fn minimal_valid_replay_bytes() -> Vec<u8> {
        build_replay_bytes(build_header(HeaderSpec::minimal()))
    }

    struct HeaderSpec {
        major_version: i32,
        minor_version: i32,
        net_version: i32,
        game_type: String,
        include_id: bool,
        include_replay_version: bool,
        include_build_version: bool,
        build_version: String,
        include_terminator: bool,
        extra_properties: Vec<PropertySpec>,
    }

    impl HeaderSpec {
        fn minimal() -> Self {
            Self {
                major_version: SUPPORTED_MAJOR_VERSION,
                minor_version: SUPPORTED_MINOR_VERSION,
                net_version: SUPPORTED_NET_VERSION,
                game_type: SUPPORTED_GAME_TYPE.to_string(),
                include_id: true,
                include_replay_version: true,
                include_build_version: true,
                build_version: SUPPORTED_BUILD_VERSION_FIXTURE_001.to_string(),
                include_terminator: true,
                extra_properties: Vec::new(),
            }
        }

        fn minimal_without_id() -> Self {
            Self {
                include_id: false,
                ..Self::minimal()
            }
        }
    }

    struct PropertySpec {
        key: String,
        kind: String,
        value: Vec<u8>,
    }

    impl PropertySpec {
        fn str(key: &str, value: &str) -> Self {
            Self {
                key: key.to_string(),
                kind: KIND_STR.to_string(),
                value: encode_text(value),
            }
        }

        fn int(key: &str, value: i32) -> Self {
            Self {
                key: key.to_string(),
                kind: KIND_INT.to_string(),
                value: value.to_le_bytes().to_vec(),
            }
        }

        fn float(key: &str, value: f32) -> Self {
            Self {
                key: key.to_string(),
                kind: KIND_FLOAT.to_string(),
                value: value.to_le_bytes().to_vec(),
            }
        }
    }

    fn build_header(spec: HeaderSpec) -> Vec<u8> {
        let mut header = Vec::new();
        header.extend_from_slice(&spec.major_version.to_le_bytes());
        header.extend_from_slice(&spec.minor_version.to_le_bytes());
        header.extend_from_slice(&spec.net_version.to_le_bytes());
        header.extend_from_slice(&encode_text(&spec.game_type));

        if spec.include_id {
            append_property(
                &mut header,
                &PropertySpec::str("Id", "7F59297811EFD8B19C444A81FB07660C"),
            );
        }
        if spec.include_replay_version {
            append_property(
                &mut header,
                &PropertySpec::int("ReplayVersion", SUPPORTED_REPLAY_VERSION),
            );
        }
        if spec.include_build_version {
            append_property(
                &mut header,
                &PropertySpec::str("BuildVersion", &spec.build_version),
            );
        }
        for property in spec.extra_properties {
            append_property(&mut header, &property);
        }
        if spec.include_terminator {
            header.extend_from_slice(&encode_str("None"));
        }

        header
    }

    fn append_property(header: &mut Vec<u8>, property: &PropertySpec) {
        header.extend_from_slice(&encode_str(&property.key));
        header.extend_from_slice(&encode_str(&property.kind));
        header.extend_from_slice(
            &(u32::try_from(property.value.len()).expect("synthetic value should fit u32"))
                .to_le_bytes(),
        );
        header.extend_from_slice(&0u32.to_le_bytes());
        header.extend_from_slice(&property.value);
    }

    fn build_replay_with_bool_property(
        mut spec: HeaderSpec,
        key: &str,
        declared_size: u32,
        value_bytes: &[u8],
        include_terminator: bool,
    ) -> Vec<u8> {
        spec.include_terminator = false;
        let mut header = build_header(spec);
        append_bool_property(&mut header, key, declared_size, value_bytes);
        if include_terminator {
            header.extend_from_slice(&encode_str("None"));
        }
        build_replay_bytes(header)
    }

    fn append_bool_property(
        header: &mut Vec<u8>,
        key: &str,
        declared_size: u32,
        value_bytes: &[u8],
    ) {
        header.extend_from_slice(&encode_str(key));
        header.extend_from_slice(&encode_str(KIND_BOOL));
        header.extend_from_slice(&declared_size.to_le_bytes());
        header.extend_from_slice(&0u32.to_le_bytes());
        header.extend_from_slice(value_bytes);
    }

    fn build_replay_bytes(header: Vec<u8>) -> Vec<u8> {
        let mut replay = Vec::new();
        replay.extend_from_slice(
            &(i32::try_from(header.len()).expect("synthetic header should fit i32")).to_le_bytes(),
        );
        replay.extend_from_slice(&0u32.to_le_bytes());
        replay.extend_from_slice(&header);
        replay
    }

    fn build_body_boundary_bytes(
        header: &[u8],
        content_crc: u32,
        declared_content_size: i32,
        content: &[u8],
    ) -> Vec<u8> {
        let mut replay = Vec::new();
        replay.extend_from_slice(
            &(i32::try_from(header.len()).expect("synthetic header should fit i32")).to_le_bytes(),
        );
        replay.extend_from_slice(&0u32.to_le_bytes());
        replay.extend_from_slice(header);
        replay.extend_from_slice(&declared_content_size.to_le_bytes());
        replay.extend_from_slice(&content_crc.to_le_bytes());
        replay.extend_from_slice(content);
        replay
    }

    fn encode_str(value: &str) -> Vec<u8> {
        encode_len_prefixed_nul(value.as_bytes())
    }

    fn encode_text(value: &str) -> Vec<u8> {
        assert!(
            value.is_ascii(),
            "synthetic text helper only encodes ASCII admitted test values"
        );
        encode_len_prefixed_nul(value.as_bytes())
    }

    fn encode_len_prefixed_nul(bytes: &[u8]) -> Vec<u8> {
        let len = i32::try_from(bytes.len() + 1).expect("synthetic string should fit i32");
        let mut encoded = Vec::with_capacity(4 + bytes.len() + 1);
        encoded.extend_from_slice(&len.to_le_bytes());
        encoded.extend_from_slice(bytes);
        encoded.push(0);
        encoded
    }

    #[test]
    fn network_lookup_registry_has_exact_observed_attribute_surface() {
        assert_eq!(OBSERVED_NETWORK_ATTRIBUTE_TAGS_V1.len(), 102);
        let names = OBSERVED_NETWORK_ATTRIBUTE_TAGS_V1
            .iter()
            .map(|(name, _)| *name)
            .collect::<BTreeSet<_>>();
        assert_eq!(names.len(), 102);
        assert!(
            OBSERVED_NETWORK_ATTRIBUTE_TAGS_V1
                .iter()
                .all(|(_, tag)| *tag != ReplayNetworkAttributeTagV1::NotImplemented)
        );
        assert_eq!(
            OBSERVED_NETWORK_ATTRIBUTE_TAGS_V1
                .iter()
                .map(|(_, tag)| *tag)
                .collect::<BTreeSet<_>>()
                .len(),
            26
        );
    }

    #[test]
    fn network_lookup_registry_preserves_qword_string_wire_tag() {
        assert_eq!(
            replay_network_attribute_tag_v1("ProjectX.GRI_X:GameServerID"),
            ReplayNetworkAttributeTagV1::QWordString
        );
        assert_eq!(
            replay_network_attribute_tag_v1("TAGame.RBActor_TA:ReplicatedRBState"),
            ReplayNetworkAttributeTagV1::RigidBody
        );
    }

    #[test]
    fn network_lookup_registry_fails_closed_to_not_implemented() {
        assert_eq!(
            replay_network_attribute_tag_v1("TAGame.FutureClass:UnknownProperty"),
            ReplayNetworkAttributeTagV1::NotImplemented
        );
    }

    #[test]
    fn network_lookup_registry_qword_string_build_threshold_is_exact() {
        assert!(!replay_network_qword_string_uses_text_v1(
            "221120.42953.406183"
        ));
        assert!(replay_network_qword_string_uses_text_v1(
            "221120.42953.406184"
        ));
        assert!(replay_network_qword_string_uses_text_v1(
            "230113.44243.411503"
        ));
        assert!(!replay_network_qword_string_uses_text_v1(
            "220826.56130.393105"
        ));
    }

    #[test]
    fn network_lookup_registry_parent_surface_is_unique_and_acyclic() {
        assert_eq!(OBSERVED_NETWORK_PARENT_CLASSES_V1.len(), 65);
        let children = OBSERVED_NETWORK_PARENT_CLASSES_V1
            .iter()
            .map(|(child, _)| *child)
            .collect::<BTreeSet<_>>();
        assert_eq!(children.len(), 65);
        for (start, _) in OBSERVED_NETWORK_PARENT_CLASSES_V1 {
            let mut seen = BTreeSet::new();
            let mut current = start.to_string();
            while let Some(parent) = replay_network_parent_class_v1(&current) {
                assert!(seen.insert(current.clone()), "parent cycle at {current}");
                current = parent.to_string();
                assert!(seen.len() <= 65);
            }
        }
    }

    #[test]
    fn network_lookup_registry_normalizes_observed_persistent_instances() {
        assert_eq!(
            replay_network_object_name_v1("TheWorld:PersistentLevel.VehiclePickup_Boost_TA_37"),
            "TheWorld:PersistentLevel.VehiclePickup_Boost_TA"
        );
        assert_eq!(
            replay_network_object_name_v1("Stadium_P.TheWorld:PersistentLevel.CrowdActor_TA_12"),
            "TheWorld:PersistentLevel.CrowdActor_TA"
        );
        assert_eq!(
            replay_network_parent_class_v1("TheWorld:PersistentLevel.VehiclePickup_Boost_TA_37"),
            Some("TAGame.VehiclePickup_Boost_TA")
        );
        assert_eq!(
            replay_network_object_name_v1("TAGame.Car_TA"),
            "TAGame.Car_TA"
        );
    }

    #[test]
    fn network_lookup_registry_spawn_surface_matches_pinned_source() {
        assert_eq!(PINNED_NETWORK_SPAWN_STATS_V1.len(), 11);
        assert_eq!(
            replay_network_spawn_trajectory_class_v1("Engine.Actor"),
            Some(ReplayNetworkSpawnTrajectoryV1::Location)
        );
        assert_eq!(
            replay_network_spawn_trajectory_class_v1("TAGame.RBActor_TA"),
            Some(ReplayNetworkSpawnTrajectoryV1::LocationAndRotation)
        );
        assert_eq!(
            replay_network_spawn_trajectory_class_v1("TAGame.KeepUpIndicator_TA"),
            Some(ReplayNetworkSpawnTrajectoryV1::LocationAndRotation)
        );
        assert_eq!(
            replay_network_spawn_trajectory_class_v1("Unknown.Class"),
            None
        );
    }

    #[test]
    fn network_lookup_registry_explicit_surface_is_present_in_supported_footer_lane() {
        let mut paths = vec![
            std::path::PathBuf::from(env!("CARGO_MANIFEST_DIR"))
                .join("../../external_fixtures/sample_001.replay"),
            std::path::PathBuf::from(env!("CARGO_MANIFEST_DIR"))
                .join("../../external_fixtures/sample_002.replay"),
            std::path::PathBuf::from(env!("CARGO_MANIFEST_DIR"))
                .join("../../external_fixtures/sample_003.replay"),
        ];
        let root = std::path::PathBuf::from(env!("CARGO_MANIFEST_DIR"))
            .join("../../test_corpus/largest_100");
        if !root.is_dir() || paths.iter().any(|path| !path.is_file()) {
            eprintln!("skipping R3.12 corpus registry regression; fixtures are absent");
            return;
        }
        let mut corpus = std::fs::read_dir(&root)
            .expect("largest_100 should be readable")
            .map(|entry| entry.expect("corpus entry should be readable").path())
            .filter(|path| path.extension().and_then(|value| value.to_str()) == Some("replay"))
            .collect::<Vec<_>>();
        corpus.sort();
        assert_eq!(corpus.len(), 100);
        paths.extend(corpus);

        let mut supported = 0usize;
        let mut explicit_names = BTreeSet::new();
        let mut fallback_names = BTreeSet::new();
        for path in paths {
            let bytes = std::fs::read(&path).expect("replay should be readable");
            let label = path.file_name().unwrap().to_string_lossy().into_owned();
            let input = ReplayInput::Memory { label, bytes };
            if MinimalReplayHeaderReader.read_header(&input).is_err() {
                continue;
            }
            supported += 1;
            let lookup = MinimalReplayFooterLookupMaterializationReader
                .read_footer_lookup_materialization(&input)
                .expect("supported replay footer lookup should materialize");
            for cache in lookup.net_cache {
                for property in cache.properties {
                    let name = &lookup.objects[property.object_index as usize];
                    if replay_network_attribute_tag_v1(name)
                        == ReplayNetworkAttributeTagV1::NotImplemented
                    {
                        fallback_names.insert(name.clone());
                    } else {
                        explicit_names.insert(name.clone());
                    }
                }
            }
        }
        assert_eq!(supported, 47);
        assert_eq!(explicit_names.len(), 102);
        assert_eq!(
            explicit_names,
            OBSERVED_NETWORK_ATTRIBUTE_TAGS_V1
                .iter()
                .map(|(name, _)| (*name).to_string())
                .collect::<BTreeSet<_>>()
        );
        assert!(!fallback_names.is_empty());
    }

    #[test]
    fn network_lookup_plan_reader_rejects_file_input() {
        let input = ReplayInput::file("outside.replay");
        let error = MinimalReplayNetworkLookupPlanReader
            .read_network_lookup_plan(&input)
            .expect_err("file input must remain outside the lookup-plan reader");
        assert_error_contains(error, "replay network lookup plan error: unsupported-input");
    }

    #[test]
    fn network_lookup_plan_matches_three_historical_fixtures() {
        for (path, label) in [
            (FIXTURE_001_PATH, FIXTURE_001_LABEL),
            (FIXTURE_002_PATH, FIXTURE_002_LABEL),
            (FIXTURE_003_PATH, FIXTURE_003_LABEL),
        ] {
            let Some(bytes) = load_fixture_bytes_or_skip(path, label) else {
                return;
            };
            let input = ReplayInput::Memory {
                label: label.to_string(),
                bytes,
            };
            let plan = MinimalReplayNetworkLookupPlanReader
                .read_network_lookup_plan(&input)
                .expect("historical fixture should build admitted lookup plan");
            assert_eq!(plan.header.source_label, label);
            assert_eq!(plan.num_frames, plan.header.total_frames.unwrap());
            assert_eq!(plan.channel_bits, 10);
            assert!(!plan.is_lan);
            assert!(plan.qword_string_uses_text);
            assert_eq!(
                plan.spawn_trajectories.len(),
                plan.footer_lookup.objects.len()
            );
            assert_eq!(plan.object_lookups.len(), plan.footer_lookup.objects.len());
            assert!(plan.object_lookups.iter().flatten().next().is_some());
        }
    }

    #[test]
    fn network_lookup_plan_does_not_consume_network_payload_bytes() {
        let Some(bytes) = load_fixture_bytes_or_skip(FIXTURE_001_PATH, FIXTURE_001_LABEL) else {
            return;
        };
        let original_input = ReplayInput::Memory {
            label: FIXTURE_001_LABEL.to_string(),
            bytes: bytes.clone(),
        };
        let original = MinimalReplayNetworkLookupPlanReader
            .read_network_lookup_plan(&original_input)
            .expect("fixture should build original lookup plan");
        let network_start = usize::try_from(original.footer_lookup.scaffold.content.network_start)
            .expect("network_start should fit usize");
        assert!(original.footer_lookup.scaffold.content.network_size >= 8);

        let mut mutated = bytes;
        mutated[network_start..network_start + 8]
            .copy_from_slice(&[0xff, 0xff, 0xff, 0xff, 0x01, 0x02, 0x03, 0x04]);
        let mutated_input = ReplayInput::Memory {
            label: FIXTURE_001_LABEL.to_string(),
            bytes: mutated,
        };
        let after_mutation = MinimalReplayNetworkLookupPlanReader
            .read_network_lookup_plan(&mutated_input)
            .expect("lookup plan must stay independent of network payload bytes");
        assert_eq!(after_mutation, original);
    }

    #[test]
    fn network_lookup_plan_preserves_supported_47_lane_and_effective_property_evidence() {
        let mut paths = vec![
            std::path::PathBuf::from(env!("CARGO_MANIFEST_DIR"))
                .join("../../external_fixtures/sample_001.replay"),
            std::path::PathBuf::from(env!("CARGO_MANIFEST_DIR"))
                .join("../../external_fixtures/sample_002.replay"),
            std::path::PathBuf::from(env!("CARGO_MANIFEST_DIR"))
                .join("../../external_fixtures/sample_003.replay"),
        ];
        let root = std::path::PathBuf::from(env!("CARGO_MANIFEST_DIR"))
            .join("../../test_corpus/largest_100");
        if !root.is_dir() || paths.iter().any(|path| !path.is_file()) {
            eprintln!("skipping R3.13 corpus lookup-plan regression; fixtures are absent");
            return;
        }
        let mut corpus = std::fs::read_dir(&root)
            .expect("largest_100 should be readable")
            .map(|entry| entry.expect("corpus entry should be readable").path())
            .filter(|path| path.extension().and_then(|value| value.to_str()) == Some("replay"))
            .collect::<Vec<_>>();
        corpus.sort();
        assert_eq!(corpus.len(), 100);
        paths.extend(corpus);

        let mut supported = 0usize;
        let mut unsupported = 0usize;
        let mut total_effective_properties = 0u64;
        let mut effective_not_implemented = 0u64;
        for path in paths {
            let bytes = std::fs::read(&path).expect("replay should be readable");
            let label = path.file_name().unwrap().to_string_lossy().into_owned();
            let input = ReplayInput::Memory { label, bytes };
            match MinimalReplayNetworkLookupPlanReader.read_network_lookup_plan(&input) {
                Ok(plan) => {
                    supported += 1;
                    assert_eq!(plan.object_lookups.len(), plan.footer_lookup.objects.len());
                    assert_eq!(
                        plan.spawn_trajectories.len(),
                        plan.footer_lookup.objects.len()
                    );
                    for lookup in plan.object_lookups.iter().flatten() {
                        total_effective_properties += lookup.properties.len() as u64;
                        effective_not_implemented += lookup
                            .properties
                            .iter()
                            .filter(|property| {
                                property.tag == ReplayNetworkAttributeTagV1::NotImplemented
                            })
                            .count() as u64;
                    }
                }
                Err(error) => {
                    unsupported += 1;
                    assert_error_contains(error, "unsupported-version");
                }
            }
        }

        assert_eq!(supported, 47);
        assert_eq!(unsupported, 56);
        assert_eq!(total_effective_properties, 125_781);
        assert!(effective_not_implemented > 0);
    }

    fn synthetic_net_cache_entry(
        object_index: u32,
        properties: Vec<(u32, u32)>,
    ) -> ReplayNetCacheEntryV1 {
        ReplayNetCacheEntryV1 {
            object_index,
            parent_id: 0,
            cache_id: 0,
            properties: properties
                .into_iter()
                .map(
                    |(stream_id, property_object_index)| ReplayNetCachePropertyV1 {
                        object_index: property_object_index,
                        stream_id,
                    },
                )
                .collect(),
        }
    }

    #[test]
    fn network_lookup_plan_child_stream_overrides_parent_stream() {
        let objects = vec![
            "Engine.Actor".to_string(),
            "Engine.Pawn".to_string(),
            "ProjectX.Pawn_X".to_string(),
            "TAGame.RBActor_TA".to_string(),
            "Engine.Actor:DrawScale".to_string(),
            "TAGame.RBActor_TA:ReplicatedRBState".to_string(),
        ];
        let net_cache = vec![
            synthetic_net_cache_entry(0, vec![(5, 4)]),
            synthetic_net_cache_entry(3, vec![(5, 5)]),
        ];
        let (spawns, lookups) = build_replay_network_lookup_tables_v1(&objects, &net_cache)
            .expect("synthetic hierarchy should resolve");

        assert_eq!(
            spawns[3],
            ReplayNetworkSpawnTrajectoryV1::LocationAndRotation
        );
        let lookup = lookups[3].as_ref().expect("RBActor should have cache");
        assert_eq!(lookup.max_prop_id, 6);
        assert_eq!(lookup.prop_id_bits, 2);
        assert_eq!(lookup.properties.len(), 1);
        assert_eq!(lookup.properties[0].stream_id, 5);
        assert_eq!(lookup.properties[0].object_index, 5);
        assert_eq!(
            lookup.properties[0].tag,
            ReplayNetworkAttributeTagV1::RigidBody
        );
    }

    #[test]
    fn network_lookup_plan_rejects_duplicate_object_names() {
        let objects = vec!["Engine.Actor".to_string(), "Engine.Actor".to_string()];
        let error = build_replay_network_lookup_tables_v1(&objects, &[])
            .expect_err("duplicate object names are outside admitted evidence");
        assert_error_contains(error, "replay network lookup plan error: malformed");
    }

    #[test]
    fn network_lookup_plan_rejects_duplicate_cache_object_rows() {
        let objects = vec!["Engine.Actor".to_string()];
        let net_cache = vec![
            synthetic_net_cache_entry(0, vec![]),
            synthetic_net_cache_entry(0, vec![]),
        ];
        let error = build_replay_network_lookup_tables_v1(&objects, &net_cache)
            .expect_err("duplicate cache object rows are outside admitted evidence");
        assert_error_contains(error, "duplicate net-cache object index");
    }

    #[test]
    fn network_lookup_plan_rejects_duplicate_local_stream_ids() {
        let objects = vec![
            "Engine.Actor".to_string(),
            "Engine.Actor:DrawScale".to_string(),
            "Engine.Actor:bHidden".to_string(),
        ];
        let net_cache = vec![synthetic_net_cache_entry(0, vec![(7, 1), (7, 2)])];
        let error = build_replay_network_lookup_tables_v1(&objects, &net_cache)
            .expect_err("duplicate local stream ids are outside admitted evidence");
        assert_error_contains(error, "duplicate stream id 7");
    }

    #[test]
    fn network_lookup_plan_rejects_out_of_bounds_property_object() {
        let objects = vec!["Engine.Actor".to_string()];
        let net_cache = vec![synthetic_net_cache_entry(0, vec![(1, 99)])];
        let error = build_replay_network_lookup_tables_v1(&objects, &net_cache)
            .expect_err("property object index must stay in bounds");
        assert_error_contains(error, "net-cache property object index 99");
    }

    #[test]
    fn network_lookup_plan_preserves_missing_cache_for_root_without_parent() {
        let objects = vec!["Core.Object".to_string()];
        let (spawns, lookups) = build_replay_network_lookup_tables_v1(&objects, &[])
            .expect("root-only object table should remain structurally valid");
        assert_eq!(spawns, vec![ReplayNetworkSpawnTrajectoryV1::None]);
        assert_eq!(lookups, vec![None]);
    }

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
        let error =
            decode_network_new_actor_v1(&mut cursor, &[ReplayNetworkSpawnTrajectoryV1::None])
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
        let expected = ReplayNetworkVector3iV1 {
            x: -123,
            y: 456,
            z: 0,
        };
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
        let expected = ReplayNetworkRotationV1 {
            yaw: None,
            pitch: None,
            roll: None,
        };
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
        let expected = ReplayNetworkRotationV1 {
            yaw: Some(-5),
            pitch: None,
            roll: Some(9),
        };
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
        let rotation = ReplayNetworkRotationV1 {
            yaw: Some(-7),
            pitch: None,
            roll: Some(12),
        };
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
            let input = ReplayInput::Memory {
                label: label.to_string(),
                bytes,
            };
            let old = MinimalReplayNetworkFirstActorEnvelopeReader
                .read_network_first_actor_envelope(&input)
                .expect("admitted R3.14D envelope");
            let extended = MinimalReplayNetworkFirstNewActorEnvelopeReader
                .read_network_first_new_actor_envelope(&input)
                .expect("R3.15C additive envelope");
            assert_eq!(extended.envelope, old);
            let actor = extended
                .new_actor
                .expect("first actor is new in admitted fixture lane");
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
}

// R3.18AN PRE-ADMISSION BEGIN bounded post-AK payload composition
/// Bounded composition of the published R3.18AK following header plus exactly one
/// R3.18AM-observed Int payload.
///
/// `stop_bit` is exactly the first bit after the 32-bit Int payload. This type is
/// deliberately boundary-specific and does not admit another property-control bit,
/// another header/payload, a repeated property loop, or a generic cursor.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadV1 {
    pub header_composition:
        ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderV1,
    pub following_payload: ReplayNetworkPrimitiveScalarDecodeV1,
    pub stop_bit: u64,
}

fn network_existing_actor_post_ak_payload_error(
    category: &str,
    detail: impl Into<String>,
) -> MimirError {
    MimirError::message(format!(
        "replay network post-AK payload error: {category}: {}",
        detail.into()
    ))
}

/// Compose exactly one R3.18AM-observed Int payload after a valid published R3.18AK header.
///
/// The nested R3.18AK composition revalidates the supplied R3.18AG control and exact
/// R3.18AJ seven-field header membership. This function then reuses the existing stateless
/// primitive scalar decoder for exactly one Int payload, requires the observed 32-bit width,
/// and stops at the payload end without reading the next `property_present` bit.
pub fn decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_v1(
    network_bytes: &[u8],
    prior: &ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadV1,
    control: &ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlV1,
    lookup_plan: &ReplayNetworkLookupPlanV1,
    context: ReplayNetworkK3DecodeContextV1,
) -> Result<ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadV1>{
    let header_composition = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_v1(
        network_bytes,
        prior,
        control,
        lookup_plan,
        context,
    )?;

    let tag = header_composition
        .following_header
        .resolved_attribute_tag
        .ok_or_else(|| {
            network_existing_actor_post_ak_payload_error(
                "missing-resolved-attribute-tag",
                "published R3.18AK header has no resolved attribute tag",
            )
        })?;
    if tag != ReplayNetworkAttributeTagV1::Int {
        return Err(network_existing_actor_post_ak_payload_error(
            "unsupported-payload-tag",
            format!("R3.18AM admits only Int at this boundary, got {tag:?}"),
        ));
    }

    let payload_start_bit = header_composition
        .following_header
        .payload_start_bit
        .ok_or_else(|| {
            network_existing_actor_post_ak_payload_error(
                "missing-payload-start",
                "published R3.18AK header has no payload start",
            )
        })?;
    if payload_start_bit != header_composition.stop_bit
        || payload_start_bit != header_composition.following_header.stop_bit
    {
        return Err(network_existing_actor_post_ak_payload_error(
            "header-stop-mismatch",
            format!(
                "payload_start={payload_start_bit}, composition_stop={}, header_stop={}",
                header_composition.stop_bit, header_composition.following_header.stop_bit,
            ),
        ));
    }

    let following_payload =
        decode_replay_network_primitive_scalar_v1(network_bytes, payload_start_bit, tag)?;
    if following_payload.attribute_tag != ReplayNetworkAttributeTagV1::Int
        || following_payload.payload_start_bit != payload_start_bit
        || following_payload.payload_width != 32
        || following_payload.payload_end_bit != following_payload.stop_bit
        || !matches!(
            &following_payload.value,
            ReplayNetworkPrimitiveScalarValueV1::Int(_)
        )
    {
        return Err(network_existing_actor_post_ak_payload_error(
            "int-boundary-mismatch",
            format!(
                "start={}, end={}, width={}, stop={}, value={:?}",
                following_payload.payload_start_bit,
                following_payload.payload_end_bit,
                following_payload.payload_width,
                following_payload.stop_bit,
                following_payload.value,
            ),
        ));
    }
    let expected_end = payload_start_bit.checked_add(32).ok_or_else(|| {
        network_existing_actor_post_ak_payload_error(
            "payload-end-overflow",
            "32-bit Int payload end overflowed u64",
        )
    })?;
    if following_payload.payload_end_bit != expected_end {
        return Err(network_existing_actor_post_ak_payload_error(
            "payload-end-mismatch",
            format!(
                "payload start {payload_start_bit} requires end {expected_end}, got {}",
                following_payload.payload_end_bit,
            ),
        ));
    }

    let stop_bit = following_payload.stop_bit;
    Ok(ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadV1 {
        header_composition,
        following_payload,
        stop_bit,
    })
}
// R3.18AN PRE-ADMISSION END bounded post-AK payload composition

// R3.18AQ PRE-ADMISSION BEGIN bounded post-AN following control
/// Bounded composition of one published R3.18AN Int/32 payload result plus exactly one
/// R3.18AP-admitted following `property_present` control bit.
///
/// Both boolean values are admitted at this exact boundary. `stop_bit` is exactly one
/// bit after the validated R3.18AN payload end. No following stream/header/payload or
/// second later control bit is consumed.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlV1 {
    pub payload_composition: ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadV1,
    pub following_property_present: bool,
    pub property_present_start_bit: u64,
    pub property_present_end_bit: u64,
    pub stop_bit: u64,
}

fn network_existing_actor_post_an_following_control_error(
    category: &str,
    detail: impl Into<String>,
) -> MimirError {
    MimirError::message(format!(
        "replay network post-AN following-control error: {category}: {}",
        detail.into()
    ))
}

/// Validate/recompute exactly one published R3.18AN payload result, then consume exactly
/// one following LSB-first `property_present` bit.
///
/// Unlike the earlier true-only R3.18M/R3.18W/R3.18AG boundaries, R3.18AP observed both
/// false and true at this exact boundary. Therefore both values are successful data here.
/// This function deliberately stops before any following stream/header/payload or second
/// control bit and exposes no repeatable property cursor.
pub fn decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_v1(
    network_bytes: &[u8],
    prior: &ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadV1,
    control: &ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlV1,
    lookup_plan: &ReplayNetworkLookupPlanV1,
    context: ReplayNetworkK3DecodeContextV1,
    an_prior: &ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadV1,
) -> Result<ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlV1>{
    let expected_an = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_v1(
        network_bytes,
        prior,
        control,
        lookup_plan,
        context,
    )?;

    if expected_an != *an_prior {
        return Err(network_existing_actor_post_an_following_control_error(
            "invalid-r3-18an-prior",
            "supplied R3.18AN payload result does not match recomputed authority",
        ));
    }

    if an_prior.header_composition.stop_bit != an_prior.following_payload.payload_start_bit
        || an_prior.following_payload.payload_end_bit
            != an_prior
                .following_payload
                .payload_start_bit
                .checked_add(32)
                .ok_or_else(|| {
                    network_existing_actor_post_an_following_control_error(
                        "invalid-prior-boundary",
                        "R3.18AN payload boundary addition overflows u64",
                    )
                })?
        || an_prior.following_payload.payload_width != 32
        || an_prior.following_payload.stop_bit != an_prior.following_payload.payload_end_bit
        || an_prior.stop_bit != an_prior.following_payload.payload_end_bit
        || an_prior.following_payload.attribute_tag != ReplayNetworkAttributeTagV1::Int
        || !matches!(
            &an_prior.following_payload.value,
            ReplayNetworkPrimitiveScalarValueV1::Int(_)
        )
    {
        return Err(network_existing_actor_post_an_following_control_error(
            "invalid-prior-boundary",
            "supplied R3.18AN result is not the exact admitted Int/32 payload boundary",
        ));
    }

    let property_present_start_bit = an_prior.stop_bit;
    let property_present_start = usize::try_from(property_present_start_bit).map_err(|_| {
        network_existing_actor_post_an_following_control_error(
            "invalid-position",
            format!("R3.18AN stop bit {property_present_start_bit} does not fit usize"),
        )
    })?;
    let property_present_end = property_present_start.checked_add(1).ok_or_else(|| {
        network_existing_actor_post_an_following_control_error(
            "invalid-position",
            "following-control bit end overflows usize",
        )
    })?;
    let total_bits = network_bytes.len().checked_mul(8).ok_or_else(|| {
        network_existing_actor_post_an_following_control_error(
            "invalid-length",
            "network bit length overflows usize",
        )
    })?;
    if property_present_end > total_bits {
        return Err(network_existing_actor_post_an_following_control_error(
            "insufficient-bits",
            format!(
                "need one following control bit at {property_present_start}, but network ends at {total_bits}"
            ),
        ));
    }

    let mut cursor = NetworkBitCursor::new(network_bytes);
    cursor.bit_position = property_present_start;
    let following_property_present = cursor.read_bit().map_err(|error| {
        network_existing_actor_post_an_following_control_error(
            "control-read-failed",
            error.to_string(),
        )
    })?;
    if cursor.position_bits() != property_present_end {
        return Err(network_existing_actor_post_an_following_control_error(
            "invalid-stop",
            format!(
                "one control bit must stop at {property_present_end}, got {}",
                cursor.position_bits()
            ),
        ));
    }

    let property_present_end_bit = u64::try_from(property_present_end).map_err(|_| {
        network_existing_actor_post_an_following_control_error(
            "invalid-position",
            "following-control end does not fit u64",
        )
    })?;

    Ok(ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlV1 {
        payload_composition: an_prior.clone(),
        following_property_present,
        property_present_start_bit,
        property_present_end_bit,
        stop_bit: property_present_end_bit,
    })
}
// R3.18AQ PRE-ADMISSION END bounded post-AN following control

/// R3.18J bounded second-property payload value.
///
/// This enum represents exactly one second payload after the already-bounded R3.18G header
/// composition. It is not a generic property value/cursor and does not authorize another control
/// bit or property.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub enum ReplayNetworkExistingActorSecondPropertyPayloadV1 {
    Int(ReplayNetworkPrimitiveScalarDecodeV1),
    String(ReplayNetworkK2DecodeV1),
}

/// Result of composing at most one R3.18I-admitted second-property payload.
///
/// A terminator retains `second_payload == None` and stops at the R3.18G control end. A
/// continuation decodes exactly one `Int` or exact-context `String` payload and stops at that
/// payload's end. The following `property_present` bit is outside this API.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadV1 {
    pub header_composition: ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyHeaderV1,
    pub second_payload: Option<ReplayNetworkExistingActorSecondPropertyPayloadV1>,
    pub stop_bit: u64,
}

/// Compose exactly one optional R3.18I-admitted second payload after the R3.18G header boundary.
///
/// The String lane is intentionally restricted to the exact observed R3.18I decode context
/// (`net_version=10`, `is_rl_223=false`). No third-property control bit is read.
pub fn decode_replay_network_existing_actor_after_first_primitive_second_property_payload_v1(
    network_bytes: &[u8],
    first_property: &ReplayNetworkExistingActorSinglePrimitivePropertyV1,
    lookup_plan: &ReplayNetworkLookupPlanV1,
    k2_context: ReplayNetworkK2DecodeContextV1,
) -> Result<ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadV1> {
    let header_composition =
        decode_replay_network_existing_actor_after_first_primitive_second_property_header_v1(
            network_bytes,
            first_property,
            lookup_plan,
        )?;

    let Some(second_header) = header_composition.second_header.as_ref() else {
        let stop_bit = header_composition.stop_bit;
        return Ok(
            ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadV1 {
                header_composition,
                second_payload: None,
                stop_bit,
            },
        );
    };

    let payload_start_bit = second_header.payload_start_bit.ok_or_else(|| {
        network_bit_error(
            "missing-second-payload-start",
            "R3.18G returned a present second header without payload_start",
        )
    })?;
    if second_header.stop_bit != payload_start_bit
        || header_composition.stop_bit != payload_start_bit
    {
        return Err(network_bit_error(
            "inconsistent-second-payload-start",
            "R3.18G second-header stop does not equal payload_start",
        ));
    }

    let tag = second_header.resolved_attribute_tag.ok_or_else(|| {
        network_bit_error(
            "missing-second-attribute-tag",
            "R3.18G returned a present second header without a resolved tag",
        )
    })?;

    let second_payload = match tag {
        ReplayNetworkAttributeTagV1::Int => {
            let decoded = decode_replay_network_primitive_scalar_v1(
                network_bytes,
                payload_start_bit,
                ReplayNetworkAttributeTagV1::Int,
            )?;
            if decoded.payload_start_bit != payload_start_bit
                || decoded.stop_bit != decoded.payload_end_bit
            {
                return Err(network_bit_error(
                    "inconsistent-second-int-boundary",
                    "primitive Int decoder returned inconsistent payload coordinates",
                ));
            }
            ReplayNetworkExistingActorSecondPropertyPayloadV1::Int(decoded)
        }
        ReplayNetworkAttributeTagV1::String => {
            let admitted_context = ReplayNetworkK2DecodeContextV1 {
                net_version: 10,
                is_rl_223: false,
            };
            if k2_context != admitted_context {
                return Err(network_bit_error(
                    "unsupported-second-string-context",
                    format!(
                        "R3.18I admits String only at net_version=10/is_rl_223=false, got net_version={}/is_rl_223={}",
                        k2_context.net_version, k2_context.is_rl_223
                    ),
                ));
            }
            let decoded = decode_replay_network_k2_v1(
                network_bytes,
                payload_start_bit,
                ReplayNetworkAttributeTagV1::String,
                k2_context,
            )?;
            if decoded.payload_start_bit != payload_start_bit {
                return Err(network_bit_error(
                    "inconsistent-second-string-boundary",
                    "K2 String decoder returned an inconsistent payload start",
                ));
            }
            ReplayNetworkExistingActorSecondPropertyPayloadV1::String(decoded)
        }
        other => {
            return Err(network_bit_error(
                "unsupported-second-payload-tag",
                format!("R3.18J admits only Int/String second payloads, got {other:?}"),
            ));
        }
    };

    let stop_bit = match &second_payload {
        ReplayNetworkExistingActorSecondPropertyPayloadV1::Int(decoded) => decoded.payload_end_bit,
        ReplayNetworkExistingActorSecondPropertyPayloadV1::String(decoded) => {
            decoded.payload_end_bit
        }
    };
    if stop_bit < payload_start_bit {
        return Err(network_bit_error(
            "invalid-second-payload-end",
            "second payload end precedes payload start",
        ));
    }

    Ok(
        ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadV1 {
            header_composition,
            second_payload: Some(second_payload),
            stop_bit,
        },
    )
}

/// Exactly one evidence-admitted `property_present` bit after a valid R3.18J second payload.
/// This is not a generic or repeatedly-chainable property cursor.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingControlV1 {
    pub following_property_present: bool,
    pub property_present_start_bit: u64,
    pub property_present_end_bit: u64,
    pub stop_bit: u64,
}

fn network_existing_actor_after_second_payload_following_control_error(
    category: &str,
    detail: impl Into<String>,
) -> MimirError {
    MimirError::message(format!(
        "replay network after-second-payload following-control error: {category}: {}",
        detail.into()
    ))
}

/// Read exactly one R3.18L-admitted following control bit after a valid R3.18J result.
/// R3.18L observed only `true` (47/47); `false` therefore fails closed. No following
/// stream id, header, payload, extra control bit, or property loop is consumed.
pub fn decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_control_v1(
    network_bytes: &[u8],
    prior: &ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadV1,
) -> Result<ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingControlV1> {
    if !prior.header_composition.control.next_property_present {
        return Err(
            network_existing_actor_after_second_payload_following_control_error(
                "invalid-prior-control",
                "R3.18J prior does not contain a present second property",
            ),
        );
    }
    let second_header = prior
        .header_composition
        .second_header
        .as_ref()
        .ok_or_else(|| {
            network_existing_actor_after_second_payload_following_control_error(
                "missing-second-header",
                "R3.18J prior is missing its second property header",
            )
        })?;
    let payload_start = second_header.payload_start_bit.ok_or_else(|| {
        network_existing_actor_after_second_payload_following_control_error(
            "missing-second-payload-start",
            "R3.18J second header has no payload start",
        )
    })?;
    if prior.header_composition.stop_bit != payload_start || second_header.stop_bit != payload_start
    {
        return Err(
            network_existing_actor_after_second_payload_following_control_error(
                "prior-header-stop-mismatch",
                "R3.18J header composition does not stop exactly at second payload start",
            ),
        );
    }
    if second_header.property_present_start_bit
        != prior.header_composition.control.property_present_start_bit
        || second_header.property_present_end_bit
            != prior.header_composition.control.property_present_end_bit
        || prior.header_composition.control.stop_bit
            != prior.header_composition.control.property_present_end_bit
    {
        return Err(
            network_existing_actor_after_second_payload_following_control_error(
                "prior-control-header-mismatch",
                "R3.18J second control/header coordinates are inconsistent",
            ),
        );
    }
    let second_payload = prior.second_payload.as_ref().ok_or_else(|| {
        network_existing_actor_after_second_payload_following_control_error(
            "missing-second-payload",
            "R3.18J prior is missing its decoded second payload",
        )
    })?;
    let (decoded_start, decoded_end, expected_tag) = match second_payload {
        ReplayNetworkExistingActorSecondPropertyPayloadV1::Int(decoded) => {
            if decoded.stop_bit != decoded.payload_end_bit {
                return Err(
                    network_existing_actor_after_second_payload_following_control_error(
                        "prior-int-stop-mismatch",
                        "R3.18J Int payload stop differs from payload end",
                    ),
                );
            }
            (
                decoded.payload_start_bit,
                decoded.payload_end_bit,
                ReplayNetworkAttributeTagV1::Int,
            )
        }
        ReplayNetworkExistingActorSecondPropertyPayloadV1::String(decoded) => (
            decoded.payload_start_bit,
            decoded.payload_end_bit,
            ReplayNetworkAttributeTagV1::String,
        ),
    };
    if decoded_start != payload_start {
        return Err(
            network_existing_actor_after_second_payload_following_control_error(
                "prior-payload-start-mismatch",
                "R3.18J decoded payload start differs from second header payload start",
            ),
        );
    }
    if second_header.resolved_attribute_tag != Some(expected_tag) {
        return Err(
            network_existing_actor_after_second_payload_following_control_error(
                "prior-payload-tag-mismatch",
                "R3.18J second header tag disagrees with decoded second payload",
            ),
        );
    }
    if prior.stop_bit != decoded_end {
        return Err(
            network_existing_actor_after_second_payload_following_control_error(
                "prior-stop-mismatch",
                format!(
                    "R3.18J prior stop {} differs from second payload end {decoded_end}",
                    prior.stop_bit
                ),
            ),
        );
    }

    let property_present_start_bit = prior.stop_bit;
    let property_present_end_bit = property_present_start_bit.checked_add(1).ok_or_else(|| {
        network_existing_actor_after_second_payload_following_control_error(
            "invalid-position",
            "following property_present end bit overflows u64",
        )
    })?;
    let start = usize::try_from(property_present_start_bit).map_err(|_| {
        network_existing_actor_after_second_payload_following_control_error(
            "invalid-position",
            "following property_present start does not fit usize",
        )
    })?;
    let end = usize::try_from(property_present_end_bit).map_err(|_| {
        network_existing_actor_after_second_payload_following_control_error(
            "invalid-position",
            "following property_present end does not fit usize",
        )
    })?;
    let total_bits = network_bytes.len().checked_mul(8).ok_or_else(|| {
        network_existing_actor_after_second_payload_following_control_error(
            "invalid-length",
            "network bit length overflows usize",
        )
    })?;
    if end > total_bits {
        return Err(
            network_existing_actor_after_second_payload_following_control_error(
                "insufficient-bits",
                format!("need one following control bit at {start}, network has {total_bits} bits"),
            ),
        );
    }
    let mut cursor = NetworkBitCursor::new(network_bytes);
    cursor.bit_position = start;
    let following_property_present = cursor.read_bit()?;
    let stop_bit = network_position_to_u64(cursor.position_bits())?;
    if stop_bit != property_present_end_bit {
        return Err(
            network_existing_actor_after_second_payload_following_control_error(
                "control-stop-mismatch",
                "one-bit following control did not stop at its exact end",
            ),
        );
    }
    if !following_property_present {
        return Err(
            network_existing_actor_after_second_payload_following_control_error(
                "unadmitted-false-following-control",
                "R3.18L observed no false after-second-payload control witness",
            ),
        );
    }
    Ok(
        ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingControlV1 {
            following_property_present,
            property_present_start_bit,
            property_present_end_bit,
            stop_bit,
        },
    )
}

/// One R3.18P-admitted following property header composed after a valid R3.18M true control.
///
/// This result stops exactly at the following header's payload boundary. It does not decode the
/// following payload, consume another property-control bit, or expose a repeatable property cursor.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingHeaderV1 {
    pub control:
        ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingControlV1,
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
            | (
                60,
                5,
                80,
                ReplayNetworkAttributeTagV1::ActiveActor,
                868,
                32,
                10
            )
            | (
                60,
                5,
                83,
                ReplayNetworkAttributeTagV1::ActiveActor,
                868,
                32,
                10
            )
            | (60, 5, 85, ReplayNetworkAttributeTagV1::Boolean, 868, 32, 10)
            | (60, 5, 87, ReplayNetworkAttributeTagV1::Boolean, 868, 32, 10)
            | (60, 5, 89, ReplayNetworkAttributeTagV1::Boolean, 868, 32, 10)
            | (60, 5, 94, ReplayNetworkAttributeTagV1::Boolean, 868, 32, 10)
            | (
                60,
                5,
                102,
                ReplayNetworkAttributeTagV1::Boolean,
                868,
                32,
                10
            )
            | (
                60,
                5,
                103,
                ReplayNetworkAttributeTagV1::Boolean,
                868,
                32,
                10
            )
            | (
                60,
                5,
                106,
                ReplayNetworkAttributeTagV1::Boolean,
                868,
                32,
                10
            )
            | (
                60,
                5,
                116,
                ReplayNetworkAttributeTagV1::Boolean,
                868,
                32,
                10
            )
            | (67, 6, 61, ReplayNetworkAttributeTagV1::Boolean, 868, 32, 10)
            | (72, 6, 62, ReplayNetworkAttributeTagV1::Boolean, 868, 32, 10)
            | (72, 6, 65, ReplayNetworkAttributeTagV1::Boolean, 868, 32, 10)
            | (
                110,
                6,
                36,
                ReplayNetworkAttributeTagV1::ActiveActor,
                868,
                32,
                10
            )
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
        return Err(
            network_existing_actor_after_second_payload_following_header_error(
                "invalid-following-control",
                "R3.18Q requires the R3.18M admitted true following control",
            ),
        );
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
        return Err(
            network_existing_actor_after_second_payload_following_header_error(
                "control-header-mismatch",
                "R3.18M reported a present following property but the header primitive did not",
            ),
        );
    }
    if following_header.property_present_start_bit != control.property_present_start_bit
        || following_header.property_present_end_bit != control.property_present_end_bit
        || control.stop_bit != following_header.property_present_end_bit
    {
        return Err(
            network_existing_actor_after_second_payload_following_header_error(
                "control-header-boundary-mismatch",
                format!(
                    "control bits [{}, {}) stop {}, header bits [{}, {})",
                    control.property_present_start_bit,
                    control.property_present_end_bit,
                    control.stop_bit,
                    following_header.property_present_start_bit,
                    following_header.property_present_end_bit
                ),
            ),
        );
    }
    if following_header.actor_object_index != actor_object_index {
        return Err(
            network_existing_actor_after_second_payload_following_header_error(
                "actor-mismatch",
                format!(
                    "prior actor {actor_object_index} differs from following header actor {}",
                    following_header.actor_object_index
                ),
            ),
        );
    }

    let payload_start_bit = following_header.payload_start_bit.ok_or_else(|| {
        network_existing_actor_after_second_payload_following_header_error(
            "missing-payload-start",
            "present following header has no payload start",
        )
    })?;
    if following_header.stop_bit != payload_start_bit {
        return Err(
            network_existing_actor_after_second_payload_following_header_error(
                "payload-boundary-mismatch",
                format!(
                    "following header stop {} differs from payload start {payload_start_bit}",
                    following_header.stop_bit
                ),
            ),
        );
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
        return Err(
            network_existing_actor_after_second_payload_following_header_error(
                "incomplete-header-context",
                "following header is missing one or more R3.18P tuple fields",
            ),
        );
    };

    if !r3_18p_following_header_context_is_admitted(
        stream_id_bound,
        prop_id_bits,
        property_object_index,
        attribute_tag,
        context,
    ) {
        return Err(
            network_existing_actor_after_second_payload_following_header_error(
                "unadmitted-following-header-context",
                format!(
                    "R3.18P exact tuple rejected bound={stream_id_bound} bits={prop_id_bits} object={property_object_index} tag={attribute_tag:?} version={}.{} net{}",
                    context.version_major, context.version_minor, context.net_version
                ),
            ),
        );
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

/// Exactly one R3.18S-admitted payload after the bounded R3.18Q following-property header.
///
/// This enum is deliberately closed to the two payload forms proven on the immutable
/// R3.18S lane. It is not a generic attribute-payload carrier.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub enum ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadValueV1 {
    Boolean(ReplayNetworkPrimitiveScalarDecodeV1),
    ActiveActor(ReplayNetworkK2DecodeV1),
}

/// Bounded composition of the published R3.18Q following header plus exactly one
/// R3.18S-admitted payload.
///
/// `stop_bit` is exactly the first bit after that payload. It does not imply permission
/// to read another property-control bit, another header/payload, actor, frame, or loop.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadV1 {
    pub header_composition:
        ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingHeaderV1,
    pub following_payload:
        ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadValueV1,
    pub stop_bit: u64,
}

/// Compose exactly one R3.18S-admitted following payload after the published R3.18Q
/// following-property header.
///
/// This function deliberately stops at the payload end and never reads the next
/// `property_present` control bit. Exact R3.18P structural/version membership remains
/// enforced by the nested R3.18Q header composition.
pub fn decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_v1(
    network_bytes: &[u8],
    prior: &ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadV1,
    lookup_plan: &ReplayNetworkLookupPlanV1,
    context: ReplayNetworkK3DecodeContextV1,
) -> Result<ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadV1> {
    let k2_context = ReplayNetworkK2DecodeContextV1 {
        net_version: context.net_version,
        is_rl_223: context.is_rl_223,
    };
    let header_composition =
        decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_header_v1(
            network_bytes,
            prior,
            lookup_plan,
            context,
        )?;

    let tag = header_composition
        .following_header
        .resolved_attribute_tag
        .ok_or_else(|| {
            MimirError::message(
                "replay existing actor R3.18T following payload error: missing-resolved-attribute-tag",
            )
        })?;
    let payload_start_bit = header_composition
        .following_header
        .payload_start_bit
        .ok_or_else(|| {
            MimirError::message(
                "replay existing actor R3.18T following payload error: missing-payload-start",
            )
        })?;
    if payload_start_bit != header_composition.stop_bit
        || payload_start_bit != header_composition.following_header.stop_bit
    {
        return Err(MimirError::message(format!(
            "replay existing actor R3.18T following payload error: header-stop-mismatch: payload_start={payload_start_bit}, composition_stop={}, header_stop={}",
            header_composition.stop_bit, header_composition.following_header.stop_bit,
        )));
    }

    let (following_payload, stop_bit) = match tag {
        ReplayNetworkAttributeTagV1::Boolean => {
            let decoded =
                decode_replay_network_primitive_scalar_v1(network_bytes, payload_start_bit, tag)?;
            if decoded.attribute_tag != ReplayNetworkAttributeTagV1::Boolean
                || decoded.payload_start_bit != payload_start_bit
                || decoded.payload_width != 1
                || decoded.payload_end_bit != decoded.stop_bit
            {
                return Err(MimirError::message(format!(
                    "replay existing actor R3.18T following payload error: boolean-boundary-mismatch: start={}, end={}, width={}, stop={}",
                    decoded.payload_start_bit,
                    decoded.payload_end_bit,
                    decoded.payload_width,
                    decoded.stop_bit,
                )));
            }
            let stop_bit = decoded.stop_bit;
            (
                ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadValueV1::Boolean(decoded),
                stop_bit,
            )
        }
        ReplayNetworkAttributeTagV1::ActiveActor => {
            let decoded =
                decode_replay_network_k2_v1(network_bytes, payload_start_bit, tag, k2_context)?;
            if decoded.attribute_tag != ReplayNetworkAttributeTagV1::ActiveActor
                || decoded.payload_start_bit != payload_start_bit
                || decoded.payload_width != 33
            {
                return Err(MimirError::message(format!(
                    "replay existing actor R3.18T following payload error: active-actor-boundary-mismatch: start={}, end={}, width={}",
                    decoded.payload_start_bit, decoded.payload_end_bit, decoded.payload_width,
                )));
            }
            let stop_bit = decoded.payload_end_bit;
            (
                ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadValueV1::ActiveActor(decoded),
                stop_bit,
            )
        }
        other => {
            return Err(MimirError::message(format!(
                "replay existing actor R3.18T following payload error: unsupported-following-payload-tag: R3.18S admits only Boolean/ActiveActor, got {other:?}",
            )));
        }
    };

    if stop_bit < payload_start_bit {
        return Err(MimirError::message(format!(
            "replay existing actor R3.18T following payload error: invalid-stop: payload_start={payload_start_bit}, stop={stop_bit}",
        )));
    }

    Ok(
        ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadV1 {
            header_composition,
            following_payload,
            stop_bit,
        },
    )
}

/// R3.18W bounded true-only control after one published R3.18T following payload.
///
/// Exactly one R3.18Z-admitted existing-actor property header after a valid R3.18W control.
///
/// This result is boundary-specific. It stops exactly at the following header's `payload_start`
/// and does not decode that payload, consume another control bit, or expose a repeatable cursor.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderV1
{
    pub control:
        ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlV1,
    pub following_header: ReplayNetworkExistingActorFirstPropertyHeaderV1,
    pub stop_bit: u64,
}

fn network_existing_actor_after_following_payload_control_following_header_error(
    category: &str,
    detail: impl Into<String>,
) -> MimirError {
    MimirError::message(format!(
        "replay network post-W following-header error: {category}: {}",
        detail.into()
    ))
}

fn r3_18z_post_w_following_header_context_admitted_v1(
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
        (
            60,
            5,
            34,
            ReplayNetworkAttributeTagV1::ActiveActor,
            868,
            32,
            10
        ) | (
            60,
            5,
            43,
            ReplayNetworkAttributeTagV1::ActiveActor,
            868,
            32,
            10
        ) | (
            60,
            5,
            80,
            ReplayNetworkAttributeTagV1::ActiveActor,
            868,
            32,
            10
        ) | (
            60,
            5,
            81,
            ReplayNetworkAttributeTagV1::ActiveActor,
            868,
            32,
            10
        ) | (60, 5, 84, ReplayNetworkAttributeTagV1::Int, 868, 32, 10)
            | (
                60,
                5,
                87,
                ReplayNetworkAttributeTagV1::ActiveActor,
                868,
                32,
                10
            )
            | (60, 5, 87, ReplayNetworkAttributeTagV1::Int, 868, 32, 10)
            | (
                60,
                5,
                89,
                ReplayNetworkAttributeTagV1::ActiveActor,
                868,
                32,
                10
            )
            | (
                60,
                5,
                91,
                ReplayNetworkAttributeTagV1::ActiveActor,
                868,
                32,
                10
            )
            | (
                60,
                5,
                96,
                ReplayNetworkAttributeTagV1::ActiveActor,
                868,
                32,
                10
            )
            | (
                60,
                5,
                104,
                ReplayNetworkAttributeTagV1::ActiveActor,
                868,
                32,
                10
            )
            | (
                60,
                5,
                105,
                ReplayNetworkAttributeTagV1::ActiveActor,
                868,
                32,
                10
            )
            | (
                60,
                5,
                108,
                ReplayNetworkAttributeTagV1::ActiveActor,
                868,
                32,
                10
            )
            | (
                60,
                5,
                118,
                ReplayNetworkAttributeTagV1::ActiveActor,
                868,
                32,
                10
            )
            | (
                67,
                6,
                63,
                ReplayNetworkAttributeTagV1::ActiveActor,
                868,
                32,
                10
            )
            | (
                72,
                6,
                65,
                ReplayNetworkAttributeTagV1::ActiveActor,
                868,
                32,
                10
            )
            | (
                72,
                6,
                68,
                ReplayNetworkAttributeTagV1::ActiveActor,
                868,
                32,
                10
            )
            | (
                110,
                6,
                25,
                ReplayNetworkAttributeTagV1::UniqueId,
                868,
                32,
                10
            )
    )
}

/// Compose exactly one post-R3.18W following header under the R3.18Z exact-tuple contract.
///
/// Exactly one R3.18AF-admitted `property_present` bit after a valid published R3.18AD payload.
///
/// R3.18AF observed true=47 and false=0 on the immutable lane. This result therefore admits
/// `true` only and stops exactly one bit later. It does not resolve a following stream/header/
/// payload, read a second later control bit, or expose a repeatable property cursor.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlV1
{
    pub following_property_present: bool,
    pub property_present_start_bit: u64,
    pub property_present_end_bit: u64,
    pub stop_bit: u64,
}

fn network_existing_actor_post_ad_following_payload_control_error(
    category: &str,
    detail: impl Into<String>,
) -> MimirError {
    MimirError::message(format!(
        "replay network post-AD following payload control error: {category}: {}",
        detail.into()
    ))
}

fn validate_network_existing_actor_post_ad_payload_prior(
    prior: &ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadV1,
) -> Result<()> {
    let header_stop = prior.header_composition.stop_bit;
    let following_header = &prior.header_composition.following_header;
    if !following_header.property_present
        || following_header.payload_start_bit != Some(header_stop)
        || following_header.stop_bit != header_stop
        || prior.payload_start_bit != header_stop
    {
        return Err(
            network_existing_actor_post_ad_following_payload_control_error(
                "invalid-prior-header",
                format!(
                    "header property_present={}, payload_start={:?}, header stop={}, composition stop={}, payload start={}",
                    following_header.property_present,
                    following_header.payload_start_bit,
                    following_header.stop_bit,
                    header_stop,
                    prior.payload_start_bit,
                ),
            ),
        );
    }

    let expected_end = prior
        .payload_start_bit
        .checked_add(prior.payload_width)
        .ok_or_else(|| {
            network_existing_actor_post_ad_following_payload_control_error(
                "invalid-prior-payload",
                "payload end overflows u64",
            )
        })?;
    if prior.stop_bit != expected_end {
        return Err(
            network_existing_actor_post_ad_following_payload_control_error(
                "invalid-prior-stop",
                format!(
                    "prior stop {} does not equal payload start {} + width {} = {expected_end}",
                    prior.stop_bit, prior.payload_start_bit, prior.payload_width
                ),
            ),
        );
    }

    let valid_shape = match &prior.following_payload {
        ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadValueV1::ActiveActor(decoded) => {
            following_header.resolved_attribute_tag == Some(ReplayNetworkAttributeTagV1::ActiveActor)
                && prior.payload_width == 33
                && decoded.attribute_tag == ReplayNetworkAttributeTagV1::ActiveActor
                && decoded.payload_start_bit == prior.payload_start_bit
                && decoded.payload_width == 33
                && decoded.payload_end_bit == expected_end
                && matches!(&decoded.value, ReplayNetworkK2ValueV1::ActiveActor { .. })
        }
        ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadValueV1::Int(decoded) => {
            following_header.resolved_attribute_tag == Some(ReplayNetworkAttributeTagV1::Int)
                && prior.payload_width == 32
                && decoded.attribute_tag == ReplayNetworkAttributeTagV1::Int
                && decoded.payload_start_bit == prior.payload_start_bit
                && decoded.payload_width == 32
                && decoded.payload_end_bit == expected_end
                && decoded.stop_bit == expected_end
                && matches!(&decoded.value, ReplayNetworkPrimitiveScalarValueV1::Int(_))
        }
        ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadValueV1::UniqueId(decoded) => {
            let admitted_unique_id = match &decoded.value {
                ReplayNetworkK2ValueV1::UniqueId(value) => {
                    value.system_id == 1
                        && matches!(&value.remote_id, ReplayNetworkUniqueIdRemoteV1::Steam { .. })
                }
                _ => false,
            };
            following_header.resolved_attribute_tag == Some(ReplayNetworkAttributeTagV1::UniqueId)
                && prior.payload_width == 80
                && decoded.attribute_tag == ReplayNetworkAttributeTagV1::UniqueId
                && decoded.payload_start_bit == prior.payload_start_bit
                && decoded.payload_width == 80
                && decoded.payload_end_bit == expected_end
                && admitted_unique_id
        }
    };
    if !valid_shape {
        return Err(
            network_existing_actor_post_ad_following_payload_control_error(
                "invalid-prior-payload",
                "prior header/payload is outside the R3.18AD ActiveActor/33, Int/32, UniqueId system1-Steam/80 allowlist",
            ),
        );
    }
    Ok(())
}

/// Consume exactly one R3.18AF-admitted true control bit after one valid published R3.18AD payload.
///
/// False is not evidence-admitted and fails closed. No following stream/header/payload or second
/// later control is read.
pub fn decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_v1(
    network_bytes: &[u8],
    prior: &ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadV1,
    context: ReplayNetworkK3DecodeContextV1,
) -> Result<ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlV1>{
    if context.version_major != 868
        || context.version_minor != 32
        || context.net_version != 10
        || context.is_rl_223
    {
        return Err(
            network_existing_actor_post_ad_following_payload_control_error(
                "unadmitted-context",
                format!(
                    "R3.18AG requires 868.32 / net10 / non-RL223, got {}.{} / net{} / rl223={}",
                    context.version_major,
                    context.version_minor,
                    context.net_version,
                    context.is_rl_223,
                ),
            ),
        );
    }
    validate_network_existing_actor_post_ad_payload_prior(prior)?;

    let property_present_start_bit = prior.stop_bit;
    let start = usize::try_from(property_present_start_bit).map_err(|_| {
        network_existing_actor_post_ad_following_payload_control_error(
            "invalid-position",
            format!("control start {property_present_start_bit} does not fit usize"),
        )
    })?;
    let mut cursor = NetworkBitCursor::new(network_bytes);
    cursor.bit_position = start;
    let following_property_present = cursor.read_bit()?;
    if !following_property_present {
        return Err(
            network_existing_actor_post_ad_following_payload_control_error(
                "unadmitted-false-control",
                format!(
                    "R3.18AF observed true=47 false=0 at exact control start {property_present_start_bit}"
                ),
            ),
        );
    }
    let property_present_end_bit = property_present_start_bit.checked_add(1).ok_or_else(|| {
        network_existing_actor_post_ad_following_payload_control_error(
            "invalid-position",
            "control end overflows u64",
        )
    })?;
    if u64::try_from(cursor.position_bits()).ok() != Some(property_present_end_bit) {
        return Err(
            network_existing_actor_post_ad_following_payload_control_error(
                "invalid-stop",
                "one-bit control cursor did not stop at the exact admitted end",
            ),
        );
    }

    Ok(ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadFollowingPayloadControlV1 {
        following_property_present,
        property_present_start_bit,
        property_present_end_bit,
        stop_bit: property_present_end_bit,
    })
}

/// The published R3.18W true-only control is recomputed from the supplied R3.18T prior and used
/// as the sole boundary authority. The existing stateless property-header primitive is replayed
/// from that exact present-bit coordinate. The complete seven-field structural tuple must belong
/// to R3.18Z. The function stops at `payload_start` and consumes no payload or later control bit.
pub fn decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_v1(
    network_bytes: &[u8],
    prior: &ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadV1,
    lookup_plan: &ReplayNetworkLookupPlanV1,
    context: ReplayNetworkK3DecodeContextV1,
) -> Result<ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderV1>{
    let control = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_v1(
        network_bytes,
        prior,
    )?;
    if !control.following_property_present {
        return Err(
            network_existing_actor_after_following_payload_control_following_header_error(
                "invalid-r3-18w-control",
                "R3.18AA requires the published R3.18W admitted true control",
            ),
        );
    }

    let actor_object_index = prior.header_composition.following_header.actor_object_index;
    let following_header = decode_replay_network_existing_actor_first_property_header_v1(
        network_bytes,
        control.property_present_start_bit,
        actor_object_index,
        lookup_plan,
    )?;

    if !following_header.property_present {
        return Err(
            network_existing_actor_after_following_payload_control_following_header_error(
                "control-header-mismatch",
                "R3.18W reported a present property but the post-W header primitive did not",
            ),
        );
    }
    if following_header.property_present_start_bit != control.property_present_start_bit
        || following_header.property_present_end_bit != control.property_present_end_bit
        || control.stop_bit != following_header.property_present_end_bit
    {
        return Err(
            network_existing_actor_after_following_payload_control_following_header_error(
                "control-header-boundary-mismatch",
                format!(
                    "control bits [{}, {}) stop {}, header bits [{}, {})",
                    control.property_present_start_bit,
                    control.property_present_end_bit,
                    control.stop_bit,
                    following_header.property_present_start_bit,
                    following_header.property_present_end_bit,
                ),
            ),
        );
    }
    if following_header.actor_object_index != actor_object_index {
        return Err(
            network_existing_actor_after_following_payload_control_following_header_error(
                "actor-mismatch",
                format!(
                    "prior actor {actor_object_index} differs from post-W header actor {}",
                    following_header.actor_object_index,
                ),
            ),
        );
    }

    let payload_start_bit = following_header.payload_start_bit.ok_or_else(|| {
        network_existing_actor_after_following_payload_control_following_header_error(
            "missing-payload-start",
            "present post-W header has no payload start",
        )
    })?;
    if following_header.stop_bit != payload_start_bit {
        return Err(
            network_existing_actor_after_following_payload_control_following_header_error(
                "payload-boundary-mismatch",
                format!(
                    "post-W header stop {} differs from payload start {payload_start_bit}",
                    following_header.stop_bit,
                ),
            ),
        );
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
        return Err(
            network_existing_actor_after_following_payload_control_following_header_error(
                "incomplete-r3-18z-header-context",
                "post-W header is missing one or more R3.18Z tuple fields",
            ),
        );
    };

    if !r3_18z_post_w_following_header_context_admitted_v1(
        stream_id_bound,
        prop_id_bits,
        property_object_index,
        attribute_tag,
        context,
    ) {
        return Err(
            network_existing_actor_after_following_payload_control_following_header_error(
                "unadmitted-r3-18z-header-context",
                format!(
                    "R3.18Z exact tuple rejected bound={stream_id_bound} bits={prop_id_bits} object={property_object_index} tag={attribute_tag:?} version={}.{} net{}",
                    context.version_major, context.version_minor, context.net_version,
                ),
            ),
        );
    }

    Ok(ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderV1 {
        control,
        following_header,
        stop_bit: payload_start_bit,
    })
}

/// Exactly one R3.18AC-admitted ordinal-3 payload after a valid published R3.18AA header.
///
/// This enum is deliberately closed to the three payload shapes proven on the immutable
/// R3.18AC lane. It is not a generic attribute-payload carrier.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub enum ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadValueV1
{
    ActiveActor(ReplayNetworkK2DecodeV1),
    Int(ReplayNetworkPrimitiveScalarDecodeV1),
    UniqueId(ReplayNetworkK2DecodeV1),
}

/// Bounded composition of a valid published R3.18AA post-W following header plus exactly one
/// R3.18AC-admitted ordinal-3 payload.
///
/// `stop_bit` is exactly the first bit after that payload. No later `property_present` control
/// bit, stream/header/payload, actor, frame, or repeatable cursor is read or exposed.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadV1 {
    pub header_composition:
        ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderV1,
    pub following_payload:
        ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadValueV1,
    pub payload_start_bit: u64,
    pub payload_width: u64,
    pub stop_bit: u64,
}

fn network_existing_actor_post_aa_following_payload_error(
    category: &str,
    detail: impl Into<String>,
) -> MimirError {
    MimirError::message(format!(
        "replay network post-AA following-payload error: {category}: {}",
        detail.into()
    ))
}

/// Compose exactly one R3.18AC-admitted ordinal-3 payload after the published R3.18AA boundary.
///
/// R3.18AA is recomputed from the supplied R3.18T prior, so the complete R3.18Z header contract
/// remains authoritative. Only the exact R3.18AC shapes are admitted: ActiveActor/33,
/// Int/32, and UniqueId system 1 / Steam / 80. The function stops at payload end and consumes
/// zero bits of another property-control boundary.
pub fn decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_v1(
    network_bytes: &[u8],
    prior: &ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadV1,
    lookup_plan: &ReplayNetworkLookupPlanV1,
    context: ReplayNetworkK3DecodeContextV1,
) -> Result<ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadV1>{
    if context.version_major != 868
        || context.version_minor != 32
        || context.net_version != 10
        || context.is_rl_223
    {
        return Err(network_existing_actor_post_aa_following_payload_error(
            "unadmitted-context",
            format!(
                "R3.18AC/AD admits only 868.32/net10/non-RL223, got {}.{}/net{}/is_rl_223={}",
                context.version_major,
                context.version_minor,
                context.net_version,
                context.is_rl_223,
            ),
        ));
    }

    let header_composition = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_v1(
        network_bytes,
        prior,
        lookup_plan,
        context,
    )?;
    let following_header = &header_composition.following_header;
    let payload_start_bit = following_header.payload_start_bit.ok_or_else(|| {
        network_existing_actor_post_aa_following_payload_error(
            "missing-payload-start",
            "valid R3.18AA result has no following-header payload_start",
        )
    })?;
    if header_composition.stop_bit != payload_start_bit
        || following_header.stop_bit != payload_start_bit
    {
        return Err(network_existing_actor_post_aa_following_payload_error(
            "header-stop-mismatch",
            format!(
                "AA stop={}, header stop={}, payload start={payload_start_bit}",
                header_composition.stop_bit, following_header.stop_bit,
            ),
        ));
    }
    let tag = following_header.resolved_attribute_tag.ok_or_else(|| {
        network_existing_actor_post_aa_following_payload_error(
            "missing-attribute-tag",
            "valid R3.18AA result has no resolved following-header tag",
        )
    })?;
    let k2_context = ReplayNetworkK2DecodeContextV1 {
        net_version: context.net_version,
        is_rl_223: context.is_rl_223,
    };

    let (following_payload, payload_width, stop_bit) = match tag {
        ReplayNetworkAttributeTagV1::ActiveActor => {
            let decoded = decode_replay_network_k2_v1(
                network_bytes,
                payload_start_bit,
                ReplayNetworkAttributeTagV1::ActiveActor,
                k2_context,
            )?;
            let expected_end = payload_start_bit.checked_add(33).ok_or_else(|| {
                network_existing_actor_post_aa_following_payload_error(
                    "invalid-active-actor-end",
                    "ActiveActor payload end overflows u64",
                )
            })?;
            if decoded.attribute_tag != ReplayNetworkAttributeTagV1::ActiveActor
                || decoded.payload_start_bit != payload_start_bit
                || decoded.payload_width != 33
                || decoded.payload_end_bit != expected_end
                || !matches!(&decoded.value, ReplayNetworkK2ValueV1::ActiveActor { .. })
            {
                return Err(network_existing_actor_post_aa_following_payload_error(
                    "active-actor-boundary-mismatch",
                    format!(
                        "tag={:?}, start={}, end={}, width={}, expected_start={payload_start_bit}, expected_end={expected_end}",
                        decoded.attribute_tag,
                        decoded.payload_start_bit,
                        decoded.payload_end_bit,
                        decoded.payload_width,
                    ),
                ));
            }
            (
                ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadValueV1::ActiveActor(decoded),
                33,
                expected_end,
            )
        }
        ReplayNetworkAttributeTagV1::Int => {
            let decoded = decode_replay_network_primitive_scalar_v1(
                network_bytes,
                payload_start_bit,
                ReplayNetworkAttributeTagV1::Int,
            )?;
            let expected_end = payload_start_bit.checked_add(32).ok_or_else(|| {
                network_existing_actor_post_aa_following_payload_error(
                    "invalid-int-end",
                    "Int payload end overflows u64",
                )
            })?;
            if decoded.attribute_tag != ReplayNetworkAttributeTagV1::Int
                || decoded.payload_start_bit != payload_start_bit
                || decoded.payload_width != 32
                || decoded.payload_end_bit != expected_end
                || decoded.stop_bit != expected_end
                || !matches!(&decoded.value, ReplayNetworkPrimitiveScalarValueV1::Int(_))
            {
                return Err(network_existing_actor_post_aa_following_payload_error(
                    "int-boundary-mismatch",
                    format!(
                        "tag={:?}, start={}, end={}, width={}, stop={}, expected_start={payload_start_bit}, expected_end={expected_end}",
                        decoded.attribute_tag,
                        decoded.payload_start_bit,
                        decoded.payload_end_bit,
                        decoded.payload_width,
                        decoded.stop_bit,
                    ),
                ));
            }
            (
                ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadValueV1::Int(decoded),
                32,
                expected_end,
            )
        }
        ReplayNetworkAttributeTagV1::UniqueId => {
            let decoded = decode_replay_network_k2_v1(
                network_bytes,
                payload_start_bit,
                ReplayNetworkAttributeTagV1::UniqueId,
                k2_context,
            )?;
            let expected_end = payload_start_bit.checked_add(80).ok_or_else(|| {
                network_existing_actor_post_aa_following_payload_error(
                    "invalid-unique-id-end",
                    "UniqueId payload end overflows u64",
                )
            })?;
            let admitted_identity = match &decoded.value {
                ReplayNetworkK2ValueV1::UniqueId(unique) => {
                    unique.system_id == 1
                        && matches!(
                            &unique.remote_id,
                            ReplayNetworkUniqueIdRemoteV1::Steam { .. }
                        )
                }
                _ => false,
            };
            if decoded.attribute_tag != ReplayNetworkAttributeTagV1::UniqueId
                || decoded.payload_start_bit != payload_start_bit
                || decoded.payload_width != 80
                || decoded.payload_end_bit != expected_end
                || !admitted_identity
            {
                return Err(network_existing_actor_post_aa_following_payload_error(
                    "unadmitted-unique-id-shape",
                    format!(
                        "tag={:?}, start={}, end={}, width={}, value={:?}; R3.18AD admits only system1/Steam/80",
                        decoded.attribute_tag,
                        decoded.payload_start_bit,
                        decoded.payload_end_bit,
                        decoded.payload_width,
                        decoded.value,
                    ),
                ));
            }
            (
                ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadValueV1::UniqueId(decoded),
                80,
                expected_end,
            )
        }
        other => {
            return Err(network_existing_actor_post_aa_following_payload_error(
                "unsupported-payload-tag",
                format!("R3.18AC/AD admits only ActiveActor/Int/UniqueId, got {other:?}"),
            ));
        }
    };

    if stop_bit < payload_start_bit {
        return Err(network_existing_actor_post_aa_following_payload_error(
            "invalid-stop",
            format!("payload start {payload_start_bit} exceeds stop {stop_bit}"),
        ));
    }

    Ok(ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlFollowingHeaderPayloadV1 {
        header_composition,
        following_payload,
        payload_start_bit,
        payload_width,
        stop_bit,
    })
}

/// R3.18V observed exactly one next `property_present` bit on the immutable 47-row lane:
/// true=47, false=0. This result is deliberately non-generic and stops exactly one bit
/// after that admitted true control. It does not resolve a stream/header/payload, read a
/// second later control bit, or expose a repeatedly-chainable property cursor.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlV1
{
    pub following_property_present: bool,
    pub property_present_start_bit: u64,
    pub property_present_end_bit: u64,
    pub stop_bit: u64,
}

fn network_existing_actor_after_following_payload_control_error(
    category: &str,
    detail: impl Into<String>,
) -> MimirError {
    MimirError::message(format!(
        "replay network after-following-payload control error: {category}: {}",
        detail.into()
    ))
}

/// Read exactly one R3.18V-admitted control bit after a valid R3.18T following payload.
///
/// Only `true` is evidence-admitted at this exact boundary. `false` fails closed. The
/// function validates the nested R3.18T payload-end relationship before touching the
/// next bit and consumes no stream id, header, payload, additional control, or loop.
pub fn decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_v1(
    network_bytes: &[u8],
    prior: &ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadV1,
) -> Result<
    ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlV1,
> {
    let header_stop = prior.header_composition.stop_bit;
    let following_header = &prior.header_composition.following_header;
    if !following_header.property_present
        || following_header.payload_start_bit != Some(header_stop)
        || following_header.stop_bit != header_stop
    {
        return Err(
            network_existing_actor_after_following_payload_control_error(
                "invalid-prior-header",
                format!(
                    "property_present={}, payload_start={:?}, header_stop={}, composed_header_stop={header_stop}",
                    following_header.property_present,
                    following_header.payload_start_bit,
                    following_header.stop_bit,
                ),
            ),
        );
    }

    let payload_end = match &prior.following_payload {
        ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadValueV1::Boolean(decoded) => {
            let expected_end = decoded
                .payload_start_bit
                .checked_add(u64::from(decoded.payload_width))
                .ok_or_else(|| {
                    network_existing_actor_after_following_payload_control_error(
                        "invalid-prior-payload",
                        "Boolean payload end overflows u64",
                    )
                })?;
            if decoded.attribute_tag != ReplayNetworkAttributeTagV1::Boolean
                || decoded.payload_start_bit != header_stop
                || decoded.payload_width != 1
                || decoded.payload_end_bit != expected_end
                || decoded.stop_bit != expected_end
            {
                return Err(network_existing_actor_after_following_payload_control_error(
                    "invalid-prior-payload",
                    format!(
                        "Boolean tag={:?}, start={}, width={}, end={}, stop={}, expected_start={header_stop}, expected_end={expected_end}",
                        decoded.attribute_tag,
                        decoded.payload_start_bit,
                        decoded.payload_width,
                        decoded.payload_end_bit,
                        decoded.stop_bit,
                    ),
                ));
            }
            expected_end
        }
        ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadValueV1::ActiveActor(decoded) => {
            let expected_end = decoded
                .payload_start_bit
                .checked_add(decoded.payload_width)
                .ok_or_else(|| {
                    network_existing_actor_after_following_payload_control_error(
                        "invalid-prior-payload",
                        "ActiveActor payload end overflows u64",
                    )
                })?;
            if decoded.attribute_tag != ReplayNetworkAttributeTagV1::ActiveActor
                || decoded.payload_start_bit != header_stop
                || decoded.payload_width != 33
                || decoded.payload_end_bit != expected_end
            {
                return Err(network_existing_actor_after_following_payload_control_error(
                    "invalid-prior-payload",
                    format!(
                        "ActiveActor tag={:?}, start={}, width={}, end={}, expected_start={header_stop}, expected_end={expected_end}",
                        decoded.attribute_tag,
                        decoded.payload_start_bit,
                        decoded.payload_width,
                        decoded.payload_end_bit,
                    ),
                ));
            }
            expected_end
        }
    };

    if prior.stop_bit != payload_end {
        return Err(
            network_existing_actor_after_following_payload_control_error(
                "invalid-prior-stop",
                format!(
                    "prior stop {} does not equal exact following-payload end {payload_end}",
                    prior.stop_bit
                ),
            ),
        );
    }

    let property_present_start_bit = prior.stop_bit;
    let start = usize::try_from(property_present_start_bit).map_err(|_| {
        network_existing_actor_after_following_payload_control_error(
            "invalid-position",
            format!("control start {property_present_start_bit} does not fit in usize"),
        )
    })?;
    let mut cursor = NetworkBitCursor {
        bytes: network_bytes,
        bit_position: start,
    };
    let following_property_present = cursor.read_bit()?;
    let property_present_end_bit = property_present_start_bit.checked_add(1).ok_or_else(|| {
        network_existing_actor_after_following_payload_control_error(
            "invalid-position",
            "control end overflows u64",
        )
    })?;
    let expected_end = start.checked_add(1).ok_or_else(|| {
        network_existing_actor_after_following_payload_control_error(
            "invalid-position",
            "control cursor end overflows usize",
        )
    })?;
    if cursor.position_bits() != expected_end {
        return Err(
            network_existing_actor_after_following_payload_control_error(
                "invalid-stop",
                format!(
                    "cursor stopped at {}, expected {expected_end}",
                    cursor.position_bits()
                ),
            ),
        );
    }
    if !following_property_present {
        return Err(
            network_existing_actor_after_following_payload_control_error(
                "unadmitted-false-control",
                format!(
                    "R3.18V observed true=47 false=0 at exact control start {property_present_start_bit}"
                ),
            ),
        );
    }

    Ok(
        ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadControlV1 {
            following_property_present: true,
            property_present_start_bit,
            property_present_end_bit,
            stop_bit: property_present_end_bit,
        },
    )
}
