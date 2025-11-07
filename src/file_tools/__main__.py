"""CLI entry point for file-tools."""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from . import organizer, renamer, llm


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Swiss-army file organizer.")
    parser.add_argument("--verbose", action="store_true", help="Enable debug logging.")
    parser.add_argument("--logfile", type=Path, help="Optional log file.")

    subparsers = parser.add_subparsers(dest="command", required=True)

    organize_parser = subparsers.add_parser("organize", help="Sort files by mime/extension.")
    organize_parser.add_argument("source", type=Path, help="Directory to process.")
    organize_parser.add_argument("target", type=Path, help="Destination root.")
    organize_parser.add_argument("--mode", choices=["mime", "extension"], default="mime")
    organize_parser.add_argument("--rename-mode", choices=["date-prefix", "none"], default="date-prefix")
    organize_parser.add_argument("--dry-run", action="store_true")
    organize_parser.add_argument("--csv-log", type=Path)

    rename_parser = subparsers.add_parser("rename", help="Rename using metadata (games, ROMs, etc.)")
    rename_parser.add_argument("directory", type=Path)
    rename_parser.add_argument("metadata", type=Path)
    rename_parser.add_argument("--template", default="{name} ({year}){ext}")
    rename_parser.add_argument("--preview", action="store_true")

    llm_parser = subparsers.add_parser("llm", help="Classify files with an LLM to plan folders.")
    llm_parser.add_argument("directory", type=Path)
    llm_parser.add_argument("--model", default="gpt-4o-mini")

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
    elif args.command == "llm":
        files = [
            {"name": entry.name, "size": entry.stat().st_size}
            for entry in args.directory.iterdir()
            if entry.is_file()
        ]
        result = llm.classify_with_llm(files, model=args.model)
        for row in result:
            print(f"{row['category']:>12} : {row['name']}")
    else:
        parser.error("Unknown command")
    return 0


def setup_logging(verbose: bool, logfile: Path | None) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    handlers = [logging.StreamHandler(sys.stdout)]
    if logfile:
        handlers.append(logging.FileHandler(logfile))
    logging.basicConfig(level=level, handlers=handlers, format="%(asctime)s [%(levelname)s] %(message)s")


if __name__ == "__main__":
    sys.exit(main())
