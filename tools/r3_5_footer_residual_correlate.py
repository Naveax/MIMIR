from __future__ import annotations

import json
from pathlib import Path

from r3_5_footer_residual_evidence import scan


def main() -> None:
    corpus_root = Path("test_corpus/largest_100")
    matrix_path = Path("target/r3_5_footer_matrix.jsonl")
    matrix_rows = {
        row["filename"]: row
        for row in (
            json.loads(line)
            for line in matrix_path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        )
    }

    manifest_rows = {
        row["filename"]: row
        for row in (
            json.loads(line)
            for line in (corpus_root / "manifest.jsonl").read_text(encoding="utf-8").splitlines()
            if line.strip()
        )
    }

    results = [scan(path) for path in sorted(corpus_root.glob("*.replay"))]
    variants = [
        row
        for row in results
        if not (row.residual_len == 4 and row.residual_hex == "00000000")
    ]

    print(f"noncanonical_residual_rows={len(variants)}")
    for result in variants:
        filename = Path(result.path).name
        manifest = manifest_rows[filename]
        matrix = matrix_rows[filename]
        tuple_text = "|".join(
            str(matrix[key])
            for key in (
                "major_version",
                "minor_version",
                "net_version",
                "game_type",
                "replay_version",
                "build_version",
            )
        )
        print(
            "variant "
            f"rank={manifest['rank']} fixture_id={manifest['fixture_id']} "
            f"filename={filename} bytes={manifest['bytes']} sha256={manifest['sha256']} "
            f"residual_len={result.residual_len} residual_hex={result.residual_hex or '<empty>'} "
            f"header_parse={matrix['header_parse']} tuple={tuple_text} "
            f"failure_category={matrix.get('failure_category')}"
        )

    if len(variants) != 1:
        raise RuntimeError(f"expected exactly one noncanonical residual row, found {len(variants)}")
    if variants[0].residual_len != 0:
        raise RuntimeError(
            f"expected the single variant to have zero residual bytes, found {variants[0].residual_len}"
        )
    print("PASS: single zero-residual variant correlated with manifest identity and replay version tuple.")


if __name__ == "__main__":
    main()
