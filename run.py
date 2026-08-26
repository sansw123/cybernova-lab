"""Run CyberNova directly from a source checkout without installing it."""

from pathlib import Path
import sys


sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from cybernova.cli import main  # noqa: E402  (path is prepared above)


if __name__ == "__main__":
    raise SystemExit(main())

