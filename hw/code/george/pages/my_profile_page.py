import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage

class MyProfilePage(BasePage):
    url = ''

    class Locators:
        BTN_TO_BE_AUTHOR = (By.XPATH, '//button//span[contains(@class, "button__text") and contains(text(), "Стать автором")]')

    def __init__(self, driver, url):
        self.url = url
        super().__init__(driver, load=False)
        self.render(self.url)

    def became_author(self):
        self.click(self.Locators.BTN_TO_BE_AUTHOR)
        self.wait(3).until_not(EC.presence_of_element_located(self.Locators.BTN_TO_BE_AUTHOR))
    
    def check_is_author(self) -> bool:
        try:
            self.find(self.Locators.BTN_TO_BE_AUTHOR)
            return False
        except:
            return True