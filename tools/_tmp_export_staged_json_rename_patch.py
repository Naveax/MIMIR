from pathlib import Path

path = Path("crates/mimir-export/src/lib.rs")
text = path.read_text(encoding="utf-8")
old = '''    if path.exists() {
        fs::copy(&stage_path, path).map_err(|error| MimirError::io(path, error))?;
        fs::remove_file(&stage_path).map_err(|error| MimirError::io(&stage_path, error))?;
    } else {
        fs::rename(&stage_path, path).map_err(|error| MimirError::io(path, error))?;
    }
'''
new = '''    if let Err(error) = fs::rename(&stage_path, path) {
        let _ = fs::remove_file(&stage_path);
        return Err(MimirError::io(path, error));
    }
'''
count = text.count(old)
if count != 1:
    raise SystemExit(f"expected exactly one staged JSON replacement block, found {count}")
path.write_text(text.replace(old, new, 1), encoding="utf-8", newline="\n")
