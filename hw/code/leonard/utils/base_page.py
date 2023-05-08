import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement


class PageNotOpenedExeption(Exception):
    pass


class BasePage(object):
    url = 'https://www.vdonate.ml'

    def __init__(self, driver: WebDriver, aLoad=False):
        self.driver = driver
        if aLoad:
            self.driver.get(self.url)
        self.IsOpened()

    def IsOpened(self, aTimeout=15):
        started = time.time()
        while time.time() - started < aTimeout:
            if self.driver.current_url == self.url:
                return True
        raise PageNotOpenedExeption(
            f'{self.url} did not open in {aTimeout} sec, current url {self.driver.current_url}')

    def Wait(self, aTimeout=5):
        return WebDriverWait(self.driver, timeout=aTimeout)

    def Find(self, aLocator, aTimeout=5, visibility=True) -> WebElement:
        method = EC.visibility_of_element_located if visibility else EC.presence_of_element_located
        return self.Wait(aTimeout).until(method(aLocator))

    def FindIn(self, aElement: WebElement, aLocator, aTimeout=5, visibility=True) -> WebElement:
        return self.Wait(aTimeout).until(
            lambda _:
                EC._element_if_visible(
                    aElement.find_element(*aLocator), visibility
                )
        )

    def CheckStaleness(self, aElement: WebElement, aTimeout=5):
        return self.Wait(aTimeout).until(EC.staleness_of(aElement))

    def Click(self, aLocator, aTimeout=5):
        elem = self.Wait(aTimeout).until(EC.element_to_be_clickable(aLocator))
        elem.click()

    def ClickAndWait(self, aLocator, aTimeout=5, aCheck=lambda x: x != None):
        self.Click(aLocator)
        if aTimeout:
            self.Wait(aTimeout).until(aCheck)

    def Reload(self):
        self.driver.refresh()
        self.Wait(20).until(
            lambda _:
                self.driver.execute_script(
                    'return document.readyState;') == 'complete'
        )
