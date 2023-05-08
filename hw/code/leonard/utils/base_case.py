from typing import Callable
import pytest
from _pytest.fixtures import FixtureRequest
from selenium.webdriver.remote.webdriver import WebDriver

from leonard.pages.login_page import LoginPage
from leonard.pages.feed_page import FeedPage


class BaseCase():
    authorize = True
    asAuthor = True

    @pytest.fixture(autouse=True, scope='function')
    def setup(self, driverFactory: Callable[[], WebDriver], request: FixtureRequest):
        self.driver = driverFactory()
        self.currentPage = LoginPage(self.driver)

        if self.authorize:
            cookies = request.getfixturevalue('cookies')
            for cookie in cookies(self.asAuthor):
                self.driver.add_cookie(cookie)
            self.driver.refresh()
            self.currentPage = FeedPage(self.driver)


class BaseDualCase():

    @pytest.fixture(autouse=True, scope='function')
    def setup(self, driverFactory: Callable[[], WebDriver], request: FixtureRequest):
        self.authorDriver = driverFactory()
        self.donatorDriver = driverFactory()
        cookies = request.getfixturevalue('cookies')

        self.authorPage = LoginPage(self.authorDriver)
        for cookie in cookies(True):
            self.authorDriver.add_cookie(cookie)
        self.authorDriver.refresh()
        self.authorPage = FeedPage(self.authorDriver)

        self.donatorPage = LoginPage(self.donatorDriver)
        for cookie in cookies(False):
            self.donatorDriver.add_cookie(cookie)
        self.donatorDriver.refresh()
        self.donatorPage = FeedPage(self.donatorDriver)
