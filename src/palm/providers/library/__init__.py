"""Library provider — publish Living Library corpora into Palm storage (0.54.4)."""

from palm.providers.library import registry as registry
from palm.providers.library.provider import LibraryProvider

__all__ = ["LibraryProvider", "registry"]
