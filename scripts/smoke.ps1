$ErrorActionPreference = "Stop"
cargo test --locked -p mimir-cli --test smoke_loop -- --nocapture
if ($LASTEXITCODE -ne 0) {
    throw "mimir-cli smoke test failed with exit code $LASTEXITCODE"
}
