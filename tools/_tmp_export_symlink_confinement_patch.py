from pathlib import Path

path = Path("crates/mimir-export/src/lib.rs")
text = path.read_text(encoding="utf-8")

old_manifest = '''    let manifest_path = bundle_dir.join(EXPORT_MANIFEST_FILE_NAME);\n'''
new_manifest = '''    let manifest_path = resolve_existing_confined_path(bundle_dir, EXPORT_MANIFEST_FILE_NAME)?;\n'''
if text.count(old_manifest) != 1:
    raise SystemExit(f"expected one manifest path join, found {text.count(old_manifest)}")
text = text.replace(old_manifest, new_manifest, 1)

old_index = '''    let index_path = resolve_relative_path(bundle_dir, &manifest.relative_index_path)?;\n'''
new_index = '''    let index_path = resolve_existing_confined_path(bundle_dir, &manifest.relative_index_path)?;\n'''
if text.count(old_index) != 1:
    raise SystemExit(f"expected one export index read path, found {text.count(old_index)}")
text = text.replace(old_index, new_index, 1)

old_artifact = '''        let artifact_path = resolve_relative_path(bundle_dir, &entry.relative_path)?;\n'''
new_artifact = '''        let artifact_path = resolve_existing_confined_path(bundle_dir, &entry.relative_path)?;\n'''
if text.count(old_artifact) != 2:
    raise SystemExit(f"expected two export artifact read paths, found {text.count(old_artifact)}")
text = text.replace(old_artifact, new_artifact)

marker = '''fn resolve_relative_path(root: &Path, relative_path: &str) -> Result<PathBuf> {\n    let relative = validate_relative_path_text(relative_path)?;\n    Ok(root.join(relative))\n}\n\n'''
if text.count(marker) != 1:
    raise SystemExit(f"expected one resolve_relative_path helper, found {text.count(marker)}")
addition = marker + '''fn resolve_existing_confined_path(root: &Path, relative_path: &str) -> Result<PathBuf> {\n    let root_metadata = fs::symlink_metadata(root).map_err(|error| MimirError::io(root, error))?;\n    if root_metadata.file_type().is_symlink() || !root_metadata.is_dir() {\n        return Err(MimirError::message(format!(\n            "export bundle root must be a non-symlink directory: {}",\n            root.display()\n        )));\n    }\n\n    let relative = validate_relative_path_text(relative_path)?;\n    let component_count = relative.components().count();\n    let mut current = root.to_path_buf();\n\n    for (index, component) in relative.components().enumerate() {\n        let Component::Normal(part) = component else {\n            return Err(MimirError::message(format!(\n                "export path component is not normal: {relative_path}"\n            )));\n        };\n        current.push(part);\n\n        let metadata =\n            fs::symlink_metadata(&current).map_err(|error| MimirError::io(&current, error))?;\n        if metadata.file_type().is_symlink() {\n            return Err(MimirError::message(format!(\n                "symlink traversal is not allowed in export bundle path: {}",\n                current.display()\n            )));\n        }\n\n        let is_final = index + 1 == component_count;\n        if !is_final && !metadata.is_dir() {\n            return Err(MimirError::message(format!(\n                "export bundle path component must be a directory: {}",\n                current.display()\n            )));\n        }\n        if is_final && !metadata.is_file() {\n            return Err(MimirError::message(format!(\n                "export bundle target must be a regular file: {}",\n                current.display()\n            )));\n        }\n    }\n\n    Ok(current)\n}\n\n'''
text = text.replace(marker, addition, 1)

if text.count("resolve_existing_confined_path") != 5:
    raise SystemExit("confined-path call/helper count drift")

path.write_text(text, encoding="utf-8", newline="\n")
