from python:3.11.2-alpine
RUN apk update
COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .

