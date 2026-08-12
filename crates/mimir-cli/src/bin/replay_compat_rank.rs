use clap::Parser;
use serde::{Deserialize, Serialize};
use std::collections::BTreeMap;
use std::error::Error;
use std::fs;
use std::path::{Path, PathBuf};

const FULL_COVERAGE_BASIS_POINTS: u32 = 10_000;

#[derive(Debug, Parser)]
#[command(name = "replay-compat-rank")]
#[command(about = "Rank replay header version tuples by observed corpus frequency")]
struct Args {
    #[arg(long)]
    matrix: PathBuf,

    #[arg(long)]
    output: PathBuf,
}

#[derive(Debug, Clone, Deserialize)]
struct MatrixRow {
    major_version: Option<i32>,
    minor_version: Option<i32>,
    net_version: Option<i32>,
    game_type: Option<String>,
    replay_version: Option<i32>,
    build_version: Option<String>,
}

#[derive(Debug, Clone, PartialEq, Eq, PartialOrd, Ord)]
struct VersionTupleKey {
    major_version: i32,
    minor_version: i32,
    net_version: i32,
    game_type: String,
    replay_version: i32,
    build_version: String,
}

#[derive(Debug, Clone, Serialize, PartialEq, Eq)]
struct VersionTupleFrequency {
    rank: usize,
    count: usize,
    cumulative_count: usize,
    coverage_basis_points: u32,
    cumulative_coverage_basis_points: u32,
    major_version: i32,
    minor_version: i32,
    net_version: i32,
    game_type: String,
    replay_version: i32,
    build_version: String,
}

#[derive(Debug, Clone, Serialize, PartialEq, Eq)]
struct VersionTupleRankingSummary {
    mode: &'static str,
    scanned: usize,
    rankable_rows: usize,
    unrankable_rows: usize,
    unique_version_tuples: usize,
    rankable_coverage_basis_points: u32,
    rankings: Vec<VersionTupleFrequency>,
}

fn main() -> Result<(), Box<dyn Error>> {
    let args = Args::parse();
    let rows = load_matrix(&args.matrix)?;
    let summary = rank_rows(&rows)?;
    write_summary(&args.output, &summary)?;

    println!("MIMIR Replay Compatibility Tuple Ranking");
    println!("scanned={}", summary.scanned);
    println!("rankable_rows={}", summary.rankable_rows);
    println!("unrankable_rows={}", summary.unrankable_rows);
    println!("unique_version_tuples={}", summary.unique_version_tuples);
    println!(
        "rankable_coverage_basis_points={}",
        summary.rankable_coverage_basis_points
    );
    println!("top_version_tuples:");
    for entry in summary.rankings.iter().take(10) {
        println!(
            "  rank={} count={} cumulative={} coverage_bps={} cumulative_bps={} tuple={}|{}|{}|{}|{}|{}",
            entry.rank,
            entry.count,
            entry.cumulative_count,
            entry.coverage_basis_points,
            entry.cumulative_coverage_basis_points,
            entry.major_version,
            entry.minor_version,
            entry.net_version,
            entry.game_type,
            entry.replay_version,
            entry.build_version
        );
    }
    println!("output={}", args.output.display());

    Ok(())
}

fn load_matrix(path: &Path) -> Result<Vec<MatrixRow>, Box<dyn Error>> {
    let text = fs::read_to_string(path)?;
    let mut rows = Vec::new();

    for (line_index, line) in text.lines().enumerate() {
        if line.trim().is_empty() {
            continue;
        }

        let row = serde_json::from_str::<MatrixRow>(line).map_err(|error| {
            format!(
                "replay compatibility matrix JSON error at {} line {}: {error}",
                path.display(),
                line_index + 1
            )
        })?;
        rows.push(row);
    }

    if rows.is_empty() {
        return Err(format!("replay compatibility matrix is empty: {}", path.display()).into());
    }

    Ok(rows)
}

