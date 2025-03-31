FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim AS base
FROM base AS builder

# Set up environment
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/app/venv

WORKDIR /app

# Install the project's dependencies using the lockfile and settings
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    sh -c 'if [ "$DEBUG" = "True" ] || [ "$DEBUG" = "true" ]; then \
      uv sync --frozen --no-install-project --all-groups; \
    else \
      uv sync --frozen --no-install-project --no-dev; \
    fi'

# Then, add the rest of the project source code and install it
# Installing separately from its dependencies allows optimal layer caching
COPY . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --all-groups

FROM base
COPY --from=builder /app /app

WORKDIR /app
ENV PATH="/app/venv/bin:$PATH"

RUN chmod +x scripts/start.sh
EXPOSE 8000

ENTRYPOINT ["scripts/start.sh"]