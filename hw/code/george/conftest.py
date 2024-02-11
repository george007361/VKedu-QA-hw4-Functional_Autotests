import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

from pages.signin_page import SigninPage
import os


def get_driver(pytestconfig):
    browser = pytestconfig.getoption('browser')
    url = pytestconfig.getoption('url')
    vnc = pytestconfig.getoption('vnc')
    is_selenoid = pytestconfig.getoption('selenoid')

    driver = None
    options = None
    capabilities = {}

    if vnc and is_selenoid:
        capabilities['enableVNC'] = True

    if browser == 'chrome':
        options = webdriver.ChromeOptions()
        capabilities['browserName'] = 'chrome'
        capabilities['version'] = '112.0'

        if is_selenoid:
            driver = webdriver.Remote(
                'http://127.0.0.1:4444/wd/hub',
                options=options,
                desired_capabilities=capabilities,
            )
        else:
            driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=options,
                desired_capabilities=capabilities,
            )
        driver.get(url)

    assert driver is not None
    driver.set_window_size(1920, 1080)
    return driver

@pytest.fixture(scope='function', autouse=True)
def browser(pytestconfig):
    driver = get_driver(pytestconfig)
    yield driver
    driver.quit()

@pytest.fixture(scope='session')
def cookies(pytestconfig):
    driver = get_driver(pytestconfig)
    driver.get(pytestconfig.getoption('url'))

    login_page = SigninPage(driver)
    login_page.signin(os.getenv('GEORGE_LOGIN'), os.getenv('GEORGE_PASSWORD'))

    api_url = "https://vdonate.ml/api/v1"
    driver.get(api_url)

    cookies = driver.get_cookies()
    driver.quit()
    return cookies
