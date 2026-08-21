use mimir_io::{read_artifact_auto, write_artifact, ArtifactFormat};
use mimir_types::{
    AnchorArtifactPayload, AnchorId, AnchorKind, ArtifactHeader, ArtifactKind, FrameIndex, Metadata,
    PersistedAnchorArtifact, ReplayId,
};
use tempfile::tempdir;

#[test]
fn toml_artifact_round_trip_matches_json_supported_boundary() {
    let directory = tempdir().expect("tempdir should be created");
    let path = directory.path().join("anchor.toml");
    let artifact = PersistedAnchorArtifact::new(
        ArtifactHeader::for_kind(ArtifactKind::Anchor, "mimir-io-toml-contract")
            .with_created_by_component("foundation-contract"),
        AnchorArtifactPayload {
            id: AnchorId::new("anchor-toml"),
            replay_id: ReplayId::new("replay-toml"),
            frame_index: FrameIndex::new(42),
            kind: AnchorKind::Manual,
            metadata: Metadata::new(),
        },
    );

    write_artifact(&path, ArtifactFormat::Toml, &artifact)
        .expect("supported TOML artifact should write");
    let decoded: PersistedAnchorArtifact =
        read_artifact_auto(&path, ArtifactKind::Anchor.schema())
            .expect("supported TOML artifact should auto-read");

    assert_eq!(decoded, artifact);
}

#[test]
fn artifact_format_inference_rejects_unknown_extensions_without_guessing() {
    assert_eq!(ArtifactFormat::from_path("artifact.json"), Some(ArtifactFormat::Json));
    assert_eq!(ArtifactFormat::from_path("artifact.toml"), Some(ArtifactFormat::Toml));
    assert_eq!(ArtifactFormat::from_path("artifact.bin"), None);
    assert_eq!(ArtifactFormat::from_path("artifact"), None);
}
