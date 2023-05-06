import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from pages.locators import BasePageLocators


class PageNotOpenedExeption(Exception):
    pass


class BasePage(object):

    locators = BasePageLocators()
    url = 'https://www.vdonate.ml'

    def is_opened(self, timeout=15):
        started = time.time()
        while time.time() - started < timeout:
            if self.driver.current_url == self.url:
                return True
        raise PageNotOpenedExeption(
            f'{self.url} did not open in {timeout} sec, current url {self.driver.current_url}')

    def __init__(self, driver):
        self.driver = driver
        self.is_opened()

    def wait(self, timeout=5):
        return WebDriverWait(self.driver, timeout=timeout)

    def find(self, locator, timeout=5):
        return self.wait(timeout).until(EC.visibility_of_element_located(locator))

    def click(self, locator, timeout=5):
        self.find(locator, timeout)
        elem = self.wait(timeout).until(EC.element_to_be_clickable(locator))
        elem.click()
