FROM ghcr.io/astral-sh/uv:debian-slim

WORKDIR /app

# Install python
RUN \
    --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=.python-version,target=.python-version \
    uv python install $(cat .python-version)

# Install dependencies
RUN \
    --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=secret,id=packagefeed-token,env=UV_INDEX_ITSDANI_VIRTUAL_PASSWORD \
    UV_INDEX_ITSDANI_VIRTUAL_USERNAME=oauth2accesstoken \
    uv sync --locked --compile-bytecode --no-install-project

# Copy the project code into the image
ADD . /app

# Install the project
RUN \
    --mount=type=cache,target=/root/.cache/uv \
    --mount=type=secret,id=packagefeed-token,env=UV_INDEX_ITSDANI_VIRTUAL_PASSWORD \
    UV_INDEX_ITSDANI_VIRTUAL_USERNAME=oauth2accesstoken \
    uv sync --locked --compile-bytecode

CMD ["uv", "run", "uvicorn", "--host", "0.0.0.0", "--port", "5005", "main:app", "--log-config=log_config.yaml", "--no-server-header"]
