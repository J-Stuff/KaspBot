FROM python:3.11

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

ADD main.py main.py

COPY requirements.txt /tmp/requirements.txt

COPY main.py /worker/main.py
COPY /cogs /worker/cogs/
COPY /config /worker/config/
COPY /database /worker/database/
COPY /modules /worker/modules/

RUN mkdir /worker/temp
RUN mkdir /worker/logs

WORKDIR /worker

RUN python3 -m pip install -r /tmp/requirements.txt
RUN rm /tmp/requirements.txt

CMD python /worker/main.py