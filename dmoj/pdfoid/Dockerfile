FROM python:3.11-slim-bullseye

RUN apt-get update && \
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

RUN python3 - <<'PYEOF'
import io
p = '/pdfoid/pdfoid/backends/direct.py'
src = io.open(p, encoding='utf-8').read()

src = src.replace(
    'from selenium.common.exceptions import TimeoutException\n',
    'from selenium.common.exceptions import TimeoutException\n'
    'from selenium.webdriver.chrome.service import Service as ChromeService\n',
    1,
)

src = src.replace(
    "        options.add_argument('--headless')\n"
    "        options.binary_location = self.backend.chrome_path\n"
    "\n"
    "        browser = webdriver.Chrome(self.backend.chromedriver_path, options=options)\n",
    "        options.add_argument('--headless=new')\n"
    "        if self.backend.chrome_path:\n"
    "            options.binary_location = self.backend.chrome_path\n"
    "\n"
    "        service = ChromeService(executable_path=self.backend.chromedriver_path)\n"
    "        browser = webdriver.Chrome(service=service, options=options)\n",
    1,
)

src = src.replace(
    "            subprocess.check_output([self.backend.exiftool_path, '-Title=%s' % title, self.output_pdf_file])\n"
    "        except subprocess.CalledProcessError as e:\n",
    "            subprocess.check_output([self.backend.exiftool_path, '-Title=%s' % title, self.output_pdf_file])\n"
    "        except FileNotFoundError:\n"
    "            raise RuntimeError('exiftool not found on PATH (set EXIFTOOL_PATH or install libimage-exiftool-perl)')\n"
    "        except subprocess.CalledProcessError as e:\n",
    1,
)

io.open(p, 'w', encoding='utf-8').write(src)

assert 'ChromeService' in src, 'Service import not patched'
assert '--headless=new' in src, 'headless=new not patched'
assert 'service=service' in src, 'webdriver.Chrome not patched'
assert 'exiftool not found on PATH' in src, 'exiftool branch not patched'
PYEOF

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
