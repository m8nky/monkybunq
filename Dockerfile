# https://hub.docker.com/_/python
FROM python:3.8-slim

# Install production dependencies.
RUN pip install bunq_sdk gspread oauth2client lxml dependency-injector

COPY src /app
COPY config /config

WORKDIR /app

ENTRYPOINT ["./run"]
