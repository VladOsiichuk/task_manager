FROM python:3.7-slim-buster

RUN apt-get update && apt-get install --no-install-recommends -y python3.7-dev build-essential zlib1g-dev gcc libpq-dev && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY . /app

CMD alembic upgrade head && exec uvicorn --host 0.0.0.0 --port 8000 app.main:app

