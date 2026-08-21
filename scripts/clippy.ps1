$ErrorActionPreference = "Stop"
cargo clippy --locked --workspace --all-targets --all-features -- -D warnings
if ($LASTEXITCODE -ne 0) {
    throw "cargo clippy failed with exit code $LASTEXITCODE"
}
