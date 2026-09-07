# Django 4.2 (DMOJ master) supports Python up to 3.12; its template Context
# breaks on 3.14 (copy(super()) in Context.__copy__), which 500s the admin.
FROM python:3.12-slim-trixie

RUN apt-get update && \
    apt-get install -y \
        git gcc g++ make curl gettext wget \
        libxml2-dev libxslt1-dev zlib1g-dev \
        mariadb-client libmariadb-dev \
        libjpeg-dev debconf-utils pkg-config && \
    curl -sL https://deb.nodesource.com/setup_26.x | bash - && \
    apt-get install -y nodejs && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

RUN npm install -g sass@1.99.0 postcss-cli postcss autoprefixer
RUN pip3 install \
        pymysql mysqlclient websocket-client uwsgi 'django-redis<6' redis

COPY repo/requirements.txt .
RUN pip3 install -r requirements.txt
