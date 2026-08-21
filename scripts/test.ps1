$ErrorActionPreference = "Stop"
cargo test --locked --workspace --all-targets --all-features
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}