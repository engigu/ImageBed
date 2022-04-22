FROM python:3.6.12-slim-stretch

LABEL MAINTAINER="sayheya@qq.com"
ADD requirements.txt /app/requirements.txt
ENV TZ=Asia/Shanghai

RUN sed -i 's@/deb.debian.org/@/mirrors.163.com/@g' /etc/apt/sources.list \
    && sed -i 's@/security.debian.org/@/mirrors.163.com/@g' /etc/apt/sources.list \
    && echo "${TZ}" > /etc/timezone \
    && ln -sf /usr/share/zoneinfo/${TZ} /etc/localtime \
    && apt update \
    && apt install -y gcc \
    && pip install -r /app/requirements.txt -i https://mirrors.aliyun.com/pypi/simple/ \
    && rm -rf /var/lib/apt/lists/*

EXPOSE 8000
COPY . /app
WORKDIR /app

ENTRYPOINT ["sh", "docker-entrypoint.sh"]

