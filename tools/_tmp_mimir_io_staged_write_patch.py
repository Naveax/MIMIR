from pathlib import Path

path = Path("crates/mimir-io/src/lib.rs")
text = path.read_text(encoding="utf-8")

old_import = "use std::fs;\nuse std::path::{Path, PathBuf};\n"
new_import = "use std::fs;\nuse std::io::Write;\nuse std::path::{Path, PathBuf};\nuse std::sync::atomic::{AtomicU64, Ordering};\n"
if text.count(old_import) != 1:
    raise SystemExit(f"mimir-io import marker drift: {text.count(old_import)}")
text = text.replace(old_import, new_import, 1)

old_function = '''pub fn write_artifact<T>(
    path: impl AsRef<Path>,
    format: ArtifactFormat,
    artifact: &ArtifactEnvelope<T>,
) -> Result<()>
where
    T: Serialize,
{
    let path = path.as_ref();
    let text = match format {
        ArtifactFormat::Json => serde_json::to_string_pretty(artifact)?,
        ArtifactFormat::Toml => toml::to_string_pretty(artifact)?,
    };

    fs::write(path, text).map_err(|error| MimirError::io(path, error))
}
'''
new_function = '''pub fn write_artifact<T>(
    path: impl AsRef<Path>,
    format: ArtifactFormat,
    artifact: &ArtifactEnvelope<T>,
) -> Result<()>
where
    T: Serialize,
{
    let path = path.as_ref();
    let text = match format {
        ArtifactFormat::Json => serde_json::to_string_pretty(artifact)?,
        ArtifactFormat::Toml => toml::to_string_pretty(artifact)?,
    };

    write_text_file_staged(path, &text)
}

static ARTIFACT_STAGE_NONCE: AtomicU64 = AtomicU64::new(0);

fn write_text_file_staged(path: &Path, text: &str) -> Result<()> {
    let parent = path.parent().unwrap_or_else(|| Path::new("."));
    let file_name = path.file_name().ok_or_else(|| {
        MimirError::message(format!("artifact path has no file name: {}", path.display()))
    })?;

    let mut stage = None;
    for _ in 0..128 {
        let nonce = ARTIFACT_STAGE_NONCE.fetch_add(1, Ordering::Relaxed);
        let candidate = parent.join(format!(
            ".{}.mimir-stage-{}-{nonce}",
            file_name.to_string_lossy(),
            std::process::id()
        ));
        match fs::OpenOptions::new()
            .write(true)
            .create_new(true)
            .open(&candidate)
        {
            Ok(file) => {
                stage = Some((candidate, file));
                break;
            }
            Err(error) if error.kind() == std::io::ErrorKind::AlreadyExists => continue,
            Err(error) => return Err(MimirError::io(&candidate, error)),
        }
    }

    let (stage_path, mut stage_file) = stage.ok_or_else(|| {
        MimirError::message(format!(
            "could not allocate unique staged artifact file for {}",
            path.display()
        ))
    })?;

    if let Err(error) = stage_file.write_all(text.as_bytes()) {
        drop(stage_file);
        let _ = fs::remove_file(&stage_path);
        return Err(MimirError::io(&stage_path, error));
    }
    if let Err(error) = stage_file.flush() {
        drop(stage_file);
        let _ = fs::remove_file(&stage_path);
        return Err(MimirError::io(&stage_path, error));
    }
    drop(stage_file);

    if let Err(error) = fs::rename(&stage_path, path) {
        let _ = fs::remove_file(&stage_path);
        return Err(MimirError::io(path, error));
    }

    Ok(())
}
'''
if text.count(old_function) != 1:
    raise SystemExit(f"write_artifact function marker drift: {text.count(old_function)}")
text = text.replace(old_function, new_function, 1)

marker = '''    #[test]\n    fn rejects_unsupported_schema_versions() {\n'''
if text.count(marker) != 1:
    raise SystemExit(f"test insertion marker drift: {text.count(marker)}")
tests = '''    #[test]\n    fn generic_artifact_writer_replaces_via_staged_file_without_leftovers() {\n        let directory = tempdir().expect("tempdir should be created");\n        let path = directory.path().join("artifact.json");\n        fs::write(&path, b"legacy-bytes").expect("seed destination");\n\n        let artifact = PersistedAnchorArtifact::new(\n            ArtifactHeader::for_kind(ArtifactKind::Anchor, "mimir-io-staged-write-test"),\n            AnchorArtifactPayload {\n                id: AnchorId::new("anchor-staged-write"),\n                replay_id: ReplayId::new("replay-staged-write"),\n                frame_index: FrameIndex::new(7),\n                kind: AnchorKind::Manual,\n                metadata: Metadata::new(),\n            },\n        );\n\n        write_artifact(&path, ArtifactFormat::Json, &artifact).expect("staged replacement");\n        let decoded: PersistedAnchorArtifact =\n            read_artifact_auto(&path, ArtifactKind::Anchor.schema()).expect("reload replacement");\n        assert_eq!(decoded, artifact);\n\n        let file_name = path.file_name().expect("file name").to_string_lossy();\n        let prefix = format!(".{file_name}.mimir-stage-");\n        let leftovers = fs::read_dir(directory.path())\n            .expect("read directory")\n            .map(|entry| entry.expect("entry").file_name().to_string_lossy().into_owned())\n            .filter(|name| name.starts_with(&prefix))\n            .collect::<Vec<_>>();\n        assert!(leftovers.is_empty(), "staged writer left temporary files: {leftovers:?}");\n    }\n\n    #[test]\n    fn generic_artifact_serialization_failure_preserves_existing_destination() {\n        let directory = tempdir().expect("tempdir should be created");\n        let path = directory.path().join("artifact.json");\n        let original = b"existing-safe-bytes";\n        fs::write(&path, original).expect("seed destination");\n\n        let artifact = PersistedAnchorArtifact::new(\n            ArtifactHeader::for_kind(ArtifactKind::Anchor, "mimir-io-staged-write-test")\n                .with_metadata(Metadata::from([(\n                    "non_finite",\n                    FieldValue::Float(f64::NAN),\n                )])),\n            AnchorArtifactPayload {\n                id: AnchorId::new("anchor-invalid"),\n                replay_id: ReplayId::new("replay-invalid"),\n                frame_index: FrameIndex::new(8),\n                kind: AnchorKind::Manual,\n                metadata: Metadata::new(),\n            },\n        );\n\n        write_artifact(&path, ArtifactFormat::Json, &artifact)\n            .expect_err("non-finite artifact serialization must fail");\n        assert_eq!(fs::read(&path).expect("read preserved destination"), original);\n    }\n\n'''
text = text.replace(marker, tests + marker, 1)
path.write_text(text, encoding="utf-8", newline="\n")
