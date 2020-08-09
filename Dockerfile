FROM jackgreenberg/poetry:latest as build

WORKDIR /tools

RUN apt-get install -y \
    --no-install-suggests \
    --no-install-recommends \
    postgresql-client \
    libpq-dev

COPY pyproject.toml poetry.lock /tools/
RUN ["poetry", "config", "virtualenvs.create", "false"]
RUN ["poetry", "install", "--no-root"]

COPY . /tools/
RUN ["poetry", "install"]

CMD ["/tools/scripts/entrypoint.sh"]
