FROM python:3.9.13-slim-buster as builder

RUN pip install poetry==1.2.2

WORKDIR /usr

COPY poetry.lock ./pyproject.toml ./

RUN poetry config virtualenvs.in-project true --local && poetry install --only main


FROM python:3.9.13-slim-buster as compile-image

WORKDIR /usr/sberbank_app

COPY --from=builder /usr /usr
COPY .. ./

RUN apt update && apt install -y build-essential

ENV PATH="/usr/.venv/bin:$PATH"
ENV PYTHONPATH="/usr/sberbank_app:$PYTHONPATH"
