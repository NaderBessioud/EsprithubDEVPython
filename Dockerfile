from 3.11.2-slim-buster
RUN apk update
COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .

