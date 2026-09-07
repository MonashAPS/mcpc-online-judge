FROM python:3.11-slim-bullseye

RUN apt-get update && \
    apt-get install -y \
        git gcc g++ make curl gettext wget \
        libxml2-dev libxslt1-dev zlib1g-dev \
        pkg-config mariadb-client libmariadb-dev \
        libjpeg-dev debconf-utils && \
    curl -sL https://deb.nodesource.com/setup_16.x | bash - && \
    apt-get install -y nodejs && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

# Pinned to the last versions that run on Node 16: sass >= 1.79 needs chokidar 4
# (ESM-only) and postcss-cli >= 11 requires Node >= 18.
RUN npm install -g sass@1.77.8 postcss-cli@10.1.0 postcss@8.4.47 autoprefixer@10.4.20
# lxml_html_clean: lxml >= 5.2 moved lxml.html.clean out into its own package,
# and judge/migrations/0091 still imports it. requirements.txt does not pin lxml.
RUN pip3 install \
        pymysql mysqlclient websocket-client uwsgi django-redis redis \
        lxml_html_clean

COPY repo/requirements.txt .
RUN pip3 install -r requirements.txt
