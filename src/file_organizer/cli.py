"""Command-line interface for File Organizer."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from . import __version__
from .organizer import OrganizeResult, organize


def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser used by the CLI."""
    parser = argparse.ArgumentParser(
        prog="file-organizer",
        description="Organize files in a folder into subfolders by extension or category.",
        epilog='Example: file-organizer "~/Downloads" --by category --dry-run',
    )
    parser.add_argument(
        "path",
        nargs="?",
        help="Folder to organize. You will be prompted when it is omitted.",
    )
    parser.add_argument(
        "-b",
        "--by",
        choices=("extension", "category"),
        default="extension",
        help="Group files by extension (default) or by category.",
    )
    parser.add_argument(
        "-r",
        "--recursive",
        action="store_true",
        help="Also process files inside subfolders.",
    )
    parser.add_argument(
        "-n",
        "--dry-run",
        action="store_true",
        help="Preview the moves without changing anything.",
    )
    parser.add_argument(
        "-i",
        "--ignore",
        action="append",
        default=[],
        metavar="GLOB",
        help="Skip files matching this glob. May be given more than once.",
    )
    parser.add_argument(
        "--skip-hidden",
        action="store_true",
        help="Skip dotfiles and files inside dot-directories.",
    )
    parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="Only print the final summary.",
    )
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the CLI and return a process exit code."""
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        raw_path = args.path if args.path is not None else input("Enter folder path: ")
    except (EOFError, KeyboardInterrupt):
        print("\nerror: no folder path provided", file=sys.stderr)
        return 2

    raw_path = raw_path.strip().strip("\"'")
    if not raw_path:
        print("error: no folder path provided", file=sys.stderr)
        return 2

    try:
        result = organize(
            Path(raw_path).expanduser(),
            by=args.by,
            recursive=args.recursive,
            dry_run=args.dry_run,
            ignore=args.ignore,
            include_hidden=not args.skip_hidden,
        )
    except OSError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        print("\nCancelled.", file=sys.stderr)
        return 130

    _print_result(result, dry_run=args.dry_run, quiet=args.quiet)
    return 1 if result.error_count else 0


def _print_result(result: OrganizeResult, *, dry_run: bool, quiet: bool) -> None:
    """Print per-file details and a final summary."""
    verb = "Would move" if dry_run else "Moved"

    if not quiet:
        for move in result.moves:
            source = move.source.relative_to(result.root).as_posix()
            print(f"{verb}: {source} -> {move.folder}/")
        for error in result.errors:
            source = error.source.relative_to(result.root).as_posix()
            print(f"error: could not move {source}: {error.message}", file=sys.stderr)

    print(f"{verb} {result.moved_count} file(s).")
    if result.ignored:
        print(f"Ignored {result.ignored} file(s).")
    if result.already_organized:
        print(f"Already organized: {result.already_organized} file(s).")
    if result.error_count:
        print(f"Failed to move {result.error_count} file(s).", file=sys.stderr)
