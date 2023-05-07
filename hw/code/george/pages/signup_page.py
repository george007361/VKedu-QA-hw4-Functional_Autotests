from pages.base_page import BasePage
from selenium.webdriver.common.by import By


class SignupPage(BasePage):
    url = 'https://vdonate.ml/signup'

    class Locators:
        EMAIL_INPUT = (By.XPATH, '//input[starts-with(@class, "input-field__input") and (@name="email")]')
        NICKNAME_INPUT = (By.XPATH, '//input[starts-with(@class, "input-field__input") and (@name="username")]')
        PASSWORD_INPUT = (By.XPATH, '//input[starts-with(@class, "input-field__input") and (@name="password")]')
        PASSWORD_REPEAT_INPUT = (By.XPATH, '//input[starts-with(@class, "input-field__input") and (@name="repeatPassword")]')
        REGISTER_BUTTON = (By.XPATH, '//button[(@type="submit")]')
        SIGNIP_LINK = (By.XPATH, '//a[(@href="/login")]')
        SIGNUP_LINK = (By.XPATH, '//a[starts-with(@class, "entry-form__link") and (@href="/signup")]')

    def signup(self, email, nickname, passwd, repeat_passwd):
        self.render(self.url)
        self.find(self.Locators.SIGNUP_LINK).click()


        self.find(self.Locators.EMAIL_INPUT).send_keys(email)
        self.find(self.Locators.NICKNAME_INPUT).send_keys(nickname)
        self.find(self.Locators.PASSWORD_INPUT).send_keys(passwd)
        self.find(self.Locators.PASSWORD_REPEAT_INPUT).send_keys(repeat_passwd)
        
        self.find(self.Locators.REGISTER_BUTTON).click()