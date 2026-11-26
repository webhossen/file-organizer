# File Organizer

A safe, fast command-line tool that tidies a folder by sorting files into
subfolders — by extension or by category.

[![CI](https://github.com/webhossen/file-organizer/actions/workflows/ci.yml/badge.svg)](https://github.com/webhossen/file-organizer/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/webhossen/file-organizer?sort=semver)](https://github.com/webhossen/file-organizer/releases)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/github/license/webhossen/file-organizer)](LICENSE)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)
[![Last commit](https://img.shields.io/github/last-commit/webhossen/file-organizer)](https://github.com/webhossen/file-organizer/commits/main)
[![Issues](https://img.shields.io/github/issues/webhossen/file-organizer)](https://github.com/webhossen/file-organizer/issues)

## Features

- **Two sorting modes** — one folder per extension (`jpg/`, `pdf/`, …) or
  broad categories (`Images/`, `Documents/`, `Audio/`, …).
- **Safe by default** — never overwrites a file; name clashes become
  `report_1.pdf`, `report_2.pdf`, and so on.
- **Dry-run preview** — see every planned move before touching the disk.
- **Recursive mode** — optionally collect files from nested subfolders.
- **Ignore globs** — leave temporary files, sync artifacts, or anything else
  in place with repeatable `--ignore` patterns.
- **Hidden-file control** — skip dotfiles and dot-directories on request.
- **No dependencies** — pure Python standard library.
- **Cross-platform** — Windows, macOS, and Linux, with a PyInstaller recipe for
  a standalone executable.
- **Tested** — pytest suite plus GitHub Actions CI on every supported Python
  version.

## Demo

Before:

```text
Downloads/
├── holiday.jpg
├── invoice.pdf
├── notes.txt
├── song.mp3
└── archive.zip
```

After `file-organizer Downloads`:

```text
Downloads/
├── jpg/holiday.jpg
├── pdf/invoice.pdf
├── txt/notes.txt
├── mp3/song.mp3
└── zip/archive.zip
```

After `file-organizer Downloads --by category`:

```text
Downloads/
├── Images/holiday.jpg
├── Documents/invoice.pdf
├── Documents/notes.txt
├── Audio/song.mp3
└── Archives/archive.zip
```

## Repository details

| Field | Value |
| --- | --- |
| **Repository** | [webhossen/file-organizer](https://github.com/webhossen/file-organizer) |
| **Version** | **1.0.0** |
| **Release** | [v1.0.0](https://github.com/webhossen/file-organizer/releases/tag/v1.0.0) |
| **License** | [MIT](LICENSE) |
| **Python** | 3.10+ |
| **Platforms** | Windows, macOS, Linux |
| **Package** | `file-organizer` (`file_organizer`) |
| **Commands** | `file-organizer`, `python -m file_organizer` |
| **Tests** | 22 pytest tests |
| **CI** | [GitHub Actions](https://github.com/webhossen/file-organizer/actions) |
| **Status** | Active |

## Installation

File Organizer requires **Python 3.10 or newer**.

### From source (recommended with pipx)

```console
git clone https://github.com/webhossen/file-organizer.git
cd file-organizer
pipx install .
```

### With pip

```console
python -m pip install .
```

### Editable install for development

```console
python -m pip install -e ".[dev]"
```

### Standalone executable (Windows, macOS, Linux)

```console
python -m pip install pyinstaller
pyinstaller FileOrganizer.spec
```

The executable is written to `dist/FileOrganizer` (or `dist/FileOrganizer.exe`
on Windows).

## Usage

```console
# Organize by extension
file-organizer ~/Downloads

# Preview a category-based cleanup
file-organizer ~/Downloads --by category --dry-run

# Recursively collect files, but leave temp files alone
file-organizer . --recursive --ignore "*.tmp" --ignore ".DS_Store"

# Same as the original script: prompt for the folder
file-organizer

# Run without installing the console script
python -m file_organizer ~/Desktop
```

### Options

| Option | Description |
| --- | --- |
| `path` | Folder to organize. Prompted interactively when omitted. |
| `-b, --by {extension,category}` | Group by extension (default) or category. |
| `-r, --recursive` | Also process files inside subfolders. |
| `-n, --dry-run` | Print the planned moves without changing anything. |
| `-i, --ignore GLOB` | Skip matching files. May be repeated. Patterns match both the file name and its path relative to the target folder. |
| `--skip-hidden` | Skip dotfiles and files inside dot-directories. |
| `-q, --quiet` | Print only the final summary. |
| `-V, --version` | Show the version and exit. |
| `-h, --help` | Show help and exit. |

Exit codes: `0` success, `1` one or more files could not be moved, `2` invalid
input or folder, `130` cancelled.

## How it works

1. Files in the target folder are collected **before** anything is moved, so
   newly created destination folders are never processed again.
2. Each file is assigned a destination folder:
   - extension mode uses the lowercased extension (`photo.JPG` → `jpg/`);
   - category mode uses the mapping in
     [`categories.py`](src/file_organizer/categories.py);
   - files without an extension go to `No Extension`;
   - unknown extensions go to `Other` in category mode.
3. If the destination already exists, a numeric suffix is added
   (`name_1.ext`, `name_2.ext`, …). Planned moves are also checked against each
   other, which matters in recursive mode.
4. In normal mode the folder is created and the file is moved with
   `shutil.move`, which handles moves across drives. In dry-run mode only the
   plan is built.
5. Directories are never moved, and a file already sitting in its target
   folder is counted as “already organized” and left untouched.

### Safety notes

- Run with `--dry-run` first on valuable folders, and keep a backup.
- Moving files into subfolders is a real filesystem change; the tool does not
  keep an undo log.
- Files locked by another program are reported as errors and skipped.

## Development

```console
git clone https://github.com/webhossen/file-organizer.git
cd file-organizer
python -m venv .venv

# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

python -m pip install -e ".[dev]"
pytest
ruff check .
ruff format --check .
python -m build
```

Run the full test suite with coverage:

```console
pytest --cov=file_organizer --cov-report=term-missing
```

## Project structure

```text
.
├── .github/
│   ├── ISSUE_TEMPLATE/
│   ├── workflows/ci.yml
│   ├── dependabot.yml
│   └── pull_request_template.md
├── docs/releases/v1.0.0.md
├── legacy/myfile.py          # original single-file script, kept for reference
├── src/file_organizer/
│   ├── __init__.py
│   ├── __main__.py           # python -m file_organizer
│   ├── categories.py         # extension → category mapping
│   ├── cli.py                # argparse front end
│   ├── organizer.py          # core logic and result objects
│   └── py.typed
├── tests/
│   ├── test_cli.py
│   └── test_organizer.py
├── CHANGELOG.md
├── CONTRIBUTING.md
├── FileOrganizer.spec        # PyInstaller build recipe
├── LICENSE
├── README.md
├── SECURITY.md
└── pyproject.toml
```

## Tags and releases

The project follows [Semantic Versioning](https://semver.org/) and every release
is tagged as `vMAJOR.MINOR.PATCH`.

| Tag | Date | Highlights |
| --- | --- | --- |
| [`v1.0.0`](https://github.com/webhossen/file-organizer/releases/tag/v1.0.0) | 2026-11-26 | Initial public release: extension and category modes, collision-safe moves, dry-run, recursion, ignore globs, hidden-file control, tests, CI, and PyInstaller build. |

Each release includes:

- `file_organizer-1.0.0-py3-none-any.whl` — installable wheel
- `file_organizer-1.0.0.tar.gz` — source distribution
- `FileOrganizer.exe` — standalone Windows executable

See the [releases page](https://github.com/webhossen/file-organizer/releases) for
downloads and full release notes.

## Roadmap

- [x] Extension and category modes
- [x] Collision-safe moves and dry-run preview
- [x] Recursive mode, ignore globs, and hidden-file controls
- [x] CI on Windows, macOS, and Linux for Python 3.10–3.14
- [ ] User-defined category rules via a config file
- [ ] `--json` machine-readable report
- [ ] Undo log for the most recent run
- [ ] Watch mode for continuously organizing a folder

## FAQ

**Does File Organizer delete files?**
No. It only moves files into subfolders.

**Will it overwrite an existing file?**
No. Name clashes get a numeric suffix such as `report_1.pdf`.

**Can I undo a run?**
There is no built-in undo yet. Use `--dry-run` first and keep backups for
important folders.

**Does it work on external or network drives?**
Yes. `shutil.move` falls back to copy-and-delete when a rename across
filesystems is not possible.

**Are hidden files processed?**
Yes by default. Pass `--skip-hidden` to leave dotfiles and dot-directories
alone.

**What Python versions are supported?**
Python 3.10 and newer. CI runs on Python 3.10–3.14 across Windows, macOS, and
Linux.

## Contributing

Contributions are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for the
development workflow and pull-request checklist.

## License

Released under the [MIT License](LICENSE).
