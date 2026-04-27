FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN mkdir -p /code
COPY ./requirements.txt /code

WORKDIR /code

RUN apt-get update && \
    apt-get -y install --no-install-recommends \
    libpq-dev gcc \
    libsasl2-dev python3-dev libldap2-dev libssl-dev libsnmp-dev && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate --noinput && gunicorn rdie.wsgi --bind 0.0.0.0:${PORT:-8000} --workers 2 --log-file -"]
