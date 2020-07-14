import pandas as pd
import os
import time

from collections import namedtuple
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium import webdriver

from episcan.scraper.DOMElem import DOMElem

class HeadlessChrome:

    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36"

    def back(self, nb_pages=-1):
        self._check_open()
        self.chrome.execute_script(f"window.history.go({nb_pages})")

    def _is_win(self):
        try:
            os.uname()
            return False
        except AttributeError:
            return True

    def _is_wsl(self):
        try:
            return 'microsoft' in os.uname().release.lower()
        except AttributeError:
            return False

    def __getattr__(self, name):
        self._check_open()
        return getattr(self.chrome, name)

    def __init__(self, test=False, headless=True):
        """
        MyHeadlessChrome with user-agent fake.

        >>> driver = HeadlessChrome(True)
        >>> driver.get("https://intoli.com/blog/making-chrome-headless-undetectable/chrome-headless-test.html")
        >>> elem   = driver.find_element_by_id("user-agent")
        >>> elem.text == driver.user_agent
        True
        >>> driver.close()
        """
        options = webdriver.ChromeOptions()
        # specify headless mode

        if self._is_wsl():
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-gpu")
            options.add_argument("--disable-features=VizDisplayCompositor")
            options.add_argument("--disable-dev-shm-usage")

        if headless:
            options.add_argument('--headless')
            options.add_argument("--no-sandbox")
            options.add_argument("--start-maximized")

        # specify the desired user agent
        options.add_argument(f'user-agent={self.user_agent}')

        self.options = options
        self.exec    = "chromedriver.exe" if self._is_win() else "chromedriver"
        self.path    = os.path.join(os.getcwd(), self.exec)



    def __enter__(self):
        if os.path.isfile(self.path):
            self.chrome = webdriver.Chrome(options=self.options, executable_path=self.path)
        else:
            self.chrome = webdriver.Chrome(options=self.options)
        return self

    def _check_open(self):
        if not hasattr(self, 'chrome'):
            raise ValueError("Chrome Driver is not open, please use HeadlessChrome in a 'with' clause")


    def find_elem(self, elem, timeout=10):
        self._check_open()
        elem = WebDriverWait(self.chrome, timeout).until(
            EC.presence_of_element_located((elem.by, elem.value))
        )

        return elem

    def get_df_from_elem(self, elem):
        self._check_open()

        if isinstance(elem, DOMElem):
            elem = self.find_elem(elem)

        if not isinstance(elem, WebElement):
            raise TypeError("The argument 'elem' must be either a DOMElem or a WebElement")

        dfs  = pd.read_html(elem.get_attribute('outerHTML'))

        return dfs[0]

    def wait_for_url(self, url, timeout=float('+inf')):
        self._check_open()
        i = 0

        while self.chrome.current_url != url and i < timeout:
            time.sleep(1)
            i += 1

        if i == timeout:
            raise TimeoutError()

    def __exit__(self, type, value, traceback):
        self.chrome.close()
        del self.chrome
        return False


if __name__ == "__main__":
    import doctest
    doctest.testmod()
