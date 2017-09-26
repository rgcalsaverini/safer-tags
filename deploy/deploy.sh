#!/bin/bash

add-apt-repository -y ppa:nginx/stable
apt-get -y update
apt-get -y upgrade
apt-get -y install \
    build-essential \
    git \
    libffi-dev \
    libmysqlclient-dev \
    libpcre3 \
    libpcre3-dev \
    libssl-dev \
    iputils-ping \
    mysql-client \
    nginx \
    nodejs-legacy \
    npm \
    python3 \
    python3-dev \
    python3-pip \
    python-setuptools
python3 -m pip install uwsgi gevent
