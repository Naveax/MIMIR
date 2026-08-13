#![allow(clippy::all)]

use mimir_replay::{
    MinimalReplayNetworkLookupPlanReader, ReplayInput, ReplayNetworkLookupPlanReader,
};
use std::ffi::OsStr;
use std::fs::{self, File, OpenOptions};
use std::io::{Read, Write};
use std::path::{Path, PathBuf};
use std::process::{Command, Stdio};

const BASE_SHA: &str = "76cbcc2094189e637e135f8c7d99e999e32311a0";
const PRODUCTION_SHA: &str = "bf4bccff82203ed049d33e942681fed07f23beb4";
const SOURCE_BLOB: &str = "f64a5e0d66962f41026b2eb10e176219d4529931";
const BOXCARS_SHA: &str = "c70e77df7af81b436cb545d070bb90c82f562d0b";
const BOXCARS_FRAME_BLOB: &str = "6f2ff153d3a27cdacccc65e3f23851489077a7d8";
const R315A_PATCHER_BLOB: &str = "c67fca03897a2995845097f39d62ab4a68dca340";
const PATHS_SHA: &str = "2ecbeea804f193796a539baee1e968719f03c0cd706efff0c22a61e6ef943dae";
const IDENTITIES_SHA: &str = "b02488b13cd6374219bbb89f884b03f8356f3744f930e39b2279df34859015cf";

fn run(command: &mut Command, label: &str) {
    let status = command
        .status()
        .unwrap_or_else(|error| panic!("{label}: failed to start: {error}"));
    assert!(status.success(), "{label}: exit status {status}");
}

fn capture(command: &mut Command, label: &str) -> Vec<u8> {
    let output = command
        .output()
        .unwrap_or_else(|error| panic!("{label}: failed to start: {error}"));
    assert!(
        output.status.success(),
        "{label}: exit status {}\nstdout={}\nstderr={}",
        output.status,
        String::from_utf8_lossy(&output.stdout),
        String::from_utf8_lossy(&output.stderr)
    );
    output.stdout
}

fn text(command: &mut Command, label: &str) -> String {
    String::from_utf8(capture(command, label))
        .unwrap_or_else(|error| panic!("{label}: non-UTF8 stdout: {error}"))
        .trim()
        .to_owned()
}

fn succeeds(command: &mut Command) -> bool {
    command.status().map(|status| status.success()).unwrap_or(false)
}

fn sha256(path: &Path) -> String {
    text(
        Command::new("python")
            .arg("-c")
            .arg("import hashlib,sys;print(hashlib.sha256(open(sys.argv[1],'rb').read()).hexdigest())")
            .arg(path),
        "sha256",
    )
}

fn git_diff_frozen() {
    run(
        Command::new("git").args([
            "diff",
            "--exit-code",
            &format!("{BASE_SHA}..HEAD"),
            "--",
            "crates/mimir-replay/src/lib.rs",
            "crates/mimir-replay/Cargo.toml",
            "Cargo.toml",
            "Cargo.lock",
            "external_fixtures",
            "test_corpus",
        ]),
        "frozen production diff",
    );
}

fn emit_file(path: &str) {
    println!("R3_16A_FILE_BEGIN\t{path}");
    let mut content = String::new();
    File::open(path)
        .unwrap_or_else(|error| panic!("open receipt {path}: {error}"))
        .read_to_string(&mut content)
        .unwrap_or_else(|error| panic!("read receipt {path}: {error}"));
    print!("{content}");
    if !content.ends_with('\n') {
        println!();
    }
    println!("R3_16A_FILE_END\t{path}");
}

