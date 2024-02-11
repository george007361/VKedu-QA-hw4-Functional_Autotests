import pytest
import os

from selenium.webdriver.remote.webdriver import WebDriver
from george.pages.feed_page import FeedPage

class BaseCase:
    authorize = True
    test_acc_link = 'https://vdonate.ml/profile?id=122'

    @pytest.fixture(autouse=True, scope='function')
    def setup(self, browser : WebDriver, request: pytest.FixtureRequest):
        self.browser = browser

        if self.authorize:
            cookies = request.getfixturevalue('cookies')
            for cookie in cookies:
                self.browser.add_cookie(cookie)
            self.browser.refresh()

            feed_page = FeedPage(self.browser)
            self.test_acc_link = feed_page.get_my_profile_link()
