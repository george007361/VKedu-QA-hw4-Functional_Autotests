import pytest
from selenium.webdriver.remote.webdriver import WebDriver
import os
from pages.feed_page import FeedPage
from pages.signin_page import SigninPage

class BaseCase:
    authorize = True

    @pytest.fixture(autouse=True, scope='function')
    def setup(self, browser : WebDriver, request: pytest.FixtureRequest):
        self.browser = browser

        if self.authorize:
            cookies = request.getfixturevalue('cookies')
            for cookie in cookies:
                self.browser.add_cookie(cookie)
            self.browser.refresh()

