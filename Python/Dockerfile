FROM python:3.8.12

ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code

COPY ./requirements.txt /code/

RUN apt update
RUN apt install -y sqlite3 vim less libgl1-mesa-dev
RUN pip install -r requirements.txt

EXPOSE 8000