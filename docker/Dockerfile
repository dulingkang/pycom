FROM python:3.9.4-slim-buster

WORKDIR /app

RUN sed -i s@/deb.debian.org/@/mirrors.aliyun.com/@g /etc/apt/sources.list \
    && sed -i s@/security.debian.org/@/mirrors.aliyun.com/@g /etc/apt/sources.list

RUN apt-get clean && apt-get update \
    && apt-get install gcc apt-utils zlib1g-dev \
    libcurl4-openssl-dev libssl-dev git python3-dev build-essential -y \
    && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

ENTRYPOINT ["python", "app.py"]
