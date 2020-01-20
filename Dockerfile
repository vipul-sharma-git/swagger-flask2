FROM python:3.7-alpine

#WORKDIR /usr/src/apps/assgn
#COPY . .
ADD . /code
WORKDIR /code
RUN ["pip", "install", "-r", "requirements.txt"]

RUN ["python", "-m", "unittest", "discover", "tests"]

CMD ["python", "server.py"]