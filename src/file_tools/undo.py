"""
Undo renaming and deletion using rename_log.csv
"""

import csv
from pathlib import Path


def revert_changes(log_path="rename_log.csv", dry_run=True):
    log_file = Path(log_path)
    if not log_file.exists():
        print("Log file not found.")
        return

    with open(log_file, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            original = row["Original"]
            action = row["Action"]
            new_name = row["NewName"]
            if action == "RENAME" and new_name != "[DELETE]":
                if Path(new_name).exists():
                    print(f"Reverting: {new_name} -> {original}")
                    if not dry_run:
                        Path(new_name).rename(original)
            elif action == "DELETE":
                print(f"Cannot auto-undo DELETE: {original} (manual restore needed)")
