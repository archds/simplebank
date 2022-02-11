FROM python:3.9-slim

WORKDIR /usr/src/app

RUN adduser --disabled-password --quiet worker
RUN chmod -R 777 .

COPY requirements.txt .
RUN python3 -m pip install --no-cache-dir -r ./requirements.txt

COPY app .

USER worker

CMD python bank.py
