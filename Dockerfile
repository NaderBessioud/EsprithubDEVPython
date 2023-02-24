from 3.12.0a5-slim-buster
RUN apk update
COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .

