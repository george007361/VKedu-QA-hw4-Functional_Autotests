import os
import pytest
from selenium import webdriver

from utils import GetDriver
from pages.login_page import LoginPage
from pages.feed_page import FeedPage
from pages.api_page import ApiPage


def pytest_addoption(parser):
    parser.addoption('--browser', default='chrome')
    parser.addoption('--url', default='https://www.vdonate.ml')
    parser.addoption('--vnc', action='store_true')


@pytest.fixture()
def driver(pytestconfig):
    browser = pytestconfig.getoption('browser')
    url = pytestconfig.getoption('url')
    vnc = pytestconfig.getoption('vnc')

    if browser == 'chrome':
        options = webdriver.ChromeOptions()
        options.set_capability('browserName', 'chrome')
        options.set_capability('browserVersion', '112.0')
    elif browser == 'firefox':
        options = webdriver.FirefoxOptions()
        options.set_capability('browserName', 'firefox')
        options.set_capability('browserVersion', '112.0')
    else:
        raise RuntimeError(f'Unsupported browser: "{browser}"')

    if vnc:
        options.set_capability('selenoid:options', {
            'enableVNC': True
        })

    driver = webdriver.Remote(
        'http://127.0.0.1:4444/wd/hub',
        options=options
    )
    driver.get(url)
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.fixture(scope='session')
def credentials():
    login = os.environ['LOGIN']
    password = os.environ['PASSWORD']
    return login, password


@pytest.fixture(scope='session')
def cookies(credentials, pytestconfig):
    driver = GetDriver(pytestconfig.getoption('browser'))
    driver.get(pytestconfig.getoption('url'))

    loginPage = LoginPage(driver)
    loginPage.Login(*credentials)

    _ = FeedPage(driver)
    _ = ApiPage(driver)

    cookies = driver.get_cookies()
    driver.quit()
    return cookies
