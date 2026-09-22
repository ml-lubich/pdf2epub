# Overview

PDF2EPUB converts PDFs to Markdown (via marker-pdf) then optionally to EPUB.

## Stack

- Python 3.11–3.14 (3.13 recommended)
- uv + hatchling (`pyproject.toml`)
- marker-pdf, transformers, markdown, latex2mathml, Pillow

## Public surface

- Console script: `pdf2epub`
- Library package: `pdf2epub` (`pdf2md`, `mark2epub`, `cli`)

## Guardrails

- No secrets in repo
- Interactive EPUB prompts only when TTY; use `-y` for automation/Docker
- Upstream: https://github.com/overcuriousity/pdf2epub (MIT)
