use std::path::PathBuf;
use std::process::Command;

fn workspace_root() -> PathBuf {
    PathBuf::from(env!("CARGO_MANIFEST_DIR"))
        .parent()
        .and_then(|path| path.parent())
        .expect("workspace root should exist")
        .to_path_buf()
}

#[test]
fn smoke_loop_with_fake_backend() {
    let output = Command::new(env!("CARGO_BIN_EXE_mimir-cli"))
        .current_dir(workspace_root())
        .args(["loop", "--fake-sim"])
        .output()
        .expect("CLI should run");

    let stdout = String::from_utf8(output.stdout).expect("stdout should be UTF-8");
    let stderr = String::from_utf8(output.stderr).expect("stderr should be UTF-8");

    assert!(output.status.success(), "stderr was: {stderr}");
    assert!(stdout.contains("\"command\": \"loop\""));
    assert!(stdout.contains("\"backend\": \"deterministic-fake-backend\""));
    assert!(stdout.contains("\"command_count\": 2"));
}
