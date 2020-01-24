FROM python:3.7-alpine

ADD . /code

WORKDIR /code

RUN apk add --no-cache python3-dev libffi-dev openssl-dev build-base

RUN ["pip", "install", "-r", "requirements.txt"]

RUN ["python", "-m", "unittest", "discover", "tests"]

CMD ["uwsgi", "--ini", "project.ini"]
