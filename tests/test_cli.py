"""Tests for the command-line interface."""

from __future__ import annotations

from pathlib import Path

import pytest

from file_organizer import __version__
from file_organizer.cli import main


def make_file(directory: Path, name: str, content: str = "x") -> Path:
    """Create a file (and its parents) and return its path."""
    directory.mkdir(parents=True, exist_ok=True)
    file = directory / name
    file.write_text(content, encoding="utf-8")
    return file


def test_cli_moves_files(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    make_file(tmp_path, "a.txt")

    exit_code = main([str(tmp_path)])

    assert exit_code == 0
    assert (tmp_path / "txt" / "a.txt").is_file()
    output = capsys.readouterr().out
    assert "Moved: a.txt -> txt/" in output
    assert "Moved 1 file(s)." in output


def test_cli_dry_run(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    make_file(tmp_path, "a.txt")

    exit_code = main([str(tmp_path), "--dry-run"])

    assert exit_code == 0
    assert (tmp_path / "a.txt").exists()
    output = capsys.readouterr().out
    assert "Would move 1 file(s)." in output


def test_cli_prompts_when_path_is_missing(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    make_file(tmp_path, "a.txt")
    monkeypatch.setattr("builtins.input", lambda _prompt: f'"{tmp_path}"')

    exit_code = main([])

    assert exit_code == 0
    assert (tmp_path / "txt" / "a.txt").is_file()
    assert "Moved 1 file(s)." in capsys.readouterr().out


def test_cli_returns_error_for_invalid_path(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    exit_code = main([str(tmp_path / "missing")])

    assert exit_code == 2
    assert "error:" in capsys.readouterr().err


def test_cli_quiet_only_prints_summary(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    make_file(tmp_path, "a.txt")

    assert main([str(tmp_path), "--quiet"]) == 0

    assert capsys.readouterr().out.strip() == "Moved 1 file(s)."


def test_cli_skip_hidden(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    make_file(tmp_path, ".env")
    make_file(tmp_path, "a.txt")

    assert main([str(tmp_path), "--skip-hidden"]) == 0

    assert (tmp_path / ".env").exists()
    assert (tmp_path / "txt" / "a.txt").is_file()
    assert "Moved 1 file(s)." in capsys.readouterr().out


def test_cli_version(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as exc_info:
        main(["--version"])

    assert exc_info.value.code == 0
    assert __version__ in capsys.readouterr().out
