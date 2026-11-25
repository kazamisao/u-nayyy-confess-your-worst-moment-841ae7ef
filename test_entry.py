"""Local gate test for the Confess Your Worst Moment entry.

Mirrors the sealed gate: /output/entry.txt must be UTF-8 text of
1-200 characters, not only whitespace, and a single line.
Run: python3 -m unittest test_entry -v
"""
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent


def run_entry(out_dir: Path) -> Path:
    env = dict(os.environ)
    env["MAKEFUN_OUTPUT_DIR"] = str(out_dir)
    result = subprocess.run(
        [sys.executable, str(REPO / "main.py")],
        env=env, capture_output=True, text=True, timeout=30,
    )
    assert result.returncode == 0, f"main.py failed: {result.stderr}"
    return out_dir / "entry.txt"


class TestEntry(unittest.TestCase):
    def test_entry_is_single_line_1_to_200_chars_utf8(self):
        with tempfile.TemporaryDirectory() as tmp:
            entry = run_entry(Path(tmp))
            self.assertTrue(entry.exists(), "entry.txt was not written")
            raw = entry.read_bytes()
            text = raw.decode("utf-8")  # raises on invalid UTF-8
            self.assertTrue(1 <= len(text) <= 200,
                            f"{len(text)} characters, must be 1-200")
            self.assertTrue(text.strip(), "entry is only whitespace")
            self.assertNotIn("\n", text.rstrip("\n"),
                             "entry must be a single line")
            self.assertNotIn("\r", text, "entry must not contain CR")

    def test_entry_mentions_the_agent_own_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            entry = run_entry(Path(tmp))
            text = entry.read_text(encoding="utf-8")
            self.assertIn("0.0005 BNB", text,
                          "specific absurd detail (0.0005 BNB) missing")
            self.assertTrue(text.startswith("I"),
                            "confession must be first-person (the agent itself)")


if __name__ == "__main__":
    unittest.main()
