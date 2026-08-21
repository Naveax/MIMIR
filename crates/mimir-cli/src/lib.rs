use clap::{Parser, Subcommand};
use mimir_anchor::HintAnchorDetector;
use mimir_branch::BoundedManualBranchGenerator;
use mimir_config::{
    AnchorsConfig, BaseConfig, BranchingConfig, LabelingConfig, LoopBackend, LoopConfig,
    ScoringConfig,
};
use mimir_core::{MimirError, NamedComponent, Result, load_toml_file};
use mimir_score::WeightedSumScorer;
use mimir_sim_bridge::{
    DeterministicFakeBackend, SimBackend, SimulationCommand, SimulationRequest,
};
use mimir_skill::{LowercaseTrimCanonicalizer, SkillCanonicalizer};
use mimir_teacher::PassThroughTeacherSynthesizer;
use mimir_types::Metadata;
use serde::Serialize;
use std::ffi::OsString;
use std::path::PathBuf;

mod replay_compat;

#[cfg(test)]
mod vertical_slice;
#[cfg(test)]
mod vertical_slice_result;
#[cfg(test)]
mod vertical_slice_test_support;

#[derive(Debug, Parser)]
#[command(
    name = "mimir-cli",
    version,
    about = "Trustworthy scaffold CLI for MIMIR"
)]
pub struct Cli {
    #[command(subcommand)]
    pub command: Commands,
}

#[derive(Debug, Subcommand)]
pub enum Commands {
    Mine {
        #[arg(long, default_value = "configs/mimir.base.toml")]
        base: PathBuf,
        #[arg(long, default_value = "configs/anchors.toml")]
        anchors: PathBuf,
        #[arg(long, default_value = "configs/branching.toml")]
        branching: PathBuf,
        #[arg(long, default_value = "configs/scoring.toml")]
        scoring: PathBuf,
    },
    Label {
        #[arg(long, default_value = "configs/mimir.base.toml")]
        base: PathBuf,
        #[arg(long, default_value = "configs/labeling.toml")]
        labeling: PathBuf,
    },
    #[command(name = "build-library")]
    BuildLibrary {
        #[arg(long, default_value = "configs/mimir.base.toml")]
        base: PathBuf,
        #[arg(long, default_value = "configs/labeling.toml")]
        labeling: PathBuf,
    },
    #[command(name = "export-bc")]
    ExportBc {
        #[arg(long, default_value = "configs/mimir.base.toml")]
        base: PathBuf,
    },
    #[command(name = "export-dagger")]
    ExportDagger {
        #[arg(long, default_value = "configs/mimir.base.toml")]
        base: PathBuf,
    },
    #[command(name = "replay-compat-matrix")]
    ReplayCompatMatrix {
        #[arg(long, default_value = "test_corpus/largest_100")]
        corpus_root: PathBuf,
        #[arg(long, default_value = "artifacts/replay_compatibility_matrix.jsonl")]
        output: PathBuf,
    },
    Loop {
        #[arg(long, default_value = "configs/mimir.base.toml")]
        base: PathBuf,
        #[arg(long = "loop-config", default_value = "configs/loop.toml")]
        loop_config: PathBuf,
        #[arg(long)]
        fake_sim: bool,
        #[arg(long)]
        seed: Option<u64>,
    },
}

#[derive(Debug, Serialize)]
#[serde(tag = "command", rename_all = "kebab-case")]
enum CommandReport {
    Mine(MineReport),
    Label(LabelReport),
    BuildLibrary(BuildLibraryReport),
    Export(ExportReport),
    ReplayCompatMatrix(replay_compat::ReplayCompatibilityMatrixReport),
    Loop(LoopReport),
}

#[derive(Debug, Serialize)]
struct MineReport {
    mode: &'static str,
    project_name: String,
    configured_detector: String,
    detector_component: &'static str,
    branch_generator_component: &'static str,
    max_anchors_per_replay: usize,
    max_branches_per_anchor: usize,
    score_metric_count: usize,
}

