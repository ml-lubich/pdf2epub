"""CLI and EPUB smoke tests (no marker models)."""

from __future__ import annotations

import zipfile
from pathlib import Path
from unittest.mock import patch

from pdf2epub.cli import build_parser, main
from pdf2epub.mark2epub import EpubMetadata, convert_to_epub


def test_parser_yes_flags() -> None:
    args = build_parser().parse_args(["book.pdf", "-y", "--title", "T", "--author", "A"])
    assert args.yes is True
    assert args.title == "T"
    assert args.author == "A"


def test_cli_yes_passes_noninteractive(tmp_path: Path) -> None:
    pdf = tmp_path / "doc.pdf"
    pdf.write_bytes(b"%PDF")
    out = tmp_path / "out"
    out.mkdir()

    with (
        patch("pdf2epub.cli.pdf2md.convert_pdf") as convert_pdf,
        patch("pdf2epub.cli.mark2epub.convert_to_epub") as convert_epub,
        patch("pdf2epub.cli.torch") as torch_mock,
    ):
        torch_mock.cuda.is_available.return_value = False
        torch_mock.backends.mps.is_available.return_value = False
        main([str(pdf), str(out), "-y", "--title", "Hello"])

    convert_pdf.assert_called_once()
    kwargs = convert_epub.call_args.kwargs
    assert kwargs["interactive"] is False
    assert kwargs["review_markdown_files"] is False
    assert kwargs["metadata_overrides"] == EpubMetadata(
        title="Hello", author=None, language=None, publisher=None
    )


def test_convert_to_epub_writes_to_output_path(tmp_path: Path) -> None:
    md_dir = tmp_path / "chapter"
    md_dir.mkdir()
    (md_dir / "chapter.md").write_text("# Hi\n\nHello world.\n", encoding="utf-8")
    epub_file = tmp_path / "exported" / "book.epub"

    convert_to_epub(
        md_dir,
        epub_file,
        interactive=False,
        review_markdown_files=False,
        metadata_overrides=EpubMetadata(title="Hi", author="Test"),
    )

    assert epub_file.is_file()
    with zipfile.ZipFile(epub_file) as zf:
        names = zf.namelist()
        assert "mimetype" in names
        assert "META-INF/container.xml" in names
        assert "OPS/package.opf" in names
        assert zf.read("mimetype") == b"application/epub+zip"
