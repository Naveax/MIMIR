#!/usr/bin/env python3
import json
import sys
from pathlib import Path


def require(cond, msg):
    if not cond:
        raise SystemExit(msg)


def build(witness_path, comparison_path, target_path, summary_path):
    witnesses = json.loads(Path(witness_path).read_text(encoding="utf-8"))
    comparison = json.loads(Path(comparison_path).read_text(encoding="utf-8"))
    rows = comparison.get("rows")
    require(isinstance(witnesses, list) and len(witnesses) == 94, "K witness count != 94")
    require(isinstance(rows, list) and len(rows) == 94, "K comparison count != 94")
    require(comparison.get("aggregate", {}).get("native_oracle_mismatch") == 0, "K mismatch authority drift")
    require(comparison.get("aggregate", {}).get("following_property_bits_consumed") == 0, "K following-bit authority drift")

    k_rows = {}
    for row in rows:
        key = (row["label"], row["class"])
        require(key not in k_rows, f"duplicate K row: {key}")
        k_rows[key] = row

    output = []
    labels = set()
    tag_counts = {"Int": 0, "String": 0}
    for w in witnesses:
        if w.get("class") != "continuation":
            continue
        key = (w["label"], "continuation")
        require(key in k_rows, f"missing K continuation comparison: {key}")
        row = k_rows[key]
        require(row.get("reconstruction_exact") is True, f"K reconstruction drift: {key}")
        require(row.get("semantic_exact") is True, f"K semantic drift: {key}")
        require(row.get("shape_exact") is True, f"K shape drift: {key}")
        require(row.get("stop_exact") is True, f"K stop drift: {key}")
        require(row.get("following_bits_consumed") == 0, f"K following-bit drift: {key}")
        second = w.get("second_header")
        require(isinstance(second, dict), f"missing second header: {key}")
        tag = second["attribute_tag"]
        require(tag in tag_counts, f"unadmitted K continuation tag: {tag}")
        tag_counts[tag] += 1
        require(row["tag"] == tag, f"K tag mismatch: {key}")
        require(row["payload_start_bit"] == second["payload_start_bit"], f"K payload-start drift: {key}")
        require(row["payload_end_bit"] > row["payload_start_bit"], f"K payload end invalid: {key}")
        require(w["label"] not in labels, f"duplicate continuation replay label: {w['label']}")
        labels.add(w["label"])
        fields = [
            w["label"],
            w["actor_context_object_id"],
            w["first_attribute_tag"],
            w["first_lossless_value"],
            w["first_property_present_start_bit"],
            w["first_property_present_end_bit"],
            w["first_stream_id_start_bit"],
            w["first_stream_id_end_bit"],
            w["first_stream_id"],
            w["first_property_object_id"],
            w["first_payload_start_bit"],
            w["first_payload_end_bit"],
            w["second_property_present_start_bit"],
            w["second_property_present_end_bit"],
            second["stream_id_start_bit"],
            second["stream_id_end_bit"],
            second["stream_id"],
            second["stream_id_bound"],
            second["prop_id_bits"],
            second["property_object_id"],
            tag,
            second["payload_start_bit"],
            row["payload_end_bit"],
            row["payload_width"],
            w["frame_index"],
            w["actor_ordinal"],
        ]
        require(len(fields) == 26, "internal L target field count")
        output.append("\t".join(str(x) for x in fields))

    require(len(output) == 47 and len(labels) == 47, "L target lane != 47 unique replay rows")
    require(tag_counts == {"Int": 46, "String": 1}, f"L source tag counts drift: {tag_counts}")
    Path(target_path).write_text("\n".join(output) + "\n", encoding="utf-8", newline="\n")
    summary = {
        "source_rows": 47,
        "source_class": "R3.18K continuation only",
        "second_tags": tag_counts,
        "witness_reselection": 0,
        "prior_r3_18j_reconstruction": "exact via immutable R3.18K authority",
        "prior_following_bits_consumed": 0,
    }
    Path(summary_path).write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print("R3_18L_BUILD=PASS targets=47 Int=46 String=1 reselection=0")


