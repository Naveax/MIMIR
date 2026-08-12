$ErrorActionPreference = "Stop"
cargo clippy --workspace --all-targets --all-features -- -D warnings
