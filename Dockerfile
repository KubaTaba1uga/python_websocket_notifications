FROM python:3.11.4-slim-bullseye

RUN apt-get update

RUN apt-get install -y libpq-dev python-dev python3-dev gcc

WORKDIR /code

COPY ./requirements.txt /code/

RUN pip install -r requirements.txt

COPY ./notifications_service /code/src

COPY ./shared /code/shared

CMD ["uvicorn", "src.web_app:app", "--host", "0.0.0.0", "--port", "80"]
