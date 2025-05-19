FROM ubuntu:22.04

# show the stdout and stderr streams right in the command line instead of getting buffered.
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

RUN apt-get update && apt-get -y --no-install-recommends install \
    curl \
    gpg \
    wget \
    ca-certificates \
    lsb-release \
    gnupg2 \
    pigz 

RUN sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -

RUN apt-get update && apt-get -y --no-install-recommends install \
    git \
    python3 \
    python3-pip \
    nano \
    python-is-python3 \
    python3-dev \
    postgresql-client-16 && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir /backup
WORKDIR /backup
COPY backup.py backup.py

RUN pip install --no-cache-dir psycopg2-binary
