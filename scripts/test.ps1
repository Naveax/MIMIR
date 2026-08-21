$ErrorActionPreference = "Stop"
cargo test --workspace --all-targets --all-features

if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}
