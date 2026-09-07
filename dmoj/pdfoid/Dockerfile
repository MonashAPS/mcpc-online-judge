FROM python:3.14-slim-trixie

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl gnupg git unzip xvfb libxi6 exiftool wget && \
    mkdir -p /etc/apt/keyrings && \
    curl -fsSL https://dl.google.com/linux/linux_signing_key.pub | \
        gpg --dearmor --yes -o /etc/apt/keyrings/google-chrome.gpg && \
    echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/google-chrome.gpg] https://dl.google.com/linux/chrome/deb/ stable main" \
        >> /etc/apt/sources.list.d/google-chrome.list && \
    sed -i 's/^Components: main$/& contrib non-free/' /etc/apt/sources.list.d/debian.sources && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        google-chrome-stable fonts-noto ttf-mscorefonts-installer && \
    rm -rf /var/lib/apt/lists/* && \
    useradd -m pdfoid

RUN git clone https://github.com/DMOJ/pdfoid.git pdfoid
WORKDIR /pdfoid/
RUN pip3 install -e . && \
    # The old chromedriver.storage.googleapis.com feed stopped at Chrome 114; let
    # Selenium Manager fetch the driver matching the Chrome installed above.
    SM=$(python3 -c "import selenium, os; print(os.path.join(os.path.dirname(selenium.__file__), 'webdriver/common/linux/selenium-manager'))") && \
    DRIVER=$("$SM" --browser chrome --browser-path /usr/bin/google-chrome --output json | python3 -c "import sys, json; print(json.load(sys.stdin)['result']['driver_path'])") && \
    cp "$DRIVER" /usr/bin/chromedriver && chmod +x /usr/bin/chromedriver && rm -rf /root/.cache/selenium

ENV CHROME_PATH=/usr/bin/google-chrome
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver
ENV EXIFTOOL_PATH=/usr/bin/exiftool

EXPOSE 8888
USER pdfoid
ENTRYPOINT pdfoid --address=pdfoid --port=8888
