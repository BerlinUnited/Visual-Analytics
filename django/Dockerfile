FROM ubuntu:22.04
ENV DEBIAN_FRONTEND=noninteractive
# show the stdout and stderr streams right in the command line instead of getting buffered.
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get -y --no-install-recommends install \
    curl \
    gpg \
    wget \
    software-properties-common \
    ca-certificates \
    lsb-release \
    gnupg2 

RUN sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -

RUN add-apt-repository -y ppa:deadsnakes/ppa
RUN apt-get update
RUN apt-get install -y --no-install-recommends python3.11 python3.11-dev python3.11-venv

RUN apt-get update && apt-get -y --no-install-recommends install \
    git \
    python3-pip \
    nano \
    postgresql-client-16

RUN mkdir /django
WORKDIR /django
COPY . .

RUN python3.11 -m venv /venv
ENV PATH=/venv/bin:$PATH

RUN pip install -r requirements.txt

RUN python --version >&2
EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000","-w","8", "core.wsgi"]