FROM python:3.11.4-slim-bullseye

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./src /code/src

CMD ["uvicorn", "src.web_app:app", "--host", "0.0.0.0", "--port", "80"]
