from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    url = 'https://www.vdonate.ml'

    def __init__(self, driver, load=True):
        self.driver = driver
        if load:
            self.render(self.url)

    def type_to(self, locator, text, timeout=3):
        self.find(locator, timeout).send_keys(text)

    def click(self, locator, timeout=3):
        self.wait(timeout).until(EC.element_to_be_clickable(locator)).click()

    def render(self, url):
        self.driver.get(url)

    def wait(self, timeout=3):
        return WebDriverWait(self.driver, timeout=timeout)

    def find(self, locator, timeout=3, is_visible=True):
        return self.wait(timeout).until(
            EC.visibility_of_element_located(locator)
            if is_visible else
            EC.presence_of_element_located(locator)
        )
