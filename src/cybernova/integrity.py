"""Create and verify SHA-256 file-integrity manifests."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import json
from pathlib import Path

from .hashing import hash_file


DEFAULT_IGNORES = {".git", ".pytest_cache", ".venv", "venv", "__pycache__"}


@dataclass(frozen=True)
class IntegrityResult:
    """Differences between a saved manifest and the current directory."""

    added: tuple[str, ...]
    removed: tuple[str, ...]
    modified: tuple[str, ...]

    @property
    def clean(self) -> bool:
        return not (self.added or self.removed or self.modified)


def _scan(root: Path, manifest_path: Path) -> dict[str, str]:
    root = root.resolve()
    files: dict[str, str] = {}
    for path in sorted(root.rglob("*")):
        if path.is_symlink() or not path.is_file():
            continue
        relative = path.relative_to(root)
        if any(part in DEFAULT_IGNORES for part in relative.parts):
            continue
        if path.resolve() == manifest_path.resolve():
            continue
        files[relative.as_posix()] = hash_file(path)
    return files


def create_manifest(root: str | Path, manifest: str | Path) -> int:
    """Create a JSON integrity manifest and return the number of tracked files."""

    root_path = Path(root)
    if not root_path.is_dir():
        raise NotADirectoryError(f"Directory not found: {root_path}")
    manifest_path = Path(manifest)
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    files = _scan(root_path, manifest_path)
    payload = {
        "format": 1,
        "algorithm": "sha256",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "root": str(root_path.resolve()),
        "files": files,
    }
    manifest_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return len(files)


def check_manifest(root: str | Path, manifest: str | Path) -> IntegrityResult:
    """Compare a directory with a previously created manifest."""

    root_path = Path(root)
    manifest_path = Path(manifest)
    if not root_path.is_dir():
        raise NotADirectoryError(f"Directory not found: {root_path}")
    payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    if payload.get("format") != 1 or payload.get("algorithm") != "sha256":
        raise ValueError("Unsupported or invalid manifest format")
    expected = payload.get("files")
    if not isinstance(expected, dict) or not all(
        isinstance(key, str) and isinstance(value, str) for key, value in expected.items()
    ):
        raise ValueError("Manifest has an invalid files section")

    current = _scan(root_path, manifest_path)
    expected_names = set(expected)
    current_names = set(current)
    return IntegrityResult(
        added=tuple(sorted(current_names - expected_names)),
        removed=tuple(sorted(expected_names - current_names)),
        modified=tuple(
            sorted(name for name in current_names & expected_names if current[name] != expected[name])
        ),
    )

