"""Local-only password strength analysis.

The password is evaluated in memory and is never logged or transmitted.
"""

from __future__ import annotations

from dataclasses import dataclass
import re


COMMON_FRAGMENTS = {
    "password",
    "qwerty",
    "admin",
    "welcome",
    "letmein",
    "123456",
    "india123",
}


@dataclass(frozen=True)
class PasswordReport:
    """A human-readable password analysis result."""

    score: int
    label: str
    checks: dict[str, bool]
    suggestions: tuple[str, ...]


def analyse_password(password: str) -> PasswordReport:
    """Evaluate a password using transparent, educational rules.

    This is a learning aid, not a replacement for a password manager or a
    breached-password service.
    """

    if not isinstance(password, str):
        raise TypeError("password must be a string")

    checks = {
        "12+ characters": len(password) >= 12,
        "16+ characters": len(password) >= 16,
        "lowercase letter": bool(re.search(r"[a-z]", password)),
        "uppercase letter": bool(re.search(r"[A-Z]", password)),
        "number": bool(re.search(r"\d", password)),
        "symbol": bool(re.search(r"[^A-Za-z0-9]", password)),
    }

    score = sum(
        (
            checks["12+ characters"],
            checks["lowercase letter"],
            checks["uppercase letter"],
            checks["number"],
            checks["symbol"],
        )
    )
    if checks["16+ characters"] and score == 5:
        score = 5

    lowered = password.casefold()
    has_common_fragment = any(fragment in lowered for fragment in COMMON_FRAGMENTS)
    has_long_repeat = bool(re.search(r"(.)\1\1", password))
    if has_common_fragment:
        score -= 1
    if has_long_repeat:
        score -= 1
    score = max(0, min(5, score))

    labels = ("Very weak", "Weak", "Fair", "Good", "Strong", "Excellent")
    suggestions: list[str] = []
    if not checks["12+ characters"]:
        suggestions.append("Use at least 12 characters; a long passphrase is easier to remember.")
    if not checks["uppercase letter"] or not checks["lowercase letter"]:
        suggestions.append("Mix uppercase and lowercase letters.")
    if not checks["number"]:
        suggestions.append("Add a number that is not your birth year or phone number.")
    if not checks["symbol"]:
        suggestions.append("Add a symbol or punctuation mark.")
    if has_common_fragment:
        suggestions.append("Avoid common words and keyboard patterns.")
    if has_long_repeat:
        suggestions.append("Avoid repeating the same character three or more times.")
    if not suggestions:
        suggestions.append("Nice! Keep it unique and store it in a trusted password manager.")

    return PasswordReport(score, labels[score], checks, tuple(suggestions))

