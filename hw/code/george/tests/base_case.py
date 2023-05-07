import pytest
from selenium.webdriver.remote.webdriver import WebDriver
import os
from pages.feed_page import FeedPage
from pages.signin_page import SigninPage

class BaseCase:
    authorize = True

    @pytest.fixture(autouse=True)
    def setup(self, browser : WebDriver, request: pytest.FixtureRequest):
        self.browser = browser
        self.currentPage = SigninPage(self.browser)

        if self.authorize:
            self.currentPage.signin(os.environ["LOGIN"], os.environ["PASSWORD"])
            self.currentPage = FeedPage(self.browser)
