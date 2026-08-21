use mimir_sim_bridge::{
    DeterministicFakeBackend, SimBackend, SimulationCommand, SimulationRequest,
};
use mimir_types::{FieldValue, Metadata};

fn command(label: &str, metadata: Metadata) -> SimulationCommand {
    SimulationCommand {
        label: label.to_string(),
        metadata,
    }
}

fn request(seed: u64, commands: Vec<SimulationCommand>) -> SimulationRequest {
    SimulationRequest {
        simulation_id: "foundation-contract".to_string(),
        seed,
        commands,
    }
}

#[test]
fn identical_requests_produce_identical_ordered_step_hashes() {
    let request = request(
        41,
        vec![
            command(
                "steer",
                Metadata::from([("direction", FieldValue::Float(0.25))]),
            ),
            command(
                "boost",
                Metadata::from([("pressed", FieldValue::Boolean(true))]),
            ),
        ],
    );

    let first = DeterministicFakeBackend
        .simulate(&request)
        .expect("fake simulation should succeed");
    let second = DeterministicFakeBackend
        .simulate(&request)
        .expect("repeated fake simulation should succeed");

    assert_eq!(first, second);
    assert_eq!(first.simulation_id, request.simulation_id);
    assert_eq!(first.step_hashes.len(), request.commands.len());
}

#[test]
fn changing_seed_changes_the_deterministic_trace_without_changing_shape() {
    let commands = vec![
        command("jump", Metadata::new()),
        command("boost", Metadata::new()),
    ];
    let baseline = DeterministicFakeBackend
        .simulate(&request(7, commands.clone()))
        .expect("baseline fake simulation should succeed");
    let mutated = DeterministicFakeBackend
        .simulate(&request(8, commands))
        .expect("seed-mutated fake simulation should succeed");

    assert_eq!(baseline.simulation_id, mutated.simulation_id);
    assert_eq!(baseline.backend, mutated.backend);
    assert_eq!(baseline.step_hashes.len(), mutated.step_hashes.len());
    assert_ne!(baseline.step_hashes, mutated.step_hashes);
}

#[test]
fn command_metadata_mutation_changes_only_the_targeted_step_hash() {
    let baseline = request(
        11,
        vec![
            command(
                "steer",
                Metadata::from([("direction", FieldValue::Float(0.5))]),
            ),
            command(
                "boost",
                Metadata::from([("pressed", FieldValue::Boolean(true))]),
            ),
        ],
    );
    let mutated = request(
        11,
        vec![
            command(
                "steer",
                Metadata::from([("direction", FieldValue::Float(0.5))]),
            ),
            command(
                "boost",
                Metadata::from([("pressed", FieldValue::Boolean(false))]),
            ),
        ],
    );

    let baseline = DeterministicFakeBackend
        .simulate(&baseline)
        .expect("baseline fake simulation should succeed");
    let mutated = DeterministicFakeBackend
        .simulate(&mutated)
        .expect("metadata-mutated fake simulation should succeed");

    assert_eq!(baseline.step_hashes.len(), 2);
    assert_eq!(mutated.step_hashes.len(), 2);
    assert_eq!(baseline.step_hashes[0], mutated.step_hashes[0]);
    assert_ne!(baseline.step_hashes[1], mutated.step_hashes[1]);
}

#[test]
fn empty_command_sequence_returns_an_empty_trace() {
    let result = DeterministicFakeBackend
        .simulate(&request(99, Vec::new()))
        .expect("empty fake simulation should still succeed");

    assert_eq!(result.simulation_id, "foundation-contract");
    assert!(result.step_hashes.is_empty());
}
