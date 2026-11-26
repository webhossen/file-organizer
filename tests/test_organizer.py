"""Tests for the core organization logic."""

from __future__ import annotations

from pathlib import Path

import pytest

from file_organizer import organize


def make_file(directory: Path, name: str, content: str = "x") -> Path:
    """Create a file (and its parents) and return its path."""
    directory.mkdir(parents=True, exist_ok=True)
    file = directory / name
    file.write_text(content, encoding="utf-8")
    return file


def test_organizes_files_by_extension(tmp_path: Path) -> None:
    make_file(tmp_path, "photo.JPG")
    make_file(tmp_path, "notes.txt")

    result = organize(tmp_path)

    assert result.moved_count == 2
    assert result.error_count == 0
    assert (tmp_path / "jpg" / "photo.JPG").is_file()
    assert (tmp_path / "txt" / "notes.txt").is_file()


def test_files_without_extension_go_to_no_extension(tmp_path: Path) -> None:
    make_file(tmp_path, "README")

    result = organize(tmp_path)

    assert result.moved_count == 1
    assert (tmp_path / "No Extension" / "README").is_file()


def test_collisions_get_a_unique_name(tmp_path: Path) -> None:
    make_file(tmp_path / "txt", "notes.txt", "existing")
    make_file(tmp_path, "notes.txt", "incoming")

    result = organize(tmp_path)

    assert result.moved_count == 1
    assert (tmp_path / "txt" / "notes.txt").read_text(encoding="utf-8") == "existing"
    assert (tmp_path / "txt" / "notes_1.txt").read_text(encoding="utf-8") == "incoming"


def test_dry_run_changes_nothing(tmp_path: Path) -> None:
    file = make_file(tmp_path, "a.txt")

    result = organize(tmp_path, dry_run=True)

    assert result.moved_count == 1
    assert result.moves[0].destination == tmp_path / "txt" / "a.txt"
    assert file.exists()
    assert not (tmp_path / "txt").exists()


def test_category_mode(tmp_path: Path) -> None:
    make_file(tmp_path, "photo.jpg")
    make_file(tmp_path, "report.pdf")
    make_file(tmp_path, "song.mp3")
    make_file(tmp_path, "mystery.xyz")

    result = organize(tmp_path, by="category")

    assert result.moved_count == 4
    assert (tmp_path / "Images" / "photo.jpg").is_file()
    assert (tmp_path / "Documents" / "report.pdf").is_file()
    assert (tmp_path / "Audio" / "song.mp3").is_file()
    assert (tmp_path / "Other" / "mystery.xyz").is_file()


def test_ignore_patterns(tmp_path: Path) -> None:
    make_file(tmp_path, "keep.txt")
    make_file(tmp_path, "skip.tmp")

    result = organize(tmp_path, ignore=["*.tmp"])

    assert result.moved_count == 1
    assert result.ignored == 1
    assert (tmp_path / "skip.tmp").exists()
    assert (tmp_path / "txt" / "keep.txt").is_file()


def test_recursive_is_opt_in(tmp_path: Path) -> None:
    make_file(tmp_path / "nested" / "deep", "a.txt")

    result = organize(tmp_path)

    assert result.moved_count == 0
    assert (tmp_path / "nested" / "deep" / "a.txt").exists()


def test_recursive_moves_files_from_subfolders(tmp_path: Path) -> None:
    make_file(tmp_path / "nested" / "deep", "a.txt")

    result = organize(tmp_path, recursive=True)

    assert result.moved_count == 1
    assert (tmp_path / "txt" / "a.txt").is_file()
    assert not (tmp_path / "nested" / "deep" / "a.txt").exists()


def test_recursive_handles_duplicate_names(tmp_path: Path) -> None:
    make_file(tmp_path / "one", "same.txt", "one")
    make_file(tmp_path / "two", "same.txt", "two")

    result = organize(tmp_path, recursive=True)

    assert result.moved_count == 2
    assert (tmp_path / "txt" / "same.txt").read_text(encoding="utf-8") in {"one", "two"}
    assert (tmp_path / "txt" / "same_1.txt").exists()


def test_already_organized_files_are_skipped(tmp_path: Path) -> None:
    make_file(tmp_path / "jpg", "photo.jpg")

    result = organize(tmp_path, recursive=True)

    assert result.moved_count == 0
    assert result.already_organized == 1
    assert (tmp_path / "jpg" / "photo.jpg").is_file()


def test_skip_hidden(tmp_path: Path) -> None:
    make_file(tmp_path, ".env")
    make_file(tmp_path, "visible.txt")

    result = organize(tmp_path, include_hidden=False)

    assert result.moved_count == 1
    assert result.ignored == 0
    assert (tmp_path / ".env").exists()
    assert (tmp_path / "txt" / "visible.txt").is_file()


def test_skip_hidden_directories(tmp_path: Path) -> None:
    make_file(tmp_path / ".secret", "note.txt")
    make_file(tmp_path, "visible.txt")

    result = organize(tmp_path, recursive=True, include_hidden=False)

    assert result.moved_count == 1
    assert (tmp_path / ".secret" / "note.txt").exists()


def test_invalid_directory_raises(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        organize(tmp_path / "missing")


def test_file_instead_of_directory_raises(tmp_path: Path) -> None:
    file = make_file(tmp_path, "a.txt")

    with pytest.raises(NotADirectoryError):
        organize(file)


def test_invalid_mode_raises(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="Unsupported mode"):
        organize(tmp_path, by="size")
