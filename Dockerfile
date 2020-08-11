FROM python:3.7-slim as dependencies
MAINTAINER Jack Greenberg <jgreenberg@olin.edu>

ENV PIP_DISABLE_PIP_VERSION_CHECK=on

WORKDIR /tools

RUN apt-get update && \
    apt-get install --no-install-recommends --no-install-suggests -y \
        build-essential \
        software-properties-common \
        python3.7-venv \
        python3.7-dev \
        python3-dev \
        python3-pip \
        curl \
        postgresql-client \
        libpq-dev \
        && ln -sf $(which python3.7) $(which python3) \
        && pip3 install --upgrade setuptools wheel \
        && { curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python3 ; } \
        && apt-get remove -y curl wget vim && apt-get autoremove -y

ENV PATH "/root/.poetry/bin:${PATH}"

COPY poetry.lock pyproject.toml /tools/
RUN ["poetry", "install", "--no-root"]

FROM dependencies as final

ARG AZURE_APPLICATION_ID
ARG AZURE_TENANT_ID
ARG AZURE_CLIENT_SECRET

COPY . /tools/
RUN ["poetry", "install"]

CMD ["/tools/scripts/entrypoint.sh"]
