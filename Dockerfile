FROM python:3.7-buster

RUN mkdir /tools
WORKDIR /tools

COPY . /tools

RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

CMD ["/tools/scripts/entrypoint.sh"]
