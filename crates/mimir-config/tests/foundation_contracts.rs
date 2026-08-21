use mimir_config::{BaseConfig, LoopBackend, LoopConfig};

#[test]
fn unsupported_loop_backend_is_rejected_instead_of_silently_defaulting() {
    let error = toml::from_str::<LoopConfig>(
        r#"
backend = "rocketsim"
default_seed = 7
command_labels = ["tick"]
"#,
    )
    .expect_err("unsupported backend must fail closed");

    assert!(error.to_string().contains("deterministic-fake"));
}

#[test]
fn missing_required_base_config_field_is_rejected() {
    let error = toml::from_str::<BaseConfig>(
        r#"
project_name = "MIMIR"
artifact_root = "artifacts"
"#,
    )
    .expect_err("missing replay_root must be rejected");

    assert!(error.to_string().contains("replay_root"));
}

#[test]
fn loop_config_toml_roundtrip_preserves_command_order_and_seed() {
    let config = LoopConfig {
        backend: LoopBackend::DeterministicFake,
        default_seed: 4242,
        command_labels: vec![
            "bootstrap".to_string(),
            "steer".to_string(),
            "boost".to_string(),
        ],
    };

    let encoded = toml::to_string(&config).expect("loop config should serialize");
    let decoded: LoopConfig = toml::from_str(&encoded).expect("loop config should roundtrip");

    assert_eq!(decoded, config);
    assert_eq!(decoded.command_labels, vec!["bootstrap", "steer", "boost"]);
}
