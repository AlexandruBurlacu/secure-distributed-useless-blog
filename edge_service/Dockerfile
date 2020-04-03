FROM python:3.7-slim

RUN useradd -ms /bin/bash usser

USER usser

RUN mkdir /home/usser/app

WORKDIR /home/usser/app

COPY . .

RUN pip install -r requirements.txt

USER root

RUN chmod -R 1555 /home/usser/app

USER usser

# CMD [ "python", "app.py" ]
CMD [ "gunicorn", "--worker-class gevent", "-w 10", "--certfile certificate.pem", "--keyfile key.pem", "-b 0.0.0.0:5000", "wsgi:app" ]