"""Command-line interface for CyberNova Lab."""

from __future__ import annotations

import argparse
from getpass import getpass
from pathlib import Path
import sys

from . import __version__
from .hashing import hash_file, hash_text
from .integrity import check_manifest, create_manifest
from .passwords import analyse_password
from .progress import add_topic, load_progress
from .quiz import run_quiz


CYAN = "\033[96m"
PURPLE = "\033[95m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"

BANNER = r"""
   ____      __              _   __                 
  / ___/_ __/ /  ___ ____   / | / /__ _  _____ _   
 / /__/ // / _ \/ -_) __/  /  |/ / _ \ |/ / _ `/   
 \___/\_, /_.__/\__/_/    /_/|_/\___/___/\_,_/    
     /___/       beginner cyber lab
"""


def _colour(text: str, code: str) -> str:
    return f"{code}{text}{RESET}" if sys.stdout.isatty() else text


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="cybernova",
        description="A beginner-friendly cybersecurity learning toolkit.",
    )
    parser.add_argument("--version", action="version", version=f"CyberNova Lab {__version__}")
    subparsers = parser.add_subparsers(dest="command")

    password = subparsers.add_parser("password", help="check password strength locally")
    password.add_argument("value", nargs="?", help="omit this to type without displaying it")

    digest = subparsers.add_parser("hash", help="calculate a SHA-256 digest")
    source = digest.add_mutually_exclusive_group(required=True)
    source.add_argument("--text", help="text to hash")
    source.add_argument("--file", type=Path, help="file to hash")

    integrity = subparsers.add_parser("integrity", help="create or check a file manifest")
    integrity_sub = integrity.add_subparsers(dest="integrity_command", required=True)
    for action in ("create", "check"):
        action_parser = integrity_sub.add_parser(action, help=f"{action} an integrity manifest")
        action_parser.add_argument("directory", type=Path, help="directory to monitor")
        action_parser.add_argument(
            "--manifest",
            type=Path,
            default=Path("cybernova-manifest.json"),
            help="manifest path (default: cybernova-manifest.json)",
        )

    quiz = subparsers.add_parser("quiz", help="test your security fundamentals")
    quiz.add_argument("--count", type=int, default=5, help="number of questions (default: 5)")

    learn = subparsers.add_parser("learn", help="maintain a local learning log")
    learn_sub = learn.add_subparsers(dest="learn_command", required=True)
    learn_add = learn_sub.add_parser("add", help="record a topic you studied")
    learn_add.add_argument("topic", help="topic name, for example 'Linux permissions'")
    learn_sub.add_parser("list", help="show recorded topics")
    return parser


def _show_password(value: str | None) -> int:
    candidate = value if value is not None else getpass("Password (hidden): ")
    report = analyse_password(candidate)
    colours = (RED, RED, YELLOW, YELLOW, GREEN, GREEN)
    print(f"\nStrength: {_colour(report.label, colours[report.score])} ({report.score}/5)")
    for name, passed in report.checks.items():
        marker = _colour("PASS", GREEN) if passed else _colour("MISS", YELLOW)
        print(f"  [{marker}] {name}")
    print("\nSuggestions:")
    for suggestion in report.suggestions:
        print(f"  - {suggestion}")
    print("\nPrivacy note: this check ran only on your device.")
    return 0


def _show_integrity(args: argparse.Namespace) -> int:
    if args.integrity_command == "create":
        count = create_manifest(args.directory, args.manifest)
        print(_colour(f"Manifest created: {args.manifest} ({count} files)", GREEN))
        return 0

    result = check_manifest(args.directory, args.manifest)
    if result.clean:
        print(_colour("Integrity check passed: no changes detected.", GREEN))
        return 0
    for label, entries in (
        ("Added", result.added),
        ("Removed", result.removed),
        ("Modified", result.modified),
    ):
        for entry in entries:
            print(f"{label:8} {entry}")
    return 1


def _show_learning_log() -> int:
    topics = load_progress()["topics"]
    if not topics:
        print("No topics yet. Try: cybernova learn add \"CIA triad\"")
        return 0
    print(_colour(f"Learning log — {len(topics)} topic(s)", PURPLE))
    for item in topics:
        print(f"  {item['date']}  {item['topic']}")
    return 0


def _interactive_menu(parser: argparse.ArgumentParser) -> int:
    print(_colour(BANNER, CYAN))
    print("Choose a mission:")
    print("  1. Password strength check")
    print("  2. Cybersecurity quiz")
    print("  3. View learning log")
    print("  4. Show all commands")
    choice = input("\nMission number: ").strip()
    if choice == "1":
        return _show_password(None)
    if choice == "2":
        score, total = run_quiz()
        print(_colour(f"\nFinal score: {score}/{total}", GREEN if score >= total * 0.7 else YELLOW))
        return 0
    if choice == "3":
        return _show_learning_log()
    parser.print_help()
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command is None:
            return _interactive_menu(parser)
        if args.command == "password":
            return _show_password(args.value)
        if args.command == "hash":
            value = hash_text(args.text) if args.text is not None else hash_file(args.file)
            print(value)
            return 0
        if args.command == "integrity":
            return _show_integrity(args)
        if args.command == "quiz":
            score, total = run_quiz(args.count)
            print(_colour(f"\nFinal score: {score}/{total}", GREEN if score >= total * 0.7 else YELLOW))
            return 0
        if args.command == "learn" and args.learn_command == "add":
            item = add_topic(args.topic)
            print(_colour(f"Logged: {item['topic']} ({item['date']})", GREEN))
            return 0
        if args.command == "learn":
            return _show_learning_log()
    except (FileNotFoundError, NotADirectoryError, PermissionError, ValueError) as error:
        print(_colour(f"Error: {error}", RED), file=sys.stderr)
        return 2
    return 0

