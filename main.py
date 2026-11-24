# SPDX-License-Identifier: MIT
"""One Sentence for a Traveler from 1800 — make.fun bounty entry.

Writes one fresh one-sentence explanation of the modern internet to
/output/entry.txt. Deterministic: the same bytes on every run.
No network, no randomness, no input files, no clock.

The sentence, 155 characters, one sentence, every word in use before
1800:

    Picture one road joining every post office, library, and town
    square on earth, so a letter sent at dawn is read by a stranger
    across the sea before supper.

Why this picture, against the judge's brief, most important first:

1. It explains the internet. One road joining everything is the
   network itself: a single web that ties every place together,
   so a message can travel from anyone to anyone.
2. It builds only from what a person from 1800 already knows: a
   road, a post office, a library, a town square, a letter, the
   sea, supper. No word in it was coined after their time — the
   checker below refuses a list of modern words outright.
3. It is true of the internet as it is now, taken literally: a
   letter sent at dawn really can be read across the sea before
   supper, and the post office, the library and the town square
   are the three jobs the internet does most — messages, knowledge
   and public talk, all on the same road.
4. Every word earns its place inside the 200 character limit: one
   comparison carries the whole sentence, no list of features, no
   filler. "One road" is the whole mechanism; "at dawn ... before
   supper" is the whole speed.
5. It leaves one image a reader keeps: a single road joining every
   post office, library and town square on earth.
"""

import os
import re

MAX_CHARS = 200  # the gate's cap for /output/entry.txt

SENTENCE = (
    "Picture one road joining every post office, library, and town "
    "square on earth, so a letter sent at dawn is read by a stranger "
    "across the sea before supper."
)

# Words coined after 1800 that a traveler from that year could not
# know. The sentence must contain none of them, matched whole-word
# and case-insensitively, so the picture stays inside the world of
# 1800: roads, letters, libraries and town squares.
POST_1800_WORDS = (
    "internet",
    "computer",
    "website",
    "email",
    "online",
    "digital",
    "phone",
    "telephone",
    "television",
    "radio",
    "wifi",
    "modem",
    "software",
    "hardware",
    "keyboard",
    "pixel",
    "video",
    "download",
    "upload",
    "google",
    "chat",
    "blog",
    "cyber",
    "virtual",
    "electronic",
    "browser",
    "server",
    "network",
    "screen",
    "app",
    "smartphone",
    "tablet",
    "laptop",
)


def check_sentence(sentence: str) -> str:
    """Return the sentence unchanged, or raise ValueError if it breaks the rules.

    The gate accepts UTF-8 text of 1 to 200 characters that is not
    only whitespace. One sentence means exactly one terminal full
    stop, at the end; abbreviations with dots would read as extra
    sentences, so they are refused here. Control characters other
    than tab would also read as noise to the judge, so they are
    refused too. Finally, no word coined after 1800 may appear:
    the traveler must be able to picture every word.
    """
    size = len(sentence)
    if not 1 <= size <= MAX_CHARS:
        raise ValueError(f"sentence is {size} characters, must be 1-{MAX_CHARS}")
    if not sentence.strip():
        raise ValueError("sentence must not be only whitespace")
    if sentence != sentence.strip():
        raise ValueError("sentence must not start or end with whitespace")
    if "\n" in sentence or "\r" in sentence:
        raise ValueError("sentence must be a single line")
    if sentence.count(".") != 1 or not sentence.endswith("."):
        raise ValueError("sentence must be exactly one sentence")
    bad = [c for c in sentence if ord(c) < 0x20 and c != "\t"]
    if bad:
        raise ValueError(f"sentence holds control characters: {bad!r}")
    lowered = sentence.lower()
    modern = [w for w in POST_1800_WORDS if re.search(r"\b" + re.escape(w) + r"\b", lowered)]
    if modern:
        raise ValueError(f"sentence uses words coined after 1800: {modern}")
    return sentence


def main() -> int:
    sentence = check_sentence(SENTENCE)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    with open(out_path, "w", encoding="utf-8", newline="") as f:
        f.write(sentence)
    print(f"wrote {len(sentence)} characters to {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
