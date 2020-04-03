FROM python:3.7-slim

RUN useradd -ms /bin/bash usser

USER usser

RUN mkdir /home/usser/app

WORKDIR /home/usser/app

COPY . .

# EXPOSE 5000

RUN pip install -r requirements.txt

# USER root

# RUN chmod -R 0504 /home/usser/app

USER usser

CMD [ "python", "app.py" ]
