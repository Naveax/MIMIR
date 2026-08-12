use serde::de::Error as DeError;
use serde::ser::Error as SerError;
use serde::{Deserialize, Deserializer, Serialize, Serializer};
use std::collections::BTreeMap;
use std::fmt::{Display, Formatter};

macro_rules! string_id {
    ($name:ident) => {
        #[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq, PartialOrd, Ord, Hash)]
        #[serde(transparent)]
        pub struct $name(String);

        impl $name {
            pub fn new(value: impl Into<String>) -> Self {
                Self(value.into())
            }

            pub fn as_str(&self) -> &str {
                &self.0
            }
        }

        impl AsRef<str> for $name {
            fn as_ref(&self) -> &str {
                self.as_str()
            }
        }

        impl Display for $name {
            fn fmt(&self, f: &mut Formatter<'_>) -> std::fmt::Result {
                f.write_str(self.as_str())
            }
        }

        impl From<String> for $name {
            fn from(value: String) -> Self {
                Self::new(value)
            }
        }

        impl From<&str> for $name {
            fn from(value: &str) -> Self {
                Self::new(value)
            }
        }
    };
}

string_id!(ReplayId);
string_id!(ReplaySliceId);
string_id!(AnchorId);
string_id!(BranchId);
string_id!(SkillId);
string_id!(TeacherLabelId);
string_id!(CacheKey);
string_id!(ReplaySubjectRef);
string_id!(RawStateWindowRef);
string_id!(LowBoostRecoveryVariantId);
string_id!(LowBoostRecoveryBcArtifactId);

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum ArtifactKind {
    Anchor,
    Branch,
    Skill,
    TeacherLabel,
    Scoreboard,
    VerticalSliceInput,
    LowBoostRecoveryBcArtifact,
}