fn rank_rows(rows: &[MatrixRow]) -> Result<VersionTupleRankingSummary, Box<dyn Error>> {
    if rows.is_empty() {
        return Err("cannot rank an empty replay compatibility matrix".into());
    }

    let mut counts = BTreeMap::<VersionTupleKey, usize>::new();
    let mut unrankable_rows = 0usize;

    for row in rows {
        let Some(key) = tuple_key(row) else {
            unrankable_rows += 1;
            continue;
        };
        *counts.entry(key).or_default() += 1;
    }

    let rankable_rows = rows.len() - unrankable_rows;
    let mut frequencies = counts.into_iter().collect::<Vec<_>>();
    frequencies.sort_by(|(left_key, left_count), (right_key, right_count)| {
        right_count
            .cmp(left_count)
            .then_with(|| left_key.cmp(right_key))
    });

    let mut cumulative_count = 0usize;
    let mut rankings = Vec::with_capacity(frequencies.len());

    for (index, (key, count)) in frequencies.into_iter().enumerate() {
        cumulative_count += count;
        rankings.push(VersionTupleFrequency {
            rank: index + 1,
            count,
            cumulative_count,
            coverage_basis_points: basis_points(count, rows.len()),
            cumulative_coverage_basis_points: basis_points(cumulative_count, rows.len()),
            major_version: key.major_version,
            minor_version: key.minor_version,
            net_version: key.net_version,
            game_type: key.game_type,
            replay_version: key.replay_version,
            build_version: key.build_version,
        });
    }

    if cumulative_count != rankable_rows {
        return Err(format!(
            "tuple ranking count drift: rankable_rows={rankable_rows}, ranked={cumulative_count}"
        )
        .into());
    }

    Ok(VersionTupleRankingSummary {
        mode: "version-tuple-frequency-v1",
        scanned: rows.len(),
        rankable_rows,
        unrankable_rows,
        unique_version_tuples: rankings.len(),
        rankable_coverage_basis_points: basis_points(rankable_rows, rows.len()),
        rankings,
    })
}

fn tuple_key(row: &MatrixRow) -> Option<VersionTupleKey> {
    Some(VersionTupleKey {
        major_version: row.major_version?,
        minor_version: row.minor_version?,
        net_version: row.net_version?,
        game_type: row.game_type.clone()?,
        replay_version: row.replay_version?,
        build_version: row.build_version.clone()?,
    })
}

fn basis_points(numerator: usize, denominator: usize) -> u32 {
    if denominator == 0 {
        return 0;
    }

    let scaled = (numerator as u128) * u128::from(FULL_COVERAGE_BASIS_POINTS);
    u32::try_from(scaled / (denominator as u128))
        .expect("basis-point ratio cannot exceed 10000 for bounded corpus counts")
}

fn write_summary(path: &Path, summary: &VersionTupleRankingSummary) -> Result<(), Box<dyn Error>> {
    if let Some(parent) = path
        .parent()
        .filter(|parent| !parent.as_os_str().is_empty())
    {
        fs::create_dir_all(parent)?;
    }

    let encoded = serde_json::to_string_pretty(summary)?;
    fs::write(path, format!("{encoded}\n"))?;
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    fn row(major: i32, build: &str) -> MatrixRow {
        MatrixRow {
            major_version: Some(major),
            minor_version: Some(32),
            net_version: Some(10),
            game_type: Some("TAGame.Replay_Soccar_TA".to_string()),
            replay_version: Some(8),
            build_version: Some(build.to_string()),
        }
    }

    #[test]
    fn ranking_orders_by_frequency_then_tuple_key() {
        let rows = vec![
            row(900, "B"),
            row(800, "A"),
            row(900, "B"),
            row(700, "C"),
            row(800, "A"),
        ];

        let summary = rank_rows(&rows).expect("ranking should succeed");

        assert_eq!(summary.scanned, 5);
        assert_eq!(summary.rankable_rows, 5);
        assert_eq!(summary.unrankable_rows, 0);
        assert_eq!(summary.unique_version_tuples, 3);
        assert_eq!(summary.rankings[0].count, 2);
        assert_eq!(summary.rankings[0].major_version, 800);
        assert_eq!(summary.rankings[1].count, 2);
        assert_eq!(summary.rankings[1].major_version, 900);
        assert_eq!(summary.rankings[2].count, 1);
        assert_eq!(summary.rankings[2].major_version, 700);
    }

    #[test]
    fn ranking_tracks_exact_basis_point_coverage() {
        let rows = vec![row(900, "B"), row(900, "B"), row(800, "A"), row(700, "C")];

        let summary = rank_rows(&rows).expect("ranking should succeed");

        assert_eq!(summary.rankable_coverage_basis_points, 10_000);
        assert_eq!(summary.rankings[0].coverage_basis_points, 5_000);
        assert_eq!(summary.rankings[0].cumulative_coverage_basis_points, 5_000);
        assert_eq!(summary.rankings[1].cumulative_coverage_basis_points, 7_500);
        assert_eq!(summary.rankings[2].cumulative_coverage_basis_points, 10_000);
    }

    #[test]
    fn ranking_preserves_unrankable_rows_without_inventing_tuple_data() {
        let mut incomplete = row(900, "B");
        incomplete.build_version = None;
        let rows = vec![row(800, "A"), incomplete];

        let summary = rank_rows(&rows).expect("ranking should succeed");

        assert_eq!(summary.scanned, 2);
        assert_eq!(summary.rankable_rows, 1);
        assert_eq!(summary.unrankable_rows, 1);
        assert_eq!(summary.unique_version_tuples, 1);
        assert_eq!(summary.rankable_coverage_basis_points, 5_000);
        assert_eq!(summary.rankings[0].coverage_basis_points, 5_000);
        assert_eq!(summary.rankings[0].cumulative_coverage_basis_points, 5_000);
    }
}