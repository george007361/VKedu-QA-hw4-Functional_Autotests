import os

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager

from pages.login_page import LoginPage
from pages.notification_page import NotificationPage
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


@pytest.fixture(scope="session")
def second_driver(pytestconfig):
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
    login_page.login(os.getenv('ALB_USERNAME'), os.getenv('ALB_PASSWORD'))

    api_url = "https://vdonate.ml/api/v1"
    driver.get(api_url)

    cookies = driver.get_cookies()
    driver.quit()
    return cookies


@pytest.fixture(scope='session', autouse=True)
def make_notifications(first_driver, second_driver: WebDriver):
    login_page_1 = LoginPage(first_driver)
    login_page_1.login(os.getenv('ALB_USERNAME'), os.getenv('ALB_PASSWORD'))

    profile_page = ProfilePage(first_driver)
    profile_page.open()

    url = profile_page.url

    login_page_2 = LoginPage(second_driver)
    login_page_2.login(os.getenv('ALB_USERNAME_2'), os.getenv('ALB_PASSWORD_2'))

    second_driver.get(url)

    for i in range(2):
        login_page_2.click(NotificationPage.Locators.SUBSCRIBE_BUTTON)
        login_page_2.click(NotificationPage.Locators.UNSUBSCRIBE_BUTTON)

    first_driver.quit()
    second_driver.quit()
