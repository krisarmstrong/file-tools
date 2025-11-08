# file-tools

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white) ![Tests](https://img.shields.io/badge/Tests-pytest-passing) ![Status](https://img.shields.io/badge/Status-Active-success)


Successor to `file_organizer`, `file_sorter`, `game_file_renamer`, and the CLI portion of
`local_llm_file_organizer`. Everything now lives under a single binary:

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

### `file-tools llm`
Send file manifests to an LLM (OpenAI Responses API by default) to brainstorm folder plans.
Install the optional extras (`pip install .[llm]`) and run:

```bash
file-tools llm ./research --model gpt-4o-mini
```

## Development
```bash
python -m venv .venv && source .venv/bin/activate
pip install -e .[test]
python -m pytest
```

CI runs `nox -s tests` (see `.github/workflows/ci.yml`). Versions are derived from git tags via
`setuptools_scm` – tag releases as `vX.Y.Z`.
