FROM python:3.12.12-slim-trixie AS builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

COPY --from=ghcr.io/astral-sh/uv:0.6.16 /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

COPY ./app .

# ---------------------------------------------------
FROM python:3.12.12-slim-trixie AS runner

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# COPY ./ca-certificates /usr/local/share/ca-certificates/
# RUN update-ca-certificates

COPY --from=builder /app /app

COPY ./docker-entrypoint.sh /

RUN useradd -m appuser && chown -R appuser /app
USER appuser

ENV PATH="/app/.venv/bin:$PATH"

WORKDIR /app

ENTRYPOINT ["/docker-entrypoint.sh"]

CMD ["python", "/app/main.py"]

# CMD ["uvicorn", \
#     "--factory", "application.api.main:create_app", \
#     "--timeout-graceful-shutdown", "3", \
#     "--host", "0.0.0.0", \
#     "--port", "8000" \
# ]
