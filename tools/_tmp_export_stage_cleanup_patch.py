from __future__ import annotations

from pathlib import Path

LIB = Path("crates/mimir-export/src/lib.rs")
text = LIB.read_text(encoding="utf-8")

fn_start = text.find("pub fn export_bundle(")
fn_end = text.find("\npub fn load_export_manifest(", fn_start)
if fn_start < 0 or fn_end < 0:
    raise SystemExit("export_bundle function boundary not found")

before = text[:fn_start]
function = text[fn_start:fn_end]
after = text[fn_end:]

stage_marker = "    create_stage_root(&stage_dir)?;\n"
if function.count(stage_marker) != 1:
    raise SystemExit(
        f"expected one create_stage_root marker in export_bundle, got {function.count(stage_marker)}"
    )
function = function.replace(
    stage_marker,
    stage_marker + "    let staged_result = (|| -> Result<()> {\n",
    1,
)

publish_marker = (
    "    fs::rename(&stage_dir, output_dir).map_err(|error| MimirError::io(output_dir, error))?;\n"
    "\n"
    "    Ok(manifest)\n"
    "}\n"
)
if function.count(publish_marker) != 1:
    raise SystemExit(
        f"expected one export publish marker, got {function.count(publish_marker)}"
    )
function = function.replace(
    publish_marker,
    "    fs::rename(&stage_dir, output_dir).map_err(|error| MimirError::io(output_dir, error))?;\n"
    "\n"
    "        Ok(())\n"
    "    })();\n"
    "\n"
    "    if let Err(error) = staged_result {\n"
    "        // Cleanup is intentionally best-effort: preserve the original export error.\n"
    "        // The path is the exact private stage directory allocated by this invocation.\n"
    "        let _ = fs::remove_dir_all(&stage_dir);\n"
    "        return Err(error);\n"
    "    }\n"
    "\n"
    "    Ok(manifest)\n"
    "}\n",
    1,
)

patched = before + function + after
if patched == text:
    raise SystemExit("stage cleanup patch made no change")
if patched.count("let staged_result = (|| -> Result<()> {") != 1:
    raise SystemExit("stage cleanup guard count drift")
if patched.count("let _ = fs::remove_dir_all(&stage_dir);") != 1:
    raise SystemExit("stage cleanup removal count drift")

LIB.write_text(patched, encoding="utf-8", newline="\n")
