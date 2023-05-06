import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class PageNotOpenedExeption(Exception):
    pass


class BasePage(object):
    url = 'https://www.vdonate.ml'

    def __init__(self, driver):
        self.driver = driver
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

    def Find(self, locator, timeout=5):
        return self.Wait(timeout).until(EC.visibility_of_element_located(locator))

    def Click(self, locator, timeout=5):
        self.Find(locator, timeout)
        elem = self.Wait(timeout).until(EC.element_to_be_clickable(locator))
        elem.click()
