"""CLI entry point for pdf2epub."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import torch

from pdf2epub import mark2epub, pdf2md
from pdf2epub.mark2epub import EpubMetadata


def _device_message() -> str:
    if torch.cuda.is_available():
        return "CUDA is available. Using GPU for processing."
    if torch.backends.mps.is_available():
        return "MPS is available. Using Apple Silicon for processing."
    return "CUDA is not available. Using CPU for processing."


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pdf2epub",
        description="Convert PDF files to EPUB format via Markdown",
    )
    parser.add_argument(
        "input_path",
        nargs="?",
        type=str,
        help="Path to input PDF file or directory (default: ./input/*.pdf)",
    )
    parser.add_argument(
        "output_path",
        nargs="?",
        type=str,
        help="Path to output directory (default: directory named after PDF)",
    )
    parser.add_argument(
        "--max-pages",
        type=int,
        default=None,
        help="Maximum number of pages to process",
    )
    parser.add_argument(
        "--start-page",
        type=int,
        default=None,
        help="Page number to start from",
    )
    parser.add_argument(
        "--skip-epub",
        action="store_true",
        help="Skip EPUB generation, only create markdown",
    )
    parser.add_argument(
        "--skip-md",
        action="store_true",
        help="Skip markdown generation, use existing markdown files",
    )
    parser.add_argument(
        "--yes",
        "-y",
        action="store_true",
        help="Non-interactive: accept default EPUB metadata (no prompts)",
    )
    parser.add_argument(
        "--no-review",
        action="store_true",
        help="Skip interactive markdown review prompts",
    )
    parser.add_argument("--title", type=str, default=None, help="EPUB title")
    parser.add_argument("--author", type=str, default=None, help="EPUB author(s)")
    parser.add_argument(
        "--language",
        type=str,
        default=None,
        help="EPUB language code (e.g. en, de)",
    )
    parser.add_argument(
        "--publisher",
        type=str,
        default=None,
        help="EPUB publisher",
    )
    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    print(_device_message())

    input_path = Path(args.input_path) if args.input_path else pdf2md.get_default_input_dir()
    queue = pdf2md.add_pdfs_to_queue(input_path)
    print(f"Found {len(queue)} PDF files to process")

    metadata_overrides = EpubMetadata(
        title=args.title,
        author=args.author,
        language=args.language,
        publisher=args.publisher,
    )
    interactive = not args.yes
    review = not (args.yes or args.no_review)

    failed: list[str] = []
    for pdf_path in queue:
        print(f"\nProcessing: {pdf_path.name}")

        if args.output_path:
            output_path = Path(args.output_path)
            markdown_dir = output_path / pdf_path.stem
        else:
            markdown_dir = pdf2md.get_default_output_dir(pdf_path)
            output_path = markdown_dir.parent

        try:
            if args.skip_md:
                if not markdown_dir.exists():
                    print(f"Error: Markdown directory not found: {markdown_dir}", file=sys.stderr)
                    failed.append(pdf_path.name)
                    continue
                print(f"Using existing markdown files from: {markdown_dir}")

            if not args.skip_md:
                print("Converting PDF to Markdown...")
                pdf2md.convert_pdf(
                    str(pdf_path),
                    markdown_dir,
                    args.max_pages,
                    args.start_page,
                )

            if not args.skip_epub:
                print("Converting Markdown to EPUB...")
                mark2epub.convert_to_epub(
                    markdown_dir,
                    output_path,
                    interactive=interactive,
                    review_markdown_files=review,
                    metadata_overrides=metadata_overrides,
                )

        except Exception as e:
            print(f"Error processing {pdf_path.name}: {str(e)}", file=sys.stderr)
            failed.append(pdf_path.name)
            continue

    if failed:
        print(
            f"\nFailed to process {len(failed)} of {len(queue)} PDF file(s):",
            file=sys.stderr,
        )
        for name in failed:
            print(f"  - {name}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
