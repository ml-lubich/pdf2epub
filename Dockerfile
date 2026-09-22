# CPU-only image. For GPU acceleration install a CUDA/ROCm PyTorch build
# instead (see README) or run natively.
FROM python:3.13-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

COPY pyproject.toml README.md LICENSE ./
COPY src/ src/

RUN uv sync --no-dev

ENV PATH="/app/.venv/bin:$PATH"
ENV HF_HOME=/models
VOLUME /models

WORKDIR /data

ENTRYPOINT ["pdf2epub"]
