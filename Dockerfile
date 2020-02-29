FROM python:3.7.6-buster

RUN apt-get update && apt-get install locales alien -y
RUN localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8
ENV LANG en_US.utf8

RUN apt-get install netcat -y

WORKDIR /app

COPY requirements.txt /app/src/requirements.txt

RUN cd src/ && pip3 install -r requirements.txt

COPY src/ /app/src
