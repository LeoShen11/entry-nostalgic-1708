#!/usr/bin/env python3
"""Make the AI Judge Feel Nostalgic: A Childhood Memory.

Writes one sentence (at most 280 characters) to /output/entry.txt.
Own validation: length cap, single line, exactly one sentence,
non-blank, and a sane word count, plus a read-back check that the
file on disk is byte-identical to the validated text.
"""

import os
import sys

ENTRY = (
    "Grandma saved the burnt corner of the rice for me, the piece that "
    "crackled like dry autumn leaves, and thirty years later I can still "
    "hear her slippers shuffling across the kitchen tiles at dusk."
)

MAX_CHARS = 280


def validate(text: str) -> list:
    problems = []
    if not text.strip():
        problems.append("entry is blank")
    if len(text) < 1:
        problems.append("entry is empty")
    if len(text) > MAX_CHARS:
        problems.append(
            "entry is %d chars, over the %d cap" % (len(text), MAX_CHARS)
        )
    if "\n" in text or "\r" in text:
        problems.append("entry must be a single line")
    if not text.rstrip().endswith("."):
        problems.append("entry must end with a full stop (one sentence)")
    if text.count(".") != 1:
        problems.append("entry must be exactly one sentence")
    words = text.split()
    if not 10 <= len(words) <= 60:
        problems.append("word count %d outside 10-60" % len(words))
    # The judge rewards concrete place/time/sensation: require at least
    # two sensory anchors (a food, a sound, a place) in the line.
    sensory = ("rice", "slippers", "tiles", "kitchen", "dusk", "leaves")
    hits = [w for w in sensory if w in text.lower()]
    if len(hits) < 2:
        problems.append("needs at least 2 sensory anchors, found %s" % hits)
    return problems


def main() -> int:
    problems = validate(ENTRY)
    if problems:
        for p in problems:
            print("INVALID: " + p, file=sys.stderr)
        return 1
    out_dir = os.environ.get("OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(ENTRY)
    # Read back and verify byte-identical.
    with open(path, "rb") as f:
        data = f.read()
    if data != ENTRY.encode("utf-8"):
        print("INVALID: read-back mismatch", file=sys.stderr)
        return 1
    print(
        "wrote %s: %d chars, %d words"
        % (path, len(ENTRY), len(ENTRY.split()))
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
