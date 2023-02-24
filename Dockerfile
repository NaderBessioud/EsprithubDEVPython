from python:3.9.12-slim-buster
RUN apk update
COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .

