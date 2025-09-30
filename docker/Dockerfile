FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

RUN groupadd --system --gid 999 ddd && useradd --system --gid 999 --uid 999 --create-home ddd

ENV UV_TOOL_BIN_DIR=/usr/local/bin

WORKDIR /usr/src/app
COPY pyproject.toml uv.lock .
RUN uv sync --locked --no-install-project

ENV PATH="/usr/src/app/.venv/bin:$PATH"
ENTRYPOINT []
USER ddd

CMD echo "Hello, world!"
