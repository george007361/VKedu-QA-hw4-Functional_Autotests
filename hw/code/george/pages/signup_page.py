from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage

class SignupPage(BasePage):
    url = 'https://vdonate.ml/signup'

    class Locators:
        EMAIL_INPUT = (
            By.XPATH, '//input[starts-with(@class, "input-field__input") and (@name="email")]')
        NICKNAME_INPUT = (
            By.XPATH, '//input[starts-with(@class, "input-field__input") and (@name="username")]')
        PASSWORD_INPUT = (
            By.XPATH, '//input[starts-with(@class, "input-field__input") and (@name="password")]')
        PASSWORD_REPEAT_INPUT = (
            By.XPATH, '//input[starts-with(@class, "input-field__input") and (@name="repeatPassword")]')
        REGISTER_BUTTON = (By.XPATH, '//button[(@type="submit")]')
        SIGNIP_LINK = (By.XPATH, '//a[(@href="/login")]')
        SIGNUP_LINK = (
            By.XPATH, '//a[starts-with(@class, "entry-form__link") and (@href="/signup")]')

    def signup(self, email, nickname, passwd, repeat_passwd):
        self.click(self.Locators.SIGNUP_LINK)

        self.type_to(self.Locators.EMAIL_INPUT, email)
        self.type_to(self.Locators.NICKNAME_INPUT, nickname)
        self.type_to(self.Locators.PASSWORD_INPUT, passwd)
        self.type_to(self.Locators.PASSWORD_REPEAT_INPUT, repeat_passwd)

        self.click(self.Locators.REGISTER_BUTTON)
        self.wait(2).until(EC.any_of(
            EC.url_changes(self.url),
            EC.element_to_be_clickable(self.Locators.REGISTER_BUTTON),
        ))
