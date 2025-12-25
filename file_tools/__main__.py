"""CLI entry point for file-tools."""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from . import organizer, renamer, classifier, undo


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Swiss-army file organizer.")
    parser.add_argument("--verbose", action="store_true", help="Enable debug logging.")
    parser.add_argument("--logfile", type=Path, help="Optional log file.")

    subparsers = parser.add_subparsers(dest="command", required=True)

    organize_parser = subparsers.add_parser("organize", help="Sort files by mime/extension.")
    organize_parser.add_argument("source", type=Path, help="Directory to process.")
    organize_parser.add_argument("target", type=Path, help="Destination root.")
    organize_parser.add_argument("--mode", choices=["mime", "extension"], default="mime")
    organize_parser.add_argument(
        "--rename-mode", choices=["date-prefix", "none"], default="date-prefix"
    )
    organize_parser.add_argument("--dry-run", action="store_true")
    organize_parser.add_argument("--csv-log", type=Path)

    rename_parser = subparsers.add_parser(
        "rename", help="Rename using metadata (games, ROMs, etc.)"
    )
    rename_parser.add_argument("directory", type=Path)
    rename_parser.add_argument("metadata", type=Path)
    rename_parser.add_argument("--template", default="{name} ({year}){ext}")
    rename_parser.add_argument("--preview", action="store_true")

    classify_parser = subparsers.add_parser("classify", help="Classify files to plan folders.")
    classify_parser.add_argument("directory", type=Path)
    classify_parser.add_argument("--model", default="gpt-4o-mini")

    subparsers.add_parser("gui", help="Launch PyQt6 GUI for file organization.")

    undo_parser = subparsers.add_parser("undo", help="Revert file operations from CSV log.")
    undo_parser.add_argument("log_file", type=Path, help="Path to rename_log.csv")
    undo_parser.add_argument(
        "--apply", action="store_true", help="Actually perform undo (default is dry-run)"
    )

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    setup_logging(args.verbose, args.logfile)

    if args.command == "organize":
        opts = organizer.OrganizerOptions(
            source=args.source,
            target=args.target,
            mode=args.mode,
            rename_mode=args.rename_mode,
            dry_run=args.dry_run,
            csv_log=args.csv_log,
        )
        organizer.organize(opts)
    elif args.command == "rename":
        renamer.rename_from_metadata(
            directory=args.directory,
            metadata_path=args.metadata,
            template=args.template,
            preview=args.preview,
        )
    elif args.command == "classify":
        files = [
            {"name": entry.name, "size": entry.stat().st_size}
            for entry in args.directory.iterdir()
            if entry.is_file()
        ]
        result = classifier.classify_files(files, model=args.model)
        for row in result:
            print(f"{row['category']:>12} : {row['name']}")
    elif args.command == "gui":
        try:
            from ..gui import file_tools_gui

            file_tools_gui.run_gui()
        except ImportError:
            print("GUI requires PyQt6. Install with: pip install PyQt6")
            return 1
    elif args.command == "undo":
        undo.revert_changes(log_path=str(args.log_file), dry_run=not args.apply)
    else:
        parser.error("Unknown command")
    return 0


def setup_logging(verbose: bool, logfile: Path | None) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    handlers = [logging.StreamHandler(sys.stdout)]
    if logfile:
        handlers.append(logging.FileHandler(logfile))
    logging.basicConfig(
        level=level, handlers=handlers, format="%(asctime)s [%(levelname)s] %(message)s"
    )


if __name__ == "__main__":
    sys.exit(main())