#[derive(Debug, Serialize)]
struct LabelReport {
    mode: &'static str,
    project_name: String,
    label_namespace: String,
    default_confidence: f32,
    teacher_component: &'static str,
}

#[derive(Debug, Serialize)]
struct BuildLibraryReport {
    mode: &'static str,
    project_name: String,
    label_namespace: String,
    canonical_namespace: String,
    canonicalizer_component: &'static str,
}

#[derive(Debug, Serialize)]
struct ExportReport {
    mode: &'static str,
    project_name: String,
    export_format: &'static str,
    artifact_root: PathBuf,
}

#[derive(Debug, Serialize)]
struct LoopReport {
    mode: &'static str,
    project_name: String,
    backend: String,
    seed: u64,
    command_count: usize,
    step_hashes: Vec<String>,
}

pub fn run_from<I, T>(args: I) -> Result<String>
where
    I: IntoIterator<Item = T>,
    T: Into<OsString> + Clone,
{
    let cli = Cli::parse_from(args);
    dispatch(cli)
}

pub fn try_run_from<I, T>(args: I) -> Result<String>
where
    I: IntoIterator<Item = T>,
    T: Into<OsString> + Clone,
{
    let cli = Cli::try_parse_from(args).map_err(|error| MimirError::message(error.to_string()))?;
    dispatch(cli)
}

pub fn dispatch(cli: Cli) -> Result<String> {
    let report = match cli.command {
        Commands::Mine {
            base,
            anchors,
            branching,
            scoring,
        } => {
            let base: BaseConfig = load_toml_file(base)?;
            let anchors: AnchorsConfig = load_toml_file(anchors)?;
            let branching: BranchingConfig = load_toml_file(branching)?;
            let scoring: ScoringConfig = load_toml_file(scoring)?;
            let scorer = WeightedSumScorer::new(scoring.weights);

            CommandReport::Mine(MineReport {
                mode: "plan-only",
                project_name: base.project_name,
                configured_detector: anchors.detector,
                detector_component: HintAnchorDetector.component_name(),
                branch_generator_component: BoundedManualBranchGenerator::default()
                    .component_name(),
                max_anchors_per_replay: anchors.max_anchors_per_replay,
                max_branches_per_anchor: branching.max_branches_per_anchor,
                score_metric_count: scorer.metric_count(),
            })
        }
        Commands::Label { base, labeling } => {
            let base: BaseConfig = load_toml_file(base)?;
            let labeling: LabelingConfig = load_toml_file(labeling)?;

            CommandReport::Label(LabelReport {
                mode: "plan-only",
                project_name: base.project_name,
                label_namespace: labeling.label_namespace,
                default_confidence: labeling.default_confidence,
                teacher_component: PassThroughTeacherSynthesizer.component_name(),
            })
        }
        Commands::BuildLibrary { base, labeling } => {
            let base: BaseConfig = load_toml_file(base)?;
            let labeling: LabelingConfig = load_toml_file(labeling)?;
            let canonicalizer = LowercaseTrimCanonicalizer;

            CommandReport::BuildLibrary(BuildLibraryReport {
                mode: "plan-only",
                project_name: base.project_name,
                label_namespace: labeling.label_namespace.clone(),
                canonical_namespace: canonicalizer.canonicalize(&labeling.label_namespace),
                canonicalizer_component: canonicalizer.component_name(),
            })
        }
        Commands::ExportBc { base } => {
            let base: BaseConfig = load_toml_file(base)?;
            CommandReport::Export(ExportReport {
                mode: "plan-only",
                project_name: base.project_name,
                export_format: "behavior-cloning",
                artifact_root: base.artifact_root,
            })
        }
        Commands::ExportDagger { base } => {
            let base: BaseConfig = load_toml_file(base)?;
            CommandReport::Export(ExportReport {
                mode: "plan-only",
                project_name: base.project_name,
                export_format: "dagger",
                artifact_root: base.artifact_root,
            })
        }
        Commands::ReplayCompatMatrix {
            corpus_root,
            output,
        } => CommandReport::ReplayCompatMatrix(replay_compat::run(corpus_root, output)?),
        Commands::Loop {
            base,
            loop_config,
            fake_sim,
            seed,
        } => {
            let base: BaseConfig = load_toml_file(base)?;
            let loop_config: LoopConfig = load_toml_file(loop_config)?;

            if !fake_sim {
                return Err(MimirError::message(
                    "loop requires --fake-sim because no non-test sim backend is bundled",
                ));
            }

            let backend = match loop_config.backend {
                LoopBackend::DeterministicFake => DeterministicFakeBackend,
            };
            let seed = seed.unwrap_or(loop_config.default_seed);
            let request = SimulationRequest {
                simulation_id: format!("{}:loop", base.project_name),
                seed,
                commands: loop_config
                    .command_labels
                    .into_iter()
                    .map(|label| SimulationCommand {
                        label,
                        metadata: Metadata::new(),
                    })
                    .collect(),
            };

            let result = backend.simulate(&request)?;

            CommandReport::Loop(LoopReport {
                mode: "simulated-with-fake-backend",
                project_name: base.project_name,
                backend: result.backend,
                seed,
                command_count: result.step_hashes.len(),
                step_hashes: result.step_hashes,
            })
        }
    };

    serde_json::to_string_pretty(&report).map_err(Into::into)
}