impl ArtifactKind {
    pub const fn schema(self) -> ArtifactSchema {
        match self {
            Self::Anchor => ArtifactSchema::new(self, "mimir.anchor_artifact", 1),
            Self::Branch => ArtifactSchema::new(self, "mimir.branch_artifact", 1),
            Self::Skill => ArtifactSchema::new(self, "mimir.skill_artifact", 1),
            Self::TeacherLabel => ArtifactSchema::new(self, "mimir.teacher_label_artifact", 1),
            Self::Scoreboard => ArtifactSchema::new(self, "mimir.scoreboard_artifact", 1),
            Self::VerticalSliceInput => {
                ArtifactSchema::new(self, "mimir.vertical_slice_input_artifact", 1)
            }
            Self::LowBoostRecoveryBcArtifact => {
                ArtifactSchema::new(self, "mimir.low_boost_recovery_bc_artifact", 1)
            }
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct ArtifactSchema {
    pub kind: ArtifactKind,
    pub name: &'static str,
    pub version: u32,
}

impl ArtifactSchema {
    pub const fn new(kind: ArtifactKind, name: &'static str, version: u32) -> Self {
        Self {
            kind,
            name,
            version,
        }
    }
}

pub const ANCHOR_ARTIFACT_SCHEMA: ArtifactSchema = ArtifactKind::Anchor.schema();
pub const ANCHOR_ARTIFACT_SCHEMA_NAME: &str = ANCHOR_ARTIFACT_SCHEMA.name;
pub const ANCHOR_ARTIFACT_SCHEMA_VERSION: u32 = ANCHOR_ARTIFACT_SCHEMA.version;

pub const BRANCH_ARTIFACT_SCHEMA: ArtifactSchema = ArtifactKind::Branch.schema();
pub const BRANCH_ARTIFACT_SCHEMA_NAME: &str = BRANCH_ARTIFACT_SCHEMA.name;
pub const BRANCH_ARTIFACT_SCHEMA_VERSION: u32 = BRANCH_ARTIFACT_SCHEMA.version;

pub const SKILL_ARTIFACT_SCHEMA: ArtifactSchema = ArtifactKind::Skill.schema();
pub const SKILL_ARTIFACT_SCHEMA_NAME: &str = SKILL_ARTIFACT_SCHEMA.name;
pub const SKILL_ARTIFACT_SCHEMA_VERSION: u32 = SKILL_ARTIFACT_SCHEMA.version;

pub const TEACHER_LABEL_ARTIFACT_SCHEMA: ArtifactSchema = ArtifactKind::TeacherLabel.schema();
pub const TEACHER_LABEL_ARTIFACT_SCHEMA_NAME: &str = TEACHER_LABEL_ARTIFACT_SCHEMA.name;
pub const TEACHER_LABEL_ARTIFACT_SCHEMA_VERSION: u32 = TEACHER_LABEL_ARTIFACT_SCHEMA.version;

pub const SCOREBOARD_ARTIFACT_SCHEMA: ArtifactSchema = ArtifactKind::Scoreboard.schema();
pub const SCOREBOARD_ARTIFACT_SCHEMA_NAME: &str = SCOREBOARD_ARTIFACT_SCHEMA.name;
pub const SCOREBOARD_ARTIFACT_SCHEMA_VERSION: u32 = SCOREBOARD_ARTIFACT_SCHEMA.version;

pub const VERTICAL_SLICE_INPUT_ARTIFACT_SCHEMA: ArtifactSchema =
    ArtifactKind::VerticalSliceInput.schema();
pub const VERTICAL_SLICE_INPUT_ARTIFACT_SCHEMA_NAME: &str =
    VERTICAL_SLICE_INPUT_ARTIFACT_SCHEMA.name;
pub const VERTICAL_SLICE_INPUT_ARTIFACT_SCHEMA_VERSION: u32 =
    VERTICAL_SLICE_INPUT_ARTIFACT_SCHEMA.version;

pub const LOW_BOOST_RECOVERY_BC_ARTIFACT_SCHEMA: ArtifactSchema =
    ArtifactKind::LowBoostRecoveryBcArtifact.schema();
pub const LOW_BOOST_RECOVERY_BC_ARTIFACT_SCHEMA_NAME: &str =
    LOW_BOOST_RECOVERY_BC_ARTIFACT_SCHEMA.name;
pub const LOW_BOOST_RECOVERY_BC_ARTIFACT_SCHEMA_VERSION: u32 =
    LOW_BOOST_RECOVERY_BC_ARTIFACT_SCHEMA.version;

#[derive(Debug, Clone, Copy, Serialize, Deserialize, PartialEq, Eq, PartialOrd, Ord, Hash)]
#[serde(transparent)]
pub struct FrameIndex(u32);

impl FrameIndex {
    pub const fn new(value: u32) -> Self {
        Self(value)
    }

    pub const fn get(self) -> u32 {
        self.0
    }
}

impl From<u32> for FrameIndex {
    fn from(value: u32) -> Self {
        Self::new(value)
    }
}

impl From<FrameIndex> for u32 {
    fn from(value: FrameIndex) -> Self {
        value.get()
    }
}

#[derive(Debug, Clone, Default, Serialize, Deserialize, PartialEq)]
#[serde(transparent)]
pub struct Metadata(BTreeMap<String, FieldValue>);

impl Metadata {
    pub fn new() -> Self {
        Self::default()
    }

    pub fn insert(&mut self, key: impl Into<String>, value: FieldValue) -> Option<FieldValue> {
        self.0.insert(key.into(), value)
    }

    pub fn get(&self, key: &str) -> Option<&FieldValue> {
        self.0.get(key)
    }

    pub fn is_empty(&self) -> bool {
        self.0.is_empty()
    }

    pub fn len(&self) -> usize {
        self.0.len()
    }

    pub fn iter(&self) -> impl Iterator<Item = (&String, &FieldValue)> {
        self.0.iter()
    }

    pub fn into_inner(self) -> BTreeMap<String, FieldValue> {
        self.0
    }
}

impl AsRef<BTreeMap<String, FieldValue>> for Metadata {
    fn as_ref(&self) -> &BTreeMap<String, FieldValue> {
        &self.0
    }
}

impl From<BTreeMap<String, FieldValue>> for Metadata {
    fn from(value: BTreeMap<String, FieldValue>) -> Self {
        Self(value)
    }
}

impl From<Metadata> for BTreeMap<String, FieldValue> {
    fn from(value: Metadata) -> Self {
        value.into_inner()
    }
}

impl<K, const N: usize> From<[(K, FieldValue); N]> for Metadata
where
    K: Into<String>,
{
    fn from(value: [(K, FieldValue); N]) -> Self {
        value.into_iter().collect()
    }
}

impl<K> FromIterator<(K, FieldValue)> for Metadata
where
    K: Into<String>,
{
    fn from_iter<T: IntoIterator<Item = (K, FieldValue)>>(iter: T) -> Self {
        let mut metadata = Self::new();
        metadata.extend(iter);
        metadata
    }
}

impl<K> Extend<(K, FieldValue)> for Metadata
where
    K: Into<String>,
{
    fn extend<T: IntoIterator<Item = (K, FieldValue)>>(&mut self, iter: T) {
        self.0
            .extend(iter.into_iter().map(|(key, value)| (key.into(), value)));
    }
}

impl IntoIterator for Metadata {
    type Item = (String, FieldValue);
    type IntoIter = std::collections::btree_map::IntoIter<String, FieldValue>;

    fn into_iter(self) -> Self::IntoIter {
        self.0.into_iter()
    }
}

impl<'a> IntoIterator for &'a Metadata {
    type Item = (&'a String, &'a FieldValue);
    type IntoIter = std::collections::btree_map::Iter<'a, String, FieldValue>;

    fn into_iter(self) -> Self::IntoIter {
        self.0.iter()
    }
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
#[serde(deny_unknown_fields)]
pub struct ArtifactHeader {
    pub schema_name: String,
    pub schema_version: u32,
    pub producer: String,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub created_by_component: Option<String>,
    #[serde(default, skip_serializing_if = "Metadata::is_empty")]
    pub metadata: Metadata,
}

impl ArtifactHeader {
    pub fn new(
        schema_name: impl Into<String>,
        schema_version: u32,
        producer: impl Into<String>,
    ) -> Self {
        Self {
            schema_name: schema_name.into(),
            schema_version,
            producer: producer.into(),
            created_by_component: None,
            metadata: Metadata::new(),
        }
    }

    pub fn for_schema(schema: ArtifactSchema, producer: impl Into<String>) -> Self {
        Self::new(schema.name, schema.version, producer)
    }

    pub fn for_kind(kind: ArtifactKind, producer: impl Into<String>) -> Self {
        Self::for_schema(kind.schema(), producer)
    }

    pub fn with_created_by_component(mut self, created_by_component: impl Into<String>) -> Self {
        self.created_by_component = Some(created_by_component.into());
        self
    }

    pub fn with_metadata(mut self, metadata: Metadata) -> Self {
        self.metadata = metadata;
        self
    }
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
#[serde(deny_unknown_fields)]
pub struct ArtifactEnvelope<T> {
    pub header: ArtifactHeader,
    pub payload: T,
}

impl<T> ArtifactEnvelope<T> {
    pub fn new(header: ArtifactHeader, payload: T) -> Self {
        Self { header, payload }
    }

    pub fn into_parts(self) -> (ArtifactHeader, T) {
        (self.header, self.payload)
    }
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
#[serde(tag = "type", content = "value")]
pub enum FieldValue {
    #[serde(rename = "text")]
    Text(String),
    #[serde(rename = "integer")]
    Integer(i64),
    #[serde(rename = "float")]
    Float(
        #[serde(
            serialize_with = "serialize_finite_f64",
            deserialize_with = "deserialize_finite_f64"
        )]
        f64,
    ),
    #[serde(rename = "boolean")]
    Boolean(bool),
    #[serde(rename = "string_list")]
    StringList(Vec<String>),
}

fn serialize_finite_f64<S>(value: &f64, serializer: S) -> Result<S::Ok, S::Error>
where
    S: Serializer,
{
    if value.is_finite() {
        serializer.serialize_f64(*value)
    } else {
        Err(S::Error::custom(
            "floating-point field values must be finite",
        ))
    }
}

fn deserialize_finite_f64<'de, D>(deserializer: D) -> Result<f64, D::Error>
where
    D: Deserializer<'de>,
{
    let value = f64::deserialize(deserializer)?;

    if value.is_finite() {
        Ok(value)
    } else {
        Err(D::Error::custom(
            "floating-point field values must be finite",
        ))
    }
}

fn serialize_optional_finite_f32<S>(value: &Option<f32>, serializer: S) -> Result<S::Ok, S::Error>
where
    S: Serializer,
{
    match value {
        Some(value) if value.is_finite() => serializer.serialize_some(value),
        Some(_) => Err(S::Error::custom("teacher label scores must be finite")),
        None => serializer.serialize_none(),
    }
}

fn deserialize_optional_finite_f32<'de, D>(deserializer: D) -> Result<Option<f32>, D::Error>
where
    D: Deserializer<'de>,
{
    let value = Option::<f32>::deserialize(deserializer)?;

    match value {
        Some(value) if value.is_finite() => Ok(Some(value)),
        Some(_) => Err(D::Error::custom("teacher label scores must be finite")),
        None => Ok(None),
    }
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct TimeWindow {
    pub start: FrameIndex,
    pub end_exclusive: FrameIndex,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq, Hash)]
#[serde(rename_all = "snake_case")]
pub enum ReplaySliceFamilyHint {
    LowBoostRecovery,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct ReplaySourceRef {
    pub replay_id: ReplayId,
    pub provenance_label: String,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct ReplaySliceRef {
    pub slice_id: ReplaySliceId,
    pub source_replay: ReplaySourceRef,
    pub frame_window: TimeWindow,
    pub subject: ReplaySubjectRef,
    pub family_hint: ReplaySliceFamilyHint,
    pub raw_state_window_ref: RawStateWindowRef,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub audit_note: Option<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq, Hash)]
#[serde(rename_all = "snake_case")]
pub enum LowBoostRecoveryCanonicalOrientationNoteV1 {
    SubjectAnchoredWindowOnly,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq, Hash)]
#[serde(rename_all = "snake_case")]
pub enum LowBoostRecoveryEnvelopeSemanticsV1 {
    RawStateWindowReferenceOnly,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq, Hash)]
#[serde(rename_all = "snake_case")]
pub enum LowBoostRecoveryCanonicalNoteV1 {
    BoostAmountUnresolved,
    ContactTruthUnresolved,
    RecoverySuccessUnresolved,
    ReplayOrientationNormalizationDeferred,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct LowBoostRecoverySubjectStateEnvelopeV1 {
    pub subject: ReplaySubjectRef,
    pub frame_window: TimeWindow,
    pub semantics: LowBoostRecoveryEnvelopeSemanticsV1,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct LowBoostRecoveryEnvironmentStateEnvelopeV1 {
    pub frame_window: TimeWindow,
    pub semantics: LowBoostRecoveryEnvelopeSemanticsV1,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct LowBoostRecoveryCanonicalStateV1 {
    pub slice_id: ReplaySliceId,
    pub source_replay: ReplaySourceRef,
    pub subject: ReplaySubjectRef,
    pub frame_window: TimeWindow,
    pub raw_state_window_ref: RawStateWindowRef,
    pub orientation_note: LowBoostRecoveryCanonicalOrientationNoteV1,
    pub subject_state_envelope: LowBoostRecoverySubjectStateEnvelopeV1,
    pub environment_state_envelope: LowBoostRecoveryEnvironmentStateEnvelopeV1,
    pub canonicalization_notes: Vec<LowBoostRecoveryCanonicalNoteV1>,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq, Hash)]
#[serde(rename_all = "snake_case")]
pub enum LowBoostRecoveryEventNodeKindV1 {
    SliceWindowStart,
    SliceWindowEndExclusive,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct LowBoostRecoveryEventNodeV1 {
    pub node_id: u8,
    pub frame_index: FrameIndex,
    pub kind: LowBoostRecoveryEventNodeKindV1,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq, Hash)]
#[serde(rename_all = "snake_case")]
pub enum LowBoostRecoveryEventEdgeKindV1 {
    ObservedSliceWindow,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct LowBoostRecoveryEventEdgeV1 {
    pub from_node_id: u8,
    pub to_node_id: u8,
    pub kind: LowBoostRecoveryEventEdgeKindV1,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq, Hash)]
#[serde(rename_all = "snake_case")]
pub enum LowBoostRecoveryContactSemanticsV1 {
    UnresolvedFromReplaySliceContract,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct LowBoostRecoveryEventContactGraphV1 {
    pub slice_id: ReplaySliceId,
    pub frame_window: TimeWindow,
    pub nodes: Vec<LowBoostRecoveryEventNodeV1>,
    pub edges: Vec<LowBoostRecoveryEventEdgeV1>,
    pub contact_semantics: LowBoostRecoveryContactSemanticsV1,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq, Hash)]
#[serde(rename_all = "snake_case")]
pub enum LowBoostRecoveryPhaseLabelV1 {
    CandidateRecoveryWindow,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct LowBoostRecoveryPhaseV1 {
    pub phase_id: u8,
    pub label: LowBoostRecoveryPhaseLabelV1,
    pub start: FrameIndex,
    pub end_exclusive: FrameIndex,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct LowBoostRecoveryPhasePlanV1 {
    pub slice_id: ReplaySliceId,
    pub phases: Vec<LowBoostRecoveryPhaseV1>,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct LowBoostRecoveryPhaseWindowLinkV1 {
    pub phase_id: u8,
    pub phase_label: LowBoostRecoveryPhaseLabelV1,
    pub window: TimeWindow,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct LowBoostRecoveryFrameRangeV1 {
    pub min_inclusive: u32,
    pub max_inclusive: u32,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq, Hash)]
#[serde(rename_all = "snake_case")]
pub enum LowBoostRecoveryWindowInterpretationV1 {
    CandidateRecoveryWindowOnly,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq, Hash)]
#[serde(rename_all = "snake_case")]
pub enum LowBoostRecoveryParameterNoteV1 {
    ObservedWindowDerivedFromCanonicalPhase,
    BoundaryVariationLimitedToSingleFrameTrims,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq, Hash)]
#[serde(rename_all = "snake_case")]
pub enum LowBoostRecoveryUnresolvedAssumptionV1 {
    LowBoostThresholdUnproven,
    ContactTruthUnproven,
    RecoverySuccessUnproven,
    ReplayOrientationNormalizationDeferred,
    PhysicsReachabilityUnproven,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct LowBoostRecoveryParameterBundleV1 {
    pub slice_id: ReplaySliceId,
    pub family: ReplaySliceFamilyHint,
    pub source_replay: ReplaySourceRef,
    pub subject: ReplaySubjectRef,
    pub raw_state_window_ref: RawStateWindowRef,
    pub phase_window_link: LowBoostRecoveryPhaseWindowLinkV1,
    pub recovery_window_interpretation: LowBoostRecoveryWindowInterpretationV1,
    pub observed_window_duration_frames: LowBoostRecoveryFrameRangeV1,
    pub boundary_trim_budget_frames: LowBoostRecoveryFrameRangeV1,
    pub parameter_notes: Vec<LowBoostRecoveryParameterNoteV1>,
    pub unresolved_assumptions: Vec<LowBoostRecoveryUnresolvedAssumptionV1>,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct LowBoostRecoveryWindowOverrideV1 {
    pub trim_start_frames: u32,
    pub trim_end_frames: u32,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq, Hash)]
#[serde(rename_all = "snake_case")]
pub enum LowBoostRecoveryDifficultyHintV1 {
    ReferenceSeedWindow,
    StricterStartBoundary,
    StricterEndBoundary,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq, Hash)]
#[serde(rename_all = "snake_case")]
pub enum LowBoostRecoveryGenerationReasonV1 {
    PreserveObservedWindow,
    ProbeStartBoundaryAmbiguity,
    ProbeEndBoundaryAmbiguity,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct LowBoostRecoveryGeneratedVariantV1 {
    pub variant_id: LowBoostRecoveryVariantId,
    pub source_slice_id: ReplaySliceId,
    pub source_phase_id: u8,
    pub family: ReplaySliceFamilyHint,
    pub variant_window: TimeWindow,
    pub window_override: LowBoostRecoveryWindowOverrideV1,
    pub difficulty_hint: LowBoostRecoveryDifficultyHintV1,
    pub generation_reason: LowBoostRecoveryGenerationReasonV1,
    pub unresolved_assumptions: Vec<LowBoostRecoveryUnresolvedAssumptionV1>,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq, Hash)]
#[serde(rename_all = "snake_case")]
pub enum LowBoostRecoveryValidationDecisionV1 {
    Malformed,
    Reject,
    Abstain,
    AcceptCandidate,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq, Hash)]
#[serde(rename_all = "snake_case")]
pub enum LowBoostRecoveryConfidenceBandV1 {
    InsufficientEvidence,
    BoundarySensitive,
    BoundaryStable,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq, Hash)]
#[serde(rename_all = "snake_case")]
pub enum LowBoostRecoveryValidationReasonV1 {
    MalformedParameterBundle,
    MalformedVariantSet,
    ExactWindowBelowMinimumEvidenceFloor,
    BoundarySensitivityTooHigh,
    ProvisionalCandidateAccepted,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq, Hash)]
#[serde(rename_all = "snake_case")]
pub enum LowBoostRecoveryValidationNoteV1 {
    ReferenceVariantPresent,
    StartTrimVariantPresent,
    EndTrimVariantPresent,
    KnownUnresolvedAssumptionsCarriedForward,
    ExactWindowMeetsMinimumEvidenceFloor,
    ExactWindowFailsMinimumEvidenceFloor,
    TrimmedVariantsMeetStabilityFloor,
    TrimmedVariantsTooShortForStability,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct LowBoostRecoveryValidationResultV1 {
    pub source_slice_id: ReplaySliceId,
    pub source_phase_id: u8,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub reference_variant_id: Option<LowBoostRecoveryVariantId>,
    pub evaluated_variant_ids: Vec<LowBoostRecoveryVariantId>,
    pub decision: LowBoostRecoveryValidationDecisionV1,
    pub reason: LowBoostRecoveryValidationReasonV1,
    pub confidence_band: LowBoostRecoveryConfidenceBandV1,
    pub carried_unresolved_assumptions: Vec<LowBoostRecoveryUnresolvedAssumptionV1>,
    pub validator_notes: Vec<LowBoostRecoveryValidationNoteV1>,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq, Hash)]
#[serde(rename_all = "snake_case")]
pub enum LowBoostRecoveryCurriculumExportShellNoteV1 {
    AcceptedCandidateOnly,
    ProvisionalAcceptanceOnly,
    UnresolvedAssumptionsCarriedForward,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq, Hash)]
#[serde(rename_all = "snake_case")]
pub enum LowBoostRecoveryCurriculumExportConsumerHintV1 {
    EvalHarnessOnly,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct LowBoostRecoveryCurriculumExportShellV1 {
    pub family: ReplaySliceFamilyHint,
    pub source_slice_id: ReplaySliceId,
    pub source_replay: ReplaySourceRef,
    pub source_subject: ReplaySubjectRef,
    pub source_raw_state_window_ref: RawStateWindowRef,
    pub source_phase_id: u8,
    pub source_phase_window: TimeWindow,
    pub accepted_reference_variant_id: LowBoostRecoveryVariantId,
    pub accepted_reference_variant_window: TimeWindow,
    pub evaluated_variant_ids: Vec<LowBoostRecoveryVariantId>,
    pub accepted_decision: LowBoostRecoveryValidationDecisionV1,
    pub decision_reason: LowBoostRecoveryValidationReasonV1,
    pub confidence_band: LowBoostRecoveryConfidenceBandV1,
    pub carried_unresolved_assumptions: Vec<LowBoostRecoveryUnresolvedAssumptionV1>,
    pub shell_notes: Vec<LowBoostRecoveryCurriculumExportShellNoteV1>,
    pub consumer_hint: LowBoostRecoveryCurriculumExportConsumerHintV1,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq, Hash)]
#[serde(rename_all = "snake_case")]
pub enum LowBoostRecoveryEvalStatusV1 {
    UnusableInput,
    ShellPresent,
    ShellAuditable,
    ShellReadyForFutureConsumer,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq, Hash)]
#[serde(rename_all = "snake_case")]
pub enum LowBoostRecoveryEvalNoteV1 {
    SourceLineagePresent,
    AcceptedReferenceVariantLineagePresent,
    AcceptedShellContractSatisfied,
    BoundedEvidenceConsistent,
    UnresolvedAssumptionsVisible,
    ReferenceWindowAvailable,
    InputStructuralDriftDetected,
    FutureConsumerReadinessLimited,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct LowBoostRecoveryEvalMetricSummaryV1 {
    pub lineage_completeness: bool,
    pub accepted_shell_completeness: bool,
    pub bounded_evidence_consistency: bool,
    pub unresolved_burden_visibility: bool,
    pub reference_window_availability: bool,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct LowBoostRecoveryEvalResultV1 {
    pub source_slice_id: ReplaySliceId,
    pub source_phase_id: u8,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub accepted_reference_variant_id: Option<LowBoostRecoveryVariantId>,
    pub eval_status: LowBoostRecoveryEvalStatusV1,
    pub eval_notes: Vec<LowBoostRecoveryEvalNoteV1>,
    pub metric_summary: LowBoostRecoveryEvalMetricSummaryV1,
    pub carried_confidence_band: LowBoostRecoveryConfidenceBandV1,
    pub carried_unresolved_assumptions: Vec<LowBoostRecoveryUnresolvedAssumptionV1>,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq, Hash)]
#[serde(rename_all = "snake_case")]
pub enum LowBoostRecoveryConsumerPlanningDispositionV1 {
    NotBcCandidate,
    BcCandidateDeferred,
    BcCandidateReadyForContractDefinition,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq, Hash)]
#[serde(rename_all = "snake_case")]
pub enum LowBoostRecoveryConsumerPlanningNoteV1 {
    BcMilestoneApproaching,
    ShellEvalBoundaryAligned,
    AcceptedReferenceVariantLineagePreserved,
    UnresolvedAssumptionsCarriedForward,
    PlanningInputNotUsable,
    EvalReadinessLimited,
    ReadyForBcContractDefinitionOnly,
    PlanningOnlyNotBcUsefulnessProof,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct LowBoostRecoveryConsumerPlanningResultV1 {
    pub source_slice_id: ReplaySliceId,
    pub source_replay: ReplaySourceRef,
    pub source_subject: ReplaySubjectRef,
    pub source_raw_state_window_ref: RawStateWindowRef,
    pub source_phase_id: u8,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub accepted_reference_variant_id: Option<LowBoostRecoveryVariantId>,
    pub eval_readiness_status: LowBoostRecoveryEvalStatusV1,
    pub carried_confidence_band: LowBoostRecoveryConfidenceBandV1,
    pub carried_unresolved_assumptions: Vec<LowBoostRecoveryUnresolvedAssumptionV1>,
    pub disposition: LowBoostRecoveryConsumerPlanningDispositionV1,
    pub planning_notes: Vec<LowBoostRecoveryConsumerPlanningNoteV1>,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq, Hash)]
#[serde(rename_all = "snake_case")]
pub enum LowBoostRecoveryBcSupervisionWindowRoleV1 {
    AcceptedReferenceVariantWindow,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq, Hash)]
