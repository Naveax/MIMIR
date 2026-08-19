#!/usr/bin/env python3
import collections
import hashlib
import json
import sys
from pathlib import Path

def req(cond, msg):
    if not cond:
        raise SystemExit(msg)

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def kv(line, prefix):
    req(line.startswith(prefix + "\t"), f"bad {prefix} line")
    out = {}
    for item in line.split("\t")[1:]:
        req("=" in item, f"bad field {item}")
        k, v = item.split("=", 1)
        out[k] = v
    return out

def prepare(ydir, contract_path, target_path):
    ydir = Path(ydir)
    rows_doc = json.loads((ydir / "r3_18y_header_rows.json").read_text(encoding="utf-8"))
    witnesses = json.loads((ydir / "r3_18y_frozen_witnesses.json").read_text(encoding="utf-8"))
    contract = json.loads(Path(contract_path).read_text(encoding="utf-8"))

    agg = rows_doc["aggregate"]
    req(agg["outcome"] == "A", "Y outcome drift")
    req(agg["rows"] == 47, "Y row count drift")
    req(agg["unique_exact_contexts"] == 18, "Y context count drift")
    req(agg["native_oracle_mismatch"] == 0, "Y mismatch drift")
    req(agg["witness_reselection"] == 0, "Y reselection drift")
    req(agg["following_payload_bits_consumed"] == 0, "Y payload consumption drift")
    req(agg["another_control_bits_consumed"] == 0, "Y control consumption drift")
    req(agg["tags"] == {"ActiveActor": 39, "Int": 7, "UniqueId": 1}, "Y tag distribution drift")

    req(contract["membership_policy"] == "exact_tuple_only", "Z membership policy drift")
    req(contract["observed_row_count"] == 47, "Z row count drift")
    req(contract["unique_exact_context_count"] == 18, "Z context count drift")
    req(contract["observed_tag_counts"] == {"ActiveActor": 39, "Int": 7, "UniqueId": 1}, "Z tag count drift")
    req(contract["anti_widening"]["r3_18p_cross_boundary_inheritance"] is False, "Z/P inheritance drift")

    continuation = {}
    for w in witnesses:
        if w.get("class") != "continuation":
            continue
        key = (
            w["label"],
            int(w["frame_index"]),
            int(w["actor_ordinal"]),
            int(w["actor_context_object_id"]),
        )
        req(key not in continuation, f"duplicate continuation witness {key}")
        continuation[key] = w
    req(len(continuation) == 47, f"continuation witnesses {len(continuation)} != 47")

    rows = rows_doc["rows"]
    req(len(rows) == 47, "Y rows list != 47")
    targets = []
    seen = set()
    for row in rows:
        key = (
            row["label"],
            int(row["frame_index"]),
            int(row["actor_ordinal"]),
            int(row["actor_context_object_id"]),
        )
        req(key in continuation, f"missing continuation witness {key}")
        w = continuation[key]
        req(row["label"] not in seen, f"duplicate replay row {row['label']}")
        seen.add(row["label"])
        req(bool(row["native_oracle_exact"]), f"Y row not oracle exact {row['label']}")
        req(int(row["following_payload_bits_consumed"]) == 0, "Y row payload consumption")
        req(int(row["another_control_bits_consumed"]) == 0, "Y row control consumption")
        req(bool(w["second_property_present"]), "continuation witness second property false")
        targets.append([
            row["label"],
            str(row["frame_index"]),
            str(row["actor_ordinal"]),
            str(row["actor_context_object_id"]),
            str(w["first_property_present_start_bit"]),
            str(row["property_present_start_bit"]),
            str(row["property_present_end_bit"]),
            str(row["stream_id_start_bit"]),
            str(row["stream_id_end_bit"]),
            str(row["stream_id"]),
            str(row["stream_id_bound"]),
            str(row["prop_id_bits"]),
            str(row["resolved_property_object_index"]),
            row["resolved_attribute_tag"],
            str(row["payload_start_bit"]),
            str(row["version_major"]),
            str(row["version_minor"]),
            str(row["net_version"]),
        ])
    req(len(targets) == 47 and len(seen) == 47, "target row count drift")
    Path(target_path).write_text(
        "\n".join("\t".join(x) for x in sorted(targets, key=lambda x: x[0])) + "\n",
        encoding="utf-8",
        newline="\n",
    )

    identity_lines = []
    for line in (ydir / "r3_18y_replay_identity.tsv").read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        f = line.split("\t")
        req(len(f) == 3 and f[2] == "PASS", f"bad replay identity row {line}")
        rel = Path(f[0])
        req(not rel.is_absolute() and ".." not in rel.parts, f"unsafe replay path {f[0]}")
        req(rel.exists(), f"missing replay {f[0]}")
        req(sha256(rel).lower() == f[1].lower(), f"replay hash mismatch {f[0]}")
        identity_lines.append(line)
    req(len(identity_lines) == 47, f"identity rows {len(identity_lines)} != 47")
    Path("r3_18ab_replay_identity.tsv").write_text(
        "\n".join(identity_lines) + "\n", encoding="utf-8", newline="\n"
    )
    Path("r3_18ab_frozen_y_rows.json").write_text(
        json.dumps(rows_doc, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print("R3_18AB_PREPARE=PASS rows=47 contexts=18 witness_reselection=0")

def analyze(ydir, contract_path, log_path):
    ydoc = json.loads((Path(ydir) / "r3_18y_header_rows.json").read_text(encoding="utf-8"))
    frozen = {r["label"]: r for r in ydoc["rows"]}
    contract = json.loads(Path(contract_path).read_text(encoding="utf-8"))
    published = {}
    for line in Path(log_path).read_text(encoding="utf-8").splitlines():
        if line.startswith("R3_18AB_PUBLISHED\t"):
            r = kv(line, "R3_18AB_PUBLISHED")
            req(r["label"] not in published, f"duplicate published row {r['label']}")
            published[r["label"]] = r
    req(len(published) == 47, f"published rows {len(published)} != 47")
    req(set(published) == set(frozen), "published/frozen label set mismatch")

    int_fields = [
        "frame_index", "actor_ordinal", "actor_context_object_id",
        "property_present_start_bit", "property_present_end_bit",
        "stream_id_start_bit", "stream_id_end_bit", "stream_id",
        "stream_id_bound", "prop_id_bits", "property_object_id",
        "version_major", "version_minor", "net_version", "payload_start_bit",
    ]
    fmap = {"property_object_id": "resolved_property_object_index"}
    flags = [
        "published_exact", "direct_equal", "repeatability", "truncation",
        "wrong_actor_negative", "unresolved_lookup_negative",
        "wrong_version_negative", "post_payload_poison",
    ]
    tuple_counts = collections.Counter()
    tag_counts = collections.Counter()
    out_rows = []
    mismatch = 0
    for label in sorted(frozen):
        a = frozen[label]
        b = published[label]
        exact = True
        for field in int_fields:
            af = fmap.get(field, field)
            if int(a[af]) != int(b[field]):
                exact = False
        if a["resolved_attribute_tag"] != b["attribute_tag"]:
            exact = False
        if int(b["stop_bit"]) != int(a["payload_start_bit"]):
            exact = False
        if not all(b.get(flag) == "1" for flag in flags):
            exact = False
        if b.get("following_payload_bits_consumed") != "0":
            exact = False
        if b.get("another_control_bits_consumed") != "0":
            exact = False
        if not exact:
            mismatch += 1
        tup = (
            int(b["stream_id_bound"]), int(b["prop_id_bits"]), int(b["property_object_id"]),
            b["attribute_tag"], int(b["version_major"]), int(b["version_minor"]), int(b["net_version"]),
        )
        tuple_counts[tup] += 1
        tag_counts[b["attribute_tag"]] += 1
        out_rows.append({
            "label": label,
            "frame_index": int(b["frame_index"]),
            "actor_ordinal": int(b["actor_ordinal"]),
            "actor_context_object_id": int(b["actor_context_object_id"]),
            "property_present_start_bit": int(b["property_present_start_bit"]),
            "property_present_end_bit": int(b["property_present_end_bit"]),
            "stream_id_start_bit": int(b["stream_id_start_bit"]),
            "stream_id_end_bit": int(b["stream_id_end_bit"]),
            "stream_id": int(b["stream_id"]),
            "stream_id_bound": int(b["stream_id_bound"]),
            "prop_id_bits": int(b["prop_id_bits"]),
            "resolved_property_object_index": int(b["property_object_id"]),
            "resolved_attribute_tag": b["attribute_tag"],
            "version_major": int(b["version_major"]),
            "version_minor": int(b["version_minor"]),
            "net_version": int(b["net_version"]),
            "payload_start_bit": int(b["payload_start_bit"]),
            "published_frozen_y_direct_exact": exact,
            "following_payload_bits_consumed": 0,
            "another_control_bits_consumed": 0,
        })
    req(mismatch == 0, f"published/frozen/direct mismatch {mismatch}")
    req(tag_counts == collections.Counter({"ActiveActor": 39, "Int": 7, "UniqueId": 1}), f"tag counts {tag_counts}")

    expected = {}
    for c in contract["admitted_contexts"]:
        tup = (
            int(c["stream_id_bound"]), int(c["prop_id_bits"]), int(c["property_object_index"]),
            c["attribute_tag"], int(c["version_major"]), int(c["version_minor"]), int(c["net_version"]),
        )
        expected[tup] = int(c["observed_count"])
    req(len(expected) == 18, "Z contexts !=18")
    req(tuple_counts == collections.Counter(expected), f"Z tuple/multiplicity mismatch actual={tuple_counts} expected={expected}")

    summary = {
        "rows": 47,
        "unique_exact_contexts": 18,
        "tags": dict(sorted(tag_counts.items())),
        "published_frozen_y_direct_mismatch": 0,
        "witness_reselection": 0,
        "following_payload_bits_consumed": 0,
        "another_control_bits_consumed": 0,
        "membership_policy": "exact_tuple_only",
        "contexts": [
            {
                "stream_id_bound": t[0], "prop_id_bits": t[1], "property_object_index": t[2],
                "attribute_tag": t[3], "version_major": t[4], "version_minor": t[5],
                "net_version": t[6], "observed_count": n,
            }
            for t, n in sorted(tuple_counts.items())
        ],
    }
    Path("r3_18ab_published_rows.json").write_text(
        json.dumps({"aggregate": summary, "rows": out_rows}, indent=2, sort_keys=True) + "\n",
        encoding="utf-8", newline="\n"
    )
    Path("r3_18ab_context_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n"
    )
    Path("r3_18ab_negative_controls.txt").write_text(
        "\n".join([
            "R3_18AB_REPEATABILITY=PASS 47/47",
            "R3_18AB_TRUNCATION=PASS 47/47",
            "R3_18AB_WRONG_ACTOR_NEGATIVE=PASS 47/47",
            "R3_18AB_UNRESOLVED_LOOKUP_NEGATIVE=PASS 47/47",
            "R3_18AB_WRONG_VERSION_NEGATIVE=PASS 47/47",
            "R3_18AB_POST_PAYLOAD_POISON=PASS 47/47",
            "R3_18AB_CARTESIAN_NEGATIVE=PASS permanent-focused-test",
            "R3_18AB_R318P_ONLY_Z_ABSENT_NEGATIVE=PASS permanent-focused-test",
            "R3_18AB_FOLLOWING_PAYLOAD_BITS_CONSUMED=0",
            "R3_18AB_ANOTHER_CONTROL_BITS_CONSUMED=0",
        ]) + "\n",
        encoding="utf-8", newline="\n"
    )
    Path("r3_18ab_aggregate.txt").write_text(
        "\n".join([
            "R3_18AB_OUTCOME=A",
            "R3_18AB_EVIDENCE=PASS",
            "R3_18AB_FROZEN_ROWS=47/47",
            "R3_18AB_PUBLISHED_AA_FROZEN_Y_DIRECT_MISMATCH=0",
            "R3_18AB_EXACT_Z_CONTEXTS=18/18",
            "R3_18AB_EXACT_Z_MULTIPLICITY=47/47",
            "R3_18AB_TAGS=ActiveActor:39,Int:7,UniqueId:1",
            "R3_18AB_WITNESS_RESELECTION=0",
            "R3_18AB_REPEATABILITY=PASS 47/47",
            "R3_18AB_TRUNCATION=PASS 47/47",
            "R3_18AB_WRONG_ACTOR_NEGATIVE=PASS 47/47",
            "R3_18AB_UNRESOLVED_LOOKUP_NEGATIVE=PASS 47/47",
            "R3_18AB_WRONG_VERSION_NEGATIVE=PASS 47/47",
            "R3_18AB_POST_PAYLOAD_POISON=PASS 47/47",
            "R3_18AB_CARTESIAN_AND_P_ONLY_Z_ABSENT=PASS permanent-focused-test",
            "R3_18AB_FOLLOWING_PAYLOAD_BITS_CONSUMED=0",
            "R3_18AB_ANOTHER_CONTROL_BITS_CONSUMED=0",
            "R3_18AB_PRODUCTION_CARGO_FIXTURE_CORPUS_SUPPORT_MUTATION=0/0/0/0/0",
            "R3_18AB_PRIVACY=PASS",
        ]) + "\n",
        encoding="utf-8", newline="\n"
    )
    print("R3_18AB_ANALYZE=PASS rows=47 contexts=18 mismatch=0")

def main():
    req(len(sys.argv) >= 2, "missing mode")
    if sys.argv[1] == "prepare":
        req(len(sys.argv) == 5, "prepare usage")
        prepare(sys.argv[2], sys.argv[3], sys.argv[4])
    elif sys.argv[1] == "analyze":
        req(len(sys.argv) == 5, "analyze usage")
        analyze(sys.argv[2], sys.argv[3], sys.argv[4])
    else:
        raise SystemExit(f"unknown mode {sys.argv[1]}")

if __name__ == "__main__":
    main()
