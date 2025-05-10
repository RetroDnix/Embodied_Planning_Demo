FROM python:3.10.0

ADD . /code

WORKDIR /code

RUN pip install -r requirements.txt