#[test]
fn r3_16a_existing_actor_first_property_evidence() {
    if std::env::var_os("GITHUB_ACTIONS").is_none() {
        eprintln!("R3.16A temporary evidence test skipped outside GitHub Actions");
        return;
    }

    let root = PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("../..");
    std::env::set_current_dir(&root).expect("set repository root");
    fs::create_dir_all(".tmp").expect("create .tmp");
    let marker = Path::new(".tmp/r3_16a_evidence_complete");
    if marker.exists() {
        println!("R3_16A_REUSE=PASS");
        return;
    }

    println!(
        "R3_16A_HEAD={}",
        text(Command::new("git").args(["rev-parse", "HEAD"]), "git head")
    );
    if !succeeds(Command::new("git").args(["cat-file", "-e", &format!("{BASE_SHA}^{{commit}}")])) {
        run(
            Command::new("git").args([
                "fetch",
                "--quiet",
                "--deepen=50",
                "origin",
                "evidence/r316a-property-envelope",
            ]),
            "deepen evidence history",
        );
    }
    assert_eq!(
        text(
            Command::new("git").args(["rev-parse", "HEAD:crates/mimir-replay/src/lib.rs"]),
            "production source blob",
        ),
        SOURCE_BLOB
    );
    git_diff_frozen();

    let changed = text(
        Command::new("git").args([
            "diff",
            "--name-only",
            &format!("{BASE_SHA}..HEAD"),
        ]),
        "source scope",
    );
    fs::write(
        "r3_16a_source_scope.txt",
        format!(
            "{changed}\nbase_sha={BASE_SHA}\nproduction_sha={PRODUCTION_SHA}\nproduction_source_blob={SOURCE_BLOB}\nproduction_mutation_count=0\ncargo_mutation_count=0\n"
        ),
    )
    .expect("write source scope");

    assert_eq!(
        sha256(Path::new("tools/_tmp_r316a_r315d_paths.txt")),
        PATHS_SHA
    );
    assert_eq!(
        sha256(Path::new("tools/_tmp_r316a_r315d_identity.tsv")),
        IDENTITIES_SHA
    );
    fs::create_dir_all(".tmp/r315d").expect("create parent projection dir");
    fs::copy(
        "tools/_tmp_r316a_r315d_paths.txt",
        ".tmp/r315d/r3_15d_paths.txt",
    )
    .expect("copy paths");
    fs::copy(
        "tools/_tmp_r316a_r315d_identity.tsv",
        ".tmp/r315d/r3_15d_replay_identity.tsv",
    )
    .expect("copy identities");
    run(
        Command::new("python").args([
            "tools/_tmp_r316a_prepare.py",
            root.to_str().expect("root UTF8"),
            ".tmp/r315d",
        ]),
        "prepare selector identities",
    );

    let boxcars = root.join(".tmp/boxcars-r316a");
    let _ = fs::remove_dir_all(&boxcars);
    run(
        Command::new("git")
            .args(["clone", "--quiet", "https://github.com/nickbabcock/boxcars.git"])
            .arg(&boxcars),
        "clone pinned Boxcars",
    );
    run(
        Command::new("git")
            .arg("-C")
            .arg(&boxcars)
            .args(["checkout", "--quiet", "--detach", BOXCARS_SHA]),
        "checkout pinned Boxcars",
    );
    assert_eq!(
        text(
            Command::new("git").arg("-C").arg(&boxcars).args(["rev-parse", "HEAD"]),
            "Boxcars head",
        ),
        BOXCARS_SHA
    );
    assert_eq!(
        text(
            Command::new("git")
                .arg("-C")
                .arg(&boxcars)
                .args(["hash-object", "src/network/frame_decoder.rs"]),
            "Boxcars frame blob",
        ),
        BOXCARS_FRAME_BLOB
    );

    run(
        Command::new("git").args([
            "fetch",
            "--quiet",
            "origin",
            "agent/evidence-next:refs/remotes/origin/agent/evidence-next",
        ]),
        "fetch admitted R3.15A patcher",
    );
    let base_patcher = Path::new(".tmp/r315a_base.py");
    fs::write(
        base_patcher,
        capture(
            Command::new("git").args([
                "show",
                "origin/agent/evidence-next:tools/_tmp_evidence_next.py",
            ]),
            "recover R3.15A patcher",
        ),
    )
    .expect("write R3.15A patcher");
    assert_eq!(
        text(
            Command::new("git").arg("hash-object").arg(base_patcher),
            "R3.15A patcher blob",
        ),
        R315A_PATCHER_BLOB
    );
    run(
        Command::new("python")
            .arg(base_patcher)
            .arg("patch-boxcars")
            .arg(&boxcars),
        "apply R3.15A instrumentation base",
    );
    run(
        Command::new("python")
            .arg("tools/_tmp_r316a_patch.py")
            .arg(&boxcars),
        "apply R3.16A property instrumentation",
    );
    run(
        Command::new("git")
            .arg("-C")
            .arg(&boxcars)
            .args(["add", "-N", "examples/r3_15a_probe.rs"]),
        "intent-to-add Boxcars probe",
    );
    run(
        Command::new("git")
            .arg("-C")
            .arg(&boxcars)
            .args(["diff", "--check"]),
        "Boxcars diff check",
    );
    let patch = capture(
        Command::new("git")
            .arg("-C")
            .arg(&boxcars)
            .args([
                "diff",
                "--binary",
                "--",
                "src/network/frame_decoder.rs",
                "examples/r3_15a_probe.rs",
            ]),
        "Boxcars instrumentation patch",
    );
    fs::write("r3_16a_boxcars_instrumentation.patch", patch).expect("write instrumentation patch");
    fs::write(
        "r3_16a_boxcars_instrumentation_sha256.txt",
        format!(
            "{}  r3_16a_boxcars_instrumentation.patch\n",
            sha256(Path::new("r3_16a_boxcars_instrumentation.patch"))
        ),
    )
    .expect("write instrumentation SHA");

    let manifest = boxcars.join("Cargo.toml");
    let boxcars_target = boxcars.join(".r316a-target");
    for (args, label) in [
        (
            vec!["check", "--manifest-path", manifest.to_str().unwrap(), "--example", "r3_15a_probe"],
            "Boxcars probe check",
        ),
        (
            vec!["test", "--manifest-path", manifest.to_str().unwrap(), "--lib", "--quiet"],
            "Boxcars library tests",
        ),
        (
            vec!["build", "--manifest-path", manifest.to_str().unwrap(), "--example", "r3_15a_probe", "--quiet"],
            "Boxcars probe build",
        ),
    ] {
        run(
            Command::new("cargo")
                .args(args)
                .env("CARGO_TARGET_DIR", &boxcars_target),
            label,
        );
    }

    let probe = boxcars_target
        .join("debug/examples")
        .join(format!("r3_15a_probe{}", std::env::consts::EXE_SUFFIX));
    assert!(probe.is_file(), "Boxcars probe missing: {}", probe.display());
    let paths = fs::read_to_string("r3_16a_paths.txt").expect("read 47 paths");
    let log_path = Path::new("r3_16a_boxcars.log");
    File::create(log_path).expect("truncate Boxcars log");
    for rel in paths.lines().filter(|line| !line.is_empty()) {
        let stdout = OpenOptions::new()
            .append(true)
            .open(log_path)
            .expect("open Boxcars stdout log");
        let stderr = stdout.try_clone().expect("clone Boxcars log handle");
        run(
            Command::new(&probe)
                .arg(root.join(rel))
                .env("MIMIR_R3_15A_LABEL", rel)
                .stdout(Stdio::from(stdout))
                .stderr(Stdio::from(stderr)),
            &format!("Boxcars replay {rel}"),
        );
    }
    let boxcars_log = fs::read_to_string(log_path).expect("read Boxcars log");
    assert_eq!(
        boxcars_log
            .lines()
            .filter(|line| *line == "R3_15A_ORACLE_PARSE=PASS")
            .count(),
        47
    );
    assert_eq!(
        boxcars_log
            .lines()
            .filter(|line| line.starts_with("R3_16A_PROPERTY\t"))
            .count(),
        47
    );
    run(
        Command::new("python").args([
            "tools/_tmp_r316a_select.py",
            "r3_16a_boxcars.log",
        ]),
        "select first property oracle rows",
    );
    fs::write(
        "r3_16a_boxcars_log_sha256.txt",
        format!("{}  r3_16a_boxcars.log\n", sha256(log_path)),
    )
    .expect("write Boxcars log SHA");

    let queries = fs::read_to_string("r3_16a_mimir_queries.tsv").expect("read MIMIR queries");
    let mut mimir_log = File::create("r3_16a_mimir.log").expect("create MIMIR log");
    let mut mimir_rows = 0usize;
    for line in queries.lines().filter(|line| !line.is_empty()) {
        let mut fields = line.split('\t');
        let rel = fields.next().expect("query path");
        let actor_object_id: usize = fields.next().expect("actor object id").parse().expect("actor object id integer");
        let stream_id: u32 = fields.next().expect("stream id").parse().expect("stream id integer");
        assert!(fields.next().is_none(), "unexpected query column");

        let bytes = fs::read(root.join(rel)).unwrap_or_else(|error| panic!("{rel}: {error}"));
        let input = ReplayInput::Memory {
            label: rel.to_owned(),
            bytes,
        };
        let plan = MinimalReplayNetworkLookupPlanReader
            .read_network_lookup_plan(&input)
            .unwrap_or_else(|error| panic!("{rel}: lookup plan: {error}"));
        let lookup = plan
            .object_lookups
            .get(actor_object_id)
            .and_then(|entry| entry.as_ref())
            .unwrap_or_else(|| panic!("{rel}: missing actor object lookup {actor_object_id}"));
        let property = lookup
            .properties
            .iter()
            .find(|property| property.stream_id == stream_id)
            .unwrap_or_else(|| panic!("{rel}: missing stream {stream_id}"));
        let actor_name = plan
            .footer_lookup
            .objects
            .get(actor_object_id)
            .expect("actor object name");
        let property_name = plan
            .footer_lookup
            .objects
            .get(property.object_index as usize)
            .expect("property object name");
        writeln!(
            mimir_log,
            "R3_16A_MIMIR\tlabel={rel}\tactor_object_id={actor_object_id}\tactor_object_name={actor_name}\tstream_id={stream_id}\tmax_prop_id={}\tprop_id_bits={}\tproperty_object_id={}\tproperty_object_name={}\ttag={:?}",
            lookup.max_prop_id,
            lookup.prop_id_bits,
            property.object_index,
            property_name,
            property.tag,
        )
        .expect("write MIMIR row");
        mimir_rows += 1;
    }
    drop(mimir_log);
    assert_eq!(mimir_rows, 47);
    run(
        Command::new("python").args([
            "tools/_tmp_r316a_compare.py",
            "r3_16a_mimir.log",
        ]),
        "compare oracle to production lookup plan",
    );
    let aggregate = fs::read_to_string("r3_16a_aggregate.txt").expect("read aggregate");
    assert!(aggregate.lines().any(|line| line == "R3_16A_OUTCOME=A"));
    assert!(aggregate.lines().any(|line| line == "R3_16A_EVIDENCE=PASS"));

    assert_eq!(
        text(
            Command::new("git").args(["rev-parse", "HEAD:crates/mimir-replay/src/lib.rs"]),
            "final source blob",
        ),
        SOURCE_BLOB
    );
    git_diff_frozen();

    for receipt in [
        "r3_16a_source_scope.txt",
        "r3_16a_parent_evidence_identity.txt",
        "r3_16a_replay_identity.tsv",
        "r3_16a_paths.txt",
        "r3_16a_boxcars_instrumentation_sha256.txt",
        "r3_16a_boxcars_log_sha256.txt",
        "r3_16a_first_property_oracle.jsonl",
        "r3_16a_oracle_selection_summary.json",
        "r3_16a_mimir_queries.tsv",
        "r3_16a_mimir.log",
        "r3_16a_comparisons.jsonl",
        "r3_16a_summary.json",
        "r3_16a_aggregate.txt",
    ] {
        emit_file(receipt);
    }
    println!("R3_16A_RECEIPT_STREAM=PASS");
    fs::write(marker, b"PASS\n").expect("write evidence marker");
}
