# file-tools
[![Checks](https://github.com/krisarmstrong/file-tools/actions/workflows/checks.yml/badge.svg)](https://github.com/krisarmstrong/file-tools/actions/workflows/checks.yml)


![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white) ![Tests](https://img.shields.io/badge/Tests-pytest-passing) ![Status](https://img.shields.io/badge/Status-Active-success)


Successor to `file_organizer`, `file_sorter`, `game_file_renamer`, and `sort-sentinel`. Everything now lives under a single binary with both CLI and GUI support:

```bash
pip install .
file-tools --help
```

## Commands

### `file-tools organize`
Sort downloads into per-type folders via MIME or extension detection, optionally prefixing
filenames with `YYYY-MM` and logging moves to CSV.

```bash
file-tools organize ~/Downloads ~/Documents/Sorted --mode mime --rename-mode date-prefix
```

### `file-tools rename`
Use metadata (CSV/JSON) to rename ROM/game collections – the workflow that previously lived
in `game_file_renamer`.

```bash
file-tools rename ./roms metadata/games.csv --template "{name} - {platform}{ext}"
```

### `file-tools gui`
Launch the PyQt6 GUI for visual file organization and renaming with smart suggestions.

```bash
file-tools gui
```

### `file-tools undo`
Revert file operations using the CSV log file created during organize or rename operations.

```bash
file-tools undo rename_log.csv [--apply]
```

## Development

Run the full local checks:

```bash
./check.sh
```

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e .[test]
python -m pytest
```

CI runs `nox -s tests` (see `.github/workflows/ci.yml`). Versions are stored in `pyproject.toml` and
release-please manages tags and changelog entries.
