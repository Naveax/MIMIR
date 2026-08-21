use mimir_core::{MimirError, NamedComponent, Result, hash_serializable};
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

/// Verifies that a result belongs to the supplied request and backend contract.
///
/// This is intentionally separate from simulation execution so persisted/cached results can be
/// checked before reuse. It does not claim physics validity and does not turn the fake backend
/// into a production RocketSim implementation.
pub trait SimResultVerifier {
    fn verify_result(&self, request: &SimulationRequest, result: &SimulationResult) -> Result<()>;
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

impl SimResultVerifier for DeterministicFakeBackend {
    fn verify_result(&self, request: &SimulationRequest, result: &SimulationResult) -> Result<()> {
        if result.simulation_id != request.simulation_id {
            return Err(MimirError::message(format!(
                "simulation result id mismatch: expected {}, got {}",
                request.simulation_id, result.simulation_id
            )));
        }
        if result.backend != self.component_name() {
            return Err(MimirError::message(format!(
                "simulation result backend mismatch: expected {}, got {}",
                self.component_name(), result.backend
            )));
        }

        let expected = self.simulate(request)?;
        if result.step_hashes.len() != expected.step_hashes.len() {
            return Err(MimirError::message(format!(
                "simulation result step count mismatch: expected {}, got {}",
                expected.step_hashes.len(),
                result.step_hashes.len()
            )));
        }

        for (index, (actual, expected_hash)) in result
            .step_hashes
            .iter()
            .zip(expected.step_hashes.iter())
            .enumerate()
        {
            if actual != expected_hash {
                return Err(MimirError::message(format!(
                    "simulation result step hash mismatch at index {index}"
                )));
            }
        }

        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn request() -> SimulationRequest {
        SimulationRequest {
            simulation_id: "loop-1".to_string(),
            seed: 7,
            commands: vec![
                SimulationCommand {
                    label: "tick-a".to_string(),
                    metadata: Metadata::new(),
                },
                SimulationCommand {
                    label: "tick-b".to_string(),
                    metadata: Metadata::new(),
                },
            ],
        }
    }

    #[test]
    fn fake_backend_is_deterministic_for_identical_inputs() {
        let request = request();

        let first = DeterministicFakeBackend
            .simulate(&request)
            .expect("simulation should succeed");
        let second = DeterministicFakeBackend
            .simulate(&request)
            .expect("simulation should succeed");

        assert_eq!(first, second);
    }

    #[test]
    fn fake_backend_verifier_accepts_exact_result() {
        let request = request();
        let backend = DeterministicFakeBackend;
        let result = backend.simulate(&request).expect("simulation should succeed");

        backend
            .verify_result(&request, &result)
            .expect("exact deterministic result should verify");
    }

    #[test]
    fn fake_backend_verifier_rejects_identity_backend_and_count_drift() {
        let request = request();
        let backend = DeterministicFakeBackend;
        let result = backend.simulate(&request).expect("simulation should succeed");

        let mut wrong_id = result.clone();
        wrong_id.simulation_id = "other".to_string();
        assert!(backend.verify_result(&request, &wrong_id).is_err());

        let mut wrong_backend = result.clone();
        wrong_backend.backend = "other-backend".to_string();
        assert!(backend.verify_result(&request, &wrong_backend).is_err());

        let mut wrong_count = result.clone();
        wrong_count.step_hashes.pop();
        assert!(backend.verify_result(&request, &wrong_count).is_err());
    }

    #[test]
    fn fake_backend_verifier_rejects_tampered_step_hash() {
        let request = request();
        let backend = DeterministicFakeBackend;
        let mut result = backend.simulate(&request).expect("simulation should succeed");
        result.step_hashes[1] = "tampered".to_string();

        let error = backend
            .verify_result(&request, &result)
            .expect_err("tampered step hash must fail closed");
        assert!(error.to_string().contains("step hash mismatch at index 1"));
    }
}
