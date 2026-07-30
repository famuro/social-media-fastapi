# ==============================================================================
# Stage 1: Builder
#
# Installs Python dependencies into a virtual environment.
# Keeping dependency installation separate from application code allows Docker
# to reuse this layer when only source files change.
# ==============================================================================

FROM python:3.14-slim AS builder

# Install the official statically compiled 'uv' binaries from the minimal
# scratch distribution image to keep the build lightweight.
COPY --from=ghcr.io/astral-sh/uv:0.5.24 /uv /uvx /bin/

# Set Python and uv micro-optimizations for deterministic container builds
# - UV_COMPILE_BYTECODE: Pre-compiles .py files to .pyc for faster cold starts
# - UV_LINK_MODE: Forces copying files into the venv instead of creating hardlinks
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

WORKDIR /build

# Copy dependency files first for Docker layer caching.
# This prevents rebuilding packages when editing application source code.
COPY pyproject.toml uv.lock ./

# Install dependencies into a standard production virtual environment (.venv).
# - --frozen: Ignores lockfile changes and forces strict adherence to uv.lock
# - --no-install-project: Skips copying the app code in this layer
# - --no-dev: Excludes development, testing, and formatting dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync \
    --frozen \
    --no-install-project \
    --no-dev


# ==============================================================================
# STAGE 2: Runtime Layer (Ultra-lightweight execution container)

# Contains only what is required to run the application
# ==============================================================================

# Match the exact base OS image version from Stage 1 to ensure binary consistency
FROM python:3.14-slim AS runtime

LABEL org.opencontainers.image.title="Social Media API" \
      org.opencontainers.image.description="Production-style social media backend built with FastAPI." \
      org.opencontainers.image.version="0.1.0" \
      org.opencontainers.image.licenses="MIT"

WORKDIR /app

# Set core production Python runtime flags
# - PYTHONDONTWRITEBYTECODE: Disables writing runtime bytecode to the host disk
# - PYTHONUNBUFFERED: Forces stdout/stderr logs to flush instantly to Docker streams
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Place the virtual environment's bin folder first on the system PATH.
ENV PATH="/app/.venv/bin:$PATH"

# Create a dedicated non-root system user and group.
# This prevents container privilege escalation attacks.
RUN groupadd --system appgroup \
    && useradd --system --gid appgroup appuser

# Copy the pre-compiled virtual environment directly from the builder stage
COPY --from=builder --chown=appuser:appgroup /build/.venv /app/.venv

# Copy the application source code into the execution workspace
COPY --chown=appuser:appgroup app ./app

# Drop root privileges and run the application as the non-privileged system user
USER appuser

# Document that the container intends to listen on port 8000
EXPOSE 8000

# Docker can use this to determine whether the container is healthy.
# This uses the existing health endpoint that we already created.
HEALTHCHECK --interval=30s \
    --timeout=5s \
    --start-period=5s \
    --retries=3 \
    CMD python -c \
    "import sys; \
    from urllib.request import urlopen; \
    response = urlopen('http://127.0.0.1:8000/api/v1/health'); \
    sys.exit(0 if response.status == 200 else 1)"

# Execute uvicorn via python -m to bypass hardcoded virtual environment paths.
# This ensures perfect compatibility across the container build pipeline.
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]