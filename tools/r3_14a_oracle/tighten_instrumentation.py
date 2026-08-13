from __future__ import annotations

import argparse
from pathlib import Path


def replace_exact(text: str, old: str, new: str, expected: int, label: str) -> str:
    count = text.count(old)
    if count != expected:
        raise SystemExit(f"{label}: expected {expected} matches, found {count}")
    return text.replace(old, new)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("boxcars_root")
    args = parser.parse_args()

    source = Path(args.boxcars_root).resolve() / "src" / "network" / "frame_decoder.rs"
    text = source.read_text(encoding="utf-8")

    text = replace_exact(
        text,
        "            if r3_14a_observe && !actor_present {\n",
        "            if r3_14a_observe\n"
        "                && !R3_14A_EVIDENCE_EMITTED.load(Ordering::Relaxed)\n"
        "                && !actor_present\n"
        "            {\n",
        1,
        "actor-present false emission guard",
    )

    old_actor_emit = (
        "                if r3_14a_observe {\n"
        "                    r3_14a_emit(\n"
    )
    new_actor_emit = (
        "                if r3_14a_observe\n"
        "                    && !R3_14A_EVIDENCE_EMITTED.load(Ordering::Relaxed)\n"
        "                {\n"
        "                    r3_14a_emit(\n"
    )
    text = replace_exact(
        text,
        old_actor_emit,
        new_actor_emit,
        2,
        "alive true/false actor emission guards",
    )

    source.write_text(text, encoding="utf-8")
    print(f"tightened={source}")
    print("single_first_actor_emission_guard=true")


if __name__ == "__main__":
    main()
