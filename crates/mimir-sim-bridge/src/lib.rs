use mimir_core::{NamedComponent, Result, hash_serializable};
use mimir_types::Metadata;
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub struct SimulationCommand {
    pub label: String,
    pub metadata: Metadata,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub struct SimulationRequest {
    pub simulation_id: String,
    pub seed: u64,
    pub commands: Vec<SimulationCommand>,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub struct SimulationResult {
    pub simulation_id: String,
    pub backend: String,
    pub step_hashes: Vec<String>,
}

pub trait SimBackend {
    fn simulate(&self, request: &SimulationRequest) -> Result<SimulationResult>;
}

#[derive(Debug, Default, Clone, Copy)]
pub struct DeterministicFakeBackend;

impl NamedComponent for DeterministicFakeBackend {
    fn component_name(&self) -> &'static str {
        "deterministic-fake-backend"
    }
}

impl SimBackend for DeterministicFakeBackend {
    fn simulate(&self, request: &SimulationRequest) -> Result<SimulationResult> {
        let step_hashes = request
            .commands
            .iter()
            .enumerate()
            .map(|(index, command)| {
                hash_serializable(&(request.simulation_id.as_str(), request.seed, index, command))
            })
            .collect::<Result<Vec<_>>>()?;

        Ok(SimulationResult {
            simulation_id: request.simulation_id.clone(),
            backend: self.component_name().to_string(),
            step_hashes,
        })
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn fake_backend_is_deterministic_for_identical_inputs() {
        let request = SimulationRequest {
            simulation_id: "loop-1".to_string(),
            seed: 7,
            commands: vec![SimulationCommand {
                label: "tick".to_string(),
                metadata: Metadata::new(),
            }],
        };

        let first = DeterministicFakeBackend
            .simulate(&request)
            .expect("simulation should succeed");
        let second = DeterministicFakeBackend
            .simulate(&request)
            .expect("simulation should succeed");

        assert_eq!(first, second);
    }
}
