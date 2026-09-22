# API

## CLI

```
pdf2epub [input_path] [output_path]
  --max-pages INT
  --start-page INT
  --skip-epub
  --skip-md
  -y / --yes
  --no-review
  --title STR
  --author STR
  --language STR
  --publisher STR
```

## Python

- `pdf2epub.pdf2md.convert_pdf(path, output_dir, max_pages=None, start_page=None)`
- `pdf2epub.mark2epub.convert_to_epub(markdown_dir, output_path, *, interactive=True, review_markdown_files=True, metadata_overrides=None)` — `output_path` is a directory or a `.epub` file path
- `pdf2epub.mark2epub.EpubMetadata` — optional Dublin Core overrides
- `pdf2epub.cli.main(argv=None)`
