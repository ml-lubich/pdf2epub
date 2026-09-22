# Deployment

## Local

```bash
uv sync --python 3.13
uv run pdf2epub …
```

Apple Silicon: stock PyTorch wheel includes MPS. For CUDA/ROCm, reinstall torch from pytorch.org after `uv sync`.

## Docker

```bash
docker build -t pdf2epub .
docker run --rm \
  -v "$(pwd)":/data \
  -v pdf2epub-models:/models \
  pdf2epub input.pdf -y --skip-epub
```

Use `-y` (or `--skip-epub`) so the container does not block on metadata prompts.

## GitHub

Repo: `https://github.com/ml-lubich/pdf2epub`  
Upstream remote optional: `overcuriousity/pdf2epub`
