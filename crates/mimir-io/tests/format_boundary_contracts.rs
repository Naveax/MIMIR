use mimir_io::{
    ArtifactFormat, read_artifact_auto, read_artifact_header_auto, write_artifact,
};
use mimir_types::{
    AnchorArtifactPayload, AnchorId, AnchorKind, ArtifactHeader, ArtifactKind, FrameIndex,
    Metadata, PersistedAnchorArtifact, ReplayId,
};
use tempfile::tempdir;

fn sample_anchor() -> PersistedAnchorArtifact {
    PersistedAnchorArtifact::new(
        ArtifactHeader::for_kind(ArtifactKind::Anchor, "mimir-io-format-contract-tests"),
        AnchorArtifactPayload {
            id: AnchorId::new("anchor-format-1"),
            replay_id: ReplayId::new("replay-format-1"),
            frame_index: FrameIndex::new(7),
            kind: AnchorKind::Manual,
            metadata: Metadata::new(),
        },
    )
}

#[test]
fn explicit_json_and_toml_writes_round_trip_through_auto_read() {
    let directory = tempdir().expect("tempdir should be created");
    let artifact = sample_anchor();

    for (extension, format) in [
        ("json", ArtifactFormat::Json),
        ("toml", ArtifactFormat::Toml),
    ] {
        let path = directory.path().join(format!("anchor.{extension}"));
        write_artifact(&path, format, &artifact).expect("artifact should write");

        let decoded = read_artifact_auto::<AnchorArtifactPayload>(
            &path,
            ArtifactKind::Anchor.schema(),
        )
        .expect("auto read should infer the matching format");

        assert_eq!(decoded, artifact);
    }
}

#[test]
fn auto_read_fails_closed_when_path_extension_disagrees_with_written_format() {
    let directory = tempdir().expect("tempdir should be created");
    let path = directory.path().join("anchor.json");
    let artifact = sample_anchor();

    write_artifact(&path, ArtifactFormat::Toml, &artifact)
        .expect("explicit writer should honor the requested format");

    assert!(
        read_artifact_auto::<AnchorArtifactPayload>(&path, ArtifactKind::Anchor.schema()).is_err(),
        "auto read must not silently reinterpret TOML bytes stored under a .json path"
    );
}

#[test]
fn auto_header_read_rejects_unknown_extension_before_claiming_a_format() {
    let directory = tempdir().expect("tempdir should be created");
    let path = directory.path().join("anchor.yaml");

    let error = read_artifact_header_auto(&path)
        .expect_err("unknown artifact extensions should fail closed");

    assert!(error.to_string().contains("cannot infer artifact format"));
}
