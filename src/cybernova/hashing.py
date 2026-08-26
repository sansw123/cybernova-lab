"""Small helpers for learning about cryptographic hashes."""

from __future__ import annotations

import hashlib
from pathlib import Path


CHUNK_SIZE = 64 * 1024


def hash_text(text: str, algorithm: str = "sha256") -> str:
    """Return the hexadecimal digest of UTF-8 text."""

    digest = hashlib.new(algorithm)
    digest.update(text.encode("utf-8"))
    return digest.hexdigest()


def hash_file(path: str | Path, algorithm: str = "sha256") -> str:
    """Hash a file in chunks so large files do not fill memory."""

    digest = hashlib.new(algorithm)
    with Path(path).open("rb") as handle:
        while chunk := handle.read(CHUNK_SIZE):
            digest.update(chunk)
    return digest.hexdigest()

