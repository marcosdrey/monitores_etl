FROM python:3.13-slim
ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app
COPY . .

RUN pip install --upgrade pip
RUN pip install poetry

RUN poetry config installer.max-workers 10
RUN poetry install --no-interaction --no-ansi

EXPOSE 8501

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]