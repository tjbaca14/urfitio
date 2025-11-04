FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    libssl-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN pip install poetry

COPY pyproject.toml poetry.lock README.md ./

COPY ./app app

COPY ./alembic /alembic

COPY ./alembic.ini ./

COPY ./data /data

COPY ./startup.sh /startup.sh


RUN chmod +x /startup.sh

RUN poetry install 

# For debug 
# CMD ["tail", "-f", "/dev/null"]

CMD ["/startup.sh"]


