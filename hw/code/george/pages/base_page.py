from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def render(self, url):
        self.driver.get(url)

    def wait(self, timeout=3):
        return WebDriverWait(self.driver, timeout=timeout)

    def find(self, locator, timeout=3):
        return self.wait(timeout).until(EC.presence_of_element_located(locator))