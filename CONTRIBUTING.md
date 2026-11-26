# Contributing to File Organizer

Thanks for taking the time to contribute!

## Reporting bugs

Please include:

- your operating system and Python version (`python --version`);
- the command you ran (redact personal paths);
- the output, including any error messages;
- a short description of the folder layout involved.

Use `--dry-run` when sharing examples from real folders.

## Development setup

```console
git clone https://github.com/webhossen/file-organizer.git
cd file-organizer
python -m venv .venv
```

Activate the environment:

```console
# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

Install the project with development tools:

```console
python -m pip install -e ".[dev]"
```

## Before opening a pull request

```console
ruff check .
ruff format .
pytest
```

All checks must pass. Please also:

- add or update tests for behaviour changes;
- update `README.md` and `CHANGELOG.md` when user-facing behaviour changes;
- keep the code compatible with Python 3.9+;
- keep the core logic in `src/file_organizer/organizer.py` free of CLI concerns.

## Commit messages

Short, imperative summaries are preferred, for example:

```text
Add --ignore support for recursive runs
Fix collision handling on case-insensitive filesystems
```

## Pull requests

- Keep each pull request focused on one change.
- Describe the problem and the chosen solution.
- Mention any trade-offs or follow-up work.
- CI must be green before merging.

## Code style

The project uses [Ruff](https://docs.astral.sh/ruff/) for linting and
formatting with a 100-character line length. Type hints are encouraged.
