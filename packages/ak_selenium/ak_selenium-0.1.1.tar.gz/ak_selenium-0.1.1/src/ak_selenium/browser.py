from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement
from webdriver_manager.chrome import ChromeDriverManager
from pathlib import Path
import sys
from typing import Literal
import requests
from functools import cached_property
from requests.adapters import HTTPAdapter, Retry
import time
import random

DEFAULT_TIMEOUT_s = 5 #seconds

class TimeoutHTTPAdapter(HTTPAdapter):
    #Courtesy of https://findwork.dev/blog/advanced-usage-python-requests-timeouts-retries-hooks/
    def __init__(self, *args, **kwargs):
        self.timeout = DEFAULT_TIMEOUT_s
        if "timeout" in kwargs:
            self.timeout = kwargs["timeout"]
            del kwargs["timeout"]
        super().__init__(*args, **kwargs)

    def send(self, request, **kwargs):
        timeout = kwargs.get("timeout")
        if timeout is None:
            kwargs["timeout"] = self.timeout
        return super().send(request, **kwargs)
    
class RequestsSession:
    MAX_RETRY = 5
    MIN_REQUEST_GAP = 0.9 #seconds
    last_request_time = None
    
    def __init__(self):
        session = requests.Session()
        self._set_default_headers()
        session = self._set_default_retry_adapter(session=session)
        self.session = session

    def __repr__(self) -> str:
        return "RequestsSession()"
    
    def __str__(self) -> str:
        return "RequestsSession class initiated by Selenium Driver"

    def _set_default_retry_adapter(self, session: requests.Session) -> requests.Session:
        retries = Retry(total=self.MAX_RETRY,
                        backoff_factor=0.5,
                        status_forcelist=[429, 500, 502, 503, 504]
                        )
        session.mount('http://', TimeoutHTTPAdapter(max_retries=retries))
        session.mount('https://', TimeoutHTTPAdapter(max_retries=retries))
        return session
    
    def get(self, *args, **kwargs) -> requests.Response:
        min_req_gap = self.MIN_REQUEST_GAP
        if self.last_request_time is not None:
            elapsed_time = time.time() - self.last_request_time
            if elapsed_time < min_req_gap:
                time.sleep(min_req_gap - elapsed_time)
        self.last_request_time = time.time()
        return self.session.get(*args, **kwargs)
    
    def bulk_get(self, urls: list[str], *args, **kwargs) -> list[requests.Response]:
        duplicate_list = urls[:]
        random.shuffle(duplicate_list)  #shuffle to prevent scrape detection
        
        req = {}
        for url in duplicate_list:
            req[url] = self.get(url, *args, **kwargs)
        return [req[url] for url in urls]
    
    def _set_default_headers(self) -> None:
        _header = {
            'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                            'AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/91.0.4472.124 Safari/537.36'),
            'Accept': ('text/html,application/xhtml+xml,application/xml;q=0.9,'
                        'image/avif,image/webp,*/*;q=0.8'),
            'Accept-Language': 'en-CA,en-US;q=0.7,en;q=0.3',
            'Connection': 'keep-alive',
            'Referer': 'https://www.google.com/',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1'
            }
        self.update_header(header=_header)
    
    def update_header(self, header: dict) -> requests.Session:
        self.session.headers.update(header)
        return self.session
    
    def update_cookies(self, cookies: list[dict]) -> requests.Session:
        self.session.cookies.update({c['name']: c['value'] for c in cookies})
        return self.session
    