#[cfg(test)]
mod tests {
    use super::*;
    use mimir_core::MimirError;
    use tempfile::tempdir;

    fn write_config(path: &std::path::Path, contents: &str) {
        std::fs::write(path, contents).expect("config should be written");
    }

    #[test]
    fn clap_parses_loop_command() {
        let cli = Cli::parse_from(["mimir-cli", "loop", "--fake-sim"]);

        match cli.command {
            Commands::Loop { fake_sim, .. } => assert!(fake_sim),
            _ => panic!("expected loop command"),
        }
    }

    #[test]
    fn clap_parses_replay_compat_matrix_command() {
        let cli = Cli::parse_from([
            "mimir-cli",
            "replay-compat-matrix",
            "--corpus-root",
            "test_corpus/largest_100",
            "--output",
            "target/matrix.jsonl",
        ]);

        match cli.command {
            Commands::ReplayCompatMatrix {
                corpus_root,
                output,
            } => {
                assert_eq!(corpus_root, PathBuf::from("test_corpus/largest_100"));
                assert_eq!(output, PathBuf::from("target/matrix.jsonl"));
            }
            _ => panic!("expected replay-compat-matrix command"),
        }
    }

    #[test]
    fn try_run_from_returns_parse_errors_without_process_exit() {
        let error = try_run_from(["mimir-cli", "definitely-not-a-command"])
            .expect_err("fallible library parsing should return an error");

        assert!(matches!(error, MimirError::Message(_)));
        let message = error.to_string();
        assert!(message.contains("unrecognized subcommand"));
        assert!(message.contains("definitely-not-a-command"));
    }

    #[test]
    fn loop_requires_fake_sim_flag() {
        let directory = tempdir().expect("tempdir should be created");
        let base_path = directory.path().join("mimir.base.toml");
        let loop_path = directory.path().join("loop.toml");

        write_config(
            &base_path,
            r#"
project_name = "MIMIR"
artifact_root = "artifacts"
replay_root = "replays"
"#,
        );
        write_config(
            &loop_path,
            r#"
backend = "deterministic-fake"
default_seed = 7
command_labels = ["bootstrap", "tick"]
"#,
        );

        let error = run_from([
            "mimir-cli",
            "loop",
            "--base",
            base_path.to_str().expect("base path should be UTF-8"),
            "--loop-config",
            loop_path.to_str().expect("loop path should be UTF-8"),
        ])
        .expect_err("loop should reject non-fake execution path");

        assert!(matches!(error, MimirError::Message(_)));
        assert_eq!(
            error.to_string(),
            "loop requires --fake-sim because no non-test sim backend is bundled"
        );
    }
}
