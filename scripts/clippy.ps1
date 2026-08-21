$ErrorActionPreference = "Stop"
cargo clippy --workspace --all-targets --all-features -- -D warnings

if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}
