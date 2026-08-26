"""Interactive quiz content for cybersecurity fundamentals."""

from __future__ import annotations

from dataclasses import dataclass
import random
from typing import Callable


@dataclass(frozen=True)
class Question:
    prompt: str
    choices: tuple[str, ...]
    answer: int
    explanation: str


QUESTIONS = (
    Question(
        "Which property means data has not been changed without permission?",
        ("Availability", "Integrity", "Confidentiality", "Authentication"),
        1,
        "Integrity protects data from unauthorised modification.",
    ),
    Question(
        "What is the safest response to an unexpected login link in an email?",
        ("Open it quickly", "Forward it", "Use the official site directly", "Reply with your password"),
        2,
        "Navigate to the known official site yourself instead of trusting the link.",
    ),
    Question(
        "What does multi-factor authentication add?",
        ("A second independent proof", "A longer username", "Public Wi-Fi", "A shared password"),
        0,
        "MFA combines independent factors, such as a password and an authenticator app.",
    ),
    Question(
        "Which is a cryptographic hash function?",
        ("SHA-256", "HTTP", "HTML", "DNS"),
        0,
        "SHA-256 maps input to a fixed-size digest and is designed to be one-way.",
    ),
    Question(
        "What is the principle of least privilege?",
        ("Give everyone admin", "Grant only needed access", "Never update software", "Reuse credentials"),
        1,
        "Users and programs should receive only the access required for their tasks.",
    ),
    Question(
        "Why are software updates important for security?",
        ("They always change passwords", "They can patch vulnerabilities", "They remove backups", "They stop encryption"),
        1,
        "Updates often fix security weaknesses discovered after release.",
    ),
    Question(
        "What is phishing?",
        ("Encrypting a disk", "A deceptive attempt to steal information", "Testing a backup", "Hashing a file"),
        1,
        "Phishing uses deceptive messages or sites to trick people into revealing data or taking unsafe actions.",
    ),
    Question(
        "Which backup approach is strongest?",
        ("One copy only", "3-2-1 backups", "No offline copy", "Only on the same laptop"),
        1,
        "The 3-2-1 rule uses three copies, two media types, and one off-site copy.",
    ),
)


def run_quiz(
    count: int = 5,
    *,
    input_fn: Callable[[str], str] = input,
    output_fn: Callable[[str], None] = print,
) -> tuple[int, int]:
    """Run an interactive quiz and return ``(correct, total)``."""

    count = max(1, min(count, len(QUESTIONS)))
    selected = random.sample(list(QUESTIONS), count)
    score = 0
    for number, question in enumerate(selected, start=1):
        output_fn(f"\nQuestion {number}/{count}: {question.prompt}")
        for index, choice in enumerate(question.choices, start=1):
            output_fn(f"  {index}. {choice}")
        while True:
            raw = input_fn("Your answer: ").strip()
            if raw.isdigit() and 1 <= int(raw) <= len(question.choices):
                break
            output_fn(f"Please enter a number from 1 to {len(question.choices)}.")
        if int(raw) - 1 == question.answer:
            score += 1
            output_fn("Correct!")
        else:
            output_fn(f"Not quite. The answer is {question.answer + 1}.")
        output_fn(question.explanation)
    return score, count

