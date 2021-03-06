FROM ubuntu:18.04

RUN rm /etc/apt/sources.list
ADD sources.list /etc/apt/sources.list

RUN buildDeps='software-properties-common git libtool cmake python-dev python3-pip python-pip libseccomp-dev' && \
    apt-get update && apt-get install -y python python3.6 python-pkg-resources python3-pkg-resources gcc g++ $buildDeps && \
    add-apt-repository ppa:openjdk-r/ppa && apt-get update && apt-get install -y openjdk-11-jdk && \
    add-apt-repository ppa:pypy/ppa && apt-get update && apt-get install -y pypy3 &&\
    pip3 install --no-cache-dir psutil gunicorn flask requests logzero

RUN git clone https://github.com/csswust/lorun && \
    cd /lorun && python3 setup.py build && python3 setup.py install &&\
    apt-get purge -y --auto-remove $buildDeps && \
    apt-get clean && rm -rf /var/lib/apt/lists/* && \
    mkdir -p /code && \
    useradd -u 12001 compiler && useradd -u 12002 code && useradd -u 12003 spj && usermod -a -G code spj

