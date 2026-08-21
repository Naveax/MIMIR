use mimir_core::{MimirError, Result, hash_serializable, load_json_file};
use mimir_io::{
    ArtifactFormat, read_artifact_auto, read_artifact_header_auto, write_anchor_artifact,
    write_branch_artifact,
};
use mimir_types::{
    AnchorRecord, ArtifactHeader, ArtifactKind, BranchRecord, PersistedAnchorArtifact,
    PersistedBranchArtifact,
};
use serde::{Deserialize, Serialize};
use std::collections::{BTreeMap, BTreeSet};
use std::fs;
use std::path::{Component, Path, PathBuf};
use std::time::{SystemTime, UNIX_EPOCH};

pub const EXPORT_BUNDLE_PRODUCER: &str = "mimir-export";
pub const EXPORT_MANIFEST_VERSION: u32 = 1;
pub const EXPORT_INDEX_VERSION: u32 = 1;
pub const EXPORT_MANIFEST_FILE_NAME: &str = "manifest.json";
pub const EXPORT_INDEX_FILE_NAME: &str = "index.json";
pub const EXECUTION_RESULT_STUB_VERSION: u32 = 1;
pub const EXECUTION_LEDGER_INDEX_VERSION: u32 = 1;
pub const EXECUTION_LEDGER_DIR_NAME: &str = "ledger";
pub const EXECUTION_LEDGER_RESULTS_DIR_NAME: &str = "results";
pub const EXECUTION_LEDGER_INDEX_FILE_NAME: &str = "index.json";
pub const EXECUTION_RESULT_JOB_REPORT_INDEX_VERSION: u32 = 1;
pub const EXECUTION_RESULT_JOB_REPORT_COLLECTION_SUMMARY_INDEX_VERSION: u32 = 1;

#[derive(Debug, Clone, Copy, Serialize, Deserialize, PartialEq, Eq)]
#[serde(rename_all = "snake_case")]
pub enum ExportEncoding {
    Json,
    Toml,
}

impl ExportEncoding {
    pub const fn as_artifact_format(self) -> ArtifactFormat {
        match self {
            Self::Json => ArtifactFormat::Json,
            Self::Toml => ArtifactFormat::Toml,
        }
    }

    pub const fn extension(self) -> &'static str {
        match self {
            Self::Json => "json",
            Self::Toml => "toml",
        }
    }
}

#[derive(Debug, Clone, PartialEq)]
pub struct ExportBundleInput {
    pub export_name: String,
    pub artifact_encoding: ExportEncoding,
    pub anchor_artifacts: Vec<PersistedAnchorArtifact>,
    pub branch_artifacts: Vec<PersistedBranchArtifact>,
    pub created_by_component: Option<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct ExportManifest {
    pub manifest_version: u32,
    pub export_name: String,
    pub producer: String,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub created_by_component: Option<String>,
    pub artifact_encoding: ExportEncoding,
    pub relative_index_path: String,
    pub artifact_count: usize,
    pub anchor_count: usize,
    pub branch_count: usize,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct ExportIndex {
    pub index_version: u32,
    pub entries: Vec<ExportIndexEntry>,
}

#[derive(Debug, Clone, Copy, Serialize, Deserialize, PartialEq, Eq)]
#[serde(rename_all = "snake_case")]
pub enum ExportArtifactKind {
    Anchor,
    Branch,
}

impl ExportArtifactKind {
    pub const fn schema_name(self) -> &'static str {
        match self {
            Self::Anchor => ArtifactKind::Anchor.schema().name,
            Self::Branch => ArtifactKind::Branch.schema().name,
        }
    }

    pub const fn schema_version(self) -> u32 {
        match self {
            Self::Anchor => ArtifactKind::Anchor.schema().version,
            Self::Branch => ArtifactKind::Branch.schema().version,
        }
    }

    pub const fn relative_directory(self) -> &'static str {
        match self {
            Self::Anchor => "anchors",
            Self::Branch => "branches",
        }
    }

    pub const fn file_stem(self) -> &'static str {
        match self {
            Self::Anchor => "anchor",
            Self::Branch => "branch",
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct ExportIndexEntry {
    pub artifact_kind: ExportArtifactKind,
    pub record_id: String,
    pub relative_path: String,
    pub schema_name: String,
    pub schema_version: u32,
    pub content_hash: String,
}

#[derive(Debug, Clone, PartialEq)]
pub struct ExportInspection {
    pub manifest: ExportManifest,
    pub index: ExportIndex,
    pub artifacts: Vec<InspectedArtifact>,
}

#[derive(Debug, Clone, PartialEq)]
pub struct InspectedArtifact {
    pub entry: ExportIndexEntry,
    pub header: ArtifactHeader,
}

#[derive(Debug, Clone, PartialEq)]
pub struct LoadedExportBundle {
    pub manifest: ExportManifest,
    pub index: ExportIndex,
    pub anchor_artifacts: Vec<PersistedAnchorArtifact>,
    pub branch_artifacts: Vec<PersistedBranchArtifact>,
}

impl LoadedExportBundle {
    pub fn into_consumer_export(self) -> ConsumerExport {
        ConsumerExport {
            manifest: self.manifest,
            anchors: self
                .anchor_artifacts
                .into_iter()
                .map(|artifact| artifact.payload)
                .collect(),
            branches: self
                .branch_artifacts
                .into_iter()
                .map(|artifact| artifact.payload)
                .collect(),
        }
    }
}

#[derive(Debug, Clone, PartialEq)]
pub struct ConsumerExport {
    pub manifest: ExportManifest,
    pub anchors: Vec<AnchorRecord>,
    pub branches: Vec<BranchRecord>,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(tag = "mode", content = "ids", rename_all = "snake_case")]
pub enum CandidateSelection {
    All,
    Explicit(Vec<String>),
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct CandidateRequest {
    pub request_id: String,
    pub export_name: String,
    pub anchor_selection: CandidateSelection,
    pub branch_selection: CandidateSelection,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub created_by_component: Option<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct ProcessingPlan {
    pub plan_id: String,
    pub request: CandidateRequest,
    #[serde(default, skip_serializing_if = "Vec::is_empty")]
    pub selected_anchor_ids: Vec<String>,
    #[serde(default, skip_serializing_if = "Vec::is_empty")]
    pub selected_branch_ids: Vec<String>,
    #[serde(default, skip_serializing_if = "Vec::is_empty")]
    pub missing_anchor_ids: Vec<String>,
    #[serde(default, skip_serializing_if = "Vec::is_empty")]
    pub missing_branch_ids: Vec<String>,
    #[serde(default, skip_serializing_if = "Vec::is_empty")]
    pub unresolved_branch_anchor_ids: Vec<String>,
}

#[derive(Debug, Clone, Copy, Serialize, Deserialize, PartialEq, Eq)]
#[serde(rename_all = "snake_case")]
pub enum ExecutionResultStatus {
    StubbedSuccess,
    StubbedFailure,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct ExecutionResultStub {
    pub execution_result_version: u32,
    pub result_id: String,
    pub recorded_at_unix_ms: u64,
    pub plan: ProcessingPlan,
    pub status: ExecutionResultStatus,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub detail: Option<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct ExecutionLedgerIndex {
    pub ledger_index_version: u32,
    pub entries: Vec<ExecutionLedgerIndexEntry>,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct ExecutionLedgerIndexEntry {
    pub result_id: String,
    pub request_id: String,
    pub plan_id: String,
    pub export_name: String,
    pub status: ExecutionResultStatus,
    pub recorded_at_unix_ms: u64,
    pub relative_result_path: String,
    pub content_hash: String,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ExecutionLedgerHistory {
    pub export_name: String,
    pub index: ExecutionLedgerIndex,
    pub entries: Vec<ExecutionLedgerHistoryEntry>,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ExecutionLedgerHistoryEntry {
    pub index_entry: ExecutionLedgerIndexEntry,
    pub result: ExecutionResultStub,
}

#[derive(Debug, Clone, Default, PartialEq, Eq)]
pub struct LedgerSelectionQuery {
    pub result_id: Option<String>,
    pub request_id: Option<String>,
    pub plan_id: Option<String>,
    pub export_name: Option<String>,
    pub status: Option<ExecutionResultStatus>,
    pub anchor_id: Option<String>,
    pub branch_id: Option<String>,
}

#[derive(Debug, Clone, Copy, Serialize, Deserialize, PartialEq, Eq)]
#[serde(rename_all = "snake_case")]
pub enum ExecutionResultSelectionMode {
    FullHistory,
    LatestOnly,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct ExecutionResultHandoffBundle {
    pub handoff_bundle_id: String,
    pub export_name: String,
    pub selection_mode: ExecutionResultSelectionMode,
    pub entry_count: usize,
    pub provenance_hash: String,
    pub entries: Vec<ExecutionResultHandoffEntry>,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct ExecutionResultHandoffEntry {
    pub ordinal: usize,
    pub result_id: String,
    pub request_id: String,
    pub plan_id: String,
    pub status: ExecutionResultStatus,
    pub recorded_at_unix_ms: u64,
    #[serde(default, skip_serializing_if = "Vec::is_empty")]
    pub selected_anchor_ids: Vec<String>,
    #[serde(default, skip_serializing_if = "Vec::is_empty")]
    pub selected_branch_ids: Vec<String>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub detail: Option<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct ExecutionResultRunRequest {
    pub run_request_id: String,
    pub source_handoff_bundle_id: String,
    pub export_name: String,
    pub selection_mode: ExecutionResultSelectionMode,
    pub expected_entry_count: usize,
    pub source_provenance_hash: String,
    pub entries: Vec<ExecutionResultRunRequestEntry>,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct ExecutionResultRunRequestEntry {
    pub ordinal: usize,
    pub result_id: String,
    pub request_id: String,
    pub plan_id: String,
    pub status: ExecutionResultStatus,
    pub recorded_at_unix_ms: u64,
    #[serde(default, skip_serializing_if = "Vec::is_empty")]
    pub selected_anchor_ids: Vec<String>,
    #[serde(default, skip_serializing_if = "Vec::is_empty")]
    pub selected_branch_ids: Vec<String>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub detail: Option<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct ExecutionResultJobSpec {
    pub job_spec_id: String,
    pub source_run_request_id: String,
    pub source_handoff_bundle_id: String,
    pub export_name: String,
    pub selection_mode: ExecutionResultSelectionMode,
    pub expected_entry_count: usize,
    pub source_provenance_hash: String,
    pub entries: Vec<ExecutionResultJobSpecEntry>,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct ExecutionResultJobSpecEntry {
    pub ordinal: usize,
    pub result_id: String,
    pub request_id: String,
    pub plan_id: String,
    pub status: ExecutionResultStatus,
    pub recorded_at_unix_ms: u64,
    #[serde(default, skip_serializing_if = "Vec::is_empty")]
    pub selected_anchor_ids: Vec<String>,
    #[serde(default, skip_serializing_if = "Vec::is_empty")]
    pub selected_branch_ids: Vec<String>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub detail: Option<String>,
}

pub trait ExecutionResultJobExecutor {
    fn execute(&self, job_spec: &ExecutionResultJobSpec) -> Result<ExecutionResultJobReport>;
}

#[derive(Debug, Default, Clone, Copy, PartialEq, Eq)]
pub struct StubExecutionResultJobExecutor;

const STUB_EXECUTION_RESULT_JOB_REPORT_STATUS: ExecutionResultJobReportStatus =
    ExecutionResultJobReportStatus::StubAccepted;

impl ExecutionResultJobExecutor for StubExecutionResultJobExecutor {
    fn execute(&self, job_spec: &ExecutionResultJobSpec) -> Result<ExecutionResultJobReport> {
        validate_execution_result_job_spec(job_spec)?;

        let report = ExecutionResultJobReport {
            job_spec_id: job_spec.job_spec_id.clone(),
            source_run_request_id: job_spec.source_run_request_id.clone(),
            source_handoff_bundle_id: job_spec.source_handoff_bundle_id.clone(),
            export_name: job_spec.export_name.clone(),
            selection_mode: job_spec.selection_mode,
            expected_entry_count: job_spec.expected_entry_count,
            source_provenance_hash: job_spec.source_provenance_hash.clone(),
            entries: job_spec
                .entries
                .iter()
                .map(|entry| ExecutionResultJobReportEntry {
                    ordinal: entry.ordinal,
                    result_id: entry.result_id.clone(),
                    request_id: entry.request_id.clone(),
                    plan_id: entry.plan_id.clone(),
                    stub_status: STUB_EXECUTION_RESULT_JOB_REPORT_STATUS,
                })
                .collect(),
        };
        validate_execution_result_job_report(&report)?;

        Ok(report)
    }
}

#[derive(Debug, Clone, Copy, Serialize, Deserialize, PartialEq, Eq)]
#[serde(rename_all = "snake_case")]
pub enum ExecutionResultJobReportStatus {
    Ready,
    StubAccepted,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct ExecutionResultJobReport {
    pub job_spec_id: String,
    pub source_run_request_id: String,
    pub source_handoff_bundle_id: String,
    pub export_name: String,
    pub selection_mode: ExecutionResultSelectionMode,
    pub expected_entry_count: usize,
    pub source_provenance_hash: String,
    pub entries: Vec<ExecutionResultJobReportEntry>,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct ExecutionResultJobReportIndex {
    pub index_version: u32,
    pub entries: Vec<ExecutionResultJobReportIndexEntry>,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct ExecutionResultJobReportIndexEntry {
    pub ordinal: usize,
    pub report_file_path: String,
    pub job_spec_id: String,
    pub source_run_request_id: String,
    pub source_handoff_bundle_id: String,
    pub export_name: String,
    pub selection_mode: ExecutionResultSelectionMode,
    pub expected_entry_count: usize,
    pub source_provenance_hash: String,
}

#[derive(Debug, Clone, Default, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct ExecutionResultJobReportIndexQuery {
    pub job_spec_id: Option<String>,
    pub report_file_path: Option<String>,
    pub export_name: Option<String>,
    pub selection_mode: Option<ExecutionResultSelectionMode>,
    pub source_run_request_id: Option<String>,
    pub source_handoff_bundle_id: Option<String>,
    pub source_provenance_hash: Option<String>,
    pub latest_only: bool,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ExecutionResultJobReportIndexSelectionSummary {
    pub query: ExecutionResultJobReportIndexQuery,
    pub selected_entry_count: usize,
    pub selected_entries: Vec<ExecutionResultJobReportIndexEntry>,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct ExecutionResultJobReportCollectionSummary {
    pub report_count: usize,
    pub total_entry_count: usize,
    pub job_spec_ids: Vec<String>,
    pub export_names: Vec<String>,
    pub selection_modes: Vec<ExecutionResultSelectionMode>,
    pub source_run_request_ids: Vec<String>,
    pub source_handoff_bundle_ids: Vec<String>,
    pub shared_export_name: Option<String>,
    pub shared_selection_mode: Option<ExecutionResultSelectionMode>,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct ExecutionResultJobReportCollectionSummaryIndex {
    pub index_version: u32,
    pub entries: Vec<ExecutionResultJobReportCollectionSummaryIndexEntry>,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct ExecutionResultJobReportCollectionSummaryIndexEntry {
    pub ordinal: usize,
    pub summary_file_path: String,
    pub report_count: usize,
    pub total_entry_count: usize,
    pub job_spec_ids: Vec<String>,
    pub export_names: Vec<String>,
    pub selection_modes: Vec<ExecutionResultSelectionMode>,
    pub source_run_request_ids: Vec<String>,
    pub source_handoff_bundle_ids: Vec<String>,
}

#[derive(Debug, Clone, Default, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct ExecutionResultJobReportCollectionSummaryIndexQuery {
    pub summary_file_path: Option<String>,
    pub report_count: Option<usize>,
    pub total_entry_count: Option<usize>,
    pub export_names: Vec<String>,
    pub selection_modes: Vec<ExecutionResultSelectionMode>,
    pub source_run_request_ids: Vec<String>,
    pub source_handoff_bundle_ids: Vec<String>,
    pub latest_only: bool,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ExecutionResultJobReportCollectionSummaryIndexSelectionSummary {
    pub query: ExecutionResultJobReportCollectionSummaryIndexQuery,
    pub selected_entry_count: usize,
    pub selected_entries: Vec<ExecutionResultJobReportCollectionSummaryIndexEntry>,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct ExecutionResultJobReportEntry {
    pub ordinal: usize,
    pub result_id: String,
    pub request_id: String,
    pub plan_id: String,
    pub stub_status: ExecutionResultJobReportStatus,
}

pub fn validate_execution_result_job_report(report: &ExecutionResultJobReport) -> Result<()> {
    validate_identifier("execution result job spec id", &report.job_spec_id)?;
    validate_identifier(
        "execution result run request id",
        &report.source_run_request_id,
    )?;
    validate_identifier(
        "execution result handoff bundle id",
        &report.source_handoff_bundle_id,
    )?;
    validate_identifier("execution result export name", &report.export_name)?;
    validate_identifier(
        "execution result job report provenance hash",
        &report.source_provenance_hash,
    )?;

    if report.expected_entry_count != report.entries.len() {
        return Err(MimirError::message(format!(
            "execution result job report entry count drift: expected {}, found {}",
            report.expected_entry_count,
            report.entries.len()
        )));
    }

    for (expected_ordinal, entry) in report.entries.iter().enumerate() {
        validate_execution_result_job_report_entry(entry, expected_ordinal)?;
    }

    Ok(())
}

pub fn validate_execution_result_job_report_entry(
    entry: &ExecutionResultJobReportEntry,
    expected_ordinal: usize,
) -> Result<()> {
    validate_pipeline_ordinal(
        "job report",
        &entry.result_id,
        entry.ordinal,
        expected_ordinal,
    )?;
    validate_identifier("execution result id", &entry.result_id)?;
    validate_identifier("candidate request id", &entry.request_id)?;
    validate_identifier("processing plan id", &entry.plan_id)?;

    Ok(())
}

pub fn validate_execution_result_job_report_index(
    index: &ExecutionResultJobReportIndex,
) -> Result<()> {
    if index.index_version != EXECUTION_RESULT_JOB_REPORT_INDEX_VERSION {
        return Err(MimirError::message(format!(
            "unsupported execution result job report index version {}",
            index.index_version
        )));
    }

    let mut seen_report_file_paths = BTreeSet::new();
    let mut seen_job_spec_ids = BTreeSet::new();

    for (expected_ordinal, entry) in index.entries.iter().enumerate() {
        validate_execution_result_job_report_index_entry(entry, expected_ordinal)?;

        if !seen_report_file_paths.insert(entry.report_file_path.clone()) {
            return Err(MimirError::message(format!(
                "duplicate execution result job report path {} in index",
                entry.report_file_path
            )));
        }

        if !seen_job_spec_ids.insert(entry.job_spec_id.clone()) {
            return Err(MimirError::message(format!(
                "duplicate execution result job spec id {} in index",
                entry.job_spec_id
            )));
        }
    }

    Ok(())
}

pub fn validate_execution_result_job_report_index_entry(
    entry: &ExecutionResultJobReportIndexEntry,
    expected_ordinal: usize,
) -> Result<()> {
    validate_pipeline_ordinal(
        "execution result job report index",
        &entry.job_spec_id,
        entry.ordinal,
        expected_ordinal,
    )?;
    validate_non_empty_file_path(
        "execution result job report file path",
        &entry.report_file_path,
    )?;
    validate_identifier("execution result job spec id", &entry.job_spec_id)?;
    validate_identifier(
        "execution result run request id",
        &entry.source_run_request_id,
    )?;
    validate_identifier(
        "execution result handoff bundle id",
        &entry.source_handoff_bundle_id,
    )?;
    validate_identifier("execution result export name", &entry.export_name)?;
    validate_identifier(
        "execution result job report provenance hash",
        &entry.source_provenance_hash,
    )?;

    Ok(())
}

pub fn validate_execution_result_job_report_index_query(
    query: &ExecutionResultJobReportIndexQuery,
) -> Result<()> {
    if let Some(job_spec_id) = &query.job_spec_id {
        validate_identifier("execution result job spec id query", job_spec_id)?;
    }

    if let Some(report_file_path) = &query.report_file_path {
        validate_non_empty_file_path(
            "execution result job report file path query",
            report_file_path,
        )?;
    }

    if let Some(export_name) = &query.export_name {
        validate_identifier("execution result export name query", export_name)?;
    }

    if let Some(source_run_request_id) = &query.source_run_request_id {
        validate_identifier(
            "execution result run request id query",
            source_run_request_id,
        )?;
    }

    if let Some(source_handoff_bundle_id) = &query.source_handoff_bundle_id {
        validate_identifier(
            "execution result handoff bundle id query",
            source_handoff_bundle_id,
        )?;
    }

    if let Some(source_provenance_hash) = &query.source_provenance_hash {
        validate_identifier(
            "execution result job report provenance hash query",
            source_provenance_hash,
        )?;
    }

    Ok(())
}

pub fn validate_execution_result_job_report_collection_summary(
    summary: &ExecutionResultJobReportCollectionSummary,
) -> Result<()> {
    validate_identifier_list(
        "execution result job report collection summary job spec id",
        &summary.job_spec_ids,
    )?;
    validate_identifier_list(
        "execution result job report collection summary export name",
        &summary.export_names,
    )?;
    validate_identifier_list(
        "execution result job report collection summary source run request id",
        &summary.source_run_request_ids,
    )?;
    validate_identifier_list(
        "execution result job report collection summary source handoff bundle id",
        &summary.source_handoff_bundle_ids,
    )?;
    validate_unique_selection_modes(
        "execution result job report collection summary selection mode",
        &summary.selection_modes,
    )?;

    if summary.report_count == 0 {
        if !summary.job_spec_ids.is_empty()
            || !summary.export_names.is_empty()
            || !summary.selection_modes.is_empty()
            || !summary.source_run_request_ids.is_empty()
            || !summary.source_handoff_bundle_ids.is_empty()
            || summary.shared_export_name.is_some()
            || summary.shared_selection_mode.is_some()
        {
            return Err(MimirError::message(
                "execution result job report collection summary with zero reports must not carry populated fields",
            ));
        }

        return Ok(());
    }

    if summary.job_spec_ids.is_empty()
        || summary.export_names.is_empty()
        || summary.selection_modes.is_empty()
        || summary.source_run_request_ids.is_empty()
        || summary.source_handoff_bundle_ids.is_empty()
    {
        return Err(MimirError::message(
            "execution result job report collection summary with reports must include non-empty summary collections",
        ));
    }

    if let Some(shared_export_name) = &summary.shared_export_name {
        validate_identifier(
            "execution result job report collection summary shared export name",
            shared_export_name,
        )?;
        if !summary
            .export_names
            .iter()
            .any(|name| name == shared_export_name)
        {
            return Err(MimirError::message(format!(
                "execution result job report collection summary shared export name {shared_export_name} must appear in export_names"
            )));
        }
    }

    if let Some(shared_selection_mode) = summary.shared_selection_mode {
        if !summary.selection_modes.contains(&shared_selection_mode) {
            return Err(MimirError::message(format!(
                "execution result job report collection summary shared selection mode {:?} must appear in selection_modes",
                shared_selection_mode
            )));
        }
    }

    Ok(())
}

pub fn validate_execution_result_job_report_collection_summary_index(
    index: &ExecutionResultJobReportCollectionSummaryIndex,
) -> Result<()> {
    if index.index_version != EXECUTION_RESULT_JOB_REPORT_COLLECTION_SUMMARY_INDEX_VERSION {
        return Err(MimirError::message(format!(
            "unsupported execution result job report collection summary index version {}",
            index.index_version
        )));
    }

    let mut seen_summary_file_paths = BTreeSet::new();

    for (expected_ordinal, entry) in index.entries.iter().enumerate() {
        validate_execution_result_job_report_collection_summary_index_entry(
            entry,
            expected_ordinal,
        )?;

        if !seen_summary_file_paths.insert(entry.summary_file_path.clone()) {
            return Err(MimirError::message(format!(
                "duplicate execution result job report collection summary path {} in index",
                entry.summary_file_path
            )));
        }
    }

    Ok(())
}

pub fn validate_execution_result_job_report_collection_summary_index_entry(
    entry: &ExecutionResultJobReportCollectionSummaryIndexEntry,
    expected_ordinal: usize,
) -> Result<()> {
    validate_pipeline_ordinal(
        "execution result job report collection summary index",
        &entry.summary_file_path,
        entry.ordinal,
        expected_ordinal,
    )?;
    validate_non_empty_file_path(
        "execution result job report collection summary file path",
        &entry.summary_file_path,
    )?;
    validate_identifier_list(
        "execution result job report collection summary index job spec id",
        &entry.job_spec_ids,
    )?;
    validate_identifier_list(
        "execution result job report collection summary index export name",
        &entry.export_names,
    )?;
    validate_unique_selection_modes(
        "execution result job report collection summary index selection mode",
        &entry.selection_modes,
    )?;
    validate_identifier_list(
        "execution result job report collection summary index source run request id",
        &entry.source_run_request_ids,
    )?;
    validate_identifier_list(
        "execution result job report collection summary index source handoff bundle id",
        &entry.source_handoff_bundle_ids,
    )?;

    if entry.report_count == 0 {
        if entry.total_entry_count != 0
            || !entry.job_spec_ids.is_empty()
            || !entry.export_names.is_empty()
            || !entry.selection_modes.is_empty()
            || !entry.source_run_request_ids.is_empty()
            || !entry.source_handoff_bundle_ids.is_empty()
        {
            return Err(MimirError::message(
                "execution result job report collection summary index entry with zero reports must not carry populated fields",
            ));
        }

        return Ok(());
    }

    if entry.total_entry_count == 0 {
        return Err(MimirError::message(
            "execution result job report collection summary index entry with reports must have a non-zero total_entry_count",
        ));
    }

    if entry.job_spec_ids.is_empty()
        || entry.export_names.is_empty()
        || entry.selection_modes.is_empty()
        || entry.source_run_request_ids.is_empty()
        || entry.source_handoff_bundle_ids.is_empty()
    {
        return Err(MimirError::message(
            "execution result job report collection summary index entry with reports must include non-empty summary collections",
        ));
    }

    Ok(())
}

pub fn validate_execution_result_job_report_collection_summary_index_query(
    query: &ExecutionResultJobReportCollectionSummaryIndexQuery,
) -> Result<()> {
    if let Some(summary_file_path) = &query.summary_file_path {
        validate_non_empty_file_path(
            "execution result job report collection summary file path query",
            summary_file_path,
        )?;
    }

    validate_identifier_list(
        "execution result job report collection summary index export name query",
        &query.export_names,
    )?;
    validate_unique_selection_modes(
        "execution result job report collection summary index selection mode query",
        &query.selection_modes,
    )?;
    validate_identifier_list(
        "execution result job report collection summary index source run request id query",
        &query.source_run_request_ids,
    )?;
    validate_identifier_list(
        "execution result job report collection summary index source handoff bundle id query",
        &query.source_handoff_bundle_ids,
    )?;

    Ok(())
}

/// Canonical report persistence boundary for validated execution-result job reports.
/// Use this when new code needs to publish one validated execution-result job report to disk.
/// Canonical report publication lane: [`persist_execution_result_job_report`] +
/// [`register_execution_result_job_report_in_index`] +
/// [`load_indexed_execution_result_job_report`].
pub fn persist_execution_result_job_report(
    report_path: impl AsRef<Path>,
    report: &ExecutionResultJobReport,
) -> Result<()> {
    let report_path = report_path.as_ref();
    validate_execution_result_job_report(report)?;
    write_json_file(report_path, report)?;
    let _reloaded_report = load_execution_result_job_report(report_path)?;

    Ok(())
}

/// Canonical report load boundary; reloads persisted reports and revalidates them.
/// Use this when new code already has an explicit report path and needs the authoritative file.
pub fn load_execution_result_job_report(
    report_path: impl AsRef<Path>,
) -> Result<ExecutionResultJobReport> {
    let report_path = report_path.as_ref();
    let report: ExecutionResultJobReport = load_json_file(report_path)?;
    validate_execution_result_job_report(&report)?;

    Ok(report)
}

/// Canonical summary persistence boundary for validated report collection summaries.
/// Use this when new code needs to publish one validated summary to disk.
/// Canonical summary publication lane: [`persist_execution_result_job_report_collection_summary`] +
/// [`register_execution_result_job_report_collection_summary_in_index`] +
/// [`load_indexed_execution_result_job_report_collection_summary`].
pub fn persist_execution_result_job_report_collection_summary(
    summary_path: impl AsRef<Path>,
    summary: &ExecutionResultJobReportCollectionSummary,
) -> Result<()> {
    let summary_path = summary_path.as_ref();
    validate_execution_result_job_report_collection_summary(summary)?;
    write_json_file(summary_path, summary)?;
    let _reloaded_summary = load_execution_result_job_report_collection_summary(summary_path)?;

    Ok(())
}

/// Canonical summary load boundary; reloads persisted summaries and revalidates them.
/// Use this when new code already has an explicit summary path and needs the authoritative file.
pub fn load_execution_result_job_report_collection_summary(
    summary_path: impl AsRef<Path>,
) -> Result<ExecutionResultJobReportCollectionSummary> {
    let summary_path = summary_path.as_ref();
    let summary: ExecutionResultJobReportCollectionSummary = load_json_file(summary_path)?;
    validate_execution_result_job_report_collection_summary(&summary)?;

    Ok(summary)
}

/// Canonical summary-index persistence boundary for validated summary index entries.
/// Preferred supported surface for new summary-index persistence composition.
pub fn persist_execution_result_job_report_collection_summary_index(
    index_path: impl AsRef<Path>,
    index: &ExecutionResultJobReportCollectionSummaryIndex,
) -> Result<()> {
    let index_path = index_path.as_ref();
    validate_execution_result_job_report_collection_summary_index(index)?;
    write_json_file_staged(index_path, index)?;
    let _reloaded_index = load_execution_result_job_report_collection_summary_index(index_path)?;

    Ok(())
}

/// Canonical summary-index load boundary; reloads and validates the persisted summary index.
/// Preferred supported surface for new summary-index reload composition.
pub fn load_execution_result_job_report_collection_summary_index(
    index_path: impl AsRef<Path>,
) -> Result<ExecutionResultJobReportCollectionSummaryIndex> {
    let index_path = index_path.as_ref();
    let index: ExecutionResultJobReportCollectionSummaryIndex = load_json_file(index_path)?;
    validate_execution_result_job_report_collection_summary_index(&index)?;

    Ok(index)
}

pub fn find_execution_result_job_report_collection_summary_index_entry_by_summary_file_path<'a>(
    index: &'a ExecutionResultJobReportCollectionSummaryIndex,
    summary_file_path: &str,
) -> Option<&'a ExecutionResultJobReportCollectionSummaryIndexEntry> {
    index
        .entries
        .iter()
        .find(|entry| entry.summary_file_path == summary_file_path)
}

pub fn find_execution_result_job_report_collection_summary_index_entry_by_report_count(
    index: &ExecutionResultJobReportCollectionSummaryIndex,
    report_count: usize,
) -> Option<&ExecutionResultJobReportCollectionSummaryIndexEntry> {
    index
        .entries
        .iter()
        .find(|entry| entry.report_count == report_count)
}

pub fn select_execution_result_job_report_collection_summary_index_entries<'a>(
    index: &'a ExecutionResultJobReportCollectionSummaryIndex,
    query: &ExecutionResultJobReportCollectionSummaryIndexQuery,
) -> Result<Vec<&'a ExecutionResultJobReportCollectionSummaryIndexEntry>> {
    validate_execution_result_job_report_collection_summary_index(index)?;
    validate_execution_result_job_report_collection_summary_index_query(query)?;

    let mut selected = index
        .entries
        .iter()
        .filter(|entry| {
            execution_result_job_report_collection_summary_index_entry_matches_query(entry, query)
        })
        .collect::<Vec<_>>();

    if query.latest_only {
        selected = selected.into_iter().rev().take(1).collect::<Vec<_>>();
        selected.reverse();
    }

    Ok(selected)
}

pub fn latest_execution_result_job_report_collection_summary_index_entry<'a>(
    index: &'a ExecutionResultJobReportCollectionSummaryIndex,
    query: &ExecutionResultJobReportCollectionSummaryIndexQuery,
) -> Result<Option<&'a ExecutionResultJobReportCollectionSummaryIndexEntry>> {
    validate_execution_result_job_report_collection_summary_index(index)?;
    validate_execution_result_job_report_collection_summary_index_query(query)?;

    Ok(index.entries.iter().rfind(|entry| {
        execution_result_job_report_collection_summary_index_entry_matches_query(entry, query)
    }))
}

/// Canonical summary-index query boundary over an already loaded summary index.
/// Use this when new code owns the loaded summary index and wants deterministic selection only.
pub fn query_execution_result_job_report_collection_summary_index(
    index: &ExecutionResultJobReportCollectionSummaryIndex,
    query: &ExecutionResultJobReportCollectionSummaryIndexQuery,
) -> Result<ExecutionResultJobReportCollectionSummaryIndexSelectionSummary> {
    let selected_entries =
        select_execution_result_job_report_collection_summary_index_entries(index, query)?
            .into_iter()
            .cloned()
            .collect::<Vec<_>>();

    Ok(
        ExecutionResultJobReportCollectionSummaryIndexSelectionSummary {
            query: query.clone(),
            selected_entry_count: selected_entries.len(),
            selected_entries,
        },
    )
}

/// Canonical summary-index access boundary that loads and queries the persisted summary index.
/// Use this when new code needs canonical summary retrieval starting from an index path and query.
pub fn load_and_query_execution_result_job_report_collection_summary_index(
    index_path: impl AsRef<Path>,
    query: &ExecutionResultJobReportCollectionSummaryIndexQuery,
) -> Result<ExecutionResultJobReportCollectionSummaryIndexSelectionSummary> {
    let index = load_execution_result_job_report_collection_summary_index(index_path)?;
    query_execution_result_job_report_collection_summary_index(&index, query)
}

/// Canonical summary load boundary from selected summary-index entries.
/// Use this when new code already has validated selected summary-index entries to reload.
pub fn load_selected_execution_result_job_report_collection_summaries(
    selected_entries: &[ExecutionResultJobReportCollectionSummaryIndexEntry],
) -> Result<Vec<ExecutionResultJobReportCollectionSummary>> {
    selected_entries
        .iter()
        .map(|entry| {
            validate_execution_result_job_report_collection_summary_index_entry(
                entry,
                entry.ordinal,
            )?;
            load_execution_result_job_report_collection_summary(Path::new(&entry.summary_file_path))
        })
        .collect()
}

/// Canonical summary retrieval boundary that composes summary-index load/query with selected-summary loads.
/// Canonical summary retrieval lane for new code:
/// [`load_and_query_execution_result_job_report_collection_summaries`].
pub fn load_and_query_execution_result_job_report_collection_summaries(
    index_path: impl AsRef<Path>,
    query: &ExecutionResultJobReportCollectionSummaryIndexQuery,
) -> Result<Vec<ExecutionResultJobReportCollectionSummary>> {
    let selection_summary =
        load_and_query_execution_result_job_report_collection_summary_index(index_path, query)?;
    load_selected_execution_result_job_report_collection_summaries(
        &selection_summary.selected_entries,
    )
}

/// Canonical summary aggregation boundary over queried persisted collection summaries.
/// Canonical summary retrieval and aggregation lane for new code:
/// [`load_query_and_aggregate_execution_result_job_report_collection_summaries`].
pub fn load_query_and_aggregate_execution_result_job_report_collection_summaries(
    index_path: impl AsRef<Path>,
    query: &ExecutionResultJobReportCollectionSummaryIndexQuery,
) -> Result<ExecutionResultJobReportCollectionSummary> {
    let loaded_summaries =
        load_and_query_execution_result_job_report_collection_summaries(index_path, query)?;

    Ok(summarize_execution_result_job_report_collection_summaries(
        &loaded_summaries,
    ))
}

/// Higher-level convenience composition over canonical summary query/load/aggregate helpers.
/// Retained for compatibility as a composition-only convenience wrapper.
/// Prefer canonical lower-level helpers for new work.
/// Candidate for future compatibility cleanup in a dedicated breaking-change pass.
pub fn load_query_summarize_and_persist_execution_result_job_report_collection_summary(
    index_path: impl AsRef<Path>,
    query: &ExecutionResultJobReportCollectionSummaryIndexQuery,
    output_summary_path: impl AsRef<Path>,
) -> Result<ExecutionResultJobReportCollectionSummary> {
    let loaded_summaries =
        load_and_query_execution_result_job_report_collection_summaries(index_path, query)?;
    let aggregate_summary =
        summarize_execution_result_job_report_collection_summaries(&loaded_summaries);

    persist_execution_result_job_report_collection_summary(
        output_summary_path,
        &aggregate_summary,
    )?;

    Ok(aggregate_summary)
}

/// Higher-level convenience composition over canonical summary persist/register helpers.
/// Retained for compatibility; prefer canonical lower-level helpers for new compositions.
pub fn load_query_summarize_persist_and_register_execution_result_job_report_collection_summary(
    index_path: impl AsRef<Path>,
    query: &ExecutionResultJobReportCollectionSummaryIndexQuery,
    output_summary_path: impl AsRef<Path>,
) -> Result<ExecutionResultJobReportCollectionSummary> {
    let index_path = index_path.as_ref();
    let output_summary_path = output_summary_path.as_ref();

    let aggregate_summary =
        load_query_summarize_and_persist_execution_result_job_report_collection_summary(
            index_path,
            query,
            output_summary_path,
        )?;
    register_execution_result_job_report_collection_summary_in_index(
        index_path,
        output_summary_path,
        &aggregate_summary,
    )?;

    Ok(aggregate_summary)
}

/// Higher-level convenience composition over canonical summary persist/register/index-load helpers.
/// Retained for compatibility; prefer canonical lower-level helpers for new compositions.
pub fn load_query_summarize_persist_register_and_index_load_execution_result_job_report_collection_summary(
    index_path: impl AsRef<Path>,
    query: &ExecutionResultJobReportCollectionSummaryIndexQuery,
    output_summary_path: impl AsRef<Path>,
) -> Result<ExecutionResultJobReportCollectionSummary> {
    let index_path = index_path.as_ref();
    let output_summary_path = output_summary_path.as_ref();

    load_query_summarize_persist_and_register_execution_result_job_report_collection_summary(
        index_path,
        query,
        output_summary_path,
    )?;

    let output_summary_file_path = path_to_owned_string(output_summary_path)?;

    load_indexed_execution_result_job_report_collection_summary(
        index_path,
        &output_summary_file_path,
    )
}

pub fn load_indexed_execution_result_job_report_collection_summary(
    index_path: impl AsRef<Path>,
    summary_file_path: &str,
) -> Result<ExecutionResultJobReportCollectionSummary> {
    let index = load_execution_result_job_report_collection_summary_index(index_path)?;
    let entry = find_execution_result_job_report_collection_summary_index_entry_by_summary_file_path(
        &index,
        summary_file_path,
    )
    .ok_or_else(|| {
        MimirError::message(format!(
            "execution result job report collection summary index entry not found for summary file path {summary_file_path}"
        ))
    })?;

    load_execution_result_job_report_collection_summary(Path::new(&entry.summary_file_path))
}

pub fn register_execution_result_job_report_collection_summary_in_index(
    index_path: impl AsRef<Path>,
    summary_file_path: impl AsRef<Path>,
    summary: &ExecutionResultJobReportCollectionSummary,
) -> Result<ExecutionResultJobReportCollectionSummaryIndexEntry> {
    let index_path = index_path.as_ref();
    let summary_file_path = summary_file_path.as_ref();
    validate_execution_result_job_report_collection_summary(summary)?;

    let mut index = if index_path.exists() {
        load_execution_result_job_report_collection_summary_index(index_path)?
    } else {
        empty_execution_result_job_report_collection_summary_index()
    };

    let entry = ExecutionResultJobReportCollectionSummaryIndexEntry {
        ordinal: index.entries.len(),
        summary_file_path: path_to_owned_string(summary_file_path)?,
        report_count: summary.report_count,
        total_entry_count: summary.total_entry_count,
        job_spec_ids: summary.job_spec_ids.clone(),
        export_names: summary.export_names.clone(),
        selection_modes: summary.selection_modes.clone(),
        source_run_request_ids: summary.source_run_request_ids.clone(),
        source_handoff_bundle_ids: summary.source_handoff_bundle_ids.clone(),
    };
    validate_execution_result_job_report_collection_summary_index_entry(&entry, entry.ordinal)?;

    index.entries.push(entry.clone());
    persist_execution_result_job_report_collection_summary_index(index_path, &index)?;

    Ok(entry)
}

/// Canonical report-index persistence boundary for validated execution-result job report entries.
/// Preferred supported surface for new report-index persistence composition.
pub fn persist_execution_result_job_report_index(
    index_path: impl AsRef<Path>,
    index: &ExecutionResultJobReportIndex,
) -> Result<()> {
    let index_path = index_path.as_ref();
    validate_execution_result_job_report_index(index)?;
    write_json_file_staged(index_path, index)?;
    let _reloaded_index = load_execution_result_job_report_index(index_path)?;

    Ok(())
}

/// Canonical report-index load boundary; reloads and validates the persisted report index.
/// Preferred supported surface for new report-index reload composition.
pub fn load_execution_result_job_report_index(
    index_path: impl AsRef<Path>,
) -> Result<ExecutionResultJobReportIndex> {
    let index_path = index_path.as_ref();
    let index: ExecutionResultJobReportIndex = load_json_file(index_path)?;
    validate_execution_result_job_report_index(&index)?;

    Ok(index)
}

pub fn find_execution_result_job_report_index_entry_by_job_spec_id<'a>(
    index: &'a ExecutionResultJobReportIndex,
    job_spec_id: &str,
) -> Option<&'a ExecutionResultJobReportIndexEntry> {
    index
        .entries
        .iter()
        .find(|entry| entry.job_spec_id == job_spec_id)
}

pub fn find_execution_result_job_report_index_entry_by_report_path<'a>(
    index: &'a ExecutionResultJobReportIndex,
    report_path: &str,
) -> Option<&'a ExecutionResultJobReportIndexEntry> {
    index
        .entries
        .iter()
        .find(|entry| entry.report_file_path == report_path)
}

pub fn select_execution_result_job_report_index_entries<'a>(
    index: &'a ExecutionResultJobReportIndex,
    query: &ExecutionResultJobReportIndexQuery,
) -> Result<Vec<&'a ExecutionResultJobReportIndexEntry>> {
    validate_execution_result_job_report_index(index)?;
    validate_execution_result_job_report_index_query(query)?;

    let mut selected = index
        .entries
        .iter()
        .filter(|entry| execution_result_job_report_index_entry_matches_query(entry, query))
        .collect::<Vec<_>>();

    if query.latest_only {
        selected = selected.into_iter().rev().take(1).collect::<Vec<_>>();
        selected.reverse();
    }

    Ok(selected)
}

pub fn latest_execution_result_job_report_index_entry<'a>(
    index: &'a ExecutionResultJobReportIndex,
    query: &ExecutionResultJobReportIndexQuery,
) -> Result<Option<&'a ExecutionResultJobReportIndexEntry>> {
    validate_execution_result_job_report_index(index)?;
    validate_execution_result_job_report_index_query(query)?;

    Ok(index
        .entries
        .iter()
        .rfind(|entry| execution_result_job_report_index_entry_matches_query(entry, query)))
}

/// Canonical report-index query boundary over an already loaded report index.
/// Preferred supported surface for new report-index query composition.
pub fn query_execution_result_job_report_index(
    index: &ExecutionResultJobReportIndex,
    query: &ExecutionResultJobReportIndexQuery,
) -> Result<ExecutionResultJobReportIndexSelectionSummary> {
    let selected_entries = select_execution_result_job_report_index_entries(index, query)?
        .into_iter()
        .cloned()
        .collect::<Vec<_>>();

    Ok(ExecutionResultJobReportIndexSelectionSummary {
        query: query.clone(),
        selected_entry_count: selected_entries.len(),
        selected_entries,
    })
}

/// Canonical report-index access boundary that loads and queries the persisted report index.
/// Preferred supported surface for new persisted report-index query composition.
pub fn load_and_query_execution_result_job_report_index(
    index_path: impl AsRef<Path>,
    query: &ExecutionResultJobReportIndexQuery,
) -> Result<ExecutionResultJobReportIndexSelectionSummary> {
    let index = load_execution_result_job_report_index(index_path)?;
    query_execution_result_job_report_index(&index, query)
}

/// Canonical report load boundary from selected report-index entries.
/// Preferred supported surface for new selected-report reload composition.
pub fn load_selected_execution_result_job_reports(
    selected_entries: &[ExecutionResultJobReportIndexEntry],
) -> Result<Vec<ExecutionResultJobReport>> {
    selected_entries
        .iter()
        .map(|entry| {
            validate_execution_result_job_report_index_entry(entry, entry.ordinal)?;
            load_execution_result_job_report(Path::new(&entry.report_file_path))
        })
        .collect()
}

pub fn summarize_execution_result_job_reports(
    reports: &[ExecutionResultJobReport],
) -> ExecutionResultJobReportCollectionSummary {
    let mut job_spec_ids = Vec::new();
    let mut export_names = Vec::new();
    let mut selection_modes = Vec::new();
    let mut source_run_request_ids = Vec::new();
    let mut source_handoff_bundle_ids = Vec::new();

    for report in reports {
        push_unique_string(&mut job_spec_ids, &report.job_spec_id);
        push_unique_string(&mut export_names, &report.export_name);
        push_unique_selection_mode(&mut selection_modes, report.selection_mode);
        push_unique_string(&mut source_run_request_ids, &report.source_run_request_id);
        push_unique_string(
            &mut source_handoff_bundle_ids,
            &report.source_handoff_bundle_id,
        );
    }

    ExecutionResultJobReportCollectionSummary {
        report_count: reports.len(),
        total_entry_count: reports.iter().map(|report| report.entries.len()).sum(),
        shared_export_name: if export_names.len() == 1 {
            export_names.first().cloned()
        } else {
            None
        },
        shared_selection_mode: if selection_modes.len() == 1 {
            selection_modes.first().copied()
        } else {
            None
        },
        job_spec_ids,
        export_names,
        selection_modes,
        source_run_request_ids,
        source_handoff_bundle_ids,
    }
}

pub fn summarize_execution_result_job_report_collection_summaries(
    summaries: &[ExecutionResultJobReportCollectionSummary],
) -> ExecutionResultJobReportCollectionSummary {
    let mut job_spec_ids = Vec::new();
    let mut export_names = Vec::new();
    let mut selection_modes = Vec::new();
    let mut source_run_request_ids = Vec::new();
    let mut source_handoff_bundle_ids = Vec::new();

    for summary in summaries {
        for job_spec_id in &summary.job_spec_ids {
            push_unique_string(&mut job_spec_ids, job_spec_id);
        }
        for export_name in &summary.export_names {
            push_unique_string(&mut export_names, export_name);
        }
        for selection_mode in &summary.selection_modes {
            push_unique_selection_mode(&mut selection_modes, *selection_mode);
        }
        for source_run_request_id in &summary.source_run_request_ids {
            push_unique_string(&mut source_run_request_ids, source_run_request_id);
        }
        for source_handoff_bundle_id in &summary.source_handoff_bundle_ids {
            push_unique_string(&mut source_handoff_bundle_ids, source_handoff_bundle_id);
        }
    }

    ExecutionResultJobReportCollectionSummary {
        report_count: summaries.iter().map(|summary| summary.report_count).sum(),
        total_entry_count: summaries
            .iter()
            .map(|summary| summary.total_entry_count)
            .sum(),
        shared_export_name: if export_names.len() == 1 {
            export_names.first().cloned()
        } else {
            None
        },
        shared_selection_mode: if selection_modes.len() == 1 {
            selection_modes.first().copied()
        } else {
            None
        },
        job_spec_ids,
        export_names,
        selection_modes,
        source_run_request_ids,
        source_handoff_bundle_ids,
    }
}

/// Canonical report retrieval boundary that composes report-index load/query with selected-report loads.
/// Canonical report retrieval lane for new code:
/// [`load_and_query_execution_result_job_reports`].
pub fn load_and_query_execution_result_job_reports(
    index_path: impl AsRef<Path>,
    query: &ExecutionResultJobReportIndexQuery,
) -> Result<Vec<ExecutionResultJobReport>> {
    let selection_summary = load_and_query_execution_result_job_report_index(index_path, query)?;
    load_selected_execution_result_job_reports(&selection_summary.selected_entries)
}

/// Higher-level convenience composition over canonical report query/load and summary publication helpers.
/// Retained for compatibility as a composition-only convenience wrapper.
/// Prefer canonical lower-level helpers for new work.
/// Candidate for future compatibility cleanup in a dedicated breaking-change pass.
pub fn load_query_reports_summarize_persist_register_and_index_load_execution_result_job_report_collection_summary(
    report_index_path: impl AsRef<Path>,
    report_index_query: &ExecutionResultJobReportIndexQuery,
    summary_index_path: impl AsRef<Path>,
    output_summary_path: impl AsRef<Path>,
) -> Result<ExecutionResultJobReportCollectionSummary> {
    let report_index_path = report_index_path.as_ref();
    let summary_index_path = summary_index_path.as_ref();
    let output_summary_path = output_summary_path.as_ref();

    let loaded_reports =
        load_and_query_execution_result_job_reports(report_index_path, report_index_query)?;
    let aggregate_summary = summarize_execution_result_job_reports(&loaded_reports);

    persist_execution_result_job_report_collection_summary(
        output_summary_path,
        &aggregate_summary,
    )?;
    register_execution_result_job_report_collection_summary_in_index(
        summary_index_path,
        output_summary_path,
        &aggregate_summary,
    )?;

    let output_summary_file_path = path_to_owned_string(output_summary_path)?;
    load_indexed_execution_result_job_report_collection_summary(
        summary_index_path,
        &output_summary_file_path,
    )
}

/// Canonical summary publication boundary that persists, registers, and reloads a summary through the summary index.
/// Use this when new code wants one call for the canonical summary publication lane.
pub fn persist_register_and_index_load_execution_result_job_report_collection_summary(
    summary: &ExecutionResultJobReportCollectionSummary,
    summary_path: impl AsRef<Path>,
    summary_index_path: impl AsRef<Path>,
) -> Result<ExecutionResultJobReportCollectionSummary> {
    let summary_path = summary_path.as_ref();
    let summary_index_path = summary_index_path.as_ref();

    persist_execution_result_job_report_collection_summary(summary_path, summary)?;
    register_execution_result_job_report_collection_summary_in_index(
        summary_index_path,
        summary_path,
        summary,
    )?;

    let summary_file_path = path_to_owned_string(summary_path)?;
    load_indexed_execution_result_job_report_collection_summary(
        summary_index_path,
        &summary_file_path,
    )
}

/// Canonical report retrieval helper that reloads one indexed report by job spec id.
/// Use this when new code already registered the report and needs authoritative indexed reload.
pub fn load_indexed_execution_result_job_report(
    index_path: impl AsRef<Path>,
    job_spec_id: &str,
) -> Result<ExecutionResultJobReport> {
    let index = load_execution_result_job_report_index(index_path)?;
    let entry = find_execution_result_job_report_index_entry_by_job_spec_id(&index, job_spec_id)
        .ok_or_else(|| {
            MimirError::message(format!(
                "execution result job report index entry not found for job spec id {job_spec_id}"
            ))
        })?;

    load_execution_result_job_report(Path::new(&entry.report_file_path))
}

/// Canonical report publication helper that appends one validated report entry to the report index.
/// Use this with [`persist_execution_result_job_report`] for new report publication flows.
pub fn register_execution_result_job_report_in_index(
    index_path: impl AsRef<Path>,
    report_file_path: impl AsRef<Path>,
    report: &ExecutionResultJobReport,
) -> Result<ExecutionResultJobReportIndexEntry> {
    let index_path = index_path.as_ref();
    let report_file_path = report_file_path.as_ref();
    validate_execution_result_job_report(report)?;

    let mut index = if index_path.exists() {
        load_execution_result_job_report_index(index_path)?
    } else {
        empty_execution_result_job_report_index()
    };

    let entry = ExecutionResultJobReportIndexEntry {
        ordinal: index.entries.len(),
        report_file_path: path_to_owned_string(report_file_path)?,
        job_spec_id: report.job_spec_id.clone(),
        source_run_request_id: report.source_run_request_id.clone(),
        source_handoff_bundle_id: report.source_handoff_bundle_id.clone(),
        export_name: report.export_name.clone(),
        selection_mode: report.selection_mode,
        expected_entry_count: report.expected_entry_count,
        source_provenance_hash: report.source_provenance_hash.clone(),
    };
    validate_execution_result_job_report_index_entry(&entry, entry.ordinal)?;

    index.entries.push(entry.clone());
    persist_execution_result_job_report_index(index_path, &index)?;

    Ok(entry)
}

pub fn export_bundle(
    output_dir: impl AsRef<Path>,
    input: &ExportBundleInput,
) -> Result<ExportManifest> {
    let output_dir = output_dir.as_ref();
    ensure_output_dir_is_available(output_dir)?;

    let stage_dir = stage_dir_for(output_dir)?;
    let manifest = build_manifest(input);
    let mut index_entries =
        Vec::with_capacity(input.anchor_artifacts.len() + input.branch_artifacts.len());
    validate_manifest(&manifest)?;

    create_stage_root(&stage_dir)?;
    create_stage_subdirectory(&stage_dir, ExportArtifactKind::Anchor)?;
    create_stage_subdirectory(&stage_dir, ExportArtifactKind::Branch)?;

    let format = input.artifact_encoding.as_artifact_format();

    for (index, artifact) in input.anchor_artifacts.iter().enumerate() {
        let entry = write_anchor_stage_entry(&stage_dir, format, index, artifact)?;
        index_entries.push(entry);
    }

    for (index, artifact) in input.branch_artifacts.iter().enumerate() {
        let entry = write_branch_stage_entry(&stage_dir, format, index, artifact)?;
        index_entries.push(entry);
    }

    let export_index = ExportIndex {
        index_version: EXPORT_INDEX_VERSION,
        entries: index_entries,
    };

    validate_manifest(&manifest)?;
    validate_index(&manifest, &export_index)?;

    let index_path = stage_dir.join(EXPORT_INDEX_FILE_NAME);
    write_json_file(&index_path, &export_index)?;

    let manifest_path = stage_dir.join(EXPORT_MANIFEST_FILE_NAME);
    write_json_file(&manifest_path, &manifest)?;
    inspect_export_bundle(&stage_dir)?;

    fs::rename(&stage_dir, output_dir).map_err(|error| MimirError::io(output_dir, error))?;

    Ok(manifest)
}

pub fn load_export_manifest(bundle_dir: impl AsRef<Path>) -> Result<ExportManifest> {
    let bundle_dir = bundle_dir.as_ref();
    let manifest_path = bundle_dir.join(EXPORT_MANIFEST_FILE_NAME);
    let manifest: ExportManifest = load_json_file(&manifest_path)?;
    validate_manifest(&manifest)?;
    Ok(manifest)
}

pub fn load_export_index(
    bundle_dir: impl AsRef<Path>,
    manifest: &ExportManifest,
) -> Result<ExportIndex> {
    let bundle_dir = bundle_dir.as_ref();
    let index_path = resolve_relative_path(bundle_dir, &manifest.relative_index_path)?;
    let index: ExportIndex = load_json_file(&index_path)?;
    validate_index(manifest, &index)?;
    Ok(index)
}

pub fn inspect_export_bundle(bundle_dir: impl AsRef<Path>) -> Result<ExportInspection> {
    let bundle_dir = bundle_dir.as_ref();
    let manifest = load_export_manifest(bundle_dir)?;
    let index = load_export_index(bundle_dir, &manifest)?;
    let mut artifacts = Vec::with_capacity(index.entries.len());

    for entry in &index.entries {
        let artifact_path = resolve_relative_path(bundle_dir, &entry.relative_path)?;
        let header = read_artifact_header_auto(&artifact_path)?;
        validate_index_entry_header(entry, &header)?;
        artifacts.push(InspectedArtifact {
            entry: entry.clone(),
            header,
        });
    }

    Ok(ExportInspection {
        manifest,
        index,
        artifacts,
    })
}

pub fn load_export_bundle(bundle_dir: impl AsRef<Path>) -> Result<LoadedExportBundle> {
    let bundle_dir = bundle_dir.as_ref();
    let manifest = load_export_manifest(bundle_dir)?;
    let index = load_export_index(bundle_dir, &manifest)?;
    let mut anchor_artifacts = Vec::with_capacity(manifest.anchor_count);
    let mut branch_artifacts = Vec::with_capacity(manifest.branch_count);

    for entry in &index.entries {
        let artifact_path = resolve_relative_path(bundle_dir, &entry.relative_path)?;

        match entry.artifact_kind {
            ExportArtifactKind::Anchor => {
                let artifact: PersistedAnchorArtifact =
                    read_artifact_auto(&artifact_path, ArtifactKind::Anchor.schema())?;
                validate_loaded_anchor_entry(entry, &artifact)?;
                anchor_artifacts.push(artifact);
            }
            ExportArtifactKind::Branch => {
                let artifact: PersistedBranchArtifact =
                    read_artifact_auto(&artifact_path, ArtifactKind::Branch.schema())?;
                validate_loaded_branch_entry(entry, &artifact)?;
                branch_artifacts.push(artifact);
            }
        }
    }

    Ok(LoadedExportBundle {
        manifest,
        index,
        anchor_artifacts,
        branch_artifacts,
    })
}

pub fn adapt_loaded_export_for_consumer(loaded: LoadedExportBundle) -> ConsumerExport {
    loaded.into_consumer_export()
}

pub fn plan_candidate_request(
    consumer_export: &ConsumerExport,
    request: &CandidateRequest,
    plan_id: impl Into<String>,
) -> Result<ProcessingPlan> {
    validate_consumer_export_for_selection(consumer_export)?;
    validate_candidate_request(request)?;

    if request.export_name != consumer_export.manifest.export_name {
        return Err(MimirError::message(format!(
            "candidate request export mismatch: request targets {}, consumer export contains {}",
            request.export_name, consumer_export.manifest.export_name
        )));
    }

    let plan_id = plan_id.into();
    validate_identifier("processing plan id", &plan_id)?;

    let anchor_ids = consumer_export
        .anchors
        .iter()
        .map(|anchor| anchor.id.as_str().to_string())
        .collect::<Vec<_>>();
    let branch_ids = consumer_export
        .branches
        .iter()
        .map(|branch| branch.id.as_str().to_string())
        .collect::<Vec<_>>();

    let (selected_anchor_ids, missing_anchor_ids) =
        resolve_candidate_selection(&request.anchor_selection, &anchor_ids);
    let (selected_branch_ids, missing_branch_ids) =
        resolve_candidate_selection(&request.branch_selection, &branch_ids);
    let unresolved_branch_anchor_ids =
        unresolved_branch_anchor_ids(consumer_export, &selected_anchor_ids, &selected_branch_ids);

    let plan = ProcessingPlan {
        plan_id,
        request: request.clone(),
        selected_anchor_ids,
        selected_branch_ids,
        missing_anchor_ids,
        missing_branch_ids,
        unresolved_branch_anchor_ids,
    };
    validate_processing_plan(&plan)?;

    Ok(plan)
}

pub fn build_execution_result_stub(
    plan: &ProcessingPlan,
    result_id: impl Into<String>,
    status: ExecutionResultStatus,
    detail: Option<String>,
) -> Result<ExecutionResultStub> {
    validate_processing_plan(plan)?;

    let result = ExecutionResultStub {
        execution_result_version: EXECUTION_RESULT_STUB_VERSION,
        result_id: result_id.into(),
        recorded_at_unix_ms: current_unix_timestamp_millis()?,
        plan: plan.clone(),
        status,
        detail,
    };
    validate_execution_result_stub(&result)?;

    Ok(result)
}

pub fn load_execution_ledger_index(bundle_dir: impl AsRef<Path>) -> Result<ExecutionLedgerIndex> {
    let bundle_dir = bundle_dir.as_ref();
    let _manifest = load_export_manifest(bundle_dir)?;
    let index_path = execution_ledger_index_path(bundle_dir);

    if !index_path.exists() {
        return Ok(empty_execution_ledger_index());
    }

    let index: ExecutionLedgerIndex = load_json_file(&index_path)?;
    validate_execution_ledger_index(&index)?;

    Ok(index)
}

pub fn persist_execution_result(
    bundle_dir: impl AsRef<Path>,
    result: &ExecutionResultStub,
) -> Result<ExecutionLedgerIndexEntry> {
    let bundle_dir = bundle_dir.as_ref();
    let manifest = load_export_manifest(bundle_dir)?;
    validate_execution_result_stub(result)?;

    if manifest.export_name != result.plan.request.export_name {
        return Err(MimirError::message(format!(
            "execution result export mismatch: result targets {}, bundle contains {}",
            result.plan.request.export_name, manifest.export_name
        )));
    }

    let mut index = load_execution_ledger_index(bundle_dir)?;

    if index
        .entries
        .iter()
        .any(|entry| entry.result_id == result.result_id)
    {
        return Err(MimirError::message(format!(
            "duplicate execution result id {} in ledger",
            result.result_id
        )));
    }

    let ledger_dir = execution_ledger_dir(bundle_dir);
    let results_dir = execution_ledger_results_dir(bundle_dir);
    fs::create_dir_all(&ledger_dir).map_err(|error| MimirError::io(&ledger_dir, error))?;
    fs::create_dir_all(&results_dir).map_err(|error| MimirError::io(&results_dir, error))?;

    let relative_result_path = next_execution_result_relative_path(bundle_dir, &index)?;
    let result_path = resolve_relative_path(bundle_dir, &relative_result_path)?;
    write_json_file_staged(&result_path, result)?;

    let stored_result: ExecutionResultStub = load_json_file(&result_path)?;
    let entry = ExecutionLedgerIndexEntry {
        result_id: result.result_id.clone(),
        request_id: result.plan.request.request_id.clone(),
        plan_id: result.plan.plan_id.clone(),
        export_name: result.plan.request.export_name.clone(),
        status: result.status,
        recorded_at_unix_ms: result.recorded_at_unix_ms,
        relative_result_path,
        content_hash: hash_serializable(result)?,
    };
    validate_loaded_execution_result(&entry, &stored_result)?;

    index.entries.push(entry.clone());
    validate_execution_ledger_index(&index)?;

    let index_path = execution_ledger_index_path(bundle_dir);
    write_json_file_staged(&index_path, &index)?;

    let reloaded_index = load_execution_ledger_index(bundle_dir)?;
    if !reloaded_index
        .entries
        .iter()
        .any(|candidate| candidate == &entry)
    {
        return Err(MimirError::message(format!(
            "persisted execution result {} was not present after ledger reload",
            entry.result_id
        )));
    }

    Ok(entry)
}

pub fn load_execution_result(
    bundle_dir: impl AsRef<Path>,
    result_id: &str,
) -> Result<ExecutionResultStub> {
    let bundle_dir = bundle_dir.as_ref();
    validate_identifier("execution result id", result_id)?;

    let index = load_execution_ledger_index(bundle_dir)?;
    let entry = index
        .entries
        .iter()
        .find(|entry| entry.result_id == result_id)
        .ok_or_else(|| {
            MimirError::message(format!(
                "execution result {} was not found in ledger index",
                result_id
            ))
        })?;

    load_execution_result_by_entry(bundle_dir, entry)
}

pub fn inspect_execution_ledger_history(
    bundle_dir: impl AsRef<Path>,
) -> Result<ExecutionLedgerHistory> {
    let bundle_dir = bundle_dir.as_ref();
    let manifest = load_export_manifest(bundle_dir)?;
    let index = load_execution_ledger_index(bundle_dir)?;
    let mut entries = Vec::with_capacity(index.entries.len());

    for entry in &index.entries {
        let result = load_execution_result_by_entry(bundle_dir, entry)?;
        entries.push(ExecutionLedgerHistoryEntry {
            index_entry: entry.clone(),
            result,
        });
    }

    Ok(ExecutionLedgerHistory {
        export_name: manifest.export_name,
        index,
        entries,
    })
}

pub fn query_execution_ledger_history(
    history: &ExecutionLedgerHistory,
    query: &LedgerSelectionQuery,
) -> Vec<ExecutionLedgerHistoryEntry> {
    history
        .entries
        .iter()
        .filter(|entry| ledger_entry_matches_query(entry, query))
        .cloned()
        .collect()
}

pub fn build_execution_result_handoff_bundle(
    history_entries: &[ExecutionLedgerHistoryEntry],
    handoff_bundle_id: impl Into<String>,
    selection_mode: ExecutionResultSelectionMode,
) -> Result<ExecutionResultHandoffBundle> {
    let export_name = resolve_history_export_name(history_entries)?.to_string();
    let selected_entries = select_history_entries(history_entries, selection_mode);
    let entries = selected_entries
        .iter()
        .enumerate()
        .map(|(ordinal, entry)| ExecutionResultHandoffEntry {
            ordinal,
            result_id: entry.index_entry.result_id.clone(),
            request_id: entry.index_entry.request_id.clone(),
            plan_id: entry.index_entry.plan_id.clone(),
            status: entry.result.status,
            recorded_at_unix_ms: entry.result.recorded_at_unix_ms,
            selected_anchor_ids: entry.result.plan.selected_anchor_ids.clone(),
            selected_branch_ids: entry.result.plan.selected_branch_ids.clone(),
            detail: entry.result.detail.clone(),
        })
        .collect::<Vec<_>>();

    let bundle = ExecutionResultHandoffBundle {
        handoff_bundle_id: handoff_bundle_id.into(),
        export_name: export_name.clone(),
        selection_mode,
        entry_count: entries.len(),
        provenance_hash: compute_handoff_bundle_provenance_hash(
            &export_name,
            selection_mode,
            &entries,
        )?,
        entries,
    };
    validate_execution_result_handoff_bundle(&bundle)?;

    Ok(bundle)
}

pub fn build_handoff_bundle_from_history(
    history: &ExecutionLedgerHistory,
    handoff_bundle_id: impl Into<String>,
    selection_mode: ExecutionResultSelectionMode,
) -> Result<ExecutionResultHandoffBundle> {
    if history.entries.is_empty() {
        return Err(MimirError::message(format!(
            "cannot build handoff bundle {} from empty execution history",
            history.export_name
        )));
    }

    build_execution_result_handoff_bundle(&history.entries, handoff_bundle_id, selection_mode)
}

pub fn query_and_build_execution_result_handoff_bundle(
    history: &ExecutionLedgerHistory,
    query: &LedgerSelectionQuery,
    handoff_bundle_id: impl Into<String>,
    selection_mode: ExecutionResultSelectionMode,
) -> Result<ExecutionResultHandoffBundle> {
    let queried_entries = query_execution_ledger_history(history, query);

    if queried_entries.is_empty() {
        return Err(MimirError::message(format!(
            "query produced no execution history entries for export {}",
            history.export_name
        )));
    }

    build_execution_result_handoff_bundle(&queried_entries, handoff_bundle_id, selection_mode)
}

pub fn build_execution_result_run_request(
    handoff_entries: &[ExecutionResultHandoffEntry],
    run_request_id: impl Into<String>,
    source_handoff_bundle_id: impl Into<String>,
    export_name: impl Into<String>,
    selection_mode: ExecutionResultSelectionMode,
) -> Result<ExecutionResultRunRequest> {
    let export_name = export_name.into();
    validate_handoff_entries_for_pipeline(&export_name, handoff_entries)?;

    let entries = handoff_entries
        .iter()
        .map(|entry| ExecutionResultRunRequestEntry {
            ordinal: entry.ordinal,
            result_id: entry.result_id.clone(),
            request_id: entry.request_id.clone(),
            plan_id: entry.plan_id.clone(),
            status: entry.status,
            recorded_at_unix_ms: entry.recorded_at_unix_ms,
            selected_anchor_ids: entry.selected_anchor_ids.clone(),
            selected_branch_ids: entry.selected_branch_ids.clone(),
            detail: entry.detail.clone(),
        })
        .collect::<Vec<_>>();

    let run_request = ExecutionResultRunRequest {
        run_request_id: run_request_id.into(),
        source_handoff_bundle_id: source_handoff_bundle_id.into(),
        export_name: export_name.clone(),
        selection_mode,
        expected_entry_count: entries.len(),
        source_provenance_hash: compute_handoff_bundle_provenance_hash(
            &export_name,
            selection_mode,
            handoff_entries,
        )?,
        entries,
    };
    validate_execution_result_run_request(&run_request)?;

    Ok(run_request)
}

pub fn build_run_request_from_handoff_bundle(
    handoff_bundle: &ExecutionResultHandoffBundle,
    run_request_id: impl Into<String>,
) -> Result<ExecutionResultRunRequest> {
    validate_execution_result_handoff_bundle(handoff_bundle)?;

    build_execution_result_run_request(
        &handoff_bundle.entries,
        run_request_id,
        handoff_bundle.handoff_bundle_id.clone(),
        handoff_bundle.export_name.clone(),
        handoff_bundle.selection_mode,
    )
}

pub fn query_and_build_execution_result_run_request(
    history: &ExecutionLedgerHistory,
    query: &LedgerSelectionQuery,
    handoff_bundle_id: impl Into<String>,
    run_request_id: impl Into<String>,
    selection_mode: ExecutionResultSelectionMode,
) -> Result<ExecutionResultRunRequest> {
    let handoff_bundle = query_and_build_execution_result_handoff_bundle(
        history,
        query,
        handoff_bundle_id,
        selection_mode,
    )?;

    build_run_request_from_handoff_bundle(&handoff_bundle, run_request_id)
}

#[allow(clippy::too_many_arguments)]
pub fn build_execution_result_job_spec(
    run_request_entries: &[ExecutionResultRunRequestEntry],
    job_spec_id: impl Into<String>,
    source_run_request_id: impl Into<String>,
    source_handoff_bundle_id: impl Into<String>,
    export_name: impl Into<String>,
    selection_mode: ExecutionResultSelectionMode,
    expected_entry_count: usize,
    source_provenance_hash: impl Into<String>,
) -> Result<ExecutionResultJobSpec> {
    let export_name = export_name.into();
    validate_run_request_entries_for_pipeline(&export_name, run_request_entries)?;
    let expected_provenance_hash =
        compute_run_request_provenance_hash(&export_name, selection_mode, run_request_entries)?;
    let source_provenance_hash = source_provenance_hash.into();

    if expected_entry_count != run_request_entries.len() {
        return Err(MimirError::message(format!(
            "execution result job spec entry count drift: expected {}, found {}",
            expected_entry_count,
            run_request_entries.len()
        )));
    }

    if source_provenance_hash != expected_provenance_hash {
        return Err(MimirError::message(
            "execution result job spec provenance drift",
        ));
    }

    let entries = run_request_entries
        .iter()
        .map(|entry| ExecutionResultJobSpecEntry {
            ordinal: entry.ordinal,
            result_id: entry.result_id.clone(),
            request_id: entry.request_id.clone(),
            plan_id: entry.plan_id.clone(),
            status: entry.status,
            recorded_at_unix_ms: entry.recorded_at_unix_ms,
            selected_anchor_ids: entry.selected_anchor_ids.clone(),
            selected_branch_ids: entry.selected_branch_ids.clone(),
            detail: entry.detail.clone(),
        })
        .collect::<Vec<_>>();

    let job_spec = ExecutionResultJobSpec {
        job_spec_id: job_spec_id.into(),
        source_run_request_id: source_run_request_id.into(),
        source_handoff_bundle_id: source_handoff_bundle_id.into(),
        export_name,
        selection_mode,
        expected_entry_count,
        source_provenance_hash,
        entries,
    };
    validate_execution_result_job_spec(&job_spec)?;

    Ok(job_spec)
}

pub fn build_job_spec_from_run_request(
    run_request: &ExecutionResultRunRequest,
    job_spec_id: impl Into<String>,
) -> Result<ExecutionResultJobSpec> {
    validate_execution_result_run_request(run_request)?;

    build_execution_result_job_spec(
        &run_request.entries,
        job_spec_id,
        run_request.run_request_id.clone(),
        run_request.source_handoff_bundle_id.clone(),
        run_request.export_name.clone(),
        run_request.selection_mode,
        run_request.expected_entry_count,
        run_request.source_provenance_hash.clone(),
    )
}

pub fn query_and_build_execution_result_job_spec(
    history: &ExecutionLedgerHistory,
    query: &LedgerSelectionQuery,
    handoff_bundle_id: impl Into<String>,
    run_request_id: impl Into<String>,
    job_spec_id: impl Into<String>,
    selection_mode: ExecutionResultSelectionMode,
) -> Result<ExecutionResultJobSpec> {
    let run_request = query_and_build_execution_result_run_request(
        history,
        query,
        handoff_bundle_id,
        run_request_id,
        selection_mode,
    )?;

    build_job_spec_from_run_request(&run_request, job_spec_id)
}

/// Canonical execution bridge from ledger selection to executor-driven report generation.
pub fn query_and_execute_execution_result_job_spec(
    bundle_dir: impl AsRef<Path>,
    query: &LedgerSelectionQuery,
    handoff_bundle_id: impl Into<String>,
    run_request_id: impl Into<String>,
    job_spec_id: impl Into<String>,
    selection_mode: ExecutionResultSelectionMode,
    executor: &impl ExecutionResultJobExecutor,
) -> Result<ExecutionResultJobReport> {
    let history = inspect_execution_ledger_history(bundle_dir)?;
    let job_spec = query_and_build_execution_result_job_spec(
        &history,
        query,
        handoff_bundle_id,
        run_request_id,
        job_spec_id,
        selection_mode,
    )?;

    executor.execute(&job_spec)
}

/// Canonical stub-execution bridge using the deterministic `StubExecutionResultJobExecutor`.
/// Preferred supported surface for new stub-execution composition before report persistence or indexing.
pub fn query_and_stub_execute_execution_result_job_spec(
    bundle_dir: impl AsRef<Path>,
    query: &LedgerSelectionQuery,
    handoff_bundle_id: impl Into<String>,
    run_request_id: impl Into<String>,
    job_spec_id: impl Into<String>,
    selection_mode: ExecutionResultSelectionMode,
) -> Result<ExecutionResultJobReport> {
    let executor = StubExecutionResultJobExecutor;

    query_and_execute_execution_result_job_spec(
        bundle_dir,
        query,
        handoff_bundle_id,
        run_request_id,
        job_spec_id,
        selection_mode,
        &executor,
    )
}

/// Canonical stub-execution bridge that materializes, reloads, and registers a report in the report index.
/// Canonical stub-execution bridge lane for new code:
/// [`query_stub_execute_persist_load_and_register_execution_result_job_report`].
#[allow(clippy::too_many_arguments)]
pub fn query_stub_execute_persist_load_and_register_execution_result_job_report(
    bundle_dir: impl AsRef<Path>,
    query: &LedgerSelectionQuery,
    handoff_bundle_id: impl Into<String>,
    run_request_id: impl Into<String>,
    job_spec_id: impl Into<String>,
    selection_mode: ExecutionResultSelectionMode,
    report_path: impl AsRef<Path>,
    report_index_path: impl AsRef<Path>,
) -> Result<ExecutionResultJobReport> {
    let report_path = report_path.as_ref();
    let report_index_path = report_index_path.as_ref();
    let report = query_and_stub_execute_execution_result_job_spec(
        bundle_dir,
        query,
        handoff_bundle_id,
        run_request_id,
        job_spec_id,
        selection_mode,
    )?;
    persist_execution_result_job_report(report_path, &report)?;
    let loaded_report = load_execution_result_job_report(report_path)?;

    register_execution_result_job_report_in_index(report_index_path, report_path, &loaded_report)?;

    Ok(loaded_report)
}

#[allow(clippy::too_many_arguments)]
/// Canonical stub-execution bridge from one stubbed report publication into canonical report-index query/load retrieval.
/// Preferred supported surface for new stub-execution report retrieval composition.
pub fn query_stub_execute_persist_load_register_query_and_load_execution_result_job_reports(
    bundle_dir: impl AsRef<Path>,
    query: &LedgerSelectionQuery,
    handoff_bundle_id: impl Into<String>,
    run_request_id: impl Into<String>,
    job_spec_id: impl Into<String>,
    selection_mode: ExecutionResultSelectionMode,
    report_path: impl AsRef<Path>,
    report_index_path: impl AsRef<Path>,
    report_index_query: &ExecutionResultJobReportIndexQuery,
) -> Result<Vec<ExecutionResultJobReport>> {
    let report_path = report_path.as_ref();
    let report_index_path = report_index_path.as_ref();

    query_stub_execute_persist_load_and_register_execution_result_job_report(
        bundle_dir,
        query,
        handoff_bundle_id,
        run_request_id,
        job_spec_id,
        selection_mode,
        report_path,
        report_index_path,
    )?;

    let selection_summary =
        load_and_query_execution_result_job_report_index(report_index_path, report_index_query)?;
    load_selected_execution_result_job_reports(&selection_summary.selected_entries)
}

#[allow(clippy::too_many_arguments)]
/// Canonical stub-execution bridge from report publication into indexed, reloaded summary materialization.
/// Preferred supported surface for new stub-execution summary publication composition.
pub fn query_stub_execute_register_report_and_index_load_summary(
    bundle_dir: impl AsRef<Path>,
    query: &LedgerSelectionQuery,
    handoff_bundle_id: impl Into<String>,
    run_request_id: impl Into<String>,
    job_spec_id: impl Into<String>,
    selection_mode: ExecutionResultSelectionMode,
    report_path: impl AsRef<Path>,
    report_index_path: impl AsRef<Path>,
    report_index_query: &ExecutionResultJobReportIndexQuery,
    summary_index_path: impl AsRef<Path>,
    output_summary_path: impl AsRef<Path>,
) -> Result<ExecutionResultJobReportCollectionSummary> {
    let report_index_path = report_index_path.as_ref();
    let summary_index_path = summary_index_path.as_ref();
    let output_summary_path = output_summary_path.as_ref();

    query_stub_execute_persist_load_register_query_and_load_execution_result_job_reports(
        bundle_dir,
        query,
        handoff_bundle_id,
        run_request_id,
        job_spec_id,
        selection_mode,
        report_path,
        report_index_path,
        report_index_query,
    )?;

    load_query_reports_summarize_persist_register_and_index_load_execution_result_job_report_collection_summary(
        report_index_path,
        report_index_query,
        summary_index_path,
        output_summary_path,
    )
}

#[allow(clippy::too_many_arguments)]
/// Higher-level convenience composition over canonical summary query/aggregate/persist/register helpers.
/// Retained for compatibility as a composition-only convenience wrapper.
/// Prefer canonical lower-level helpers for new work.
/// Candidate for future compatibility cleanup in a dedicated breaking-change pass.
pub fn query_stub_execute_register_report_and_aggregate_queried_execution_result_job_report_collection_summaries(
    bundle_dir: impl AsRef<Path>,
    query: &LedgerSelectionQuery,
    handoff_bundle_id: impl Into<String>,
    run_request_id: impl Into<String>,
    job_spec_id: impl Into<String>,
    selection_mode: ExecutionResultSelectionMode,
    report_path: impl AsRef<Path>,
    report_index_path: impl AsRef<Path>,
    report_index_query: &ExecutionResultJobReportIndexQuery,
    summary_index_path: impl AsRef<Path>,
    output_summary_path: impl AsRef<Path>,
    summary_index_query: &ExecutionResultJobReportCollectionSummaryIndexQuery,
    aggregate_output_summary_path: impl AsRef<Path>,
) -> Result<ExecutionResultJobReportCollectionSummary> {
    let summary_index_path = summary_index_path.as_ref();

    query_stub_execute_register_report_and_index_load_summary(
        bundle_dir,
        query,
        handoff_bundle_id,
        run_request_id,
        job_spec_id,
        selection_mode,
        report_path,
        report_index_path,
        report_index_query,
        summary_index_path,
        output_summary_path,
    )?;

    load_query_summarize_persist_register_and_index_load_execution_result_job_report_collection_summary(
        summary_index_path,
        summary_index_query,
        aggregate_output_summary_path,
    )
}

#[derive(Serialize)]
struct PipelineProvenance<'a, E>
where
    E: Serialize,
{
    export_name: &'a str,
    selection_mode: ExecutionResultSelectionMode,
    entries: &'a [E],
}

fn resolve_history_export_name(history_entries: &[ExecutionLedgerHistoryEntry]) -> Result<&str> {
    let first_entry = history_entries.first().ok_or_else(|| {
        MimirError::message("cannot build handoff bundle from empty execution history")
    })?;
    validate_identifier(
        "execution history export name",
        &first_entry.index_entry.export_name,
    )?;

    for entry in history_entries {
        if entry.index_entry.export_name != first_entry.index_entry.export_name {
            return Err(MimirError::message(format!(
                "execution history export mismatch: expected {}, found {} at result {}",
                first_entry.index_entry.export_name,
                entry.index_entry.export_name,
                entry.index_entry.result_id
            )));
        }
    }

    Ok(first_entry.index_entry.export_name.as_str())
}

fn select_history_entries(
    history_entries: &[ExecutionLedgerHistoryEntry],
    selection_mode: ExecutionResultSelectionMode,
) -> Vec<ExecutionLedgerHistoryEntry> {
    match selection_mode {
        ExecutionResultSelectionMode::FullHistory => history_entries.to_vec(),
        ExecutionResultSelectionMode::LatestOnly => {
            let mut latest_by_plan = BTreeMap::<String, (u64, usize)>::new();

            for (index, entry) in history_entries.iter().enumerate() {
                let candidate = (entry.result.recorded_at_unix_ms, index);
                match latest_by_plan.get(&entry.index_entry.plan_id) {
                    Some(current) if *current >= candidate => {}
                    _ => {
                        latest_by_plan.insert(entry.index_entry.plan_id.clone(), candidate);
                    }
                }
            }

            history_entries
                .iter()
                .enumerate()
                .filter(|(index, entry)| {
                    latest_by_plan
                        .get(&entry.index_entry.plan_id)
                        .is_some_and(|(_, selected_index)| selected_index == index)
                })
                .map(|(_, entry)| entry.clone())
                .collect()
        }
    }
}

fn compute_pipeline_provenance_hash<E>(
    export_name: &str,
    selection_mode: ExecutionResultSelectionMode,
    entries: &[E],
) -> Result<String>
where
    E: Serialize,
{
    validate_identifier("pipeline export name", export_name)?;
    hash_serializable(&PipelineProvenance {
        export_name,
        selection_mode,
        entries,
    })
}

fn compute_handoff_bundle_provenance_hash(
    export_name: &str,
    selection_mode: ExecutionResultSelectionMode,
    entries: &[ExecutionResultHandoffEntry],
) -> Result<String> {
    compute_pipeline_provenance_hash(export_name, selection_mode, entries)
}

fn compute_run_request_provenance_hash(
    export_name: &str,
    selection_mode: ExecutionResultSelectionMode,
    entries: &[ExecutionResultRunRequestEntry],
) -> Result<String> {
    compute_pipeline_provenance_hash(export_name, selection_mode, entries)
}

fn compute_job_spec_provenance_hash(
    export_name: &str,
    selection_mode: ExecutionResultSelectionMode,
    entries: &[ExecutionResultJobSpecEntry],
) -> Result<String> {
    compute_pipeline_provenance_hash(export_name, selection_mode, entries)
}

fn validate_execution_result_handoff_bundle(
    handoff_bundle: &ExecutionResultHandoffBundle,
) -> Result<()> {
    validate_identifier(
        "execution result handoff bundle id",
        &handoff_bundle.handoff_bundle_id,
    )?;
    validate_identifier(
        "execution result handoff provenance hash",
        &handoff_bundle.provenance_hash,
    )?;
    validate_handoff_entries_for_pipeline(&handoff_bundle.export_name, &handoff_bundle.entries)?;

    if handoff_bundle.entry_count != handoff_bundle.entries.len() {
        return Err(MimirError::message(format!(
            "execution result handoff bundle entry count drift: expected {}, found {}",
            handoff_bundle.entry_count,
            handoff_bundle.entries.len()
        )));
    }

    let expected_hash = compute_handoff_bundle_provenance_hash(
        &handoff_bundle.export_name,
        handoff_bundle.selection_mode,
        &handoff_bundle.entries,
    )?;
    if handoff_bundle.provenance_hash != expected_hash {
        return Err(MimirError::message(
            "execution result handoff bundle provenance drift",
        ));
    }

    Ok(())
}

fn validate_handoff_entries_for_pipeline(
    export_name: &str,
    handoff_entries: &[ExecutionResultHandoffEntry],
) -> Result<()> {
    validate_identifier("execution result export name", export_name)?;
    if handoff_entries.is_empty() {
        return Err(MimirError::message(format!(
            "execution result handoff entries must not be empty for export {export_name}"
        )));
    }

    let mut seen_result_ids = BTreeSet::new();

    for (expected_ordinal, entry) in handoff_entries.iter().enumerate() {
        validate_handoff_entry(entry, expected_ordinal)?;

        if !seen_result_ids.insert(entry.result_id.clone()) {
            return Err(MimirError::message(format!(
                "duplicate execution result id {} in handoff bundle",
                entry.result_id
            )));
        }
    }

    Ok(())
}

fn validate_execution_result_run_request(run_request: &ExecutionResultRunRequest) -> Result<()> {
    validate_identifier(
        "execution result run request id",
        &run_request.run_request_id,
    )?;
    validate_identifier(
        "execution result handoff bundle id",
        &run_request.source_handoff_bundle_id,
    )?;
    validate_identifier(
        "execution result run request provenance hash",
        &run_request.source_provenance_hash,
    )?;
    validate_run_request_entries_for_pipeline(&run_request.export_name, &run_request.entries)?;

    if run_request.expected_entry_count != run_request.entries.len() {
        return Err(MimirError::message(format!(
            "execution result run request entry count drift: expected {}, found {}",
            run_request.expected_entry_count,
            run_request.entries.len()
        )));
    }

    let expected_hash = compute_run_request_provenance_hash(
        &run_request.export_name,
        run_request.selection_mode,
        &run_request.entries,
    )?;
    if run_request.source_provenance_hash != expected_hash {
        return Err(MimirError::message(
            "execution result run request provenance drift",
        ));
    }

    Ok(())
}

fn validate_run_request_entries_for_pipeline(
    export_name: &str,
    run_request_entries: &[ExecutionResultRunRequestEntry],
) -> Result<()> {
    validate_identifier("execution result export name", export_name)?;
    if run_request_entries.is_empty() {
        return Err(MimirError::message(format!(
            "execution result run request entries must not be empty for export {export_name}"
        )));
    }

    let mut seen_result_ids = BTreeSet::new();

    for (expected_ordinal, entry) in run_request_entries.iter().enumerate() {
        validate_run_request_entry(entry, expected_ordinal)?;

        if !seen_result_ids.insert(entry.result_id.clone()) {
            return Err(MimirError::message(format!(
                "duplicate execution result id {} in run request",
                entry.result_id
            )));
        }
    }

    Ok(())
}

fn validate_execution_result_job_spec(job_spec: &ExecutionResultJobSpec) -> Result<()> {
    validate_identifier("execution result job spec id", &job_spec.job_spec_id)?;
    validate_identifier(
        "execution result run request id",
        &job_spec.source_run_request_id,
    )?;
    validate_identifier(
        "execution result handoff bundle id",
        &job_spec.source_handoff_bundle_id,
    )?;
    validate_identifier(
        "execution result job spec provenance hash",
        &job_spec.source_provenance_hash,
    )?;
    validate_job_spec_entries_for_pipeline(&job_spec.export_name, &job_spec.entries)?;

    if job_spec.expected_entry_count != job_spec.entries.len() {
        return Err(MimirError::message(format!(
            "execution result job spec entry count drift: expected {}, found {}",
            job_spec.expected_entry_count,
            job_spec.entries.len()
        )));
    }

    let expected_hash = compute_job_spec_provenance_hash(
        &job_spec.export_name,
        job_spec.selection_mode,
        &job_spec.entries,
    )?;
    if job_spec.source_provenance_hash != expected_hash {
        return Err(MimirError::message(
            "execution result job spec provenance drift",
        ));
    }

    Ok(())
}

fn validate_job_spec_entries_for_pipeline(
    export_name: &str,
    job_spec_entries: &[ExecutionResultJobSpecEntry],
) -> Result<()> {
    validate_identifier("execution result export name", export_name)?;
    if job_spec_entries.is_empty() {
        return Err(MimirError::message(format!(
            "execution result job spec entries must not be empty for export {export_name}"
        )));
    }

    let mut seen_result_ids = BTreeSet::new();

    for (expected_ordinal, entry) in job_spec_entries.iter().enumerate() {
        validate_job_spec_entry(entry, expected_ordinal)?;

        if !seen_result_ids.insert(entry.result_id.clone()) {
            return Err(MimirError::message(format!(
                "duplicate execution result id {} in job spec",
                entry.result_id
            )));
        }
    }

    Ok(())
}

fn validate_handoff_entry(
    entry: &ExecutionResultHandoffEntry,
    expected_ordinal: usize,
) -> Result<()> {
    validate_pipeline_ordinal(
        "handoff bundle",
        &entry.result_id,
        entry.ordinal,
        expected_ordinal,
    )?;
    validate_identifier("execution result id", &entry.result_id)?;
    validate_identifier("candidate request id", &entry.request_id)?;
    validate_identifier("processing plan id", &entry.plan_id)?;
    validate_identifier_list("selected anchor ids", &entry.selected_anchor_ids)?;
    validate_identifier_list("selected branch ids", &entry.selected_branch_ids)?;
    validate_optional_text("execution result handoff detail", entry.detail.as_deref())?;

    Ok(())
}

fn validate_run_request_entry(
    entry: &ExecutionResultRunRequestEntry,
    expected_ordinal: usize,
) -> Result<()> {
    validate_pipeline_ordinal(
        "run request",
        &entry.result_id,
        entry.ordinal,
        expected_ordinal,
    )?;
    validate_identifier("execution result id", &entry.result_id)?;
    validate_identifier("candidate request id", &entry.request_id)?;
    validate_identifier("processing plan id", &entry.plan_id)?;
    validate_identifier_list("selected anchor ids", &entry.selected_anchor_ids)?;
    validate_identifier_list("selected branch ids", &entry.selected_branch_ids)?;
    validate_optional_text(
        "execution result run request detail",
        entry.detail.as_deref(),
    )?;

    Ok(())
}

fn validate_job_spec_entry(
    entry: &ExecutionResultJobSpecEntry,
    expected_ordinal: usize,
) -> Result<()> {
    validate_pipeline_ordinal(
        "job spec",
        &entry.result_id,
        entry.ordinal,
        expected_ordinal,
    )?;
    validate_identifier("execution result id", &entry.result_id)?;
    validate_identifier("candidate request id", &entry.request_id)?;
    validate_identifier("processing plan id", &entry.plan_id)?;
    validate_identifier_list("selected anchor ids", &entry.selected_anchor_ids)?;
    validate_identifier_list("selected branch ids", &entry.selected_branch_ids)?;
    validate_optional_text("execution result job spec detail", entry.detail.as_deref())?;

    Ok(())
}

fn validate_pipeline_ordinal(
    label: &str,
    result_id: &str,
    actual_ordinal: usize,
    expected_ordinal: usize,
) -> Result<()> {
    if actual_ordinal != expected_ordinal {
        return Err(MimirError::message(format!(
            "execution result {label} ordinal drift at result {result_id}: expected {expected_ordinal}, found {actual_ordinal}"
        )));
    }

    Ok(())
}

fn validate_optional_text(label: &str, value: Option<&str>) -> Result<()> {
    if let Some(value) = value {
        if value.trim().is_empty() {
            return Err(MimirError::message(format!("{label} must not be empty")));
        }
    }

    Ok(())
}

fn validate_consumer_export_for_selection(consumer_export: &ConsumerExport) -> Result<()> {
    let anchor_ids = consumer_export
        .anchors
        .iter()
        .map(|anchor| anchor.id.as_str().to_string())
        .collect::<Vec<_>>();
    let branch_ids = consumer_export
        .branches
        .iter()
        .map(|branch| branch.id.as_str().to_string())
        .collect::<Vec<_>>();

    validate_identifier_list("consumer export anchor ids", &anchor_ids)?;
    validate_identifier_list("consumer export branch ids", &branch_ids)?;

    Ok(())
}

fn validate_candidate_request(request: &CandidateRequest) -> Result<()> {
    validate_identifier("candidate request id", &request.request_id)?;
    validate_identifier("candidate request export name", &request.export_name)?;
    validate_candidate_selection("candidate anchor selection", &request.anchor_selection)?;
    validate_candidate_selection("candidate branch selection", &request.branch_selection)?;

    Ok(())
}

fn validate_candidate_selection(label: &str, selection: &CandidateSelection) -> Result<()> {
    if let CandidateSelection::Explicit(ids) = selection {
        validate_identifier_list(label, ids)?;
    }

    Ok(())
}

fn validate_processing_plan(plan: &ProcessingPlan) -> Result<()> {
    validate_identifier("processing plan id", &plan.plan_id)?;
    validate_candidate_request(&plan.request)?;
    validate_identifier_list("selected anchor ids", &plan.selected_anchor_ids)?;
    validate_identifier_list("selected branch ids", &plan.selected_branch_ids)?;
    validate_identifier_list("missing anchor ids", &plan.missing_anchor_ids)?;
    validate_identifier_list("missing branch ids", &plan.missing_branch_ids)?;
    validate_identifier_list(
        "unresolved branch anchor ids",
        &plan.unresolved_branch_anchor_ids,
    )?;

    Ok(())
}

fn validate_execution_result_stub(result: &ExecutionResultStub) -> Result<()> {
    if result.execution_result_version != EXECUTION_RESULT_STUB_VERSION {
        return Err(MimirError::message(format!(
            "unsupported execution result stub version {}",
            result.execution_result_version
        )));
    }

    validate_identifier("execution result id", &result.result_id)?;
    validate_processing_plan(&result.plan)?;

    Ok(())
}

fn validate_execution_ledger_index(index: &ExecutionLedgerIndex) -> Result<()> {
    if index.ledger_index_version != EXECUTION_LEDGER_INDEX_VERSION {
        return Err(MimirError::message(format!(
            "unsupported execution ledger index version {}",
            index.ledger_index_version
        )));
    }

    let mut seen_result_ids = BTreeSet::new();
    let mut seen_relative_paths = BTreeSet::new();

    for entry in &index.entries {
        validate_execution_ledger_index_entry(entry)?;

        if !seen_result_ids.insert(entry.result_id.clone()) {
            return Err(MimirError::message(format!(
                "duplicate execution result id {} in ledger index",
                entry.result_id
            )));
        }

        if !seen_relative_paths.insert(entry.relative_result_path.clone()) {
            return Err(MimirError::message(format!(
                "duplicate execution ledger result path {}",
                entry.relative_result_path
            )));
        }
    }

    Ok(())
}

fn validate_execution_ledger_index_entry(entry: &ExecutionLedgerIndexEntry) -> Result<()> {
    validate_identifier("execution result id", &entry.result_id)?;
    validate_identifier("candidate request id", &entry.request_id)?;
    validate_identifier("processing plan id", &entry.plan_id)?;
    validate_identifier("execution result export name", &entry.export_name)?;
    validate_relative_path_text(&entry.relative_result_path)?;

    if path_extension(&entry.relative_result_path) != Some("json") {
        return Err(MimirError::message(format!(
            "execution ledger result path must end with .json: {}",
            entry.relative_result_path
        )));
    }

    if !entry
        .relative_result_path
        .starts_with(EXECUTION_LEDGER_DIR_NAME)
    {
        return Err(MimirError::message(format!(
            "execution ledger result path must stay under {}: {}",
            EXECUTION_LEDGER_DIR_NAME, entry.relative_result_path
        )));
    }

    validate_identifier("execution result content hash", &entry.content_hash)?;

    Ok(())
}

fn validate_loaded_execution_result(
    entry: &ExecutionLedgerIndexEntry,
    result: &ExecutionResultStub,
) -> Result<()> {
    validate_execution_ledger_index_entry(entry)?;
    validate_execution_result_stub(result)?;

    if entry.result_id != result.result_id {
        return Err(MimirError::message(format!(
            "execution result id mismatch at {}: index expects {}, file contains {}",
            entry.relative_result_path, entry.result_id, result.result_id
        )));
    }

    if entry.request_id != result.plan.request.request_id {
        return Err(MimirError::message(format!(
            "candidate request id mismatch at {}: index expects {}, file contains {}",
            entry.relative_result_path, entry.request_id, result.plan.request.request_id
        )));
    }

    if entry.plan_id != result.plan.plan_id {
        return Err(MimirError::message(format!(
            "processing plan id mismatch at {}: index expects {}, file contains {}",
            entry.relative_result_path, entry.plan_id, result.plan.plan_id
        )));
    }

    if entry.export_name != result.plan.request.export_name {
        return Err(MimirError::message(format!(
            "execution result export mismatch at {}: index expects {}, file contains {}",
            entry.relative_result_path, entry.export_name, result.plan.request.export_name
        )));
    }

    if entry.status != result.status {
        return Err(MimirError::message(format!(
            "execution result status mismatch at {}",
            entry.relative_result_path
        )));
    }

    if entry.recorded_at_unix_ms != result.recorded_at_unix_ms {
        return Err(MimirError::message(format!(
            "execution result timestamp mismatch at {}",
            entry.relative_result_path
        )));
    }

    let content_hash = hash_serializable(result)?;
    if entry.content_hash != content_hash {
        return Err(MimirError::message(format!(
            "execution result content hash mismatch at {}",
            entry.relative_result_path
        )));
    }

    Ok(())
}

fn validate_identifier(label: &str, value: &str) -> Result<()> {
    if value.trim().is_empty() {
        return Err(MimirError::message(format!("{label} must not be empty")));
    }

    Ok(())
}

fn push_unique_string(values: &mut Vec<String>, value: &str) {
    if !values.iter().any(|existing| existing == value) {
        values.push(value.to_string());
    }
}

fn push_unique_selection_mode(
    values: &mut Vec<ExecutionResultSelectionMode>,
    value: ExecutionResultSelectionMode,
) {
    if !values.contains(&value) {
        values.push(value);
    }
}

fn validate_identifier_list(label: &str, values: &[String]) -> Result<()> {
    let mut seen = BTreeSet::new();

    for value in values {
        validate_identifier(label, value)?;

        if !seen.insert(value.clone()) {
            return Err(MimirError::message(format!(
                "{label} must not contain duplicate value {value}"
            )));
        }
    }

    Ok(())
}

fn validate_unique_selection_modes(
    label: &str,
    values: &[ExecutionResultSelectionMode],
) -> Result<()> {
    let mut seen = Vec::new();

    for value in values {
        if seen.contains(value) {
            return Err(MimirError::message(format!(
                "{label} must not contain duplicate value {:?}",
                value
            )));
        }

        seen.push(*value);
    }

    Ok(())
}

fn resolve_candidate_selection(
    selection: &CandidateSelection,
    available_ids: &[String],
) -> (Vec<String>, Vec<String>) {
    let available = available_ids
        .iter()
        .map(String::as_str)
        .collect::<BTreeSet<_>>();

    match selection {
        CandidateSelection::All => (available_ids.to_vec(), Vec::new()),
        CandidateSelection::Explicit(requested_ids) => {
            let mut selected = Vec::new();
            let mut missing = Vec::new();

            for requested_id in requested_ids {
                if available.contains(requested_id.as_str()) {
                    selected.push(requested_id.clone());
                } else {
                    missing.push(requested_id.clone());
                }
            }

            (selected, missing)
        }
    }
}

fn unresolved_branch_anchor_ids(
    consumer_export: &ConsumerExport,
    selected_anchor_ids: &[String],
    selected_branch_ids: &[String],
) -> Vec<String> {
    let selected_anchors = selected_anchor_ids
        .iter()
        .map(String::as_str)
        .collect::<BTreeSet<_>>();
    let selected_branches = selected_branch_ids
        .iter()
        .map(String::as_str)
        .collect::<BTreeSet<_>>();
    let mut unresolved = Vec::new();
    let mut seen = BTreeSet::new();

    for branch in &consumer_export.branches {
        if selected_branches.contains(branch.id.as_str())
            && !selected_anchors.contains(branch.anchor_id.as_str())
            && seen.insert(branch.anchor_id.as_str().to_string())
        {
            unresolved.push(branch.anchor_id.as_str().to_string());
        }
    }

    unresolved
}

fn empty_execution_ledger_index() -> ExecutionLedgerIndex {
    ExecutionLedgerIndex {
        ledger_index_version: EXECUTION_LEDGER_INDEX_VERSION,
        entries: Vec::new(),
    }
}

fn execution_ledger_dir(bundle_dir: &Path) -> PathBuf {
    bundle_dir.join(EXECUTION_LEDGER_DIR_NAME)
}

fn execution_ledger_results_dir(bundle_dir: &Path) -> PathBuf {
    execution_ledger_dir(bundle_dir).join(EXECUTION_LEDGER_RESULTS_DIR_NAME)
}

fn execution_ledger_index_path(bundle_dir: &Path) -> PathBuf {
    execution_ledger_dir(bundle_dir).join(EXECUTION_LEDGER_INDEX_FILE_NAME)
}

fn next_execution_result_relative_path(
    bundle_dir: &Path,
    index: &ExecutionLedgerIndex,
) -> Result<String> {
    for ordinal in index.entries.len()..index.entries.len() + 1024 {
        let relative_path = format!(
            "{}/{}/result-{ordinal:04}.json",
            EXECUTION_LEDGER_DIR_NAME, EXECUTION_LEDGER_RESULTS_DIR_NAME
        );
        let full_path = resolve_relative_path(bundle_dir, &relative_path)?;
        if !full_path.exists() {
            return Ok(relative_path);
        }
    }

    Err(MimirError::message(format!(
        "failed to allocate a ledger result path under {}",
        bundle_dir.display()
    )))
}

fn load_execution_result_by_entry(
    bundle_dir: &Path,
    entry: &ExecutionLedgerIndexEntry,
) -> Result<ExecutionResultStub> {
    let result_path = resolve_relative_path(bundle_dir, &entry.relative_result_path)?;
    let result: ExecutionResultStub = load_json_file(&result_path)?;
    validate_loaded_execution_result(entry, &result)?;

    Ok(result)
}

fn ledger_entry_matches_query(
    entry: &ExecutionLedgerHistoryEntry,
    query: &LedgerSelectionQuery,
) -> bool {
    matches_optional_string(&query.result_id, &entry.index_entry.result_id)
        && matches_optional_string(&query.request_id, &entry.index_entry.request_id)
        && matches_optional_string(&query.plan_id, &entry.index_entry.plan_id)
        && matches_optional_string(&query.export_name, &entry.index_entry.export_name)
        && matches_optional_status(query.status, entry.index_entry.status)
        && matches_optional_membership(&query.anchor_id, &entry.result.plan.selected_anchor_ids)
        && matches_optional_membership(&query.branch_id, &entry.result.plan.selected_branch_ids)
}

fn matches_optional_string(expected: &Option<String>, actual: &str) -> bool {
    expected.as_deref().is_none_or(|value| value == actual)
}

fn matches_optional_status(
    expected: Option<ExecutionResultStatus>,
    actual: ExecutionResultStatus,
) -> bool {
    expected.is_none_or(|value| value == actual)
}

fn matches_optional_membership(expected: &Option<String>, values: &[String]) -> bool {
    expected
        .as_deref()
        .is_none_or(|value| values.iter().any(|candidate| candidate == value))
}

fn current_unix_timestamp_millis() -> Result<u64> {
    let duration = SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .map_err(|_| MimirError::message("system clock is before UNIX_EPOCH"))?;
    u64::try_from(duration.as_millis())
        .map_err(|_| MimirError::message("unix timestamp millis overflowed u64"))
}

fn build_manifest(input: &ExportBundleInput) -> ExportManifest {
    ExportManifest {
        manifest_version: EXPORT_MANIFEST_VERSION,
        export_name: input.export_name.clone(),
        producer: EXPORT_BUNDLE_PRODUCER.to_string(),
        created_by_component: input.created_by_component.clone(),
        artifact_encoding: input.artifact_encoding,
        relative_index_path: EXPORT_INDEX_FILE_NAME.to_string(),
        artifact_count: input.anchor_artifacts.len() + input.branch_artifacts.len(),
        anchor_count: input.anchor_artifacts.len(),
        branch_count: input.branch_artifacts.len(),
    }
}

fn ensure_output_dir_is_available(output_dir: &Path) -> Result<()> {
    let parent = output_parent_dir(output_dir);
    fs::create_dir_all(parent).map_err(|error| MimirError::io(parent, error))?;

    if output_dir.exists() {
        return Err(MimirError::message(format!(
            "export output directory already exists: {}",
            output_dir.display()
        )));
    }

    Ok(())
}

fn stage_dir_for(output_dir: &Path) -> Result<PathBuf> {
    let parent = output_parent_dir(output_dir);
    let file_name = output_dir
        .file_name()
        .and_then(|value| value.to_str())
        .ok_or_else(|| {
            MimirError::message(format!(
                "export output directory {} must end with a valid UTF-8 path segment",
                output_dir.display()
            ))
        })?;
    let nonce = SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .map_err(|_| MimirError::message("system clock is before UNIX_EPOCH"))?
        .as_nanos();

    for attempt in 0u32..32 {
        let candidate = parent.join(format!(".{file_name}.stage-{nonce}-{attempt}"));
        if !candidate.exists() {
            return Ok(candidate);
        }
    }

    Err(MimirError::message(format!(
        "failed to allocate a unique stage directory for {}",
        output_dir.display()
    )))
}

fn create_stage_root(stage_dir: &Path) -> Result<()> {
    fs::create_dir(stage_dir).map_err(|error| MimirError::io(stage_dir, error))
}

fn create_stage_subdirectory(stage_dir: &Path, artifact_kind: ExportArtifactKind) -> Result<()> {
    let path = stage_dir.join(artifact_kind.relative_directory());
    fs::create_dir_all(&path).map_err(|error| MimirError::io(path, error))
}

fn write_anchor_stage_entry(
    stage_dir: &Path,
    format: ArtifactFormat,
    index: usize,
    artifact: &PersistedAnchorArtifact,
) -> Result<ExportIndexEntry> {
    validate_exported_header(ExportArtifactKind::Anchor, &artifact.header)?;

    let relative_path = format_stage_relative_path(ExportArtifactKind::Anchor, index, format);
    let full_path = resolve_relative_path(stage_dir, &relative_path)?;
    write_anchor_artifact(&full_path, format, artifact)?;

    let content_hash = hash_serializable(artifact)?;
    let entry = ExportIndexEntry {
        artifact_kind: ExportArtifactKind::Anchor,
        record_id: artifact.payload.id.as_str().to_string(),
        relative_path,
        schema_name: artifact.header.schema_name.clone(),
        schema_version: artifact.header.schema_version,
        content_hash,
    };
    let written_header = read_artifact_header_auto(&full_path)?;
    validate_index_entry_header(&entry, &written_header)?;
    let written_artifact: PersistedAnchorArtifact =
        read_artifact_auto(&full_path, ArtifactKind::Anchor.schema())?;
    validate_loaded_anchor_entry(&entry, &written_artifact)?;

    Ok(entry)
}

fn write_branch_stage_entry(
    stage_dir: &Path,
    format: ArtifactFormat,
    index: usize,
    artifact: &PersistedBranchArtifact,
) -> Result<ExportIndexEntry> {
    validate_exported_header(ExportArtifactKind::Branch, &artifact.header)?;

    let relative_path = format_stage_relative_path(ExportArtifactKind::Branch, index, format);
    let full_path = resolve_relative_path(stage_dir, &relative_path)?;
    write_branch_artifact(&full_path, format, artifact)?;

    let content_hash = hash_serializable(artifact)?;
    let entry = ExportIndexEntry {
        artifact_kind: ExportArtifactKind::Branch,
        record_id: artifact.payload.id.as_str().to_string(),
        relative_path,
        schema_name: artifact.header.schema_name.clone(),
        schema_version: artifact.header.schema_version,
        content_hash,
    };
    let written_header = read_artifact_header_auto(&full_path)?;
    validate_index_entry_header(&entry, &written_header)?;
    let written_artifact: PersistedBranchArtifact =
        read_artifact_auto(&full_path, ArtifactKind::Branch.schema())?;
    validate_loaded_branch_entry(&entry, &written_artifact)?;

    Ok(entry)
}

fn format_stage_relative_path(
    artifact_kind: ExportArtifactKind,
    index: usize,
    format: ArtifactFormat,
) -> String {
    format!(
        "{}/{}-{index:04}.{}",
        artifact_kind.relative_directory(),
        artifact_kind.file_stem(),
        format.extension()
    )
}

fn write_json_file<T>(path: &Path, value: &T) -> Result<()>
where
    T: Serialize,
{
    let encoded = serde_json::to_string_pretty(value)?;
    fs::write(path, encoded).map_err(|error| MimirError::io(path, error))
}

fn write_json_file_staged<T>(path: &Path, value: &T) -> Result<()>
where
    T: Serialize,
{
    let parent = path.parent().ok_or_else(|| {
        MimirError::message(format!(
            "staged write target {} must have a parent directory",
            path.display()
        ))
    })?;
    fs::create_dir_all(parent).map_err(|error| MimirError::io(parent, error))?;

    let stage_path = file_stage_path(path)?;
    write_json_file(&stage_path, value)?;

    if path.exists() {
        fs::copy(&stage_path, path).map_err(|error| MimirError::io(path, error))?;
        fs::remove_file(&stage_path).map_err(|error| MimirError::io(&stage_path, error))?;
    } else {
        fs::rename(&stage_path, path).map_err(|error| MimirError::io(path, error))?;
    }

    Ok(())
}

fn empty_execution_result_job_report_index() -> ExecutionResultJobReportIndex {
    ExecutionResultJobReportIndex {
        index_version: EXECUTION_RESULT_JOB_REPORT_INDEX_VERSION,
        entries: Vec::new(),
    }
}

fn empty_execution_result_job_report_collection_summary_index()
-> ExecutionResultJobReportCollectionSummaryIndex {
    ExecutionResultJobReportCollectionSummaryIndex {
        index_version: EXECUTION_RESULT_JOB_REPORT_COLLECTION_SUMMARY_INDEX_VERSION,
        entries: Vec::new(),
    }
}

fn path_to_owned_string(path: &Path) -> Result<String> {
    let path_text = path.to_str().ok_or_else(|| {
        MimirError::message(format!(
            "path {} must be valid UTF-8 for persisted execution result job report indexing",
            path.display()
        ))
    })?;

    Ok(path_text.to_string())
}

fn execution_result_job_report_index_entry_matches_query(
    entry: &ExecutionResultJobReportIndexEntry,
    query: &ExecutionResultJobReportIndexQuery,
) -> bool {
    query
        .job_spec_id
        .as_ref()
        .is_none_or(|job_spec_id| entry.job_spec_id == *job_spec_id)
        && query
            .report_file_path
            .as_ref()
            .is_none_or(|report_file_path| entry.report_file_path == *report_file_path)
        && query
            .export_name
            .as_ref()
            .is_none_or(|export_name| entry.export_name == *export_name)
        && query
            .selection_mode
            .is_none_or(|selection_mode| entry.selection_mode == selection_mode)
        && query
            .source_run_request_id
            .as_ref()
            .is_none_or(|source_run_request_id| {
                entry.source_run_request_id == *source_run_request_id
            })
        && query
            .source_handoff_bundle_id
            .as_ref()
            .is_none_or(|source_handoff_bundle_id| {
                entry.source_handoff_bundle_id == *source_handoff_bundle_id
            })
        && query
            .source_provenance_hash
            .as_ref()
            .is_none_or(|source_provenance_hash| {
                entry.source_provenance_hash == *source_provenance_hash
            })
}

fn execution_result_job_report_collection_summary_index_entry_matches_query(
    entry: &ExecutionResultJobReportCollectionSummaryIndexEntry,
    query: &ExecutionResultJobReportCollectionSummaryIndexQuery,
) -> bool {
    query
        .summary_file_path
        .as_ref()
        .is_none_or(|summary_file_path| entry.summary_file_path == *summary_file_path)
        && query
            .report_count
            .is_none_or(|report_count| entry.report_count == report_count)
        && query
            .total_entry_count
            .is_none_or(|total_entry_count| entry.total_entry_count == total_entry_count)
        && query
            .export_names
            .iter()
            .all(|export_name| entry.export_names.contains(export_name))
        && query
            .selection_modes
            .iter()
            .all(|selection_mode| entry.selection_modes.contains(selection_mode))
        && query
            .source_run_request_ids
            .iter()
            .all(|source_run_request_id| {
                entry.source_run_request_ids.contains(source_run_request_id)
            })
        && query
            .source_handoff_bundle_ids
            .iter()
            .all(|source_handoff_bundle_id| {
                entry
                    .source_handoff_bundle_ids
                    .contains(source_handoff_bundle_id)
            })
}

fn validate_non_empty_file_path(label: &str, path: &str) -> Result<()> {
    if path.trim().is_empty() {
        return Err(MimirError::message(format!("{label} must not be empty")));
    }

    if path_extension(path) != Some("json") {
        return Err(MimirError::message(format!(
            "{label} must end with .json: {path}"
        )));
    }

    Ok(())
}

fn file_stage_path(path: &Path) -> Result<PathBuf> {
    let parent = path.parent().ok_or_else(|| {
        MimirError::message(format!(
            "staged write target {} must have a parent directory",
            path.display()
        ))
    })?;
    let file_name = path
        .file_name()
        .and_then(|value| value.to_str())
        .ok_or_else(|| {
            MimirError::message(format!(
                "staged write target {} must end with a valid UTF-8 path segment",
                path.display()
            ))
        })?;
    let nonce = SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .map_err(|_| MimirError::message("system clock is before UNIX_EPOCH"))?
        .as_nanos();

    for attempt in 0u32..32 {
        let candidate = parent.join(format!(".{file_name}.write-{nonce}-{attempt}"));
        if !candidate.exists() {
            return Ok(candidate);
        }
    }

    Err(MimirError::message(format!(
        "failed to allocate staged write path for {}",
        path.display()
    )))
}

fn validate_manifest(manifest: &ExportManifest) -> Result<()> {
    if manifest.manifest_version != EXPORT_MANIFEST_VERSION {
        return Err(MimirError::message(format!(
            "unsupported export manifest version {}",
            manifest.manifest_version
        )));
    }

    if manifest.export_name.trim().is_empty() {
        return Err(MimirError::message(
            "export manifest name must not be empty",
        ));
    }

    if manifest.producer.trim().is_empty() {
        return Err(MimirError::message(
            "export manifest producer must not be empty",
        ));
    }

    if manifest.relative_index_path != EXPORT_INDEX_FILE_NAME {
        return Err(MimirError::message(format!(
            "unsupported export index location {}; expected {}",
            manifest.relative_index_path, EXPORT_INDEX_FILE_NAME
        )));
    }

    if manifest.artifact_count != manifest.anchor_count + manifest.branch_count {
        return Err(MimirError::message(format!(
            "artifact count mismatch in manifest: {} != {} + {}",
            manifest.artifact_count, manifest.anchor_count, manifest.branch_count
        )));
    }

    Ok(())
}

fn validate_index(manifest: &ExportManifest, index: &ExportIndex) -> Result<()> {
    if index.index_version != EXPORT_INDEX_VERSION {
        return Err(MimirError::message(format!(
            "unsupported export index version {}",
            index.index_version
        )));
    }

    if index.entries.len() != manifest.artifact_count {
        return Err(MimirError::message(format!(
            "export index entry count mismatch: manifest expects {}, index contains {}",
            manifest.artifact_count,
            index.entries.len()
        )));
    }

    let mut anchor_count = 0usize;
    let mut branch_count = 0usize;
    let mut seen_paths = BTreeSet::new();
    let mut seen_anchor_record_ids = BTreeSet::new();
    let mut seen_branch_record_ids = BTreeSet::new();

    for entry in &index.entries {
        validate_relative_path_text(&entry.relative_path)?;

        if path_extension(&entry.relative_path) != Some(manifest.artifact_encoding.extension()) {
            return Err(MimirError::message(format!(
                "index entry {} does not match export encoding {}",
                entry.relative_path,
                manifest.artifact_encoding.extension()
            )));
        }

        if !seen_paths.insert(entry.relative_path.clone()) {
            return Err(MimirError::message(format!(
                "duplicate index relative path {}",
                entry.relative_path
            )));
        }

        if entry.record_id.trim().is_empty() {
            return Err(MimirError::message(format!(
                "index entry {} has an empty record id",
                entry.relative_path
            )));
        }

        let seen_record_ids = match entry.artifact_kind {
            ExportArtifactKind::Anchor => &mut seen_anchor_record_ids,
            ExportArtifactKind::Branch => &mut seen_branch_record_ids,
        };
        if !seen_record_ids.insert(entry.record_id.clone()) {
            return Err(MimirError::message(format!(
                "duplicate {} record id {} in export index",
                entry.artifact_kind.file_stem(),
                entry.record_id
            )));
        }

        if entry.schema_name != entry.artifact_kind.schema_name() {
            return Err(MimirError::message(format!(
                "index entry {} schema mismatch: expected {}, found {}",
                entry.relative_path,
                entry.artifact_kind.schema_name(),
                entry.schema_name
            )));
        }

        if entry.schema_version != entry.artifact_kind.schema_version() {
            return Err(MimirError::message(format!(
                "index entry {} schema version mismatch: expected {}, found {}",
                entry.relative_path,
                entry.artifact_kind.schema_version(),
                entry.schema_version
            )));
        }

        if entry.content_hash.trim().is_empty() {
            return Err(MimirError::message(format!(
                "index entry {} has an empty content hash",
                entry.relative_path
            )));
        }

        match entry.artifact_kind {
            ExportArtifactKind::Anchor => anchor_count += 1,
            ExportArtifactKind::Branch => branch_count += 1,
        }
    }

    if anchor_count != manifest.anchor_count {
        return Err(MimirError::message(format!(
            "anchor count mismatch: manifest expects {}, index contains {}",
            manifest.anchor_count, anchor_count
        )));
    }

    if branch_count != manifest.branch_count {
        return Err(MimirError::message(format!(
            "branch count mismatch: manifest expects {}, index contains {}",
            manifest.branch_count, branch_count
        )));
    }

    Ok(())
}

fn output_parent_dir(output_dir: &Path) -> &Path {
    output_dir
        .parent()
        .filter(|path| !path.as_os_str().is_empty())
        .unwrap_or_else(|| Path::new("."))
}

fn path_extension(relative_path: &str) -> Option<&str> {
    Path::new(relative_path)
        .extension()
        .and_then(|value| value.to_str())
}

fn validate_exported_header(
    artifact_kind: ExportArtifactKind,
    header: &ArtifactHeader,
) -> Result<()> {
    if header.schema_name != artifact_kind.schema_name() {
        return Err(MimirError::message(format!(
            "exported {} artifact schema mismatch: expected {}, found {}",
            artifact_kind.file_stem(),
            artifact_kind.schema_name(),
            header.schema_name
        )));
    }

    if header.schema_version != artifact_kind.schema_version() {
        return Err(MimirError::message(format!(
            "exported {} artifact schema version mismatch: expected {}, found {}",
            artifact_kind.file_stem(),
            artifact_kind.schema_version(),
            header.schema_version
        )));
    }

    Ok(())
}

fn validate_index_entry_header(entry: &ExportIndexEntry, header: &ArtifactHeader) -> Result<()> {
    if header.schema_name != entry.schema_name {
        return Err(MimirError::message(format!(
            "artifact header schema mismatch at {}: index expects {}, file contains {}",
            entry.relative_path, entry.schema_name, header.schema_name
        )));
    }

    if header.schema_version != entry.schema_version {
        return Err(MimirError::message(format!(
            "artifact header schema version mismatch at {}: index expects {}, file contains {}",
            entry.relative_path, entry.schema_version, header.schema_version
        )));
    }

    Ok(())
}

fn validate_loaded_anchor_entry(
    entry: &ExportIndexEntry,
    artifact: &PersistedAnchorArtifact,
) -> Result<()> {
    validate_index_entry_header(entry, &artifact.header)?;

    if entry.record_id != artifact.payload.id.as_str() {
        return Err(MimirError::message(format!(
            "anchor record id mismatch at {}: index expects {}, file contains {}",
            entry.relative_path,
            entry.record_id,
            artifact.payload.id.as_str()
        )));
    }

    let content_hash = hash_serializable(artifact)?;
    if entry.content_hash != content_hash {
        return Err(MimirError::message(format!(
            "anchor content hash mismatch at {}",
            entry.relative_path
        )));
    }

    Ok(())
}

fn validate_loaded_branch_entry(
    entry: &ExportIndexEntry,
    artifact: &PersistedBranchArtifact,
) -> Result<()> {
    validate_index_entry_header(entry, &artifact.header)?;

    if entry.record_id != artifact.payload.id.as_str() {
        return Err(MimirError::message(format!(
            "branch record id mismatch at {}: index expects {}, file contains {}",
            entry.relative_path,
            entry.record_id,
            artifact.payload.id.as_str()
        )));
    }

    let content_hash = hash_serializable(artifact)?;
    if entry.content_hash != content_hash {
        return Err(MimirError::message(format!(
            "branch content hash mismatch at {}",
            entry.relative_path
        )));
    }

    Ok(())
}

fn resolve_relative_path(root: &Path, relative_path: &str) -> Result<PathBuf> {
    let relative = validate_relative_path_text(relative_path)?;
    Ok(root.join(relative))
}

fn validate_relative_path_text(relative_path: &str) -> Result<PathBuf> {
    let path = Path::new(relative_path);

    if path.is_absolute() {
        return Err(MimirError::message(format!(
            "absolute paths are not allowed in export index: {relative_path}"
        )));
    }

    if relative_path.trim().is_empty() {
        return Err(MimirError::message(
            "relative paths in export index must not be empty",
        ));
    }

    let mut normalized = PathBuf::new();
    for component in path.components() {
        match component {
            Component::Normal(value) => normalized.push(value),
            _ => {
                return Err(MimirError::message(format!(
                    "non-normal relative path component is not allowed in export index: {relative_path}"
                )));
            }
        }
    }

    Ok(normalized)
}

#[cfg(test)]
mod tests {
    use super::*;
    use mimir_anchor::ANCHOR_ARTIFACT_PRODUCER;
    use mimir_branch::BRANCH_ARTIFACT_PRODUCER;
    use mimir_types::{
        ActionRecord, AnchorArtifactPayload, AnchorId, AnchorKind, BranchArtifactPayload, BranchId,
        BranchOrigin, FieldValue, FrameIndex, Metadata, ReplayId,
    };
    use serde_json::Value;
    use tempfile::{TempDir, tempdir};

    fn read_json_value(path: &Path) -> Value {
        serde_json::from_slice(&fs::read(path).expect("json file should be readable"))
            .expect("json file should parse")
    }

    fn write_json_value(path: &Path, value: &Value) {
        fs::write(
            path,
            serde_json::to_vec_pretty(value).expect("json value should serialize"),
        )
        .expect("json value should be written");
    }

    fn assert_object_keys(value: &Value, expected_keys: &[&str]) {
        let object = value.as_object().expect("json value should be an object");
        assert_eq!(
            object.len(),
            expected_keys.len(),
            "unexpected key count: {:?}",
            object.keys().collect::<Vec<_>>()
        );

        for key in expected_keys {
            assert!(
                object.contains_key(*key),
                "expected object to contain key {key:?}, got {:?}",
                object.keys().collect::<Vec<_>>()
            );
        }
    }

    #[test]
    fn export_bundle_writes_manifest_index_and_artifacts() {
        let directory = tempdir().expect("tempdir should be created");
        let output_dir = directory.path().join("bundle");
        let input = sample_export_input(ExportEncoding::Json);

        let manifest = export_bundle(&output_dir, &input).expect("bundle export should succeed");

        assert_eq!(manifest.manifest_version, EXPORT_MANIFEST_VERSION);
        assert_eq!(manifest.artifact_count, 2);
        assert!(output_dir.join(EXPORT_MANIFEST_FILE_NAME).exists());
        assert!(output_dir.join(EXPORT_INDEX_FILE_NAME).exists());
        assert!(output_dir.join("anchors").join("anchor-0000.json").exists());
        assert!(
            output_dir
                .join("branches")
                .join("branch-0000.json")
                .exists()
        );
    }

    #[test]
    fn inspect_export_bundle_reads_headers_from_written_artifacts() {
        let directory = tempdir().expect("tempdir should be created");
        let output_dir = directory.path().join("bundle");
        let input = sample_export_input(ExportEncoding::Json);

        export_bundle(&output_dir, &input).expect("bundle export should succeed");
        let inspection =
            inspect_export_bundle(&output_dir).expect("bundle inspection should succeed");

        assert_eq!(inspection.manifest.anchor_count, 1);
        assert_eq!(inspection.manifest.branch_count, 1);
        assert_eq!(inspection.artifacts.len(), 2);
        assert_eq!(inspection.artifacts[0].header.schema_version, 1);
        assert_eq!(inspection.artifacts[1].header.schema_version, 1);
    }

    #[test]
    fn load_export_bundle_round_trips_and_adapts_for_consumer() {
        let directory = tempdir().expect("tempdir should be created");
        let output_dir = directory.path().join("bundle");
        let input = sample_export_input(ExportEncoding::Json);

        export_bundle(&output_dir, &input).expect("bundle export should succeed");
        let loaded = load_export_bundle(&output_dir).expect("bundle load should succeed");
        let consumer = adapt_loaded_export_for_consumer(loaded);

        assert_eq!(consumer.anchors.len(), 1);
        assert_eq!(consumer.branches.len(), 1);
        assert_eq!(consumer.anchors[0].id.as_str(), "anchor-1");
        assert_eq!(consumer.branches[0].id.as_str(), "branch-1");
    }

    #[test]
    fn export_bundle_rejects_existing_output_directory() {
        let directory = tempdir().expect("tempdir should be created");
        let output_dir = directory.path().join("bundle");
        fs::create_dir_all(&output_dir).expect("existing output directory should be created");

        let error = export_bundle(&output_dir, &sample_export_input(ExportEncoding::Json))
            .expect_err("existing output directory should be rejected");

        assert!(error.to_string().contains("already exists"));
    }

    #[test]
    fn load_export_index_rejects_parent_traversal_paths() {
        let directory = tempdir().expect("tempdir should be created");
        let bundle_dir = directory.path().join("bundle");
        fs::create_dir_all(&bundle_dir).expect("bundle directory should be created");

        let manifest = ExportManifest {
            manifest_version: EXPORT_MANIFEST_VERSION,
            export_name: "restore-stage-1".to_string(),
            producer: EXPORT_BUNDLE_PRODUCER.to_string(),
            created_by_component: Some("unit-test".to_string()),
            artifact_encoding: ExportEncoding::Json,
            relative_index_path: EXPORT_INDEX_FILE_NAME.to_string(),
            artifact_count: 1,
            anchor_count: 1,
            branch_count: 0,
        };
        let index = ExportIndex {
            index_version: EXPORT_INDEX_VERSION,
            entries: vec![ExportIndexEntry {
                artifact_kind: ExportArtifactKind::Anchor,
                record_id: "anchor-1".to_string(),
                relative_path: "../escape.json".to_string(),
                schema_name: ArtifactKind::Anchor.schema().name.to_string(),
                schema_version: ArtifactKind::Anchor.schema().version,
                content_hash: "hash".to_string(),
            }],
        };

        write_json_file(&bundle_dir.join(EXPORT_MANIFEST_FILE_NAME), &manifest)
            .expect("manifest should be written");
        write_json_file(&bundle_dir.join(EXPORT_INDEX_FILE_NAME), &index)
            .expect("index should be written");

        let error = load_export_index(&bundle_dir, &manifest)
            .expect_err("parent traversal path should be rejected");

        assert!(
            error
                .to_string()
                .contains("non-normal relative path component")
        );
    }

    #[test]
    fn validate_index_rejects_duplicate_record_ids_within_the_same_artifact_kind() {
        let manifest = ExportManifest {
            manifest_version: EXPORT_MANIFEST_VERSION,
            export_name: "duplicate-anchor-ids".to_string(),
            producer: EXPORT_BUNDLE_PRODUCER.to_string(),
            created_by_component: Some("unit-test".to_string()),
            artifact_encoding: ExportEncoding::Json,
            relative_index_path: EXPORT_INDEX_FILE_NAME.to_string(),
            artifact_count: 2,
            anchor_count: 2,
            branch_count: 0,
        };
        let index = ExportIndex {
            index_version: EXPORT_INDEX_VERSION,
            entries: vec![
                ExportIndexEntry {
                    artifact_kind: ExportArtifactKind::Anchor,
                    record_id: "anchor-duplicate".to_string(),
                    relative_path: "anchors/anchor-0000.json".to_string(),
                    schema_name: ArtifactKind::Anchor.schema().name.to_string(),
                    schema_version: ArtifactKind::Anchor.schema().version,
                    content_hash: "hash-a".to_string(),
                },
                ExportIndexEntry {
                    artifact_kind: ExportArtifactKind::Anchor,
                    record_id: "anchor-duplicate".to_string(),
                    relative_path: "anchors/anchor-0001.json".to_string(),
                    schema_name: ArtifactKind::Anchor.schema().name.to_string(),
                    schema_version: ArtifactKind::Anchor.schema().version,
                    content_hash: "hash-b".to_string(),
                },
            ],
        };

        let error = validate_index(&manifest, &index)
            .expect_err("same-kind duplicate record ids must fail closed");

        assert!(
            error
                .to_string()
                .contains("duplicate anchor record id anchor-duplicate in export index")
        );
    }

    #[test]
    fn validate_index_allows_the_same_textual_record_id_across_artifact_kinds() {
        let manifest = ExportManifest {
            manifest_version: EXPORT_MANIFEST_VERSION,
            export_name: "cross-kind-id-reuse".to_string(),
            producer: EXPORT_BUNDLE_PRODUCER.to_string(),
            created_by_component: Some("unit-test".to_string()),
            artifact_encoding: ExportEncoding::Json,
            relative_index_path: EXPORT_INDEX_FILE_NAME.to_string(),
            artifact_count: 2,
            anchor_count: 1,
            branch_count: 1,
        };
        let index = ExportIndex {
            index_version: EXPORT_INDEX_VERSION,
            entries: vec![
                ExportIndexEntry {
                    artifact_kind: ExportArtifactKind::Anchor,
                    record_id: "shared-id".to_string(),
                    relative_path: "anchors/anchor-0000.json".to_string(),
                    schema_name: ArtifactKind::Anchor.schema().name.to_string(),
                    schema_version: ArtifactKind::Anchor.schema().version,
                    content_hash: "hash-anchor".to_string(),
                },
                ExportIndexEntry {
                    artifact_kind: ExportArtifactKind::Branch,
                    record_id: "shared-id".to_string(),
                    relative_path: "branches/branch-0000.json".to_string(),
                    schema_name: ArtifactKind::Branch.schema().name.to_string(),
                    schema_version: ArtifactKind::Branch.schema().version,
                    content_hash: "hash-branch".to_string(),
                },
            ],
        };

        validate_index(&manifest, &index).expect("cross-kind textual id reuse remains valid");
    }

    #[test]
    fn load_export_bundle_rejects_hash_mismatch() {
        let directory = tempdir().expect("tempdir should be created");
        let output_dir = directory.path().join("bundle");
        let input = sample_export_input(ExportEncoding::Json);

        export_bundle(&output_dir, &input).expect("bundle export should succeed");

        let index_path = output_dir.join(EXPORT_INDEX_FILE_NAME);
        let mut index: ExportIndex = load_json_file(&index_path).expect("index should load");
        index.entries[0].content_hash = "tampered".to_string();
        write_json_file(&index_path, &index).expect("tampered index should write");

        let error = load_export_bundle(&output_dir).expect_err("tampered hash should be rejected");

        assert!(error.to_string().contains("content hash mismatch"));
    }

    #[test]
    fn export_bundle_supports_toml_artifacts_with_json_manifest_and_index() {
        let directory = tempdir().expect("tempdir should be created");
        let output_dir = directory.path().join("bundle");
        let input = sample_export_input(ExportEncoding::Toml);

        export_bundle(&output_dir, &input).expect("bundle export should succeed");
        let loaded = load_export_bundle(&output_dir).expect("bundle load should succeed");

        assert!(output_dir.join("anchors").join("anchor-0000.toml").exists());
        assert!(
            output_dir
                .join("branches")
                .join("branch-0000.toml")
                .exists()
        );
        assert_eq!(loaded.anchor_artifacts.len(), 1);
        assert_eq!(loaded.branch_artifacts.len(), 1);
    }

    #[test]
    fn load_execution_ledger_index_is_empty_before_persisted_results_exist() {
        let directory = tempdir().expect("tempdir should be created");
        let output_dir = directory.path().join("bundle");

        export_bundle(&output_dir, &sample_export_input(ExportEncoding::Json))
            .expect("bundle export should succeed");

        let index = load_execution_ledger_index(&output_dir)
            .expect("empty execution ledger index should load");
        let history = inspect_execution_ledger_history(&output_dir)
            .expect("empty execution ledger history should load");

        assert_eq!(index.ledger_index_version, EXECUTION_LEDGER_INDEX_VERSION);
        assert!(index.entries.is_empty());
        assert!(history.entries.is_empty());
    }

    #[test]
    fn plan_candidate_request_tracks_missing_ids_and_branch_anchor_gaps() {
        let directory = tempdir().expect("tempdir should be created");
        let output_dir = directory.path().join("bundle");

        export_bundle(&output_dir, &sample_export_input(ExportEncoding::Json))
            .expect("bundle export should succeed");
        let consumer = load_sample_consumer_export(&output_dir);
        let request = CandidateRequest {
            request_id: "request-gap".to_string(),
            export_name: consumer.manifest.export_name.clone(),
            anchor_selection: CandidateSelection::Explicit(Vec::new()),
            branch_selection: CandidateSelection::Explicit(vec![
                "branch-1".to_string(),
                "missing-branch".to_string(),
            ]),
            created_by_component: Some("unit-test".to_string()),
        };

        let plan =
            plan_candidate_request(&consumer, &request, "plan-gap").expect("plan should build");

        assert!(plan.selected_anchor_ids.is_empty());
        assert_eq!(plan.selected_branch_ids, vec!["branch-1".to_string()]);
        assert!(plan.missing_anchor_ids.is_empty());
        assert_eq!(plan.missing_branch_ids, vec!["missing-branch".to_string()]);
        assert_eq!(
            plan.unresolved_branch_anchor_ids,
            vec!["anchor-1".to_string()]
        );
    }

    #[test]
    fn persist_execution_result_updates_ledger_and_supports_reload() {
        let directory = tempdir().expect("tempdir should be created");
        let output_dir = directory.path().join("bundle");

        export_bundle(&output_dir, &sample_export_input(ExportEncoding::Json))
            .expect("bundle export should succeed");
        let consumer = load_sample_consumer_export(&output_dir);
        let request = CandidateRequest {
            request_id: "request-success".to_string(),
            export_name: consumer.manifest.export_name.clone(),
            anchor_selection: CandidateSelection::All,
            branch_selection: CandidateSelection::All,
            created_by_component: Some("unit-test".to_string()),
        };
        let plan =
            plan_candidate_request(&consumer, &request, "plan-success").expect("plan should build");
        let result = build_execution_result_stub(
            &plan,
            "result-success",
            ExecutionResultStatus::StubbedSuccess,
            Some("smoke".to_string()),
        )
        .expect("execution result stub should build");

        let entry = persist_execution_result(&output_dir, &result)
            .expect("execution result should persist");
        let loaded_result = load_execution_result(&output_dir, "result-success")
            .expect("execution result should reload");
        let index =
            load_execution_ledger_index(&output_dir).expect("execution ledger index should reload");

        assert_eq!(entry.result_id, "result-success");
        assert_eq!(loaded_result.result_id, "result-success");
        assert_eq!(loaded_result.status, ExecutionResultStatus::StubbedSuccess);
        assert_eq!(index.entries.len(), 1);
        assert!(
            output_dir
                .join(EXECUTION_LEDGER_DIR_NAME)
                .join(EXECUTION_LEDGER_RESULTS_DIR_NAME)
                .join("result-0000.json")
                .exists()
        );
    }

    #[test]
    fn inspect_and_query_execution_ledger_history_filters_results() {
        let directory = tempdir().expect("tempdir should be created");
        let output_dir = directory.path().join("bundle");

        export_bundle(&output_dir, &sample_export_input(ExportEncoding::Json))
            .expect("bundle export should succeed");
        let consumer = load_sample_consumer_export(&output_dir);

        let success_plan = plan_candidate_request(
            &consumer,
            &CandidateRequest {
                request_id: "request-success".to_string(),
                export_name: consumer.manifest.export_name.clone(),
                anchor_selection: CandidateSelection::All,
                branch_selection: CandidateSelection::Explicit(Vec::new()),
                created_by_component: Some("unit-test".to_string()),
            },
            "plan-success",
        )
        .expect("success plan should build");
        let success_result = build_execution_result_stub(
            &success_plan,
            "result-success",
            ExecutionResultStatus::StubbedSuccess,
            Some("success".to_string()),
        )
        .expect("success stub should build");
        persist_execution_result(&output_dir, &success_result)
            .expect("success result should persist");

        let failure_plan = plan_candidate_request(
            &consumer,
            &CandidateRequest {
                request_id: "request-failure".to_string(),
                export_name: consumer.manifest.export_name.clone(),
                anchor_selection: CandidateSelection::Explicit(Vec::new()),
                branch_selection: CandidateSelection::Explicit(vec!["branch-1".to_string()]),
                created_by_component: Some("unit-test".to_string()),
            },
            "plan-failure",
        )
        .expect("failure plan should build");
        let failure_result = build_execution_result_stub(
            &failure_plan,
            "result-failure",
            ExecutionResultStatus::StubbedFailure,
            Some("failure".to_string()),
        )
        .expect("failure stub should build");
        persist_execution_result(&output_dir, &failure_result)
            .expect("failure result should persist");

        let history = inspect_execution_ledger_history(&output_dir)
            .expect("execution ledger history should load");
        let success_entries = query_execution_ledger_history(
            &history,
            &LedgerSelectionQuery {
                status: Some(ExecutionResultStatus::StubbedSuccess),
                ..LedgerSelectionQuery::default()
            },
        );
        let failure_branch_entries = query_execution_ledger_history(
            &history,
            &LedgerSelectionQuery {
                status: Some(ExecutionResultStatus::StubbedFailure),
                branch_id: Some("branch-1".to_string()),
                ..LedgerSelectionQuery::default()
            },
        );
        let anchor_entries = query_execution_ledger_history(
            &history,
            &LedgerSelectionQuery {
                anchor_id: Some("anchor-1".to_string()),
                ..LedgerSelectionQuery::default()
            },
        );

        assert_eq!(history.entries.len(), 2);
        assert_eq!(success_entries.len(), 1);
        assert_eq!(failure_branch_entries.len(), 1);
        assert_eq!(anchor_entries.len(), 1);
        assert_eq!(
            failure_branch_entries[0].index_entry.result_id,
            "result-failure"
        );
    }

    #[test]
    fn canonical_history_surface_preserves_persisted_order_and_filtered_subsets() {
        let (_directory, history) = sample_execution_ledger_history();

        assert_eq!(history.export_name, "restore-stage-1");
        assert_eq!(history.index.entries.len(), 3);
        assert_eq!(history.entries.len(), 3);
        assert_eq!(
            history
                .entries
                .iter()
                .map(|entry| entry.index_entry.result_id.clone())
                .collect::<Vec<_>>(),
            vec![
                "result-shared-older".to_string(),
                "result-failure".to_string(),
                "result-shared-newer".to_string(),
            ]
        );
        assert_eq!(
            history
                .entries
                .iter()
                .map(|entry| entry.result.recorded_at_unix_ms)
                .collect::<Vec<_>>(),
            vec![100, 150, 200]
        );

        let shared_success_entries = query_execution_ledger_history(
            &history,
            &LedgerSelectionQuery {
                request_id: Some("request-shared".to_string()),
                status: Some(ExecutionResultStatus::StubbedSuccess),
                ..LedgerSelectionQuery::default()
            },
        );
        let failure_branch_entries = query_execution_ledger_history(
            &history,
            &LedgerSelectionQuery {
                status: Some(ExecutionResultStatus::StubbedFailure),
                branch_id: Some("branch-1".to_string()),
                ..LedgerSelectionQuery::default()
            },
        );

        assert_eq!(shared_success_entries.len(), 2);
        assert_eq!(
            shared_success_entries
                .iter()
                .map(|entry| entry.index_entry.result_id.clone())
                .collect::<Vec<_>>(),
            vec![
                "result-shared-older".to_string(),
                "result-shared-newer".to_string(),
            ]
        );
        assert_eq!(
            shared_success_entries[0].result.detail.as_deref(),
            Some("older")
        );
        assert_eq!(
            shared_success_entries[1].result.detail.as_deref(),
            Some("newer")
        );
        assert_eq!(failure_branch_entries.len(), 1);
        assert_eq!(
            failure_branch_entries[0].index_entry.result_id,
            "result-failure"
        );
        assert_eq!(
            failure_branch_entries[0].result.plan.selected_branch_ids,
            vec!["branch-1".to_string()]
        );
        assert_eq!(
            failure_branch_entries[0].result.detail.as_deref(),
            Some("failure")
        );
    }

    #[test]
    fn canonical_handoff_surface_matches_explicit_and_queried_history_pipelines() {
        let (_directory, history) = sample_execution_ledger_history();
        let full_history_explicit = build_execution_result_handoff_bundle(
            &history.entries,
            "handoff-full-history",
            ExecutionResultSelectionMode::FullHistory,
        )
        .expect("explicit handoff bundle should build");
        let full_history_from_history = build_handoff_bundle_from_history(
            &history,
            "handoff-full-history",
            ExecutionResultSelectionMode::FullHistory,
        )
        .expect("history handoff bundle should build");

        assert_eq!(full_history_from_history, full_history_explicit);
        assert_handoff_bundle_matches_history_entries(&full_history_explicit, &history.entries);

        let query = LedgerSelectionQuery {
            request_id: Some("request-shared".to_string()),
            status: Some(ExecutionResultStatus::StubbedSuccess),
            ..LedgerSelectionQuery::default()
        };
        let queried_entries = query_execution_ledger_history(&history, &query);
        let explicit_queried_handoff = build_execution_result_handoff_bundle(
            &queried_entries,
            "handoff-query",
            ExecutionResultSelectionMode::FullHistory,
        )
        .expect("explicit queried handoff bundle should build");
        let queried_handoff = query_and_build_execution_result_handoff_bundle(
            &history,
            &query,
            "handoff-query",
            ExecutionResultSelectionMode::FullHistory,
        )
        .expect("queried handoff bundle should build");

        assert_eq!(queried_handoff, explicit_queried_handoff);
        assert_handoff_bundle_matches_history_entries(&queried_handoff, &queried_entries);
    }

    #[test]
    fn canonical_run_request_surface_matches_explicit_handoff_and_query_pipeline() {
        let (_directory, history) = sample_execution_ledger_history();
        let query = LedgerSelectionQuery {
            request_id: Some("request-shared".to_string()),
            status: Some(ExecutionResultStatus::StubbedSuccess),
            ..LedgerSelectionQuery::default()
        };
        let queried_entries = query_execution_ledger_history(&history, &query);
        let explicit_handoff = build_execution_result_handoff_bundle(
            &queried_entries,
            "handoff-run-request",
            ExecutionResultSelectionMode::FullHistory,
        )
        .expect("explicit handoff bundle should build");
        let explicit_run_request = build_execution_result_run_request(
            &explicit_handoff.entries,
            "run-request-query",
            explicit_handoff.handoff_bundle_id.clone(),
            explicit_handoff.export_name.clone(),
            explicit_handoff.selection_mode,
        )
        .expect("explicit run request should build");
        let run_request_from_handoff =
            build_run_request_from_handoff_bundle(&explicit_handoff, "run-request-query")
                .expect("run request from handoff should build");
        let queried_run_request = query_and_build_execution_result_run_request(
            &history,
            &query,
            "handoff-run-request",
            "run-request-query",
            ExecutionResultSelectionMode::FullHistory,
        )
        .expect("queried run request should build");

        assert_eq!(run_request_from_handoff, explicit_run_request);
        assert_eq!(queried_run_request, explicit_run_request);
        assert_run_request_matches_handoff_bundle(&explicit_run_request, &explicit_handoff);
    }

    #[test]
    fn canonical_job_spec_surface_matches_explicit_run_request_and_query_pipeline() {
        let (_directory, history) = sample_execution_ledger_history();
        let query = LedgerSelectionQuery {
            request_id: Some("request-shared".to_string()),
            ..LedgerSelectionQuery::default()
        };
        let queried_entries = query_execution_ledger_history(&history, &query);
        let explicit_handoff = build_execution_result_handoff_bundle(
            &queried_entries,
            "handoff-job-spec",
            ExecutionResultSelectionMode::FullHistory,
        )
        .expect("explicit handoff bundle should build");
        let explicit_run_request =
            build_run_request_from_handoff_bundle(&explicit_handoff, "run-request-job-spec")
                .expect("explicit run request should build");
        let explicit_job_spec = build_execution_result_job_spec(
            &explicit_run_request.entries,
            "job-spec-query",
            explicit_run_request.run_request_id.clone(),
            explicit_run_request.source_handoff_bundle_id.clone(),
            explicit_run_request.export_name.clone(),
            explicit_run_request.selection_mode,
            explicit_run_request.expected_entry_count,
            explicit_run_request.source_provenance_hash.clone(),
        )
        .expect("explicit job spec should build");
        let job_spec_from_run_request =
            build_job_spec_from_run_request(&explicit_run_request, "job-spec-query")
                .expect("job spec from run request should build");
        let queried_job_spec = query_and_build_execution_result_job_spec(
            &history,
            &query,
            "handoff-job-spec",
            "run-request-job-spec",
            "job-spec-query",
            ExecutionResultSelectionMode::FullHistory,
        )
        .expect("queried job spec should build");

        assert_eq!(job_spec_from_run_request, explicit_job_spec);
        assert_eq!(queried_job_spec, explicit_job_spec);
        assert_job_spec_matches_run_request(&explicit_job_spec, &explicit_run_request);
    }

    #[test]
    fn build_execution_result_job_spec_from_full_history_run_request_preserves_order_and_fields() {
        let (_directory, history) = sample_execution_ledger_history();
        let handoff_bundle = build_handoff_bundle_from_history(
            &history,
            "handoff-full-history",
            ExecutionResultSelectionMode::FullHistory,
        )
        .expect("handoff bundle should build");
        let run_request =
            build_run_request_from_handoff_bundle(&handoff_bundle, "run-request-full-history")
                .expect("run request should build");
        let job_spec = build_job_spec_from_run_request(&run_request, "job-spec-full-history")
            .expect("job spec should build");

        assert_eq!(job_spec.job_spec_id, "job-spec-full-history");
        assert_job_spec_matches_run_request(&job_spec, &run_request);
        assert_eq!(
            collect_job_spec_result_ids(&job_spec),
            vec![
                "result-shared-older".to_string(),
                "result-failure".to_string(),
                "result-shared-newer".to_string(),
            ]
        );
    }

    #[test]
    fn build_execution_result_job_spec_from_filtered_pipeline_matches_run_request() {
        let (_directory, history) = sample_execution_ledger_history();
        let filtered_history = query_execution_ledger_history(
            &history,
            &LedgerSelectionQuery {
                status: Some(ExecutionResultStatus::StubbedFailure),
                ..LedgerSelectionQuery::default()
            },
        );
        let handoff_bundle = build_execution_result_handoff_bundle(
            &filtered_history,
            "handoff-filtered",
            ExecutionResultSelectionMode::FullHistory,
        )
        .expect("filtered handoff bundle should build");
        let run_request =
            build_run_request_from_handoff_bundle(&handoff_bundle, "run-request-filtered")
                .expect("filtered run request should build");
        let job_spec = build_job_spec_from_run_request(&run_request, "job-spec-filtered")
            .expect("filtered job spec should build");

        assert_job_spec_matches_run_request(&job_spec, &run_request);
        assert_eq!(
            collect_job_spec_result_ids(&job_spec),
            vec!["result-failure".to_string()]
        );
    }

    #[test]
    fn build_execution_result_job_spec_preserves_latest_only_selection() {
        let (_directory, history) = sample_execution_ledger_history();
        let handoff_bundle = build_handoff_bundle_from_history(
            &history,
            "handoff-latest-only",
            ExecutionResultSelectionMode::LatestOnly,
        )
        .expect("latest-only handoff bundle should build");
        let run_request =
            build_run_request_from_handoff_bundle(&handoff_bundle, "run-request-latest-only")
                .expect("latest-only run request should build");
        let job_spec = build_job_spec_from_run_request(&run_request, "job-spec-latest-only")
            .expect("latest-only job spec should build");

        assert_eq!(
            collect_job_spec_result_ids(&job_spec),
            vec![
                "result-failure".to_string(),
                "result-shared-newer".to_string(),
            ]
        );
        assert_job_spec_matches_run_request(&job_spec, &run_request);
        assert_eq!(job_spec.entries[1].recorded_at_unix_ms, 200);
    }

    #[test]
    fn query_and_build_execution_result_job_spec_matches_explicit_pipeline() {
        let (_directory, history) = sample_execution_ledger_history();
        let query = LedgerSelectionQuery {
            request_id: Some("request-shared".to_string()),
            ..LedgerSelectionQuery::default()
        };
        let queried_history = query_execution_ledger_history(&history, &query);
        let explicit_handoff_bundle = build_execution_result_handoff_bundle(
            &queried_history,
            "handoff-query",
            ExecutionResultSelectionMode::FullHistory,
        )
        .expect("explicit handoff bundle should build");
        let explicit_run_request =
            build_run_request_from_handoff_bundle(&explicit_handoff_bundle, "run-request-query")
                .expect("explicit run request should build");
        let explicit_job_spec =
            build_job_spec_from_run_request(&explicit_run_request, "job-spec-query")
                .expect("explicit job spec should build");
        let queried_job_spec = query_and_build_execution_result_job_spec(
            &history,
            &query,
            "handoff-query",
            "run-request-query",
            "job-spec-query",
            ExecutionResultSelectionMode::FullHistory,
        )
        .expect("queried job spec should build");

        assert_eq!(queried_job_spec, explicit_job_spec);
    }

    #[test]
    fn build_execution_result_job_spec_rejects_entry_count_drift() {
        let (_directory, history) = sample_execution_ledger_history();
        let handoff_bundle = build_handoff_bundle_from_history(
            &history,
            "handoff-entry-count-drift",
            ExecutionResultSelectionMode::FullHistory,
        )
        .expect("handoff bundle should build");
        let run_request =
            build_run_request_from_handoff_bundle(&handoff_bundle, "run-request-entry-count-drift")
                .expect("run request should build");

        let error = build_execution_result_job_spec(
            &run_request.entries,
            "job-spec-entry-count-drift",
            run_request.run_request_id.clone(),
            run_request.source_handoff_bundle_id.clone(),
            run_request.export_name.clone(),
            run_request.selection_mode,
            run_request.expected_entry_count + 1,
            run_request.source_provenance_hash.clone(),
        )
        .expect_err("entry count drift should be rejected");

        assert!(error.to_string().contains("entry count drift"));
    }

    #[test]
    fn build_execution_result_job_spec_rejects_provenance_drift() {
        let (_directory, history) = sample_execution_ledger_history();
        let handoff_bundle = build_handoff_bundle_from_history(
            &history,
            "handoff-provenance-drift",
            ExecutionResultSelectionMode::FullHistory,
        )
        .expect("handoff bundle should build");
        let run_request =
            build_run_request_from_handoff_bundle(&handoff_bundle, "run-request-provenance-drift")
                .expect("run request should build");

        let error = build_execution_result_job_spec(
            &run_request.entries,
            "job-spec-provenance-drift",
            run_request.run_request_id.clone(),
            run_request.source_handoff_bundle_id.clone(),
            run_request.export_name.clone(),
            run_request.selection_mode,
            run_request.expected_entry_count,
            "tampered-provenance".to_string(),
        )
        .expect_err("provenance drift should be rejected");

        assert!(error.to_string().contains("provenance drift"));
    }

    #[test]
    fn validate_execution_result_job_report_accepts_minimal_stub_report() {
        let report = sample_execution_result_job_report();

        validate_execution_result_job_report(&report).expect("minimal stub report should validate");
    }

    #[test]
    fn validate_execution_result_job_report_rejects_entry_count_drift() {
        let mut report = sample_execution_result_job_report();
        report.expected_entry_count += 1;

        let error = validate_execution_result_job_report(&report)
            .expect_err("entry count drift should be rejected");

        assert!(error.to_string().contains("entry count drift"));
    }

    #[test]
    fn validate_execution_result_job_report_rejects_ordinal_drift() {
        let mut report = sample_execution_result_job_report();
        report.entries[1].ordinal = 3;

        let error = validate_execution_result_job_report(&report)
            .expect_err("ordinal drift should be rejected");

        assert!(error.to_string().contains("ordinal drift"));
    }

    #[test]
    fn validate_execution_result_job_report_rejects_empty_provenance_hash() {
        let mut report = sample_execution_result_job_report();
        report.source_provenance_hash.clear();

        let error = validate_execution_result_job_report(&report)
            .expect_err("empty provenance hash should be rejected");

        assert!(error.to_string().contains("must not be empty"));
    }

    #[test]
    fn stub_execution_result_job_executor_preserves_entry_order() {
        let job_spec = sample_execution_result_job_spec(
            ExecutionResultSelectionMode::FullHistory,
            vec![
                sample_execution_result_job_spec_entry(
                    0,
                    "result-c",
                    "request-c",
                    "plan-c",
                    ExecutionResultStatus::StubbedSuccess,
                    300,
                ),
                sample_execution_result_job_spec_entry(
                    1,
                    "result-a",
                    "request-a",
                    "plan-a",
                    ExecutionResultStatus::StubbedFailure,
                    100,
                ),
                sample_execution_result_job_spec_entry(
                    2,
                    "result-b",
                    "request-b",
                    "plan-b",
                    ExecutionResultStatus::StubbedSuccess,
                    200,
                ),
            ],
        );
        let executor = StubExecutionResultJobExecutor;

        let report = executor
            .execute(&job_spec)
            .expect("stub executor should project report");

        assert_eq!(
            report
                .entries
                .iter()
                .map(|entry| entry.result_id.as_str())
                .collect::<Vec<_>>(),
            vec!["result-c", "result-a", "result-b"]
        );
    }

    #[test]
    fn stub_execution_result_job_executor_preserves_provenance_fields() {
        let job_spec = sample_execution_result_job_spec(
            ExecutionResultSelectionMode::FullHistory,
            vec![
                sample_execution_result_job_spec_entry(
                    0,
                    "result-a",
                    "request-a",
                    "plan-a",
                    ExecutionResultStatus::StubbedSuccess,
                    100,
                ),
                sample_execution_result_job_spec_entry(
                    1,
                    "result-b",
                    "request-b",
                    "plan-b",
                    ExecutionResultStatus::StubbedFailure,
                    200,
                ),
            ],
        );
        let executor = StubExecutionResultJobExecutor;

        let report = executor
            .execute(&job_spec)
            .expect("stub executor should project report");

        assert_eq!(report.job_spec_id, job_spec.job_spec_id);
        assert_eq!(report.source_run_request_id, job_spec.source_run_request_id);
        assert_eq!(
            report.source_handoff_bundle_id,
            job_spec.source_handoff_bundle_id
        );
        assert_eq!(report.export_name, job_spec.export_name);
        assert_eq!(report.selection_mode, job_spec.selection_mode);
        assert_eq!(report.expected_entry_count, job_spec.expected_entry_count);
        assert_eq!(
            report.source_provenance_hash,
            job_spec.source_provenance_hash
        );
        assert_eq!(report.entries.len(), job_spec.entries.len());

        for (report_entry, job_entry) in report.entries.iter().zip(&job_spec.entries) {
            assert_eq!(report_entry.ordinal, job_entry.ordinal);
            assert_eq!(report_entry.result_id, job_entry.result_id);
            assert_eq!(report_entry.request_id, job_entry.request_id);
            assert_eq!(report_entry.plan_id, job_entry.plan_id);
        }
    }

    #[test]
    fn stub_execution_result_job_executor_returns_expected_stub_status() {
        let job_spec = sample_execution_result_job_spec(
            ExecutionResultSelectionMode::FullHistory,
            vec![
                sample_execution_result_job_spec_entry(
                    0,
                    "result-a",
                    "request-a",
                    "plan-a",
                    ExecutionResultStatus::StubbedSuccess,
                    100,
                ),
                sample_execution_result_job_spec_entry(
                    1,
                    "result-b",
                    "request-b",
                    "plan-b",
                    ExecutionResultStatus::StubbedFailure,
                    200,
                ),
            ],
        );
        let executor = StubExecutionResultJobExecutor;

        let report = executor
            .execute(&job_spec)
            .expect("stub executor should project report");

        assert!(
            report
                .entries
                .iter()
                .all(|entry| entry.stub_status == ExecutionResultJobReportStatus::StubAccepted)
        );
    }

    #[test]
    fn stub_execution_result_job_executor_output_passes_report_validation() {
        let job_spec = sample_execution_result_job_spec(
            ExecutionResultSelectionMode::FullHistory,
            vec![
                sample_execution_result_job_spec_entry(
                    0,
                    "result-a",
                    "request-a",
                    "plan-a",
                    ExecutionResultStatus::StubbedSuccess,
                    100,
                ),
                sample_execution_result_job_spec_entry(
                    1,
                    "result-b",
                    "request-b",
                    "plan-b",
                    ExecutionResultStatus::StubbedFailure,
                    200,
                ),
            ],
        );
        let executor = StubExecutionResultJobExecutor;

        let report = executor
            .execute(&job_spec)
            .expect("stub executor should project report");

        validate_execution_result_job_report(&report)
            .expect("stub executor output should validate");
    }

    #[test]
    fn stub_execution_result_job_executor_supports_latest_only_single_entry_job_spec() {
        let job_spec = sample_execution_result_job_spec(
            ExecutionResultSelectionMode::LatestOnly,
            vec![sample_execution_result_job_spec_entry(
                0,
                "result-latest",
                "request-latest",
                "plan-latest",
                ExecutionResultStatus::StubbedSuccess,
                500,
            )],
        );
        let executor = StubExecutionResultJobExecutor;

        let report = executor
            .execute(&job_spec)
            .expect("stub executor should project single-entry report");

        assert_eq!(
            report.selection_mode,
            ExecutionResultSelectionMode::LatestOnly
        );
        assert_eq!(report.expected_entry_count, 1);
        assert_eq!(report.entries.len(), 1);
        assert_eq!(report.entries[0].ordinal, 0);
        assert_eq!(report.entries[0].result_id, "result-latest");
        assert_eq!(report.entries[0].request_id, "request-latest");
        assert_eq!(report.entries[0].plan_id, "plan-latest");
        assert_eq!(
            report.entries[0].stub_status,
            ExecutionResultJobReportStatus::StubAccepted
        );
    }

    #[test]
    fn query_and_stub_execute_execution_result_job_spec_matches_injected_stub_helper() {
        let (directory, _) = sample_execution_ledger_history();
        let bundle_dir = directory.path().join("bundle");
        let query = LedgerSelectionQuery {
            status: Some(ExecutionResultStatus::StubbedSuccess),
            anchor_id: Some("anchor-1".to_string()),
            ..LedgerSelectionQuery::default()
        };
        let executor = StubExecutionResultJobExecutor;
        let injected_report = query_and_execute_execution_result_job_spec(
            &bundle_dir,
            &query,
            "handoff-query-execute",
            "run-request-query-execute",
            "job-spec-query-execute",
            ExecutionResultSelectionMode::FullHistory,
            &executor,
        )
        .expect("injected stub convenience helper should execute");
        let default_stub_report = query_and_stub_execute_execution_result_job_spec(
            &bundle_dir,
            &query,
            "handoff-query-execute",
            "run-request-query-execute",
            "job-spec-query-execute",
            ExecutionResultSelectionMode::FullHistory,
        )
        .expect("default stub convenience helper should execute");

        assert_eq!(default_stub_report, injected_report);
    }

    #[test]
    fn query_and_stub_execute_execution_result_job_spec_supports_latest_only_selection() {
        let (directory, _) = sample_execution_ledger_history();
        let bundle_dir = directory.path().join("bundle");
        let query = LedgerSelectionQuery {
            request_id: Some("request-shared".to_string()),
            ..LedgerSelectionQuery::default()
        };

        let report = query_and_stub_execute_execution_result_job_spec(
            &bundle_dir,
            &query,
            "handoff-execute-latest",
            "run-request-execute-latest",
            "job-spec-execute-latest",
            ExecutionResultSelectionMode::LatestOnly,
        )
        .expect("latest-only default stub convenience helper should execute");

        validate_execution_result_job_report(&report)
            .expect("latest-only default stub report should validate");
        assert_eq!(
            report.selection_mode,
            ExecutionResultSelectionMode::LatestOnly
        );
        assert_eq!(report.expected_entry_count, 1);
        assert_eq!(report.entries.len(), 1);
        assert_eq!(report.entries[0].ordinal, 0);
        assert_eq!(report.entries[0].result_id, "result-shared-newer");
    }

    #[test]
    fn query_and_stub_execute_execution_result_job_spec_supports_full_history_selection() {
        let (directory, _) = sample_execution_ledger_history();
        let bundle_dir = directory.path().join("bundle");
        let query = LedgerSelectionQuery {
            request_id: Some("request-shared".to_string()),
            ..LedgerSelectionQuery::default()
        };
        let report = query_and_stub_execute_execution_result_job_spec(
            &bundle_dir,
            &query,
            "handoff-execute-full-history",
            "run-request-execute-full-history",
            "job-spec-execute-full-history",
            ExecutionResultSelectionMode::FullHistory,
        )
        .expect("full-history default stub convenience helper should execute");

        validate_execution_result_job_report(&report)
            .expect("full-history default stub report should validate");
        assert_eq!(
            report.selection_mode,
            ExecutionResultSelectionMode::FullHistory
        );
        assert_eq!(report.expected_entry_count, 2);
        assert_eq!(report.entries.len(), 2);
        assert_eq!(
            report
                .entries
                .iter()
                .map(|entry| entry.result_id.as_str())
                .collect::<Vec<_>>(),
            vec!["result-shared-older", "result-shared-newer"]
        );
    }

    #[test]
    fn query_and_stub_execute_execution_result_job_spec_returns_validated_report() {
        let (directory, _) = sample_execution_ledger_history();
        let bundle_dir = directory.path().join("bundle");
        let query = LedgerSelectionQuery {
            request_id: Some("request-shared".to_string()),
            ..LedgerSelectionQuery::default()
        };

        let report = query_and_stub_execute_execution_result_job_spec(
            &bundle_dir,
            &query,
            "handoff-validate-default-stub",
            "run-request-validate-default-stub",
            "job-spec-validate-default-stub",
            ExecutionResultSelectionMode::LatestOnly,
        )
        .expect("default stub convenience helper should execute");

        validate_execution_result_job_report(&report)
            .expect("default stub convenience helper should return a valid report");
    }

    #[test]
    fn query_stub_execute_persist_load_and_register_execution_result_job_report_matches_explicit_pipeline()
     {
        let (directory, _) = sample_execution_ledger_history();
        let bundle_dir = directory.path().join("bundle");
        let explicit_report_path = directory.path().join("stage9-explicit-report.json");
        let explicit_index_path = directory.path().join("stage9-explicit-index.json");
        let wrapper_report_path = directory.path().join("stage9-wrapper-report.json");
        let wrapper_index_path = directory.path().join("stage9-wrapper-index.json");
        let query = LedgerSelectionQuery {
            status: Some(ExecutionResultStatus::StubbedSuccess),
            anchor_id: Some("anchor-1".to_string()),
            ..LedgerSelectionQuery::default()
        };

        let explicit_report = query_and_stub_execute_execution_result_job_spec(
            &bundle_dir,
            &query,
            "handoff-stage9-explicit",
            "run-request-stage9-explicit",
            "job-spec-stage9-explicit",
            ExecutionResultSelectionMode::FullHistory,
        )
        .expect("explicit stub execute helper should succeed");
        persist_execution_result_job_report(&explicit_report_path, &explicit_report)
            .expect("explicit pipeline should persist report");
        let explicit_loaded = load_execution_result_job_report(&explicit_report_path)
            .expect("explicit pipeline should reload persisted report");
        let explicit_entry = register_execution_result_job_report_in_index(
            &explicit_index_path,
            &explicit_report_path,
            &explicit_loaded,
        )
        .expect("explicit pipeline should register loaded report");
        let explicit_index = load_execution_result_job_report_index(&explicit_index_path)
            .expect("explicit pipeline index should reload");

        let wrapper_loaded =
            query_stub_execute_persist_load_and_register_execution_result_job_report(
                &bundle_dir,
                &query,
                "handoff-stage9-explicit",
                "run-request-stage9-explicit",
                "job-spec-stage9-explicit",
                ExecutionResultSelectionMode::FullHistory,
                &wrapper_report_path,
                &wrapper_index_path,
            )
            .expect("wrapper should execute, persist, reload, and register report");
        let wrapper_reloaded = load_execution_result_job_report(&wrapper_report_path)
            .expect("wrapper report should reload");
        let wrapper_index = load_execution_result_job_report_index(&wrapper_index_path)
            .expect("wrapper index should reload");

        validate_execution_result_job_report_index(&wrapper_index)
            .expect("wrapper index should validate");
        assert_eq!(wrapper_loaded, explicit_loaded);
        assert_eq!(wrapper_reloaded, explicit_loaded);
        assert_eq!(wrapper_index.entries.len(), 1);
        assert_eq!(wrapper_index.entries[0].ordinal, explicit_entry.ordinal);
        assert_eq!(
            wrapper_index.entries[0].job_spec_id,
            explicit_entry.job_spec_id
        );
        assert_eq!(
            wrapper_index.entries[0].source_run_request_id,
            explicit_entry.source_run_request_id
        );
        assert_eq!(
            wrapper_index.entries[0].source_handoff_bundle_id,
            explicit_entry.source_handoff_bundle_id
        );
        assert_eq!(
            wrapper_index.entries[0].export_name,
            explicit_entry.export_name
        );
        assert_eq!(
            wrapper_index.entries[0].selection_mode,
            explicit_entry.selection_mode
        );
        assert_eq!(
            wrapper_index.entries[0].expected_entry_count,
            explicit_entry.expected_entry_count
        );
        assert_eq!(
            wrapper_index.entries[0].source_provenance_hash,
            explicit_entry.source_provenance_hash
        );
        assert_eq!(
            wrapper_index.entries[0].report_file_path,
            path_to_owned_string(&wrapper_report_path)
                .expect("wrapper report path should serialize"),
        );
        assert_eq!(wrapper_index.entries.len(), explicit_index.entries.len());
    }

    #[test]
    fn query_stub_execute_persist_load_and_register_execution_result_job_report_supports_latest_only_selection()
     {
        let (directory, _) = sample_execution_ledger_history();
        let bundle_dir = directory.path().join("bundle");
        let report_path = directory.path().join("stage9-latest-report.json");
        let index_path = directory.path().join("stage9-latest-index.json");
        let query = LedgerSelectionQuery {
            request_id: Some("request-shared".to_string()),
            ..LedgerSelectionQuery::default()
        };

        let report = query_stub_execute_persist_load_and_register_execution_result_job_report(
            &bundle_dir,
            &query,
            "handoff-stage9-latest-only",
            "run-request-stage9-latest-only",
            "job-spec-stage9-latest-only",
            ExecutionResultSelectionMode::LatestOnly,
            &report_path,
            &index_path,
        )
        .expect("latest-only wrapper should succeed");
        let loaded = load_execution_result_job_report(&report_path)
            .expect("latest-only wrapper report should reload");
        let index = load_execution_result_job_report_index(&index_path)
            .expect("latest-only wrapper index should reload");

        validate_execution_result_job_report_index(&index)
            .expect("latest-only wrapper index should validate");
        assert_eq!(report, loaded);
        assert_eq!(
            loaded.selection_mode,
            ExecutionResultSelectionMode::LatestOnly
        );
        assert_eq!(loaded.expected_entry_count, 1);
        assert_eq!(loaded.entries.len(), 1);
        assert_eq!(loaded.entries[0].result_id, "result-shared-newer");
        assert_eq!(index.entries.len(), 1);
        assert_eq!(
            index.entries[0].selection_mode,
            ExecutionResultSelectionMode::LatestOnly
        );
        assert_eq!(index.entries[0].expected_entry_count, 1);
        assert_eq!(
            index.entries[0].report_file_path,
            path_to_owned_string(&report_path).expect("report path should serialize"),
        );
    }

    #[test]
    fn query_stub_execute_persist_load_and_register_execution_result_job_report_supports_full_history_selection()
     {
        let (directory, _) = sample_execution_ledger_history();
        let bundle_dir = directory.path().join("bundle");
        let report_path = directory.path().join("stage9-full-history-report.json");
        let index_path = directory.path().join("stage9-full-history-index.json");
        let query = LedgerSelectionQuery {
            request_id: Some("request-shared".to_string()),
            ..LedgerSelectionQuery::default()
        };

        let report = query_stub_execute_persist_load_and_register_execution_result_job_report(
            &bundle_dir,
            &query,
            "handoff-stage9-full-history",
            "run-request-stage9-full-history",
            "job-spec-stage9-full-history",
            ExecutionResultSelectionMode::FullHistory,
            &report_path,
            &index_path,
        )
        .expect("full-history wrapper should succeed");
        let loaded = load_execution_result_job_report(&report_path)
            .expect("full-history wrapper report should reload");
        let index = load_execution_result_job_report_index(&index_path)
            .expect("full-history wrapper index should reload");

        validate_execution_result_job_report_index(&index)
            .expect("full-history wrapper index should validate");
        assert_eq!(report, loaded);
        assert_eq!(
            loaded.selection_mode,
            ExecutionResultSelectionMode::FullHistory
        );
        assert_eq!(loaded.expected_entry_count, 2);
        assert_eq!(loaded.entries.len(), 2);
        assert_eq!(
            loaded
                .entries
                .iter()
                .map(|entry| entry.result_id.as_str())
                .collect::<Vec<_>>(),
            vec!["result-shared-older", "result-shared-newer"]
        );
        assert_eq!(index.entries.len(), 1);
        assert_eq!(
            index.entries[0].selection_mode,
            ExecutionResultSelectionMode::FullHistory
        );
        assert_eq!(index.entries[0].expected_entry_count, 2);
    }

    #[test]
    fn query_stub_execute_persist_load_and_register_execution_result_job_report_preserves_report_fields()
     {
        let (directory, _) = sample_execution_ledger_history();
        let bundle_dir = directory.path().join("bundle");
        let explicit_report_path = directory
            .path()
            .join("stage9-field-drift-explicit-report.json");
        let explicit_index_path = directory
            .path()
            .join("stage9-field-drift-explicit-index.json");
        let wrapper_report_path = directory
            .path()
            .join("stage9-field-drift-wrapper-report.json");
        let wrapper_index_path = directory
            .path()
            .join("stage9-field-drift-wrapper-index.json");
        let query = LedgerSelectionQuery {
            request_id: Some("request-shared".to_string()),
            ..LedgerSelectionQuery::default()
        };

        let explicit_report = query_and_stub_execute_execution_result_job_spec(
            &bundle_dir,
            &query,
            "handoff-stage9-field-drift",
            "run-request-stage9-field-drift",
            "job-spec-stage9-field-drift",
            ExecutionResultSelectionMode::LatestOnly,
        )
        .expect("explicit stub execute helper should succeed");
        persist_execution_result_job_report(&explicit_report_path, &explicit_report)
            .expect("explicit pipeline should persist report");
        let explicit_loaded = load_execution_result_job_report(&explicit_report_path)
            .expect("explicit pipeline should reload persisted report");
        let explicit_entry = register_execution_result_job_report_in_index(
            &explicit_index_path,
            &explicit_report_path,
            &explicit_loaded,
        )
        .expect("explicit pipeline should register loaded report");

        let wrapper_loaded =
            query_stub_execute_persist_load_and_register_execution_result_job_report(
                &bundle_dir,
                &query,
                "handoff-stage9-field-drift",
                "run-request-stage9-field-drift",
                "job-spec-stage9-field-drift",
                ExecutionResultSelectionMode::LatestOnly,
                &wrapper_report_path,
                &wrapper_index_path,
            )
            .expect("wrapper should preserve report fields");
        let wrapper_reloaded = load_execution_result_job_report(&wrapper_report_path)
            .expect("wrapper report should reload");
        let wrapper_index = load_execution_result_job_report_index(&wrapper_index_path)
            .expect("wrapper index should reload");

        validate_execution_result_job_report_index(&wrapper_index)
            .expect("wrapper index should validate");
        assert_eq!(wrapper_loaded, explicit_loaded);
        assert_eq!(wrapper_reloaded, explicit_loaded);
        assert_eq!(wrapper_index.entries.len(), 1);
        assert_eq!(wrapper_index.entries[0].ordinal, explicit_entry.ordinal);
        assert_eq!(
            wrapper_index.entries[0].job_spec_id,
            explicit_loaded.job_spec_id
        );
        assert_eq!(
            wrapper_index.entries[0].source_run_request_id,
            explicit_loaded.source_run_request_id
        );
        assert_eq!(
            wrapper_index.entries[0].source_handoff_bundle_id,
            explicit_loaded.source_handoff_bundle_id
        );
        assert_eq!(
            wrapper_index.entries[0].export_name,
            explicit_loaded.export_name
        );
        assert_eq!(
            wrapper_index.entries[0].source_provenance_hash,
            explicit_loaded.source_provenance_hash
        );
        assert_eq!(
            wrapper_index.entries[0].report_file_path,
            path_to_owned_string(&wrapper_report_path)
                .expect("wrapper report path should serialize"),
        );
    }

    #[test]
    fn query_stub_execute_persist_load_register_query_and_load_execution_result_job_reports_matches_explicit_pipeline()
     {
        let (directory, _) = sample_execution_ledger_history();
        let bundle_dir = directory.path().join("bundle");
        let explicit_report_path = directory.path().join("stage14-explicit-report.json");
        let explicit_index_path = directory.path().join("stage14-explicit-index.json");
        let wrapper_report_path = directory.path().join("stage14-wrapper-report.json");
        let wrapper_index_path = directory.path().join("stage14-wrapper-index.json");
        let query = LedgerSelectionQuery {
            status: Some(ExecutionResultStatus::StubbedSuccess),
            anchor_id: Some("anchor-1".to_string()),
            ..LedgerSelectionQuery::default()
        };
        let report_index_query = ExecutionResultJobReportIndexQuery {
            job_spec_id: Some("job-spec-stage14-match".to_string()),
            ..ExecutionResultJobReportIndexQuery::default()
        };

        query_stub_execute_persist_load_and_register_execution_result_job_report(
            &bundle_dir,
            &query,
            "handoff-stage14-match",
            "run-request-stage14-match",
            "job-spec-stage14-match",
            ExecutionResultSelectionMode::FullHistory,
            &explicit_report_path,
            &explicit_index_path,
        )
        .expect("explicit stage14 helper should succeed");
        let explicit_selection = load_and_query_execution_result_job_report_index(
            &explicit_index_path,
            &report_index_query,
        )
        .expect("explicit stage14 index query should succeed");
        let explicit_loaded =
            load_selected_execution_result_job_reports(&explicit_selection.selected_entries)
                .expect("explicit stage14 selected reports should load");

        let wrapper_loaded =
            query_stub_execute_persist_load_register_query_and_load_execution_result_job_reports(
                &bundle_dir,
                &query,
                "handoff-stage14-match",
                "run-request-stage14-match",
                "job-spec-stage14-match",
                ExecutionResultSelectionMode::FullHistory,
                &wrapper_report_path,
                &wrapper_index_path,
                &report_index_query,
            )
            .expect("stage14 wrapper should match explicit pipeline");

        assert_eq!(wrapper_loaded, explicit_loaded);
        for report in &wrapper_loaded {
            validate_execution_result_job_report(report)
                .expect("stage14 wrapper-loaded report should validate");
        }
    }

    #[test]
    fn query_stub_execute_persist_load_register_query_and_load_execution_result_job_reports_latest_only_returns_exactly_one_loaded_report()
     {
        let (directory, _) = sample_execution_ledger_history();
        let bundle_dir = directory.path().join("bundle");
        let index_path = directory.path().join("stage14-latest-index.json");
        let first_report_path = directory.path().join("stage14-latest-first-report.json");
        let wrapper_report_path = directory.path().join("stage14-latest-wrapper-report.json");
        let ledger_query = LedgerSelectionQuery {
            request_id: Some("request-shared".to_string()),
            ..LedgerSelectionQuery::default()
        };

        query_stub_execute_persist_load_and_register_execution_result_job_report(
            &bundle_dir,
            &ledger_query,
            "handoff-stage14-latest-shared",
            "run-request-stage14-latest-shared",
            "job-spec-stage14-latest-first",
            ExecutionResultSelectionMode::FullHistory,
            &first_report_path,
            &index_path,
        )
        .expect("first stage14 latest report should register");

        let report_index_query = ExecutionResultJobReportIndexQuery {
            source_run_request_id: Some("run-request-stage14-latest-shared".to_string()),
            source_handoff_bundle_id: Some("handoff-stage14-latest-shared".to_string()),
            latest_only: true,
            ..ExecutionResultJobReportIndexQuery::default()
        };

        let wrapper_loaded =
            query_stub_execute_persist_load_register_query_and_load_execution_result_job_reports(
                &bundle_dir,
                &ledger_query,
                "handoff-stage14-latest-shared",
                "run-request-stage14-latest-shared",
                "job-spec-stage14-latest-second",
                ExecutionResultSelectionMode::LatestOnly,
                &wrapper_report_path,
                &index_path,
                &report_index_query,
            )
            .expect("stage14 latest-only wrapper should succeed");
        let explicit_selection =
            load_and_query_execution_result_job_report_index(&index_path, &report_index_query)
                .expect("explicit latest-only query should succeed");
        let explicit_loaded =
            load_selected_execution_result_job_reports(&explicit_selection.selected_entries)
                .expect("explicit latest-only selected reports should load");

        assert_eq!(wrapper_loaded, explicit_loaded);
        assert_eq!(wrapper_loaded.len(), 1);
        validate_execution_result_job_report(&wrapper_loaded[0])
            .expect("latest-only wrapper-loaded report should validate");
        assert_eq!(
            wrapper_loaded[0].job_spec_id,
            "job-spec-stage14-latest-second"
        );
    }

    #[test]
    fn query_stub_execute_persist_load_register_query_and_load_execution_result_job_reports_full_history_returns_all_matches_in_index_order()
     {
        let (directory, _) = sample_execution_ledger_history();
        let bundle_dir = directory.path().join("bundle");
        let index_path = directory.path().join("stage14-full-history-index.json");
        let first_report_path = directory
            .path()
            .join("stage14-full-history-first-report.json");
        let second_report_path = directory
            .path()
            .join("stage14-full-history-second-report.json");
        let wrapper_report_path = directory
            .path()
            .join("stage14-full-history-wrapper-report.json");
        let ledger_query = LedgerSelectionQuery {
            request_id: Some("request-shared".to_string()),
            ..LedgerSelectionQuery::default()
        };

        query_stub_execute_persist_load_and_register_execution_result_job_report(
            &bundle_dir,
            &ledger_query,
            "handoff-stage14-full-history-shared",
            "run-request-stage14-full-history-shared",
            "job-spec-stage14-full-history-first",
            ExecutionResultSelectionMode::FullHistory,
            &first_report_path,
            &index_path,
        )
        .expect("first stage14 full-history report should register");
        query_stub_execute_persist_load_and_register_execution_result_job_report(
            &bundle_dir,
            &ledger_query,
            "handoff-stage14-full-history-shared",
            "run-request-stage14-full-history-shared",
            "job-spec-stage14-full-history-second",
            ExecutionResultSelectionMode::LatestOnly,
            &second_report_path,
            &index_path,
        )
        .expect("second stage14 full-history report should register");

        let report_index_query = ExecutionResultJobReportIndexQuery {
            source_run_request_id: Some("run-request-stage14-full-history-shared".to_string()),
            source_handoff_bundle_id: Some("handoff-stage14-full-history-shared".to_string()),
            ..ExecutionResultJobReportIndexQuery::default()
        };

        let wrapper_loaded =
            query_stub_execute_persist_load_register_query_and_load_execution_result_job_reports(
                &bundle_dir,
                &ledger_query,
                "handoff-stage14-full-history-shared",
                "run-request-stage14-full-history-shared",
                "job-spec-stage14-full-history-third",
                ExecutionResultSelectionMode::FullHistory,
                &wrapper_report_path,
                &index_path,
                &report_index_query,
            )
            .expect("stage14 full-history wrapper should succeed");
        let explicit_selection =
            load_and_query_execution_result_job_report_index(&index_path, &report_index_query)
                .expect("explicit full-history query should succeed");
        let explicit_loaded =
            load_selected_execution_result_job_reports(&explicit_selection.selected_entries)
                .expect("explicit full-history selected reports should load");

        assert_eq!(wrapper_loaded, explicit_loaded);
        assert_eq!(wrapper_loaded.len(), 3);
        assert_eq!(
            wrapper_loaded
                .iter()
                .map(|report| report.job_spec_id.as_str())
                .collect::<Vec<_>>(),
            vec![
                "job-spec-stage14-full-history-first",
                "job-spec-stage14-full-history-second",
                "job-spec-stage14-full-history-third",
            ]
        );
        for report in &wrapper_loaded {
            validate_execution_result_job_report(report)
                .expect("full-history wrapper-loaded report should validate");
        }
    }

    #[test]
    fn query_stub_execute_persist_load_register_query_and_load_execution_result_job_reports_preserves_report_fields_without_drift()
     {
        let (directory, _) = sample_execution_ledger_history();
        let bundle_dir = directory.path().join("bundle");
        let index_path = directory.path().join("stage14-field-drift-index.json");
        let first_report_path = directory
            .path()
            .join("stage14-field-drift-first-report.json");
        let explicit_report_path = directory
            .path()
            .join("stage14-field-drift-explicit-report.json");
        let wrapper_report_path = directory
            .path()
            .join("stage14-field-drift-wrapper-report.json");
        let ledger_query = LedgerSelectionQuery {
            request_id: Some("request-shared".to_string()),
            ..LedgerSelectionQuery::default()
        };

        query_stub_execute_persist_load_and_register_execution_result_job_report(
            &bundle_dir,
            &ledger_query,
            "handoff-stage14-field-drift-shared",
            "run-request-stage14-field-drift-shared",
            "job-spec-stage14-field-drift-first",
            ExecutionResultSelectionMode::FullHistory,
            &first_report_path,
            &index_path,
        )
        .expect("first stage14 field-drift report should register");

        let report_index_query = ExecutionResultJobReportIndexQuery {
            source_run_request_id: Some("run-request-stage14-field-drift-shared".to_string()),
            source_handoff_bundle_id: Some("handoff-stage14-field-drift-shared".to_string()),
            ..ExecutionResultJobReportIndexQuery::default()
        };

        query_stub_execute_persist_load_and_register_execution_result_job_report(
            &bundle_dir,
            &ledger_query,
            "handoff-stage14-field-drift-shared",
            "run-request-stage14-field-drift-shared",
            "job-spec-stage14-field-drift-second",
            ExecutionResultSelectionMode::LatestOnly,
            &explicit_report_path,
            &index_path,
        )
        .expect("explicit stage14 field-drift report should register");
        let explicit_selection =
            load_and_query_execution_result_job_report_index(&index_path, &report_index_query)
                .expect("explicit field-drift query should succeed");
        let explicit_loaded =
            load_selected_execution_result_job_reports(&explicit_selection.selected_entries)
                .expect("explicit field-drift selected reports should load");

        let wrapper_loaded =
            query_stub_execute_persist_load_register_query_and_load_execution_result_job_reports(
                &bundle_dir,
                &ledger_query,
                "handoff-stage14-field-drift-shared",
                "run-request-stage14-field-drift-shared",
                "job-spec-stage14-field-drift-third",
                ExecutionResultSelectionMode::FullHistory,
                &wrapper_report_path,
                &index_path,
                &report_index_query,
            )
            .expect("stage14 field-drift wrapper should succeed");

        assert_eq!(wrapper_loaded.len(), 3);
        assert_eq!(wrapper_loaded[0], explicit_loaded[0]);
        assert_eq!(wrapper_loaded[1], explicit_loaded[1]);
        assert_eq!(
            wrapper_loaded[2].job_spec_id,
            "job-spec-stage14-field-drift-third"
        );
        assert_eq!(
            wrapper_loaded[2].source_run_request_id,
            "run-request-stage14-field-drift-shared"
        );
        assert_eq!(
            wrapper_loaded[2].source_handoff_bundle_id,
            "handoff-stage14-field-drift-shared"
        );
        for report in &wrapper_loaded {
            validate_execution_result_job_report(report)
                .expect("field-drift wrapper-loaded report should validate");
        }
    }

    #[test]
    fn summarize_execution_result_job_reports_reports_exact_report_and_entry_counts() {
        let reports = sample_queryable_execution_result_job_reports();

        let summary = summarize_execution_result_job_reports(&reports);

        assert_eq!(summary.report_count, 3);
        assert_eq!(summary.total_entry_count, 6);
    }

    #[test]
    fn summarize_execution_result_job_reports_preserves_deterministic_job_spec_id_order() {
        let reports = sample_queryable_execution_result_job_reports();

        let summary = summarize_execution_result_job_reports(&reports);

        assert_eq!(
            summary.job_spec_ids,
            vec![
                "job-spec-alpha".to_string(),
                "job-spec-beta".to_string(),
                "job-spec-gamma".to_string(),
            ]
        );
    }

    fn sample_execution_ledger_history() -> (TempDir, ExecutionLedgerHistory) {
        let directory = tempdir().expect("tempdir should be created");
        let output_dir = directory.path().join("bundle");

        export_bundle(&output_dir, &sample_export_input(ExportEncoding::Json))
            .expect("bundle export should succeed");
        let consumer = load_sample_consumer_export(&output_dir);

        persist_sample_execution_result(
            &output_dir,
            &consumer,
            "request-shared",
            "plan-shared",
            "result-shared-older",
            ExecutionResultStatus::StubbedSuccess,
            100,
            CandidateSelection::All,
            CandidateSelection::Explicit(Vec::new()),
            Some("older"),
        );
        persist_sample_execution_result(
            &output_dir,
            &consumer,
            "request-failure",
            "plan-failure",
            "result-failure",
            ExecutionResultStatus::StubbedFailure,
            150,
            CandidateSelection::Explicit(Vec::new()),
            CandidateSelection::Explicit(vec!["branch-1".to_string()]),
            Some("failure"),
        );
        persist_sample_execution_result(
            &output_dir,
            &consumer,
            "request-shared",
            "plan-shared",
            "result-shared-newer",
            ExecutionResultStatus::StubbedSuccess,
            200,
            CandidateSelection::All,
            CandidateSelection::Explicit(Vec::new()),
            Some("newer"),
        );

        let history = inspect_execution_ledger_history(&output_dir)
            .expect("execution ledger history should load");

        (directory, history)
    }

    #[allow(clippy::too_many_arguments)]
    fn persist_sample_execution_result(
        output_dir: &Path,
        consumer: &ConsumerExport,
        request_id: &str,
        plan_id: &str,
        result_id: &str,
        status: ExecutionResultStatus,
        recorded_at_unix_ms: u64,
        anchor_selection: CandidateSelection,
        branch_selection: CandidateSelection,
        detail: Option<&str>,
    ) {
        let plan = plan_candidate_request(
            consumer,
            &CandidateRequest {
                request_id: request_id.to_string(),
                export_name: consumer.manifest.export_name.clone(),
                anchor_selection,
                branch_selection,
                created_by_component: Some("unit-test".to_string()),
            },
            plan_id,
        )
        .expect("plan should build");
        let mut result =
            build_execution_result_stub(&plan, result_id, status, detail.map(str::to_string))
                .expect("execution result stub should build");
        result.recorded_at_unix_ms = recorded_at_unix_ms;

        persist_execution_result(output_dir, &result).expect("execution result should persist");
    }

    fn assert_job_spec_matches_run_request(
        job_spec: &ExecutionResultJobSpec,
        run_request: &ExecutionResultRunRequest,
    ) {
        assert_eq!(job_spec.source_run_request_id, run_request.run_request_id);
        assert_eq!(
            job_spec.source_handoff_bundle_id,
            run_request.source_handoff_bundle_id
        );
        assert_eq!(job_spec.export_name, run_request.export_name);
        assert_eq!(job_spec.selection_mode, run_request.selection_mode);
        assert_eq!(
            job_spec.expected_entry_count,
            run_request.expected_entry_count
        );
        assert_eq!(
            job_spec.source_provenance_hash,
            run_request.source_provenance_hash
        );
        assert_eq!(job_spec.entries.len(), run_request.entries.len());

        for (job_entry, request_entry) in job_spec.entries.iter().zip(&run_request.entries) {
            assert_eq!(job_entry.ordinal, request_entry.ordinal);
            assert_eq!(job_entry.result_id, request_entry.result_id);
            assert_eq!(job_entry.request_id, request_entry.request_id);
            assert_eq!(job_entry.plan_id, request_entry.plan_id);
            assert_eq!(job_entry.status, request_entry.status);
            assert_eq!(
                job_entry.recorded_at_unix_ms,
                request_entry.recorded_at_unix_ms
            );
            assert_eq!(
                job_entry.selected_anchor_ids,
                request_entry.selected_anchor_ids
            );
            assert_eq!(
                job_entry.selected_branch_ids,
                request_entry.selected_branch_ids
            );
            assert_eq!(job_entry.detail, request_entry.detail);
        }
    }

    fn assert_handoff_bundle_matches_history_entries(
        handoff_bundle: &ExecutionResultHandoffBundle,
        history_entries: &[ExecutionLedgerHistoryEntry],
    ) {
        assert_eq!(handoff_bundle.entry_count, handoff_bundle.entries.len());
        assert_eq!(handoff_bundle.entries.len(), history_entries.len());

        for (expected_ordinal, (handoff_entry, history_entry)) in handoff_bundle
            .entries
            .iter()
            .zip(history_entries)
            .enumerate()
        {
            assert_eq!(handoff_entry.ordinal, expected_ordinal);
            assert_eq!(handoff_entry.result_id, history_entry.index_entry.result_id);
            assert_eq!(
                handoff_entry.request_id,
                history_entry.index_entry.request_id
            );
            assert_eq!(handoff_entry.plan_id, history_entry.index_entry.plan_id);
            assert_eq!(handoff_entry.status, history_entry.result.status);
            assert_eq!(
                handoff_entry.recorded_at_unix_ms,
                history_entry.result.recorded_at_unix_ms
            );
            assert_eq!(
                handoff_entry.selected_anchor_ids,
                history_entry.result.plan.selected_anchor_ids
            );
            assert_eq!(
                handoff_entry.selected_branch_ids,
                history_entry.result.plan.selected_branch_ids
            );
            assert_eq!(handoff_entry.detail, history_entry.result.detail);
        }
    }

    fn assert_run_request_matches_handoff_bundle(
        run_request: &ExecutionResultRunRequest,
        handoff_bundle: &ExecutionResultHandoffBundle,
    ) {
        assert_eq!(
            run_request.source_handoff_bundle_id,
            handoff_bundle.handoff_bundle_id
        );
        assert_eq!(run_request.export_name, handoff_bundle.export_name);
        assert_eq!(run_request.selection_mode, handoff_bundle.selection_mode);
        assert_eq!(run_request.expected_entry_count, handoff_bundle.entry_count);
        assert_eq!(
            run_request.source_provenance_hash,
            handoff_bundle.provenance_hash
        );
        assert_eq!(run_request.entries.len(), handoff_bundle.entries.len());

        for (request_entry, handoff_entry) in
            run_request.entries.iter().zip(&handoff_bundle.entries)
        {
            assert_eq!(request_entry.ordinal, handoff_entry.ordinal);
            assert_eq!(request_entry.result_id, handoff_entry.result_id);
            assert_eq!(request_entry.request_id, handoff_entry.request_id);
            assert_eq!(request_entry.plan_id, handoff_entry.plan_id);
            assert_eq!(request_entry.status, handoff_entry.status);
            assert_eq!(
                request_entry.recorded_at_unix_ms,
                handoff_entry.recorded_at_unix_ms
            );
            assert_eq!(
                request_entry.selected_anchor_ids,
                handoff_entry.selected_anchor_ids
            );
            assert_eq!(
                request_entry.selected_branch_ids,
                handoff_entry.selected_branch_ids
            );
            assert_eq!(request_entry.detail, handoff_entry.detail);
        }
    }

    fn collect_job_spec_result_ids(job_spec: &ExecutionResultJobSpec) -> Vec<String> {
        job_spec
            .entries
            .iter()
            .map(|entry| entry.result_id.clone())
            .collect()
    }

    fn sample_execution_result_job_report() -> ExecutionResultJobReport {
        ExecutionResultJobReport {
            job_spec_id: "job-spec-stub".to_string(),
            source_run_request_id: "run-request-stub".to_string(),
            source_handoff_bundle_id: "handoff-stub".to_string(),
            export_name: "restore-stage-1".to_string(),
            selection_mode: ExecutionResultSelectionMode::FullHistory,
            expected_entry_count: 2,
            source_provenance_hash: "provenance-hash".to_string(),
            entries: vec![
                ExecutionResultJobReportEntry {
                    ordinal: 0,
                    result_id: "result-a".to_string(),
                    request_id: "request-a".to_string(),
                    plan_id: "plan-a".to_string(),
                    stub_status: ExecutionResultJobReportStatus::Ready,
                },
                ExecutionResultJobReportEntry {
                    ordinal: 1,
                    result_id: "result-b".to_string(),
                    request_id: "request-b".to_string(),
                    plan_id: "plan-b".to_string(),
                    stub_status: ExecutionResultJobReportStatus::StubAccepted,
                },
            ],
        }
    }

    fn sample_execution_result_job_report_latest_only() -> ExecutionResultJobReport {
        ExecutionResultJobReport {
            job_spec_id: "job-spec-latest-only".to_string(),
            source_run_request_id: "run-request-latest-only".to_string(),
            source_handoff_bundle_id: "handoff-latest-only".to_string(),
            export_name: "restore-stage-5-latest-only".to_string(),
            selection_mode: ExecutionResultSelectionMode::LatestOnly,
            expected_entry_count: 1,
            source_provenance_hash: "latest-only-provenance-hash".to_string(),
            entries: vec![ExecutionResultJobReportEntry {
                ordinal: 0,
                result_id: "result-latest".to_string(),
                request_id: "request-latest".to_string(),
                plan_id: "plan-latest".to_string(),
                stub_status: ExecutionResultJobReportStatus::StubAccepted,
            }],
        }
    }

    #[test]
    fn persist_and_load_execution_result_job_report_round_trips_exactly() {
        let directory = tempdir().expect("tempdir should be created");
        let report_path = directory.path().join("execution-result-job-report.json");
        let report = sample_execution_result_job_report();

        persist_execution_result_job_report(&report_path, &report)
            .expect("job report should persist");
        let loaded = load_execution_result_job_report(&report_path)
            .expect("job report should reload after persist");

        assert_eq!(loaded, report);
    }

    #[test]
    fn execution_result_job_report_persisted_json_schema_stays_stable() {
        let directory = tempdir().expect("tempdir should be created");
        let report_path = directory
            .path()
            .join("execution-result-job-report-schema.json");
        let report = sample_execution_result_job_report();

        persist_execution_result_job_report(&report_path, &report)
            .expect("job report should persist");

        let persisted = read_json_value(&report_path);
        assert_object_keys(
            &persisted,
            &[
                "job_spec_id",
                "source_run_request_id",
                "source_handoff_bundle_id",
                "export_name",
                "selection_mode",
                "expected_entry_count",
                "source_provenance_hash",
                "entries",
            ],
        );
        let object = persisted.as_object().expect("report should be an object");
        assert_eq!(
            object.get("selection_mode"),
            Some(&Value::String("full_history".to_string()))
        );

        let entries = object
            .get("entries")
            .and_then(Value::as_array)
            .expect("entries should be an array");
        assert_eq!(entries.len(), 2);
        assert_object_keys(
            &entries[0],
            &[
                "ordinal",
                "result_id",
                "request_id",
                "plan_id",
                "stub_status",
            ],
        );
        assert_eq!(
            entries[0]["stub_status"],
            Value::String("ready".to_string())
        );
        assert_eq!(
            entries[1]["stub_status"],
            Value::String("stub_accepted".to_string())
        );

        let loaded = load_execution_result_job_report(&report_path)
            .expect("persisted report should reload through canonical loader");
        assert_eq!(loaded, report);
        assert_eq!(
            serde_json::to_value(&loaded).expect("loaded report should convert to json"),
            persisted
        );
    }

    #[test]
    fn execution_result_job_report_load_rejects_unknown_fields_in_persisted_json() {
        let directory = tempdir().expect("tempdir should be created");
        let report_path = directory
            .path()
            .join("execution-result-job-report-schema-invalid.json");
        let report = sample_execution_result_job_report();

        persist_execution_result_job_report(&report_path, &report)
            .expect("job report should persist");

        let mut top_level_unknown = read_json_value(&report_path);
        top_level_unknown
            .as_object_mut()
            .expect("report should be an object")
            .insert(
                "unexpected_top_level".to_string(),
                Value::String("drift".to_string()),
            );
        write_json_value(&report_path, &top_level_unknown);
        let top_level_error = load_execution_result_job_report(&report_path)
            .expect_err("unknown report top-level field should be rejected");
        assert!(
            top_level_error.to_string().contains("unknown field"),
            "unexpected error: {top_level_error}"
        );

        persist_execution_result_job_report(&report_path, &report)
            .expect("report should repersist cleanly");
        let mut nested_unknown = read_json_value(&report_path);
        nested_unknown["entries"][0]
            .as_object_mut()
            .expect("report entry should be an object")
            .insert(
                "unexpected_entry_field".to_string(),
                Value::String("drift".to_string()),
            );
        write_json_value(&report_path, &nested_unknown);
        let nested_error = load_execution_result_job_report(&report_path)
            .expect_err("unknown report entry field should be rejected");
        assert!(
            nested_error.to_string().contains("unknown field"),
            "unexpected error: {nested_error}"
        );
    }

    #[test]
    fn load_execution_result_job_report_round_trips_latest_only_single_entry() {
        let directory = tempdir().expect("tempdir should be created");
        let report_path = directory
            .path()
            .join("execution-result-job-report-latest.json");
        let report = sample_execution_result_job_report_latest_only();

        persist_execution_result_job_report(&report_path, &report)
            .expect("latest-only job report should persist");
        let loaded = load_execution_result_job_report(&report_path)
            .expect("latest-only job report should reload");

        assert_eq!(loaded, report);
    }

    #[test]
    fn load_execution_result_job_report_round_trips_full_history_multi_entry() {
        let directory = tempdir().expect("tempdir should be created");
        let report_path = directory
            .path()
            .join("execution-result-job-report-full-history.json");
        let report = sample_execution_result_job_report();

        persist_execution_result_job_report(&report_path, &report)
            .expect("full-history job report should persist");
        let loaded = load_execution_result_job_report(&report_path)
            .expect("full-history job report should reload");

        assert_eq!(loaded, report);
    }

    #[test]
    fn persist_execution_result_job_report_rejects_invalid_report_values() {
        let directory = tempdir().expect("tempdir should be created");
        let report_path = directory
            .path()
            .join("invalid-execution-result-job-report.json");
        let mut report = sample_execution_result_job_report();
        report.expected_entry_count += 1;

        let error = persist_execution_result_job_report(&report_path, &report)
            .expect_err("invalid report should be rejected before persist");

        assert!(
            error
                .to_string()
                .contains("execution result job report entry count drift"),
            "unexpected error: {error}"
        );
        assert!(
            !report_path.exists(),
            "persist helper should not write invalid report content"
        );
    }

    #[test]
    fn load_execution_result_job_report_rejects_invalid_persisted_content() {
        let directory = tempdir().expect("tempdir should be created");
        let report_path = directory
            .path()
            .join("invalid-persisted-execution-result-job-report.json");
        let mut report = sample_execution_result_job_report();
        report.entries[1].ordinal = 2;
        let encoded = serde_json::to_string_pretty(&report)
            .expect("invalid report should still serialize for load-path test");
        fs::write(&report_path, encoded).expect("invalid persisted report should be written");

        let error = load_execution_result_job_report(&report_path)
            .expect_err("invalid persisted report should be rejected on load");

        assert!(
            error.to_string().contains("job report"),
            "unexpected error: {error}"
        );
    }

    #[test]
    fn persist_and_load_execution_result_job_report_collection_summary_round_trips_exactly() {
        let directory = tempdir().expect("tempdir should be created");
        let summary_path = directory
            .path()
            .join("execution-result-job-report-collection-summary.json");
        let summary =
            sample_execution_result_job_report_collection_summary_full_history_multi_report();

        persist_execution_result_job_report_collection_summary(&summary_path, &summary)
            .expect("job report collection summary should persist");
        let loaded = load_execution_result_job_report_collection_summary(&summary_path)
            .expect("job report collection summary should reload after persist");

        assert_eq!(loaded, summary);
    }

    #[test]
    fn execution_result_job_report_collection_summary_persisted_json_schema_stays_stable() {
        let directory = tempdir().expect("tempdir should be created");
        let latest_only_path = directory
            .path()
            .join("execution-result-job-report-collection-summary-latest-schema.json");
        let full_history_path = directory
            .path()
            .join("execution-result-job-report-collection-summary-full-schema.json");
        let latest_only = sample_execution_result_job_report_collection_summary_latest_only();
        let full_history =
            sample_execution_result_job_report_collection_summary_full_history_multi_report();

        persist_execution_result_job_report_collection_summary(&latest_only_path, &latest_only)
            .expect("latest-only summary should persist");
        persist_execution_result_job_report_collection_summary(&full_history_path, &full_history)
            .expect("full-history summary should persist");

        let latest_only_json = read_json_value(&latest_only_path);
        let full_history_json = read_json_value(&full_history_path);
        let expected_keys = [
            "report_count",
            "total_entry_count",
            "job_spec_ids",
            "export_names",
            "selection_modes",
            "source_run_request_ids",
            "source_handoff_bundle_ids",
            "shared_export_name",
            "shared_selection_mode",
        ];
        assert_object_keys(&latest_only_json, &expected_keys);
        assert_object_keys(&full_history_json, &expected_keys);

        assert_eq!(
            latest_only_json["selection_modes"],
            Value::Array(vec![Value::String("latest_only".to_string())])
        );
        assert_eq!(
            latest_only_json["shared_export_name"],
            Value::String("restore-stage-5-latest-only".to_string())
        );
        assert_eq!(
            latest_only_json["shared_selection_mode"],
            Value::String("latest_only".to_string())
        );
        assert_eq!(
            full_history_json["selection_modes"],
            Value::Array(vec![
                Value::String("full_history".to_string()),
                Value::String("latest_only".to_string()),
            ])
        );
        assert_eq!(
            full_history_json["shared_export_name"],
            Value::String("restore-stage-shared".to_string())
        );
        assert_eq!(full_history_json["shared_selection_mode"], Value::Null);

        let loaded_latest_only =
            load_execution_result_job_report_collection_summary(&latest_only_path)
                .expect("latest-only summary should reload");
        let loaded_full_history =
            load_execution_result_job_report_collection_summary(&full_history_path)
                .expect("full-history summary should reload");
        assert_eq!(loaded_latest_only, latest_only);
        assert_eq!(loaded_full_history, full_history);
        assert_eq!(
            serde_json::to_value(&loaded_latest_only)
                .expect("loaded latest-only summary should convert to json"),
            latest_only_json
        );
        assert_eq!(
            serde_json::to_value(&loaded_full_history)
                .expect("loaded full-history summary should convert to json"),
            full_history_json
        );
    }

    #[test]
    fn execution_result_job_report_collection_summary_load_rejects_unknown_fields_in_persisted_json()
     {
        let directory = tempdir().expect("tempdir should be created");
        let summary_path = directory
            .path()
            .join("execution-result-job-report-collection-summary-schema-invalid.json");
        let summary = sample_execution_result_job_report_collection_summary_latest_only();

        persist_execution_result_job_report_collection_summary(&summary_path, &summary)
            .expect("summary should persist");

        let mut mutated = read_json_value(&summary_path);
        mutated
            .as_object_mut()
            .expect("summary should be an object")
            .insert(
                "unexpected_top_level".to_string(),
                Value::String("drift".to_string()),
            );
        write_json_value(&summary_path, &mutated);

        let error = load_execution_result_job_report_collection_summary(&summary_path)
            .expect_err("unknown summary field should be rejected");
        assert!(
            error.to_string().contains("unknown field"),
            "unexpected error: {error}"
        );
    }

    #[test]
    fn execution_result_job_report_collection_summary_latest_only_single_loaded_report_round_trips()
    {
        let directory = tempdir().expect("tempdir should be created");
        let summary_path = directory
            .path()
            .join("execution-result-job-report-collection-summary-latest-only.json");
        let summary = sample_execution_result_job_report_collection_summary_latest_only();

        persist_execution_result_job_report_collection_summary(&summary_path, &summary)
            .expect("latest-only job report collection summary should persist");
        let loaded = load_execution_result_job_report_collection_summary(&summary_path)
            .expect("latest-only job report collection summary should reload");

        assert_eq!(loaded, summary);
    }

    #[test]
    fn execution_result_job_report_collection_summary_full_history_multi_report_round_trips() {
        let directory = tempdir().expect("tempdir should be created");
        let summary_path = directory
            .path()
            .join("execution-result-job-report-collection-summary-full-history.json");
        let summary =
            sample_execution_result_job_report_collection_summary_full_history_multi_report();

        persist_execution_result_job_report_collection_summary(&summary_path, &summary)
            .expect("full-history multi-report collection summary should persist");
        let loaded = load_execution_result_job_report_collection_summary(&summary_path)
            .expect("full-history multi-report collection summary should reload");

        assert_eq!(loaded, summary);
    }

    #[test]
    fn persist_execution_result_job_report_collection_summary_rejects_invalid_summary_values() {
        let directory = tempdir().expect("tempdir should be created");
        let summary_path = directory
            .path()
            .join("invalid-execution-result-job-report-collection-summary.json");
        let mut summary = sample_execution_result_job_report_collection_summary_latest_only();
        summary.job_spec_ids.clear();

        let error = persist_execution_result_job_report_collection_summary(&summary_path, &summary)
            .expect_err("invalid summary should be rejected before persist");

        assert!(
            error
                .to_string()
                .contains("with reports must include non-empty summary collections"),
            "unexpected error: {error}"
        );
        assert!(
            !summary_path.exists(),
            "persist helper should not write invalid summary content"
        );
    }

    #[test]
    fn load_execution_result_job_report_collection_summary_rejects_invalid_persisted_content() {
        let directory = tempdir().expect("tempdir should be created");
        let summary_path = directory
            .path()
            .join("invalid-persisted-execution-result-job-report-collection-summary.json");
        let mut summary =
            sample_execution_result_job_report_collection_summary_full_history_multi_report();
        summary.shared_export_name = Some("missing-export-name".to_string());
        let encoded = serde_json::to_string_pretty(&summary)
            .expect("invalid summary should still serialize for load-path test");
        fs::write(&summary_path, encoded).expect("invalid persisted summary should be written");

        let error = load_execution_result_job_report_collection_summary(&summary_path)
            .expect_err("invalid persisted summary should be rejected on load");

        assert!(
            error
                .to_string()
                .contains("shared export name missing-export-name must appear in export_names"),
            "unexpected error: {error}"
        );
    }

    #[test]
    fn persist_and_load_execution_result_job_report_collection_summary_index_round_trips_exactly() {
        let directory = tempdir().expect("tempdir should be created");
        let index_path = directory
            .path()
            .join("execution-result-job-report-collection-summary-index.json");
        let index = sample_execution_result_job_report_collection_summary_index();

        persist_execution_result_job_report_collection_summary_index(&index_path, &index)
            .expect("job report collection summary index should persist");
        let loaded = load_execution_result_job_report_collection_summary_index(&index_path)
            .expect("job report collection summary index should reload after persist");

        assert_eq!(loaded, index);
    }

    #[test]
    fn execution_result_job_report_collection_summary_index_persisted_json_schema_stays_stable() {
        let directory = tempdir().expect("tempdir should be created");
        let index_path = directory
            .path()
            .join("execution-result-job-report-collection-summary-index-schema.json");
        let summary_a_path = directory.path().join("summary-a.json");
        let summary_b_path = directory.path().join("summary-b.json");
        let summary_a = sample_execution_result_job_report_collection_summary_latest_only();
        let summary_b =
            sample_execution_result_job_report_collection_summary_full_history_multi_report();

        register_execution_result_job_report_collection_summary_in_index(
            &index_path,
            &summary_a_path,
            &summary_a,
        )
        .expect("first summary should register");
        register_execution_result_job_report_collection_summary_in_index(
            &index_path,
            &summary_b_path,
            &summary_b,
        )
        .expect("second summary should register");

        let persisted = read_json_value(&index_path);
        assert_object_keys(&persisted, &["index_version", "entries"]);
        let entries = persisted["entries"]
            .as_array()
            .expect("summary index entries should be an array");
        assert_eq!(entries.len(), 2);
        assert_object_keys(
            &entries[0],
            &[
                "ordinal",
                "summary_file_path",
                "report_count",
                "total_entry_count",
                "job_spec_ids",
                "export_names",
                "selection_modes",
                "source_run_request_ids",
                "source_handoff_bundle_ids",
            ],
        );
        assert_eq!(
            entries[0]["selection_modes"],
            Value::Array(vec![Value::String("latest_only".to_string())])
        );
        assert_eq!(
            entries[1]["selection_modes"],
            Value::Array(vec![
                Value::String("full_history".to_string()),
                Value::String("latest_only".to_string()),
            ])
        );

        let loaded = load_execution_result_job_report_collection_summary_index(&index_path)
            .expect("registered summary index should reload");
        assert_eq!(
            loaded.entries[0].selection_modes,
            summary_a.selection_modes.clone()
        );
        assert_eq!(
            loaded.entries[1].selection_modes,
            summary_b.selection_modes.clone()
        );
        assert_eq!(
            serde_json::to_value(&loaded).expect("loaded summary index should convert to json"),
            persisted
        );
    }

    #[test]
    fn execution_result_job_report_collection_summary_index_load_rejects_unknown_fields_in_persisted_json()
     {
        let directory = tempdir().expect("tempdir should be created");
        let index_path = directory
            .path()
            .join("execution-result-job-report-collection-summary-index-schema-invalid.json");
        let index = sample_execution_result_job_report_collection_summary_index();

        persist_execution_result_job_report_collection_summary_index(&index_path, &index)
            .expect("summary index should persist");

        let mut top_level_unknown = read_json_value(&index_path);
        top_level_unknown
            .as_object_mut()
            .expect("summary index should be an object")
            .insert(
                "unexpected_top_level".to_string(),
                Value::String("drift".to_string()),
            );
        write_json_value(&index_path, &top_level_unknown);
        let top_level_error =
            load_execution_result_job_report_collection_summary_index(&index_path)
                .expect_err("unknown summary index top-level field should be rejected");
        assert!(
            top_level_error.to_string().contains("unknown field"),
            "unexpected error: {top_level_error}"
        );

        persist_execution_result_job_report_collection_summary_index(&index_path, &index)
            .expect("summary index should repersist cleanly");
        let mut nested_unknown = read_json_value(&index_path);
        nested_unknown["entries"][0]
            .as_object_mut()
            .expect("summary index entry should be an object")
            .insert(
                "unexpected_entry_field".to_string(),
                Value::String("drift".to_string()),
            );
        write_json_value(&index_path, &nested_unknown);
        let nested_error = load_execution_result_job_report_collection_summary_index(&index_path)
            .expect_err("unknown summary index entry field should be rejected");
        assert!(
            nested_error.to_string().contains("unknown field"),
            "unexpected error: {nested_error}"
        );
    }

    #[test]
    fn register_execution_result_job_report_collection_summary_in_index_appends_in_order() {
        let directory = tempdir().expect("tempdir should be created");
        let index_path = directory
            .path()
            .join("execution-result-job-report-collection-summary-index.json");
        let summary_a_path = directory
            .path()
            .join("execution-result-job-report-collection-summary-a.json");
        let summary_b_path = directory
            .path()
            .join("execution-result-job-report-collection-summary-b.json");
        let summary_a = sample_execution_result_job_report_collection_summary_latest_only();
        let summary_b =
            sample_execution_result_job_report_collection_summary_full_history_multi_report();

        let entry_a = register_execution_result_job_report_collection_summary_in_index(
            &index_path,
            &summary_a_path,
            &summary_a,
        )
        .expect("first summary should register");
        let entry_b = register_execution_result_job_report_collection_summary_in_index(
            &index_path,
            &summary_b_path,
            &summary_b,
        )
        .expect("second summary should register");

        assert_eq!(entry_a.ordinal, 0);
        assert_eq!(entry_b.ordinal, 1);

        let loaded = load_execution_result_job_report_collection_summary_index(&index_path)
            .expect("registered summary index should reload");
        assert_eq!(loaded.entries, vec![entry_a, entry_b]);
    }

    #[test]
    fn register_execution_result_job_report_collection_summary_in_index_rejects_duplicate_summary_file_path()
     {
        let directory = tempdir().expect("tempdir should be created");
        let index_path = directory
            .path()
            .join("execution-result-job-report-collection-summary-index.json");
        let summary_path = directory
            .path()
            .join("execution-result-job-report-collection-summary.json");
        let summary_a = sample_execution_result_job_report_collection_summary_latest_only();
        let summary_b =
            sample_execution_result_job_report_collection_summary_full_history_multi_report();

        register_execution_result_job_report_collection_summary_in_index(
            &index_path,
            &summary_path,
            &summary_a,
        )
        .expect("first summary should register");
        let error = register_execution_result_job_report_collection_summary_in_index(
            &index_path,
            &summary_path,
            &summary_b,
        )
        .expect_err("duplicate summary path should be rejected");

        assert!(
            error
                .to_string()
                .contains("duplicate execution result job report collection summary path"),
            "unexpected error: {error}"
        );
    }

    #[test]
    fn register_execution_result_job_report_collection_summary_in_index_supports_latest_only_and_full_history_summaries()
     {
        let directory = tempdir().expect("tempdir should be created");
        let index_path = directory
            .path()
            .join("execution-result-job-report-collection-summary-index.json");
        let summary_a_path = directory
            .path()
            .join("execution-result-job-report-collection-summary-a.json");
        let summary_b_path = directory
            .path()
            .join("execution-result-job-report-collection-summary-b.json");

        register_execution_result_job_report_collection_summary_in_index(
            &index_path,
            &summary_a_path,
            &sample_execution_result_job_report_collection_summary_full_history_multi_report(),
        )
        .expect("full-history summary should register");
        register_execution_result_job_report_collection_summary_in_index(
            &index_path,
            &summary_b_path,
            &sample_execution_result_job_report_collection_summary_latest_only(),
        )
        .expect("latest-only summary should register");

        let loaded = load_execution_result_job_report_collection_summary_index(&index_path)
            .expect("mixed summary index should reload");

        assert_eq!(loaded.entries.len(), 2);
        assert_eq!(
            loaded.entries[0].selection_modes,
            vec![
                ExecutionResultSelectionMode::FullHistory,
                ExecutionResultSelectionMode::LatestOnly,
            ]
        );
        assert_eq!(
            loaded.entries[1].selection_modes,
            vec![ExecutionResultSelectionMode::LatestOnly]
        );
    }

    #[test]
    fn loaded_execution_result_job_report_collection_summary_index_validates_cleanly() {
        let directory = tempdir().expect("tempdir should be created");
        let index_path = directory
            .path()
            .join("execution-result-job-report-collection-summary-index.json");
        let index = sample_execution_result_job_report_collection_summary_index();

        persist_execution_result_job_report_collection_summary_index(&index_path, &index)
            .expect("job report collection summary index should persist");
        let loaded = load_execution_result_job_report_collection_summary_index(&index_path)
            .expect("job report collection summary index should reload");

        validate_execution_result_job_report_collection_summary_index(&loaded)
            .expect("loaded summary index should validate");
    }

    #[test]
    fn find_execution_result_job_report_collection_summary_index_entry_by_summary_file_path_returns_matching_entry()
     {
        let index = sample_execution_result_job_report_collection_summary_index();

        let entry =
            find_execution_result_job_report_collection_summary_index_entry_by_summary_file_path(
                &index,
                r"D:\reports\execution-result-job-report-collection-summary-b.json",
            )
            .expect("summary index entry should be found by summary file path");

        assert_eq!(entry.ordinal, 1);
        assert_eq!(entry.report_count, 3);
    }

    #[test]
    fn find_execution_result_job_report_collection_summary_index_entry_by_report_count_returns_matching_entry()
     {
        let index = sample_execution_result_job_report_collection_summary_index();

        let entry =
            find_execution_result_job_report_collection_summary_index_entry_by_report_count(
                &index, 1,
            )
            .expect("summary index entry should be found by report count");

        assert_eq!(
            entry.summary_file_path,
            r"D:\reports\execution-result-job-report-collection-summary-a.json"
        );
        assert_eq!(entry.ordinal, 0);
    }

    #[test]
    fn find_execution_result_job_report_collection_summary_index_entry_by_summary_file_path_returns_none_when_missing()
     {
        let index = sample_execution_result_job_report_collection_summary_index();

        let entry =
            find_execution_result_job_report_collection_summary_index_entry_by_summary_file_path(
                &index,
                r"D:\reports\missing-execution-result-job-report-collection-summary.json",
            );

        assert!(entry.is_none(), "missing summary path should not resolve");
    }

    #[test]
    fn select_execution_result_job_report_collection_summary_index_entries_filters_by_summary_file_path()
     {
        let index = sample_execution_result_job_report_collection_summary_index();
        let query = ExecutionResultJobReportCollectionSummaryIndexQuery {
            summary_file_path: Some(
                r"D:\reports\execution-result-job-report-collection-summary-b.json".to_string(),
            ),
            ..ExecutionResultJobReportCollectionSummaryIndexQuery::default()
        };

        let selected =
            select_execution_result_job_report_collection_summary_index_entries(&index, &query)
                .expect("summary file path query should select deterministically");

        assert_eq!(selected, vec![&index.entries[1]]);
    }

    #[test]
    fn select_execution_result_job_report_collection_summary_index_entries_filters_by_report_count()
    {
        let index = sample_execution_result_job_report_collection_summary_index();
        let query = ExecutionResultJobReportCollectionSummaryIndexQuery {
            report_count: Some(1),
            ..ExecutionResultJobReportCollectionSummaryIndexQuery::default()
        };

        let selected =
            select_execution_result_job_report_collection_summary_index_entries(&index, &query)
                .expect("report count query should select deterministically");

        assert_eq!(selected, vec![&index.entries[0]]);
    }

    #[test]
    fn select_execution_result_job_report_collection_summary_index_entries_filters_by_export_name_and_selection_mode()
     {
        let index = sample_execution_result_job_report_collection_summary_index();
        let query = ExecutionResultJobReportCollectionSummaryIndexQuery {
            export_names: vec!["restore-stage-shared".to_string()],
            selection_modes: vec![ExecutionResultSelectionMode::FullHistory],
            ..ExecutionResultJobReportCollectionSummaryIndexQuery::default()
        };

        let selected =
            select_execution_result_job_report_collection_summary_index_entries(&index, &query)
                .expect("export name and selection mode query should select deterministically");

        assert_eq!(selected, vec![&index.entries[1]]);
    }

    #[test]
    fn select_execution_result_job_report_collection_summary_index_entries_preserves_index_order() {
        let mut index = sample_execution_result_job_report_collection_summary_index();
        let mut trailing_match = index.entries[1].clone();
        trailing_match.ordinal = 2;
        trailing_match.summary_file_path =
            r"D:\reports\execution-result-job-report-collection-summary-c.json".to_string();
        index.entries.push(trailing_match);

        let query = ExecutionResultJobReportCollectionSummaryIndexQuery {
            export_names: vec!["restore-stage-shared".to_string()],
            ..ExecutionResultJobReportCollectionSummaryIndexQuery::default()
        };

        let selected =
            select_execution_result_job_report_collection_summary_index_entries(&index, &query)
                .expect("shared run request query should preserve original index order");

        assert_eq!(selected, vec![&index.entries[1], &index.entries[2]]);
    }

    #[test]
    fn latest_execution_result_job_report_collection_summary_index_entry_returns_last_matching_entry()
     {
        let mut index = sample_execution_result_job_report_collection_summary_index();
        let mut latest_entry = index.entries[1].clone();
        latest_entry.ordinal = 2;
        latest_entry.summary_file_path =
            r"D:\reports\execution-result-job-report-collection-summary-c.json".to_string();
        index.entries.push(latest_entry.clone());

        let query = ExecutionResultJobReportCollectionSummaryIndexQuery {
            export_names: vec!["restore-stage-shared".to_string()],
            ..ExecutionResultJobReportCollectionSummaryIndexQuery::default()
        };

        let selected =
            latest_execution_result_job_report_collection_summary_index_entry(&index, &query)
                .expect("latest query should validate");

        assert_eq!(selected, Some(&index.entries[2]));
        assert_eq!(selected.cloned(), Some(latest_entry));
    }

    #[test]
    fn query_execution_result_job_report_collection_summary_index_can_reduce_to_latest_only_entry()
    {
        let mut index = sample_execution_result_job_report_collection_summary_index();
        let mut latest_entry = index.entries[1].clone();
        latest_entry.ordinal = 2;
        latest_entry.summary_file_path =
            r"D:\reports\execution-result-job-report-collection-summary-c.json".to_string();
        index.entries.push(latest_entry.clone());

        let query = ExecutionResultJobReportCollectionSummaryIndexQuery {
            export_names: vec!["restore-stage-shared".to_string()],
            latest_only: true,
            ..ExecutionResultJobReportCollectionSummaryIndexQuery::default()
        };

        let summary = query_execution_result_job_report_collection_summary_index(&index, &query)
            .expect("latest-only query should produce summary");

        assert_eq!(summary.query, query);
        assert_eq!(summary.selected_entry_count, 1);
        assert_eq!(summary.selected_entries, vec![latest_entry]);
    }

    #[test]
    fn load_and_query_execution_result_job_report_collection_summary_index_matches_explicit_load_and_select_path()
     {
        let directory = tempdir().expect("tempdir should be created");
        let index_path = directory
            .path()
            .join("execution-result-job-report-collection-summary-index.json");
        let index = sample_execution_result_job_report_collection_summary_index();
        let query = ExecutionResultJobReportCollectionSummaryIndexQuery {
            source_run_request_ids: vec!["run-request-shared".to_string()],
            source_handoff_bundle_ids: vec!["handoff-shared".to_string()],
            total_entry_count: Some(7),
            ..ExecutionResultJobReportCollectionSummaryIndexQuery::default()
        };

        persist_execution_result_job_report_collection_summary_index(&index_path, &index)
            .expect("queryable summary index should persist");
        let explicitly_loaded =
            load_execution_result_job_report_collection_summary_index(&index_path)
                .expect("queryable summary index should load explicitly");
        let explicit_summary =
            query_execution_result_job_report_collection_summary_index(&explicitly_loaded, &query)
                .expect("explicit load plus query should succeed");
        let convenience_summary =
            load_and_query_execution_result_job_report_collection_summary_index(
                &index_path,
                &query,
            )
            .expect("convenience load plus query should succeed");

        assert_eq!(convenience_summary, explicit_summary);
        assert_eq!(
            convenience_summary.selected_entries,
            vec![index.entries[1].clone()]
        );
    }

    #[test]
    fn load_selected_execution_result_job_report_collection_summaries_preserves_selected_entry_order()
     {
        let (
            _directory,
            index_path,
            latest_only_summary_path,
            latest_only_summary,
            full_history_summary_path,
            full_history_summary,
        ) = persist_sample_execution_result_job_report_collection_summaries_with_index();
        let loaded_index = load_execution_result_job_report_collection_summary_index(&index_path)
            .expect("persisted summary index should reload for selected-entry loading");
        let selected_entries = vec![
            loaded_index.entries[1].clone(),
            loaded_index.entries[0].clone(),
        ];

        let loaded_summaries =
            load_selected_execution_result_job_report_collection_summaries(&selected_entries)
                .expect("selected summaries should load in provided order");

        assert_eq!(
            loaded_summaries,
            vec![full_history_summary.clone(), latest_only_summary.clone()]
        );
        assert_eq!(
            loaded_summaries[0],
            load_execution_result_job_report_collection_summary(&full_history_summary_path)
                .expect("explicit full-history summary should reload")
        );
        assert_eq!(
            loaded_summaries[1],
            load_execution_result_job_report_collection_summary(&latest_only_summary_path)
                .expect("explicit latest-only summary should reload")
        );
    }

    #[test]
    fn load_and_query_execution_result_job_report_collection_summaries_matches_explicit_index_query_and_load_path()
     {
        let (_directory, index_path, _latest_only_path, _latest_only, _full_history_path, _) =
            persist_sample_execution_result_job_report_collection_summaries_with_index();
        let query = ExecutionResultJobReportCollectionSummaryIndexQuery {
            source_run_request_ids: vec!["run-request-shared".to_string()],
            source_handoff_bundle_ids: vec!["handoff-shared".to_string()],
            ..ExecutionResultJobReportCollectionSummaryIndexQuery::default()
        };
        let explicit_index = load_execution_result_job_report_collection_summary_index(&index_path)
            .expect("persisted summary index should load explicitly");
        let explicit_selection =
            query_execution_result_job_report_collection_summary_index(&explicit_index, &query)
                .expect("explicit summary index query should succeed");
        let explicit_loaded = load_selected_execution_result_job_report_collection_summaries(
            &explicit_selection.selected_entries,
        )
        .expect("explicitly selected summaries should load");

        let convenience_loaded =
            load_and_query_execution_result_job_report_collection_summaries(&index_path, &query)
                .expect("convenience query-and-load should succeed");

        assert_eq!(convenience_loaded, explicit_loaded);
    }

    #[test]
    fn load_and_query_execution_result_job_report_collection_summaries_latest_only_returns_exactly_one_summary()
     {
        let (
            _directory,
            index_path,
            _latest_only_summary_path,
            _latest_only_summary,
            _full_history_summary_path,
            full_history_summary,
        ) = persist_sample_execution_result_job_report_collection_summaries_with_index();
        let query = ExecutionResultJobReportCollectionSummaryIndexQuery {
            source_run_request_ids: vec!["run-request-shared".to_string()],
            source_handoff_bundle_ids: vec!["handoff-shared".to_string()],
            latest_only: true,
            ..ExecutionResultJobReportCollectionSummaryIndexQuery::default()
        };

        let loaded_summaries =
            load_and_query_execution_result_job_report_collection_summaries(&index_path, &query)
                .expect("latest-only summary query should load");

        assert_eq!(loaded_summaries, vec![full_history_summary]);
        assert_eq!(loaded_summaries.len(), 1);
        validate_execution_result_job_report_collection_summary(&loaded_summaries[0])
            .expect("latest-only loaded summary should remain valid");
    }

    #[test]
    fn load_and_query_execution_result_job_report_collection_summaries_full_history_returns_all_matches_in_index_order()
     {
        let (
            _directory,
            index_path,
            _latest_only_summary_path,
            latest_only_summary,
            _full_history_summary_path,
            full_history_summary,
        ) = persist_sample_execution_result_job_report_collection_summaries_with_index();
        let query = ExecutionResultJobReportCollectionSummaryIndexQuery {
            ..ExecutionResultJobReportCollectionSummaryIndexQuery::default()
        };

        let loaded_summaries =
            load_and_query_execution_result_job_report_collection_summaries(&index_path, &query)
                .expect("full-history summary query should load");

        assert_eq!(
            loaded_summaries,
            vec![latest_only_summary, full_history_summary]
        );
        for summary in &loaded_summaries {
            validate_execution_result_job_report_collection_summary(summary)
                .expect("full-history loaded summaries should remain valid");
        }
    }

    #[test]
    fn load_and_query_execution_result_job_report_collection_summaries_matches_explicit_persist_and_indexed_load_path_without_field_drift()
     {
        let (
            _directory,
            index_path,
            _latest_only_summary_path,
            latest_only_summary,
            _full_history_summary_path,
            full_history_summary,
        ) = persist_sample_execution_result_job_report_collection_summaries_with_index();
        let query = ExecutionResultJobReportCollectionSummaryIndexQuery {
            ..ExecutionResultJobReportCollectionSummaryIndexQuery::default()
        };

        let loaded_summaries =
            load_and_query_execution_result_job_report_collection_summaries(&index_path, &query)
                .expect("query-and-load path should reload persisted summaries");

        assert_eq!(
            loaded_summaries,
            vec![latest_only_summary.clone(), full_history_summary.clone()]
        );
        assert_eq!(
            loaded_summaries[0].shared_selection_mode,
            latest_only_summary.shared_selection_mode
        );
        assert_eq!(
            loaded_summaries[1].selection_modes,
            full_history_summary.selection_modes
        );
        assert_eq!(
            loaded_summaries[1].job_spec_ids,
            full_history_summary.job_spec_ids
        );
    }

    #[test]
    fn load_query_summarize_and_persist_execution_result_job_report_collection_summary_matches_explicit_pipeline()
     {
        let (
            directory,
            index_path,
            _latest_only_summary_path,
            _latest_only_summary,
            _full_history_summary_path,
            _full_history_summary,
        ) = persist_sample_execution_result_job_report_collection_summaries_with_index();
        let output_summary_path = directory.path().join("aggregate-summary.json");
        let query = ExecutionResultJobReportCollectionSummaryIndexQuery {
            source_run_request_ids: vec!["run-request-shared".to_string()],
            source_handoff_bundle_ids: vec!["handoff-shared".to_string()],
            ..ExecutionResultJobReportCollectionSummaryIndexQuery::default()
        };
        let explicitly_loaded =
            load_and_query_execution_result_job_report_collection_summaries(&index_path, &query)
                .expect("explicit pipeline should load queried summaries");
        let mut job_spec_ids = Vec::new();
        let mut export_names = Vec::new();
        let mut selection_modes = Vec::new();
        let mut source_run_request_ids = Vec::new();
        let mut source_handoff_bundle_ids = Vec::new();
        for summary in &explicitly_loaded {
            for job_spec_id in &summary.job_spec_ids {
                push_unique_string(&mut job_spec_ids, job_spec_id);
            }
            for export_name in &summary.export_names {
                push_unique_string(&mut export_names, export_name);
            }
            for selection_mode in &summary.selection_modes {
                push_unique_selection_mode(&mut selection_modes, *selection_mode);
            }
            for source_run_request_id in &summary.source_run_request_ids {
                push_unique_string(&mut source_run_request_ids, source_run_request_id);
            }
            for source_handoff_bundle_id in &summary.source_handoff_bundle_ids {
                push_unique_string(&mut source_handoff_bundle_ids, source_handoff_bundle_id);
            }
        }
        let explicit_aggregate = ExecutionResultJobReportCollectionSummary {
            report_count: explicitly_loaded
                .iter()
                .map(|summary| summary.report_count)
                .sum(),
            total_entry_count: explicitly_loaded
                .iter()
                .map(|summary| summary.total_entry_count)
                .sum(),
            shared_export_name: if export_names.len() == 1 {
                export_names.first().cloned()
            } else {
                None
            },
            shared_selection_mode: if selection_modes.len() == 1 {
                selection_modes.first().copied()
            } else {
                None
            },
            job_spec_ids,
            export_names,
            selection_modes,
            source_run_request_ids,
            source_handoff_bundle_ids,
        };
        persist_execution_result_job_report_collection_summary(
            &output_summary_path,
            &explicit_aggregate,
        )
        .expect("explicit aggregate summary should persist");
        let explicit_reloaded =
            load_execution_result_job_report_collection_summary(&output_summary_path)
                .expect("explicit aggregate summary should reload");

        let wrapper_output =
            load_query_summarize_and_persist_execution_result_job_report_collection_summary(
                &index_path,
                &query,
                &output_summary_path,
            )
            .expect("wrapper should load, summarize, and persist queried summaries");
        let wrapper_reloaded =
            load_execution_result_job_report_collection_summary(&output_summary_path)
                .expect("wrapper aggregate summary should reload");

        assert_eq!(wrapper_output, explicit_aggregate);
        assert_eq!(wrapper_output, explicit_reloaded);
        assert_eq!(wrapper_output, wrapper_reloaded);
    }

    #[test]
    fn load_query_and_aggregate_execution_result_job_report_collection_summaries_matches_explicit_query_load_and_aggregate_pipeline()
     {
        let (
            _directory,
            index_path,
            _latest_only_summary_path,
            _latest_only_summary,
            _full_history_summary_path,
            _full_history_summary,
        ) = persist_sample_execution_result_job_report_collection_summaries_with_index();
        let query = ExecutionResultJobReportCollectionSummaryIndexQuery {
            source_run_request_ids: vec!["run-request-shared".to_string()],
            source_handoff_bundle_ids: vec!["handoff-shared".to_string()],
            ..ExecutionResultJobReportCollectionSummaryIndexQuery::default()
        };
        let explicit_loaded =
            load_and_query_execution_result_job_report_collection_summaries(&index_path, &query)
                .expect("explicit query-and-load pipeline should succeed");
        let explicit_aggregate =
            summarize_execution_result_job_report_collection_summaries(&explicit_loaded);

        let helper_aggregate =
            load_query_and_aggregate_execution_result_job_report_collection_summaries(
                &index_path,
                &query,
            )
            .expect("pure query/load/aggregate helper should succeed");

        assert_eq!(helper_aggregate, explicit_aggregate);
    }

    #[test]
    fn load_query_and_aggregate_execution_result_job_report_collection_summaries_latest_only_matches_latest_summary()
     {
        let (
            _directory,
            index_path,
            _latest_only_summary_path,
            _latest_only_summary,
            _full_history_summary_path,
            full_history_summary,
        ) = persist_sample_execution_result_job_report_collection_summaries_with_index();
        let query = ExecutionResultJobReportCollectionSummaryIndexQuery {
            latest_only: true,
            ..ExecutionResultJobReportCollectionSummaryIndexQuery::default()
        };

        let aggregate = load_query_and_aggregate_execution_result_job_report_collection_summaries(
            &index_path,
            &query,
        )
        .expect("latest-only pure helper should aggregate the selected summary");

        assert_eq!(aggregate, full_history_summary);
    }

    #[test]
    fn load_query_and_aggregate_execution_result_job_report_collection_summaries_full_history_aggregates_in_summary_index_order()
     {
        let (
            _directory,
            index_path,
            _latest_only_summary_path,
            latest_only_summary,
            _full_history_summary_path,
            full_history_summary,
        ) = persist_sample_execution_result_job_report_collection_summaries_with_index();
        let query = ExecutionResultJobReportCollectionSummaryIndexQuery::default();
        let explicit_aggregate = summarize_execution_result_job_report_collection_summaries(&[
            latest_only_summary.clone(),
            full_history_summary.clone(),
        ]);

        let aggregate = load_query_and_aggregate_execution_result_job_report_collection_summaries(
            &index_path,
            &query,
        )
        .expect("full-history pure helper should aggregate selected summaries");

        assert_eq!(aggregate, explicit_aggregate);
    }

    #[test]
    fn load_query_and_aggregate_execution_result_job_report_collection_summaries_preserves_established_aggregate_semantics_without_field_drift()
     {
        let (
            _directory,
            index_path,
            _latest_only_summary_path,
            latest_only_summary,
            _full_history_summary_path,
            full_history_summary,
        ) = persist_sample_execution_result_job_report_collection_summaries_with_index();
        let query = ExecutionResultJobReportCollectionSummaryIndexQuery::default();
        let explicit_loaded =
            load_and_query_execution_result_job_report_collection_summaries(&index_path, &query)
                .expect("explicit query-and-load pipeline should succeed");
        let explicit_aggregate =
            summarize_execution_result_job_report_collection_summaries(&explicit_loaded);

        let aggregate = load_query_and_aggregate_execution_result_job_report_collection_summaries(
            &index_path,
            &query,
        )
        .expect("pure query/load/aggregate helper should succeed");

        assert_eq!(aggregate, explicit_aggregate);
        assert_eq!(
            aggregate.report_count,
            latest_only_summary.report_count + full_history_summary.report_count
        );
        assert_eq!(
            aggregate.total_entry_count,
            latest_only_summary.total_entry_count + full_history_summary.total_entry_count
        );
        let mut expected_job_spec_ids = Vec::new();
        let mut expected_export_names = Vec::new();
        let mut expected_selection_modes = Vec::new();
        let mut expected_source_run_request_ids = Vec::new();
        let mut expected_source_handoff_bundle_ids = Vec::new();
        for summary in [&latest_only_summary, &full_history_summary] {
            for job_spec_id in &summary.job_spec_ids {
                push_unique_string(&mut expected_job_spec_ids, job_spec_id);
            }
            for export_name in &summary.export_names {
                push_unique_string(&mut expected_export_names, export_name);
            }
            for selection_mode in &summary.selection_modes {
                push_unique_selection_mode(&mut expected_selection_modes, *selection_mode);
            }
            for source_run_request_id in &summary.source_run_request_ids {
                push_unique_string(&mut expected_source_run_request_ids, source_run_request_id);
            }
            for source_handoff_bundle_id in &summary.source_handoff_bundle_ids {
                push_unique_string(
                    &mut expected_source_handoff_bundle_ids,
                    source_handoff_bundle_id,
                );
            }
        }
        assert_eq!(aggregate.job_spec_ids, explicit_aggregate.job_spec_ids);
        assert_eq!(aggregate.export_names, explicit_aggregate.export_names);
        assert_eq!(
            aggregate.selection_modes,
            explicit_aggregate.selection_modes
        );
        assert_eq!(
            aggregate.source_run_request_ids,
            explicit_aggregate.source_run_request_ids
        );
        assert_eq!(
            aggregate.source_handoff_bundle_ids,
            explicit_aggregate.source_handoff_bundle_ids
        );
        assert_eq!(aggregate.job_spec_ids, expected_job_spec_ids);
        assert_eq!(aggregate.export_names, expected_export_names);
        assert_eq!(aggregate.selection_modes, expected_selection_modes);
        assert_eq!(
            aggregate.source_run_request_ids,
            expected_source_run_request_ids
        );
        assert_eq!(
            aggregate.source_handoff_bundle_ids,
            expected_source_handoff_bundle_ids
        );
    }

    #[test]
    fn load_query_summarize_and_persist_execution_result_job_report_collection_summary_latest_only_persists_one_summary_aggregate()
     {
        let (
            directory,
            index_path,
            _latest_only_summary_path,
            _latest_only_summary,
            _full_history_summary_path,
            full_history_summary,
        ) = persist_sample_execution_result_job_report_collection_summaries_with_index();
        let output_summary_path = directory.path().join("aggregate-latest-only-summary.json");
        let query = ExecutionResultJobReportCollectionSummaryIndexQuery {
            latest_only: true,
            ..ExecutionResultJobReportCollectionSummaryIndexQuery::default()
        };

        let aggregate =
            load_query_summarize_and_persist_execution_result_job_report_collection_summary(
                &index_path,
                &query,
                &output_summary_path,
            )
            .expect("latest-only wrapper should persist aggregate summary");
        let reloaded = load_execution_result_job_report_collection_summary(&output_summary_path)
            .expect("latest-only aggregate summary should reload");

        assert_eq!(aggregate, full_history_summary);
        assert_eq!(reloaded, full_history_summary);
        assert_eq!(aggregate.report_count, 3);
    }

    #[test]
    fn load_query_summarize_and_persist_execution_result_job_report_collection_summary_full_history_persists_aggregate_in_index_order()
     {
        let (
            directory,
            index_path,
            _latest_only_summary_path,
            latest_only_summary,
            _full_history_summary_path,
            full_history_summary,
        ) = persist_sample_execution_result_job_report_collection_summaries_with_index();
        let output_summary_path = directory.path().join("aggregate-full-history-summary.json");
        let query = ExecutionResultJobReportCollectionSummaryIndexQuery::default();

        let aggregate =
            load_query_summarize_and_persist_execution_result_job_report_collection_summary(
                &index_path,
                &query,
                &output_summary_path,
            )
            .expect("full-history wrapper should persist aggregate summary");
        let reloaded = load_execution_result_job_report_collection_summary(&output_summary_path)
            .expect("full-history aggregate summary should reload");

        assert_eq!(aggregate.report_count, 4);
        assert_eq!(aggregate.total_entry_count, 7);
        assert_eq!(
            aggregate.job_spec_ids,
            vec![
                latest_only_summary.job_spec_ids[0].clone(),
                full_history_summary.job_spec_ids[0].clone(),
                full_history_summary.job_spec_ids[1].clone(),
                full_history_summary.job_spec_ids[2].clone(),
            ]
        );
        assert_eq!(
            aggregate.export_names,
            vec![
                latest_only_summary.export_names[0].clone(),
                full_history_summary.export_names[0].clone(),
            ]
        );
        assert_eq!(
            aggregate.selection_modes,
            vec![
                latest_only_summary.selection_modes[0],
                full_history_summary.selection_modes[0],
            ]
        );
        assert_eq!(reloaded, aggregate);
    }

    #[test]
    fn load_query_summarize_and_persist_execution_result_job_report_collection_summary_reloads_without_field_drift_vs_explicit_pipeline()
     {
        let (
            directory,
            index_path,
            _latest_only_summary_path,
            latest_only_summary,
            _full_history_summary_path,
            full_history_summary,
        ) = persist_sample_execution_result_job_report_collection_summaries_with_index();
        let output_summary_path = directory.path().join("aggregate-no-drift-summary.json");
        let query = ExecutionResultJobReportCollectionSummaryIndexQuery::default();
        let explicit_aggregate = ExecutionResultJobReportCollectionSummary {
            report_count: latest_only_summary.report_count + full_history_summary.report_count,
            total_entry_count: latest_only_summary.total_entry_count
                + full_history_summary.total_entry_count,
            shared_export_name: None,
            shared_selection_mode: None,
            job_spec_ids: vec![
                "job-spec-latest-only".to_string(),
                "job-spec-alpha".to_string(),
                "job-spec-beta".to_string(),
                "job-spec-gamma".to_string(),
            ],
            export_names: vec![
                "restore-stage-5-latest-only".to_string(),
                "restore-stage-shared".to_string(),
            ],
            selection_modes: vec![
                ExecutionResultSelectionMode::LatestOnly,
                ExecutionResultSelectionMode::FullHistory,
            ],
            source_run_request_ids: vec![
                "run-request-latest-only".to_string(),
                "run-request-shared".to_string(),
            ],
            source_handoff_bundle_ids: vec![
                "handoff-latest-only".to_string(),
                "handoff-shared".to_string(),
            ],
        };

        let aggregate =
            load_query_summarize_and_persist_execution_result_job_report_collection_summary(
                &index_path,
                &query,
                &output_summary_path,
            )
            .expect("wrapper should persist explicit full-history aggregate");
        let reloaded = load_execution_result_job_report_collection_summary(&output_summary_path)
            .expect("persisted aggregate should reload");

        assert_eq!(aggregate, explicit_aggregate);
        assert_eq!(reloaded, explicit_aggregate);
        assert_eq!(
            aggregate.shared_export_name,
            explicit_aggregate.shared_export_name
        );
        assert_eq!(
            aggregate.shared_selection_mode,
            explicit_aggregate.shared_selection_mode
        );
        assert_eq!(
            aggregate.source_run_request_ids,
            explicit_aggregate.source_run_request_ids
        );
        assert_eq!(
            aggregate.source_handoff_bundle_ids,
            explicit_aggregate.source_handoff_bundle_ids
        );
    }

    #[test]
    fn load_query_summarize_persist_and_register_execution_result_job_report_collection_summary_matches_explicit_pipeline()
     {
        let (
            directory,
            index_path,
            latest_only_summary_path,
            latest_only_summary,
            full_history_summary_path,
            full_history_summary,
        ) = persist_sample_execution_result_job_report_collection_summaries_with_index();
        let explicit_index_path = directory.path().join("explicit-summary-index.json");
        let explicit_output_summary_path = directory.path().join("explicit-aggregate-summary.json");
        let wrapper_output_summary_path = directory.path().join("wrapper-aggregate-summary.json");
        let query = ExecutionResultJobReportCollectionSummaryIndexQuery {
            source_run_request_ids: vec!["run-request-shared".to_string()],
            source_handoff_bundle_ids: vec!["handoff-shared".to_string()],
            ..ExecutionResultJobReportCollectionSummaryIndexQuery::default()
        };

        register_execution_result_job_report_collection_summary_in_index(
            &explicit_index_path,
            &latest_only_summary_path,
            &latest_only_summary,
        )
        .expect("explicit latest-only seed summary should register");
        register_execution_result_job_report_collection_summary_in_index(
            &explicit_index_path,
            &full_history_summary_path,
            &full_history_summary,
        )
        .expect("explicit full-history seed summary should register");

        let explicit_aggregate =
            load_query_summarize_and_persist_execution_result_job_report_collection_summary(
                &explicit_index_path,
                &query,
                &explicit_output_summary_path,
            )
            .expect("explicit summarize-and-persist step should succeed");
        let explicit_entry = register_execution_result_job_report_collection_summary_in_index(
            &explicit_index_path,
            &explicit_output_summary_path,
            &explicit_aggregate,
        )
        .expect("explicit register step should succeed");
        let explicit_index =
            load_execution_result_job_report_collection_summary_index(&explicit_index_path)
                .expect("explicit pipeline index should reload");

        let wrapper_aggregate =
            load_query_summarize_persist_and_register_execution_result_job_report_collection_summary(
                &index_path,
                &query,
                &wrapper_output_summary_path,
            )
            .expect("wrapper pipeline should succeed");
        let wrapper_reloaded =
            load_execution_result_job_report_collection_summary(&wrapper_output_summary_path)
                .expect("wrapper summary should reload");
        let wrapper_index = load_execution_result_job_report_collection_summary_index(&index_path)
            .expect("wrapper pipeline index should reload");
        let wrapper_entry = wrapper_index
            .entries
            .last()
            .cloned()
            .expect("wrapper pipeline should append an index entry");

        assert_eq!(wrapper_aggregate, explicit_aggregate);
        assert_eq!(wrapper_reloaded, explicit_aggregate);
        assert_eq!(wrapper_entry.report_count, explicit_entry.report_count);
        assert_eq!(
            wrapper_entry.total_entry_count,
            explicit_entry.total_entry_count
        );
        assert_eq!(wrapper_entry.job_spec_ids, explicit_entry.job_spec_ids);
        assert_eq!(wrapper_entry.export_names, explicit_entry.export_names);
        assert_eq!(
            wrapper_entry.selection_modes,
            explicit_entry.selection_modes
        );
        assert_eq!(
            wrapper_entry.source_run_request_ids,
            explicit_entry.source_run_request_ids
        );
        assert_eq!(
            wrapper_entry.source_handoff_bundle_ids,
            explicit_entry.source_handoff_bundle_ids
        );
        assert_eq!(explicit_entry.ordinal, explicit_index.entries.len() - 1);
        assert_eq!(wrapper_entry.ordinal, wrapper_index.entries.len() - 1);
        assert_eq!(wrapper_index.entries.len(), 3);
    }

    #[test]
    fn load_query_summarize_persist_and_register_execution_result_job_report_collection_summary_latest_only_registers_one_summary_aggregate()
     {
        let (
            directory,
            index_path,
            _latest_only_summary_path,
            _latest_only_summary,
            _full_history_summary_path,
            full_history_summary,
        ) = persist_sample_execution_result_job_report_collection_summaries_with_index();
        let output_summary_path = directory
            .path()
            .join("wrapper-aggregate-latest-only-summary.json");
        let query = ExecutionResultJobReportCollectionSummaryIndexQuery {
            latest_only: true,
            ..ExecutionResultJobReportCollectionSummaryIndexQuery::default()
        };

        let aggregate =
            load_query_summarize_persist_and_register_execution_result_job_report_collection_summary(
                &index_path,
                &query,
                &output_summary_path,
            )
            .expect("latest-only wrapper should summarize, persist, and register");
        let reloaded = load_execution_result_job_report_collection_summary(&output_summary_path)
            .expect("latest-only persisted aggregate should reload");
        let index = load_execution_result_job_report_collection_summary_index(&index_path)
            .expect("latest-only index should reload");
        let registered_entry = index
            .entries
            .last()
            .expect("latest-only wrapper should append one registered summary");

        assert_eq!(aggregate, full_history_summary);
        assert_eq!(reloaded, full_history_summary);
        assert_eq!(index.entries.len(), 3);
        assert_eq!(registered_entry.ordinal, 2);
        assert_eq!(
            registered_entry.summary_file_path,
            path_to_owned_string(&output_summary_path)
                .expect("latest-only output summary path should serialize")
        );
        assert_eq!(
            registered_entry.report_count,
            full_history_summary.report_count
        );
        assert_eq!(
            registered_entry.total_entry_count,
            full_history_summary.total_entry_count
        );
        assert_eq!(
            registered_entry.job_spec_ids,
            full_history_summary.job_spec_ids
        );
    }

    #[test]
    fn load_query_summarize_persist_and_register_execution_result_job_report_collection_summary_full_history_registers_aggregate_in_index_order()
     {
        let (
            directory,
            index_path,
            _latest_only_summary_path,
            latest_only_summary,
            _full_history_summary_path,
            full_history_summary,
        ) = persist_sample_execution_result_job_report_collection_summaries_with_index();
        let output_summary_path = directory
            .path()
            .join("wrapper-aggregate-full-history-summary.json");
        let query = ExecutionResultJobReportCollectionSummaryIndexQuery::default();

        let aggregate =
            load_query_summarize_persist_and_register_execution_result_job_report_collection_summary(
                &index_path,
                &query,
                &output_summary_path,
            )
            .expect("full-history wrapper should summarize, persist, and register");
        let reloaded = load_execution_result_job_report_collection_summary(&output_summary_path)
            .expect("full-history persisted aggregate should reload");
        let index = load_execution_result_job_report_collection_summary_index(&index_path)
            .expect("full-history index should reload");
        let registered_entry = index
            .entries
            .last()
            .expect("full-history wrapper should append one registered summary");

        assert_eq!(aggregate.report_count, 4);
        assert_eq!(aggregate.total_entry_count, 7);
        assert_eq!(
            aggregate.job_spec_ids,
            vec![
                latest_only_summary.job_spec_ids[0].clone(),
                full_history_summary.job_spec_ids[0].clone(),
                full_history_summary.job_spec_ids[1].clone(),
                full_history_summary.job_spec_ids[2].clone(),
            ]
        );
        assert_eq!(
            aggregate.export_names,
            vec![
                latest_only_summary.export_names[0].clone(),
                full_history_summary.export_names[0].clone(),
            ]
        );
        assert_eq!(
            aggregate.selection_modes,
            vec![
                latest_only_summary.selection_modes[0],
                full_history_summary.selection_modes[0],
            ]
        );
        assert_eq!(reloaded, aggregate);
        assert_eq!(index.entries.len(), 3);
        assert_eq!(registered_entry.ordinal, 2);
        assert_eq!(registered_entry.report_count, aggregate.report_count);
        assert_eq!(
            registered_entry.total_entry_count,
            aggregate.total_entry_count
        );
        assert_eq!(registered_entry.job_spec_ids, aggregate.job_spec_ids);
        assert_eq!(registered_entry.export_names, aggregate.export_names);
        assert_eq!(registered_entry.selection_modes, aggregate.selection_modes);
        assert_eq!(
            registered_entry.source_run_request_ids,
            aggregate.source_run_request_ids
        );
        assert_eq!(
            registered_entry.source_handoff_bundle_ids,
            aggregate.source_handoff_bundle_ids
        );
    }

    #[test]
    fn load_query_summarize_persist_and_register_execution_result_job_report_collection_summary_reloads_without_field_drift_vs_explicit_pipeline()
     {
        let (
            directory,
            index_path,
            latest_only_summary_path,
            latest_only_summary,
            full_history_summary_path,
            full_history_summary,
        ) = persist_sample_execution_result_job_report_collection_summaries_with_index();
        let explicit_index_path = directory
            .path()
            .join("explicit-no-drift-summary-index.json");
        let explicit_output_summary_path = directory
            .path()
            .join("explicit-wrapper-no-drift-summary.json");
        let wrapper_output_summary_path = directory.path().join("wrapper-no-drift-summary.json");
        let query = ExecutionResultJobReportCollectionSummaryIndexQuery::default();

        register_execution_result_job_report_collection_summary_in_index(
            &explicit_index_path,
            &latest_only_summary_path,
            &latest_only_summary,
        )
        .expect("explicit latest-only seed summary should register");
        register_execution_result_job_report_collection_summary_in_index(
            &explicit_index_path,
            &full_history_summary_path,
            &full_history_summary,
        )
        .expect("explicit full-history seed summary should register");

        let explicit_aggregate =
            load_query_summarize_and_persist_execution_result_job_report_collection_summary(
                &explicit_index_path,
                &query,
                &explicit_output_summary_path,
            )
            .expect("explicit summarize-and-persist step should succeed");
        let explicit_entry = register_execution_result_job_report_collection_summary_in_index(
            &explicit_index_path,
            &explicit_output_summary_path,
            &explicit_aggregate,
        )
        .expect("explicit register step should succeed");

        let wrapper_aggregate =
            load_query_summarize_persist_and_register_execution_result_job_report_collection_summary(
                &index_path,
                &query,
                &wrapper_output_summary_path,
            )
            .expect("wrapper pipeline should succeed");
        let wrapper_reloaded =
            load_execution_result_job_report_collection_summary(&wrapper_output_summary_path)
                .expect("wrapper persisted aggregate should reload");
        let wrapper_index = load_execution_result_job_report_collection_summary_index(&index_path)
            .expect("wrapper pipeline index should reload");
        let wrapper_entry = wrapper_index
            .entries
            .last()
            .expect("wrapper pipeline should append an index entry");

        assert_eq!(wrapper_aggregate, explicit_aggregate);
        assert_eq!(wrapper_reloaded, explicit_aggregate);
        assert_eq!(wrapper_entry.report_count, explicit_entry.report_count);
        assert_eq!(
            wrapper_entry.total_entry_count,
            explicit_entry.total_entry_count
        );
        assert_eq!(wrapper_entry.job_spec_ids, explicit_entry.job_spec_ids);
        assert_eq!(wrapper_entry.export_names, explicit_entry.export_names);
        assert_eq!(
            wrapper_entry.selection_modes,
            explicit_entry.selection_modes
        );
        assert_eq!(
            wrapper_entry.source_run_request_ids,
            explicit_entry.source_run_request_ids
        );
        assert_eq!(
            wrapper_entry.source_handoff_bundle_ids,
            explicit_entry.source_handoff_bundle_ids
        );
    }

    #[test]
    fn load_query_summarize_persist_register_and_index_load_execution_result_job_report_collection_summary_matches_explicit_pipeline()
     {
        let (
            directory,
            index_path,
            latest_only_summary_path,
            latest_only_summary,
            full_history_summary_path,
            full_history_summary,
        ) = persist_sample_execution_result_job_report_collection_summaries_with_index();
        let explicit_index_path = directory
            .path()
            .join("explicit-index-load-summary-index.json");
        let explicit_output_summary_path = directory
            .path()
            .join("explicit-index-load-aggregate-summary.json");
        let wrapper_output_summary_path = directory
            .path()
            .join("wrapper-index-load-aggregate-summary.json");
        let query = ExecutionResultJobReportCollectionSummaryIndexQuery {
            source_run_request_ids: vec!["run-request-shared".to_string()],
            source_handoff_bundle_ids: vec!["handoff-shared".to_string()],
            ..ExecutionResultJobReportCollectionSummaryIndexQuery::default()
        };

        register_execution_result_job_report_collection_summary_in_index(
            &explicit_index_path,
            &latest_only_summary_path,
            &latest_only_summary,
        )
        .expect("explicit latest-only seed summary should register");
        register_execution_result_job_report_collection_summary_in_index(
            &explicit_index_path,
            &full_history_summary_path,
            &full_history_summary,
        )
        .expect("explicit full-history seed summary should register");

        let explicit_aggregate =
            load_query_summarize_persist_and_register_execution_result_job_report_collection_summary(
                &explicit_index_path,
                &query,
                &explicit_output_summary_path,
            )
            .expect("explicit summarize, persist, and register step should succeed");
        let explicit_indexed_loaded = load_indexed_execution_result_job_report_collection_summary(
            &explicit_index_path,
            &path_to_owned_string(&explicit_output_summary_path)
                .expect("explicit output summary path should serialize"),
        )
        .expect("explicit indexed-load step should succeed");

        let wrapper_indexed_loaded = load_query_summarize_persist_register_and_index_load_execution_result_job_report_collection_summary(
            &index_path,
            &query,
            &wrapper_output_summary_path,
        )
        .expect("wrapper summarize, persist, register, and indexed-load path should succeed");

        assert_eq!(wrapper_indexed_loaded, explicit_aggregate);
        assert_eq!(wrapper_indexed_loaded, explicit_indexed_loaded);
    }

    #[test]
    fn load_query_summarize_persist_register_and_index_load_execution_result_job_report_collection_summary_latest_only_index_loads_one_summary_aggregate()
     {
        let (
            directory,
            index_path,
            _latest_only_summary_path,
            _latest_only_summary,
            _full_history_summary_path,
            full_history_summary,
        ) = persist_sample_execution_result_job_report_collection_summaries_with_index();
        let output_summary_path = directory
            .path()
            .join("wrapper-index-load-latest-only-summary.json");
        let query = ExecutionResultJobReportCollectionSummaryIndexQuery {
            latest_only: true,
            ..ExecutionResultJobReportCollectionSummaryIndexQuery::default()
        };

        let indexed_loaded = load_query_summarize_persist_register_and_index_load_execution_result_job_report_collection_summary(
            &index_path,
            &query,
            &output_summary_path,
        )
        .expect("latest-only indexed-load wrapper should succeed");

        assert_eq!(indexed_loaded, full_history_summary);
    }

    #[test]
    fn load_query_summarize_persist_register_and_index_load_execution_result_job_report_collection_summary_full_history_index_loads_aggregate_in_index_order()
     {
        let (
            directory,
            index_path,
            _latest_only_summary_path,
            latest_only_summary,
            _full_history_summary_path,
            full_history_summary,
        ) = persist_sample_execution_result_job_report_collection_summaries_with_index();
        let output_summary_path = directory
            .path()
            .join("wrapper-index-load-full-history-summary.json");
        let query = ExecutionResultJobReportCollectionSummaryIndexQuery::default();

        let indexed_loaded = load_query_summarize_persist_register_and_index_load_execution_result_job_report_collection_summary(
            &index_path,
            &query,
            &output_summary_path,
        )
        .expect("full-history indexed-load wrapper should succeed");

        assert_eq!(indexed_loaded.report_count, 4);
        assert_eq!(indexed_loaded.total_entry_count, 7);
        assert_eq!(
            indexed_loaded.job_spec_ids,
            vec![
                latest_only_summary.job_spec_ids[0].clone(),
                full_history_summary.job_spec_ids[0].clone(),
                full_history_summary.job_spec_ids[1].clone(),
                full_history_summary.job_spec_ids[2].clone(),
            ]
        );
        assert_eq!(
            indexed_loaded.export_names,
            vec![
                latest_only_summary.export_names[0].clone(),
                full_history_summary.export_names[0].clone(),
            ]
        );
        assert_eq!(
            indexed_loaded.selection_modes,
            vec![
                latest_only_summary.selection_modes[0],
                full_history_summary.selection_modes[0],
            ]
        );
    }

    #[test]
    fn load_query_summarize_persist_register_and_index_load_execution_result_job_report_collection_summary_indexed_loaded_aggregate_reloads_exactly()
     {
        let (
            directory,
            index_path,
            _latest_only_summary_path,
            _latest_only_summary,
            _full_history_summary_path,
            _full_history_summary,
        ) = persist_sample_execution_result_job_report_collection_summaries_with_index();
        let output_summary_path = directory
            .path()
            .join("wrapper-index-load-reload-summary.json");
        let query = ExecutionResultJobReportCollectionSummaryIndexQuery::default();

        let indexed_loaded = load_query_summarize_persist_register_and_index_load_execution_result_job_report_collection_summary(
            &index_path,
            &query,
            &output_summary_path,
        )
        .expect("indexed-load wrapper should succeed");
        let direct_reloaded =
            load_execution_result_job_report_collection_summary(&output_summary_path)
                .expect("persisted aggregate summary should reload directly");

        assert_eq!(indexed_loaded, direct_reloaded);
    }

    #[test]
    fn load_query_summarize_persist_register_and_index_load_execution_result_job_report_collection_summary_has_no_field_drift_vs_explicit_pipeline()
     {
        let (
            directory,
            index_path,
            latest_only_summary_path,
            latest_only_summary,
            full_history_summary_path,
            full_history_summary,
        ) = persist_sample_execution_result_job_report_collection_summaries_with_index();
        let explicit_index_path = directory
            .path()
            .join("explicit-index-load-no-drift-index.json");
        let explicit_output_summary_path = directory
            .path()
            .join("explicit-index-load-no-drift-summary.json");
        let wrapper_output_summary_path = directory
            .path()
            .join("wrapper-index-load-no-drift-summary.json");
        let query = ExecutionResultJobReportCollectionSummaryIndexQuery::default();

        register_execution_result_job_report_collection_summary_in_index(
            &explicit_index_path,
            &latest_only_summary_path,
            &latest_only_summary,
        )
        .expect("explicit latest-only seed summary should register");
        register_execution_result_job_report_collection_summary_in_index(
            &explicit_index_path,
            &full_history_summary_path,
            &full_history_summary,
        )
        .expect("explicit full-history seed summary should register");

        load_query_summarize_persist_and_register_execution_result_job_report_collection_summary(
            &explicit_index_path,
            &query,
            &explicit_output_summary_path,
        )
        .expect("explicit summarize, persist, and register step should succeed");
        let explicit_indexed_loaded = load_indexed_execution_result_job_report_collection_summary(
            &explicit_index_path,
            &path_to_owned_string(&explicit_output_summary_path)
                .expect("explicit output summary path should serialize"),
        )
        .expect("explicit indexed-loaded aggregate summary should reload");

        let wrapper_indexed_loaded = load_query_summarize_persist_register_and_index_load_execution_result_job_report_collection_summary(
            &index_path,
            &query,
            &wrapper_output_summary_path,
        )
        .expect("wrapper indexed-load path should succeed");

        assert_eq!(wrapper_indexed_loaded, explicit_indexed_loaded);
        assert_eq!(
            wrapper_indexed_loaded.shared_export_name,
            explicit_indexed_loaded.shared_export_name
        );
        assert_eq!(
            wrapper_indexed_loaded.shared_selection_mode,
            explicit_indexed_loaded.shared_selection_mode
        );
        assert_eq!(
            wrapper_indexed_loaded.job_spec_ids,
            explicit_indexed_loaded.job_spec_ids
        );
        assert_eq!(
            wrapper_indexed_loaded.export_names,
            explicit_indexed_loaded.export_names
        );
        assert_eq!(
            wrapper_indexed_loaded.selection_modes,
            explicit_indexed_loaded.selection_modes
        );
        assert_eq!(
            wrapper_indexed_loaded.source_run_request_ids,
            explicit_indexed_loaded.source_run_request_ids
        );
        assert_eq!(
            wrapper_indexed_loaded.source_handoff_bundle_ids,
            explicit_indexed_loaded.source_handoff_bundle_ids
        );
    }

    #[test]
    fn load_query_reports_summarize_persist_register_and_index_load_execution_result_job_report_collection_summary_matches_explicit_pipeline()
     {
        let (directory, report_index_path, reports) =
            persist_sample_execution_result_job_reports_with_index();
        let explicit_summary_index_path =
            directory.path().join("stage24-explicit-summary-index.json");
        let explicit_output_summary_path = directory.path().join("stage24-explicit-summary.json");
        let wrapper_summary_index_path =
            directory.path().join("stage24-wrapper-summary-index.json");
        let wrapper_output_summary_path = directory.path().join("stage24-wrapper-summary.json");
        let query = ExecutionResultJobReportIndexQuery {
            job_spec_id: Some(reports[1].job_spec_id.clone()),
            ..ExecutionResultJobReportIndexQuery::default()
        };

        let explicit_loaded =
            load_and_query_execution_result_job_reports(&report_index_path, &query)
                .expect("explicit stage24 report query/load should succeed");
        let explicit_summary = summarize_execution_result_job_reports(&explicit_loaded);
        persist_execution_result_job_report_collection_summary(
            &explicit_output_summary_path,
            &explicit_summary,
        )
        .expect("explicit stage24 summary persist should succeed");
        register_execution_result_job_report_collection_summary_in_index(
            &explicit_summary_index_path,
            &explicit_output_summary_path,
            &explicit_summary,
        )
        .expect("explicit stage24 summary register should succeed");
        let explicit_indexed_loaded = load_indexed_execution_result_job_report_collection_summary(
            &explicit_summary_index_path,
            &path_to_owned_string(&explicit_output_summary_path)
                .expect("explicit stage24 summary path should serialize"),
        )
        .expect("explicit stage24 indexed-load should succeed");

        let wrapper_indexed_loaded = load_query_reports_summarize_persist_register_and_index_load_execution_result_job_report_collection_summary(
            &report_index_path,
            &query,
            &wrapper_summary_index_path,
            &wrapper_output_summary_path,
        )
        .expect("stage24 wrapper should match explicit pipeline");

        assert_eq!(wrapper_indexed_loaded, explicit_summary);
        assert_eq!(wrapper_indexed_loaded, explicit_indexed_loaded);
    }

    #[test]
    fn load_query_reports_summarize_persist_register_and_index_load_execution_result_job_report_collection_summary_latest_only_produces_one_report_summary()
     {
        let (directory, report_index_path, reports) =
            persist_sample_execution_result_job_reports_with_index();
        let summary_index_path = directory
            .path()
            .join("stage24-latest-only-summary-index.json");
        let output_summary_path = directory.path().join("stage24-latest-only-summary.json");
        let query = ExecutionResultJobReportIndexQuery {
            source_run_request_id: Some("run-request-shared".to_string()),
            source_handoff_bundle_id: Some("handoff-shared".to_string()),
            latest_only: true,
            ..ExecutionResultJobReportIndexQuery::default()
        };

        let indexed_loaded = load_query_reports_summarize_persist_register_and_index_load_execution_result_job_report_collection_summary(
            &report_index_path,
            &query,
            &summary_index_path,
            &output_summary_path,
        )
        .expect("stage24 latest-only wrapper should succeed");

        assert_eq!(indexed_loaded.report_count, 1);
        assert_eq!(indexed_loaded.total_entry_count, reports[2].entries.len());
        assert_eq!(
            indexed_loaded.job_spec_ids,
            vec![reports[2].job_spec_id.clone()]
        );
        assert_eq!(
            indexed_loaded.export_names,
            vec![reports[2].export_name.clone()]
        );
        assert_eq!(
            indexed_loaded.selection_modes,
            vec![reports[2].selection_mode]
        );
    }

    #[test]
    fn load_query_reports_summarize_persist_register_and_index_load_execution_result_job_report_collection_summary_full_history_produces_aggregate_in_report_index_order()
     {
        let (directory, report_index_path, reports) =
            persist_sample_execution_result_job_reports_with_index();
        let summary_index_path = directory
            .path()
            .join("stage24-full-history-summary-index.json");
        let output_summary_path = directory.path().join("stage24-full-history-summary.json");
        let query = ExecutionResultJobReportIndexQuery {
            source_run_request_id: Some("run-request-shared".to_string()),
            source_handoff_bundle_id: Some("handoff-shared".to_string()),
            ..ExecutionResultJobReportIndexQuery::default()
        };

        let indexed_loaded = load_query_reports_summarize_persist_register_and_index_load_execution_result_job_report_collection_summary(
            &report_index_path,
            &query,
            &summary_index_path,
            &output_summary_path,
        )
        .expect("stage24 full-history wrapper should succeed");

        assert_eq!(indexed_loaded.report_count, reports.len());
        assert_eq!(
            indexed_loaded.total_entry_count,
            reports
                .iter()
                .map(|report| report.entries.len())
                .sum::<usize>()
        );
        assert_eq!(
            indexed_loaded.job_spec_ids,
            reports
                .iter()
                .map(|report| report.job_spec_id.clone())
                .collect::<Vec<_>>()
        );
        assert_eq!(
            indexed_loaded.export_names,
            vec![reports[0].export_name.clone()]
        );
        assert_eq!(
            indexed_loaded.selection_modes,
            vec![reports[0].selection_mode, reports[1].selection_mode,]
        );
    }

    #[test]
    fn load_query_reports_summarize_persist_register_and_index_load_execution_result_job_report_collection_summary_indexed_loaded_summary_reloads_exactly()
     {
        let (directory, report_index_path, _) =
            persist_sample_execution_result_job_reports_with_index();
        let summary_index_path = directory.path().join("stage24-reload-summary-index.json");
        let output_summary_path = directory.path().join("stage24-reload-summary.json");
        let query = ExecutionResultJobReportIndexQuery::default();

        let indexed_loaded = load_query_reports_summarize_persist_register_and_index_load_execution_result_job_report_collection_summary(
            &report_index_path,
            &query,
            &summary_index_path,
            &output_summary_path,
        )
        .expect("stage24 reload wrapper should succeed");
        let direct_reloaded =
            load_execution_result_job_report_collection_summary(&output_summary_path)
                .expect("stage24 persisted summary should reload directly");

        assert_eq!(indexed_loaded, direct_reloaded);
    }

    #[test]
    fn load_query_reports_summarize_persist_register_and_index_load_execution_result_job_report_collection_summary_has_no_field_drift_vs_explicit_pipeline()
     {
        let (directory, report_index_path, _) =
            persist_sample_execution_result_job_reports_with_index();
        let explicit_summary_index_path = directory
            .path()
            .join("stage24-no-drift-explicit-summary-index.json");
        let explicit_output_summary_path = directory
            .path()
            .join("stage24-no-drift-explicit-summary.json");
        let wrapper_summary_index_path = directory
            .path()
            .join("stage24-no-drift-wrapper-summary-index.json");
        let wrapper_output_summary_path = directory
            .path()
            .join("stage24-no-drift-wrapper-summary.json");
        let query = ExecutionResultJobReportIndexQuery::default();

        let explicit_loaded =
            load_and_query_execution_result_job_reports(&report_index_path, &query)
                .expect("explicit stage24 no-drift report query/load should succeed");
        let explicit_summary = summarize_execution_result_job_reports(&explicit_loaded);
        persist_execution_result_job_report_collection_summary(
            &explicit_output_summary_path,
            &explicit_summary,
        )
        .expect("explicit stage24 no-drift summary persist should succeed");
        register_execution_result_job_report_collection_summary_in_index(
            &explicit_summary_index_path,
            &explicit_output_summary_path,
            &explicit_summary,
        )
        .expect("explicit stage24 no-drift summary register should succeed");
        let explicit_indexed_loaded = load_indexed_execution_result_job_report_collection_summary(
            &explicit_summary_index_path,
            &path_to_owned_string(&explicit_output_summary_path)
                .expect("explicit stage24 no-drift summary path should serialize"),
        )
        .expect("explicit stage24 no-drift indexed-load should succeed");

        let wrapper_indexed_loaded = load_query_reports_summarize_persist_register_and_index_load_execution_result_job_report_collection_summary(
            &report_index_path,
            &query,
            &wrapper_summary_index_path,
            &wrapper_output_summary_path,
        )
        .expect("stage24 no-drift wrapper should succeed");

        assert_eq!(wrapper_indexed_loaded, explicit_indexed_loaded);
        assert_eq!(
            wrapper_indexed_loaded.shared_export_name,
            explicit_indexed_loaded.shared_export_name
        );
        assert_eq!(
            wrapper_indexed_loaded.shared_selection_mode,
            explicit_indexed_loaded.shared_selection_mode
        );
        assert_eq!(
            wrapper_indexed_loaded.job_spec_ids,
            explicit_indexed_loaded.job_spec_ids
        );
        assert_eq!(
            wrapper_indexed_loaded.export_names,
            explicit_indexed_loaded.export_names
        );
        assert_eq!(
            wrapper_indexed_loaded.selection_modes,
            explicit_indexed_loaded.selection_modes
        );
        assert_eq!(
            wrapper_indexed_loaded.source_run_request_ids,
            explicit_indexed_loaded.source_run_request_ids
        );
        assert_eq!(
            wrapper_indexed_loaded.source_handoff_bundle_ids,
            explicit_indexed_loaded.source_handoff_bundle_ids
        );
    }

    #[test]
    fn query_stub_execute_register_report_and_index_load_summary_matches_explicit_pipeline() {
        let (directory, _) = sample_execution_ledger_history();
        let bundle_dir = directory.path().join("bundle");
        let explicit_report_path = directory.path().join("stage25-explicit-report.json");
        let explicit_report_index_path =
            directory.path().join("stage25-explicit-report-index.json");
        let explicit_summary_index_path =
            directory.path().join("stage25-explicit-summary-index.json");
        let explicit_output_summary_path = directory.path().join("stage25-explicit-summary.json");
        let wrapper_report_path = directory.path().join("stage25-wrapper-report.json");
        let wrapper_report_index_path = directory.path().join("stage25-wrapper-report-index.json");
        let wrapper_summary_index_path =
            directory.path().join("stage25-wrapper-summary-index.json");
        let wrapper_output_summary_path = directory.path().join("stage25-wrapper-summary.json");
        let ledger_query = LedgerSelectionQuery {
            status: Some(ExecutionResultStatus::StubbedSuccess),
            anchor_id: Some("anchor-1".to_string()),
            ..LedgerSelectionQuery::default()
        };
        let report_index_query = ExecutionResultJobReportIndexQuery {
            job_spec_id: Some("job-spec-stage25-match".to_string()),
            ..ExecutionResultJobReportIndexQuery::default()
        };

        query_stub_execute_persist_load_and_register_execution_result_job_report(
            &bundle_dir,
            &ledger_query,
            "handoff-stage25-match",
            "run-request-stage25-match",
            "job-spec-stage25-match",
            ExecutionResultSelectionMode::FullHistory,
            &explicit_report_path,
            &explicit_report_index_path,
        )
        .expect("explicit stage25 report pipeline should succeed");
        let explicit_loaded_reports = load_and_query_execution_result_job_reports(
            &explicit_report_index_path,
            &report_index_query,
        )
        .expect("explicit stage25 report query/load should succeed");
        let explicit_summary = summarize_execution_result_job_reports(&explicit_loaded_reports);
        persist_execution_result_job_report_collection_summary(
            &explicit_output_summary_path,
            &explicit_summary,
        )
        .expect("explicit stage25 summary persist should succeed");
        register_execution_result_job_report_collection_summary_in_index(
            &explicit_summary_index_path,
            &explicit_output_summary_path,
            &explicit_summary,
        )
        .expect("explicit stage25 summary register should succeed");
        let explicit_indexed_loaded = load_indexed_execution_result_job_report_collection_summary(
            &explicit_summary_index_path,
            &path_to_owned_string(&explicit_output_summary_path)
                .expect("explicit stage25 summary path should serialize"),
        )
        .expect("explicit stage25 summary indexed-load should succeed");

        let wrapper_indexed_loaded = query_stub_execute_register_report_and_index_load_summary(
            &bundle_dir,
            &ledger_query,
            "handoff-stage25-match",
            "run-request-stage25-match",
            "job-spec-stage25-match",
            ExecutionResultSelectionMode::FullHistory,
            &wrapper_report_path,
            &wrapper_report_index_path,
            &report_index_query,
            &wrapper_summary_index_path,
            &wrapper_output_summary_path,
        )
        .expect("stage25 wrapper should match explicit pipeline");

        assert_eq!(wrapper_indexed_loaded, explicit_summary);
        assert_eq!(wrapper_indexed_loaded, explicit_indexed_loaded);
    }

    #[test]
    fn query_stub_execute_register_report_and_index_load_summary_latest_only_produces_one_report_summary_correctly()
     {
        let (directory, _) = sample_execution_ledger_history();
        let bundle_dir = directory.path().join("bundle");
        let report_index_path = directory.path().join("stage25-latest-report-index.json");
        let first_report_path = directory.path().join("stage25-latest-first-report.json");
        let wrapper_report_path = directory.path().join("stage25-latest-wrapper-report.json");
        let summary_index_path = directory.path().join("stage25-latest-summary-index.json");
        let output_summary_path = directory.path().join("stage25-latest-summary.json");
        let ledger_query = LedgerSelectionQuery {
            request_id: Some("request-shared".to_string()),
            ..LedgerSelectionQuery::default()
        };

        query_stub_execute_persist_load_and_register_execution_result_job_report(
            &bundle_dir,
            &ledger_query,
            "handoff-stage25-latest-shared",
            "run-request-stage25-latest-shared",
            "job-spec-stage25-latest-first",
            ExecutionResultSelectionMode::FullHistory,
            &first_report_path,
            &report_index_path,
        )
        .expect("first stage25 latest report should register");

        let report_index_query = ExecutionResultJobReportIndexQuery {
            source_run_request_id: Some("run-request-stage25-latest-shared".to_string()),
            source_handoff_bundle_id: Some("handoff-stage25-latest-shared".to_string()),
            latest_only: true,
            ..ExecutionResultJobReportIndexQuery::default()
        };

        let indexed_loaded = query_stub_execute_register_report_and_index_load_summary(
            &bundle_dir,
            &ledger_query,
            "handoff-stage25-latest-shared",
            "run-request-stage25-latest-shared",
            "job-spec-stage25-latest-second",
            ExecutionResultSelectionMode::LatestOnly,
            &wrapper_report_path,
            &report_index_path,
            &report_index_query,
            &summary_index_path,
            &output_summary_path,
        )
        .expect("stage25 latest-only wrapper should succeed");

        assert_eq!(indexed_loaded.report_count, 1);
        assert_eq!(
            indexed_loaded.job_spec_ids,
            vec!["job-spec-stage25-latest-second".to_string()]
        );
        assert_eq!(
            indexed_loaded.source_run_request_ids,
            vec!["run-request-stage25-latest-shared".to_string()]
        );
        assert_eq!(
            indexed_loaded.source_handoff_bundle_ids,
            vec!["handoff-stage25-latest-shared".to_string()]
        );
    }

    #[test]
    fn query_stub_execute_register_report_and_index_load_summary_full_history_produces_aggregate_summary_in_report_index_order()
     {
        let (directory, _) = sample_execution_ledger_history();
        let bundle_dir = directory.path().join("bundle");
        let report_index_path = directory
            .path()
            .join("stage25-full-history-report-index.json");
        let first_report_path = directory
            .path()
            .join("stage25-full-history-first-report.json");
        let second_report_path = directory
            .path()
            .join("stage25-full-history-second-report.json");
        let wrapper_report_path = directory
            .path()
            .join("stage25-full-history-wrapper-report.json");
        let summary_index_path = directory
            .path()
            .join("stage25-full-history-summary-index.json");
        let output_summary_path = directory.path().join("stage25-full-history-summary.json");
        let ledger_query = LedgerSelectionQuery {
            request_id: Some("request-shared".to_string()),
            ..LedgerSelectionQuery::default()
        };

        query_stub_execute_persist_load_and_register_execution_result_job_report(
            &bundle_dir,
            &ledger_query,
            "handoff-stage25-full-history-shared",
            "run-request-stage25-full-history-shared",
            "job-spec-stage25-full-history-first",
            ExecutionResultSelectionMode::FullHistory,
            &first_report_path,
            &report_index_path,
        )
        .expect("first stage25 full-history report should register");
        query_stub_execute_persist_load_and_register_execution_result_job_report(
            &bundle_dir,
            &ledger_query,
            "handoff-stage25-full-history-shared",
            "run-request-stage25-full-history-shared",
            "job-spec-stage25-full-history-second",
            ExecutionResultSelectionMode::LatestOnly,
            &second_report_path,
            &report_index_path,
        )
        .expect("second stage25 full-history report should register");

        let report_index_query = ExecutionResultJobReportIndexQuery {
            source_run_request_id: Some("run-request-stage25-full-history-shared".to_string()),
            source_handoff_bundle_id: Some("handoff-stage25-full-history-shared".to_string()),
            ..ExecutionResultJobReportIndexQuery::default()
        };

        let indexed_loaded = query_stub_execute_register_report_and_index_load_summary(
            &bundle_dir,
            &ledger_query,
            "handoff-stage25-full-history-shared",
            "run-request-stage25-full-history-shared",
            "job-spec-stage25-full-history-third",
            ExecutionResultSelectionMode::FullHistory,
            &wrapper_report_path,
            &report_index_path,
            &report_index_query,
            &summary_index_path,
            &output_summary_path,
        )
        .expect("stage25 full-history wrapper should succeed");

        assert_eq!(indexed_loaded.report_count, 3);
        assert_eq!(
            indexed_loaded.job_spec_ids,
            vec![
                "job-spec-stage25-full-history-first".to_string(),
                "job-spec-stage25-full-history-second".to_string(),
                "job-spec-stage25-full-history-third".to_string(),
            ]
        );
        assert_eq!(
            indexed_loaded.selection_modes,
            vec![
                ExecutionResultSelectionMode::FullHistory,
                ExecutionResultSelectionMode::LatestOnly,
            ]
        );
    }

    #[test]
    fn query_stub_execute_register_report_and_index_load_summary_indexed_loaded_summary_reloads_exactly()
     {
        let (directory, _) = sample_execution_ledger_history();
        let bundle_dir = directory.path().join("bundle");
        let report_path = directory.path().join("stage25-reload-report.json");
        let report_index_path = directory.path().join("stage25-reload-report-index.json");
        let summary_index_path = directory.path().join("stage25-reload-summary-index.json");
        let output_summary_path = directory.path().join("stage25-reload-summary.json");
        let ledger_query = LedgerSelectionQuery {
            status: Some(ExecutionResultStatus::StubbedSuccess),
            ..LedgerSelectionQuery::default()
        };
        let report_index_query = ExecutionResultJobReportIndexQuery::default();

        let indexed_loaded = query_stub_execute_register_report_and_index_load_summary(
            &bundle_dir,
            &ledger_query,
            "handoff-stage25-reload",
            "run-request-stage25-reload",
            "job-spec-stage25-reload",
            ExecutionResultSelectionMode::FullHistory,
            &report_path,
            &report_index_path,
            &report_index_query,
            &summary_index_path,
            &output_summary_path,
        )
        .expect("stage25 reload wrapper should succeed");
        let direct_reloaded =
            load_execution_result_job_report_collection_summary(&output_summary_path)
                .expect("stage25 persisted summary should reload directly");

        assert_eq!(indexed_loaded, direct_reloaded);
    }

    #[test]
    fn query_stub_execute_register_report_and_index_load_summary_has_no_field_drift_vs_explicit_pipeline()
     {
        let (directory, _) = sample_execution_ledger_history();
        let bundle_dir = directory.path().join("bundle");
        let explicit_report_path = directory
            .path()
            .join("stage25-no-drift-explicit-report.json");
        let explicit_report_index_path = directory
            .path()
            .join("stage25-no-drift-explicit-report-index.json");
        let explicit_summary_index_path = directory
            .path()
            .join("stage25-no-drift-explicit-summary-index.json");
        let explicit_output_summary_path = directory
            .path()
            .join("stage25-no-drift-explicit-summary.json");
        let wrapper_report_path = directory
            .path()
            .join("stage25-no-drift-wrapper-report.json");
        let wrapper_report_index_path = directory
            .path()
            .join("stage25-no-drift-wrapper-report-index.json");
        let wrapper_summary_index_path = directory
            .path()
            .join("stage25-no-drift-wrapper-summary-index.json");
        let wrapper_output_summary_path = directory
            .path()
            .join("stage25-no-drift-wrapper-summary.json");
        let ledger_query = LedgerSelectionQuery::default();
        let report_index_query = ExecutionResultJobReportIndexQuery::default();

        query_stub_execute_persist_load_and_register_execution_result_job_report(
            &bundle_dir,
            &ledger_query,
            "handoff-stage25-no-drift",
            "run-request-stage25-no-drift",
            "job-spec-stage25-no-drift",
            ExecutionResultSelectionMode::FullHistory,
            &explicit_report_path,
            &explicit_report_index_path,
        )
        .expect("explicit stage25 no-drift report pipeline should succeed");
        let explicit_loaded_reports = load_and_query_execution_result_job_reports(
            &explicit_report_index_path,
            &report_index_query,
        )
        .expect("explicit stage25 no-drift report query/load should succeed");
        let explicit_summary = summarize_execution_result_job_reports(&explicit_loaded_reports);
        persist_execution_result_job_report_collection_summary(
            &explicit_output_summary_path,
            &explicit_summary,
        )
        .expect("explicit stage25 no-drift summary persist should succeed");
        register_execution_result_job_report_collection_summary_in_index(
            &explicit_summary_index_path,
            &explicit_output_summary_path,
            &explicit_summary,
        )
        .expect("explicit stage25 no-drift summary register should succeed");
        let explicit_indexed_loaded = load_indexed_execution_result_job_report_collection_summary(
            &explicit_summary_index_path,
            &path_to_owned_string(&explicit_output_summary_path)
                .expect("explicit stage25 no-drift summary path should serialize"),
        )
        .expect("explicit stage25 no-drift summary indexed-load should succeed");

        let wrapper_indexed_loaded = query_stub_execute_register_report_and_index_load_summary(
            &bundle_dir,
            &ledger_query,
            "handoff-stage25-no-drift",
            "run-request-stage25-no-drift",
            "job-spec-stage25-no-drift",
            ExecutionResultSelectionMode::FullHistory,
            &wrapper_report_path,
            &wrapper_report_index_path,
            &report_index_query,
            &wrapper_summary_index_path,
            &wrapper_output_summary_path,
        )
        .expect("stage25 no-drift wrapper should succeed");

        assert_eq!(wrapper_indexed_loaded, explicit_indexed_loaded);
        assert_eq!(
            wrapper_indexed_loaded.shared_export_name,
            explicit_indexed_loaded.shared_export_name
        );
        assert_eq!(
            wrapper_indexed_loaded.shared_selection_mode,
            explicit_indexed_loaded.shared_selection_mode
        );
        assert_eq!(
            wrapper_indexed_loaded.job_spec_ids,
            explicit_indexed_loaded.job_spec_ids
        );
        assert_eq!(
            wrapper_indexed_loaded.export_names,
            explicit_indexed_loaded.export_names
        );
        assert_eq!(
            wrapper_indexed_loaded.selection_modes,
            explicit_indexed_loaded.selection_modes
        );
        assert_eq!(
            wrapper_indexed_loaded.source_run_request_ids,
            explicit_indexed_loaded.source_run_request_ids
        );
        assert_eq!(
            wrapper_indexed_loaded.source_handoff_bundle_ids,
            explicit_indexed_loaded.source_handoff_bundle_ids
        );
    }

    #[test]
    fn query_stub_execute_register_report_and_aggregate_queried_execution_result_job_report_collection_summaries_matches_explicit_pipeline()
     {
        let (directory, _) = sample_execution_ledger_history();
        let bundle_dir = directory.path().join("bundle");
        let explicit_report_path = directory.path().join("stage27-explicit-report.json");
        let explicit_report_index_path =
            directory.path().join("stage27-explicit-report-index.json");
        let explicit_summary_index_path =
            directory.path().join("stage27-explicit-summary-index.json");
        let explicit_output_summary_path = directory.path().join("stage27-explicit-summary.json");
        let explicit_aggregate_output_summary_path = directory
            .path()
            .join("stage27-explicit-aggregate-summary.json");
        let wrapper_report_path = directory.path().join("stage27-wrapper-report.json");
        let wrapper_report_index_path = directory.path().join("stage27-wrapper-report-index.json");
        let wrapper_summary_index_path =
            directory.path().join("stage27-wrapper-summary-index.json");
        let wrapper_output_summary_path = directory.path().join("stage27-wrapper-summary.json");
        let wrapper_aggregate_output_summary_path = directory
            .path()
            .join("stage27-wrapper-aggregate-summary.json");
        let ledger_query = LedgerSelectionQuery {
            status: Some(ExecutionResultStatus::StubbedSuccess),
            anchor_id: Some("anchor-1".to_string()),
            ..LedgerSelectionQuery::default()
        };
        let report_index_query = ExecutionResultJobReportIndexQuery {
            job_spec_id: Some("job-spec-stage27-match".to_string()),
            ..ExecutionResultJobReportIndexQuery::default()
        };
        let summary_index_query = ExecutionResultJobReportCollectionSummaryIndexQuery::default();

        query_stub_execute_register_report_and_index_load_summary(
            &bundle_dir,
            &ledger_query,
            "handoff-stage27-match",
            "run-request-stage27-match",
            "job-spec-stage27-match",
            ExecutionResultSelectionMode::FullHistory,
            &explicit_report_path,
            &explicit_report_index_path,
            &report_index_query,
            &explicit_summary_index_path,
            &explicit_output_summary_path,
        )
        .expect("explicit stage27 stage25 wrapper should succeed");
        let explicit_indexed_loaded =
            load_query_summarize_persist_register_and_index_load_execution_result_job_report_collection_summary(
                &explicit_summary_index_path,
                &summary_index_query,
                &explicit_aggregate_output_summary_path,
            )
            .expect("explicit stage27 stage23 wrapper should succeed");

        let wrapper_indexed_loaded =
            query_stub_execute_register_report_and_aggregate_queried_execution_result_job_report_collection_summaries(
                &bundle_dir,
                &ledger_query,
                "handoff-stage27-match",
                "run-request-stage27-match",
                "job-spec-stage27-match",
                ExecutionResultSelectionMode::FullHistory,
                &wrapper_report_path,
                &wrapper_report_index_path,
                &report_index_query,
                &wrapper_summary_index_path,
                &wrapper_output_summary_path,
                &summary_index_query,
                &wrapper_aggregate_output_summary_path,
            )
            .expect("stage27 wrapper should match explicit pipeline");

        assert_eq!(wrapper_indexed_loaded, explicit_indexed_loaded);
    }

    #[test]
    fn query_stub_execute_register_report_and_aggregate_queried_execution_result_job_report_collection_summaries_latest_only_produces_one_summary_aggregate_correctly()
     {
        let (directory, _) = sample_execution_ledger_history();
        let bundle_dir = directory.path().join("bundle");
        let report_index_path = directory.path().join("stage27-latest-report-index.json");
        let first_report_path = directory.path().join("stage27-latest-first-report.json");
        let wrapper_report_path = directory.path().join("stage27-latest-wrapper-report.json");
        let summary_index_path = directory.path().join("stage27-latest-summary-index.json");
        let output_summary_path = directory.path().join("stage27-latest-summary.json");
        let aggregate_output_summary_path = directory
            .path()
            .join("stage27-latest-aggregate-summary.json");
        let ledger_query = LedgerSelectionQuery {
            request_id: Some("request-shared".to_string()),
            ..LedgerSelectionQuery::default()
        };

        query_stub_execute_persist_load_and_register_execution_result_job_report(
            &bundle_dir,
            &ledger_query,
            "handoff-stage27-latest-shared",
            "run-request-stage27-latest-shared",
            "job-spec-stage27-latest-first",
            ExecutionResultSelectionMode::FullHistory,
            &first_report_path,
            &report_index_path,
        )
        .expect("first stage27 latest report should register");

        let report_index_query = ExecutionResultJobReportIndexQuery {
            source_run_request_id: Some("run-request-stage27-latest-shared".to_string()),
            source_handoff_bundle_id: Some("handoff-stage27-latest-shared".to_string()),
            latest_only: true,
            ..ExecutionResultJobReportIndexQuery::default()
        };
        let summary_index_query = ExecutionResultJobReportCollectionSummaryIndexQuery {
            source_run_request_ids: vec!["run-request-stage27-latest-shared".to_string()],
            source_handoff_bundle_ids: vec!["handoff-stage27-latest-shared".to_string()],
            latest_only: true,
            ..ExecutionResultJobReportCollectionSummaryIndexQuery::default()
        };

        let indexed_loaded =
            query_stub_execute_register_report_and_aggregate_queried_execution_result_job_report_collection_summaries(
                &bundle_dir,
                &ledger_query,
                "handoff-stage27-latest-shared",
                "run-request-stage27-latest-shared",
                "job-spec-stage27-latest-second",
                ExecutionResultSelectionMode::LatestOnly,
                &wrapper_report_path,
                &report_index_path,
                &report_index_query,
                &summary_index_path,
                &output_summary_path,
                &summary_index_query,
                &aggregate_output_summary_path,
            )
            .expect("stage27 latest-only wrapper should succeed");

        assert_eq!(indexed_loaded.report_count, 1);
        assert_eq!(indexed_loaded.total_entry_count, 1);
        assert_eq!(
            indexed_loaded.job_spec_ids,
            vec!["job-spec-stage27-latest-second".to_string()]
        );
    }

    #[test]
    fn query_stub_execute_register_report_and_aggregate_queried_execution_result_job_report_collection_summaries_full_history_produces_registers_and_aggregates_in_summary_index_order()
     {
        let (directory, _) = sample_execution_ledger_history();
        let bundle_dir = directory.path().join("bundle");
        let report_index_path = directory.path().join("stage27-history-report-index.json");
        let first_report_path = directory.path().join("stage27-history-first-report.json");
        let second_report_path = directory.path().join("stage27-history-second-report.json");
        let third_report_path = directory.path().join("stage27-history-third-report.json");
        let summary_index_path = directory.path().join("stage27-history-summary-index.json");
        let first_output_summary_path = directory.path().join("stage27-history-first-summary.json");
        let second_output_summary_path =
            directory.path().join("stage27-history-second-summary.json");
        let wrapper_output_summary_path = directory
            .path()
            .join("stage27-history-wrapper-summary.json");
        let aggregate_output_summary_path = directory
            .path()
            .join("stage27-history-aggregate-summary.json");
        let ledger_query = LedgerSelectionQuery {
            request_id: Some("request-shared".to_string()),
            ..LedgerSelectionQuery::default()
        };

        query_stub_execute_register_report_and_index_load_summary(
            &bundle_dir,
            &ledger_query,
            "handoff-stage27-history-shared",
            "run-request-stage27-history-shared",
            "job-spec-stage27-history-first",
            ExecutionResultSelectionMode::FullHistory,
            &first_report_path,
            &report_index_path,
            &ExecutionResultJobReportIndexQuery {
                source_run_request_id: Some("run-request-stage27-history-shared".to_string()),
                source_handoff_bundle_id: Some("handoff-stage27-history-shared".to_string()),
                job_spec_id: Some("job-spec-stage27-history-first".to_string()),
                ..ExecutionResultJobReportIndexQuery::default()
            },
            &summary_index_path,
            &first_output_summary_path,
        )
        .expect("first stage27 history summary should register");
        query_stub_execute_register_report_and_index_load_summary(
            &bundle_dir,
            &ledger_query,
            "handoff-stage27-history-shared",
            "run-request-stage27-history-shared",
            "job-spec-stage27-history-second",
            ExecutionResultSelectionMode::LatestOnly,
            &second_report_path,
            &report_index_path,
            &ExecutionResultJobReportIndexQuery {
                source_run_request_id: Some("run-request-stage27-history-shared".to_string()),
                source_handoff_bundle_id: Some("handoff-stage27-history-shared".to_string()),
                latest_only: true,
                ..ExecutionResultJobReportIndexQuery::default()
            },
            &summary_index_path,
            &second_output_summary_path,
        )
        .expect("second stage27 history summary should register");

        let report_index_query = ExecutionResultJobReportIndexQuery {
            source_run_request_id: Some("run-request-stage27-history-shared".to_string()),
            source_handoff_bundle_id: Some("handoff-stage27-history-shared".to_string()),
            ..ExecutionResultJobReportIndexQuery::default()
        };
        let summary_index_query = ExecutionResultJobReportCollectionSummaryIndexQuery {
            source_run_request_ids: vec!["run-request-stage27-history-shared".to_string()],
            source_handoff_bundle_ids: vec!["handoff-stage27-history-shared".to_string()],
            ..ExecutionResultJobReportCollectionSummaryIndexQuery::default()
        };

        let indexed_loaded =
            query_stub_execute_register_report_and_aggregate_queried_execution_result_job_report_collection_summaries(
                &bundle_dir,
                &ledger_query,
                "handoff-stage27-history-shared",
                "run-request-stage27-history-shared",
                "job-spec-stage27-history-third",
                ExecutionResultSelectionMode::FullHistory,
                &third_report_path,
                &report_index_path,
                &report_index_query,
                &summary_index_path,
                &wrapper_output_summary_path,
                &summary_index_query,
                &aggregate_output_summary_path,
            )
            .expect("stage27 history wrapper should succeed");

        assert_eq!(indexed_loaded.report_count, 5);
        assert_eq!(indexed_loaded.total_entry_count, 8);
        assert_eq!(
            indexed_loaded.job_spec_ids,
            vec![
                "job-spec-stage27-history-first".to_string(),
                "job-spec-stage27-history-second".to_string(),
                "job-spec-stage27-history-third".to_string(),
            ]
        );
    }

    #[test]
    fn query_stub_execute_register_report_and_aggregate_queried_execution_result_job_report_collection_summaries_indexed_loaded_aggregate_reloads_exactly()
     {
        let (directory, _) = sample_execution_ledger_history();
        let bundle_dir = directory.path().join("bundle");
        let report_path = directory.path().join("stage27-reload-report.json");
        let report_index_path = directory.path().join("stage27-reload-report-index.json");
        let summary_index_path = directory.path().join("stage27-reload-summary-index.json");
        let output_summary_path = directory.path().join("stage27-reload-summary.json");
        let aggregate_output_summary_path = directory
            .path()
            .join("stage27-reload-aggregate-summary.json");
        let ledger_query = LedgerSelectionQuery {
            status: Some(ExecutionResultStatus::StubbedSuccess),
            ..LedgerSelectionQuery::default()
        };
        let report_index_query = ExecutionResultJobReportIndexQuery::default();
        let summary_index_query = ExecutionResultJobReportCollectionSummaryIndexQuery::default();

        let indexed_loaded =
            query_stub_execute_register_report_and_aggregate_queried_execution_result_job_report_collection_summaries(
                &bundle_dir,
                &ledger_query,
                "handoff-stage27-reload",
                "run-request-stage27-reload",
                "job-spec-stage27-reload",
                ExecutionResultSelectionMode::FullHistory,
                &report_path,
                &report_index_path,
                &report_index_query,
                &summary_index_path,
                &output_summary_path,
                &summary_index_query,
                &aggregate_output_summary_path,
            )
            .expect("stage27 reload wrapper should succeed");
        let direct_reloaded =
            load_execution_result_job_report_collection_summary(&aggregate_output_summary_path)
                .expect("stage27 aggregate summary should reload directly");

        assert_eq!(indexed_loaded, direct_reloaded);
    }

    #[test]
    fn query_stub_execute_register_report_and_aggregate_queried_execution_result_job_report_collection_summaries_has_no_field_drift_vs_explicit_pipeline()
     {
        let (directory, _) = sample_execution_ledger_history();
        let bundle_dir = directory.path().join("bundle");
        let explicit_report_path = directory
            .path()
            .join("stage27-no-drift-explicit-report.json");
        let explicit_report_index_path = directory
            .path()
            .join("stage27-no-drift-explicit-report-index.json");
        let explicit_summary_index_path = directory
            .path()
            .join("stage27-no-drift-explicit-summary-index.json");
        let explicit_output_summary_path = directory
            .path()
            .join("stage27-no-drift-explicit-summary.json");
        let explicit_aggregate_output_summary_path = directory
            .path()
            .join("stage27-no-drift-explicit-aggregate-summary.json");
        let wrapper_report_path = directory
            .path()
            .join("stage27-no-drift-wrapper-report.json");
        let wrapper_report_index_path = directory
            .path()
            .join("stage27-no-drift-wrapper-report-index.json");
        let wrapper_summary_index_path = directory
            .path()
            .join("stage27-no-drift-wrapper-summary-index.json");
        let wrapper_output_summary_path = directory
            .path()
            .join("stage27-no-drift-wrapper-summary.json");
        let wrapper_aggregate_output_summary_path = directory
            .path()
            .join("stage27-no-drift-wrapper-aggregate-summary.json");
        let ledger_query = LedgerSelectionQuery::default();
        let report_index_query = ExecutionResultJobReportIndexQuery::default();
        let summary_index_query = ExecutionResultJobReportCollectionSummaryIndexQuery::default();

        query_stub_execute_register_report_and_index_load_summary(
            &bundle_dir,
            &ledger_query,
            "handoff-stage27-no-drift",
            "run-request-stage27-no-drift",
            "job-spec-stage27-no-drift",
            ExecutionResultSelectionMode::FullHistory,
            &explicit_report_path,
            &explicit_report_index_path,
            &report_index_query,
            &explicit_summary_index_path,
            &explicit_output_summary_path,
        )
        .expect("explicit stage27 no-drift stage25 wrapper should succeed");
        let explicit_indexed_loaded =
            load_query_summarize_persist_register_and_index_load_execution_result_job_report_collection_summary(
                &explicit_summary_index_path,
                &summary_index_query,
                &explicit_aggregate_output_summary_path,
            )
            .expect("explicit stage27 no-drift stage23 wrapper should succeed");

        let wrapper_indexed_loaded =
            query_stub_execute_register_report_and_aggregate_queried_execution_result_job_report_collection_summaries(
                &bundle_dir,
                &ledger_query,
                "handoff-stage27-no-drift",
                "run-request-stage27-no-drift",
                "job-spec-stage27-no-drift",
                ExecutionResultSelectionMode::FullHistory,
                &wrapper_report_path,
                &wrapper_report_index_path,
                &report_index_query,
                &wrapper_summary_index_path,
                &wrapper_output_summary_path,
                &summary_index_query,
                &wrapper_aggregate_output_summary_path,
            )
            .expect("stage27 no-drift wrapper should succeed");

        assert_eq!(wrapper_indexed_loaded, explicit_indexed_loaded);
        assert_eq!(
            wrapper_indexed_loaded.shared_export_name,
            explicit_indexed_loaded.shared_export_name
        );
        assert_eq!(
            wrapper_indexed_loaded.shared_selection_mode,
            explicit_indexed_loaded.shared_selection_mode
        );
        assert_eq!(
            wrapper_indexed_loaded.job_spec_ids,
            explicit_indexed_loaded.job_spec_ids
        );
        assert_eq!(
            wrapper_indexed_loaded.export_names,
            explicit_indexed_loaded.export_names
        );
        assert_eq!(
            wrapper_indexed_loaded.selection_modes,
            explicit_indexed_loaded.selection_modes
        );
        assert_eq!(
            wrapper_indexed_loaded.source_run_request_ids,
            explicit_indexed_loaded.source_run_request_ids
        );
        assert_eq!(
            wrapper_indexed_loaded.source_handoff_bundle_ids,
            explicit_indexed_loaded.source_handoff_bundle_ids
        );
    }

    fn sample_execution_result_job_report_index() -> ExecutionResultJobReportIndex {
        ExecutionResultJobReportIndex {
            index_version: EXECUTION_RESULT_JOB_REPORT_INDEX_VERSION,
            entries: vec![
                ExecutionResultJobReportIndexEntry {
                    ordinal: 0,
                    report_file_path: r"D:\reports\execution-result-job-report-a.json".to_string(),
                    job_spec_id: "job-spec-stub".to_string(),
                    source_run_request_id: "run-request-stub".to_string(),
                    source_handoff_bundle_id: "handoff-stub".to_string(),
                    export_name: "restore-stage-1".to_string(),
                    selection_mode: ExecutionResultSelectionMode::FullHistory,
                    expected_entry_count: 2,
                    source_provenance_hash: "provenance-hash".to_string(),
                },
                ExecutionResultJobReportIndexEntry {
                    ordinal: 1,
                    report_file_path: r"D:\reports\execution-result-job-report-b.json".to_string(),
                    job_spec_id: "job-spec-latest-only".to_string(),
                    source_run_request_id: "run-request-latest-only".to_string(),
                    source_handoff_bundle_id: "handoff-latest-only".to_string(),
                    export_name: "restore-stage-5-latest-only".to_string(),
                    selection_mode: ExecutionResultSelectionMode::LatestOnly,
                    expected_entry_count: 1,
                    source_provenance_hash: "latest-only-provenance-hash".to_string(),
                },
            ],
        }
    }

    fn sample_queryable_execution_result_job_report_index() -> ExecutionResultJobReportIndex {
        ExecutionResultJobReportIndex {
            index_version: EXECUTION_RESULT_JOB_REPORT_INDEX_VERSION,
            entries: vec![
                ExecutionResultJobReportIndexEntry {
                    ordinal: 0,
                    report_file_path: r"D:\reports\execution-result-job-report-a.json".to_string(),
                    job_spec_id: "job-spec-alpha".to_string(),
                    source_run_request_id: "run-request-shared".to_string(),
                    source_handoff_bundle_id: "handoff-shared".to_string(),
                    export_name: "restore-stage-shared".to_string(),
                    selection_mode: ExecutionResultSelectionMode::FullHistory,
                    expected_entry_count: 2,
                    source_provenance_hash: "provenance-alpha".to_string(),
                },
                ExecutionResultJobReportIndexEntry {
                    ordinal: 1,
                    report_file_path: r"D:\reports\execution-result-job-report-b.json".to_string(),
                    job_spec_id: "job-spec-beta".to_string(),
                    source_run_request_id: "run-request-shared".to_string(),
                    source_handoff_bundle_id: "handoff-shared".to_string(),
                    export_name: "restore-stage-shared".to_string(),
                    selection_mode: ExecutionResultSelectionMode::LatestOnly,
                    expected_entry_count: 1,
                    source_provenance_hash: "provenance-beta".to_string(),
                },
                ExecutionResultJobReportIndexEntry {
                    ordinal: 2,
                    report_file_path: r"D:\reports\execution-result-job-report-c.json".to_string(),
                    job_spec_id: "job-spec-gamma".to_string(),
                    source_run_request_id: "run-request-shared".to_string(),
                    source_handoff_bundle_id: "handoff-shared".to_string(),
                    export_name: "restore-stage-shared".to_string(),
                    selection_mode: ExecutionResultSelectionMode::FullHistory,
                    expected_entry_count: 3,
                    source_provenance_hash: "provenance-gamma".to_string(),
                },
            ],
        }
    }

    fn sample_queryable_execution_result_job_reports() -> Vec<ExecutionResultJobReport> {
        vec![
            ExecutionResultJobReport {
                job_spec_id: "job-spec-alpha".to_string(),
                source_run_request_id: "run-request-shared".to_string(),
                source_handoff_bundle_id: "handoff-shared".to_string(),
                export_name: "restore-stage-shared".to_string(),
                selection_mode: ExecutionResultSelectionMode::FullHistory,
                expected_entry_count: 2,
                source_provenance_hash: "provenance-alpha".to_string(),
                entries: vec![
                    ExecutionResultJobReportEntry {
                        ordinal: 0,
                        result_id: "result-alpha-a".to_string(),
                        request_id: "request-alpha-a".to_string(),
                        plan_id: "plan-alpha-a".to_string(),
                        stub_status: ExecutionResultJobReportStatus::Ready,
                    },
                    ExecutionResultJobReportEntry {
                        ordinal: 1,
                        result_id: "result-alpha-b".to_string(),
                        request_id: "request-alpha-b".to_string(),
                        plan_id: "plan-alpha-b".to_string(),
                        stub_status: ExecutionResultJobReportStatus::StubAccepted,
                    },
                ],
            },
            ExecutionResultJobReport {
                job_spec_id: "job-spec-beta".to_string(),
                source_run_request_id: "run-request-shared".to_string(),
                source_handoff_bundle_id: "handoff-shared".to_string(),
                export_name: "restore-stage-shared".to_string(),
                selection_mode: ExecutionResultSelectionMode::LatestOnly,
                expected_entry_count: 1,
                source_provenance_hash: "provenance-beta".to_string(),
                entries: vec![ExecutionResultJobReportEntry {
                    ordinal: 0,
                    result_id: "result-beta-a".to_string(),
                    request_id: "request-beta-a".to_string(),
                    plan_id: "plan-beta-a".to_string(),
                    stub_status: ExecutionResultJobReportStatus::StubAccepted,
                }],
            },
            ExecutionResultJobReport {
                job_spec_id: "job-spec-gamma".to_string(),
                source_run_request_id: "run-request-shared".to_string(),
                source_handoff_bundle_id: "handoff-shared".to_string(),
                export_name: "restore-stage-shared".to_string(),
                selection_mode: ExecutionResultSelectionMode::FullHistory,
                expected_entry_count: 3,
                source_provenance_hash: "provenance-gamma".to_string(),
                entries: vec![
                    ExecutionResultJobReportEntry {
                        ordinal: 0,
                        result_id: "result-gamma-a".to_string(),
                        request_id: "request-gamma-a".to_string(),
                        plan_id: "plan-gamma-a".to_string(),
                        stub_status: ExecutionResultJobReportStatus::Ready,
                    },
                    ExecutionResultJobReportEntry {
                        ordinal: 1,
                        result_id: "result-gamma-b".to_string(),
                        request_id: "request-gamma-b".to_string(),
                        plan_id: "plan-gamma-b".to_string(),
                        stub_status: ExecutionResultJobReportStatus::StubAccepted,
                    },
                    ExecutionResultJobReportEntry {
                        ordinal: 2,
                        result_id: "result-gamma-c".to_string(),
                        request_id: "request-gamma-c".to_string(),
                        plan_id: "plan-gamma-c".to_string(),
                        stub_status: ExecutionResultJobReportStatus::StubAccepted,
                    },
                ],
            },
        ]
    }

    fn sample_execution_result_job_report_collection_summary_latest_only()
    -> ExecutionResultJobReportCollectionSummary {
        summarize_execution_result_job_reports(&[sample_execution_result_job_report_latest_only()])
    }

    fn sample_execution_result_job_report_collection_summary_full_history_multi_report()
    -> ExecutionResultJobReportCollectionSummary {
        summarize_execution_result_job_reports(&sample_queryable_execution_result_job_reports())
    }

    #[test]
    fn summarize_execution_result_job_report_collection_summaries_single_input_preserves_semantics()
    {
        let summary =
            sample_execution_result_job_report_collection_summary_full_history_multi_report();

        let aggregate = summarize_execution_result_job_report_collection_summaries(
            std::slice::from_ref(&summary),
        );

        assert_eq!(aggregate, summary);
    }

    #[test]
    fn summarize_execution_result_job_report_collection_summaries_sum_counts_across_inputs() {
        let latest_only = sample_execution_result_job_report_collection_summary_latest_only();
        let full_history =
            sample_execution_result_job_report_collection_summary_full_history_multi_report();

        let aggregate = summarize_execution_result_job_report_collection_summaries(&[
            latest_only.clone(),
            full_history.clone(),
        ]);

        assert_eq!(
            aggregate.report_count,
            latest_only.report_count + full_history.report_count
        );
        assert_eq!(
            aggregate.total_entry_count,
            latest_only.total_entry_count + full_history.total_entry_count
        );
    }

    #[test]
    fn summarize_execution_result_job_report_collection_summaries_preserves_unique_first_seen_order()
     {
        let aggregate = summarize_execution_result_job_report_collection_summaries(&[
            ExecutionResultJobReportCollectionSummary {
                report_count: 2,
                total_entry_count: 5,
                job_spec_ids: vec!["job-a".to_string(), "job-b".to_string()],
                export_names: vec!["export-a".to_string(), "export-b".to_string()],
                selection_modes: vec![
                    ExecutionResultSelectionMode::LatestOnly,
                    ExecutionResultSelectionMode::FullHistory,
                ],
                source_run_request_ids: vec!["run-a".to_string(), "run-b".to_string()],
                source_handoff_bundle_ids: vec!["handoff-a".to_string(), "handoff-b".to_string()],
                shared_export_name: None,
                shared_selection_mode: None,
            },
            ExecutionResultJobReportCollectionSummary {
                report_count: 3,
                total_entry_count: 7,
                job_spec_ids: vec!["job-b".to_string(), "job-c".to_string()],
                export_names: vec!["export-b".to_string(), "export-c".to_string()],
                selection_modes: vec![
                    ExecutionResultSelectionMode::FullHistory,
                    ExecutionResultSelectionMode::LatestOnly,
                ],
                source_run_request_ids: vec!["run-b".to_string(), "run-c".to_string()],
                source_handoff_bundle_ids: vec!["handoff-b".to_string(), "handoff-c".to_string()],
                shared_export_name: None,
                shared_selection_mode: None,
            },
        ]);

        assert_eq!(
            aggregate.job_spec_ids,
            vec![
                "job-a".to_string(),
                "job-b".to_string(),
                "job-c".to_string()
            ]
        );
        assert_eq!(
            aggregate.export_names,
            vec![
                "export-a".to_string(),
                "export-b".to_string(),
                "export-c".to_string()
            ]
        );
        assert_eq!(
            aggregate.selection_modes,
            vec![
                ExecutionResultSelectionMode::LatestOnly,
                ExecutionResultSelectionMode::FullHistory,
            ]
        );
        assert_eq!(
            aggregate.source_run_request_ids,
            vec![
                "run-a".to_string(),
                "run-b".to_string(),
                "run-c".to_string()
            ]
        );
        assert_eq!(
            aggregate.source_handoff_bundle_ids,
            vec![
                "handoff-a".to_string(),
                "handoff-b".to_string(),
                "handoff-c".to_string()
            ]
        );
    }

    #[test]
    fn summarize_execution_result_job_report_collection_summaries_matches_wrapper_aggregate_semantics_on_shared_fixture()
     {
        let latest_only = sample_execution_result_job_report_collection_summary_latest_only();
        let full_history =
            sample_execution_result_job_report_collection_summary_full_history_multi_report();
        let expected = ExecutionResultJobReportCollectionSummary {
            report_count: latest_only.report_count + full_history.report_count,
            total_entry_count: latest_only.total_entry_count + full_history.total_entry_count,
            shared_export_name: None,
            shared_selection_mode: None,
            job_spec_ids: vec![
                "job-spec-latest-only".to_string(),
                "job-spec-alpha".to_string(),
                "job-spec-beta".to_string(),
                "job-spec-gamma".to_string(),
            ],
            export_names: vec![
                "restore-stage-5-latest-only".to_string(),
                "restore-stage-shared".to_string(),
            ],
            selection_modes: vec![
                ExecutionResultSelectionMode::LatestOnly,
                ExecutionResultSelectionMode::FullHistory,
            ],
            source_run_request_ids: vec![
                "run-request-latest-only".to_string(),
                "run-request-shared".to_string(),
            ],
            source_handoff_bundle_ids: vec![
                "handoff-latest-only".to_string(),
                "handoff-shared".to_string(),
            ],
        };

        let aggregate = summarize_execution_result_job_report_collection_summaries(&[
            latest_only,
            full_history,
        ]);

        assert_eq!(aggregate, expected);
    }

    fn sample_execution_result_job_report_collection_summary_index()
    -> ExecutionResultJobReportCollectionSummaryIndex {
        ExecutionResultJobReportCollectionSummaryIndex {
            index_version: EXECUTION_RESULT_JOB_REPORT_COLLECTION_SUMMARY_INDEX_VERSION,
            entries: vec![
                ExecutionResultJobReportCollectionSummaryIndexEntry {
                    ordinal: 0,
                    summary_file_path:
                        r"D:\reports\execution-result-job-report-collection-summary-a.json"
                            .to_string(),
                    report_count: 1,
                    total_entry_count: 1,
                    job_spec_ids: vec!["job-spec-latest-only".to_string()],
                    export_names: vec!["restore-stage-5-latest-only".to_string()],
                    selection_modes: vec![ExecutionResultSelectionMode::LatestOnly],
                    source_run_request_ids: vec!["run-request-latest-only".to_string()],
                    source_handoff_bundle_ids: vec!["handoff-latest-only".to_string()],
                },
                ExecutionResultJobReportCollectionSummaryIndexEntry {
                    ordinal: 1,
                    summary_file_path:
                        r"D:\reports\execution-result-job-report-collection-summary-b.json"
                            .to_string(),
                    report_count: 3,
                    total_entry_count: 7,
                    job_spec_ids: vec![
                        "job-spec-alpha".to_string(),
                        "job-spec-beta".to_string(),
                        "job-spec-gamma".to_string(),
                    ],
                    export_names: vec![
                        "restore-stage-shared".to_string(),
                        "restore-stage-unique".to_string(),
                    ],
                    selection_modes: vec![
                        ExecutionResultSelectionMode::FullHistory,
                        ExecutionResultSelectionMode::LatestOnly,
                    ],
                    source_run_request_ids: vec![
                        "run-request-shared".to_string(),
                        "run-request-unique".to_string(),
                    ],
                    source_handoff_bundle_ids: vec![
                        "handoff-shared".to_string(),
                        "handoff-unique".to_string(),
                    ],
                },
            ],
        }
    }

    fn persist_sample_execution_result_job_report_collection_summaries_with_index() -> (
        TempDir,
        PathBuf,
        PathBuf,
        ExecutionResultJobReportCollectionSummary,
        PathBuf,
        ExecutionResultJobReportCollectionSummary,
    ) {
        let directory = tempdir().expect("tempdir should be created");
        let index_path = directory
            .path()
            .join("execution-result-job-report-collection-summary-index.json");
        let latest_only_summary_path = directory
            .path()
            .join("execution-result-job-report-collection-summary-latest-only.json");
        let full_history_summary_path = directory
            .path()
            .join("execution-result-job-report-collection-summary-full-history.json");
        let latest_only_summary =
            sample_execution_result_job_report_collection_summary_latest_only();
        let full_history_summary =
            sample_execution_result_job_report_collection_summary_full_history_multi_report();

        persist_execution_result_job_report_collection_summary(
            &latest_only_summary_path,
            &latest_only_summary,
        )
        .expect("latest-only summary should persist");
        register_execution_result_job_report_collection_summary_in_index(
            &index_path,
            &latest_only_summary_path,
            &latest_only_summary,
        )
        .expect("latest-only summary should register");

        persist_execution_result_job_report_collection_summary(
            &full_history_summary_path,
            &full_history_summary,
        )
        .expect("full-history summary should persist");
        register_execution_result_job_report_collection_summary_in_index(
            &index_path,
            &full_history_summary_path,
            &full_history_summary,
        )
        .expect("full-history summary should register");

        (
            directory,
            index_path,
            latest_only_summary_path,
            latest_only_summary,
            full_history_summary_path,
            full_history_summary,
        )
    }

    fn persist_sample_execution_result_job_reports_with_index()
    -> (TempDir, PathBuf, Vec<ExecutionResultJobReport>) {
        let directory = tempdir().expect("tempdir should be created");
        let index_path = directory
            .path()
            .join("execution-result-job-report-query-index.json");
        let reports = sample_queryable_execution_result_job_reports();

        for report in &reports {
            let report_path = directory
                .path()
                .join(format!("{}.json", report.job_spec_id));
            persist_execution_result_job_report(&report_path, report)
                .expect("sample queryable report should persist");
            register_execution_result_job_report_in_index(&index_path, &report_path, report)
                .expect("sample queryable report should register");
        }

        (directory, index_path, reports)
    }

    fn snapshot_directory_file_bytes(root: &Path) -> std::collections::BTreeMap<PathBuf, Vec<u8>> {
        fn collect(
            root: &Path,
            current: &Path,
            snapshot: &mut std::collections::BTreeMap<PathBuf, Vec<u8>>,
        ) {
            let mut entries = std::fs::read_dir(current)
                .expect("directory should be readable")
                .map(|entry| entry.expect("directory entry should be readable"))
                .collect::<Vec<_>>();
            entries.sort_by_key(|entry| entry.path());

            for entry in entries {
                let path = entry.path();
                if path.is_dir() {
                    collect(root, &path, snapshot);
                } else {
                    let relative_path = path
                        .strip_prefix(root)
                        .expect("snapshotted path should stay under root")
                        .to_path_buf();
                    let bytes = std::fs::read(&path).expect("snapshotted file should be readable");
                    snapshot.insert(relative_path, bytes);
                }
            }
        }

        let mut snapshot = std::collections::BTreeMap::new();
        collect(root, root, &mut snapshot);
        snapshot
    }

    fn changed_paths_between_snapshots(
        before: &std::collections::BTreeMap<PathBuf, Vec<u8>>,
        after: &std::collections::BTreeMap<PathBuf, Vec<u8>>,
    ) -> std::collections::BTreeSet<PathBuf> {
        let paths = before
            .keys()
            .chain(after.keys())
            .cloned()
            .collect::<std::collections::BTreeSet<_>>();

        paths
            .into_iter()
            .filter(|path| before.get(path) != after.get(path))
            .collect()
    }

    fn relative_paths(root: &Path, paths: &[&Path]) -> std::collections::BTreeSet<PathBuf> {
        paths
            .iter()
            .map(|path| {
                path.strip_prefix(root)
                    .expect("expected path should stay under snapshot root")
                    .to_path_buf()
            })
            .collect()
    }

    fn assert_only_expected_paths_changed(
        root: &Path,
        before: &std::collections::BTreeMap<PathBuf, Vec<u8>>,
        after: &std::collections::BTreeMap<PathBuf, Vec<u8>>,
        expected_changed_paths: &[&Path],
    ) {
        let changed_paths = changed_paths_between_snapshots(before, after);
        let expected_paths = relative_paths(root, expected_changed_paths);

        assert_eq!(changed_paths, expected_paths);
    }

    fn assert_directory_snapshot_unchanged(
        before: &std::collections::BTreeMap<PathBuf, Vec<u8>>,
        after: &std::collections::BTreeMap<PathBuf, Vec<u8>>,
    ) {
        let changed_paths = changed_paths_between_snapshots(before, after);

        assert!(
            changed_paths.is_empty(),
            "unexpected file mutations: {changed_paths:?}"
        );
    }

    // Canonical contract tests lock the documented stage39 execution-result surface only.

    #[test]
    fn canonical_execution_result_read_only_helpers_do_not_mutate_persisted_artifacts() {
        let (directory, history) = sample_execution_ledger_history();
        let root = directory.path();
        let bundle_dir = root.join("bundle");
        let report_path = root.join("stage44-read-only-report.json");
        let report_index_path = root.join("stage44-read-only-report-index.json");
        let summary_path = root.join("stage44-read-only-summary.json");
        let summary_index_path = root.join("stage44-read-only-summary-index.json");
        let report = sample_execution_result_job_report_latest_only();
        let summary = sample_execution_result_job_report_collection_summary_latest_only();

        persist_execution_result_job_report(&report_path, &report)
            .expect("read-only test report should persist");
        register_execution_result_job_report_in_index(&report_index_path, &report_path, &report)
            .expect("read-only test report should register");
        persist_execution_result_job_report_collection_summary(&summary_path, &summary)
            .expect("read-only test summary should persist");
        register_execution_result_job_report_collection_summary_in_index(
            &summary_index_path,
            &summary_path,
            &summary,
        )
        .expect("read-only test summary should register");

        let before = snapshot_directory_file_bytes(root);
        let report_index = load_execution_result_job_report_index(&report_index_path)
            .expect("report index should load");
        let summary_index =
            load_execution_result_job_report_collection_summary_index(&summary_index_path)
                .expect("summary index should load");

        load_execution_result_job_report(&report_path).expect("report load should stay read-only");
        query_execution_result_job_report_index(
            &report_index,
            &ExecutionResultJobReportIndexQuery::default(),
        )
        .expect("report index query should stay read-only");
        load_and_query_execution_result_job_reports(
            &report_index_path,
            &ExecutionResultJobReportIndexQuery::default(),
        )
        .expect("report query/load should stay read-only");
        load_execution_result_job_report_collection_summary(&summary_path)
            .expect("summary load should stay read-only");
        query_execution_result_job_report_collection_summary_index(
            &summary_index,
            &ExecutionResultJobReportCollectionSummaryIndexQuery::default(),
        )
        .expect("summary index query should stay read-only");
        load_and_query_execution_result_job_report_collection_summaries(
            &summary_index_path,
            &ExecutionResultJobReportCollectionSummaryIndexQuery::default(),
        )
        .expect("summary query/load should stay read-only");
        load_query_and_aggregate_execution_result_job_report_collection_summaries(
            &summary_index_path,
            &ExecutionResultJobReportCollectionSummaryIndexQuery::default(),
        )
        .expect("summary aggregate should stay read-only");
        inspect_execution_ledger_history(&bundle_dir)
            .expect("ledger inspection should stay read-only");
        query_execution_ledger_history(&history, &LedgerSelectionQuery::default());

        let after = snapshot_directory_file_bytes(root);
        assert_directory_snapshot_unchanged(&before, &after);
    }

    #[test]
    fn canonical_execution_result_write_helpers_mutate_only_explicit_targets() {
        let directory = tempdir().expect("tempdir should be created");
        let root = directory.path();
        let report = sample_execution_result_job_report();
        let summary =
            sample_execution_result_job_report_collection_summary_full_history_multi_report();

        let report_path = root.join("stage44-write-report.json");
        let report_index_path = root.join("stage44-write-report-index.json");
        let summary_path = root.join("stage44-write-summary.json");
        let summary_index_path = root.join("stage44-write-summary-index.json");
        let combined_summary_path = root.join("stage44-write-combined-summary.json");
        let combined_summary_index_path = root.join("stage44-write-combined-summary-index.json");
        let untouched_sibling_path = root.join("stage44-write-untouched.txt");
        std::fs::write(&untouched_sibling_path, b"untouched sibling sentinel")
            .expect("untouched sibling sentinel should persist");

        let before_report_persist = snapshot_directory_file_bytes(root);
        persist_execution_result_job_report(&report_path, &report)
            .expect("report persist should succeed");
        let after_report_persist = snapshot_directory_file_bytes(root);
        assert_only_expected_paths_changed(
            root,
            &before_report_persist,
            &after_report_persist,
            &[report_path.as_path()],
        );

        let before_report_index_persist = after_report_persist.clone();
        persist_execution_result_job_report_index(
            &report_index_path,
            &empty_execution_result_job_report_index(),
        )
        .expect("report index persist should succeed");
        let after_report_index_persist = snapshot_directory_file_bytes(root);
        assert_only_expected_paths_changed(
            root,
            &before_report_index_persist,
            &after_report_index_persist,
            &[report_index_path.as_path()],
        );

        let before_report_register = after_report_index_persist.clone();
        register_execution_result_job_report_in_index(&report_index_path, &report_path, &report)
            .expect("report register should succeed");
        let after_report_register = snapshot_directory_file_bytes(root);
        assert_only_expected_paths_changed(
            root,
            &before_report_register,
            &after_report_register,
            &[report_index_path.as_path()],
        );

        let before_summary_persist = after_report_register.clone();
        persist_execution_result_job_report_collection_summary(&summary_path, &summary)
            .expect("summary persist should succeed");
        let after_summary_persist = snapshot_directory_file_bytes(root);
        assert_only_expected_paths_changed(
            root,
            &before_summary_persist,
            &after_summary_persist,
            &[summary_path.as_path()],
        );

        let before_summary_index_persist = after_summary_persist.clone();
        persist_execution_result_job_report_collection_summary_index(
            &summary_index_path,
            &empty_execution_result_job_report_collection_summary_index(),
        )
        .expect("summary index persist should succeed");
        let after_summary_index_persist = snapshot_directory_file_bytes(root);
        assert_only_expected_paths_changed(
            root,
            &before_summary_index_persist,
            &after_summary_index_persist,
            &[summary_index_path.as_path()],
        );

        let before_summary_register = after_summary_index_persist.clone();
        register_execution_result_job_report_collection_summary_in_index(
            &summary_index_path,
            &summary_path,
            &summary,
        )
        .expect("summary register should succeed");
        let after_summary_register = snapshot_directory_file_bytes(root);
        assert_only_expected_paths_changed(
            root,
            &before_summary_register,
            &after_summary_register,
            &[summary_index_path.as_path()],
        );

        let before_combined_helper = after_summary_register.clone();
        persist_register_and_index_load_execution_result_job_report_collection_summary(
            &summary,
            &combined_summary_path,
            &combined_summary_index_path,
        )
        .expect("combined summary helper should succeed");
        let after_combined_helper = snapshot_directory_file_bytes(root);
        assert_only_expected_paths_changed(
            root,
            &before_combined_helper,
            &after_combined_helper,
            &[
                combined_summary_path.as_path(),
                combined_summary_index_path.as_path(),
            ],
        );
    }

    #[test]
    fn canonical_publication_bridges_mutate_only_documented_artifacts() {
        {
            let (directory, _) = sample_execution_ledger_history();
            let root = directory.path();
            let bundle_dir = root.join("bundle");
            let report_path = root.join("stage44-bridge-a-report.json");
            let report_index_path = root.join("stage44-bridge-a-report-index.json");
            let untouched_sibling_path = root.join("stage44-bridge-a-untouched.txt");
            std::fs::write(&untouched_sibling_path, b"bridge a sentinel")
                .expect("bridge a sentinel should persist");

            let before = snapshot_directory_file_bytes(root);
            query_stub_execute_persist_load_and_register_execution_result_job_report(
                &bundle_dir,
                &LedgerSelectionQuery::default(),
                "handoff-stage44-bridge-a",
                "run-request-stage44-bridge-a",
                "job-spec-stage44-bridge-a",
                ExecutionResultSelectionMode::FullHistory,
                &report_path,
                &report_index_path,
            )
            .expect("bridge a should succeed");
            let after = snapshot_directory_file_bytes(root);
            assert_only_expected_paths_changed(
                root,
                &before,
                &after,
                &[report_path.as_path(), report_index_path.as_path()],
            );
        }

        {
            let (directory, _) = sample_execution_ledger_history();
            let root = directory.path();
            let bundle_dir = root.join("bundle");
            let report_path = root.join("stage44-bridge-b-report.json");
            let report_index_path = root.join("stage44-bridge-b-report-index.json");
            let untouched_sibling_path = root.join("stage44-bridge-b-untouched.txt");
            std::fs::write(&untouched_sibling_path, b"bridge b sentinel")
                .expect("bridge b sentinel should persist");

            let before = snapshot_directory_file_bytes(root);
            query_stub_execute_persist_load_register_query_and_load_execution_result_job_reports(
                &bundle_dir,
                &LedgerSelectionQuery::default(),
                "handoff-stage44-bridge-b",
                "run-request-stage44-bridge-b",
                "job-spec-stage44-bridge-b",
                ExecutionResultSelectionMode::FullHistory,
                &report_path,
                &report_index_path,
                &ExecutionResultJobReportIndexQuery::default(),
            )
            .expect("bridge b should succeed");
            let after = snapshot_directory_file_bytes(root);
            assert_only_expected_paths_changed(
                root,
                &before,
                &after,
                &[report_path.as_path(), report_index_path.as_path()],
            );
        }

        {
            let (directory, _) = sample_execution_ledger_history();
            let root = directory.path();
            let bundle_dir = root.join("bundle");
            let report_path = root.join("stage44-bridge-c-report.json");
            let report_index_path = root.join("stage44-bridge-c-report-index.json");
            let summary_path = root.join("stage44-bridge-c-summary.json");
            let summary_index_path = root.join("stage44-bridge-c-summary-index.json");
            let untouched_sibling_path = root.join("stage44-bridge-c-untouched.txt");
            std::fs::write(&untouched_sibling_path, b"bridge c sentinel")
                .expect("bridge c sentinel should persist");

            let before = snapshot_directory_file_bytes(root);
            query_stub_execute_register_report_and_index_load_summary(
                &bundle_dir,
                &LedgerSelectionQuery::default(),
                "handoff-stage44-bridge-c",
                "run-request-stage44-bridge-c",
                "job-spec-stage44-bridge-c",
                ExecutionResultSelectionMode::FullHistory,
                &report_path,
                &report_index_path,
                &ExecutionResultJobReportIndexQuery::default(),
                &summary_index_path,
                &summary_path,
            )
            .expect("bridge c should succeed");
            let after = snapshot_directory_file_bytes(root);
            assert_only_expected_paths_changed(
                root,
                &before,
                &after,
                &[
                    report_path.as_path(),
                    report_index_path.as_path(),
                    summary_path.as_path(),
                    summary_index_path.as_path(),
                ],
            );
        }
    }

    #[test]
    fn canonical_end_to_end_side_effect_boundary_stays_on_explicit_output_paths() {
        let (directory, _) = sample_execution_ledger_history();
        let root = directory.path();
        let bundle_dir = root.join("bundle");
        let report_path = root.join("stage44-end-to-end-report.json");
        let report_index_path = root.join("stage44-end-to-end-report-index.json");
        let summary_path = root.join("stage44-end-to-end-summary.json");
        let summary_index_path = root.join("stage44-end-to-end-summary-index.json");
        let report_query = ExecutionResultJobReportIndexQuery::default();
        let summary_query = ExecutionResultJobReportCollectionSummaryIndexQuery::default();
        let initial_snapshot = snapshot_directory_file_bytes(root);

        let history = inspect_execution_ledger_history(&bundle_dir)
            .expect("end-to-end history load should stay read-only");
        let queried_entries =
            query_execution_ledger_history(&history, &LedgerSelectionQuery::default());
        let handoff_bundle = build_execution_result_handoff_bundle(
            &queried_entries,
            "handoff-stage44-end-to-end",
            ExecutionResultSelectionMode::FullHistory,
        )
        .expect("handoff should build");
        let run_request = build_run_request_from_handoff_bundle(
            &handoff_bundle,
            "run-request-stage44-end-to-end",
        )
        .expect("run request should build");
        let job_spec = build_job_spec_from_run_request(&run_request, "job-spec-stage44-end-to-end")
            .expect("job spec should build");
        let executor = StubExecutionResultJobExecutor;
        let report = executor
            .execute(&job_spec)
            .expect("stub executor should produce report");

        let after_report_build = snapshot_directory_file_bytes(root);
        assert_directory_snapshot_unchanged(&initial_snapshot, &after_report_build);

        persist_execution_result_job_report(&report_path, &report)
            .expect("end-to-end report should persist");
        let after_report_persist = snapshot_directory_file_bytes(root);
        assert_only_expected_paths_changed(
            root,
            &after_report_build,
            &after_report_persist,
            &[report_path.as_path()],
        );

        register_execution_result_job_report_in_index(&report_index_path, &report_path, &report)
            .expect("end-to-end report should register");
        let after_report_register = snapshot_directory_file_bytes(root);
        assert_only_expected_paths_changed(
            root,
            &after_report_persist,
            &after_report_register,
            &[report_index_path.as_path()],
        );

        load_execution_result_job_report(&report_path)
            .expect("report reload should stay read-only");
        let report_index = load_execution_result_job_report_index(&report_index_path)
            .expect("report index reload should stay read-only");
        query_execution_result_job_report_index(&report_index, &report_query)
            .expect("report index query should stay read-only");
        let loaded_reports =
            load_and_query_execution_result_job_reports(&report_index_path, &report_query)
                .expect("report query/load should stay read-only");
        let after_report_reads = snapshot_directory_file_bytes(root);
        assert_directory_snapshot_unchanged(&after_report_register, &after_report_reads);

        let summary = summarize_execution_result_job_reports(&loaded_reports);
        persist_execution_result_job_report_collection_summary(&summary_path, &summary)
            .expect("end-to-end summary should persist");
        let after_summary_persist = snapshot_directory_file_bytes(root);
        assert_only_expected_paths_changed(
            root,
            &after_report_reads,
            &after_summary_persist,
            &[summary_path.as_path()],
        );

        register_execution_result_job_report_collection_summary_in_index(
            &summary_index_path,
            &summary_path,
            &summary,
        )
        .expect("end-to-end summary should register");
        let after_summary_register = snapshot_directory_file_bytes(root);
        assert_only_expected_paths_changed(
            root,
            &after_summary_persist,
            &after_summary_register,
            &[summary_index_path.as_path()],
        );

        load_execution_result_job_report_collection_summary(&summary_path)
            .expect("summary reload should stay read-only");
        let summary_index =
            load_execution_result_job_report_collection_summary_index(&summary_index_path)
                .expect("summary index reload should stay read-only");
        query_execution_result_job_report_collection_summary_index(&summary_index, &summary_query)
            .expect("summary index query should stay read-only");
        load_and_query_execution_result_job_report_collection_summaries(
            &summary_index_path,
            &summary_query,
        )
        .expect("summary query/load should stay read-only");
        load_query_and_aggregate_execution_result_job_report_collection_summaries(
            &summary_index_path,
            &summary_query,
        )
        .expect("summary aggregate should stay read-only");
        let final_snapshot = snapshot_directory_file_bytes(root);
        assert_directory_snapshot_unchanged(&after_summary_register, &final_snapshot);
    }

    #[test]
    fn canonical_contract_builder_failure_paths_reject_handoff_run_request_and_job_spec_drift() {
        let (_directory, history) = sample_execution_ledger_history();
        let handoff_bundle = build_handoff_bundle_from_history(
            &history,
            "handoff-canonical-failure",
            ExecutionResultSelectionMode::FullHistory,
        )
        .expect("canonical handoff bundle should build");

        let mut handoff_entry_count_drift = handoff_bundle.clone();
        handoff_entry_count_drift.entry_count += 1;
        let handoff_entry_count_error = build_run_request_from_handoff_bundle(
            &handoff_entry_count_drift,
            "run-request-canonical-handoff-entry-count-drift",
        )
        .expect_err("handoff entry count drift should be rejected before run request build");
        assert!(
            handoff_entry_count_error
                .to_string()
                .contains("handoff bundle entry count drift"),
            "unexpected error: {handoff_entry_count_error}"
        );

        let mut handoff_provenance_drift = handoff_bundle.clone();
        handoff_provenance_drift.provenance_hash = "tampered-handoff-provenance".to_string();
        let handoff_provenance_error = build_run_request_from_handoff_bundle(
            &handoff_provenance_drift,
            "run-request-canonical-handoff-provenance-drift",
        )
        .expect_err("handoff provenance drift should be rejected before run request build");
        assert!(
            handoff_provenance_error
                .to_string()
                .contains("handoff bundle provenance drift"),
            "unexpected error: {handoff_provenance_error}"
        );

        let run_request =
            build_run_request_from_handoff_bundle(&handoff_bundle, "run-request-canonical-failure")
                .expect("canonical run request should build");

        let direct_entry_count_error = build_execution_result_job_spec(
            &run_request.entries,
            "job-spec-canonical-entry-count-drift",
            run_request.run_request_id.clone(),
            run_request.source_handoff_bundle_id.clone(),
            run_request.export_name.clone(),
            run_request.selection_mode,
            run_request.expected_entry_count + 1,
            run_request.source_provenance_hash.clone(),
        )
        .expect_err("job spec entry count drift should be rejected");
        assert!(
            direct_entry_count_error
                .to_string()
                .contains("job spec entry count drift"),
            "unexpected error: {direct_entry_count_error}"
        );

        let direct_provenance_error = build_execution_result_job_spec(
            &run_request.entries,
            "job-spec-canonical-provenance-drift",
            run_request.run_request_id.clone(),
            run_request.source_handoff_bundle_id.clone(),
            run_request.export_name.clone(),
            run_request.selection_mode,
            run_request.expected_entry_count,
            "tampered-run-request-provenance".to_string(),
        )
        .expect_err("job spec provenance drift should be rejected");
        assert!(
            direct_provenance_error
                .to_string()
                .contains("job spec provenance drift"),
            "unexpected error: {direct_provenance_error}"
        );

        let mut run_request_entry_count_drift = run_request.clone();
        run_request_entry_count_drift.expected_entry_count += 1;
        let run_request_entry_count_error = build_job_spec_from_run_request(
            &run_request_entry_count_drift,
            "job-spec-canonical-run-request-entry-count-drift",
        )
        .expect_err("run request entry count drift should be rejected before job spec build");
        assert!(
            run_request_entry_count_error
                .to_string()
                .contains("run request entry count drift"),
            "unexpected error: {run_request_entry_count_error}"
        );

        let mut run_request_provenance_drift = run_request;
        run_request_provenance_drift.source_provenance_hash =
            "tampered-run-request-provenance".to_string();
        let run_request_provenance_error = build_job_spec_from_run_request(
            &run_request_provenance_drift,
            "job-spec-canonical-run-request-provenance-drift",
        )
        .expect_err("run request provenance drift should be rejected before job spec build");
        assert!(
            run_request_provenance_error
                .to_string()
                .contains("run request provenance drift"),
            "unexpected error: {run_request_provenance_error}"
        );
    }

    #[test]
    fn canonical_contract_report_failure_paths_reject_invalid_content_duplicate_registrations_and_missing_entries()
     {
        let directory = tempdir().expect("tempdir should be created");
        let invalid_report_path = directory.path().join("canonical-invalid-report.json");
        let mut invalid_report = sample_execution_result_job_report();
        invalid_report.entries[1].ordinal = 3;
        fs::write(
            &invalid_report_path,
            serde_json::to_vec_pretty(&invalid_report)
                .expect("invalid canonical report should serialize"),
        )
        .expect("invalid canonical report should be written");

        let invalid_report_error = load_execution_result_job_report(&invalid_report_path)
            .expect_err("invalid canonical persisted report should be rejected");
        assert!(
            invalid_report_error.to_string().contains("job report"),
            "unexpected error: {invalid_report_error}"
        );

        let index_path = directory.path().join("canonical-report-index.json");
        let report_a_path = directory.path().join("canonical-report-a.json");
        let report_b_path = directory.path().join("canonical-report-b.json");
        let report_a = sample_execution_result_job_report();
        let mut report_b = sample_execution_result_job_report_latest_only();

        register_execution_result_job_report_in_index(&index_path, &report_a_path, &report_a)
            .expect("first canonical report should register");

        let duplicate_path_error =
            register_execution_result_job_report_in_index(&index_path, &report_a_path, &report_b)
                .expect_err("duplicate canonical report path should be rejected");
        assert!(
            duplicate_path_error
                .to_string()
                .contains("duplicate execution result job report path"),
            "unexpected error: {duplicate_path_error}"
        );

        report_b.job_spec_id = report_a.job_spec_id.clone();
        let duplicate_job_spec_error =
            register_execution_result_job_report_in_index(&index_path, &report_b_path, &report_b)
                .expect_err("duplicate canonical job spec id should be rejected");
        assert!(
            duplicate_job_spec_error
                .to_string()
                .contains("duplicate execution result job spec id"),
            "unexpected error: {duplicate_job_spec_error}"
        );

        let missing_entry_error =
            load_indexed_execution_result_job_report(&index_path, "missing-job-spec")
                .expect_err("missing canonical indexed report entry should be rejected");
        assert!(
            missing_entry_error
                .to_string()
                .contains("index entry not found for job spec id missing-job-spec"),
            "unexpected error: {missing_entry_error}"
        );
    }

    #[test]
    fn canonical_contract_report_failure_paths_keep_latest_only_query_edges_deterministic() {
        let (_directory, index_path, reports) =
            persist_sample_execution_result_job_reports_with_index();

        let no_match_query = ExecutionResultJobReportIndexQuery {
            export_name: Some("missing-export".to_string()),
            latest_only: true,
            ..ExecutionResultJobReportIndexQuery::default()
        };
        let no_match_loaded =
            load_and_query_execution_result_job_reports(&index_path, &no_match_query)
                .expect("latest-only canonical no-match report query should succeed");
        assert!(no_match_loaded.is_empty());

        let one_match_query = ExecutionResultJobReportIndexQuery {
            job_spec_id: Some(reports[1].job_spec_id.clone()),
            latest_only: true,
            ..ExecutionResultJobReportIndexQuery::default()
        };
        let one_match_loaded =
            load_and_query_execution_result_job_reports(&index_path, &one_match_query)
                .expect("latest-only canonical single-match report query should succeed");
        assert_eq!(one_match_loaded, vec![reports[1].clone()]);
    }

    #[test]
    fn canonical_contract_summary_failure_paths_reject_invalid_content_duplicate_paths_and_missing_entries()
     {
        let directory = tempdir().expect("tempdir should be created");
        let invalid_summary_path = directory.path().join("canonical-invalid-summary.json");
        let mut invalid_summary =
            sample_execution_result_job_report_collection_summary_latest_only();
        invalid_summary.job_spec_ids.clear();
        fs::write(
            &invalid_summary_path,
            serde_json::to_vec_pretty(&invalid_summary)
                .expect("invalid canonical summary should serialize"),
        )
        .expect("invalid canonical summary should be written");

        let invalid_summary_error =
            load_execution_result_job_report_collection_summary(&invalid_summary_path)
                .expect_err("invalid canonical persisted summary should be rejected");
        assert!(
            invalid_summary_error
                .to_string()
                .contains("job report collection summary"),
            "unexpected error: {invalid_summary_error}"
        );

        let index_path = directory.path().join("canonical-summary-index.json");
        let summary_path = directory.path().join("canonical-summary.json");
        let summary_a = sample_execution_result_job_report_collection_summary_latest_only();
        let summary_b =
            sample_execution_result_job_report_collection_summary_full_history_multi_report();

        register_execution_result_job_report_collection_summary_in_index(
            &index_path,
            &summary_path,
            &summary_a,
        )
        .expect("first canonical summary should register");

        let duplicate_path_error =
            register_execution_result_job_report_collection_summary_in_index(
                &index_path,
                &summary_path,
                &summary_b,
            )
            .expect_err("duplicate canonical summary path should be rejected");
        assert!(
            duplicate_path_error
                .to_string()
                .contains("duplicate execution result job report collection summary path"),
            "unexpected error: {duplicate_path_error}"
        );

        let missing_entry_error = load_indexed_execution_result_job_report_collection_summary(
            &index_path,
            "missing-summary.json",
        )
        .expect_err("missing canonical indexed summary entry should be rejected");
        assert!(
            missing_entry_error
                .to_string()
                .contains("index entry not found for summary file path missing-summary.json"),
            "unexpected error: {missing_entry_error}"
        );
    }

    #[test]
    fn canonical_contract_summary_failure_paths_keep_latest_only_query_edges_deterministic() {
        let (
            _directory,
            index_path,
            latest_only_summary_path,
            latest_only_summary,
            _full_history_summary_path,
            _full_history_summary,
        ) = persist_sample_execution_result_job_report_collection_summaries_with_index();

        let no_match_query = ExecutionResultJobReportCollectionSummaryIndexQuery {
            export_names: vec!["missing-export".to_string()],
            latest_only: true,
            ..ExecutionResultJobReportCollectionSummaryIndexQuery::default()
        };
        let no_match_loaded = load_and_query_execution_result_job_report_collection_summaries(
            &index_path,
            &no_match_query,
        )
        .expect("latest-only canonical no-match summary query should succeed");
        assert!(no_match_loaded.is_empty());

        let one_match_query = ExecutionResultJobReportCollectionSummaryIndexQuery {
            summary_file_path: Some(
                path_to_owned_string(&latest_only_summary_path)
                    .expect("canonical latest-only summary path should serialize"),
            ),
            latest_only: true,
            ..ExecutionResultJobReportCollectionSummaryIndexQuery::default()
        };
        let one_match_loaded = load_and_query_execution_result_job_report_collection_summaries(
            &index_path,
            &one_match_query,
        )
        .expect("latest-only canonical single-match summary query should succeed");
        assert_eq!(one_match_loaded, vec![latest_only_summary]);
    }

    #[test]
    fn canonical_contract_end_to_end_failure_path_rejects_invalid_report_artifact_at_report_load_boundary()
     {
        let (directory, _) = sample_execution_ledger_history();
        let bundle_dir = directory.path().join("bundle");
        let query = LedgerSelectionQuery {
            request_id: Some("request-shared".to_string()),
            ..LedgerSelectionQuery::default()
        };
        let report = query_and_stub_execute_execution_result_job_spec(
            &bundle_dir,
            &query,
            "handoff-canonical-end-to-end-failure",
            "run-request-canonical-end-to-end-failure",
            "job-spec-canonical-end-to-end-failure",
            ExecutionResultSelectionMode::LatestOnly,
        )
        .expect("canonical end-to-end stub report should build");
        let report_path = directory
            .path()
            .join("canonical-end-to-end-invalid-intermediate-report.json");
        let index_path = directory
            .path()
            .join("canonical-end-to-end-invalid-intermediate-index.json");

        persist_execution_result_job_report(&report_path, &report)
            .expect("canonical end-to-end report should persist");
        register_execution_result_job_report_in_index(&index_path, &report_path, &report)
            .expect("canonical end-to-end report should register");

        let mut invalid_report = report.clone();
        invalid_report.expected_entry_count += 1;
        fs::write(
            &report_path,
            serde_json::to_vec_pretty(&invalid_report)
                .expect("invalid intermediate canonical report should serialize"),
        )
        .expect("invalid intermediate canonical report should overwrite persisted artifact");

        let error = load_and_query_execution_result_job_reports(
            &index_path,
            &ExecutionResultJobReportIndexQuery {
                job_spec_id: Some(report.job_spec_id.clone()),
                latest_only: true,
                ..ExecutionResultJobReportIndexQuery::default()
            },
        )
        .expect_err("invalid intermediate canonical report should fail at report load boundary");
        assert!(
            error.to_string().contains("job report"),
            "unexpected error: {error}"
        );
    }

    #[test]
    fn canonical_contract_report_surface_round_trips_indexes_queries_and_loads_without_drift() {
        let directory = tempdir().expect("tempdir should be created");
        let round_trip_report_path = directory.path().join("canonical-round-trip-report.json");
        let round_trip_report = sample_execution_result_job_report();

        persist_execution_result_job_report(&round_trip_report_path, &round_trip_report)
            .expect("canonical report persist should succeed");
        let round_trip_loaded = load_execution_result_job_report(&round_trip_report_path)
            .expect("canonical report load should succeed");

        assert_eq!(round_trip_loaded, round_trip_report);

        let canonical_index_path = directory.path().join("canonical-report-index.json");
        let canonical_reports = sample_queryable_execution_result_job_reports();

        for report in &canonical_reports {
            let report_path = directory
                .path()
                .join(format!("canonical-{}.json", report.job_spec_id));
            persist_execution_result_job_report(&report_path, report)
                .expect("canonical queryable report should persist");
            register_execution_result_job_report_in_index(
                &canonical_index_path,
                &report_path,
                report,
            )
            .expect("canonical queryable report should register");
        }

        let loaded_index = load_execution_result_job_report_index(&canonical_index_path)
            .expect("canonical report index should reload");
        let query = ExecutionResultJobReportIndexQuery {
            source_run_request_id: Some("run-request-shared".to_string()),
            source_handoff_bundle_id: Some("handoff-shared".to_string()),
            export_name: Some("restore-stage-shared".to_string()),
            ..ExecutionResultJobReportIndexQuery::default()
        };
        let selection = query_execution_result_job_report_index(&loaded_index, &query)
            .expect("canonical report index query should succeed");
        let loaded_reports =
            load_and_query_execution_result_job_reports(&canonical_index_path, &query)
                .expect("canonical report query/load should succeed");

        assert_eq!(selection.selected_entry_count, canonical_reports.len());
        assert_eq!(
            selection
                .selected_entries
                .iter()
                .map(|entry| entry.ordinal)
                .collect::<Vec<_>>(),
            vec![0, 1, 2]
        );
        assert_eq!(
            selection
                .selected_entries
                .iter()
                .map(|entry| entry.job_spec_id.as_str())
                .collect::<Vec<_>>(),
            vec!["job-spec-alpha", "job-spec-beta", "job-spec-gamma"]
        );
        assert_eq!(loaded_reports, canonical_reports);
    }

    #[test]
    fn canonical_contract_summary_surface_queries_loads_and_aggregates_without_drift() {
        let (
            _directory,
            index_path,
            _latest_only_summary_path,
            latest_only_summary,
            _full_history_summary_path,
            full_history_summary,
        ) = persist_sample_execution_result_job_report_collection_summaries_with_index();
        let query = ExecutionResultJobReportCollectionSummaryIndexQuery::default();
        let loaded_index = load_execution_result_job_report_collection_summary_index(&index_path)
            .expect("canonical summary index should reload");
        let selection =
            query_execution_result_job_report_collection_summary_index(&loaded_index, &query)
                .expect("canonical summary index query should succeed");
        let loaded_summaries =
            load_and_query_execution_result_job_report_collection_summaries(&index_path, &query)
                .expect("canonical summary query/load should succeed");
        let aggregate = load_query_and_aggregate_execution_result_job_report_collection_summaries(
            &index_path,
            &query,
        )
        .expect("canonical summary aggregate should succeed");
        let expected_aggregate =
            summarize_execution_result_job_report_collection_summaries(&loaded_summaries);

        assert_eq!(selection.selected_entry_count, 2);
        assert_eq!(
            selection
                .selected_entries
                .iter()
                .map(|entry| entry.ordinal)
                .collect::<Vec<_>>(),
            vec![0, 1]
        );
        assert_eq!(
            loaded_summaries,
            vec![latest_only_summary.clone(), full_history_summary.clone()]
        );
        assert_eq!(aggregate, expected_aggregate);
        assert_eq!(
            aggregate,
            summarize_execution_result_job_report_collection_summaries(&[
                latest_only_summary,
                full_history_summary,
            ])
        );
    }

    #[test]
    fn canonical_contract_summary_publication_bridge_preserves_built_summary_exactly() {
        let directory = tempdir().expect("tempdir should be created");
        let summary_index_path = directory.path().join("canonical-summary-bridge-index.json");
        let summary_output_path = directory
            .path()
            .join("canonical-summary-bridge-output.json");
        let built_summary =
            sample_execution_result_job_report_collection_summary_full_history_multi_report();

        persist_execution_result_job_report_collection_summary(
            &summary_output_path,
            &built_summary,
        )
        .expect("canonical built summary should persist");
        let loaded_summary =
            load_execution_result_job_report_collection_summary(&summary_output_path)
                .expect("canonical built summary should reload");

        assert_eq!(loaded_summary, built_summary);

        let indexed_loaded =
            persist_register_and_index_load_execution_result_job_report_collection_summary(
                &built_summary,
                &summary_output_path,
                &summary_index_path,
            )
            .expect("canonical summary publication bridge should succeed");
        let loaded_index =
            load_execution_result_job_report_collection_summary_index(&summary_index_path)
                .expect("canonical summary bridge index should reload");
        let selection = query_execution_result_job_report_collection_summary_index(
            &loaded_index,
            &ExecutionResultJobReportCollectionSummaryIndexQuery::default(),
        )
        .expect("canonical summary bridge index query should succeed");

        assert_eq!(indexed_loaded, built_summary);
        assert_eq!(selection.selected_entry_count, 1);
        assert_eq!(
            selection.selected_entries[0].summary_file_path,
            path_to_owned_string(&summary_output_path)
                .expect("summary output path should serialize")
        );
        assert_eq!(
            selection.selected_entries[0].report_count,
            built_summary.report_count
        );
        assert_eq!(
            selection.selected_entries[0].total_entry_count,
            built_summary.total_entry_count
        );
    }

    #[test]
    fn canonical_contract_stub_bridge_preserves_report_and_summary_fields_across_public_boundaries()
    {
        let (directory, _) = sample_execution_ledger_history();
        let bundle_dir = directory.path().join("bundle");
        let ledger_query = LedgerSelectionQuery {
            request_id: Some("request-shared".to_string()),
            ..LedgerSelectionQuery::default()
        };
        let direct_report = query_and_stub_execute_execution_result_job_spec(
            &bundle_dir,
            &ledger_query,
            "handoff-canonical-bridge-direct",
            "run-request-canonical-bridge-direct",
            "job-spec-canonical-bridge-direct",
            ExecutionResultSelectionMode::LatestOnly,
        )
        .expect("canonical direct stub bridge should execute");
        let report_path = directory.path().join("canonical-bridge-report.json");
        let report_index_path = directory.path().join("canonical-bridge-report-index.json");
        let registered_report =
            query_stub_execute_persist_load_and_register_execution_result_job_report(
                &bundle_dir,
                &ledger_query,
                "handoff-canonical-bridge-direct",
                "run-request-canonical-bridge-direct",
                "job-spec-canonical-bridge-direct",
                ExecutionResultSelectionMode::LatestOnly,
                &report_path,
                &report_index_path,
            )
            .expect("canonical report registration bridge should succeed");
        let report_index_query = ExecutionResultJobReportIndexQuery {
            job_spec_id: Some("job-spec-canonical-bridge-direct".to_string()),
            ..ExecutionResultJobReportIndexQuery::default()
        };
        let expected_summary_report = query_and_stub_execute_execution_result_job_spec(
            &bundle_dir,
            &ledger_query,
            "handoff-canonical-bridge-summary",
            "run-request-canonical-bridge-summary",
            "job-spec-canonical-bridge-summary",
            ExecutionResultSelectionMode::LatestOnly,
        )
        .expect("canonical expected summary stub report should execute");
        let queried_reports =
            query_stub_execute_persist_load_register_query_and_load_execution_result_job_reports(
                &bundle_dir,
                &ledger_query,
                "handoff-canonical-bridge-query",
                "run-request-canonical-bridge-query",
                "job-spec-canonical-bridge-query",
                ExecutionResultSelectionMode::LatestOnly,
                directory.path().join("canonical-query-report.json"),
                directory.path().join("canonical-query-report-index.json"),
                &ExecutionResultJobReportIndexQuery {
                    job_spec_id: Some("job-spec-canonical-bridge-query".to_string()),
                    ..ExecutionResultJobReportIndexQuery::default()
                },
            )
            .expect("canonical report query/load bridge should succeed");
        let indexed_loaded_summary = query_stub_execute_register_report_and_index_load_summary(
            &bundle_dir,
            &ledger_query,
            "handoff-canonical-bridge-summary",
            "run-request-canonical-bridge-summary",
            "job-spec-canonical-bridge-summary",
            ExecutionResultSelectionMode::LatestOnly,
            directory.path().join("canonical-summary-report.json"),
            directory.path().join("canonical-summary-report-index.json"),
            &ExecutionResultJobReportIndexQuery {
                job_spec_id: Some("job-spec-canonical-bridge-summary".to_string()),
                ..ExecutionResultJobReportIndexQuery::default()
            },
            directory.path().join("canonical-summary-index.json"),
            directory.path().join("canonical-summary-output.json"),
        )
        .expect("canonical summary bridge should succeed");

        validate_execution_result_job_report(&direct_report)
            .expect("canonical direct stub report should validate");
        assert_eq!(registered_report, direct_report);
        assert_eq!(
            load_and_query_execution_result_job_reports(&report_index_path, &report_index_query)
                .expect("canonical registered report should query/load"),
            vec![direct_report.clone()]
        );
        assert_eq!(queried_reports.len(), 1);
        validate_execution_result_job_report(&queried_reports[0])
            .expect("canonical queried stub report should validate");
        assert_eq!(
            queried_reports[0].job_spec_id,
            "job-spec-canonical-bridge-query"
        );
        assert_eq!(
            indexed_loaded_summary,
            summarize_execution_result_job_reports(&[expected_summary_report])
        );
    }

    #[test]
    fn canonical_execution_result_builders_are_repeatable_under_identical_inputs() {
        let (directory, history) = sample_execution_ledger_history();
        let bundle_dir = directory.path().join("bundle");
        let query = LedgerSelectionQuery {
            request_id: Some("request-shared".to_string()),
            ..LedgerSelectionQuery::default()
        };

        let first_history = inspect_execution_ledger_history(&bundle_dir)
            .expect("first canonical history inspection should succeed");
        let second_history = inspect_execution_ledger_history(&bundle_dir)
            .expect("second canonical history inspection should succeed");
        assert_eq!(first_history, history);
        assert_eq!(second_history, history);

        let first_query = query_execution_ledger_history(&history, &query);
        let second_query = query_execution_ledger_history(&history, &query);
        assert_eq!(first_query, second_query);
        assert_eq!(
            first_query
                .iter()
                .map(|entry| (
                    entry.index_entry.result_id.clone(),
                    entry.index_entry.request_id.clone(),
                    entry.index_entry.plan_id.clone(),
                    entry.result.status,
                    entry.result.recorded_at_unix_ms,
                ))
                .collect::<Vec<_>>(),
            second_query
                .iter()
                .map(|entry| (
                    entry.index_entry.result_id.clone(),
                    entry.index_entry.request_id.clone(),
                    entry.index_entry.plan_id.clone(),
                    entry.result.status,
                    entry.result.recorded_at_unix_ms,
                ))
                .collect::<Vec<_>>()
        );

        let first_handoff = build_execution_result_handoff_bundle(
            &first_query,
            "handoff-stage46-repeatable",
            ExecutionResultSelectionMode::FullHistory,
        )
        .expect("first canonical handoff build should succeed");
        let second_handoff = build_execution_result_handoff_bundle(
            &second_query,
            "handoff-stage46-repeatable",
            ExecutionResultSelectionMode::FullHistory,
        )
        .expect("second canonical handoff build should succeed");
        let history_handoff = build_handoff_bundle_from_history(
            &history,
            "handoff-stage46-history-repeatable",
            ExecutionResultSelectionMode::FullHistory,
        )
        .expect("canonical handoff-from-history build should succeed");
        let history_handoff_repeat = build_handoff_bundle_from_history(
            &history,
            "handoff-stage46-history-repeatable",
            ExecutionResultSelectionMode::FullHistory,
        )
        .expect("repeated canonical handoff-from-history build should succeed");
        assert_eq!(first_handoff, second_handoff);
        assert_eq!(history_handoff, history_handoff_repeat);

        let first_run_request = build_execution_result_run_request(
            &first_handoff.entries,
            "run-request-stage46-repeatable",
            first_handoff.handoff_bundle_id.clone(),
            first_handoff.export_name.clone(),
            first_handoff.selection_mode,
        )
        .expect("first canonical run request build should succeed");
        let second_run_request = build_execution_result_run_request(
            &second_handoff.entries,
            "run-request-stage46-repeatable",
            second_handoff.handoff_bundle_id.clone(),
            second_handoff.export_name.clone(),
            second_handoff.selection_mode,
        )
        .expect("second canonical run request build should succeed");
        let history_run_request = build_run_request_from_handoff_bundle(
            &history_handoff,
            "run-request-stage46-history-repeatable",
        )
        .expect("canonical run request-from-handoff should succeed");
        let history_run_request_repeat = build_run_request_from_handoff_bundle(
            &history_handoff_repeat,
            "run-request-stage46-history-repeatable",
        )
        .expect("repeated canonical run request-from-handoff should succeed");
        assert_eq!(first_run_request, second_run_request);
        assert_eq!(history_run_request, history_run_request_repeat);

        let first_job_spec = build_execution_result_job_spec(
            &first_run_request.entries,
            "job-spec-stage46-repeatable",
            first_run_request.run_request_id.clone(),
            first_run_request.source_handoff_bundle_id.clone(),
            first_run_request.export_name.clone(),
            first_run_request.selection_mode,
            first_run_request.expected_entry_count,
            first_run_request.source_provenance_hash.clone(),
        )
        .expect("first canonical job spec build should succeed");
        let second_job_spec = build_execution_result_job_spec(
            &second_run_request.entries,
            "job-spec-stage46-repeatable",
            second_run_request.run_request_id.clone(),
            second_run_request.source_handoff_bundle_id.clone(),
            second_run_request.export_name.clone(),
            second_run_request.selection_mode,
            second_run_request.expected_entry_count,
            second_run_request.source_provenance_hash.clone(),
        )
        .expect("second canonical job spec build should succeed");
        let history_job_spec = build_job_spec_from_run_request(
            &history_run_request,
            "job-spec-stage46-history-repeatable",
        )
        .expect("canonical job spec-from-run-request should succeed");
        let history_job_spec_repeat = build_job_spec_from_run_request(
            &history_run_request_repeat,
            "job-spec-stage46-history-repeatable",
        )
        .expect("repeated canonical job spec-from-run-request should succeed");
        assert_eq!(first_job_spec, second_job_spec);
        assert_eq!(history_job_spec, history_job_spec_repeat);
    }

    #[test]
    fn canonical_stub_execution_publication_and_reload_are_repeatable_under_identical_inputs() {
        let (directory, _) = sample_execution_ledger_history();
        let bundle_dir = directory.path().join("bundle");
        let ledger_query = LedgerSelectionQuery {
            request_id: Some("request-shared".to_string()),
            ..LedgerSelectionQuery::default()
        };

        let first_report = query_and_stub_execute_execution_result_job_spec(
            &bundle_dir,
            &ledger_query,
            "handoff-stage46-stub-repeatable",
            "run-request-stage46-stub-repeatable",
            "job-spec-stage46-stub-repeatable",
            ExecutionResultSelectionMode::LatestOnly,
        )
        .expect("first canonical stub execution should succeed");
        let second_report = query_and_stub_execute_execution_result_job_spec(
            &bundle_dir,
            &ledger_query,
            "handoff-stage46-stub-repeatable",
            "run-request-stage46-stub-repeatable",
            "job-spec-stage46-stub-repeatable",
            ExecutionResultSelectionMode::LatestOnly,
        )
        .expect("second canonical stub execution should succeed");
        assert_eq!(first_report, second_report);

        let first_registered_report =
            query_stub_execute_persist_load_and_register_execution_result_job_report(
                &bundle_dir,
                &ledger_query,
                "handoff-stage46-stub-publish",
                "run-request-stage46-stub-publish",
                "job-spec-stage46-stub-publish",
                ExecutionResultSelectionMode::LatestOnly,
                directory.path().join("stage46-stub-report-a.json"),
                directory.path().join("stage46-stub-report-index-a.json"),
            )
            .expect("first canonical stub publication should succeed");
        let second_registered_report =
            query_stub_execute_persist_load_and_register_execution_result_job_report(
                &bundle_dir,
                &ledger_query,
                "handoff-stage46-stub-publish",
                "run-request-stage46-stub-publish",
                "job-spec-stage46-stub-publish",
                ExecutionResultSelectionMode::LatestOnly,
                directory.path().join("stage46-stub-report-b.json"),
                directory.path().join("stage46-stub-report-index-b.json"),
            )
            .expect("second canonical stub publication should succeed");
        assert_eq!(first_registered_report, second_registered_report);

        let report_index_query = ExecutionResultJobReportIndexQuery {
            job_spec_id: Some("job-spec-stage46-stub-query".to_string()),
            ..ExecutionResultJobReportIndexQuery::default()
        };
        let first_loaded_reports =
            query_stub_execute_persist_load_register_query_and_load_execution_result_job_reports(
                &bundle_dir,
                &ledger_query,
                "handoff-stage46-stub-query",
                "run-request-stage46-stub-query",
                "job-spec-stage46-stub-query",
                ExecutionResultSelectionMode::LatestOnly,
                directory.path().join("stage46-stub-query-report-a.json"),
                directory
                    .path()
                    .join("stage46-stub-query-report-index-a.json"),
                &report_index_query,
            )
            .expect("first canonical stub query/load publication should succeed");
        let second_loaded_reports =
            query_stub_execute_persist_load_register_query_and_load_execution_result_job_reports(
                &bundle_dir,
                &ledger_query,
                "handoff-stage46-stub-query",
                "run-request-stage46-stub-query",
                "job-spec-stage46-stub-query",
                ExecutionResultSelectionMode::LatestOnly,
                directory.path().join("stage46-stub-query-report-b.json"),
                directory
                    .path()
                    .join("stage46-stub-query-report-index-b.json"),
                &report_index_query,
            )
            .expect("second canonical stub query/load publication should succeed");
        assert_eq!(first_loaded_reports, second_loaded_reports);

        let summary_report_index_query = ExecutionResultJobReportIndexQuery {
            job_spec_id: Some("job-spec-stage46-stub-summary".to_string()),
            ..ExecutionResultJobReportIndexQuery::default()
        };
        let first_summary = query_stub_execute_register_report_and_index_load_summary(
            &bundle_dir,
            &ledger_query,
            "handoff-stage46-stub-summary",
            "run-request-stage46-stub-summary",
            "job-spec-stage46-stub-summary",
            ExecutionResultSelectionMode::LatestOnly,
            directory.path().join("stage46-stub-summary-report-a.json"),
            directory
                .path()
                .join("stage46-stub-summary-report-index-a.json"),
            &summary_report_index_query,
            directory.path().join("stage46-stub-summary-index-a.json"),
            directory.path().join("stage46-stub-summary-a.json"),
        )
        .expect("first canonical stub summary publication should succeed");
        let second_summary = query_stub_execute_register_report_and_index_load_summary(
            &bundle_dir,
            &ledger_query,
            "handoff-stage46-stub-summary",
            "run-request-stage46-stub-summary",
            "job-spec-stage46-stub-summary",
            ExecutionResultSelectionMode::LatestOnly,
            directory.path().join("stage46-stub-summary-report-b.json"),
            directory
                .path()
                .join("stage46-stub-summary-report-index-b.json"),
            &summary_report_index_query,
            directory.path().join("stage46-stub-summary-index-b.json"),
            directory.path().join("stage46-stub-summary-b.json"),
        )
        .expect("second canonical stub summary publication should succeed");
        assert_eq!(first_summary, second_summary);
        assert_eq!(
            first_summary,
            summarize_execution_result_job_reports(&[
                query_and_stub_execute_execution_result_job_spec(
                    &bundle_dir,
                    &ledger_query,
                    "handoff-stage46-stub-summary",
                    "run-request-stage46-stub-summary",
                    "job-spec-stage46-stub-summary",
                    ExecutionResultSelectionMode::LatestOnly,
                )
                .expect("canonical stub summary seed report should execute")
            ])
        );
    }

    #[test]
    fn canonical_summary_publication_query_and_aggregate_are_repeatable_under_unchanged_inputs() {
        let directory = tempdir().expect("tempdir should be created");
        let reports = sample_queryable_execution_result_job_reports();
        let first_summary = summarize_execution_result_job_reports(&reports);
        let second_summary = summarize_execution_result_job_reports(&reports);
        assert_eq!(first_summary, second_summary);

        let first_indexed_loaded =
            persist_register_and_index_load_execution_result_job_report_collection_summary(
                &first_summary,
                directory.path().join("stage46-summary-a.json"),
                directory.path().join("stage46-summary-index-a.json"),
            )
            .expect("first canonical summary publication should succeed");
        let second_indexed_loaded =
            persist_register_and_index_load_execution_result_job_report_collection_summary(
                &second_summary,
                directory.path().join("stage46-summary-b.json"),
                directory.path().join("stage46-summary-index-b.json"),
            )
            .expect("second canonical summary publication should succeed");
        assert_eq!(first_indexed_loaded, second_indexed_loaded);

        let repeated_index_path = directory.path().join("stage46-summary-repeat-index.json");
        let repeated_summary_path = directory.path().join("stage46-summary-repeat.json");
        persist_register_and_index_load_execution_result_job_report_collection_summary(
            &first_summary,
            &repeated_summary_path,
            &repeated_index_path,
        )
        .expect("repeated canonical summary publication seed should succeed");
        let summary_query = ExecutionResultJobReportCollectionSummaryIndexQuery::default();
        let first_loaded = load_and_query_execution_result_job_report_collection_summaries(
            &repeated_index_path,
            &summary_query,
        )
        .expect("first canonical summary query/load should succeed");
        let second_loaded = load_and_query_execution_result_job_report_collection_summaries(
            &repeated_index_path,
            &summary_query,
        )
        .expect("second canonical summary query/load should succeed");
        assert_eq!(first_loaded, second_loaded);
        assert_eq!(first_loaded, vec![first_summary.clone()]);

        let first_aggregate =
            load_query_and_aggregate_execution_result_job_report_collection_summaries(
                &repeated_index_path,
                &summary_query,
            )
            .expect("first canonical summary aggregate should succeed");
        let second_aggregate =
            load_query_and_aggregate_execution_result_job_report_collection_summaries(
                &repeated_index_path,
                &summary_query,
            )
            .expect("second canonical summary aggregate should succeed");
        assert_eq!(first_aggregate, second_aggregate);
        assert_eq!(first_aggregate, first_summary);
    }

    #[test]
    fn canonical_end_to_end_execution_result_flow_is_repeatable_under_identical_inputs() {
        let (directory, _) = sample_execution_ledger_history();
        let bundle_dir = directory.path().join("bundle");
        let ledger_query = LedgerSelectionQuery {
            request_id: Some("request-shared".to_string()),
            status: Some(ExecutionResultStatus::StubbedSuccess),
            ..LedgerSelectionQuery::default()
        };
        let report_index_query = ExecutionResultJobReportIndexQuery {
            job_spec_id: Some("job-spec-stage46-end-to-end".to_string()),
            ..ExecutionResultJobReportIndexQuery::default()
        };
        let summary_query = ExecutionResultJobReportCollectionSummaryIndexQuery::default();

        let first_report = query_and_stub_execute_execution_result_job_spec(
            &bundle_dir,
            &ledger_query,
            "handoff-stage46-end-to-end",
            "run-request-stage46-end-to-end",
            "job-spec-stage46-end-to-end",
            ExecutionResultSelectionMode::FullHistory,
        )
        .expect("first canonical end-to-end report build should succeed");
        let second_report = query_and_stub_execute_execution_result_job_spec(
            &bundle_dir,
            &ledger_query,
            "handoff-stage46-end-to-end",
            "run-request-stage46-end-to-end",
            "job-spec-stage46-end-to-end",
            ExecutionResultSelectionMode::FullHistory,
        )
        .expect("second canonical end-to-end report build should succeed");
        assert_eq!(first_report, second_report);

        let first_loaded_reports =
            query_stub_execute_persist_load_register_query_and_load_execution_result_job_reports(
                &bundle_dir,
                &ledger_query,
                "handoff-stage46-end-to-end",
                "run-request-stage46-end-to-end",
                "job-spec-stage46-end-to-end",
                ExecutionResultSelectionMode::FullHistory,
                directory.path().join("stage46-end-to-end-report-a.json"),
                directory
                    .path()
                    .join("stage46-end-to-end-report-index-a.json"),
                &report_index_query,
            )
            .expect("first canonical end-to-end report publication should succeed");
        let second_loaded_reports =
            query_stub_execute_persist_load_register_query_and_load_execution_result_job_reports(
                &bundle_dir,
                &ledger_query,
                "handoff-stage46-end-to-end",
                "run-request-stage46-end-to-end",
                "job-spec-stage46-end-to-end",
                ExecutionResultSelectionMode::FullHistory,
                directory.path().join("stage46-end-to-end-report-b.json"),
                directory
                    .path()
                    .join("stage46-end-to-end-report-index-b.json"),
                &report_index_query,
            )
            .expect("second canonical end-to-end report publication should succeed");
        assert_eq!(first_loaded_reports, second_loaded_reports);
        assert_eq!(first_loaded_reports, vec![first_report.clone()]);

        let first_summary = summarize_execution_result_job_reports(&first_loaded_reports);
        let second_summary = summarize_execution_result_job_reports(&second_loaded_reports);
        assert_eq!(first_summary, second_summary);

        let first_indexed_loaded_summary =
            persist_register_and_index_load_execution_result_job_report_collection_summary(
                &first_summary,
                directory.path().join("stage46-end-to-end-summary-a.json"),
                directory
                    .path()
                    .join("stage46-end-to-end-summary-index-a.json"),
            )
            .expect("first canonical end-to-end summary publication should succeed");
        let second_indexed_loaded_summary =
            persist_register_and_index_load_execution_result_job_report_collection_summary(
                &second_summary,
                directory.path().join("stage46-end-to-end-summary-b.json"),
                directory
                    .path()
                    .join("stage46-end-to-end-summary-index-b.json"),
            )
            .expect("second canonical end-to-end summary publication should succeed");
        assert_eq!(first_indexed_loaded_summary, second_indexed_loaded_summary);

        let repeated_summary_index_path = directory
            .path()
            .join("stage46-end-to-end-summary-repeat-index.json");
        let repeated_summary_path = directory
            .path()
            .join("stage46-end-to-end-summary-repeat.json");
        persist_register_and_index_load_execution_result_job_report_collection_summary(
            &first_summary,
            &repeated_summary_path,
            &repeated_summary_index_path,
        )
        .expect("canonical end-to-end repeated summary publication seed should succeed");
        let first_loaded_summaries =
            load_and_query_execution_result_job_report_collection_summaries(
                &repeated_summary_index_path,
                &summary_query,
            )
            .expect("first canonical end-to-end summary query/load should succeed");
        let second_loaded_summaries =
            load_and_query_execution_result_job_report_collection_summaries(
                &repeated_summary_index_path,
                &summary_query,
            )
            .expect("second canonical end-to-end summary query/load should succeed");
        assert_eq!(first_loaded_summaries, second_loaded_summaries);
        assert_eq!(first_loaded_summaries, vec![first_summary.clone()]);

        let first_aggregate =
            load_query_and_aggregate_execution_result_job_report_collection_summaries(
                &repeated_summary_index_path,
                &summary_query,
            )
            .expect("first canonical end-to-end aggregate should succeed");
        let second_aggregate =
            load_query_and_aggregate_execution_result_job_report_collection_summaries(
                &repeated_summary_index_path,
                &summary_query,
            )
            .expect("second canonical end-to-end aggregate should succeed");
        assert_eq!(first_aggregate, second_aggregate);
        assert_eq!(first_aggregate, first_summary);
    }

    #[test]
    fn canonical_end_to_end_full_history_path_locks_reports_summaries_and_aggregate_order() {
        let (directory, _) = sample_execution_ledger_history();
        let bundle_dir = directory.path().join("bundle");
        let report_index_path = directory
            .path()
            .join("stage42-full-history-report-index.json");
        let summary_index_path = directory
            .path()
            .join("stage42-full-history-summary-index.json");

        let history = inspect_execution_ledger_history(&bundle_dir)
            .expect("full-history canonical end-to-end history should load");
        let shared_query = LedgerSelectionQuery {
            request_id: Some("request-shared".to_string()),
            status: Some(ExecutionResultStatus::StubbedSuccess),
            ..LedgerSelectionQuery::default()
        };
        let failure_query = LedgerSelectionQuery {
            status: Some(ExecutionResultStatus::StubbedFailure),
            branch_id: Some("branch-1".to_string()),
            ..LedgerSelectionQuery::default()
        };

        let shared_entries = query_execution_ledger_history(&history, &shared_query);
        let failure_entries = query_execution_ledger_history(&history, &failure_query);
        let shared_handoff = build_execution_result_handoff_bundle(
            &shared_entries,
            "handoff-stage42-full-history-shared",
            ExecutionResultSelectionMode::FullHistory,
        )
        .expect("shared full-history handoff should build");
        let failure_handoff = build_execution_result_handoff_bundle(
            &failure_entries,
            "handoff-stage42-full-history-failure",
            ExecutionResultSelectionMode::FullHistory,
        )
        .expect("failure full-history handoff should build");
        let shared_run_request = build_execution_result_run_request(
            &shared_handoff.entries,
            "run-request-stage42-full-history-shared",
            shared_handoff.handoff_bundle_id.clone(),
            shared_handoff.export_name.clone(),
            shared_handoff.selection_mode,
        )
        .expect("shared full-history run request should build");
        let failure_run_request = build_execution_result_run_request(
            &failure_handoff.entries,
            "run-request-stage42-full-history-failure",
            failure_handoff.handoff_bundle_id.clone(),
            failure_handoff.export_name.clone(),
            failure_handoff.selection_mode,
        )
        .expect("failure full-history run request should build");
        let shared_job_spec = build_execution_result_job_spec(
            &shared_run_request.entries,
            "job-spec-stage42-full-history-shared",
            shared_run_request.run_request_id.clone(),
            shared_run_request.source_handoff_bundle_id.clone(),
            shared_run_request.export_name.clone(),
            shared_run_request.selection_mode,
            shared_run_request.expected_entry_count,
            shared_run_request.source_provenance_hash.clone(),
        )
        .expect("shared full-history job spec should build");
        let failure_job_spec = build_execution_result_job_spec(
            &failure_run_request.entries,
            "job-spec-stage42-full-history-failure",
            failure_run_request.run_request_id.clone(),
            failure_run_request.source_handoff_bundle_id.clone(),
            failure_run_request.export_name.clone(),
            failure_run_request.selection_mode,
            failure_run_request.expected_entry_count,
            failure_run_request.source_provenance_hash.clone(),
        )
        .expect("failure full-history job spec should build");
        let shared_report = query_and_stub_execute_execution_result_job_spec(
            &bundle_dir,
            &shared_query,
            "handoff-stage42-full-history-shared",
            "run-request-stage42-full-history-shared",
            "job-spec-stage42-full-history-shared",
            ExecutionResultSelectionMode::FullHistory,
        )
        .expect("shared full-history report should execute");
        let failure_report = query_and_stub_execute_execution_result_job_spec(
            &bundle_dir,
            &failure_query,
            "handoff-stage42-full-history-failure",
            "run-request-stage42-full-history-failure",
            "job-spec-stage42-full-history-failure",
            ExecutionResultSelectionMode::FullHistory,
        )
        .expect("failure full-history report should execute");

        assert_job_spec_matches_run_request(&shared_job_spec, &shared_run_request);
        assert_job_spec_matches_run_request(&failure_job_spec, &failure_run_request);
        assert_eq!(shared_report.job_spec_id, shared_job_spec.job_spec_id);
        assert_eq!(
            shared_report.source_provenance_hash,
            shared_job_spec.source_provenance_hash
        );
        assert_eq!(
            shared_report.expected_entry_count,
            shared_job_spec.expected_entry_count
        );
        assert_eq!(
            shared_report
                .entries
                .iter()
                .map(|entry| entry.result_id.as_str())
                .collect::<Vec<_>>(),
            collect_job_spec_result_ids(&shared_job_spec)
                .iter()
                .map(String::as_str)
                .collect::<Vec<_>>()
        );
        assert_eq!(failure_report.job_spec_id, failure_job_spec.job_spec_id);
        assert_eq!(
            failure_report.source_provenance_hash,
            failure_job_spec.source_provenance_hash
        );
        assert_eq!(
            failure_report
                .entries
                .iter()
                .map(|entry| entry.result_id.as_str())
                .collect::<Vec<_>>(),
            collect_job_spec_result_ids(&failure_job_spec)
                .iter()
                .map(String::as_str)
                .collect::<Vec<_>>()
        );

        let shared_report_path = directory
            .path()
            .join("stage42-full-history-shared-report.json");
        let failure_report_path = directory
            .path()
            .join("stage42-full-history-failure-report.json");
        persist_execution_result_job_report(&shared_report_path, &shared_report)
            .expect("shared full-history report should persist");
        register_execution_result_job_report_in_index(
            &report_index_path,
            &shared_report_path,
            &shared_report,
        )
        .expect("shared full-history report should register");
        persist_execution_result_job_report(&failure_report_path, &failure_report)
            .expect("failure full-history report should persist");
        register_execution_result_job_report_in_index(
            &report_index_path,
            &failure_report_path,
            &failure_report,
        )
        .expect("failure full-history report should register");

        let loaded_reports = load_and_query_execution_result_job_reports(
            &report_index_path,
            &ExecutionResultJobReportIndexQuery::default(),
        )
        .expect("full-history reports should load in index order");
        let loaded_reports_round_trip = load_and_query_execution_result_job_reports(
            &report_index_path,
            &ExecutionResultJobReportIndexQuery::default(),
        )
        .expect("full-history reports should load deterministically");

        assert_eq!(
            loaded_reports,
            vec![shared_report.clone(), failure_report.clone()]
        );
        assert_eq!(loaded_reports_round_trip, loaded_reports);

        let shared_summary =
            summarize_execution_result_job_reports(std::slice::from_ref(&shared_report));
        let all_reports_summary = summarize_execution_result_job_reports(&loaded_reports);
        let shared_summary_path = directory
            .path()
            .join("stage42-full-history-shared-summary.json");
        let all_reports_summary_path = directory
            .path()
            .join("stage42-full-history-all-reports-summary.json");
        let indexed_shared_summary =
            persist_register_and_index_load_execution_result_job_report_collection_summary(
                &shared_summary,
                &shared_summary_path,
                &summary_index_path,
            )
            .expect("shared full-history summary should persist/register/index-load");
        let indexed_all_reports_summary =
            persist_register_and_index_load_execution_result_job_report_collection_summary(
                &all_reports_summary,
                &all_reports_summary_path,
                &summary_index_path,
            )
            .expect("aggregate full-history summary should persist/register/index-load");

        assert_eq!(indexed_shared_summary, shared_summary);
        assert_eq!(indexed_all_reports_summary, all_reports_summary);

        let loaded_summaries = load_and_query_execution_result_job_report_collection_summaries(
            &summary_index_path,
            &ExecutionResultJobReportCollectionSummaryIndexQuery::default(),
        )
        .expect("full-history summaries should load in index order");
        let loaded_summaries_round_trip =
            load_and_query_execution_result_job_report_collection_summaries(
                &summary_index_path,
                &ExecutionResultJobReportCollectionSummaryIndexQuery::default(),
            )
            .expect("full-history summaries should load deterministically");
        let aggregate = load_query_and_aggregate_execution_result_job_report_collection_summaries(
            &summary_index_path,
            &ExecutionResultJobReportCollectionSummaryIndexQuery::default(),
        )
        .expect("full-history summaries should aggregate");
        let aggregate_round_trip =
            load_query_and_aggregate_execution_result_job_report_collection_summaries(
                &summary_index_path,
                &ExecutionResultJobReportCollectionSummaryIndexQuery::default(),
            )
            .expect("full-history summaries should aggregate deterministically");
        let expected_aggregate = summarize_execution_result_job_report_collection_summaries(&[
            indexed_shared_summary.clone(),
            indexed_all_reports_summary.clone(),
        ]);

        assert_eq!(
            loaded_summaries,
            vec![
                indexed_shared_summary.clone(),
                indexed_all_reports_summary.clone()
            ]
        );
        assert_eq!(loaded_summaries_round_trip, loaded_summaries);
        assert_eq!(aggregate, expected_aggregate);
        assert_eq!(aggregate_round_trip, aggregate);
        assert_eq!(aggregate.report_count, 3);
        assert_eq!(aggregate.total_entry_count, 5);
        assert_eq!(
            aggregate.job_spec_ids,
            vec![
                "job-spec-stage42-full-history-shared".to_string(),
                "job-spec-stage42-full-history-failure".to_string(),
            ]
        );
    }

    #[test]
    fn canonical_end_to_end_latest_only_path_reduces_to_one_report_one_summary_and_exact_aggregate()
    {
        let (directory, _) = sample_execution_ledger_history();
        let bundle_dir = directory.path().join("bundle");
        let report_index_path = directory
            .path()
            .join("stage42-latest-only-report-index.json");
        let summary_index_path = directory
            .path()
            .join("stage42-latest-only-summary-index.json");
        let history = inspect_execution_ledger_history(&bundle_dir)
            .expect("latest-only canonical end-to-end history should load");
        let shared_query = LedgerSelectionQuery {
            request_id: Some("request-shared".to_string()),
            status: Some(ExecutionResultStatus::StubbedSuccess),
            ..LedgerSelectionQuery::default()
        };

        let shared_entries = query_execution_ledger_history(&history, &shared_query);
        let shared_handoff = build_execution_result_handoff_bundle(
            &shared_entries,
            "handoff-stage42-latest-only-shared",
            ExecutionResultSelectionMode::LatestOnly,
        )
        .expect("latest-only handoff should build");
        let shared_run_request = build_execution_result_run_request(
            &shared_handoff.entries,
            "run-request-stage42-latest-only-shared",
            shared_handoff.handoff_bundle_id.clone(),
            shared_handoff.export_name.clone(),
            shared_handoff.selection_mode,
        )
        .expect("latest-only run request should build");
        let shared_job_spec = build_execution_result_job_spec(
            &shared_run_request.entries,
            "job-spec-stage42-latest-only-second",
            shared_run_request.run_request_id.clone(),
            shared_run_request.source_handoff_bundle_id.clone(),
            shared_run_request.export_name.clone(),
            shared_run_request.selection_mode,
            shared_run_request.expected_entry_count,
            shared_run_request.source_provenance_hash.clone(),
        )
        .expect("latest-only job spec should build");

        let first_report = query_and_stub_execute_execution_result_job_spec(
            &bundle_dir,
            &shared_query,
            "handoff-stage42-latest-only-shared",
            "run-request-stage42-latest-only-shared",
            "job-spec-stage42-latest-only-first",
            ExecutionResultSelectionMode::FullHistory,
        )
        .expect("first shared report should execute");
        let second_report = query_and_stub_execute_execution_result_job_spec(
            &bundle_dir,
            &shared_query,
            "handoff-stage42-latest-only-shared",
            "run-request-stage42-latest-only-shared",
            "job-spec-stage42-latest-only-second",
            ExecutionResultSelectionMode::LatestOnly,
        )
        .expect("second shared report should execute");

        assert_eq!(second_report.job_spec_id, shared_job_spec.job_spec_id);
        assert_eq!(
            second_report.source_provenance_hash,
            shared_job_spec.source_provenance_hash
        );
        assert_eq!(
            second_report
                .entries
                .iter()
                .map(|entry| entry.result_id.as_str())
                .collect::<Vec<_>>(),
            collect_job_spec_result_ids(&shared_job_spec)
                .iter()
                .map(String::as_str)
                .collect::<Vec<_>>()
        );
        assert_eq!(second_report.entries.len(), 1);
        assert_eq!(second_report.entries[0].result_id, "result-shared-newer");

        let first_report_path = directory
            .path()
            .join("stage42-latest-only-first-report.json");
        let second_report_path = directory
            .path()
            .join("stage42-latest-only-second-report.json");
        persist_execution_result_job_report(&first_report_path, &first_report)
            .expect("first shared report should persist");
        register_execution_result_job_report_in_index(
            &report_index_path,
            &first_report_path,
            &first_report,
        )
        .expect("first shared report should register");
        persist_execution_result_job_report(&second_report_path, &second_report)
            .expect("second shared report should persist");
        register_execution_result_job_report_in_index(
            &report_index_path,
            &second_report_path,
            &second_report,
        )
        .expect("second shared report should register");

        let report_query = ExecutionResultJobReportIndexQuery {
            source_run_request_id: Some("run-request-stage42-latest-only-shared".to_string()),
            source_handoff_bundle_id: Some("handoff-stage42-latest-only-shared".to_string()),
            latest_only: true,
            ..ExecutionResultJobReportIndexQuery::default()
        };
        let latest_loaded_reports =
            load_and_query_execution_result_job_reports(&report_index_path, &report_query)
                .expect("latest-only report query should reduce to one report");

        assert_eq!(latest_loaded_reports, vec![second_report.clone()]);

        let first_summary = summarize_execution_result_job_reports(&[first_report]);
        let second_summary = summarize_execution_result_job_reports(&latest_loaded_reports);
        let first_summary_path = directory
            .path()
            .join("stage42-latest-only-first-summary.json");
        let second_summary_path = directory
            .path()
            .join("stage42-latest-only-second-summary.json");
        let indexed_first_summary =
            persist_register_and_index_load_execution_result_job_report_collection_summary(
                &first_summary,
                &first_summary_path,
                &summary_index_path,
            )
            .expect("first shared summary should persist/register/index-load");
        let indexed_second_summary =
            persist_register_and_index_load_execution_result_job_report_collection_summary(
                &second_summary,
                &second_summary_path,
                &summary_index_path,
            )
            .expect("second shared summary should persist/register/index-load");

        assert_eq!(indexed_first_summary, first_summary);
        assert_eq!(indexed_second_summary, second_summary);

        let summary_query = ExecutionResultJobReportCollectionSummaryIndexQuery {
            source_run_request_ids: vec!["run-request-stage42-latest-only-shared".to_string()],
            source_handoff_bundle_ids: vec!["handoff-stage42-latest-only-shared".to_string()],
            latest_only: true,
            ..ExecutionResultJobReportCollectionSummaryIndexQuery::default()
        };
        let latest_loaded_summaries =
            load_and_query_execution_result_job_report_collection_summaries(
                &summary_index_path,
                &summary_query,
            )
            .expect("latest-only summary query should reduce to one summary");
        let aggregate = load_query_and_aggregate_execution_result_job_report_collection_summaries(
            &summary_index_path,
            &summary_query,
        )
        .expect("latest-only summary aggregate should be exact");

        assert_eq!(
            latest_loaded_summaries,
            vec![indexed_second_summary.clone()]
        );
        assert_eq!(aggregate, indexed_second_summary);
        assert_eq!(aggregate.report_count, 1);
        assert_eq!(aggregate.total_entry_count, 1);
        assert_eq!(
            aggregate.job_spec_ids,
            vec!["job-spec-stage42-latest-only-second".to_string()]
        );
        assert_eq!(
            aggregate.selection_modes,
            vec![ExecutionResultSelectionMode::LatestOnly]
        );
    }

    #[test]
    fn canonical_end_to_end_explicit_and_canonical_compositions_produce_equivalent_artifacts() {
        let (directory, history) = sample_execution_ledger_history();
        let query = LedgerSelectionQuery::default();
        let queried_entries = query_execution_ledger_history(&history, &query);

        let explicit_handoff = build_execution_result_handoff_bundle(
            &queried_entries,
            "handoff-stage42-equivalence",
            ExecutionResultSelectionMode::FullHistory,
        )
        .expect("explicit equivalence handoff should build");
        let explicit_run_request = build_execution_result_run_request(
            &explicit_handoff.entries,
            "run-request-stage42-equivalence",
            explicit_handoff.handoff_bundle_id.clone(),
            explicit_handoff.export_name.clone(),
            explicit_handoff.selection_mode,
        )
        .expect("explicit equivalence run request should build");
        let explicit_job_spec = build_execution_result_job_spec(
            &explicit_run_request.entries,
            "job-spec-stage42-equivalence",
            explicit_run_request.run_request_id.clone(),
            explicit_run_request.source_handoff_bundle_id.clone(),
            explicit_run_request.export_name.clone(),
            explicit_run_request.selection_mode,
            explicit_run_request.expected_entry_count,
            explicit_run_request.source_provenance_hash.clone(),
        )
        .expect("explicit equivalence job spec should build");

        let canonical_handoff = build_handoff_bundle_from_history(
            &history,
            "handoff-stage42-equivalence",
            ExecutionResultSelectionMode::FullHistory,
        )
        .expect("canonical equivalence handoff should build");
        let canonical_run_request = build_run_request_from_handoff_bundle(
            &canonical_handoff,
            "run-request-stage42-equivalence",
        )
        .expect("canonical equivalence run request should build");
        let canonical_job_spec =
            build_job_spec_from_run_request(&canonical_run_request, "job-spec-stage42-equivalence")
                .expect("canonical equivalence job spec should build");
        let executor = StubExecutionResultJobExecutor;
        let explicit_report = executor
            .execute(&explicit_job_spec)
            .expect("explicit equivalence report should execute");
        let canonical_report = executor
            .execute(&canonical_job_spec)
            .expect("canonical equivalence report should execute");

        assert_eq!(canonical_handoff, explicit_handoff);
        assert_eq!(canonical_run_request, explicit_run_request);
        assert_eq!(canonical_job_spec, explicit_job_spec);
        assert_eq!(canonical_report, explicit_report);

        let explicit_report_index_path = directory
            .path()
            .join("stage42-equivalence-explicit-report-index.json");
        let explicit_report_path = directory
            .path()
            .join("stage42-equivalence-explicit-report.json");
        persist_execution_result_job_report(&explicit_report_path, &explicit_report)
            .expect("explicit equivalence report should persist");
        register_execution_result_job_report_in_index(
            &explicit_report_index_path,
            &explicit_report_path,
            &explicit_report,
        )
        .expect("explicit equivalence report should register");
        let explicit_loaded_reports = load_and_query_execution_result_job_reports(
            &explicit_report_index_path,
            &ExecutionResultJobReportIndexQuery {
                job_spec_id: Some("job-spec-stage42-equivalence".to_string()),
                ..ExecutionResultJobReportIndexQuery::default()
            },
        )
        .expect("explicit equivalence report should query/load");
        let explicit_summary = summarize_execution_result_job_reports(&explicit_loaded_reports);
        let explicit_summary_index_path = directory
            .path()
            .join("stage42-equivalence-explicit-summary-index.json");
        let explicit_summary_path = directory
            .path()
            .join("stage42-equivalence-explicit-summary.json");
        persist_execution_result_job_report_collection_summary(
            &explicit_summary_path,
            &explicit_summary,
        )
        .expect("explicit equivalence summary should persist");
        register_execution_result_job_report_collection_summary_in_index(
            &explicit_summary_index_path,
            &explicit_summary_path,
            &explicit_summary,
        )
        .expect("explicit equivalence summary should register");
        let explicit_loaded_summaries =
            load_and_query_execution_result_job_report_collection_summaries(
                &explicit_summary_index_path,
                &ExecutionResultJobReportCollectionSummaryIndexQuery::default(),
            )
            .expect("explicit equivalence summary should query/load");
        let explicit_aggregate =
            load_query_and_aggregate_execution_result_job_report_collection_summaries(
                &explicit_summary_index_path,
                &ExecutionResultJobReportCollectionSummaryIndexQuery::default(),
            )
            .expect("explicit equivalence summary should aggregate");

        let canonical_report_index_path = directory
            .path()
            .join("stage42-equivalence-canonical-report-index.json");
        let canonical_report_path = directory
            .path()
            .join("stage42-equivalence-canonical-report.json");
        persist_execution_result_job_report(&canonical_report_path, &canonical_report)
            .expect("canonical equivalence report should persist");
        register_execution_result_job_report_in_index(
            &canonical_report_index_path,
            &canonical_report_path,
            &canonical_report,
        )
        .expect("canonical equivalence report should register");
        let canonical_loaded_reports = load_and_query_execution_result_job_reports(
            &canonical_report_index_path,
            &ExecutionResultJobReportIndexQuery {
                job_spec_id: Some("job-spec-stage42-equivalence".to_string()),
                ..ExecutionResultJobReportIndexQuery::default()
            },
        )
        .expect("canonical equivalence report should query/load");
        let canonical_summary = summarize_execution_result_job_reports(&canonical_loaded_reports);
        let canonical_summary_index_path = directory
            .path()
            .join("stage42-equivalence-canonical-summary-index.json");
        let canonical_summary_path = directory
            .path()
            .join("stage42-equivalence-canonical-summary.json");
        let canonical_indexed_summary =
            persist_register_and_index_load_execution_result_job_report_collection_summary(
                &canonical_summary,
                &canonical_summary_path,
                &canonical_summary_index_path,
            )
            .expect("canonical equivalence summary should persist/register/index-load");
        let canonical_loaded_summaries =
            load_and_query_execution_result_job_report_collection_summaries(
                &canonical_summary_index_path,
                &ExecutionResultJobReportCollectionSummaryIndexQuery::default(),
            )
            .expect("canonical equivalence summary should query/load");
        let canonical_aggregate =
            load_query_and_aggregate_execution_result_job_report_collection_summaries(
                &canonical_summary_index_path,
                &ExecutionResultJobReportCollectionSummaryIndexQuery::default(),
            )
            .expect("canonical equivalence summary should aggregate");

        assert_eq!(canonical_loaded_reports, explicit_loaded_reports);
        assert_eq!(canonical_summary, explicit_summary);
        assert_eq!(canonical_indexed_summary, explicit_summary);
        assert_eq!(canonical_loaded_summaries, explicit_loaded_summaries);
        assert_eq!(canonical_aggregate, explicit_aggregate);
    }

    #[test]
    fn persist_and_load_execution_result_job_report_index_round_trips_exactly() {
        let directory = tempdir().expect("tempdir should be created");
        let index_path = directory
            .path()
            .join("execution-result-job-report-index.json");
        let index = sample_execution_result_job_report_index();

        persist_execution_result_job_report_index(&index_path, &index)
            .expect("job report index should persist");
        let loaded = load_execution_result_job_report_index(&index_path)
            .expect("job report index should reload after persist");

        assert_eq!(loaded, index);
    }

    #[test]
    fn execution_result_job_report_index_persisted_json_schema_stays_stable() {
        let directory = tempdir().expect("tempdir should be created");
        let index_path = directory
            .path()
            .join("execution-result-job-report-index-schema.json");
        let report_a_path = directory.path().join("report-a.json");
        let report_b_path = directory.path().join("report-b.json");
        let report_a = sample_execution_result_job_report();
        let report_b = sample_execution_result_job_report_latest_only();

        register_execution_result_job_report_in_index(&index_path, &report_a_path, &report_a)
            .expect("first report should register");
        register_execution_result_job_report_in_index(&index_path, &report_b_path, &report_b)
            .expect("second report should register");

        let persisted = read_json_value(&index_path);
        assert_object_keys(&persisted, &["index_version", "entries"]);
        let entries = persisted["entries"]
            .as_array()
            .expect("report index entries should be an array");
        assert_eq!(entries.len(), 2);
        assert_object_keys(
            &entries[0],
            &[
                "ordinal",
                "report_file_path",
                "job_spec_id",
                "source_run_request_id",
                "source_handoff_bundle_id",
                "export_name",
                "selection_mode",
                "expected_entry_count",
                "source_provenance_hash",
            ],
        );
        assert_eq!(
            entries[0]["selection_mode"],
            Value::String("full_history".to_string())
        );
        assert_eq!(
            entries[1]["selection_mode"],
            Value::String("latest_only".to_string())
        );

        let loaded = load_execution_result_job_report_index(&index_path)
            .expect("registered report index should reload");
        assert_eq!(loaded.entries.len(), 2);
        assert_eq!(loaded.entries[0].job_spec_id, report_a.job_spec_id);
        assert_eq!(loaded.entries[1].job_spec_id, report_b.job_spec_id);
        assert_eq!(
            serde_json::to_value(&loaded).expect("loaded report index should convert to json"),
            persisted
        );
    }

    #[test]
    fn execution_result_job_report_index_load_rejects_unknown_fields_in_persisted_json() {
        let directory = tempdir().expect("tempdir should be created");
        let index_path = directory
            .path()
            .join("execution-result-job-report-index-schema-invalid.json");
        let index = sample_execution_result_job_report_index();

        persist_execution_result_job_report_index(&index_path, &index)
            .expect("report index should persist");

        let mut top_level_unknown = read_json_value(&index_path);
        top_level_unknown
            .as_object_mut()
            .expect("report index should be an object")
            .insert(
                "unexpected_top_level".to_string(),
                Value::String("drift".to_string()),
            );
        write_json_value(&index_path, &top_level_unknown);
        let top_level_error = load_execution_result_job_report_index(&index_path)
            .expect_err("unknown report index top-level field should be rejected");
        assert!(
            top_level_error.to_string().contains("unknown field"),
            "unexpected error: {top_level_error}"
        );

        persist_execution_result_job_report_index(&index_path, &index)
            .expect("report index should repersist cleanly");
        let mut nested_unknown = read_json_value(&index_path);
        nested_unknown["entries"][0]
            .as_object_mut()
            .expect("report index entry should be an object")
            .insert(
                "unexpected_entry_field".to_string(),
                Value::String("drift".to_string()),
            );
        write_json_value(&index_path, &nested_unknown);
        let nested_error = load_execution_result_job_report_index(&index_path)
            .expect_err("unknown report index entry field should be rejected");
        assert!(
            nested_error.to_string().contains("unknown field"),
            "unexpected error: {nested_error}"
        );
    }

    #[test]
    fn register_execution_result_job_report_in_index_appends_in_order() {
        let directory = tempdir().expect("tempdir should be created");
        let index_path = directory
            .path()
            .join("execution-result-job-report-index.json");
        let report_a_path = directory.path().join("execution-result-job-report-a.json");
        let report_b_path = directory.path().join("execution-result-job-report-b.json");
        let report_a = sample_execution_result_job_report();
        let report_b = sample_execution_result_job_report_latest_only();

        let entry_a =
            register_execution_result_job_report_in_index(&index_path, &report_a_path, &report_a)
                .expect("first report should register");
        let entry_b =
            register_execution_result_job_report_in_index(&index_path, &report_b_path, &report_b)
                .expect("second report should register");

        assert_eq!(entry_a.ordinal, 0);
        assert_eq!(entry_b.ordinal, 1);

        let loaded = load_execution_result_job_report_index(&index_path)
            .expect("registered index should reload");
        assert_eq!(loaded.entries, vec![entry_a, entry_b]);
    }

    #[test]
    fn register_execution_result_job_report_in_index_rejects_duplicate_report_path() {
        let directory = tempdir().expect("tempdir should be created");
        let index_path = directory
            .path()
            .join("execution-result-job-report-index.json");
        let report_path = directory.path().join("execution-result-job-report.json");
        let report_a = sample_execution_result_job_report();
        let report_b = sample_execution_result_job_report_latest_only();

        register_execution_result_job_report_in_index(&index_path, &report_path, &report_a)
            .expect("first report should register");
        let error =
            register_execution_result_job_report_in_index(&index_path, &report_path, &report_b)
                .expect_err("duplicate report path should be rejected");

        assert!(
            error
                .to_string()
                .contains("duplicate execution result job report path"),
            "unexpected error: {error}"
        );
    }

    #[test]
    fn register_execution_result_job_report_in_index_rejects_duplicate_job_spec_id() {
        let directory = tempdir().expect("tempdir should be created");
        let index_path = directory
            .path()
            .join("execution-result-job-report-index.json");
        let report_a_path = directory.path().join("execution-result-job-report-a.json");
        let report_b_path = directory.path().join("execution-result-job-report-b.json");
        let report_a = sample_execution_result_job_report();
        let mut report_b = sample_execution_result_job_report_latest_only();
        report_b.job_spec_id = report_a.job_spec_id.clone();

        register_execution_result_job_report_in_index(&index_path, &report_a_path, &report_a)
            .expect("first report should register");
        let error =
            register_execution_result_job_report_in_index(&index_path, &report_b_path, &report_b)
                .expect_err("duplicate job spec id should be rejected");

        assert!(
            error
                .to_string()
                .contains("duplicate execution result job spec id"),
            "unexpected error: {error}"
        );
    }

    #[test]
    fn register_execution_result_job_report_in_index_supports_latest_only_and_full_history_reports()
    {
        let directory = tempdir().expect("tempdir should be created");
        let index_path = directory
            .path()
            .join("execution-result-job-report-index.json");
        let report_a_path = directory.path().join("execution-result-job-report-a.json");
        let report_b_path = directory.path().join("execution-result-job-report-b.json");

        register_execution_result_job_report_in_index(
            &index_path,
            &report_a_path,
            &sample_execution_result_job_report(),
        )
        .expect("full-history report should register");
        register_execution_result_job_report_in_index(
            &index_path,
            &report_b_path,
            &sample_execution_result_job_report_latest_only(),
        )
        .expect("latest-only report should register");

        let loaded = load_execution_result_job_report_index(&index_path)
            .expect("mixed selection-mode index should reload");

        assert_eq!(loaded.entries.len(), 2);
        assert_eq!(
            loaded.entries[0].selection_mode,
            ExecutionResultSelectionMode::FullHistory
        );
        assert_eq!(
            loaded.entries[1].selection_mode,
            ExecutionResultSelectionMode::LatestOnly
        );
    }

    #[test]
    fn load_execution_result_job_report_index_validates_cleanly() {
        let directory = tempdir().expect("tempdir should be created");
        let index_path = directory
            .path()
            .join("execution-result-job-report-index.json");
        let index = sample_execution_result_job_report_index();
        let encoded = serde_json::to_string_pretty(&index).expect("valid index should serialize");
        fs::write(&index_path, encoded).expect("valid index should be written");

        let loaded = load_execution_result_job_report_index(&index_path)
            .expect("valid persisted index should load");

        assert_eq!(loaded, index);
    }

    #[test]
    fn find_execution_result_job_report_index_entry_by_job_spec_id_returns_matching_entry() {
        let index = sample_execution_result_job_report_index();

        let entry = find_execution_result_job_report_index_entry_by_job_spec_id(
            &index,
            "job-spec-latest-only",
        )
        .expect("job spec id should be present in index");

        assert_eq!(entry, &index.entries[1]);
    }

    #[test]
    fn find_execution_result_job_report_index_entry_by_report_path_returns_matching_entry() {
        let index = sample_execution_result_job_report_index();

        let entry = find_execution_result_job_report_index_entry_by_report_path(
            &index,
            r"D:\reports\execution-result-job-report-a.json",
        )
        .expect("report path should be present in index");

        assert_eq!(entry, &index.entries[0]);
    }

    #[test]
    fn find_execution_result_job_report_index_entry_by_job_spec_id_returns_none_when_missing() {
        let index = sample_execution_result_job_report_index();

        let entry =
            find_execution_result_job_report_index_entry_by_job_spec_id(&index, "missing-job-spec");

        assert!(entry.is_none(), "missing job spec id should not resolve");
    }

    #[test]
    fn select_execution_result_job_report_index_entries_filters_by_job_spec_id() {
        let index = sample_execution_result_job_report_index();
        let query = ExecutionResultJobReportIndexQuery {
            job_spec_id: Some("job-spec-latest-only".to_string()),
            ..ExecutionResultJobReportIndexQuery::default()
        };

        let selected = select_execution_result_job_report_index_entries(&index, &query)
            .expect("job spec id query should select deterministically");

        assert_eq!(selected, vec![&index.entries[1]]);
    }

    #[test]
    fn select_execution_result_job_report_index_entries_filters_by_report_file_path() {
        let index = sample_execution_result_job_report_index();
        let query = ExecutionResultJobReportIndexQuery {
            report_file_path: Some(r"D:\reports\execution-result-job-report-a.json".to_string()),
            ..ExecutionResultJobReportIndexQuery::default()
        };

        let selected = select_execution_result_job_report_index_entries(&index, &query)
            .expect("report path query should select deterministically");

        assert_eq!(selected, vec![&index.entries[0]]);
    }

    #[test]
    fn select_execution_result_job_report_index_entries_filters_by_export_name_and_selection_mode()
    {
        let index = sample_queryable_execution_result_job_report_index();
        let query = ExecutionResultJobReportIndexQuery {
            export_name: Some("restore-stage-shared".to_string()),
            selection_mode: Some(ExecutionResultSelectionMode::LatestOnly),
            ..ExecutionResultJobReportIndexQuery::default()
        };

        let selected = select_execution_result_job_report_index_entries(&index, &query)
            .expect("export name and selection mode query should select deterministically");

        assert_eq!(selected, vec![&index.entries[1]]);
    }

    #[test]
    fn select_execution_result_job_report_index_entries_preserves_index_order() {
        let index = sample_queryable_execution_result_job_report_index();
        let query = ExecutionResultJobReportIndexQuery {
            export_name: Some("restore-stage-shared".to_string()),
            ..ExecutionResultJobReportIndexQuery::default()
        };

        let selected = select_execution_result_job_report_index_entries(&index, &query)
            .expect("shared export query should preserve original index order");

        assert_eq!(
            selected,
            vec![&index.entries[0], &index.entries[1], &index.entries[2]]
        );
    }

    #[test]
    fn latest_execution_result_job_report_index_entry_returns_last_matching_entry() {
        let index = sample_queryable_execution_result_job_report_index();
        let query = ExecutionResultJobReportIndexQuery {
            export_name: Some("restore-stage-shared".to_string()),
            ..ExecutionResultJobReportIndexQuery::default()
        };

        let selected = latest_execution_result_job_report_index_entry(&index, &query)
            .expect("latest query should validate");

        assert_eq!(selected, Some(&index.entries[2]));
    }

    #[test]
    fn query_execution_result_job_report_index_can_reduce_to_latest_only_entry() {
        let index = sample_queryable_execution_result_job_report_index();
        let query = ExecutionResultJobReportIndexQuery {
            export_name: Some("restore-stage-shared".to_string()),
            latest_only: true,
            ..ExecutionResultJobReportIndexQuery::default()
        };

        let summary = query_execution_result_job_report_index(&index, &query)
            .expect("latest-only query should produce summary");

        assert_eq!(summary.query, query);
        assert_eq!(summary.selected_entry_count, 1);
        assert_eq!(summary.selected_entries, vec![index.entries[2].clone()]);
    }

    #[test]
    fn load_and_query_execution_result_job_report_index_matches_explicit_load_and_select_path() {
        let directory = tempdir().expect("tempdir should be created");
        let index_path = directory
            .path()
            .join("execution-result-job-report-index.json");
        let index = sample_queryable_execution_result_job_report_index();
        let query = ExecutionResultJobReportIndexQuery {
            source_run_request_id: Some("run-request-shared".to_string()),
            source_handoff_bundle_id: Some("handoff-shared".to_string()),
            source_provenance_hash: Some("provenance-beta".to_string()),
            ..ExecutionResultJobReportIndexQuery::default()
        };

        persist_execution_result_job_report_index(&index_path, &index)
            .expect("queryable index should persist");
        let explicitly_loaded = load_execution_result_job_report_index(&index_path)
            .expect("queryable index should load explicitly");
        let explicit_summary = query_execution_result_job_report_index(&explicitly_loaded, &query)
            .expect("explicit load plus query should succeed");
        let convenience_summary =
            load_and_query_execution_result_job_report_index(&index_path, &query)
                .expect("convenience load plus query should succeed");

        assert_eq!(convenience_summary, explicit_summary);
        assert_eq!(
            convenience_summary.selected_entries,
            vec![index.entries[1].clone()]
        );
    }

    #[test]
    fn load_selected_execution_result_job_reports_preserves_selected_entry_order() {
        let (_directory, index_path, reports) =
            persist_sample_execution_result_job_reports_with_index();
        let loaded_index = load_execution_result_job_report_index(&index_path)
            .expect("persisted index should reload for selected-entry loading");
        let selected_entries = vec![
            loaded_index.entries[2].clone(),
            loaded_index.entries[0].clone(),
            loaded_index.entries[1].clone(),
        ];

        let loaded_reports = load_selected_execution_result_job_reports(&selected_entries)
            .expect("selected reports should load in provided order");

        assert_eq!(
            loaded_reports,
            vec![reports[2].clone(), reports[0].clone(), reports[1].clone()]
        );
    }

    #[test]
    fn load_and_query_execution_result_job_reports_matches_explicit_index_query_and_load_path() {
        let (_directory, index_path, _reports) =
            persist_sample_execution_result_job_reports_with_index();
        let query = ExecutionResultJobReportIndexQuery {
            source_run_request_id: Some("run-request-shared".to_string()),
            source_handoff_bundle_id: Some("handoff-shared".to_string()),
            export_name: Some("restore-stage-shared".to_string()),
            ..ExecutionResultJobReportIndexQuery::default()
        };
        let explicit_index = load_execution_result_job_report_index(&index_path)
            .expect("persisted index should load explicitly");
        let explicit_selection = query_execution_result_job_report_index(&explicit_index, &query)
            .expect("explicit index query should succeed");
        let explicit_loaded =
            load_selected_execution_result_job_reports(&explicit_selection.selected_entries)
                .expect("explicitly selected reports should load");

        let convenience_loaded = load_and_query_execution_result_job_reports(&index_path, &query)
            .expect("convenience query-and-load should succeed");

        assert_eq!(convenience_loaded, explicit_loaded);
    }

    #[test]
    fn load_and_query_execution_result_job_reports_latest_only_returns_exactly_one_report() {
        let (_directory, index_path, reports) =
            persist_sample_execution_result_job_reports_with_index();
        let query = ExecutionResultJobReportIndexQuery {
            source_run_request_id: Some("run-request-shared".to_string()),
            source_handoff_bundle_id: Some("handoff-shared".to_string()),
            export_name: Some("restore-stage-shared".to_string()),
            latest_only: true,
            ..ExecutionResultJobReportIndexQuery::default()
        };

        let loaded_reports = load_and_query_execution_result_job_reports(&index_path, &query)
            .expect("latest-only report query should load");

        assert_eq!(loaded_reports, vec![reports[2].clone()]);
        assert_eq!(loaded_reports.len(), 1);
        validate_execution_result_job_report(&loaded_reports[0])
            .expect("latest-only loaded report should remain valid");
    }

    #[test]
    fn load_and_query_execution_result_job_reports_full_history_returns_all_matches_in_index_order()
    {
        let (_directory, index_path, reports) =
            persist_sample_execution_result_job_reports_with_index();
        let query = ExecutionResultJobReportIndexQuery {
            source_run_request_id: Some("run-request-shared".to_string()),
            source_handoff_bundle_id: Some("handoff-shared".to_string()),
            export_name: Some("restore-stage-shared".to_string()),
            ..ExecutionResultJobReportIndexQuery::default()
        };

        let loaded_reports = load_and_query_execution_result_job_reports(&index_path, &query)
            .expect("full-history report query should load");

        assert_eq!(loaded_reports, reports);
        for report in &loaded_reports {
            validate_execution_result_job_report(report)
                .expect("full-history loaded reports should remain valid");
        }
    }

    #[test]
    fn load_and_query_execution_result_job_reports_matches_explicit_persist_and_indexed_load_path_without_field_drift()
     {
        let (_directory, index_path, reports) =
            persist_sample_execution_result_job_reports_with_index();
        let query = ExecutionResultJobReportIndexQuery {
            source_run_request_id: Some("run-request-shared".to_string()),
            source_handoff_bundle_id: Some("handoff-shared".to_string()),
            export_name: Some("restore-stage-shared".to_string()),
            ..ExecutionResultJobReportIndexQuery::default()
        };

        let loaded_reports = load_and_query_execution_result_job_reports(&index_path, &query)
            .expect("query-and-load path should reload persisted reports");

        assert_eq!(loaded_reports, reports);
        assert_eq!(
            loaded_reports[0].source_provenance_hash,
            reports[0].source_provenance_hash
        );
        assert_eq!(loaded_reports[1].selection_mode, reports[1].selection_mode);
        assert_eq!(loaded_reports[2].entries, reports[2].entries);
    }

    #[test]
    fn load_indexed_execution_result_job_report_returns_exact_persisted_report() {
        let directory = tempdir().expect("tempdir should be created");
        let report_path = directory.path().join("indexed-report.json");
        let index_path = directory.path().join("indexed-report-index.json");
        let report = sample_execution_result_job_report();

        persist_execution_result_job_report(&report_path, &report)
            .expect("report should persist before indexed load");
        register_execution_result_job_report_in_index(&index_path, &report_path, &report)
            .expect("report should register before indexed load");

        let loaded = load_indexed_execution_result_job_report(&index_path, &report.job_spec_id)
            .expect("indexed report should load by job spec id");

        assert_eq!(loaded, report);
    }

    #[test]
    fn load_indexed_execution_result_job_report_supports_latest_only_selection() {
        let directory = tempdir().expect("tempdir should be created");
        let report_path = directory.path().join("indexed-latest-only-report.json");
        let index_path = directory.path().join("indexed-latest-only-index.json");
        let report = sample_execution_result_job_report_latest_only();

        persist_execution_result_job_report(&report_path, &report)
            .expect("latest-only report should persist before indexed load");
        register_execution_result_job_report_in_index(&index_path, &report_path, &report)
            .expect("latest-only report should register before indexed load");

        let loaded = load_indexed_execution_result_job_report(&index_path, &report.job_spec_id)
            .expect("latest-only indexed report should load");

        assert_eq!(loaded, report);
        assert_eq!(
            loaded.selection_mode,
            ExecutionResultSelectionMode::LatestOnly
        );
    }

    #[test]
    fn load_indexed_execution_result_job_report_supports_full_history_selection() {
        let directory = tempdir().expect("tempdir should be created");
        let report_path = directory.path().join("indexed-full-history-report.json");
        let index_path = directory.path().join("indexed-full-history-index.json");
        let report = sample_execution_result_job_report();

        persist_execution_result_job_report(&report_path, &report)
            .expect("full-history report should persist before indexed load");
        register_execution_result_job_report_in_index(&index_path, &report_path, &report)
            .expect("full-history report should register before indexed load");

        let loaded = load_indexed_execution_result_job_report(&index_path, &report.job_spec_id)
            .expect("full-history indexed report should load");

        assert_eq!(loaded, report);
        assert_eq!(
            loaded.selection_mode,
            ExecutionResultSelectionMode::FullHistory
        );
    }

    #[test]
    fn load_indexed_execution_result_job_report_matches_explicit_persist_and_load_pipeline() {
        let directory = tempdir().expect("tempdir should be created");
        let report_path = directory.path().join("indexed-drift-report.json");
        let index_path = directory.path().join("indexed-drift-index.json");
        let report = sample_execution_result_job_report_latest_only();

        persist_execution_result_job_report(&report_path, &report)
            .expect("report should persist before indexed comparison");
        register_execution_result_job_report_in_index(&index_path, &report_path, &report)
            .expect("report should register before indexed comparison");

        let explicit_loaded = load_execution_result_job_report(&report_path)
            .expect("explicit persisted report should reload");
        let indexed_loaded =
            load_indexed_execution_result_job_report(&index_path, &report.job_spec_id)
                .expect("indexed report should reload");

        assert_eq!(indexed_loaded, explicit_loaded);
        assert_eq!(indexed_loaded, report);
    }

    #[test]
    fn load_indexed_execution_result_job_report_collection_summary_returns_exact_persisted_summary()
    {
        let (_directory, index_path, latest_only_summary_path, latest_only_summary, _, _) =
            persist_sample_execution_result_job_report_collection_summaries_with_index();

        let loaded = load_indexed_execution_result_job_report_collection_summary(
            &index_path,
            &latest_only_summary_path.to_string_lossy(),
        )
        .expect("indexed summary should load by summary file path");

        assert_eq!(loaded, latest_only_summary);
    }

    #[test]
    fn load_indexed_execution_result_job_report_collection_summary_supports_latest_only_selection()
    {
        let (_directory, index_path, latest_only_summary_path, latest_only_summary, _, _) =
            persist_sample_execution_result_job_report_collection_summaries_with_index();

        let loaded = load_indexed_execution_result_job_report_collection_summary(
            &index_path,
            &latest_only_summary_path.to_string_lossy(),
        )
        .expect("latest-only indexed summary should load");

        assert_eq!(loaded, latest_only_summary);
        assert_eq!(
            loaded.selection_modes,
            vec![ExecutionResultSelectionMode::LatestOnly]
        );
    }

    #[test]
    fn load_indexed_execution_result_job_report_collection_summary_supports_full_history_selection()
    {
        let (_directory, index_path, _, _, full_history_summary_path, full_history_summary) =
            persist_sample_execution_result_job_report_collection_summaries_with_index();

        let loaded = load_indexed_execution_result_job_report_collection_summary(
            &index_path,
            &full_history_summary_path.to_string_lossy(),
        )
        .expect("full-history indexed summary should load");

        assert_eq!(loaded, full_history_summary);
        assert_eq!(
            loaded.selection_modes,
            vec![
                ExecutionResultSelectionMode::FullHistory,
                ExecutionResultSelectionMode::LatestOnly,
            ]
        );
    }

    #[test]
    fn load_indexed_execution_result_job_report_collection_summary_matches_explicit_persist_and_load_pipeline()
     {
        let (_directory, index_path, latest_only_summary_path, latest_only_summary, _, _) =
            persist_sample_execution_result_job_report_collection_summaries_with_index();

        let explicit_loaded =
            load_execution_result_job_report_collection_summary(&latest_only_summary_path)
                .expect("explicit persisted summary should reload");
        let indexed_loaded = load_indexed_execution_result_job_report_collection_summary(
            &index_path,
            &latest_only_summary_path.to_string_lossy(),
        )
        .expect("indexed summary should reload");

        assert_eq!(indexed_loaded, explicit_loaded);
        assert_eq!(indexed_loaded, latest_only_summary);
    }

    #[test]
    fn persist_register_and_index_load_execution_result_job_report_collection_summary_matches_explicit_pipeline()
     {
        let directory = tempdir().expect("tempdir should be created");
        let summary = sample_execution_result_job_report_collection_summary_latest_only();
        let explicit_summary_path = directory.path().join("explicit-summary.json");
        let explicit_index_path = directory.path().join("explicit-summary-index.json");
        let helper_summary_path = directory.path().join("helper-summary.json");
        let helper_index_path = directory.path().join("helper-summary-index.json");

        persist_execution_result_job_report_collection_summary(&explicit_summary_path, &summary)
            .expect("explicit summary persist should succeed");
        register_execution_result_job_report_collection_summary_in_index(
            &explicit_index_path,
            &explicit_summary_path,
            &summary,
        )
        .expect("explicit summary register should succeed");
        let explicit_indexed_loaded = load_indexed_execution_result_job_report_collection_summary(
            &explicit_index_path,
            &path_to_owned_string(&explicit_summary_path)
                .expect("explicit summary path should serialize"),
        )
        .expect("explicit indexed-load should succeed");

        let helper_indexed_loaded =
            persist_register_and_index_load_execution_result_job_report_collection_summary(
                &summary,
                &helper_summary_path,
                &helper_index_path,
            )
            .expect("helper summary pipeline should succeed");

        assert_eq!(helper_indexed_loaded, explicit_indexed_loaded);
        assert_eq!(helper_indexed_loaded, summary);
    }

    #[test]
    fn persist_register_and_index_load_execution_result_job_report_collection_summary_latest_only_round_trips_exactly()
     {
        let directory = tempdir().expect("tempdir should be created");
        let summary = sample_execution_result_job_report_collection_summary_latest_only();
        let summary_path = directory.path().join("latest-only-summary.json");
        let index_path = directory.path().join("latest-only-summary-index.json");

        let indexed_loaded =
            persist_register_and_index_load_execution_result_job_report_collection_summary(
                &summary,
                &summary_path,
                &index_path,
            )
            .expect("latest-only helper round-trip should succeed");
        let reloaded = load_indexed_execution_result_job_report_collection_summary(
            &index_path,
            &summary_path.to_string_lossy(),
        )
        .expect("latest-only indexed reload should succeed");

        assert_eq!(indexed_loaded, summary);
        assert_eq!(reloaded, summary);
        assert_eq!(reloaded, indexed_loaded);
    }

    #[test]
    fn persist_register_and_index_load_execution_result_job_report_collection_summary_full_history_round_trips_exactly()
     {
        let directory = tempdir().expect("tempdir should be created");
        let summary =
            sample_execution_result_job_report_collection_summary_full_history_multi_report();
        let summary_path = directory.path().join("full-history-summary.json");
        let index_path = directory.path().join("full-history-summary-index.json");

        let indexed_loaded =
            persist_register_and_index_load_execution_result_job_report_collection_summary(
                &summary,
                &summary_path,
                &index_path,
            )
            .expect("full-history helper round-trip should succeed");
        let reloaded = load_indexed_execution_result_job_report_collection_summary(
            &index_path,
            &summary_path.to_string_lossy(),
        )
        .expect("full-history indexed reload should succeed");

        assert_eq!(indexed_loaded, summary);
        assert_eq!(reloaded, summary);
        assert_eq!(reloaded, indexed_loaded);
    }

    #[test]
    fn persist_register_and_index_load_execution_result_job_report_collection_summary_reloads_without_field_drift_vs_explicit_pipeline()
     {
        let directory = tempdir().expect("tempdir should be created");
        let summary =
            sample_execution_result_job_report_collection_summary_full_history_multi_report();
        let explicit_summary_path = directory.path().join("drift-explicit-summary.json");
        let explicit_index_path = directory.path().join("drift-explicit-summary-index.json");
        let helper_summary_path = directory.path().join("drift-helper-summary.json");
        let helper_index_path = directory.path().join("drift-helper-summary-index.json");

        persist_execution_result_job_report_collection_summary(&explicit_summary_path, &summary)
            .expect("explicit summary persist should succeed");
        register_execution_result_job_report_collection_summary_in_index(
            &explicit_index_path,
            &explicit_summary_path,
            &summary,
        )
        .expect("explicit summary register should succeed");
        let explicit_indexed_loaded = load_indexed_execution_result_job_report_collection_summary(
            &explicit_index_path,
            &path_to_owned_string(&explicit_summary_path)
                .expect("explicit summary path should serialize"),
        )
        .expect("explicit indexed-load should succeed");

        let helper_indexed_loaded =
            persist_register_and_index_load_execution_result_job_report_collection_summary(
                &summary,
                &helper_summary_path,
                &helper_index_path,
            )
            .expect("helper summary pipeline should succeed");
        let helper_reloaded = load_indexed_execution_result_job_report_collection_summary(
            &helper_index_path,
            &helper_summary_path.to_string_lossy(),
        )
        .expect("helper indexed reload should succeed");

        assert_eq!(helper_indexed_loaded, explicit_indexed_loaded);
        assert_eq!(helper_reloaded, explicit_indexed_loaded);
        assert_eq!(helper_reloaded, helper_indexed_loaded);
    }

    #[test]
    fn stage47_compatibility_wrapper_parity_cluster_matches_explicit_canonical_compositions() {
        {
            let (directory, _) = sample_execution_ledger_history();
            let bundle_dir = directory.path().join("bundle");
            let ledger_query = LedgerSelectionQuery::default();
            let explicit_report_path = directory
                .path()
                .join("stage47-register-explicit-report.json");
            let explicit_index_path = directory
                .path()
                .join("stage47-register-explicit-report-index.json");
            let wrapper_report_path = directory
                .path()
                .join("stage47-register-wrapper-report.json");
            let wrapper_index_path = directory
                .path()
                .join("stage47-register-wrapper-report-index.json");

            let explicit =
                stage47_explicit_query_stub_execute_persist_load_and_register_execution_result_job_report(
                    &bundle_dir,
                    &ledger_query,
                    "handoff-stage47-register",
                    "run-request-stage47-register",
                    "job-spec-stage47-register",
                    ExecutionResultSelectionMode::FullHistory,
                    &explicit_report_path,
                    &explicit_index_path,
                )
                .expect("stage47 explicit persist/load/register pipeline should succeed");
            let wrapper = query_stub_execute_persist_load_and_register_execution_result_job_report(
                &bundle_dir,
                &ledger_query,
                "handoff-stage47-register",
                "run-request-stage47-register",
                "job-spec-stage47-register",
                ExecutionResultSelectionMode::FullHistory,
                &wrapper_report_path,
                &wrapper_index_path,
            )
            .expect("stage47 persist/load/register wrapper should succeed");

            assert_eq!(wrapper, explicit);
            assert_execution_result_job_report_index_semantically_equal(
                &load_execution_result_job_report_index(&explicit_index_path)
                    .expect("stage47 explicit report index should reload"),
                &load_execution_result_job_report_index(&wrapper_index_path)
                    .expect("stage47 wrapper report index should reload"),
            );
        }

        {
            let (directory, _) = sample_execution_ledger_history();
            let bundle_dir = directory.path().join("bundle");
            let ledger_query = LedgerSelectionQuery {
                request_id: Some("request-shared".to_string()),
                ..LedgerSelectionQuery::default()
            };
            let handoff_bundle_id = "handoff-stage47-query-load-shared";
            let run_request_id = "run-request-stage47-query-load-shared";
            let report_index_query = ExecutionResultJobReportIndexQuery {
                source_run_request_id: Some(run_request_id.to_string()),
                source_handoff_bundle_id: Some(handoff_bundle_id.to_string()),
                ..ExecutionResultJobReportIndexQuery::default()
            };
            let explicit_index_path = directory
                .path()
                .join("stage47-query-load-explicit-report-index.json");
            let wrapper_index_path = directory
                .path()
                .join("stage47-query-load-wrapper-report-index.json");

            stage47_seed_registered_report(
                &bundle_dir,
                &ledger_query,
                handoff_bundle_id,
                run_request_id,
                "job-spec-stage47-query-load-seed",
                ExecutionResultSelectionMode::FullHistory,
                &directory
                    .path()
                    .join("stage47-query-load-explicit-seed-report.json"),
                &explicit_index_path,
            );
            stage47_seed_registered_report(
                &bundle_dir,
                &ledger_query,
                handoff_bundle_id,
                run_request_id,
                "job-spec-stage47-query-load-seed",
                ExecutionResultSelectionMode::FullHistory,
                &directory
                    .path()
                    .join("stage47-query-load-wrapper-seed-report.json"),
                &wrapper_index_path,
            );

            let explicit =
                stage47_explicit_query_stub_execute_persist_load_register_query_and_load_execution_result_job_reports(
                    &bundle_dir,
                    &ledger_query,
                    handoff_bundle_id,
                    run_request_id,
                    "job-spec-stage47-query-load-target",
                    ExecutionResultSelectionMode::LatestOnly,
                    &directory.path().join("stage47-query-load-explicit-report.json"),
                    &explicit_index_path,
                    &report_index_query,
                )
                .expect("stage47 explicit query/load report pipeline should succeed");
            let wrapper =
                query_stub_execute_persist_load_register_query_and_load_execution_result_job_reports(
                    &bundle_dir,
                    &ledger_query,
                    handoff_bundle_id,
                    run_request_id,
                    "job-spec-stage47-query-load-target",
                    ExecutionResultSelectionMode::LatestOnly,
                    directory.path().join("stage47-query-load-wrapper-report.json"),
                    &wrapper_index_path,
                    &report_index_query,
                )
                .expect("stage47 query/load report wrapper should succeed");

            assert_eq!(wrapper, explicit);
            assert_execution_result_job_report_index_semantically_equal(
                &load_execution_result_job_report_index(&explicit_index_path)
                    .expect("stage47 explicit query/load report index should reload"),
                &load_execution_result_job_report_index(&wrapper_index_path)
                    .expect("stage47 wrapper query/load report index should reload"),
            );
        }

        {
            let (directory, _) = sample_execution_ledger_history();
            let bundle_dir = directory.path().join("bundle");
            let ledger_query = LedgerSelectionQuery {
                request_id: Some("request-shared".to_string()),
                ..LedgerSelectionQuery::default()
            };
            let handoff_bundle_id = "handoff-stage47-summary-shared";
            let run_request_id = "run-request-stage47-summary-shared";
            let report_index_query = ExecutionResultJobReportIndexQuery {
                source_run_request_id: Some(run_request_id.to_string()),
                source_handoff_bundle_id: Some(handoff_bundle_id.to_string()),
                ..ExecutionResultJobReportIndexQuery::default()
            };
            let explicit_report_index_path = directory
                .path()
                .join("stage47-summary-explicit-report-index.json");
            let explicit_summary_index_path = directory
                .path()
                .join("stage47-summary-explicit-summary-index.json");
            let wrapper_report_index_path = directory
                .path()
                .join("stage47-summary-wrapper-report-index.json");
            let wrapper_summary_index_path = directory
                .path()
                .join("stage47-summary-wrapper-summary-index.json");

            stage47_seed_registered_report(
                &bundle_dir,
                &ledger_query,
                handoff_bundle_id,
                run_request_id,
                "job-spec-stage47-summary-seed",
                ExecutionResultSelectionMode::FullHistory,
                &directory
                    .path()
                    .join("stage47-summary-explicit-seed-report.json"),
                &explicit_report_index_path,
            );
            stage47_seed_registered_report(
                &bundle_dir,
                &ledger_query,
                handoff_bundle_id,
                run_request_id,
                "job-spec-stage47-summary-seed",
                ExecutionResultSelectionMode::FullHistory,
                &directory
                    .path()
                    .join("stage47-summary-wrapper-seed-report.json"),
                &wrapper_report_index_path,
            );

            let explicit =
                stage47_explicit_query_stub_execute_register_report_and_index_load_summary(
                    &bundle_dir,
                    &ledger_query,
                    handoff_bundle_id,
                    run_request_id,
                    "job-spec-stage47-summary-target",
                    ExecutionResultSelectionMode::LatestOnly,
                    &directory
                        .path()
                        .join("stage47-summary-explicit-report.json"),
                    &explicit_report_index_path,
                    &report_index_query,
                    &explicit_summary_index_path,
                    &directory
                        .path()
                        .join("stage47-summary-explicit-summary.json"),
                )
                .expect("stage47 explicit summary index-load pipeline should succeed");
            let wrapper = query_stub_execute_register_report_and_index_load_summary(
                &bundle_dir,
                &ledger_query,
                handoff_bundle_id,
                run_request_id,
                "job-spec-stage47-summary-target",
                ExecutionResultSelectionMode::LatestOnly,
                directory.path().join("stage47-summary-wrapper-report.json"),
                &wrapper_report_index_path,
                &report_index_query,
                &wrapper_summary_index_path,
                directory
                    .path()
                    .join("stage47-summary-wrapper-summary.json"),
            )
            .expect("stage47 summary index-load wrapper should succeed");

            assert_eq!(wrapper, explicit);
            assert_execution_result_job_report_collection_summary_index_semantically_equal(
                &load_execution_result_job_report_collection_summary_index(
                    &explicit_summary_index_path,
                )
                .expect("stage47 explicit summary index should reload"),
                &load_execution_result_job_report_collection_summary_index(
                    &wrapper_summary_index_path,
                )
                .expect("stage47 wrapper summary index should reload"),
            );
        }
    }

    #[allow(clippy::too_many_arguments)]
    fn stage47_explicit_query_stub_execute_persist_load_and_register_execution_result_job_report(
        bundle_dir: &Path,
        query: &LedgerSelectionQuery,
        handoff_bundle_id: &str,
        run_request_id: &str,
        job_spec_id: &str,
        selection_mode: ExecutionResultSelectionMode,
        report_path: &Path,
        report_index_path: &Path,
    ) -> Result<ExecutionResultJobReport> {
        let report = query_and_stub_execute_execution_result_job_spec(
            bundle_dir,
            query,
            handoff_bundle_id.to_string(),
            run_request_id.to_string(),
            job_spec_id.to_string(),
            selection_mode,
        )?;
        persist_execution_result_job_report(report_path, &report)?;
        let loaded_report = load_execution_result_job_report(report_path)?;
        register_execution_result_job_report_in_index(
            report_index_path,
            report_path,
            &loaded_report,
        )?;
        Ok(loaded_report)
    }

    #[allow(clippy::too_many_arguments)]
    fn stage47_explicit_query_stub_execute_persist_load_register_query_and_load_execution_result_job_reports(
        bundle_dir: &Path,
        query: &LedgerSelectionQuery,
        handoff_bundle_id: &str,
        run_request_id: &str,
        job_spec_id: &str,
        selection_mode: ExecutionResultSelectionMode,
        report_path: &Path,
        report_index_path: &Path,
        report_index_query: &ExecutionResultJobReportIndexQuery,
    ) -> Result<Vec<ExecutionResultJobReport>> {
        stage47_explicit_query_stub_execute_persist_load_and_register_execution_result_job_report(
            bundle_dir,
            query,
            handoff_bundle_id,
            run_request_id,
            job_spec_id,
            selection_mode,
            report_path,
            report_index_path,
        )?;
        let selection_summary = load_and_query_execution_result_job_report_index(
            report_index_path,
            report_index_query,
        )?;
        load_selected_execution_result_job_reports(&selection_summary.selected_entries)
    }

    #[allow(clippy::too_many_arguments)]
    fn stage47_explicit_query_stub_execute_register_report_and_index_load_summary(
        bundle_dir: &Path,
        query: &LedgerSelectionQuery,
        handoff_bundle_id: &str,
        run_request_id: &str,
        job_spec_id: &str,
        selection_mode: ExecutionResultSelectionMode,
        report_path: &Path,
        report_index_path: &Path,
        report_index_query: &ExecutionResultJobReportIndexQuery,
        summary_index_path: &Path,
        output_summary_path: &Path,
    ) -> Result<ExecutionResultJobReportCollectionSummary> {
        let loaded_reports =
            stage47_explicit_query_stub_execute_persist_load_register_query_and_load_execution_result_job_reports(
                bundle_dir,
                query,
                handoff_bundle_id,
                run_request_id,
                job_spec_id,
                selection_mode,
                report_path,
                report_index_path,
                report_index_query,
            )?;
        let summary = summarize_execution_result_job_reports(&loaded_reports);
        persist_execution_result_job_report_collection_summary(output_summary_path, &summary)?;
        register_execution_result_job_report_collection_summary_in_index(
            summary_index_path,
            output_summary_path,
            &summary,
        )?;
        load_indexed_execution_result_job_report_collection_summary(
            summary_index_path,
            &stage47_owned_path(output_summary_path),
        )
    }

    #[allow(clippy::too_many_arguments)]
    fn stage47_seed_registered_report(
        bundle_dir: &Path,
        query: &LedgerSelectionQuery,
        handoff_bundle_id: &str,
        run_request_id: &str,
        job_spec_id: &str,
        selection_mode: ExecutionResultSelectionMode,
        report_path: &Path,
        report_index_path: &Path,
    ) {
        stage47_explicit_query_stub_execute_persist_load_and_register_execution_result_job_report(
            bundle_dir,
            query,
            handoff_bundle_id,
            run_request_id,
            job_spec_id,
            selection_mode,
            report_path,
            report_index_path,
        )
        .expect("stage47 seed report pipeline should succeed");
    }

    fn stage47_owned_path(path: &Path) -> String {
        path_to_owned_string(path).expect("stage47 path should serialize")
    }

    fn assert_execution_result_job_report_index_semantically_equal(
        explicit: &ExecutionResultJobReportIndex,
        wrapper: &ExecutionResultJobReportIndex,
    ) {
        assert_eq!(wrapper.index_version, explicit.index_version);
        assert_eq!(wrapper.entries.len(), explicit.entries.len());

        for (wrapper_entry, explicit_entry) in wrapper.entries.iter().zip(&explicit.entries) {
            assert_eq!(wrapper_entry.ordinal, explicit_entry.ordinal);
            assert_eq!(wrapper_entry.job_spec_id, explicit_entry.job_spec_id);
            assert_eq!(
                wrapper_entry.source_run_request_id,
                explicit_entry.source_run_request_id
            );
            assert_eq!(
                wrapper_entry.source_handoff_bundle_id,
                explicit_entry.source_handoff_bundle_id
            );
            assert_eq!(wrapper_entry.export_name, explicit_entry.export_name);
            assert_eq!(wrapper_entry.selection_mode, explicit_entry.selection_mode);
            assert_eq!(
                wrapper_entry.expected_entry_count,
                explicit_entry.expected_entry_count
            );
            assert_eq!(
                wrapper_entry.source_provenance_hash,
                explicit_entry.source_provenance_hash
            );
        }
    }

    fn assert_execution_result_job_report_collection_summary_index_semantically_equal(
        explicit: &ExecutionResultJobReportCollectionSummaryIndex,
        wrapper: &ExecutionResultJobReportCollectionSummaryIndex,
    ) {
        assert_eq!(wrapper.index_version, explicit.index_version);
        assert_eq!(wrapper.entries.len(), explicit.entries.len());

        for (wrapper_entry, explicit_entry) in wrapper.entries.iter().zip(&explicit.entries) {
            assert_eq!(wrapper_entry.ordinal, explicit_entry.ordinal);
            assert_eq!(wrapper_entry.report_count, explicit_entry.report_count);
            assert_eq!(
                wrapper_entry.total_entry_count,
                explicit_entry.total_entry_count
            );
            assert_eq!(wrapper_entry.job_spec_ids, explicit_entry.job_spec_ids);
            assert_eq!(wrapper_entry.export_names, explicit_entry.export_names);
            assert_eq!(
                wrapper_entry.selection_modes,
                explicit_entry.selection_modes
            );
            assert_eq!(
                wrapper_entry.source_run_request_ids,
                explicit_entry.source_run_request_ids
            );
            assert_eq!(
                wrapper_entry.source_handoff_bundle_ids,
                explicit_entry.source_handoff_bundle_ids
            );
        }
    }

    fn sample_execution_result_job_spec(
        selection_mode: ExecutionResultSelectionMode,
        entries: Vec<ExecutionResultJobSpecEntry>,
    ) -> ExecutionResultJobSpec {
        let export_name = match selection_mode {
            ExecutionResultSelectionMode::FullHistory => "restore-stage-2-full-history",
            ExecutionResultSelectionMode::LatestOnly => "restore-stage-2-latest-only",
        }
        .to_string();
        let source_provenance_hash =
            compute_job_spec_provenance_hash(&export_name, selection_mode, &entries)
                .expect("job spec provenance hash should compute");

        let job_spec = ExecutionResultJobSpec {
            job_spec_id: format!("job-spec-{}", entries.len()),
            source_run_request_id: "run-request-stage-2".to_string(),
            source_handoff_bundle_id: "handoff-stage-2".to_string(),
            export_name,
            selection_mode,
            expected_entry_count: entries.len(),
            source_provenance_hash,
            entries,
        };
        validate_execution_result_job_spec(&job_spec)
            .expect("sample job spec should satisfy executor contract");

        job_spec
    }

    fn sample_execution_result_job_spec_entry(
        ordinal: usize,
        result_id: &str,
        request_id: &str,
        plan_id: &str,
        status: ExecutionResultStatus,
        recorded_at_unix_ms: u64,
    ) -> ExecutionResultJobSpecEntry {
        ExecutionResultJobSpecEntry {
            ordinal,
            result_id: result_id.to_string(),
            request_id: request_id.to_string(),
            plan_id: plan_id.to_string(),
            status,
            recorded_at_unix_ms,
            selected_anchor_ids: vec![format!("anchor-{ordinal}")],
            selected_branch_ids: vec![format!("branch-{ordinal}")],
            detail: Some(format!("detail-{ordinal}")),
        }
    }

    fn sample_export_input(artifact_encoding: ExportEncoding) -> ExportBundleInput {
        ExportBundleInput {
            export_name: "restore-stage-1".to_string(),
            artifact_encoding,
            anchor_artifacts: vec![sample_anchor_artifact()],
            branch_artifacts: vec![sample_branch_artifact()],
            created_by_component: Some("unit-test".to_string()),
        }
    }

    fn sample_anchor_artifact() -> PersistedAnchorArtifact {
        PersistedAnchorArtifact::new(
            ArtifactHeader::for_kind(ArtifactKind::Anchor, ANCHOR_ARTIFACT_PRODUCER)
                .with_created_by_component("restore-stage-1")
                .with_metadata(Metadata::from([(
                    "source",
                    FieldValue::Text("manual".to_string()),
                )])),
            AnchorArtifactPayload {
                id: AnchorId::new("anchor-1"),
                replay_id: ReplayId::new("replay-1"),
                frame_index: FrameIndex::new(12),
                kind: AnchorKind::Manual,
                metadata: Metadata::from([("note", FieldValue::Text("seed".to_string()))]),
            },
        )
    }

    fn sample_branch_artifact() -> PersistedBranchArtifact {
        PersistedBranchArtifact::new(
            ArtifactHeader::for_kind(ArtifactKind::Branch, BRANCH_ARTIFACT_PRODUCER)
                .with_created_by_component("restore-stage-1")
                .with_metadata(Metadata::from([(
                    "source",
                    FieldValue::Text("manual".to_string()),
                )])),
            BranchArtifactPayload {
                id: BranchId::new("branch-1"),
                anchor_id: AnchorId::new("anchor-1"),
                origin: BranchOrigin::Manual,
                label: Some("keep".to_string()),
                actions: vec![ActionRecord {
                    action_key: "jump".to_string(),
                    fields: Metadata::from([("pressed", FieldValue::Boolean(true))]),
                }],
                legality_hint: Some(true),
                metadata: Metadata::from([("note", FieldValue::Text("seed".to_string()))]),
            },
        )
    }

    fn load_sample_consumer_export(output_dir: &Path) -> ConsumerExport {
        adapt_loaded_export_for_consumer(
            load_export_bundle(output_dir).expect("bundle should load for consumer export"),
        )
    }
}
