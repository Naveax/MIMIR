$ErrorActionPreference = "Stop"
cargo test --locked -p mimir-cli --test smoke_loop -- --nocapture