$ErrorActionPreference = "Stop"
cargo test --locked --workspace --all-targets --all-features
if ($LASTEXITCODE -ne 0) {
    throw "cargo test failed with exit code $LASTEXITCODE"
}
