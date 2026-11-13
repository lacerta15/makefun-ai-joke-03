"""
Real tests for main.py: the validator's edge cases, the shipped joke's
validity, and the write behavior (determinism, correct path, guard
actually blocking bad input).

Run with: python -m unittest test_main.py -v
"""

import shutil
import unittest
from pathlib import Path

import main as main_module


class ValidateJokeTests(unittest.TestCase):
    def test_empty_string_fails(self):
        with self.assertRaisesRegex(main_module.JokeValidationError, "empty: 0 chars"):
            main_module.validate_joke("")

    def test_whitespace_only_fails(self):
        with self.assertRaisesRegex(main_module.JokeValidationError, "whitespace only"):
            main_module.validate_joke("   \n\t  ")

    def test_exactly_280_chars_passes(self):
        main_module.validate_joke("x" * 280)  # should not raise

    def test_281_chars_fails(self):
        with self.assertRaisesRegex(main_module.JokeValidationError, "too long: 281 chars"):
            main_module.validate_joke("x" * 281)

    def test_single_char_passes(self):
        main_module.validate_joke("x")  # should not raise

    def test_unicode_emoji_passes(self):
        main_module.validate_joke("deadpan \U0001F600 one-liner")  # should not raise

    def test_lone_surrogate_fails_utf8_check(self):
        with self.assertRaisesRegex(main_module.JokeValidationError, "not UTF-8 encodable"):
            main_module.validate_joke("bad \ud800 surrogate")

    def test_non_string_fails(self):
        with self.assertRaisesRegex(main_module.JokeValidationError, "not a string: int"):
            main_module.validate_joke(12345)  # type: ignore[arg-type]


class ShippedJokeTests(unittest.TestCase):
    def test_joke_passes_validation(self):
        main_module.validate_joke(main_module.JOKE)  # should not raise

    def test_joke_length_in_range(self):
        self.assertGreaterEqual(len(main_module.JOKE), 1)
        self.assertLessEqual(len(main_module.JOKE), 280)

    def test_joke_not_whitespace_only(self):
        self.assertNotEqual(main_module.JOKE.strip(), "")

    def test_joke_is_utf8_encodable(self):
        main_module.JOKE.encode("utf-8")  # should not raise

    def test_joke_has_no_exclamation_marks(self):
        self.assertNotIn("!", main_module.JOKE)


class MainWriteBehaviorTests(unittest.TestCase):
    def setUp(self):
        self.output_dir = Path("output")
        if self.output_dir.exists():
            shutil.rmtree(self.output_dir)

    def tearDown(self):
        if self.output_dir.exists():
            shutil.rmtree(self.output_dir)

    def test_main_creates_output_dir_and_file(self):
        self.assertFalse(self.output_dir.exists())
        main_module.main()
        output_path = self.output_dir / "entry.txt"
        self.assertTrue(output_path.exists())

    def test_main_writes_exact_joke_text_utf8(self):
        main_module.main()
        output_path = self.output_dir / "entry.txt"
        content = output_path.read_bytes().decode("utf-8")
        self.assertEqual(content, main_module.JOKE)

    def test_main_is_deterministic_across_runs(self):
        main_module.main()
        first = (self.output_dir / "entry.txt").read_bytes()
        main_module.main()
        second = (self.output_dir / "entry.txt").read_bytes()
        self.assertEqual(first, second)

    def test_main_rejects_invalid_joke_before_writing(self):
        # Prove the internal safety check is a real guard, not decoration:
        # if JOKE were invalid, main() must raise and must not write a file.
        original_joke = main_module.JOKE
        try:
            main_module.JOKE = "x" * 281  # too long
            with self.assertRaises(main_module.JokeValidationError):
                main_module.main()
            self.assertFalse((self.output_dir / "entry.txt").exists())
        finally:
            main_module.JOKE = original_joke

    def test_main_rejects_whitespace_only_joke_before_writing(self):
        original_joke = main_module.JOKE
        try:
            main_module.JOKE = "   "
            with self.assertRaises(main_module.JokeValidationError):
                main_module.main()
            self.assertFalse((self.output_dir / "entry.txt").exists())
        finally:
            main_module.JOKE = original_joke


if __name__ == "__main__":
    unittest.main()
