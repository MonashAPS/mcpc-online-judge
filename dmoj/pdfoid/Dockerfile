FROM python:3.11-slim-bullseye

RUN printf '%s\n' \
        'deb [check-valid-until=no] http://snapshot.debian.org/archive/debian/20260901T000000Z bullseye main' \
        'deb [check-valid-until=no] http://snapshot.debian.org/archive/debian-security/20260901T000000Z bullseye-security main' \
        'deb [check-valid-until=no] http://snapshot.debian.org/archive/debian/20260901T000000Z bullseye-updates main' \
        > /etc/apt/sources.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        curl gnupg git unzip xvfb libxi6 libgconf-2-4 exiftool ca-certificates && \
    install -m 0755 -d /etc/apt/keyrings && \
    curl -fsSL https://dl-ssl.google.com/linux/linux_signing_key.pub \
        | gpg --dearmor -o /etc/apt/keyrings/google-chrome.gpg && \
    echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main" \
        > /etc/apt/sources.list.d/google-chrome.list && \
    sed -r -i 's/^deb(.*)$/deb\1 contrib/g' /etc/apt/sources.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        google-chrome-stable fonts-noto ttf-mscorefonts-installer && \
    rm -rf /var/lib/apt/lists/* && \
    useradd -m pdfoid

RUN git clone https://github.com/DMOJ/pdfoid.git pdfoid && \
    cd pdfoid && git checkout 865c5b5
WORKDIR /pdfoid/

COPY pdfoid/patch_direct.py /tmp/patch_direct.py
RUN python3 /tmp/patch_direct.py && rm /tmp/patch_direct.py

RUN pip3 install -e . 'selenium>=4.10' && \
    SM=$(python3 -c "import selenium, os; print(os.path.join(os.path.dirname(selenium.__file__), 'webdriver/common/linux/selenium-manager'))") && \
    DRIVER=$("$SM" --browser chrome --output json | python3 -c "import sys,json; print(json.load(sys.stdin)['result']['driver_path'])") && \
    cp "$DRIVER" /usr/local/bin/chromedriver && \
    chmod +x /usr/local/bin/chromedriver && \
    rm -rf /root/.cache/selenium

ENV CHROMEDRIVER_PATH=/usr/local/bin/chromedriver
ENV EXIFTOOL_PATH=/usr/bin/exiftool

EXPOSE 8888
USER pdfoid
ENTRYPOINT pdfoid --address=pdfoid --port=8888
