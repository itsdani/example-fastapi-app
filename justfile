install:
    UV_INDEX_ITSDANI_VIRTUAL_PASSWORD="$(gcloud auth application-default print-access-token)" \
    UV_INDEX_ITSDANI_VIRTUAL_USERNAME=oauth2accesstoken \
    uv sync --locked --compile-bytecode

run-dev:
    uv run uvicorn --host 0.0.0.0 --reload --port 5005 main:app --log-config=log_config.local.yaml --no-server-header

run-prod:
    uv run uvicorn --host 0.0.0.0 --port 5005 main:app --log-config=log_config.yaml --no-server-header

docker-build:
    PACKAGEFEED_TOKEN="$(gcloud auth application-default print-access-token)" \
    docker build \
        --secret id=packagefeed-token,env=PACKAGEFEED_TOKEN \
        -t example-fastapi-app:latest .

docker-run:
    docker run --rm -p 5005:5005 --name example-app example-fastapi-app:latest
