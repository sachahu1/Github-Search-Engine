# syntax = docker/dockerfile
FROM python:3.10-slim-bookworm as python-base-image

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PATH="/root/.local/bin:$PATH" \
    SETUPTOOLS_USE_DISTUTILS=stdlib\
    work_dir=/function

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

ENV VIRTUAL_ENV=$work_dir/.venv \
    PATH="$work_dir/.venv/bin:$PATH"

RUN apt-get update && apt-get upgrade -y

# Install poetry
RUN apt-get install -y --no-install-recommends curl && \
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && python get-pip.py && \
    curl -sSL https://install.python-poetry.org | python3 - && \
    apt-get purge -y curl && \
    rm -rf /var/lib/apt/lists/*

# Set up work directory
WORKDIR $work_dir

FROM python-base-image as build-env

# copy in code
COPY poetry.lock pyproject.toml README.md $work_dir/

RUN poetry install --only main --no-ansi --no-interaction --no-root

COPY github_search_engine $work_dir/github_search_engine

RUN poetry install --only main --no-ansi --no-interaction

FROM build-env as tests

RUN poetry install --without test
COPY tests $work_dir/tests

CMD poetry run coverage run -m pytest ; coverage xml -o test_results/coverage.xml

FROM build-env as build-documentation

ENV SPHINX_APIDOC_OPTIONS=members

RUN apt-get update && apt-get upgrade -y

# Install documentation dependencies
RUN apt-get install --no-install-recommends -y make git
RUN poetry install --no-ansi --no-interaction --with=documentation

# Copy in documentation files
COPY docs $work_dir/docs
COPY examples $work_dir/examples
COPY .git $work_dir/.git

# Run Sphinx generation
RUN poetry run sphinx-build -M html docs/source/ /docs/build

FROM nginx AS documentation

COPY --from=build-documentation /docs/build/html /usr/share/nginx/html

FROM build-env AS lambda

CMD ["poetry", "run", "run_github_search_engine"]

