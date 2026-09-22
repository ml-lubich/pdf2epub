# Design

## CLI UX

- Default: interactive EPUB metadata + optional markdown review
- Automation: `-y` / `--yes` accepts defaults; `--title` / `--author` / `--language` / `--publisher` override
- `--no-review` skips markdown review without forcing metadata defaults
- `--skip-epub` / `--skip-md` for partial pipelines

## Output tree

```
<stem>/
  <stem>.md
  <stem>.epub
  <stem>_metadata.json
  description.json
  images/
```

## EPUB cover

Simple centered title/author XHTML; XML-escaped user strings.
