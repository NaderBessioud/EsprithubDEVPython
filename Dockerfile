from python:3.9.12-slim-buster
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*
 
COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD ["python3 badwords.py && python3 UserProfiling.py"]


