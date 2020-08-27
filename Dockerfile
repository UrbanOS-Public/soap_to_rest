FROM python:3.8 as base-python

RUN apt-get clean \
    && apt-get -y update

RUN apt-get -y install nginx \
    && apt-get -y install python3-dev \
    && apt-get -y install libpcre3 libpcre3-dev \
    && apt-get -y install build-essential \
    && apt-get -y install locales \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install 'poetry==1.0.9'

ADD pyproject.toml poetry.lock /

COPY soap_to_rest /soap_to_rest
RUN chmod +x soap_to_rest/start.sh

FROM base-python as test
COPY ./tests /tests
RUN apt-get -y update \
    && apt-get -y install libspatialindex-dev \
    && poetry install
RUN poetry run pytest /tests

FROM base-python as production

COPY nginx.conf /etc/nginx

WORKDIR /soap_to_rest
