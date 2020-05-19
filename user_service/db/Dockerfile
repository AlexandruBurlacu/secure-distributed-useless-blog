FROM postgres:10.4-alpine

# run create.sql on init
COPY ./create.sql /docker-entrypoint-initdb.d/init.sql

RUN chmod a+r /docker-entrypoint-initdb.d/*
