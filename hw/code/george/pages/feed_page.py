from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from george.pages.base_page import BasePage

class FeedPage(BasePage):
    url = 'https://vdonate.ml/feed'

    class Locators:
        LINK_TO_PROFILE = (By.XPATH, '//a[contains(@class, "profile-container__profile-mini")]')

    def get_my_profile_link(self):
        link = self.find(self.Locators.LINK_TO_PROFILE).get_attribute('href')
        return link
    
    def open_my_profile(self):
        self.find(self.Locators.LINK_TO_PROFILE).click()
        self.wait(3).until(EC.url_changes(self.url))
