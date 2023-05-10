import os

import pytest
from _pytest.fixtures import FixtureRequest
from selenium.webdriver.remote.webdriver import WebDriver

from zenehu.pages.login_page import LoginPage
from zenehu.pages.notification_page import NotificationPage
from zenehu.pages.profile_page import ProfilePage


class BaseCase:
    authorize = True

    @pytest.fixture(autouse=True, scope='function')
    def setup(self, browser: WebDriver, request: FixtureRequest):
        self.browser = browser

        if self.authorize:
            cookies = request.getfixturevalue('cookies')
            for cookie in cookies:
                self.browser.add_cookie(cookie)
            self.browser.refresh()
