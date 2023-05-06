from pages.base_page import BasePage
from pages.locators import LoginPageLocators


class LoginPage(BasePage):
    locators = LoginPageLocators()
    url = 'https://vdonate.ml/login'

    def login(self, username, password):
        self.find(self.locators.USERNAME).send_keys(username)
        self.find(self.locators.PASSWORD).send_keys(password)
        self.click(self.locators.SUBMIT_BTN)
        return
