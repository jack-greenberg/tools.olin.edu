FROM jackgreenberg/poetry:latest as base
MAINTAINER Jack Greenberg <jgreenberg@olin.edu>

ENV PIP_DISABLE_PIP_VERSION_CHECK=on \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_VERSION=1.0.10

RUN apt-get install --no-install-recommends --no-install-suggests -y \
        postgresql-client \
        libpq-dev

WORKDIR /tools
COPY poetry.lock pyproject.toml /tools/
RUN ["poetry", "install", "--no-root"]


# The final built image
FROM dependencies as final

ARG AZURE_APPLICATION_ID
ARG AZURE_TENANT_ID
ARG AZURE_CLIENT_SECRET

WORKDIR /tools

COPY . /tools/
RUN poetry install

CMD ["/tools/scripts/entrypoint.sh"]
