from leonard.utils.base_page import BasePage
from leonard.utils.locators import LoginPageLocators


class LoginPage(BasePage):
    locators = LoginPageLocators()
    url = 'https://vdonate.ml/login'

    def Login(self, username, password):
        self.Find(self.locators.USERNAME).send_keys(username)
        self.Find(self.locators.PASSWORD).send_keys(password)
        self.Click(self.locators.SUBMIT_BTN)
        return
