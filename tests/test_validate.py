import sys
import os
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import validate_dataset

class TestValidator(unittest.TestCase):

    def _write_file(self, tmpdir, name, content):
        path = os.path.join(tmpdir, name)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return path

    def test_clean_file_returns_no_violations(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            self._write_file(tmpdir, "001.txt",
                "the man went to the house <EOL> he got water and food <EOL>")
            violations = validate_dataset.check_directory(tmpdir)
            self.assertEqual(violations, {})

    def test_file_with_bad_word_is_flagged(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            self._write_file(tmpdir, "001.txt",
                "the man walked to the house <EOL>")
            violations = validate_dataset.check_directory(tmpdir)
            self.assertIn("001.txt", violations)
            self.assertIn("walked", violations["001.txt"])

    def test_eol_token_is_always_valid(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            self._write_file(tmpdir, "001.txt",
                "<EOL> <EOL> the man <EOL>")
            violations = validate_dataset.check_directory(tmpdir)
            self.assertEqual(violations, {})

    def test_case_insensitive_matching(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            self._write_file(tmpdir, "001.txt",
                "I want to go <EOL> We have food <EOL>")
            violations = validate_dataset.check_directory(tmpdir)
            self.assertEqual(violations, {})

    def test_multiple_files_all_reported(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            self._write_file(tmpdir, "001.txt", "the man ran <EOL>")
            self._write_file(tmpdir, "002.txt", "a woman danced <EOL>")
            violations = validate_dataset.check_directory(tmpdir)
            self.assertIn("001.txt", violations)
            self.assertIn("002.txt", violations)

    def test_non_txt_files_are_ignored(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            self._write_file(tmpdir, "notes.md", "this file has random words xyz")
            violations = validate_dataset.check_directory(tmpdir)
            self.assertEqual(violations, {})

if __name__ == "__main__":
    unittest.main()
