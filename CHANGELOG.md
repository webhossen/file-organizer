# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- Expanded the README with repository details, badges, release history, roadmap,
  and FAQ.
- Added release notes, issue templates, a pull-request template, Dependabot
  configuration, and a security policy.

## [1.0.0] - 2026-11-26

### Added

- Packaged `file_organizer` library with an `organize()` API and result objects.
- `file-organizer` console script and `python -m file_organizer` entry point.
- Extension mode, category mode, and an `Other` bucket for unknown extensions.
- Collision-safe renaming (`name_1.ext`, `name_2.ext`, …), including collisions
  between planned moves in recursive runs.
- `--recursive`, `--dry-run`, `--ignore`, `--skip-hidden`, and `--quiet` options.
- Interactive folder prompt when no path is supplied.
- PyInstaller build recipe (`FileOrganizer.spec`).
- Pytest suite, Ruff configuration, and GitHub Actions CI.
- MIT license, README, and contributing guide.
