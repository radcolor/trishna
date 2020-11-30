FROM python:3.8.4-slim-buster

RUN apt update && apt upgrade -y && \
    apt install --no-install-recommends -y \
    debian-keyring \
    debian-archive-keyring \
    bash \
    curl \
    git \
    sudo \
    python3-pip \
    python3-requests \
    python3

RUN mkdir /app
ADD . /app
WORKDIR /app

RUN pip3 install --upgrade pip setuptools
RUN pip3 install -U -r requirements.txt

CMD python3 /app/main.py 
