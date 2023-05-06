import pytest
from _pytest.fixtures import FixtureRequest
from selenium.webdriver.remote.webdriver import WebDriver

from pages.login_page import LoginPage
from pages.feed_page import FeedPage

import time


class BaseCase():
    authorize = True

    @pytest.fixture(autouse=True)
    def setup(self, driver: WebDriver, request: FixtureRequest):
        self.driver = driver
        self.loginPage = LoginPage(driver)

        if self.authorize:
            cookies = request.getfixturevalue('cookies')
            for cookie in cookies:
                self.driver.add_cookie(cookie)
            self.driver.refresh()
            self.feedPage = FeedPage(driver)
