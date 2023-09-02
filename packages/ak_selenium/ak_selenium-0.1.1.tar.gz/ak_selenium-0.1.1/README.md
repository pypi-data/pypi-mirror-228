<!--- Heading --->
<div align="center">
  <h1>ak_selenium</h1>
  <p>
    Selenium package with requests integration and anti-bot detection measures
  </p>
<h4>
    <a href="https://github.com/rpakishore/ak_selenium">Documentation</a>
  <span> · </span>
    <a href="https://github.com/rpakishore/ak_selenium/issues/">Report Bug</a>
  <span> · </span>
    <a href="https://github.com/rpakishore/ak_selenium/issues/">Request Feature</a>
  </h4>
</div>
<br />

![GitHub commit activity](https://img.shields.io/github/commit-activity/m/rpakishore/ak_selenium)
![GitHub last commit](https://img.shields.io/github/last-commit/rpakishore/ak_selenium)
[![tests](https://github.com/rpakishore/ak_selenium/actions/workflows/test.yml/badge.svg)](https://github.com/rpakishore/ak_selenium/actions/workflows/test.yml)

<!-- Table of Contents -->
<h2>Table of Contents</h2>

- [1. About the Project](#1-about-the-project)
  - [1.1. Features](#11-features)
- [2. Getting Started](#2-getting-started)
  - [2.1. Dependencies](#21-dependencies)
  - [2.3. Installation](#23-installation)
    - [2.3.1. Production](#231-production)
    - [2.3.2. Development](#232-development)
- [3. Usage](#3-usage)
  - [Additional Options](#additional-options)
- [4. Roadmap](#4-roadmap)
- [5. License](#5-license)
- [6. Contact](#6-contact)
- [7. Acknowledgements](#7-acknowledgements)

<!-- About the Project -->
## 1. About the Project

`ak_selenium` is a Python package that provides an interface for automating browser tasks using Selenium. It comes with built-in functionalities for handling common tasks such as form filling, scrolling, and waiting for elements to load. Additionally, it has a built-in requests session that handles retries and timeouts, making it easier to send HTTP requests.

<!-- Features -->
### 1.1. Features

- Chrome browser automation using Selenium WebDriver.
- Built-in methods for form filling, scrolling, and waiting for elements.
- Anti-bot detection measures
- Pass selenium headers/cookies to requests library
- Built-in requests session with retries and timeouts.
- Ability to use Chrome user data for browser automation.
- RAM optimization for browser options.

<!-- Getting Started -->
## 2. Getting Started

### 2.1. Dependencies

Create the virutual environment and install dependencies

```bash
python -m venv .venv

.venv\Scripts\activate.bat

pip install flit
```

<!-- Installation -->
### 2.3. Installation

#### 2.3.1. Production

Install with flit

```bash
  flit install --deps production
```

Alternatively, you can use pip

```bash
pip install ak_selenium
```

#### 2.3.2. Development

Install with flit

```bash
  flit install --pth-file
```

<!-- Usage -->
## 3. Usage

```python
from ak_selenium import Chrome, By, Keys

from ak_selenium import Chrome

# Create a new Chrome browser instance
browser = Chrome(headless=True)

#Get Chromedriver
driver = chrome.driver

# Navigate to a webpage
driver.get("https://example.com")

# Wait for an element to load
#Wait for elements to load
locator = (By.TAG_NAME, "h1")
chrome.Wait_for_locator(locator)

# Fill a form
element = browser.driver.find_element_by_id("my-form")
browser.fill_userinput_form(element, "Hello, world!")

# Pass selenium session to requests
s = chrome.session

# Get a website
s.get("https://www.iana.org/domains/reserved")

# Get a list of websites
## Will randomize requests to not trigger bot detection
s.bulk_get(["https://www.iana.org/domains/reserved", "https://www.example.com"])
```

### Additional Options

```python
# Selenium Overrides
## Overide default useragent
chrome.USERAGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                    AppleWebKit/537.36 (KHTML, like Gecko) \
                    Chrome/83.0.4103.53 Safari/537.36'

## Override implicit and max wait times for selenium
chrome.IMPLICITLY_WAIT_TIME = 3 #seconds
chrome.MAX_WAIT_TIME = 5 #seconds

# Requests.Session Override
MAX_RETRY = 5
MIN_REQUEST_GAP = 0.9 #seconds between requests
```

<!-- Roadmap -->
## 4. Roadmap

- [ ] Add beautifulsoup integration
- [ ] Proxy

<!-- License -->
## 5. License

See LICENSE for more information.

<!-- Contact -->
## 6. Contact

Arun Kishore - [@rpakishore](mailto:pypi@rpakishore.co.in)

Project Link: [https://github.com/rpakishore/ak_selenium](https://github.com/rpakishore/ak_selenium)

<!-- Acknowledgments -->
## 7. Acknowledgements

- [Awesome README Template](https://github.com/Louis3797/awesome-readme-template/blob/main/README-WITHOUT-EMOJI.md)
- [Banner Maker](https://banner.godori.dev/)
- [Shields.io](https://shields.io/)
- [Carbon](https://carbon.now.sh/)