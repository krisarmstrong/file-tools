"""Bulk rename helpers (game libraries, metadata driven)."""

from __future__ import annotations

import csv
import json
import logging
from pathlib import Path
from typing import Iterable, List, Mapping, Optional


def load_metadata(path: Path) -> list[dict]:
    if path.suffix == ".json":
        return json.loads(path.read_text(encoding="utf-8"))
    rows: list[dict] = []
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        rows.extend(reader)
    return rows


def rename_from_metadata(
    directory: Path,
    metadata_path: Path,
    *,
    template: str = "{name} ({year}){ext}",
    preview: bool = False,
) -> list[tuple[Path, Path]]:
    """Rename files using metadata (inspired by game_file_renamer)."""

    metadata = load_metadata(metadata_path)
    mappings = {row.get("source") or row.get("filename"): row for row in metadata}

    operations: list[tuple[Path, Path]] = []
    for file_path in directory.iterdir():
        if not file_path.is_file():
            continue
        record = mappings.get(file_path.name)
        if not record:
            continue
        new_name = template.format(
            name=record.get("name") or record.get("title") or file_path.stem,
            year=record.get("year", ""),
            platform=record.get("platform", ""),
            ext=file_path.suffix,
        )
        new_path = file_path.with_name(new_name)
        operations.append((file_path, new_path))
        logging.info("%s -> %s", file_path.name, new_name)
        if not preview:
            new_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.rename(new_path)
    return operations
