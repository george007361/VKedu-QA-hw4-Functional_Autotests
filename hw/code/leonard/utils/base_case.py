import pytest
from _pytest.fixtures import FixtureRequest
from selenium.webdriver.remote.webdriver import WebDriver

from leonard.pages.login_page import LoginPage
from leonard.pages.feed_page import FeedPage


class BaseCase():
    authorize = True

    @pytest.fixture(autouse=True, scope='function')
    def setup(self, driver: WebDriver, request: FixtureRequest):
        self.driver = driver
        self.currentPage = LoginPage(driver)

        if self.authorize:
            cookies = request.getfixturevalue('cookies')
            for cookie in cookies:
                self.driver.add_cookie(cookie)
            self.driver.refresh()
            self.currentPage = FeedPage(driver)
