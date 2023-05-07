import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement


class PageNotOpenedExeption(Exception):
    pass


class BasePage(object):
    url = 'https://www.vdonate.ml'

    def __init__(self, driver: WebDriver, load=False):
        self.driver = driver
        if load:
            self.driver.get(self.url)
        self.IsOpened()

    def IsOpened(self, timeout=15):
        started = time.time()
        while time.time() - started < timeout:
            if self.driver.current_url == self.url:
                return True
        raise PageNotOpenedExeption(
            f'{self.url} did not open in {timeout} sec, current url {self.driver.current_url}')

    def Wait(self, timeout=5):
        return WebDriverWait(self.driver, timeout=timeout)

    def Find(self, locator, timeout=5) -> WebElement:
        return self.Wait(timeout).until(EC.visibility_of_element_located(locator))

    def Click(self, locator, timeout=5):
        self.Find(locator, timeout)
        elem = self.Wait(timeout).until(EC.element_to_be_clickable(locator))
        elem.click()