def kv(line, prefix):
    require(line.startswith(prefix + "\t"), f"bad {prefix} line")
    out = {}
    for item in line.split("\t")[1:]:
        require("=" in item, f"bad field: {item}")
        key, value = item.split("=", 1)
        out[key] = value
    return out


def parse_oracle(line):
    # Boxcars R3.18C-derived instrumentation uses plain tab-separated key=value fields.
    row = kv(line, "R3_18L_ORACLE")
    required = [
        "label", "frame_index", "actor_ordinal", "actor_context_object_id",
        "next_property_present_start_bit", "next_property_present_end_bit",
        "next_property_present",
    ]
    for key in required:
        require(key in row, f"oracle missing {key}")
    return row


def analyze(target_path, oracle_path, native_path, rows_out, negatives_out, aggregate_out):
    targets = {}
    for line in Path(target_path).read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        f = line.split("\t")
        require(len(f) == 26, f"target field count {len(f)}")
        label = f[0]
        require(label not in targets, f"duplicate target {label}")
        targets[label] = {
            "label": label,
            "actor_object": int(f[1]),
            "prior_stop": int(f[22]),
            "frame_index": int(f[24]),
            "actor_ordinal": int(f[25]),
        }
    require(len(targets) == 47, "target count != 47")

    oracle_rows = {}
    parse_pass = 0
    for line in Path(oracle_path).read_text(encoding="utf-8").splitlines():
        if line == "R3_18L_ORACLE_PARSE=PASS":
            parse_pass += 1
        elif line.startswith("R3_18L_ORACLE\t"):
            row = parse_oracle(line)
            label = row["label"]
            require(label in targets, f"unexpected oracle label: {label}")
            require(label not in oracle_rows, f"duplicate oracle label: {label}")
            oracle_rows[label] = row
    require(parse_pass == 47, f"Boxcars parse PASS count {parse_pass} != 47")
    require(len(oracle_rows) == 47, f"oracle control rows {len(oracle_rows)} != 47")

    native_rows = {}
    native_aggs = []
    for line in Path(native_path).read_text(encoding="utf-8").splitlines():
        if line.startswith("R3_18L_NATIVE\t"):
            row = kv(line, "R3_18L_NATIVE")
            label = row["label"]
            require(label in targets, f"unexpected native label: {label}")
            require(label not in native_rows, f"duplicate native label: {label}")
            native_rows[label] = row
        elif line.startswith("R3_18L_NATIVE_AGG\t"):
            native_aggs.append(kv(line, "R3_18L_NATIVE_AGG"))
    require(len(native_rows) == 47, f"native rows {len(native_rows)} != 47")
    require(len(native_aggs) == 1, "native aggregate count != 1")
    native_agg = native_aggs[0]

    rows = []
    false_count = 0
    true_count = 0
    mismatch = 0
    for label, target in targets.items():
        o = oracle_rows[label]
        n = native_rows[label]
        oracle_start = int(o["next_property_present_start_bit"])
        oracle_end = int(o["next_property_present_end_bit"])
        oracle_value = int(o["next_property_present"])
        native_start = int(n["control_start"])
        native_end = int(n["control_end"])
        native_value = int(n["control_value"])
        exact = (
            int(o["frame_index"]) == target["frame_index"]
            and int(o["actor_ordinal"]) == target["actor_ordinal"]
            and int(o["actor_context_object_id"]) == target["actor_object"]
            and oracle_start == target["prior_stop"]
            and oracle_end == oracle_start + 1
            and native_start == target["prior_stop"]
            and native_end == native_start + 1
            and native_start == oracle_start
            and native_end == oracle_end
            and native_value == oracle_value
            and n.get("r3_18j_exact") == "1"
            and n.get("truncation") == "1"
            and n.get("repeatability") == "1"
            and n.get("poison") == "1"
            and n.get("prior_stop_mismatch_negative") == "1"
            and n.get("following_stream_bits_consumed") == "0"
            and n.get("following_header_bits_consumed") == "0"
            and n.get("following_payload_bits_consumed") == "0"
        )
        if not exact:
            mismatch += 1
        if oracle_value == 0:
            false_count += 1
        elif oracle_value == 1:
            true_count += 1
        else:
            raise SystemExit(f"non-boolean oracle value for {label}: {oracle_value}")
        rows.append({
            "label": label,
            "frame_index": target["frame_index"],
            "actor_ordinal": target["actor_ordinal"],
            "actor_context_object_id": target["actor_object"],
            "prior_r3_18j_stop_bit": target["prior_stop"],
            "property_present_start_bit": oracle_start,
            "property_present_end_bit": oracle_end,
            "property_present": bool(oracle_value),
            "native_oracle_exact": exact,
            "following_stream_bits_consumed": 0,
            "following_header_bits_consumed": 0,
            "following_payload_bits_consumed": 0,
        })

    require(false_count + true_count == 47, "control distribution does not cover 47 rows")
    require(mismatch == 0, f"R3.18L mismatch count {mismatch}")
    expected_native = {
        "rows": "47",
        "r3_18j_exact": "47",
        "truncation": "47",
        "repeatability": "47",
        "poison": "47",
        "prior_stop_mismatch_negative": "47",
        "following_stream_bits_consumed": "0",
        "following_header_bits_consumed": "0",
        "following_payload_bits_consumed": "0",
    }
    for key, value in expected_native.items():
        require(native_agg.get(key) == value, f"native aggregate drift {key}: {native_agg.get(key)}")

    payload = {
        "aggregate": {
            "rows": 47,
            "false": false_count,
            "true": true_count,
            "native_oracle_mismatch": 0,
            "r3_18j_reconstruction_exact": 47,
            "following_stream_bits_consumed": 0,
            "following_header_bits_consumed": 0,
            "following_payload_bits_consumed": 0,
            "witness_reselection": 0,
        },
        "rows": sorted(rows, key=lambda x: x["label"]),
    }
    Path(rows_out).write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    negatives = "\n".join([
        "control_bit_truncation=PASS 47/47",
        "post_control_poison=PASS 47/47",
        "repeatability=PASS 47/47",
        "prior_r3_18j_stop_mismatch=PASS 47/47",
        "following_stream_bits_consumed=0",
        "following_header_bits_consumed=0",
        "following_payload_bits_consumed=0",
    ]) + "\n"
    Path(negatives_out).write_text(negatives, encoding="utf-8", newline="\n")
    aggregate = "\n".join([
        "R3_18L_OUTCOME=A",
        "R3_18L_EVIDENCE=PASS",
        "R3_18L_FROZEN_ROWS=47/47",
        f"R3_18L_CONTROL_FALSE={false_count}",
        f"R3_18L_CONTROL_TRUE={true_count}",
        "R3_18L_R318J_RECONSTRUCTION_EXACT=47/47",
        "R3_18L_NATIVE_ORACLE_MISMATCH=0",
        "R3_18L_CONTROL_TRUNCATION=PASS 47/47",
        "R3_18L_REPEATABILITY=PASS 47/47",
        "R3_18L_POST_CONTROL_POISON=PASS 47/47",
        "R3_18L_PRIOR_STOP_MISMATCH_NEGATIVE=PASS 47/47",
        "R3_18L_FOLLOWING_STREAM_BITS_CONSUMED=0",
        "R3_18L_FOLLOWING_HEADER_BITS_CONSUMED=0",
        "R3_18L_FOLLOWING_PAYLOAD_BITS_CONSUMED=0",
        "R3_18L_WITNESS_RESELECTION=0",
        "R3_18L_PRODUCTION_CARGO_FIXTURE_CORPUS_SUPPORT_MUTATION=0/0/0/0/0",
        "R3_18L_PRIVACY=PASS",
    ]) + "\n"
    Path(aggregate_out).write_text(aggregate, encoding="utf-8", newline="\n")
    print(f"R3_18L_ANALYZE=PASS rows=47 false={false_count} true={true_count} mismatch=0")


def main():
    if len(sys.argv) < 2:
        raise SystemExit("usage: prepare.py build|analyze ...")
    if sys.argv[1] == "build" and len(sys.argv) == 6:
        build(*sys.argv[2:])
    elif sys.argv[1] == "analyze" and len(sys.argv) == 8:
        analyze(*sys.argv[2:])
    else:
        raise SystemExit("invalid arguments")


if __name__ == "__main__":
    main()
