FROM python:3.6.9-alpine

RUN apk --update-cache \
    add curl \
    tzdata \
    gcc \
    g++ && \
    cp /usr/share/zoneinfo/Asia/Tokyo /etc/localtime && \
    apk del tzdata && \
    rm -rf /var/cache/apk/*

COPY requirements.txt .
RUN pip install -r requirements.txt

