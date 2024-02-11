import os
import pytest
from selenium import webdriver

from leonard.pages.login_page import LoginPage
from leonard.pages.feed_page import FeedPage
from leonard.pages.api_page import ApiPage
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from _pytest.config import Config


def GetDriver(config: Config):
    browser = config.getoption('browser')
    url = config.getoption('url')
    vnc = config.getoption('vnc')
    selenoid = config.getoption('selenoid')

    if browser == 'chrome':
        options = webdriver.ChromeOptions()
        options.set_capability('browserName', 'chrome')
        options.set_capability('browserVersion', '112.0')
        if selenoid:
            if vnc:
                options.set_capability('selenoid:options', {
                    'enableVNC': True
                })
            driver = webdriver.Remote(
                'http://127.0.0.1:4444/wd/hub',
                options=options
            )
        else:
            driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=options,
            )
    else:
        raise RuntimeError(f'Unsupported browser: "{browser}"')

    driver.get(url)
    driver.maximize_window()
    return driver


@pytest.fixture()
def driverFactory(pytestconfig):
    drivers = []

    def _driver():
        driver = GetDriver(pytestconfig)
        drivers.append(driver)
        return driver

    yield _driver

    for driver in drivers:
        driver.quit()


@pytest.fixture(scope='session')
def profileID():
    idAuthor = os.environ['LEO_ID']
    idDonator = os.environ['LEO_ID_DONATOR']

    def _predicate(aAsAuthor: bool):
        return idAuthor if aAsAuthor else idDonator
    return _predicate


@pytest.fixture(scope='session')
def credentialsAuthor():
    login = os.environ['LEO_LOGIN']
    password = os.environ['LEO_PASSWORD']
    return login, password


@pytest.fixture(scope='session')
def credentialsDonator():
    login = os.environ['LEO_LOGIN_DONATOR']
    password = os.environ['LEO_PASSWORD_DONATOR']
    return login, password


def GetCookies(credentials, config):
    driver = GetDriver(config)

    loginPage = LoginPage(driver)
    loginPage.Login(*credentials)

    _ = FeedPage(driver)
    _ = ApiPage(driver, True)

    cookies = driver.get_cookies()
    driver.quit()
    return cookies


@pytest.fixture(scope='session')
def cookies(credentialsAuthor, credentialsDonator, pytestconfig):
    cookies = []
    cookies.append(GetCookies(credentialsAuthor, pytestconfig))
    cookies.append(GetCookies(credentialsDonator, pytestconfig))

    def _predicate(aAsAuthor: bool):
        return cookies[0] if aAsAuthor else cookies[1]
    return _predicate
