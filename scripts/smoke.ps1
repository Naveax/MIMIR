$ErrorActionPreference = "Stop"
cargo test -p mimir-cli --test smoke_loop -- --nocapture

if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}
