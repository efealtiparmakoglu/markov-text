"""Model building and text generation.

The model maps order-length word windows to the list of words that
followed them in the corpus. Generation walks the chain from a seed
window, stopping at a sentence end once the word budget is met.
"""

from __future__ import annotations

import random
import re
from collections import defaultdict

_SENTENCE_END = re.compile(r"[.!?]")
_NOISE = re.compile(r"""[^A-Za-zÇĞİÖŞÜçğıöşü0-9\s.,;:!?'"\-()]""")


def clean_corpus(text: str) -> str:
    """Normalize a corpus: strip noise characters, collapse whitespace."""
    text = _NOISE.sub(" ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def _tokenize(text: str) -> list[str]:
    """Split into word tokens; sentence enders stand alone."""
    tokens = []
    for word in text.split():
        if len(word) > 1 and _SENTENCE_END.fullmatch(word[-1]):
            tokens.append(word[:-1])
            tokens.append(word[-1])
        else:
            tokens.append(word)
    return tokens


def build_model(text: str, order: int = 2) -> dict[tuple[str, ...], list[str]]:
    """Build the transition table: order-length window -> following words."""
    if order < 1:
        raise ValueError("order must be at least 1")
    tokens = _tokenize(clean_corpus(text))
    if len(tokens) <= order:
        raise ValueError(f"corpus too small: {len(tokens)} tokens, order {order}")
    model: dict[tuple[str, ...], list[str]] = defaultdict(list)
    for i in range(len(tokens) - order):
        window = tuple(tokens[i:i + order])
        model[window].append(tokens[i + order])
    return dict(model)


def generate(
    model: dict[tuple[str, ...], list[str]],
    words: int = 60,
    seed: int | None = None,
    rng: random.Random | None = None,
    order: int | None = None,
) -> str:
    """Generate text by walking the chain; deterministic for a fixed seed.

    Stops at a sentence boundary once `words` are emitted, or early if the
    chain reaches a window with no continuation.
    """
    if not model:
        raise ValueError("empty model")
    if order is None:
        order = len(next(iter(model.keys())))
    randomizer = rng if rng is not None else random.Random(seed)
    window = randomizer.choice(list(model.keys()))
    output = list(window)

    while len(output) < words:
        nexts = model.get(tuple(output[-order:]))
        if not nexts:
            break
        choice = randomizer.choice(nexts)
        output.append(choice)
        if len(output) >= words and _SENTENCE_END.fullmatch(choice):
            break
    text = " ".join(output)
    text = re.sub(r"\s+([.,;:!?])", r"\1", text)
    return text
