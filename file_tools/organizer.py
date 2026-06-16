"""File organization utilities consolidating prior tools."""

from __future__ import annotations

import csv
import logging
import mimetypes
import re
import shutil
from collections.abc import Iterator
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

try:  # pragma: no cover
    import magic  # type: ignore
except ImportError:  # pragma: no cover
    magic = None  # type: ignore

try:  # pragma: no cover
    from PIL import Image
except ImportError:  # pragma: no cover
    Image = None  # type: ignore

DEFAULT_FOLDERS = {
    "application/pdf": "PDF",
    "application/msword": "Word",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "Word",
    "application/vnd.ms-excel": "Excel",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": "Excel",
    "application/vnd.ms-powerpoint": "Presentations",
    "application/vnd.openxmlformats-officedocument.presentationml.presentation": "Presentations",
    "application/zip": "Compressed",
    "application/x-7z-compressed": "Compressed",
    "application/x-rar-compressed": "Compressed",
    "application/vnd.tcpdump.pcap": "PCAP",
    "application/x-pcapng": "PCAP",
}

EXTENSION_FOLDERS = {
    ".pcap": "PCAP",
    ".pcapng": "PCAP",
    ".txt": "Text",
    ".conf": "Config",
}

GARBAGE_EXTS = {".ics"}
GARBAGE_PATTERNS = [
    re.compile(r"^outlook-.*(?<!\\.pdf)$"),
    re.compile(r"^image\\d+\\.(png|jpg|gif|jfif)$"),
]


@dataclass
class OrganizerOptions:
    source: Path
    target: Path
    mode: str = "mime"
    rename_mode: str = "date-prefix"
    dry_run: bool = False
    csv_log: Path | None = None


class FileOrganizer:
    def __init__(self, options: OrganizerOptions) -> None:
        self.options = options
        self.target = options.target
        self.target.mkdir(parents=True, exist_ok=True)
        self.log_rows: list[list[str]] = []

    def run(self) -> None:
        for path in self._iter_files(self.options.source):
            self._process(path)
        if self.options.csv_log and self.log_rows:
            self._write_csv()

    def _iter_files(self, root: Path) -> Iterator[Path]:
        for entry in root.rglob("*"):
            if entry.is_file():
                yield entry

    def _process(self, file_path: Path) -> None:
        if self._is_garbage(file_path.name):
            self._delete(file_path, reason="garbage pattern")
            return

        destination = self._resolve_destination(file_path)
        if not destination:
            return
        dest_dir, rename = destination
        dest_dir.mkdir(parents=True, exist_ok=True)

        final_name = rename or file_path.name
        final_path = dest_dir / final_name
        if final_path.exists():
            final_path = self._dedupe(final_path)
        self._move(file_path, final_path)

    def _resolve_destination(self, file_path: Path) -> tuple[Path, str | None] | None:
        if self.options.mode == "extension":
            ext = file_path.suffix.lower() or "No_Extension"
            folder = EXTENSION_FOLDERS.get(ext, ext.strip("."))
            return self.target / folder, self._rename(file_path)

        if magic is not None:
            try:
                mime = magic.from_file(str(file_path), mime=True)
            except Exception:
                mime = None
        else:
            mime = None
        if not mime:
            mime = mimetypes.guess_type(file_path.name)[0]

        if not mime:
            folder = EXTENSION_FOLDERS.get(file_path.suffix.lower(), "Others")
        elif mime.startswith("image/"):
            if not self._is_useful_image(file_path):
                self._delete(file_path, reason="low-res image")
                return None
            folder = "Images"
        elif mime.startswith("video/"):
            folder = "Videos"
        elif mime.startswith("audio/"):
            folder = "Music"
        else:
            folder = DEFAULT_FOLDERS.get(mime, "Others")
        return self.target / folder, self._rename(file_path)

    def _rename(self, file_path: Path) -> str | None:
        if self.options.rename_mode == "none":
            return None
        prefix = datetime.fromtimestamp(file_path.stat().st_mtime).strftime("%Y-%m")
        new_name = f"{prefix}-{file_path.name}"
        return new_name

    def _move(self, src: Path, dest: Path) -> None:
        logging.info("%s -> %s", src, dest)
        if self.options.dry_run:
            return
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(src), str(dest))
        self.log_rows.append([str(src), str(dest)])

    def _dedupe(self, dest: Path) -> Path:
        stem = dest.stem
        for counter in range(2, 9999):
            candidate = dest.with_name(f"{stem}-{counter}{dest.suffix}")
            if not candidate.exists():
                return candidate
        raise RuntimeError("Could not generate unique filename")

    def _write_csv(self) -> None:
        with self.options.csv_log.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.writer(handle)
            writer.writerow(["source", "destination"])
            writer.writerows(self.log_rows)

    def _is_useful_image(self, file_path: Path) -> bool:
        if Image is None:
            return False
        try:
            with Image.open(file_path) as img:
                width, height = img.size
                return width >= 100 and height >= 100
        except Exception:
            return False

    def _is_garbage(self, name: str) -> bool:
        lowered = name.lower()
        if any(lowered.endswith(ext) for ext in GARBAGE_EXTS):
            return True
        return any(pattern.match(lowered) for pattern in GARBAGE_PATTERNS)

    def _delete(self, file_path: Path, reason: str) -> None:
        logging.info("Deleting %s (%s)", file_path, reason)
        if not self.options.dry_run:
            file_path.unlink(missing_ok=True)


def organize(options: OrganizerOptions) -> None:
    organizer = FileOrganizer(options)
    organizer.run()