#[serde(rename_all = "snake_case")]
pub enum LowBoostRecoveryBcObservationBindingKindV1 {
    AcceptedReferenceWindowFromRawStateWindowRef,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq, Hash)]
#[serde(rename_all = "snake_case")]
pub enum LowBoostRecoveryBcTargetBindingKindV1 {
    AcceptedReferenceVariantControlTargetDeferred,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq, Hash)]
#[serde(rename_all = "snake_case")]
pub enum LowBoostRecoveryBcContractNoteV1 {
    ContractDefinitionOnly,
    AcceptedShellPlanningBoundaryAligned,
    ObservationBindingDeferredToLaterSerialization,
    TargetBindingDeferredToLaterSerialization,
    ProvisionalConfidenceCarriedForward,
    UnresolvedAssumptionsCarriedForward,
    NotBcUsefulnessProof,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct LowBoostRecoveryBcRowV1 {
    pub family: ReplaySliceFamilyHint,
    pub source_slice_id: ReplaySliceId,
    pub source_replay: ReplaySourceRef,
    pub source_subject: ReplaySubjectRef,
    pub source_raw_state_window_ref: RawStateWindowRef,
    pub source_phase_id: u8,
    pub accepted_reference_variant_id: LowBoostRecoveryVariantId,
    pub supervision_window_role: LowBoostRecoveryBcSupervisionWindowRoleV1,
    pub observation_binding_kind: LowBoostRecoveryBcObservationBindingKindV1,
    pub target_binding_kind: LowBoostRecoveryBcTargetBindingKindV1,
    pub carried_confidence_band: LowBoostRecoveryConfidenceBandV1,
    pub carried_unresolved_assumptions: Vec<LowBoostRecoveryUnresolvedAssumptionV1>,
    pub bc_contract_notes: Vec<LowBoostRecoveryBcContractNoteV1>,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct LowBoostRecoveryBcObservationV1 {
    pub binding_kind: LowBoostRecoveryBcObservationBindingKindV1,
    pub supervision_window_role: LowBoostRecoveryBcSupervisionWindowRoleV1,
    pub accepted_reference_window: TimeWindow,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct LowBoostRecoveryBcTargetV1 {
    pub binding_kind: LowBoostRecoveryBcTargetBindingKindV1,
    pub accepted_reference_variant_id: LowBoostRecoveryVariantId,
    pub accepted_reference_window: TimeWindow,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq, Hash)]
#[serde(rename_all = "snake_case")]
pub enum LowBoostRecoveryBcArtifactNoteV1 {
    SerializedFromBcContractRow,
    AcceptedShellReferenceWindowMaterialized,
    ObservationPayloadReferenceBound,
    TargetPayloadControlDeferred,
    ProvisionalConfidenceCarriedForward,
    UnresolvedAssumptionsCarriedForward,
    NotBcUsefulnessProof,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct LowBoostRecoveryBcSerializedArtifactV1 {
    pub artifact_id: LowBoostRecoveryBcArtifactId,
    pub family: ReplaySliceFamilyHint,
    pub source_slice_id: ReplaySliceId,
    pub source_replay: ReplaySourceRef,
    pub source_subject: ReplaySubjectRef,
    pub source_raw_state_window_ref: RawStateWindowRef,
    pub source_phase_id: u8,
    pub accepted_reference_variant_id: LowBoostRecoveryVariantId,
    pub observation: LowBoostRecoveryBcObservationV1,
    pub target: LowBoostRecoveryBcTargetV1,
    pub carried_confidence_band: LowBoostRecoveryConfidenceBandV1,
    pub carried_unresolved_assumptions: Vec<LowBoostRecoveryUnresolvedAssumptionV1>,
    pub artifact_notes: Vec<LowBoostRecoveryBcArtifactNoteV1>,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct LowBoostRecoveryBcActualFilesystemEmissionSpecimenFileV1 {
    pub lane_ordinal: usize,
    pub specimen_ordinal: usize,
    pub artifact_id: LowBoostRecoveryBcArtifactId,
    pub source_slice_id: ReplaySliceId,
    pub source_replay: ReplaySourceRef,
    pub source_subject: ReplaySubjectRef,
    pub source_raw_state_window_ref: RawStateWindowRef,
    pub source_phase_id: u8,
    pub accepted_reference_variant_id: LowBoostRecoveryVariantId,
    pub observation_binding_kind: LowBoostRecoveryBcObservationBindingKindV1,
    pub supervision_window_role: LowBoostRecoveryBcSupervisionWindowRoleV1,
    pub accepted_reference_window: TimeWindow,
    pub target_binding_kind: LowBoostRecoveryBcTargetBindingKindV1,
    pub carried_confidence_band: LowBoostRecoveryConfidenceBandV1,
    pub carried_unresolved_assumptions: Vec<LowBoostRecoveryUnresolvedAssumptionV1>,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
#[serde(deny_unknown_fields)]
pub struct StateSnapshot {
    pub replay_id: ReplayId,
    pub frame_index: FrameIndex,
    #[serde(default, skip_serializing_if = "Metadata::is_empty")]
    pub fields: Metadata,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
#[serde(deny_unknown_fields)]
pub struct ActionRecord {
    pub action_key: String,
    #[serde(default, skip_serializing_if = "Metadata::is_empty")]
    pub fields: Metadata,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq, Hash)]
#[serde(rename_all = "snake_case")]
pub enum AnchorKind {
    Manual,
    ExternalMarker,
    Unknown,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
#[serde(deny_unknown_fields)]
pub struct AnchorRecord {
    pub id: AnchorId,
    pub replay_id: ReplayId,
    pub frame_index: FrameIndex,
    pub kind: AnchorKind,
    #[serde(default, skip_serializing_if = "Metadata::is_empty")]
    pub metadata: Metadata,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq, Hash)]
#[serde(rename_all = "snake_case")]
pub enum BranchOrigin {
    Manual,
    Counterfactual,
    Imported,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
#[serde(deny_unknown_fields)]
pub struct BranchRecord {
    pub id: BranchId,
    pub anchor_id: AnchorId,
    pub origin: BranchOrigin,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub label: Option<String>,
    #[serde(default, skip_serializing_if = "Vec::is_empty")]
    pub actions: Vec<ActionRecord>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub legality_hint: Option<bool>,
    #[serde(default, skip_serializing_if = "Metadata::is_empty")]
    pub metadata: Metadata,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
#[serde(deny_unknown_fields)]
pub struct SkillRecord {
    pub id: SkillId,
    pub family: String,
    pub canonical_name: String,
    #[serde(default, skip_serializing_if = "Vec::is_empty")]
    pub aliases: Vec<String>,
    #[serde(default, skip_serializing_if = "Metadata::is_empty")]
    pub metadata: Metadata,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(rename_all = "snake_case", tag = "target_type", content = "id")]
pub enum TeacherLabelTarget {
    Replay(ReplayId),
    Anchor(AnchorId),
    Branch(BranchId),
    Skill(SkillId),
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
#[serde(deny_unknown_fields)]
pub struct TeacherLabelRecord {
    pub id: TeacherLabelId,
    pub target: TeacherLabelTarget,
    pub label: String,
    #[serde(
        default,
        skip_serializing_if = "Option::is_none",
        serialize_with = "serialize_optional_finite_f32",
        deserialize_with = "deserialize_optional_finite_f32"
    )]
    pub score: Option<f32>,
    #[serde(default, skip_serializing_if = "Metadata::is_empty")]
    pub metadata: Metadata,
}

/// Persisted anchor payload intentionally reuses `AnchorRecord`.
///
/// The shared DTO is already the full persisted contract for a single anchor artifact, so a
/// separate persisted-only struct would duplicate the shape without narrowing it.
pub type AnchorArtifactPayload = AnchorRecord;

/// Persisted branch payload intentionally reuses `BranchRecord`.
///
/// The shared DTO is already the full persisted contract for a single branch artifact, including
/// its optional action list and metadata, so a second struct would not add persistence clarity.
pub type BranchArtifactPayload = BranchRecord;

/// Persisted skill payload intentionally reuses `SkillRecord`.
///
/// The shared DTO is already the full persisted contract for a single skill artifact.
pub type SkillArtifactPayload = SkillRecord;

/// Persisted teacher-label payload intentionally reuses `TeacherLabelRecord`.
///
/// The shared DTO is already the full persisted contract for a single teacher-label artifact.
pub type TeacherLabelArtifactPayload = TeacherLabelRecord;

pub type PersistedAnchorArtifact = ArtifactEnvelope<AnchorArtifactPayload>;
pub type PersistedBranchArtifact = ArtifactEnvelope<BranchArtifactPayload>;
pub type PersistedSkillArtifact = ArtifactEnvelope<SkillArtifactPayload>;
pub type PersistedTeacherLabelArtifact = ArtifactEnvelope<TeacherLabelArtifactPayload>;

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
#[serde(deny_unknown_fields)]
pub struct PersistedVerticalSliceAnchorHint {
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub anchor_id: Option<AnchorId>,
    pub frame_index: FrameIndex,
    pub kind: AnchorKind,
    #[serde(default, skip_serializing_if = "Metadata::is_empty")]
    pub metadata: Metadata,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
#[serde(deny_unknown_fields)]
pub struct PersistedVerticalSliceProposal {
    pub label: String,
    #[serde(default, skip_serializing_if = "Vec::is_empty")]
    pub actions: Vec<ActionRecord>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub legal_hint: Option<bool>,
    #[serde(default, skip_serializing_if = "Metadata::is_empty")]
    pub metadata: Metadata,
    #[serde(default, skip_serializing_if = "BTreeMap::is_empty")]
    pub score_signals: BTreeMap<String, f64>,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
#[serde(deny_unknown_fields)]
pub struct PersistedVerticalSliceInput {
    pub replay_id: ReplayId,
    pub export_name: String,
    pub teacher_namespace: String,
    pub simulation_seed: u64,
    pub anchor_hint: PersistedVerticalSliceAnchorHint,
    pub proposals: Vec<PersistedVerticalSliceProposal>,
    #[serde(default, skip_serializing_if = "BTreeMap::is_empty")]
    pub scorer_weights: BTreeMap<String, f64>,
}

pub type VerticalSliceInputArtifactPayload = PersistedVerticalSliceInput;
pub type PersistedVerticalSliceInputArtifact = ArtifactEnvelope<VerticalSliceInputArtifactPayload>;
pub type LowBoostRecoveryBcArtifactPayload = LowBoostRecoveryBcSerializedArtifactV1;
pub type PersistedLowBoostRecoveryBcArtifact = ArtifactEnvelope<LowBoostRecoveryBcArtifactPayload>;

pub mod shared {
    pub use super::{
        ActionRecord, AnchorId, AnchorKind, AnchorRecord, BranchId, BranchOrigin, BranchRecord,
        CacheKey, FieldValue, FrameIndex, LowBoostRecoveryBcArtifactId,
        LowBoostRecoveryBcArtifactNoteV1, LowBoostRecoveryBcObservationV1,
        LowBoostRecoveryBcSerializedArtifactV1, LowBoostRecoveryBcTargetV1,
        LowBoostRecoveryCanonicalNoteV1, LowBoostRecoveryCanonicalOrientationNoteV1,
        LowBoostRecoveryCanonicalStateV1, LowBoostRecoveryContactSemanticsV1,
        LowBoostRecoveryEnvelopeSemanticsV1, LowBoostRecoveryEnvironmentStateEnvelopeV1,
        LowBoostRecoveryEventContactGraphV1, LowBoostRecoveryEventEdgeKindV1,
        LowBoostRecoveryEventEdgeV1, LowBoostRecoveryEventNodeKindV1, LowBoostRecoveryEventNodeV1,
        LowBoostRecoveryPhaseLabelV1, LowBoostRecoveryPhasePlanV1, LowBoostRecoveryPhaseV1,
        LowBoostRecoverySubjectStateEnvelopeV1, Metadata, RawStateWindowRef, ReplayId,
        ReplaySliceFamilyHint, ReplaySliceId, ReplaySliceRef, ReplaySourceRef, ReplaySubjectRef,
        SkillId, SkillRecord, StateSnapshot, TeacherLabelId, TeacherLabelRecord,
        TeacherLabelTarget, TimeWindow,
    };
}

pub mod persisted {
    pub use super::{
        ANCHOR_ARTIFACT_SCHEMA, ANCHOR_ARTIFACT_SCHEMA_NAME, ANCHOR_ARTIFACT_SCHEMA_VERSION,
        AnchorArtifactPayload, ArtifactEnvelope, ArtifactHeader, ArtifactKind, ArtifactSchema,
        BRANCH_ARTIFACT_SCHEMA, BRANCH_ARTIFACT_SCHEMA_NAME, BRANCH_ARTIFACT_SCHEMA_VERSION,
        BranchArtifactPayload, LOW_BOOST_RECOVERY_BC_ARTIFACT_SCHEMA,
        LOW_BOOST_RECOVERY_BC_ARTIFACT_SCHEMA_NAME, LOW_BOOST_RECOVERY_BC_ARTIFACT_SCHEMA_VERSION,
        LowBoostRecoveryBcArtifactPayload, PersistedAnchorArtifact, PersistedBranchArtifact,
        PersistedLowBoostRecoveryBcArtifact, PersistedSkillArtifact, PersistedTeacherLabelArtifact,
        PersistedVerticalSliceInputArtifact, SCOREBOARD_ARTIFACT_SCHEMA,
        SCOREBOARD_ARTIFACT_SCHEMA_NAME, SCOREBOARD_ARTIFACT_SCHEMA_VERSION, SKILL_ARTIFACT_SCHEMA,
        SKILL_ARTIFACT_SCHEMA_NAME, SKILL_ARTIFACT_SCHEMA_VERSION, SkillArtifactPayload,
        TEACHER_LABEL_ARTIFACT_SCHEMA, TEACHER_LABEL_ARTIFACT_SCHEMA_NAME,
        TEACHER_LABEL_ARTIFACT_SCHEMA_VERSION, TeacherLabelArtifactPayload,
        VERTICAL_SLICE_INPUT_ARTIFACT_SCHEMA, VERTICAL_SLICE_INPUT_ARTIFACT_SCHEMA_NAME,
        VERTICAL_SLICE_INPUT_ARTIFACT_SCHEMA_VERSION, VerticalSliceInputArtifactPayload,
    };
}

#[cfg(test)]
mod tests {
    use super::*;
    use serde_json::json;

    #[test]
    fn anchor_record_round_trips_through_json() {
        let record = AnchorRecord {
            id: AnchorId::new("anchor-1"),
            replay_id: ReplayId::new("replay-1"),
            frame_index: FrameIndex::new(42),
            kind: AnchorKind::Manual,
            metadata: Metadata::from([
                ("notes", FieldValue::StringList(vec!["manual".to_string()])),
                ("source", FieldValue::Text("manual".to_string())),
            ]),
        };

        let encoded = serde_json::to_value(&record).expect("record should serialize");
        assert_eq!(
            encoded,
            json!({
                "id": "anchor-1",
                "replay_id": "replay-1",
                "frame_index": 42,
                "kind": "manual",
                "metadata": {
                    "notes": {
                        "type": "string_list",
                        "value": ["manual"]
                    },
                    "source": {
                        "type": "text",
                        "value": "manual"
                    }
                }
            })
        );

        let decoded: AnchorRecord =
            serde_json::from_value(encoded).expect("record should deserialize");

        assert_eq!(decoded, record);
    }

    #[test]
    fn branch_record_round_trips_through_json() {
        let record = BranchRecord {
            id: BranchId::new("branch-1"),
            anchor_id: AnchorId::new("anchor-1"),
            origin: BranchOrigin::Manual,
            label: Some("candidate".to_string()),
            actions: vec![ActionRecord {
                action_key: "jump".to_string(),
                fields: Metadata::from([
                    ("pressed", FieldValue::Boolean(true)),
                    ("strength", FieldValue::Float(0.5)),
                ]),
            }],
            legality_hint: Some(true),
            metadata: Metadata::from([("source", FieldValue::Text("manual".to_string()))]),
        };

        let encoded = serde_json::to_value(&record).expect("record should serialize");
        assert_eq!(
            encoded,
            json!({
                "id": "branch-1",
                "anchor_id": "anchor-1",
                "origin": "manual",
                "label": "candidate",
                "actions": [
                    {
                        "action_key": "jump",
                        "fields": {
                            "pressed": {
                                "type": "boolean",
                                "value": true
                            },
                            "strength": {
                                "type": "float",
                                "value": 0.5
                            }
                        }
                    }
                ],
                "legality_hint": true,
                "metadata": {
                    "source": {
                        "type": "text",
                        "value": "manual"
                    }
                }
            })
        );

        let decoded: BranchRecord =
            serde_json::from_value(encoded).expect("record should deserialize");

        assert_eq!(decoded, record);
    }

    #[test]
    fn skill_record_round_trips_through_json() {
        let record = SkillRecord {
            id: SkillId::new("skill-1"),
            family: "movement".to_string(),
            canonical_name: "fast aerial".to_string(),
            aliases: vec!["speed aerial".to_string()],
            metadata: Metadata::from([(
                "tags",
                FieldValue::StringList(vec!["manual".to_string(), "seed".to_string()]),
            )]),
        };

        let encoded = serde_json::to_value(&record).expect("record should serialize");
        assert_eq!(
            encoded,
            json!({
                "id": "skill-1",
                "family": "movement",
                "canonical_name": "fast aerial",
                "aliases": ["speed aerial"],
                "metadata": {
                    "tags": {
                        "type": "string_list",
                        "value": ["manual", "seed"]
                    }
                }
            })
        );

        let decoded: SkillRecord =
            serde_json::from_value(encoded).expect("record should deserialize");

        assert_eq!(decoded, record);
    }

    #[test]
    fn teacher_label_record_round_trips_through_json() {
        let record = TeacherLabelRecord {
            id: TeacherLabelId::new("label-1"),
            target: TeacherLabelTarget::Branch(BranchId::new("branch-1")),
            label: "interesting".to_string(),
            score: Some(0.75),
            metadata: Metadata::from([("source", FieldValue::Text("teacher".to_string()))]),
        };

        let encoded = serde_json::to_value(&record).expect("record should serialize");
        assert_eq!(
            encoded,
            json!({
                "id": "label-1",
                "target": {
                    "target_type": "branch",
                    "id": "branch-1"
                },
                "label": "interesting",
                "score": 0.75,
                "metadata": {
                    "source": {
                        "type": "text",
                        "value": "teacher"
                    }
                }
            })
        );

        let decoded: TeacherLabelRecord =
            serde_json::from_value(encoded).expect("record should deserialize");

        assert_eq!(decoded, record);
    }

    #[test]
    fn persisted_anchor_artifact_round_trips_through_json() {
        let artifact = PersistedAnchorArtifact::new(
            ArtifactHeader::for_kind(ArtifactKind::Anchor, "mimir-tests")
                .with_created_by_component("mimir-anchor")
                .with_metadata(Metadata::from([(
                    "trace_id",
                    FieldValue::Text("trace-1".to_string()),
                )])),
            AnchorArtifactPayload {
                id: AnchorId::new("anchor-1"),
                replay_id: ReplayId::new("replay-1"),
                frame_index: FrameIndex::new(42),
                kind: AnchorKind::Manual,
                metadata: Metadata::from([("source", FieldValue::Text("manual".to_string()))]),
            },
        );

        let encoded = serde_json::to_value(&artifact).expect("artifact should serialize");
        assert_eq!(
            encoded,
            json!({
                "header": {
                    "schema_name": "mimir.anchor_artifact",
                    "schema_version": 1,
                    "producer": "mimir-tests",
                    "created_by_component": "mimir-anchor",
                    "metadata": {
                        "trace_id": {
                            "type": "text",
                            "value": "trace-1"
                        }
                    }
                },
                "payload": {
                    "id": "anchor-1",
                    "replay_id": "replay-1",
                    "frame_index": 42,
                    "kind": "manual",
                    "metadata": {
                        "source": {
                            "type": "text",
                            "value": "manual"
                        }
                    }
                }
            })
        );

        let decoded: PersistedAnchorArtifact =
            serde_json::from_value(encoded).expect("artifact should deserialize");

        assert_eq!(decoded, artifact);
    }

    #[test]
    fn persisted_branch_artifact_round_trips_through_json() {
        let artifact = PersistedBranchArtifact::new(
            ArtifactHeader::for_kind(ArtifactKind::Branch, "mimir-tests")
                .with_created_by_component("mimir-branch")
                .with_metadata(Metadata::from([(
                    "trace_id",
                    FieldValue::Text("trace-branch-1".to_string()),
                )])),
            BranchArtifactPayload {
                id: BranchId::new("branch-1"),
                anchor_id: AnchorId::new("anchor-1"),
                origin: BranchOrigin::Counterfactual,
                label: Some("flip_reset_line".to_string()),
                actions: vec![ActionRecord {
                    action_key: "jump".to_string(),
                    fields: Metadata::from([("pressed", FieldValue::Boolean(true))]),
                }],
                legality_hint: Some(false),
                metadata: Metadata::from([("source", FieldValue::Text("seed".to_string()))]),
            },
        );

        let encoded = serde_json::to_value(&artifact).expect("artifact should serialize");
        assert_eq!(
            encoded,
            json!({
                "header": {
                    "schema_name": "mimir.branch_artifact",
                    "schema_version": 1,
                    "producer": "mimir-tests",
                    "created_by_component": "mimir-branch",
                    "metadata": {
                        "trace_id": {
                            "type": "text",
                            "value": "trace-branch-1"
                        }
                    }
                },
                "payload": {
                    "id": "branch-1",
                    "anchor_id": "anchor-1",
                    "origin": "counterfactual",
                    "label": "flip_reset_line",
                    "actions": [
                        {
                            "action_key": "jump",
                            "fields": {
                                "pressed": {
                                    "type": "boolean",
                                    "value": true
                                }
                            }
                        }
                    ],
                    "legality_hint": false,
                    "metadata": {
                        "source": {
                            "type": "text",
                            "value": "seed"
                        }
                    }
                }
            })
        );

        let decoded: PersistedBranchArtifact =
            serde_json::from_value(encoded).expect("artifact should deserialize");

        assert_eq!(decoded, artifact);
    }

    #[test]
    fn artifact_kind_schema_constants_stay_paired() {
        assert_eq!(ArtifactKind::Anchor.schema(), ANCHOR_ARTIFACT_SCHEMA);
        assert_eq!(ANCHOR_ARTIFACT_SCHEMA.kind, ArtifactKind::Anchor);
        assert_eq!(ANCHOR_ARTIFACT_SCHEMA_NAME, ANCHOR_ARTIFACT_SCHEMA.name);
        assert_eq!(
            ANCHOR_ARTIFACT_SCHEMA_VERSION,
            ANCHOR_ARTIFACT_SCHEMA.version
        );

        assert_eq!(ArtifactKind::Branch.schema(), BRANCH_ARTIFACT_SCHEMA);
        assert_eq!(BRANCH_ARTIFACT_SCHEMA.kind, ArtifactKind::Branch);
        assert_eq!(BRANCH_ARTIFACT_SCHEMA_NAME, BRANCH_ARTIFACT_SCHEMA.name);
        assert_eq!(
            BRANCH_ARTIFACT_SCHEMA_VERSION,
            BRANCH_ARTIFACT_SCHEMA.version
        );

        assert_eq!(ArtifactKind::Skill.schema(), SKILL_ARTIFACT_SCHEMA);
        assert_eq!(SKILL_ARTIFACT_SCHEMA.kind, ArtifactKind::Skill);
        assert_eq!(SKILL_ARTIFACT_SCHEMA_NAME, SKILL_ARTIFACT_SCHEMA.name);
        assert_eq!(SKILL_ARTIFACT_SCHEMA_VERSION, SKILL_ARTIFACT_SCHEMA.version);

        assert_eq!(
            ArtifactKind::TeacherLabel.schema(),
            TEACHER_LABEL_ARTIFACT_SCHEMA
        );
        assert_eq!(
            TEACHER_LABEL_ARTIFACT_SCHEMA.kind,
            ArtifactKind::TeacherLabel
        );
        assert_eq!(
            TEACHER_LABEL_ARTIFACT_SCHEMA_NAME,
            TEACHER_LABEL_ARTIFACT_SCHEMA.name
        );
        assert_eq!(
            TEACHER_LABEL_ARTIFACT_SCHEMA_VERSION,
            TEACHER_LABEL_ARTIFACT_SCHEMA.version
        );

        assert_eq!(
            ArtifactKind::Scoreboard.schema(),
            SCOREBOARD_ARTIFACT_SCHEMA
        );
        assert_eq!(SCOREBOARD_ARTIFACT_SCHEMA.kind, ArtifactKind::Scoreboard);
        assert_eq!(
            SCOREBOARD_ARTIFACT_SCHEMA_NAME,
            SCOREBOARD_ARTIFACT_SCHEMA.name
        );
        assert_eq!(
            SCOREBOARD_ARTIFACT_SCHEMA_VERSION,
            SCOREBOARD_ARTIFACT_SCHEMA.version
        );

        assert_eq!(
            ArtifactKind::VerticalSliceInput.schema(),
            VERTICAL_SLICE_INPUT_ARTIFACT_SCHEMA
        );
        assert_eq!(
            VERTICAL_SLICE_INPUT_ARTIFACT_SCHEMA.kind,
            ArtifactKind::VerticalSliceInput
        );
        assert_eq!(
            VERTICAL_SLICE_INPUT_ARTIFACT_SCHEMA_NAME,
            VERTICAL_SLICE_INPUT_ARTIFACT_SCHEMA.name
        );
        assert_eq!(
            VERTICAL_SLICE_INPUT_ARTIFACT_SCHEMA_VERSION,
            VERTICAL_SLICE_INPUT_ARTIFACT_SCHEMA.version
        );

        assert_eq!(
            ArtifactKind::LowBoostRecoveryBcArtifact.schema(),
            LOW_BOOST_RECOVERY_BC_ARTIFACT_SCHEMA
        );
        assert_eq!(
            LOW_BOOST_RECOVERY_BC_ARTIFACT_SCHEMA.kind,
            ArtifactKind::LowBoostRecoveryBcArtifact
        );
        assert_eq!(
            LOW_BOOST_RECOVERY_BC_ARTIFACT_SCHEMA_NAME,
            LOW_BOOST_RECOVERY_BC_ARTIFACT_SCHEMA.name
        );
        assert_eq!(
            LOW_BOOST_RECOVERY_BC_ARTIFACT_SCHEMA_VERSION,
            LOW_BOOST_RECOVERY_BC_ARTIFACT_SCHEMA.version
        );
    }

    #[test]
    fn persisted_vertical_slice_input_artifact_round_trips_through_json() {
        let artifact = PersistedVerticalSliceInputArtifact::new(
            ArtifactHeader::for_kind(ArtifactKind::VerticalSliceInput, "mimir-tests")
                .with_created_by_component("mimir-cli")
                .with_metadata(Metadata::from([(
                    "fixture_lane",
                    FieldValue::Text("Stage69Sample".to_string()),
                )])),
            PersistedVerticalSliceInput {
                replay_id: ReplayId::new("replay-stage69"),
                export_name: "stage69-vertical-slice".to_string(),
                teacher_namespace: "stage69.teacher".to_string(),
                simulation_seed: 69,
                anchor_hint: PersistedVerticalSliceAnchorHint {
                    anchor_id: Some(AnchorId::new("anchor-stage69")),
                    frame_index: FrameIndex::new(128),
                    kind: AnchorKind::Manual,
                    metadata: Metadata::from([(
                        "source",
                        FieldValue::Text("stage69-fixture".to_string()),
                    )]),
                },
                proposals: vec![
                    PersistedVerticalSliceProposal {
                        label: "candidate-alpha".to_string(),
                        actions: vec![ActionRecord {
                            action_key: "jump".to_string(),
                            fields: Metadata::from([("pressed", FieldValue::Boolean(true))]),
                        }],
                        legal_hint: Some(true),
                        metadata: Metadata::from([(
                            "proposal_source",
                            FieldValue::Text("fixture-alpha".to_string()),
                        )]),
                        score_signals: BTreeMap::from([
                            ("coverage".to_string(), 2.0),
                            ("stability".to_string(), 3.0),
                        ]),
                    },
                    PersistedVerticalSliceProposal {
                        label: "candidate-beta".to_string(),
                        actions: vec![
                            ActionRecord {
                                action_key: "boost".to_string(),
                                fields: Metadata::from([("pressed", FieldValue::Boolean(true))]),
                            },
                            ActionRecord {
                                action_key: "steer".to_string(),
                                fields: Metadata::from([("direction", FieldValue::Float(0.5))]),
                            },
                        ],
                        legal_hint: Some(true),
                        metadata: Metadata::from([(
                            "proposal_source",
                            FieldValue::Text("fixture-beta".to_string()),
                        )]),
                        score_signals: BTreeMap::from([
                            ("coverage".to_string(), 4.0),
                            ("stability".to_string(), 2.0),
                        ]),
                    },
                ],
                scorer_weights: BTreeMap::from([
                    ("coverage".to_string(), 1.0),
                    ("stability".to_string(), 0.5),
                ]),
            },
        );

        let encoded = serde_json::to_value(&artifact).expect("artifact should serialize");
        let decoded: PersistedVerticalSliceInputArtifact =
            serde_json::from_value(encoded).expect("artifact should deserialize");

        assert_eq!(decoded, artifact);
    }

    #[test]
    fn float_field_values_reject_non_finite_numbers() {
        let error = serde_json::to_string(&FieldValue::Float(f64::NAN))
            .expect_err("non-finite floats should be rejected");

        assert!(
            error
                .to_string()
                .contains("floating-point field values must be finite")
        );
    }

    #[test]
    fn teacher_label_scores_reject_non_finite_numbers() {
        let record = TeacherLabelRecord {
            id: TeacherLabelId::new("label-1"),
            target: TeacherLabelTarget::Replay(ReplayId::new("replay-1")),
            label: "interesting".to_string(),
            score: Some(f32::NAN),
            metadata: Metadata::new(),
        };

        let error =
            serde_json::to_string(&record).expect_err("non-finite scores should be rejected");

        assert!(
            error
                .to_string()
                .contains("teacher label scores must be finite")
        );
    }

    #[test]
    fn replay_slice_ref_round_trips_through_json() {
        let slice = ReplaySliceRef {
            slice_id: ReplaySliceId::new("slice-1"),
            source_replay: ReplaySourceRef {
                replay_id: ReplayId::new("replay-1"),
                provenance_label: "manual.replay".to_string(),
            },
            frame_window: TimeWindow {
                start: FrameIndex::new(120),
                end_exclusive: FrameIndex::new(180),
            },
            subject: ReplaySubjectRef::new("player:blue:0"),
            family_hint: ReplaySliceFamilyHint::LowBoostRecovery,
            raw_state_window_ref: RawStateWindowRef::new("window-1"),
            audit_note: Some("seed candidate".to_string()),
        };

        let encoded = serde_json::to_value(&slice).expect("slice should serialize");
        let decoded: ReplaySliceRef =
            serde_json::from_value(encoded).expect("slice should deserialize");

        assert_eq!(decoded, slice);
    }

    #[test]
    fn replay_slice_ref_rejects_unknown_family_hint() {
        let error = serde_json::from_value::<ReplaySliceRef>(json!({
            "slice_id": "slice-1",
            "source_replay": {
                "replay_id": "replay-1",
                "provenance_label": "manual.replay"
            },
            "frame_window": {
                "start": 120,
                "end_exclusive": 180
            },
            "subject": "player:blue:0",
            "family_hint": "unsupported_family",
            "raw_state_window_ref": "window-1"
        }))
        .expect_err("unknown family hints should be rejected");

        assert!(error.to_string().contains("unknown variant"));
    }

    #[test]
    fn low_boost_recovery_contract_types_round_trip_through_json() {
        let canonical_state = LowBoostRecoveryCanonicalStateV1 {
            slice_id: ReplaySliceId::new("slice-1"),
            source_replay: ReplaySourceRef {
                replay_id: ReplayId::new("replay-1"),
                provenance_label: "manual.replay".to_string(),
            },
            subject: ReplaySubjectRef::new("player:blue:0"),
            frame_window: TimeWindow {
                start: FrameIndex::new(120),
                end_exclusive: FrameIndex::new(180),
            },
            raw_state_window_ref: RawStateWindowRef::new("window-1"),
            orientation_note: LowBoostRecoveryCanonicalOrientationNoteV1::SubjectAnchoredWindowOnly,
            subject_state_envelope: LowBoostRecoverySubjectStateEnvelopeV1 {
                subject: ReplaySubjectRef::new("player:blue:0"),
                frame_window: TimeWindow {
                    start: FrameIndex::new(120),
                    end_exclusive: FrameIndex::new(180),
                },
                semantics: LowBoostRecoveryEnvelopeSemanticsV1::RawStateWindowReferenceOnly,
            },
            environment_state_envelope: LowBoostRecoveryEnvironmentStateEnvelopeV1 {
                frame_window: TimeWindow {
                    start: FrameIndex::new(120),
                    end_exclusive: FrameIndex::new(180),
                },
                semantics: LowBoostRecoveryEnvelopeSemanticsV1::RawStateWindowReferenceOnly,
            },
            canonicalization_notes: vec![
                LowBoostRecoveryCanonicalNoteV1::BoostAmountUnresolved,
                LowBoostRecoveryCanonicalNoteV1::ContactTruthUnresolved,
                LowBoostRecoveryCanonicalNoteV1::RecoverySuccessUnresolved,
                LowBoostRecoveryCanonicalNoteV1::ReplayOrientationNormalizationDeferred,
            ],
        };

        let encoded =
            serde_json::to_value(&canonical_state).expect("canonical state should serialize");
        let decoded: LowBoostRecoveryCanonicalStateV1 =
            serde_json::from_value(encoded).expect("canonical state should deserialize");

        assert_eq!(decoded, canonical_state);

        let graph = LowBoostRecoveryEventContactGraphV1 {
            slice_id: ReplaySliceId::new("slice-1"),
            frame_window: TimeWindow {
                start: FrameIndex::new(120),
                end_exclusive: FrameIndex::new(180),
            },
            nodes: vec![
                LowBoostRecoveryEventNodeV1 {
                    node_id: 0,
                    frame_index: FrameIndex::new(120),
                    kind: LowBoostRecoveryEventNodeKindV1::SliceWindowStart,
                },
                LowBoostRecoveryEventNodeV1 {
                    node_id: 1,
                    frame_index: FrameIndex::new(180),
                    kind: LowBoostRecoveryEventNodeKindV1::SliceWindowEndExclusive,
                },
            ],
            edges: vec![LowBoostRecoveryEventEdgeV1 {
                from_node_id: 0,
                to_node_id: 1,
                kind: LowBoostRecoveryEventEdgeKindV1::ObservedSliceWindow,
            }],
            contact_semantics:
                LowBoostRecoveryContactSemanticsV1::UnresolvedFromReplaySliceContract,
        };

        let encoded = serde_json::to_value(&graph).expect("graph should serialize");
        let decoded: LowBoostRecoveryEventContactGraphV1 =
            serde_json::from_value(encoded).expect("graph should deserialize");

        assert_eq!(decoded, graph);

        let phase_plan = LowBoostRecoveryPhasePlanV1 {
            slice_id: ReplaySliceId::new("slice-1"),
            phases: vec![LowBoostRecoveryPhaseV1 {
                phase_id: 0,
                label: LowBoostRecoveryPhaseLabelV1::CandidateRecoveryWindow,
                start: FrameIndex::new(120),
                end_exclusive: FrameIndex::new(180),
            }],
        };

        let encoded = serde_json::to_value(&phase_plan).expect("phase plan should serialize");
        let decoded: LowBoostRecoveryPhasePlanV1 =
            serde_json::from_value(encoded).expect("phase plan should deserialize");

        assert_eq!(decoded, phase_plan);
    }

    #[test]
    fn low_boost_recovery_parameter_and_variant_types_round_trip_through_json() {
        let parameter_bundle = LowBoostRecoveryParameterBundleV1 {
            slice_id: ReplaySliceId::new("slice-1"),
            family: ReplaySliceFamilyHint::LowBoostRecovery,
            source_replay: ReplaySourceRef {
                replay_id: ReplayId::new("replay-1"),
                provenance_label: "manual.replay".to_string(),
            },
            subject: ReplaySubjectRef::new("player:blue:0"),
            raw_state_window_ref: RawStateWindowRef::new("window-1"),
            phase_window_link: LowBoostRecoveryPhaseWindowLinkV1 {
                phase_id: 0,
                phase_label: LowBoostRecoveryPhaseLabelV1::CandidateRecoveryWindow,
                window: TimeWindow {
                    start: FrameIndex::new(120),
                    end_exclusive: FrameIndex::new(180),
                },
            },
            recovery_window_interpretation:
                LowBoostRecoveryWindowInterpretationV1::CandidateRecoveryWindowOnly,
            observed_window_duration_frames: LowBoostRecoveryFrameRangeV1 {
                min_inclusive: 60,
                max_inclusive: 60,
            },
            boundary_trim_budget_frames: LowBoostRecoveryFrameRangeV1 {
                min_inclusive: 0,
                max_inclusive: 1,
            },
            parameter_notes: vec![
                LowBoostRecoveryParameterNoteV1::ObservedWindowDerivedFromCanonicalPhase,
                LowBoostRecoveryParameterNoteV1::BoundaryVariationLimitedToSingleFrameTrims,
            ],
            unresolved_assumptions: vec![
                LowBoostRecoveryUnresolvedAssumptionV1::LowBoostThresholdUnproven,
                LowBoostRecoveryUnresolvedAssumptionV1::ContactTruthUnproven,
                LowBoostRecoveryUnresolvedAssumptionV1::RecoverySuccessUnproven,
                LowBoostRecoveryUnresolvedAssumptionV1::ReplayOrientationNormalizationDeferred,
                LowBoostRecoveryUnresolvedAssumptionV1::PhysicsReachabilityUnproven,
            ],
        };

        let encoded =
            serde_json::to_value(&parameter_bundle).expect("parameter bundle should serialize");
        let decoded: LowBoostRecoveryParameterBundleV1 =
            serde_json::from_value(encoded).expect("parameter bundle should deserialize");
        assert_eq!(decoded, parameter_bundle);

        let variant = LowBoostRecoveryGeneratedVariantV1 {
            variant_id: LowBoostRecoveryVariantId::new("slice-1:candidate_recovery_window:exact"),
            source_slice_id: ReplaySliceId::new("slice-1"),
            source_phase_id: 0,
            family: ReplaySliceFamilyHint::LowBoostRecovery,
            variant_window: TimeWindow {
                start: FrameIndex::new(120),
                end_exclusive: FrameIndex::new(180),
            },
            window_override: LowBoostRecoveryWindowOverrideV1 {
                trim_start_frames: 0,
                trim_end_frames: 0,
            },
            difficulty_hint: LowBoostRecoveryDifficultyHintV1::ReferenceSeedWindow,
            generation_reason: LowBoostRecoveryGenerationReasonV1::PreserveObservedWindow,
            unresolved_assumptions: vec![
                LowBoostRecoveryUnresolvedAssumptionV1::LowBoostThresholdUnproven,
                LowBoostRecoveryUnresolvedAssumptionV1::ContactTruthUnproven,
                LowBoostRecoveryUnresolvedAssumptionV1::RecoverySuccessUnproven,
                LowBoostRecoveryUnresolvedAssumptionV1::ReplayOrientationNormalizationDeferred,
                LowBoostRecoveryUnresolvedAssumptionV1::PhysicsReachabilityUnproven,
            ],
        };

        let encoded = serde_json::to_value(&variant).expect("variant should serialize");
        let decoded: LowBoostRecoveryGeneratedVariantV1 =
            serde_json::from_value(encoded).expect("variant should deserialize");
        assert_eq!(decoded, variant);
    }

    #[test]
    fn low_boost_recovery_validation_types_round_trip_through_json() {
        let result = LowBoostRecoveryValidationResultV1 {
            source_slice_id: ReplaySliceId::new("slice-1"),
            source_phase_id: 0,
            reference_variant_id: Some(LowBoostRecoveryVariantId::new(
                "slice-1:candidate_recovery_window:exact",
            )),
            evaluated_variant_ids: vec![
                LowBoostRecoveryVariantId::new("slice-1:candidate_recovery_window:exact"),
                LowBoostRecoveryVariantId::new("slice-1:candidate_recovery_window:trim_start_1"),
                LowBoostRecoveryVariantId::new("slice-1:candidate_recovery_window:trim_end_1"),
            ],
            decision: LowBoostRecoveryValidationDecisionV1::AcceptCandidate,
            reason: LowBoostRecoveryValidationReasonV1::ProvisionalCandidateAccepted,
            confidence_band: LowBoostRecoveryConfidenceBandV1::BoundaryStable,
            carried_unresolved_assumptions: vec![
                LowBoostRecoveryUnresolvedAssumptionV1::LowBoostThresholdUnproven,
                LowBoostRecoveryUnresolvedAssumptionV1::ContactTruthUnproven,
                LowBoostRecoveryUnresolvedAssumptionV1::RecoverySuccessUnproven,
                LowBoostRecoveryUnresolvedAssumptionV1::ReplayOrientationNormalizationDeferred,
                LowBoostRecoveryUnresolvedAssumptionV1::PhysicsReachabilityUnproven,
            ],
            validator_notes: vec![
                LowBoostRecoveryValidationNoteV1::ReferenceVariantPresent,
                LowBoostRecoveryValidationNoteV1::StartTrimVariantPresent,
                LowBoostRecoveryValidationNoteV1::EndTrimVariantPresent,
                LowBoostRecoveryValidationNoteV1::KnownUnresolvedAssumptionsCarriedForward,
                LowBoostRecoveryValidationNoteV1::ExactWindowMeetsMinimumEvidenceFloor,
                LowBoostRecoveryValidationNoteV1::TrimmedVariantsMeetStabilityFloor,
            ],
        };

        let encoded = serde_json::to_value(&result).expect("validation result should serialize");
        let decoded: LowBoostRecoveryValidationResultV1 =
            serde_json::from_value(encoded).expect("validation result should deserialize");

        assert_eq!(decoded, result);
    }

    #[test]
    fn low_boost_recovery_curriculum_export_shell_types_round_trip_through_json() {
        let shell = LowBoostRecoveryCurriculumExportShellV1 {
            family: ReplaySliceFamilyHint::LowBoostRecovery,
            source_slice_id: ReplaySliceId::new("slice-1"),
            source_replay: ReplaySourceRef {
                replay_id: ReplayId::new("replay-1"),
                provenance_label: "manual.replay".to_string(),
            },
            source_subject: ReplaySubjectRef::new("player:blue:0"),
            source_raw_state_window_ref: RawStateWindowRef::new("window-1"),
            source_phase_id: 0,
            source_phase_window: TimeWindow {
                start: FrameIndex::new(120),
                end_exclusive: FrameIndex::new(180),
            },
            accepted_reference_variant_id: LowBoostRecoveryVariantId::new(
                "slice-1:candidate_recovery_window:exact",
            ),
            accepted_reference_variant_window: TimeWindow {
                start: FrameIndex::new(120),
                end_exclusive: FrameIndex::new(180),
            },
            evaluated_variant_ids: vec![
                LowBoostRecoveryVariantId::new("slice-1:candidate_recovery_window:exact"),
                LowBoostRecoveryVariantId::new("slice-1:candidate_recovery_window:trim_start_1"),
                LowBoostRecoveryVariantId::new("slice-1:candidate_recovery_window:trim_end_1"),
            ],
            accepted_decision: LowBoostRecoveryValidationDecisionV1::AcceptCandidate,
            decision_reason: LowBoostRecoveryValidationReasonV1::ProvisionalCandidateAccepted,
            confidence_band: LowBoostRecoveryConfidenceBandV1::BoundaryStable,
            carried_unresolved_assumptions: vec![
                LowBoostRecoveryUnresolvedAssumptionV1::LowBoostThresholdUnproven,
                LowBoostRecoveryUnresolvedAssumptionV1::ContactTruthUnproven,
                LowBoostRecoveryUnresolvedAssumptionV1::RecoverySuccessUnproven,
                LowBoostRecoveryUnresolvedAssumptionV1::ReplayOrientationNormalizationDeferred,
                LowBoostRecoveryUnresolvedAssumptionV1::PhysicsReachabilityUnproven,
            ],
            shell_notes: vec![
                LowBoostRecoveryCurriculumExportShellNoteV1::AcceptedCandidateOnly,
                LowBoostRecoveryCurriculumExportShellNoteV1::ProvisionalAcceptanceOnly,
                LowBoostRecoveryCurriculumExportShellNoteV1::UnresolvedAssumptionsCarriedForward,
            ],
            consumer_hint: LowBoostRecoveryCurriculumExportConsumerHintV1::EvalHarnessOnly,
        };

        let encoded = serde_json::to_value(&shell).expect("shell should serialize");
        let decoded: LowBoostRecoveryCurriculumExportShellV1 =
            serde_json::from_value(encoded).expect("shell should deserialize");

        assert_eq!(decoded, shell);
    }

    #[test]
    fn low_boost_recovery_eval_result_types_round_trip_through_json() {
        let result = LowBoostRecoveryEvalResultV1 {
            source_slice_id: ReplaySliceId::new("slice-1"),
            source_phase_id: 0,
            accepted_reference_variant_id: Some(LowBoostRecoveryVariantId::new(
                "slice-1:candidate_recovery_window:exact",
            )),
            eval_status: LowBoostRecoveryEvalStatusV1::ShellReadyForFutureConsumer,
            eval_notes: vec![
                LowBoostRecoveryEvalNoteV1::SourceLineagePresent,
                LowBoostRecoveryEvalNoteV1::AcceptedReferenceVariantLineagePresent,
                LowBoostRecoveryEvalNoteV1::AcceptedShellContractSatisfied,
                LowBoostRecoveryEvalNoteV1::BoundedEvidenceConsistent,
                LowBoostRecoveryEvalNoteV1::UnresolvedAssumptionsVisible,
                LowBoostRecoveryEvalNoteV1::ReferenceWindowAvailable,
            ],
            metric_summary: LowBoostRecoveryEvalMetricSummaryV1 {
                lineage_completeness: true,
                accepted_shell_completeness: true,
                bounded_evidence_consistency: true,
                unresolved_burden_visibility: true,
                reference_window_availability: true,
            },
            carried_confidence_band: LowBoostRecoveryConfidenceBandV1::BoundaryStable,
            carried_unresolved_assumptions: vec![
                LowBoostRecoveryUnresolvedAssumptionV1::LowBoostThresholdUnproven,
                LowBoostRecoveryUnresolvedAssumptionV1::ContactTruthUnproven,
                LowBoostRecoveryUnresolvedAssumptionV1::RecoverySuccessUnproven,
                LowBoostRecoveryUnresolvedAssumptionV1::ReplayOrientationNormalizationDeferred,
                LowBoostRecoveryUnresolvedAssumptionV1::PhysicsReachabilityUnproven,
            ],
        };

        let encoded = serde_json::to_value(&result).expect("eval result should serialize");
        let decoded: LowBoostRecoveryEvalResultV1 =
            serde_json::from_value(encoded).expect("eval result should deserialize");

        assert_eq!(decoded, result);
    }

    #[test]
    fn low_boost_recovery_consumer_planning_result_types_round_trip_through_json() {
        let result = LowBoostRecoveryConsumerPlanningResultV1 {
            source_slice_id: ReplaySliceId::new("slice-1"),
            source_replay: ReplaySourceRef {
                replay_id: ReplayId::new("replay-1"),
                provenance_label: "manual.replay".to_string(),
            },
            source_subject: ReplaySubjectRef::new("player:blue:0"),
            source_raw_state_window_ref: RawStateWindowRef::new("window-1"),
            source_phase_id: 0,
            accepted_reference_variant_id: Some(LowBoostRecoveryVariantId::new(
                "slice-1:candidate_recovery_window:exact",
            )),
            eval_readiness_status: LowBoostRecoveryEvalStatusV1::ShellReadyForFutureConsumer,
            carried_confidence_band: LowBoostRecoveryConfidenceBandV1::BoundaryStable,
            carried_unresolved_assumptions: vec![
                LowBoostRecoveryUnresolvedAssumptionV1::LowBoostThresholdUnproven,
                LowBoostRecoveryUnresolvedAssumptionV1::ContactTruthUnproven,
                LowBoostRecoveryUnresolvedAssumptionV1::RecoverySuccessUnproven,
                LowBoostRecoveryUnresolvedAssumptionV1::ReplayOrientationNormalizationDeferred,
                LowBoostRecoveryUnresolvedAssumptionV1::PhysicsReachabilityUnproven,
            ],
            disposition:
                LowBoostRecoveryConsumerPlanningDispositionV1::BcCandidateReadyForContractDefinition,
            planning_notes: vec![
                LowBoostRecoveryConsumerPlanningNoteV1::BcMilestoneApproaching,
                LowBoostRecoveryConsumerPlanningNoteV1::ShellEvalBoundaryAligned,
                LowBoostRecoveryConsumerPlanningNoteV1::AcceptedReferenceVariantLineagePreserved,
                LowBoostRecoveryConsumerPlanningNoteV1::UnresolvedAssumptionsCarriedForward,
                LowBoostRecoveryConsumerPlanningNoteV1::ReadyForBcContractDefinitionOnly,
                LowBoostRecoveryConsumerPlanningNoteV1::PlanningOnlyNotBcUsefulnessProof,
            ],
        };

        let encoded =
            serde_json::to_value(&result).expect("consumer planning result should serialize");
        let decoded: LowBoostRecoveryConsumerPlanningResultV1 =
            serde_json::from_value(encoded).expect("consumer planning result should deserialize");

        assert_eq!(decoded, result);
    }

    #[test]
    fn low_boost_recovery_bc_row_types_round_trip_through_json() {
        let row = LowBoostRecoveryBcRowV1 {
            family: ReplaySliceFamilyHint::LowBoostRecovery,
            source_slice_id: ReplaySliceId::new("slice-1"),
            source_replay: ReplaySourceRef {
                replay_id: ReplayId::new("replay-1"),
                provenance_label: "manual.replay".to_string(),
            },
            source_subject: ReplaySubjectRef::new("player:blue:0"),
            source_raw_state_window_ref: RawStateWindowRef::new("window-1"),
            source_phase_id: 0,
            accepted_reference_variant_id: LowBoostRecoveryVariantId::new(
                "slice-1:candidate_recovery_window:exact",
            ),
            supervision_window_role:
                LowBoostRecoveryBcSupervisionWindowRoleV1::AcceptedReferenceVariantWindow,
            observation_binding_kind:
                LowBoostRecoveryBcObservationBindingKindV1::AcceptedReferenceWindowFromRawStateWindowRef,
            target_binding_kind:
                LowBoostRecoveryBcTargetBindingKindV1::AcceptedReferenceVariantControlTargetDeferred,
            carried_confidence_band: LowBoostRecoveryConfidenceBandV1::BoundaryStable,
            carried_unresolved_assumptions: vec![
                LowBoostRecoveryUnresolvedAssumptionV1::LowBoostThresholdUnproven,
                LowBoostRecoveryUnresolvedAssumptionV1::ContactTruthUnproven,
                LowBoostRecoveryUnresolvedAssumptionV1::RecoverySuccessUnproven,
                LowBoostRecoveryUnresolvedAssumptionV1::ReplayOrientationNormalizationDeferred,
                LowBoostRecoveryUnresolvedAssumptionV1::PhysicsReachabilityUnproven,
            ],
            bc_contract_notes: vec![
                LowBoostRecoveryBcContractNoteV1::ContractDefinitionOnly,
                LowBoostRecoveryBcContractNoteV1::AcceptedShellPlanningBoundaryAligned,
                LowBoostRecoveryBcContractNoteV1::ObservationBindingDeferredToLaterSerialization,
                LowBoostRecoveryBcContractNoteV1::TargetBindingDeferredToLaterSerialization,
                LowBoostRecoveryBcContractNoteV1::ProvisionalConfidenceCarriedForward,
                LowBoostRecoveryBcContractNoteV1::UnresolvedAssumptionsCarriedForward,
                LowBoostRecoveryBcContractNoteV1::NotBcUsefulnessProof,
            ],
        };

        let encoded = serde_json::to_value(&row).expect("bc row should serialize");
        let decoded: LowBoostRecoveryBcRowV1 =
            serde_json::from_value(encoded).expect("bc row should deserialize");

        assert_eq!(decoded, row);
    }

    #[test]
    fn low_boost_recovery_bc_serialized_artifact_types_round_trip_through_json() {
        let artifact = LowBoostRecoveryBcSerializedArtifactV1 {
            artifact_id: LowBoostRecoveryBcArtifactId::new(
                "slice-1:candidate_recovery_window:exact:bc_artifact_v1",
            ),
            family: ReplaySliceFamilyHint::LowBoostRecovery,
            source_slice_id: ReplaySliceId::new("slice-1"),
            source_replay: ReplaySourceRef {
                replay_id: ReplayId::new("replay-1"),
                provenance_label: "manual.replay".to_string(),
            },
            source_subject: ReplaySubjectRef::new("player:blue:0"),
            source_raw_state_window_ref: RawStateWindowRef::new("window-1"),
            source_phase_id: 0,
            accepted_reference_variant_id: LowBoostRecoveryVariantId::new(
                "slice-1:candidate_recovery_window:exact",
            ),
            observation: LowBoostRecoveryBcObservationV1 {
                binding_kind:
                    LowBoostRecoveryBcObservationBindingKindV1::AcceptedReferenceWindowFromRawStateWindowRef,
                supervision_window_role:
                    LowBoostRecoveryBcSupervisionWindowRoleV1::AcceptedReferenceVariantWindow,
                accepted_reference_window: TimeWindow {
                    start: FrameIndex::new(120),
                    end_exclusive: FrameIndex::new(180),
                },
            },
            target: LowBoostRecoveryBcTargetV1 {
                binding_kind:
                    LowBoostRecoveryBcTargetBindingKindV1::AcceptedReferenceVariantControlTargetDeferred,
                accepted_reference_variant_id: LowBoostRecoveryVariantId::new(
                    "slice-1:candidate_recovery_window:exact",
                ),
                accepted_reference_window: TimeWindow {
                    start: FrameIndex::new(120),
                    end_exclusive: FrameIndex::new(180),
                },
            },
            carried_confidence_band: LowBoostRecoveryConfidenceBandV1::BoundaryStable,
            carried_unresolved_assumptions: vec![
                LowBoostRecoveryUnresolvedAssumptionV1::LowBoostThresholdUnproven,
                LowBoostRecoveryUnresolvedAssumptionV1::ContactTruthUnproven,
                LowBoostRecoveryUnresolvedAssumptionV1::RecoverySuccessUnproven,
                LowBoostRecoveryUnresolvedAssumptionV1::ReplayOrientationNormalizationDeferred,
                LowBoostRecoveryUnresolvedAssumptionV1::PhysicsReachabilityUnproven,
            ],
            artifact_notes: vec![
                LowBoostRecoveryBcArtifactNoteV1::SerializedFromBcContractRow,
                LowBoostRecoveryBcArtifactNoteV1::AcceptedShellReferenceWindowMaterialized,
                LowBoostRecoveryBcArtifactNoteV1::ObservationPayloadReferenceBound,
                LowBoostRecoveryBcArtifactNoteV1::TargetPayloadControlDeferred,
                LowBoostRecoveryBcArtifactNoteV1::ProvisionalConfidenceCarriedForward,
                LowBoostRecoveryBcArtifactNoteV1::UnresolvedAssumptionsCarriedForward,
                LowBoostRecoveryBcArtifactNoteV1::NotBcUsefulnessProof,
            ],
        };

        let encoded = serde_json::to_value(&artifact).expect("bc artifact should serialize");
        let decoded: LowBoostRecoveryBcSerializedArtifactV1 =
            serde_json::from_value(encoded).expect("bc artifact should deserialize");

        assert_eq!(decoded, artifact);
    }

    #[test]
    fn low_boost_recovery_bc_actual_filesystem_emission_specimen_file_types_round_trip_through_json()
     {
        let specimen = LowBoostRecoveryBcActualFilesystemEmissionSpecimenFileV1 {
            lane_ordinal: 0,
            specimen_ordinal: 1,
            artifact_id: LowBoostRecoveryBcArtifactId::new(
                "slice-1:candidate_recovery_window:trim_start_1:bc_artifact_v1",
            ),
            source_slice_id: ReplaySliceId::new("slice-1"),
            source_replay: ReplaySourceRef {
                replay_id: ReplayId::new("replay-1"),
                provenance_label: "manual.replay".to_string(),
            },
            source_subject: ReplaySubjectRef::new("player:blue:0"),
            source_raw_state_window_ref: RawStateWindowRef::new("window-1"),
            source_phase_id: 0,
            accepted_reference_variant_id: LowBoostRecoveryVariantId::new(
                "slice-1:candidate_recovery_window:trim_start_1",
            ),
            observation_binding_kind:
                LowBoostRecoveryBcObservationBindingKindV1::AcceptedReferenceWindowFromRawStateWindowRef,
            supervision_window_role:
                LowBoostRecoveryBcSupervisionWindowRoleV1::AcceptedReferenceVariantWindow,
            accepted_reference_window: TimeWindow {
                start: FrameIndex::new(121),
                end_exclusive: FrameIndex::new(180),
            },
            target_binding_kind:
                LowBoostRecoveryBcTargetBindingKindV1::AcceptedReferenceVariantControlTargetDeferred,
            carried_confidence_band: LowBoostRecoveryConfidenceBandV1::BoundaryStable,
            carried_unresolved_assumptions: vec![
                LowBoostRecoveryUnresolvedAssumptionV1::LowBoostThresholdUnproven,
                LowBoostRecoveryUnresolvedAssumptionV1::ContactTruthUnproven,
                LowBoostRecoveryUnresolvedAssumptionV1::RecoverySuccessUnproven,
                LowBoostRecoveryUnresolvedAssumptionV1::ReplayOrientationNormalizationDeferred,
                LowBoostRecoveryUnresolvedAssumptionV1::PhysicsReachabilityUnproven,
            ],
        };

        let encoded = serde_json::to_value(&specimen).expect("emitted specimen should serialize");
        let decoded: LowBoostRecoveryBcActualFilesystemEmissionSpecimenFileV1 =
            serde_json::from_value(encoded).expect("emitted specimen should deserialize");

        assert_eq!(decoded, specimen);
    }
}
