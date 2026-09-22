# markov-text

Order-N Markov chain text generator — feed it a local corpus, tune the
context window, seed the RNG and get reproducible nonsense. Pure
standard library.

```text
$ markov-text -c corpus.txt -o 3 -w 60 -s 42
the cat ate the fish. a dog saw the cat and the dog barked. the fish
swam away. ...
```

## Controls

- **Order** (`-o N`) — the context window length. Order 1 wanders word
  to word; higher orders reproduce the corpus's phrasing more exactly
  (the test suite proves order-3 output only ever emits 4-grams that
  literally exist in the corpus).
- **Corpus cleaning** — noise characters are stripped, whitespace
  collapsed, sentence punctuation kept as standalone tokens so the
  chain can end sentences.
- **Seeding** — `-s N` makes generation fully reproducible; the same
  seed always walks the same path.

## Usage

```
markov-text -c corpus.txt [-o order] [-w words] [-s seed]
```

Exit codes: 0 ok, 1 unreadable/too-small corpus, 2 usage error.

## Development

```console
$ python3 -m unittest discover -s tests   # 14 tests
```

## License

MIT — see [LICENSE](LICENSE).
