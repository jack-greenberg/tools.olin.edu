FROM ubuntu:18.04 as base
MAINTAINER Jack Greenberg <jgreenberg@olin.edu>

ENV PIP_DISABLE_PIP_VERSION_CHECK=on \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_VERSION=1.0.10

FROM base as dependencies

RUN apt-get update && \
    apt-get install --no-install-recommends --no-install-suggests -y \
        build-essential \
        software-properties-common \
        python3.7-venv \
        python3.7-dev \
        python3-dev \
        python3-pip \
        curl \
        git \
        postgresql-client \
        libpq-dev \
        && ln -sf $(which python3.7) $(which python3) \
        && pip3 install --upgrade setuptools wheel \
        && { curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/${POETRY_VERSION}/get-poetry.py | python3 ; } \
        && apt-get remove -y curl wget vim && apt-get autoremove -y

# Add poetry to path
ENV PATH "/root/.poetry/bin:${PATH}"

WORKDIR /tools
COPY poetry.lock pyproject.toml /tools/
RUN ["poetry", "install", "--no-root"]


FROM jackgreenberg/poetry as final
COPY --from=dependencies /usr/local/lib/python3.7/dist-packages /usr/local/lib/python3.7/dist-packages

ARG AZURE_APPLICATION_ID
ARG AZURE_TENANT_ID
ARG AZURE_CLIENT_SECRET

WORKDIR /tools

COPY . /tools/
RUN poetry config virtualenvs.create false && poetry install

CMD ["/tools/scripts/entrypoint.sh"]