class Chrome:
    USERAGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                AppleWebKit/537.36 (KHTML, like Gecko) \
                Chrome/83.0.4103.53 Safari/537.36'
    IMPLICITLY_WAIT_TIME = 3
    MAX_WAIT_TIME = 5
    EXCEPTIONS = exceptions

    def __init__(self, headless:bool = False, 
        chrome_userdata_path:str|None=None, half_screen:bool=True) -> None:
        
        self.headless = headless
        self._set_userdata_path(datapath=chrome_userdata_path)
        self.half_screen = half_screen
        return None
    
    def _set_userdata_path(self, datapath: str | None) -> str | None:
        self.chrome_userdata_path: str | None = None
        
        if not datapath and sys.platform=="win32":
            _chrome_userdata_path: Path = Path.home() / 'AppData' / 'Local' / 'Google' / 'Chrome' / 'User Data'
            if not _chrome_userdata_path.exists():
                self.chrome_userdata_path = None
            else:
                self.chrome_userdata_path = str(_chrome_userdata_path)
        
        return self.chrome_userdata_path
    
    def __str__(self) -> str:
        return f"""
        Chrome.Object
        UserAgent:{self.USERAGENT}
        Implicit Wait Time: {self.IMPLICITLY_WAIT_TIME:.2f}s
        Max Wait Time: {self.MAX_WAIT_TIME:.2f}s
        Headless: {self.headless}
        Chrome Userdata Path: {self.chrome_userdata_path}
        Half Screen View: {self.half_screen}
        """
    
    def __repr__(self) -> str:
        return f"Chrome(headless={self.headless},\
                chrome_userdata_path={self.chrome_userdata_path},\
                half_screen={self.half_screen})"
    
    def __del__(self) -> None:
        if self.driver:
            self.driver.quit()
        return None
    
    @cached_property
    def driver(self) -> webdriver.Chrome:
        """
        Initializes a Chrome web driver with specific options and configurations.
        
        Returns:
            webdriver.Chrome: The initialized Chrome driver object.
        """
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-gpu')
        if self.headless:
            options.add_argument('--headless')
            options.add_argument("--window-size=1920,1080")
        options.add_argument("start-maximized")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        if self.chrome_userdata_path:
            options.add_argument('--user-data-dir=' + self.chrome_userdata_path)
        options.add_experimental_option('useAutomationExtension', False)
    
        options = self._ram_optimization_browser_options(options)

        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options)

        driver.implicitly_wait(self.IMPLICITLY_WAIT_TIME) 

        driver.execute_script('window.focus()')
        driver.execute_cdp_cmd('Network.setUserAgentOverride',
                                {"userAgent": self.USERAGENT})

        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument",
        {
            "source": """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
                })
                """})

        driver.execute_cdp_cmd("Network.enable", {})
        driver.execute_cdp_cmd("Network.setExtraHTTPHeaders",
                                {"headers": {"User-Agent": "browser1"}})

        if self.half_screen:
            size = driver.get_window_size()
            driver.set_window_size(size['width']/2, size['height'])
            driver.set_window_position(size['width']/2-13, 0)
            
        return driver
        
    @staticmethod
    def _ram_optimization_browser_options(options: Options) -> Options:
        options.add_argument("disable-infobars")
        options.add_experimental_option("excludeSwitches", 
                                        ['enable-automation', "enable-logging"])
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-application-cache")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--lang=en-US")
        
        # Based on https://stackoverflow.com/questions/59514049/unable-to-sign-into-google-with-selenium-automation-because-of-this-browser-or
        options.add_argument("--allow-running-insecure-content")
        options.add_argument("--disable-web-security")
        return options
    
    def wait_for_locator(self, locator: tuple) -> None:
        """
        Wait until the element with the specified locator is present.

        Args:
            locator (tuple): The locator tuple (By, value) of the element to wait for.
        """
        (
            WebDriverWait(self.driver, self.MAX_WAIT_TIME, 0.5)
            .until(EC.presence_of_element_located(locator))
        )
        return None

    @staticmethod
    def fill_userinput_form(element: WebElement, 
                            text: str, clear_existing: bool=True) -> None:
        """
        Fill a user input form element with the specified text.

        Args:
            element (WebElement): The input form element.
            text (str): The text to fill in the form element.
            clear_existing (bool): Whether to clear existing text before filling.\
                Defaults to True.
        """
        if clear_existing:
            element.clear()
        element.send_keys(text)
        
        return None
    
    @cached_property
    def base_session(self) -> RequestsSession:
        _s = RequestsSession()
        return _s
    
    @property
    def session(self) -> RequestsSession:
        driver = self.driver
        s = self.base_session
        s.update_cookies(driver.get_cookies())
        s.update_header({
        "Accept-Language": driver.execute_script("return window.navigator.language;"),
        "X-Forwarded-For": driver.execute_script("return window.navigator.ip;"),
        "X-Timezone": driver.execute_script("return window.navigator.timezone;"),
        "User-Agent": driver.execute_script("return window.navigator.userAgent;"),
        })
        return s
    
    @staticmethod
    def find_element_by_text(elements:list[WebElement], text: str) -> WebElement | None:
        """
        Finds a WebElement from a list based on its text content.

        Args:
            elements (List[WebElement]): The list of WebElements to search through.
            text (str): The text to match against the elements' text content.

        Returns:
            WebElement or None: The first WebElement that matches the provided text,\
                or None if no match is found.
        """
        for element in elements:
            if element.text.strip() == text:
                return element
        return None
    
    def scroll(self, direction: Literal["top", "bottom"] = "bottom", 
                alternative_method: bool = False) -> None:
        """
        Scroll the webpage to the specified direction.
        Args:
            direction (Literal["top", "bottom"]): The direction to scroll. Valid 
                values are "top" and "bottom". Defaults to "bottom"
            alternative_method (bool): Uses `Keys` to scroll. Defaults to False.
        """
        _el = self.driver.find_element(By.TAG_NAME, 'div')
        match direction:
            case "top":
                if alternative_method:
                    _el.send_keys(Keys.HOME)
                else:
                    self.driver.execute_script("window.scrollTo(0, 0)")
                
            case "bottom":
                if alternative_method:
                    _el.send_keys(Keys.END)
                else:
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # noqa: E501