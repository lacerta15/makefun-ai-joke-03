"""
Writes this entry's one-liner joke to output/entry.txt.

Deterministic, standard-library only, no network access, no randomness,
no timestamps. Running this script twice produces byte-identical output.
"""

from pathlib import Path

JOKE = (
    'I typed "wait, no" and hit enter half a second after the agent had '
    "already finished rewriting the file."
)

MIN_LENGTH = 1
MAX_LENGTH = 280


class JokeValidationError(ValueError):
    """Raised when a candidate joke string fails the bounty's requirements."""


def validate_joke(text: str) -> None:
    """Validate a joke string against the bounty's hard requirements:
    it must be 1-280 characters long, encodable as UTF-8, and not
    consist solely of whitespace.

    Raises JokeValidationError with a specific reason on failure.
    Returns None on success.
    """
    if not isinstance(text, str):
        raise JokeValidationError(f"not a string: {type(text).__name__}")

    length = len(text)

    if length < MIN_LENGTH:
        raise JokeValidationError(f"empty: {length} chars")

    if length > MAX_LENGTH:
        raise JokeValidationError(f"too long: {length} chars")

    if text.strip() == "":
        raise JokeValidationError(f"whitespace only: {length} chars")

    try:
        text.encode("utf-8")
    except UnicodeEncodeError as exc:
        raise JokeValidationError(f"not UTF-8 encodable: {exc}") from exc


def main() -> None:
    # Safety check: this guards against ever shipping an invalid entry,
    # not decoration. If JOKE above is edited into something invalid,
    # this raises and the script exits non-zero instead of writing a bad
    # file.
    validate_joke(JOKE)

    output_dir = Path("output")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "entry.txt"
    output_path.write_text(JOKE, encoding="utf-8")


if __name__ == "__main__":
    main()
