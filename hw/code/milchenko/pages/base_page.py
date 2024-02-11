from selenium.webdriver.chrome import webdriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement

class BasePage:
    default_timeout = 5

    def __init__(self, driver: webdriver.WebDriver):
        self.driver = driver

    def render(self, url):
        self.driver.get(url)

    def wait(self, timeout=None):
        if timeout is None:
            timeout = 10
        return WebDriverWait(self.driver, timeout=timeout)
    
    def click_and_wait(self, aLocator, aTimeout=5, aCheck=lambda x: x != None):
        self.click(aLocator)
        if aTimeout:
            self.wait(aTimeout).until(aCheck)

    def FindIn(self, aElement: WebElement, aLocator, aTimeout=5, visibility=True) -> WebElement:
        return self.wait(aTimeout).until(
            lambda _:
                ec._element_if_visible(
                    aElement.find_element(*aLocator), visibility
                )
        )
    
    def find(self, locator, timeout=None):
        return self.wait(timeout).until(ec.presence_of_element_located(locator))

    def clear_and_send_keys(self, locator, keys):
        elem = self.find(locator)
        elem.clear()
        elem.send_keys(keys)

    def click(self, locator, timeout=5):
        elem = self.wait(timeout).until(ec.element_to_be_clickable(locator))
        elem.click()

    def is_clickable(self, locator):
        return ec.element_to_be_clickable(locator)

    def wait_until_clickable(self, locator, timeout=None):
        if timeout is None:
            timeout = 10
        self.wait(timeout).until(ec.element_to_be_clickable(locator))
