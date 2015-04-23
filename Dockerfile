FROM ubuntu:14.04.1
MAINTAINER justinc@yelp.com

run apt-get update && apt-get upgrade -y
run apt-get install -y wget language-pack-en-base

run locale-gen en_US en_US.UTF-8 && dpkg-reconfigure locales

run mkdir /src

workdir /src

run wget https://bitbucket.org/pypy/pypy/downloads/pypy-2.5.0-linux64.tar.bz2
run bunzip2 pypy-2.5.0-linux64.tar.bz2
run tar xvf pypy-2.5.0-linux64.tar

ENV PATH $PATH:/src/pypy-2.5.0-linux64/bin/

run wget https://bootstrap.pypa.io/get-pip.py
run pypy get-pip.py

run apt-get update && apt-get install -y build-essential git vim libpq5 libpq-dev


run ln -s /usr/bin/gcc /usr/local/bin/cc

run pip install virtualenv tox

VOLUME ["/data"]

WORKDIR /data

