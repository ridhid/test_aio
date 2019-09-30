FROM python:3.7-alpine


ENV PYTHONUNBUFFERED 1

RUN apk --update --no-cache add postgresql-libs tzdata && pip install --upgrade pip
RUN mkdir /app
WORKDIR /app
RUN mkdir /app/config

RUN apk add --no-cache --update --virtual .build-deps  \
    py3-pip \
    build-base \
    linux-headers \
    postgresql-dev \
    gcc

COPY /config/base /app/config/base
RUN pip install -U --no-cache-dir -r /app/config/base/requirements.txt

COPY /config/prod/requirements.txt /app/config/prod/requirements.txt
RUN pip install -U --no-cache-dir -r /app/config/prod/requirements.txt

RUN find /usr/local \
        \( -type d -a -name test -o -name tests \) \
        -o \( -type f -a -name '*.pyc' -o -name '*.pyo' \) \
        -exec rm -rf '{}' + &&\
    runDeps="$( \
        scanelf --needed --nobanner --recursive /usr/local \
                | awk '{ gsub(/,/, "\nso:", $2); print "so:" $2 }' \
                | sort -u \
                | xargs -r apk info --installed \
                | sort -u \
    )" \
    && apk add --virtual .rundeps $runDeps \
    && apk del --no-cache .build-deps &&   rm -rf /var/cache/apk/*

COPY /docker/start.sh ./start.sh
COPY . /app

RUN pip install -e /app

EXPOSE 8000
CMD ./start.sh
