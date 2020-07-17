FROM alpine
RUN apk add --no-cache \
    python3-dev \

RUN mkdir /tools
WORKDIR /tools

COPY . /tools

RUN poetry config virtualenvs.create false \
    && poetry install $(test "$YOUR_ENV" == production && echo "--no-dev") \
        --no-interaction --no-ansi

CMD ["/tools/scripts/entrypoint.sh"]
