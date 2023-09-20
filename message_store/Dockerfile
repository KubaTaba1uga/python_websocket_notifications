FROM python:3.11.4-slim-bullseye


# Psycopg requirements
RUN apt-get update
RUN apt-get install -y libpq-dev python-dev python3-dev gcc

WORKDIR /code

COPY message_store/requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY message_store/src /code/src

COPY shared /code/shared

CMD ["uvicorn", "src.web_app:app", "--host", "0.0.0.0", "--port", "80"]
