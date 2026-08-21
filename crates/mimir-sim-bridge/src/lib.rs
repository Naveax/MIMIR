use mimir_core::{MimirError, NamedComponent, Result, hash_serializable};
use mimir_types::Metadata;
use serde::{Deserialize, Serialize};

pub const BOUND_SIMULATION_RESULT_VERSION_V1: u32 = 1;
const SIMULATION_REQUEST_DIGEST_DOMAIN_V1: &str = "mimir.simulation_request.v1";

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

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
#[serde(deny_unknown_fields)]
pub struct BoundSimulationResultV1 {
    pub version: u32,
    pub request_digest: String,
    pub result: SimulationResult,
}

#[derive(Serialize)]
struct SimulationRequestDigestMaterialV1<'a> {
    domain: &'static str,
    request: &'a SimulationRequest,
}

pub fn simulation_request_digest_v1(request: &SimulationRequest) -> Result<String> {
    hash_serializable(&SimulationRequestDigestMaterialV1 {
        domain: SIMULATION_REQUEST_DIGEST_DOMAIN_V1,
        request,
    })
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

impl DeterministicFakeBackend {
    pub fn simulate_bound_v1(
        &self,
        request: &SimulationRequest,
    ) -> Result<BoundSimulationResultV1> {
        Ok(BoundSimulationResultV1 {
            version: BOUND_SIMULATION_RESULT_VERSION_V1,
            request_digest: simulation_request_digest_v1(request)?,
            result: self.simulate(request)?,
        })
    }

    pub fn verify_bound_result_v1(
        &self,
        request: &SimulationRequest,
        bound: &BoundSimulationResultV1,
    ) -> Result<()> {
        if bound.version != BOUND_SIMULATION_RESULT_VERSION_V1 {
            return Err(MimirError::message(format!(
                "unsupported bound simulation result version {}",
                bound.version
            )));
        }

        let expected_digest = simulation_request_digest_v1(request)?;
        if bound.request_digest != expected_digest {
            return Err(MimirError::message(
                "bound simulation result request digest mismatch",
            ));
        }

        let expected_result = self.simulate(request)?;
        if bound.result != expected_result {
            return Err(MimirError::message(
                "bound simulation result does not match deterministic backend output",
            ));
        }

        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use mimir_types::FieldValue;

    fn request() -> SimulationRequest {
        SimulationRequest {
            simulation_id: "loop-1".to_string(),
            seed: 7,
            commands: vec![SimulationCommand {
                label: "tick".to_string(),
                metadata: Metadata::from([("mode", FieldValue::Text("baseline".to_string()))]),
            }],
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
    fn request_digest_binds_seed_command_and_metadata_content() {
        let baseline = request();
        let baseline_digest = simulation_request_digest_v1(&baseline).expect("digest");

        let mut seed_drift = baseline.clone();
        seed_drift.seed += 1;
        assert_ne!(
            baseline_digest,
            simulation_request_digest_v1(&seed_drift).expect("seed drift digest")
        );

        let mut command_drift = baseline.clone();
        command_drift.commands[0].label = "other".to_string();
        assert_ne!(
            baseline_digest,
            simulation_request_digest_v1(&command_drift).expect("command drift digest")
        );

        let mut metadata_drift = baseline.clone();
        metadata_drift.commands[0]
            .metadata
            .insert("mode".to_string(), FieldValue::Text("changed".to_string()));
        assert_ne!(
            baseline_digest,
            simulation_request_digest_v1(&metadata_drift).expect("metadata drift digest")
        );
    }

    #[test]
    fn bound_result_accepts_exact_request_and_rejects_stale_request_content() {
        let backend = DeterministicFakeBackend;
        let baseline = request();
        let bound = backend
            .simulate_bound_v1(&baseline)
            .expect("bound simulation should succeed");

        backend
            .verify_bound_result_v1(&baseline, &bound)
            .expect("exact bound result should verify");

        let mut stale_request = baseline.clone();
        stale_request.seed += 1;
        assert!(
            backend
                .verify_bound_result_v1(&stale_request, &bound)
                .is_err()
        );
    }

    #[test]
    fn bound_result_rejects_version_digest_and_result_tampering() {
        let backend = DeterministicFakeBackend;
        let request = request();
        let bound = backend
            .simulate_bound_v1(&request)
            .expect("bound simulation should succeed");

        let mut wrong_version = bound.clone();
        wrong_version.version += 1;
        assert!(
            backend
                .verify_bound_result_v1(&request, &wrong_version)
                .is_err()
        );

        let mut wrong_digest = bound.clone();
        wrong_digest.request_digest = "tampered".to_string();
        assert!(
            backend
                .verify_bound_result_v1(&request, &wrong_digest)
                .is_err()
        );

        let mut wrong_result = bound;
        wrong_result.result.step_hashes[0] = "tampered".to_string();
        assert!(
            backend
                .verify_bound_result_v1(&request, &wrong_result)
                .is_err()
        );
    }
}
