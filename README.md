# PDF2EPUB

Convert PDF → Markdown → EPUB with layout-aware extraction (marker-pdf).

Fork of [overcuriousity/pdf2epub](https://github.com/overcuriousity/pdf2epub),
packaged for **uv** / `pyproject.toml` under `ml-lubich`.

## Install

Requires Python 3.11–3.14 (**3.13 recommended**).

```bash
# clone + sync
git clone https://github.com/ml-lubich/pdf2epub.git
cd pdf2epub
uv sync --python 3.13

# or install the CLI as a tool
uv tool install .
```

## Usage

```bash
uv run pdf2epub book.pdf
uv run pdf2epub book.pdf --skip-epub
uv run pdf2epub book.pdf -y --title "My Book" --author "Ada"
uv run pdf2epub input_dir/ out_dir/ --max-pages 20
```

`-y` / `--yes` skips interactive EPUB metadata and markdown review prompts.

## Development

```bash
uv sync --python 3.13
uv run pytest
uv run ruff check --select E9,F src tests
```

## License

MIT — see [LICENSE](LICENSE). Upstream copyright retained; this fork adds packaging and CLI improvements.
