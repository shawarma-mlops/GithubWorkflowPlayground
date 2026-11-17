"""
Parse Ruff and Mypy output and print them in a format that GitHub Actions can parse and display as annotations.

Ruff warnings are warnings, while Mypy warnings are merge-blocking errors.
"""
import argparse
import re
import sys


def parse_ruff(output: str) -> None:
    """
    Parse Ruff output and print it in a format that GitHub Actions can parse and display as annotations.
    """
    for line in output.splitlines():
        match = re.match(r"(.+):(\d+):(\d+): (.+)", line)
        if match:
            file_path, line_number, column_number, message = match.groups()
            print(f"::warning file={file_path},line={line_number},col={column_number}::{message}")


def parse_mypy(output: str) -> None:
    """
    Parse Mypy output and print it in a format that GitHub Actions can parse and display as annotations.
    """
    for line in output.splitlines():
        match = re.match(r"(.+):(\d+): (.+)", line)
        if match:
            file_path, line_number, message = match.groups()
            print(f"::error file={file_path},line={line_number}::{message}")


def main() -> None:
    argument_parser = argparse.ArgumentParser(
        description="Parse Ruff and Mypy output and print them in a format that GitHub Actions can parse and display as annotations."
    )
    argument_parser.add_argument(
        "--ruff-output",
        help="Set this flag if the input is Ruff output.",
        action="store_true",
        default=False
    )
    argument_parser.add_argument(
        "--mypy-output",
        help="Set this flag if the input is Mypy output.",
        action="store_true",
        default=False
    )

    args = argument_parser.parse_args()

    if not (args.ruff_output or args.mypy_output):
        print("Error: You must specify either --ruff-output or --mypy-output.")
        sys.exit(1)

    if args.ruff_output and args.mypy_output:
        print("Error: You cannot specify both --ruff-output and --mypy-output.")
        sys.exit(1)

    stdin = sys.stdin.read()
    if args.ruff_output:
        parse_ruff(stdin)
    elif args.mypy_output:
        parse_mypy(stdin)


if __name__ == "__main__":
    main()
