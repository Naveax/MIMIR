$ErrorActionPreference = "Stop"
cargo fmt --all
if ($LASTEXITCODE -ne 0) {
    throw "cargo fmt failed with exit code $LASTEXITCODE"
}
