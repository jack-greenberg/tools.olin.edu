FROM jackgreenberg/poetry:latest as base

RUN apt-get install -y --no-install-suggests --no-install-recommends postgresql-client libpq-dev

FROM base as build

RUN ["mkdir", "/tools"]
WORKDIR /tools
COPY pyproject.toml /tools/

RUN poetry config virtualenvs.create false
RUN poetry install --no-root --no-dev

FROM build

ADD . /tools/
WORKDIR /tools
RUN ["poetry", "install", "--no-dev"]

CMD ["/tools/scripts/entrypoint.sh"]
