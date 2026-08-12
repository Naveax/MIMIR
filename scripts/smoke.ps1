$ErrorActionPreference = "Stop"
cargo test -p mimir-cli --test smoke_loop -- --nocapture
