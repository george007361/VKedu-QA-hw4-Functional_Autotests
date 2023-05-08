import os
import pytest
from selenium import webdriver

from leonard.pages.login_page import LoginPage
from leonard.pages.feed_page import FeedPage
from leonard.pages.api_page import ApiPage


@pytest.fixture()
def driverFactory(pytestconfig):
    drivers = []

    def _driver():
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
        drivers.append(driver)
        driver.get(url)
        driver.maximize_window()
        return driver

    yield _driver

    for driver in drivers:
        driver.quit()


@pytest.fixture(scope='session')
def profileID():
    idAuthor = os.environ['ID']
    idDonator = os.environ['ID_DONATOR']

    def _predicate(aAsAuthor: bool):
        return idAuthor if aAsAuthor else idDonator
    return _predicate


@pytest.fixture(scope='session')
def credentialsAuthor():
    login = os.environ['LOGIN']
    password = os.environ['PASSWORD']
    return login, password


@pytest.fixture(scope='session')
def credentialsDonator():
    login = os.environ['LOGIN_DONATOR']
    password = os.environ['PASSWORD_DONATOR']
    return login, password


def GetDriver(aBrowserName):
    if aBrowserName == 'chrome':
        options = webdriver.ChromeOptions()
        options.set_capability('browserName', 'chrome')
        options.set_capability('browserVersion', '112.0')
    elif aBrowserName == 'firefox':
        options = webdriver.FirefoxOptions()
        options.set_capability('browserName', 'firefox')
        options.set_capability('browserVersion', '112.0')
    else:
        raise RuntimeError(f'Unsupported browser: "{aBrowserName}"')

    driver = webdriver.Remote(
        'http://127.0.0.1:4444/wd/hub',
        options=options
    )
    driver.maximize_window()
    return driver


def GetCookies(credentials, config):
    driver = GetDriver(config.getoption('browser'))
    driver.get(config.getoption('url'))

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
