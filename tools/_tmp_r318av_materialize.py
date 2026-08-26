from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

as_dir = Path(sys.argv[1])
contract_path = Path(sys.argv[2])
out_path = Path(sys.argv[3])

contract = json.loads(contract_path.read_text(encoding="utf-8"))
assert contract["status"] == "admitted"
assert contract["membership_policy"] == "exact_tuple_only"
assert contract["frozen_lane_row_count"] == 47
assert contract["false_terminator_count"] == 7
assert contract["observed_header_row_count"] == 40
assert contract["unique_exact_context_count"] == 16
assert contract["observed_tag_counts"] == {"Int": 40}

tuple_fields = contract["tuple_fields"]
assert tuple_fields == [
    "stream_id_bound",
    "prop_id_bits",
    "property_object_index",
    "attribute_tag",
    "version_major",
    "version_minor",
    "net_version",
    "is_rl_223",
]

order: list[str] = []
seen: set[str] = set()
for line in (as_dir / "r3_18as_frozen_control_rows.tsv").read_text(encoding="utf-8").splitlines():
    if not line.strip():
        continue
    fields: dict[str, str] = {}
    for part in line.split("\t")[1:]:
        key, value = part.split("=", 1)
        fields[key] = value
    label = fields["label"]
    assert label not in seen
    seen.add(label)
    order.append(label)
assert len(order) == 47

targets: dict[str, dict[str, object]] = {}
for name in ("r3_18as_continuation_targets.tsv", "r3_18as_terminator_rows.tsv"):
    for line in (as_dir / name).read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        parts = line.split("\t")
        assert len(parts) == 8
        label, frame, actor, actor_object, first_start, control_start, control_end, control_value = parts
        assert label not in targets
        targets[label] = {
            "label": label,
            "frame_index": int(frame),
            "actor_ordinal": int(actor),
            "actor_context_object_id": int(actor_object),
            "first_start": int(first_start),
            "control_start": int(control_start),
            "control_end": int(control_end),
            "control_value": bool(int(control_value)),
        }
assert len(targets) == 47 and set(targets) == set(order)

header_rows = json.loads((as_dir / "r3_18as_header_rows.json").read_text(encoding="utf-8"))["rows"]
headers = {row["label"]: row for row in header_rows}
assert len(headers) == 40

observed = Counter(
    tuple(row[field] for field in tuple_fields)
    for row in header_rows
)
admitted = Counter()
for context in contract["admitted_contexts"]:
    admitted[tuple(context[field] for field in tuple_fields)] += int(context["observed_count"])
assert len(admitted) == 16
assert sum(admitted.values()) == 40
assert observed == admitted

columns = [
    "label", "frame_index", "actor_ordinal", "actor_context_object_id", "first_start",
    "control_start", "control_end", "control_value", "stream_start", "stream_end", "stream_id",
    "stream_id_bound", "prop_id_bits", "property_object_index", "attribute_tag", "payload_start_bit",
    "header_stop_bit", "version_major", "version_minor", "net_version", "is_rl_223",
]
lines = ["\t".join(columns)]
false_count = 0
true_count = 0
for label in order:
    target = targets[label]
    header = headers.get(label)
    if not target["control_value"]:
        false_count += 1
        assert header is None
        row = dict(target)
    else:
        true_count += 1
        assert header is not None
        row = {
            **target,
            **{key: header[key] for key in (
                "stream_start", "stream_end", "stream_id", "stream_id_bound", "prop_id_bits",
                "property_object_index", "attribute_tag", "payload_start_bit", "header_stop_bit",
                "version_major", "version_minor", "net_version", "is_rl_223",
            )},
        }
    values: list[str] = []
    for key in columns:
        value = row.get(key)
        if value is None:
            values.append("")
        elif isinstance(value, bool):
            values.append(str(value).lower())
        else:
            values.append(str(value))
    assert len(values) == 21
    lines.append("\t".join(values))

assert false_count == 7 and true_count == 40 and len(lines) == 48
out_path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
print("R3_18AV_MATERIALIZE=PASS rows=47 false=7 true=40 contexts=16 multiplicity=40")
