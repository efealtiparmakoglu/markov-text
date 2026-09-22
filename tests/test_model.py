import random
import unittest

from markov_text.model import build_model, clean_corpus, generate

CORPUS = (
    "the cat sat on the mat. the cat ate the fish. "
    "a dog saw the cat and the dog barked. the fish swam away."
)


class TestClean(unittest.TestCase):
    def test_strips_noise_and_collapses_whitespace(self):
        dirty = "Hello\u00a0  world!  <html> #noise \n\tnew  lines\n"
        cleaned = clean_corpus(dirty)
        self.assertEqual(cleaned, "Hello world! html noise new lines")

    def test_keeps_sentence_punctuation(self):
        self.assertEqual(clean_corpus("Stop! Wait... go?"), "Stop! Wait... go?")


class TestModel(unittest.TestCase):
    def test_build_counts_transitions(self):
        model = build_model("the cat sat. the cat ran.", order=1)
        self.assertEqual(sorted(model[("the",)]), ["cat", "cat"])

    def test_order_two_windows_are_pairs(self):
        model = build_model("a b c a b d", order=2)
        self.assertEqual(sorted(model[("a", "b")]), ["c", "d"])

    def test_order_must_be_positive(self):
        with self.assertRaises(ValueError):
            build_model("some words here", order=0)

    def test_tiny_corpus_rejected(self):
        with self.assertRaises(ValueError):
            build_model("one two", order=2)


class TestGenerate(unittest.TestCase):
    def setUp(self):
        self.model = build_model(CORPUS, order=2)

    def test_deterministic_with_seed(self):
        self.assertEqual(
            generate(self.model, words=30, seed=7),
            generate(self.model, words=30, seed=7),
        )

    def test_words_come_from_corpus(self):
        corpus_words = {w.strip(".,!?") for w in CORPUS.split()}
        text = generate(self.model, words=40, seed=3)
        for word in text.split():
            self.assertIn(word.strip(".,!?"), corpus_words)

    def test_explicit_rng_beats_seed(self):
        a = generate(self.model, words=20, rng=random.Random(11))
        b = generate(self.model, words=20, rng=random.Random(11))
        self.assertEqual(a, b)

    def test_empty_model_rejected(self):
        with self.assertRaises(ValueError):
            generate({}, words=10)


class TestOrderEffect(unittest.TestCase):
    def test_higher_order_produces_only_corpus_ngrams(self):
        corpus = "the quick brown fox jumps over the lazy dog. " * 10
        corpus_tokens = corpus.split()
        corpus_4grams = {tuple(corpus_tokens[i:i + 4]) for i in range(len(corpus_tokens) - 3)}
        text = generate(build_model(corpus, order=3), words=30, seed=1)
        tokens = text.split()
        for i in range(len(tokens) - 3):
            self.assertIn(tuple(tokens[i:i + 4]), corpus_4grams,
                          f"order-3 chain invented a novel 4-gram: {tokens[i:i + 4]}")

    def test_low_order_uses_all_transitions(self):
        model = build_model(CORPUS, order=1)
        self.assertGreater(len(model), 5)


if __name__ == "__main__":
    unittest.main()
