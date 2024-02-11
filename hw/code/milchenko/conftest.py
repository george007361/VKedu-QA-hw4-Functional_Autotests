import os

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager

from pages.login_page import LoginPage
from pages.profile_page import ProfilePage


@pytest.fixture(scope="function")
def browser(pytestconfig):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.set_window_size(1920, 1080)
    driver.get(pytestconfig.getoption('url'))
    yield driver
    driver.quit()


@pytest.fixture(scope="session")
def first_driver(pytestconfig):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.set_window_size(1920, 1080)
    driver.get(pytestconfig.getoption('url'))
    yield driver
    driver.quit()


@pytest.fixture(scope='session')
def cookies(pytestconfig):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(pytestconfig.getoption('url'))

    login_page = LoginPage(driver)
    login_page.login(os.getenv('IVAN_USERNAME'), os.getenv('IVAN_PASSWORD'))

    api_url = "https://vdonate.ml/api/v1"
    driver.get(api_url)

    cookies = driver.get_cookies()
    driver.quit()
    return cookies
