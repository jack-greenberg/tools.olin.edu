FROM jackgreenberg/poetry:latest as base

RUN apt-get install -y --no-install-suggests --no-install-recommends postgresql-client libpq-dev

FROM base as build

RUN ["mkdir", "/tools"]
WORKDIR /tools
COPY pyproject.toml /tools/

RUN poetry config virtualenvs.create false

FROM build

ADD . /tools/
WORKDIR /tools
RUN ["poetry", "install"]

CMD ["/tools/scripts/entrypoint.sh"]
