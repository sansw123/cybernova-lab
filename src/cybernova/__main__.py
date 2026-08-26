"""Allow ``python -m cybernova`` to launch the toolkit."""

from .cli import main


if __name__ == "__main__":
    raise SystemExit(main())

