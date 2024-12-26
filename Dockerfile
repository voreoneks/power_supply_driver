FROM python:3.10

ARG PROJECT_NAME=power_supply_driver
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN apt update && \
    pip3 install --upgrade pip && \
    pip3 install --upgrade setuptools && \
    pip3 install poetry

WORKDIR /opt/$PROJECT_NAME
COPY poetry.lock pyproject.toml /opt/$PROJECT_NAME
RUN poetry config virtualenvs.create false && poetry install --no-dev --no-interaction --no-ansi
COPY . /opt/$PROJECT_NAME
CMD python main.py
