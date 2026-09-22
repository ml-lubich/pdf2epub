# Architecture

## Layout

```
src/pdf2epub/
  cli.py          # argparse entrypoint
  pdf2md.py       # PDF → markdown + images (marker-pdf)
  mark2epub.py    # markdown → EPUB zip/OPF
  postprocessing/ # optional LLM postprocessing helpers
```

## Data flow

1. Resolve input PDF(s) → queue
2. `PdfConverter` (marker) → `.md`, `_metadata.json`, `images/`
3. Optional interactive or CLI metadata → `description.json`
4. Build EPUB: mimetype, META-INF, OPS (xhtml, css, images, toc)

## Device selection

CLI prints CUDA / MPS / CPU based on `torch` availability. Marker uses the same backends.
