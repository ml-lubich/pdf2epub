"""Tests for pdf2epub helpers (no marker-pdf model download)."""

from __future__ import annotations

from pathlib import Path

import pytest

from pdf2epub.mark2epub import EpubMetadata, build_epub_description, get_coverpage_XML
from pdf2epub.pdf2md import add_pdfs_to_queue, get_default_output_dir


def test_get_default_output_dir(tmp_path: Path) -> None:
    pdf = tmp_path / "Book.pdf"
    assert get_default_output_dir(pdf) == tmp_path / "Book"


def test_add_pdfs_to_queue_file(tmp_path: Path) -> None:
    pdf = tmp_path / "a.pdf"
    pdf.write_bytes(b"%PDF")
    queue = add_pdfs_to_queue(pdf)
    assert queue == [pdf]


def test_add_pdfs_to_queue_dir(tmp_path: Path) -> None:
    (tmp_path / "one.pdf").write_bytes(b"%PDF")
    (tmp_path / "two.pdf").write_bytes(b"%PDF")
    (tmp_path / "skip.txt").write_text("nope")
    queue = add_pdfs_to_queue(tmp_path)
    assert {p.name for p in queue} == {"one.pdf", "two.pdf"}


def test_add_pdfs_to_queue_empty_dir(tmp_path: Path) -> None:
    with pytest.raises(SystemExit):
        add_pdfs_to_queue(tmp_path)


def test_build_epub_description_noninteractive_overrides() -> None:
    desc = build_epub_description(
        interactive=False,
        overrides=EpubMetadata(title="T", author="A", language="de", publisher="P"),
    )
    assert desc["metadata"]["dc:title"] == "T"
    assert desc["metadata"]["dc:creator"] == "A"
    assert desc["metadata"]["dc:language"] == "de"
    assert desc["metadata"]["dc:publisher"] == "P"
    assert desc["default_css"] == ["style.css"]


def test_coverpage_escapes_xml() -> None:
    html = get_coverpage_XML("A & B <C>", "Alice")
    assert "A &amp; B &lt;C&gt;" in html
    assert "Alice" in html