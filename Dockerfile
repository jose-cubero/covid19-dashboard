FROM python:3.8 as base

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1

WORKDIR /app

FROM base as builder

ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.1.4

# RUN apk add --no-cache gcc libffi-dev musl-dev postgresql-dev
# RUN pip install "poetry==$POETRY_VERSION"
# alternative
RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python -
ENV PATH="${PATH}:/root/.poetry/bin"

RUN python -m venv /venv

COPY pyproject.toml poetry.lock ./
# RUN poetry export --without-hashes -f requirements.txt | /venv/bin/pip install -r /dev/stdin
RUN poetry export -f requirements.txt | /venv/bin/pip install -r /dev/stdin

COPY . .
RUN poetry build && /venv/bin/pip install dist/*.whl

FROM base as final

# RUN apk add --no-cache libffi libpq
COPY --from=builder /venv /venv
COPY server.py ./

# Define environment variables for the dash server app
ENV dash_port=8050
ENV dash_debug="True"
CMD ["/venv/bin/python", "server.py"]