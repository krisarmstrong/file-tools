# File Tools Documentation

Unified CLI for file organization and bulk renaming.

## Quick Links

- [Installation](installation.md)
- [Usage Guide](usage.md)
- [Commands Reference](commands.md)
- [Contributing](../CONTRIBUTING.md)

## Overview

File Tools is a comprehensive command-line utility for managing files with operations including:

- **Organize** - Sort files by type (MIME or extension)
- **Rename** - Bulk renaming with metadata support
- **Classify** - Intelligent file classification
- **GUI** - Visual interface for file operations
- **Undo** - Revert operations safely

## Features

- Smart file organization by MIME type or extension
- Date-based filename prefixing
- CSV logging of all operations
- Undo functionality for safety
- Visual GUI mode with PyQt6
- Metadata-driven bulk renaming
- Support for ROM/game collections

## Installation

```bash
pip install .
```

## Quick Start

```bash
# Organize files
file-tools organize ~/Downloads ~/Sorted --mode mime

# Rename with metadata
file-tools rename ./files metadata.csv --template "{name}{ext}"

# Launch GUI
file-tools gui

# Undo operations
file-tools undo log.csv --apply
```

## License

MIT License - See [LICENSE](../LICENSE) for details.

## Author

Kris Armstrong
