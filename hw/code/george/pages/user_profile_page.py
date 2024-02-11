from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage

class UserProfilePage(BasePage):
    url = ''

    class Locators:
        SUBSCRIBE_BTN = (By.XPATH, '//div[contains(@class, "follow-button")]//button//span[contains(@class, "button__text")]')

    def __init__(self, driver, url):
        self.url = url
        super().__init__(driver, load=False)
        self.render(self.url)

    def is_followed(self):
        try:
            text = self.find(self.Locators.SUBSCRIBE_BTN).text
            if text == 'Подписаться': 
                return False
            elif text == 'Отписаться':
                return True
            else:
                raise Exception(f"Invalid text in follow btn: {text}")
        except:
            raise Exception("Cant locate elem")
        
    def change_subscription(self):
        self.click(self.Locators.SUBSCRIBE_BTN)
        self.wait(2).until(EC.element_to_be_clickable(self.Locators.SUBSCRIBE_BTN))