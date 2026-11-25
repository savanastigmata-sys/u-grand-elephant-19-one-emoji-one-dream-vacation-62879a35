"""One Emoji, One Dream Vacation — make.fun entry.

Writes exactly one emoji to $MAKEFUN_OUTPUT_DIR/entry.txt:
a shooting star (U+1F320 SHOOTING STAR) — one wish, one night
under a meteor shower in a dark-sky desert, the trip of a lifetime.

Deterministic, stdlib only, no network, no randomness, no clock.
"""

import os
import sys
import unicodedata

# U+1F320 SHOOTING STAR — a single code point, one grapheme cluster.
EMOJI = "\U0001F320"

OUTPUT_FILENAME = "entry.txt"


def resolve_output_dir():
    """Return the output directory, falling back to ./output."""
    out = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if out:
        return out
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")


def validate(text):
    """Enforce the competition gate: 1-8 chars, exactly one emoji."""
    if not isinstance(text, str):
        raise ValueError("entry must be text")
    if not 1 <= len(text) <= 8:
        raise ValueError("entry must be 1 to 8 characters")
    if text.strip() == "":
        raise ValueError("entry must not be only whitespace")
    if len(text) != 1:
        raise ValueError("entry must be exactly one character")
    if unicodedata.category(text) != "So":
        raise ValueError("entry must be a symbol (emoji)")
    if not (0x1F300 <= ord(text) <= 0x1FAFF or 0x2600 <= ord(text) <= 0x27BF):
        raise ValueError("entry must be an emoji code point")
    # A lone emoji with no variation selector or combining mark:
    # exactly 4 UTF-8 bytes, the smallest size the tie-break rewards.
    if len(text.encode("utf-8")) != 4:
        raise ValueError("entry must be a single 4-byte emoji")
    return text


def main():
    text = validate(EMOJI)
    out_dir = resolve_output_dir()
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, OUTPUT_FILENAME)
    # No trailing newline: the file is the emoji and nothing else.
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    # Read back and re-validate so a bad write can never pass silently.
    with open(path, "r", encoding="utf-8", newline="") as f:
        written = f.read()
    validate(written)
    if written != text:
        raise ValueError("written entry does not match the validated emoji")
    return 0


if __name__ == "__main__":
    sys.exit(main())
