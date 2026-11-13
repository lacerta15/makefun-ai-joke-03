"""
Writes the entry's one-liner joke to output/entry.txt.

Deterministic, stdlib-only, no network, no randomness, no timestamps.
"""

from pathlib import Path

JOKE = (
    "I grepped the codebase for handleSubmit and got four matches: "
    "handleSubmit, handleSubmit2, handleSubmitNew, and handleSubmitFinal. "
    "My coding agent wrote all four in the same pull request."
)


def main() -> None:
    output_dir = Path("output")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "entry.txt"
    output_path.write_text(JOKE, encoding="utf-8")


if __name__ == "__main__":
    main()
