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
