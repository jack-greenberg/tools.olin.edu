FROM ubuntu:18.04 as tools-base

MAINTAINER Jack Greenberg <j@jackgreenberg.co>

ENV PIP_DISABLE_PIP_VERSION_CHECK=on

RUN apt-get update && \
    apt-get install --no-install-recommends --no-install-suggests -y \
        build-essential \
        software-properties-common \
        python3.7-dev \
        python3-dev \
        python3-pip \
        postgresql-client \
        libpq-dev \
        git \
        wget \
        curl \
        vim && \
        pip3 install --upgrade setuptools wheel

RUN pip3 install poetry

ENV PATH="${HOME}/.poetry/bin:$PATH"

RUN ["mkdir", "/tools"]
WORKDIR /tools
COPY pyproject.toml /tools/

RUN poetry config virtualenvs.create false
RUN poetry install --no-root --no-dev

FROM tools-base
ADD . /tools/
WORKDIR /tools
RUN ["poetry", "install", "--no-dev"]

CMD ["/tools/scripts/entrypoint.sh"]
