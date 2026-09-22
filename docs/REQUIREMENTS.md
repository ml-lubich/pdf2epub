# Requirements

1. Convert one PDF or a directory of PDFs to markdown and/or EPUB
2. Installable via `uv sync` / `uv tool install` / pip from `pyproject.toml`
3. Console entrypoint `pdf2epub`
4. Non-interactive mode for CI/Docker (`-y`)
5. Page range via `--start-page` + `--max-pages` (marker-pdf list range)
6. Preserve MIT license and upstream attribution
7. Fail the process with non-zero exit if any PDF in a batch fails
