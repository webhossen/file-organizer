"""Core logic for organizing files into folders."""

from __future__ import annotations

import fnmatch
import os
import shutil
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field
from pathlib import Path

from .categories import NO_EXTENSION, category_for

VALID_MODES = ("extension", "category")


@dataclass(frozen=True)
class Move:
    """A single planned or completed file move."""

    source: Path
    destination: Path
    folder: str


@dataclass(frozen=True)
class MoveError:
    """A file that could not be moved."""

    source: Path
    message: str


@dataclass
class OrganizeResult:
    """Outcome of an :func:`organize` run."""

    root: Path
    moves: list[Move] = field(default_factory=list)
    errors: list[MoveError] = field(default_factory=list)
    ignored: int = 0
    already_organized: int = 0

    @property
    def moved_count(self) -> int:
        """Number of files that were moved (or would be moved in a dry run)."""
        return len(self.moves)

    @property
    def error_count(self) -> int:
        """Number of files that could not be moved."""
        return len(self.errors)


def organize(
    directory: str | Path,
    *,
    by: str = "extension",
    recursive: bool = False,
    dry_run: bool = False,
    ignore: Iterable[str] | None = None,
    include_hidden: bool = True,
) -> OrganizeResult:
    """Organize the files directly inside *directory*.

    Parameters
    ----------
    directory:
        Folder whose files should be organized.
    by:
        ``"extension"`` creates one folder per extension. ``"category"``
        groups extensions into folders such as ``Images`` and ``Documents``.
    recursive:
        Also process files inside subfolders.
    dry_run:
        Compute every move without creating folders or moving files.
    ignore:
        Glob patterns matched against the file name and its path relative to
        *directory*. Matching files are left alone.
    include_hidden:
        Process dotfiles and files inside dot-directories when true.

    Returns
    -------
    OrganizeResult
        The moves, per-file errors, and counts for the run.

    Raises
    ------
    ValueError
        If *by* is not a supported mode.
    FileNotFoundError
        If *directory* does not exist.
    NotADirectoryError
        If *directory* is not a folder.
    """
    if by not in VALID_MODES:
        raise ValueError(f"Unsupported mode {by!r}; choose from {', '.join(VALID_MODES)}.")

    root = Path(directory).expanduser().resolve()
    if not root.exists():
        raise FileNotFoundError(f"Folder does not exist: {root}")
    if not root.is_dir():
        raise NotADirectoryError(f"Not a folder: {root}")

    patterns = tuple(ignore or ())
    result = OrganizeResult(root=root)
    reserved: set[str] = set()

    for source in _collect_files(root, recursive=recursive, include_hidden=include_hidden):
        relative = source.relative_to(root)
        if _matches_any(relative, patterns):
            result.ignored += 1
            continue

        folder_name = _folder_for(source, by)
        folder_path = root / folder_name

        # A file that already sits in its target folder is left untouched.
        if _same_path(source, folder_path / source.name):
            result.already_organized += 1
            continue

        destination = _unique_destination(folder_path, source.name, reserved)
        reserved.add(_path_key(destination))

        if not dry_run:
            try:
                folder_path.mkdir(parents=True, exist_ok=True)
                shutil.move(str(source), str(destination))
            except OSError as error:
                result.errors.append(MoveError(source, str(error)))
                continue

        result.moves.append(Move(source, destination, folder_name))

    return result


def _collect_files(root: Path, *, recursive: bool, include_hidden: bool) -> list[Path]:
    """Return the files to consider, sorted for deterministic output."""
    entries = root.rglob("*") if recursive else root.iterdir()
    files = []
    for entry in entries:
        if not entry.is_file():
            continue
        if not include_hidden and _is_hidden(entry, root):
            continue
        files.append(entry)
    return sorted(files, key=lambda path: str(path).lower())


def _folder_for(source: Path, mode: str) -> str:
    """Return the destination folder name for a file."""
    extension = source.suffix[1:].lower()
    if not extension:
        return NO_EXTENSION
    if mode == "category":
        return category_for(extension)
    return extension


def _unique_destination(folder: Path, name: str, reserved: set[str]) -> Path:
    """Return a collision-free path inside *folder* for *name*."""
    candidate = folder / name
    if not candidate.exists() and _path_key(candidate) not in reserved:
        return candidate

    stem, suffix = os.path.splitext(name)
    counter = 1
    while True:
        candidate = folder / f"{stem}_{counter}{suffix}"
        if not candidate.exists() and _path_key(candidate) not in reserved:
            return candidate
        counter += 1


def _matches_any(relative: Path, patterns: Sequence[str]) -> bool:
    """Return true when *relative* matches any glob pattern."""
    name = relative.name
    posix = relative.as_posix()
    if os.name == "nt":
        name = name.lower()
        posix = posix.lower()

    for pattern in patterns:
        normalized = pattern.replace("\\", "/")
        if os.name == "nt":
            normalized = normalized.lower()
        if fnmatch.fnmatchcase(name, normalized) or fnmatch.fnmatchcase(posix, normalized):
            return True
    return False


def _is_hidden(path: Path, root: Path) -> bool:
    """Return true when the path or one of its parents is a dot-entry."""
    return any(part.startswith(".") for part in path.relative_to(root).parts)


def _path_key(path: Path) -> str:
    """Return a case-normalized absolute key for path comparisons."""
    return os.path.normcase(os.path.abspath(str(path)))


def _same_path(first: Path, second: Path) -> bool:
    """Compare two paths using platform-aware case rules."""
    return _path_key(first) == _path_key(second)
