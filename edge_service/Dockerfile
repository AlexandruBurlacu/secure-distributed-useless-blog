FROM python:3.7-slim

RUN useradd -ms /bin/bash usser

USER usser

RUN mkdir /home/usser/app

WORKDIR /home/usser/app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

USER root

RUN chmod -R 1555 /home/usser/app

USER usser

ENV GUNICORN_CMD_ARGS="--worker-class=gevent --workers=10 --certfile=certificate.pem --keyfile=key.pem --bind=0.0.0.0:5000"

CMD [ "/home/usser/.local/bin/gunicorn", "wsgi:app" ]