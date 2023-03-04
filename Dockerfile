FROM python:3.11

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

ADD main.py main.py

COPY requirements.txt /tmp/requirements.txt

COPY ./logs /logging

COPY ./config /config

COPY ./database /database

COPY . /worker
WORKDIR /worker

RUN python3 -m pip install -r /tmp/requirements.txt

CMD python /worker/main.py