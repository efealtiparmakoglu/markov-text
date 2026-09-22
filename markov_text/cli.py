"""CLI: generate text from a corpus file."""

from __future__ import annotations

import argparse
import sys

from . import __version__
from .model import build_model, generate

USAGE = f"""markov-text v{{__version__}} — order-N Markov chain text generator

USAGE
  markov-text -c <corpus.txt> [options]

OPTIONS
  -c, --corpus <file>   input text file (required)
  -o, --order <N>       chain order / context window (default: 2)
  -w, --words <N>       words to generate (default: 80)
  -s, --seed <N>        random seed (default: random)
  -h, --help            show this help
  -V, --version         print version

Fully offline: the corpus is a local file, generation is seeded and
reproducible."""


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("-c", "--corpus", required=True)
    parser.add_argument("-o", "--order", type=int, default=2)
    parser.add_argument("-w", "--words", type=int, default=80)
    parser.add_argument("-s", "--seed", type=int, default=None)
    parser.add_argument("-h", "--help", action="store_true")
    parser.add_argument("-V", "--version", action="store_true")
    args = parser.parse_args(argv)

    if args.help:
        print(USAGE.format(__version__=__version__))
        return
    if args.version:
        print("markov-text", __version__)
        return
    if args.order < 1 or args.words < 1:
        parser.exit(2, "markov-text: --order and --words expect positive integers\n")

    try:
        text = open(args.corpus, encoding="utf-8", errors="replace").read()
    except OSError as error:
        parser.exit(1, f"markov-text: {error}\n")

    try:
        model = build_model(text, order=args.order)
    except ValueError as error:
        parser.exit(1, f"markov-text: {error}\n")
    print(generate(model, words=args.words, seed=args.seed, order=args.order))


if __name__ == "__main__":
    main(sys.argv[1:])
