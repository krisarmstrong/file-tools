from file_tools import organizer


def test_organize_moves_files(tmp_path):
    src = tmp_path / "src"
    dst = tmp_path / "dst"
    src.mkdir()
    dst.mkdir()
    file = src / "example.txt"
    file.write_text("hello", encoding="utf-8")

    opts = organizer.OrganizerOptions(
        source=src,
        target=dst,
        mode="extension",
        rename_mode="none",
        dry_run=False,
        csv_log=None,
    )

    organizer.organize(opts)

    assert not file.exists()
    assert (dst / "Text" / "example.txt").exists()
