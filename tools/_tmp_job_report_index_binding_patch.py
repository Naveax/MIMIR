from pathlib import Path

path = Path("crates/mimir-export/src/lib.rs")
text = path.read_text(encoding="utf-8")

old_selected = '''    selected_entries\n        .iter()\n        .map(|entry| {\n            validate_execution_result_job_report_index_entry(entry, entry.ordinal)?;\n            load_execution_result_job_report(Path::new(&entry.report_file_path))\n        })\n        .collect()\n}\n'''
new_selected = '''    selected_entries\n        .iter()\n        .map(load_execution_result_job_report_for_index_entry)\n        .collect()\n}\n'''
if text.count(old_selected) != 1:
    raise SystemExit(f"selected report loader marker drift: {text.count(old_selected)}")
text = text.replace(old_selected, new_selected, 1)

old_indexed = '''    load_execution_result_job_report(Path::new(&entry.report_file_path))\n}\n\n/// Canonical report publication helper'''
new_indexed = '''    load_execution_result_job_report_for_index_entry(entry)\n}\n\nfn load_execution_result_job_report_for_index_entry(\n    entry: &ExecutionResultJobReportIndexEntry,\n) -> Result<ExecutionResultJobReport> {\n    validate_execution_result_job_report_index_entry(entry, entry.ordinal)?;\n    let report = load_execution_result_job_report(Path::new(&entry.report_file_path))?;\n    validate_execution_result_job_report_index_binding(entry, &report)?;\n    Ok(report)\n}\n\nfn validate_execution_result_job_report_index_binding(\n    entry: &ExecutionResultJobReportIndexEntry,\n    report: &ExecutionResultJobReport,\n) -> Result<()> {\n    let mismatch = |field: &str| {\n        MimirError::message(format!(\n            "execution result job report index binding mismatch for {field} at {}",\n            entry.report_file_path\n        ))\n    };\n\n    if entry.job_spec_id != report.job_spec_id {\n        return Err(mismatch("job_spec_id"));\n    }\n    if entry.source_run_request_id != report.source_run_request_id {\n        return Err(mismatch("source_run_request_id"));\n    }\n    if entry.source_handoff_bundle_id != report.source_handoff_bundle_id {\n        return Err(mismatch("source_handoff_bundle_id"));\n    }\n    if entry.export_name != report.export_name {\n        return Err(mismatch("export_name"));\n    }\n    if entry.selection_mode != report.selection_mode {\n        return Err(mismatch("selection_mode"));\n    }\n    if entry.expected_entry_count != report.expected_entry_count {\n        return Err(mismatch("expected_entry_count"));\n    }\n    if entry.source_provenance_hash != report.source_provenance_hash {\n        return Err(mismatch("source_provenance_hash"));\n    }\n\n    Ok(())\n}\n\n/// Canonical report publication helper'''
if text.count(old_indexed) != 1:
    raise SystemExit(f"indexed report loader marker drift: {text.count(old_indexed)}")
text = text.replace(old_indexed, new_indexed, 1)

path.write_text(text, encoding="utf-8", newline="\n")
