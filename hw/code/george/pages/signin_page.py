from selenium.webdriver.common.by import By

from pages.base_page import BasePage

class SigninPage(BasePage):
    url = 'https://vdonate.ml/login'
    class Locators:
        LOGIN_INPUT = (By.XPATH, '//input[starts-with(@class, "input-field__input") and (@name="username")]')
        PASSWORD_INPUT = (By.XPATH, '//input[starts-with(@class, "input-field__input") and (@name="password")]')
        LOGIN_BUTTON = (By.XPATH, '//button[(@type="submit")]')
        SIGNUP_LINK = (By.XPATH, '//a[(@href="/signup")]')

    def signin(self, user, passwd):
        self.render(self.url)

        self.find(self.Locators.LOGIN_INPUT).send_keys(user)
        self.find(self.Locators.PASSWORD_INPUT).send_keys(passwd)
        
        self.find(self.Locators.LOGIN_BUTTON).click()

