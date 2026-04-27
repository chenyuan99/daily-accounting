FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

RUN mkdir -p /code
COPY ./requirements.txt /code

WORKDIR /code

RUN apt-get update && \
    apt-get -y install --no-install-recommends \
    libsasl2-dev python3-dev libldap2-dev libssl-dev libsnmp-dev libpq-dev && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir -r requirements.txt

COPY ./* /code/