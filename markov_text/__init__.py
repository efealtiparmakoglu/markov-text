"""Markov chain text generator: order-N model from a local corpus."""

from .model import build_model, generate, clean_corpus

__version__ = "1.0.0"

__all__ = ["build_model", "generate", "clean_corpus"]
