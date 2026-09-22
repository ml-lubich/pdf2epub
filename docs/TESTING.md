# Testing

## Commands

```bash
uv sync --python 3.13
uv run pytest
uv run ruff check --select E9,F src tests
uv run python -m compileall -q src
```

## Strategy

- Unit tests cover path queueing, non-interactive metadata, and cover XML escaping
- Do not call marker model downloads in CI (heavy); `compileall` + ruff catch import/syntax issues
- Smoke: `uv run pdf2epub --help`

## CI

GitHub Actions: Python 3.13, `uv sync`, pytest, ruff, compileall.
