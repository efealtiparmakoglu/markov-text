"""End-to-end CLI test over a real corpus file."""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

CORPUS = (
    "the cat sat on the mat. the cat ate the fish. "
    "a dog saw the cat and the dog barked. the fish swam away. " * 5
)


class TestCli(unittest.TestCase):
    def test_generate_with_seed_is_reproducible(self):
        corpus_file = Path(tempfile.mkdtemp()) / "corpus.txt"
        corpus_file.write_text(CORPUS, encoding="utf-8")
        runs = []
        for _ in range(2):
            out = subprocess.run(
                [sys.executable, "-m", "markov_text.cli", "-c", str(corpus_file), "-o", "2", "-w", "25", "-s", "5"],
                capture_output=True, text=True, check=True, cwd=ROOT,
            )
            runs.append(out.stdout.strip())
        self.assertEqual(runs[0], runs[1])
        # 25 tokens were requested; attaching sentence punctuation to the
        # preceding word lowers the whitespace-split count a little
        self.assertGreaterEqual(len(runs[0].split()), 18)

    def test_rejects_bad_order(self):
        corpus_file = Path(tempfile.mkdtemp()) / "corpus.txt"
        corpus_file.write_text(CORPUS, encoding="utf-8")
        out = subprocess.run(
            [sys.executable, "-m", "markov_text.cli", "-c", str(corpus_file), "-o", "0"],
            capture_output=True, text=True, cwd=ROOT,
        )
        self.assertEqual(out.returncode, 2)


if __name__ == "__main__":
    unittest.main()
