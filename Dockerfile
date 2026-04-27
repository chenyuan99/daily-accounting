FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /code

RUN apt-get update && \
    apt-get -y install --no-install-recommends \
    libsasl2-dev python3-dev libldap2-dev libssl-dev libsnmp-dev && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "rdie.wsgi", "--bind", "0.0.0.0:8000", "--log-file", "-"]
