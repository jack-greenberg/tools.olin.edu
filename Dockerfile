FROM jackgreenberg/poetry:latest as build
MAINTAINER Jack Greenberg <jgreenberg@olin.edu>

WORKDIR /tools

RUN apt-get install -y \
    --no-install-suggests \
    --no-install-recommends \
    postgresql-client \
    libpq-dev

ARG AZURE_APPLICATION_ID
ARG AZURE_TENANT_ID
ARG AZURE_CLIENT_SECRET

COPY pyproject.toml poetry.lock /tools/
RUN ["poetry", "config", "virtualenvs.create", "false"]
RUN ["poetry", "install", "--no-root"]

COPY . /tools/
RUN ["poetry", "install"]

CMD ["/tools/scripts/entrypoint.sh"]
