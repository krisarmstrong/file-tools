from pathlib import Path

from file_tools import renamer


def test_rename_from_metadata(tmp_path):
    directory = tmp_path / "games"
    directory.mkdir()
    rom = directory / "sonic.rom"
    rom.write_text("data", encoding="utf-8")

    metadata = tmp_path / "metadata.csv"
    metadata.write_text("source,name,year\nsonic.rom,Sonic,1991\n", encoding="utf-8")

    renamer.rename_from_metadata(directory, metadata, template="{name}-{year}{ext}")

    assert not rom.exists()
    assert (directory / "Sonic-1991.rom").exists()
