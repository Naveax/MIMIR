$ErrorActionPreference = "Stop"
cargo check --locked --workspace --all-targets --all-features
if ($LASTEXITCODE -ne 0) {
    throw "cargo check failed with exit code $LASTEXITCODE"
}
