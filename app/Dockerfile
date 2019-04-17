FROM ubuntu:16.04

MAINTAINER SravaniM "sravani.manukonda7@gmail.com"

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev python-setuptools libcurl4-openssl-dev libssl-dev

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

ENTRYPOINT [ "python" ]

CMD [ "app.py" ]
