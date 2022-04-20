FROM python:3.7-alpine

LABEL MAINTAINER="sayheya@163.com"

ADD requirements.txt /app/requirements.txt

ENV TZ=Asia/Shanghai
ENV RUN_IN_DOCKER=yes

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories \
	&& apk update \
    && apk add --no-cache --virtual .build-deps make gcc musl-dev tzdata \
    && echo "${TZ}" > /etc/timezone \
    && ln -sf /usr/share/zoneinfo/${TZ} /etc/localtime \
	&& pip install -r /app/requirements.txt -i https://mirrors.aliyun.com/pypi/simple/ \
    && rm /var/cache/apk/* \
    && apk del .build-deps 

EXPOSE 8000

COPY . /app
WORKDIR /app
RUN chmod +x /app/docker-entrypoint.sh

ENTRYPOINT ["docker-entrypoint.sh"]
