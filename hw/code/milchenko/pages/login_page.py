from selenium.webdriver.common.by import By

from milchenko.pages.base_page import BasePage

class LoginPage(BasePage):
    url = 'https://vdonate.ml/login'

    class Locators:
        LOGIN_INPUT = (By.XPATH, '//input[starts-with(@class, "input-field__input") and (@name="username")]')
        PASSWORD_INPUT = (By.XPATH, '//input[starts-with(@class, "input-field__input") and (@name="password")]')
        LOGIN_BUTTON = (By.XPATH, '//button[(@type="submit")]')
        MENU_BTN = (By.XPATH, '//div[@class="profile-container"]/button')
        LOGOUT_BTN = (By.XPATH, '//span[text()="Выйти"]/parent::button')

    def login(self, username, password):
        self.render(self.url)

        self.find(self.Locators.LOGIN_INPUT).send_keys(username)
        self.find(self.Locators.PASSWORD_INPUT).send_keys(password)

        self.click(self.Locators.LOGIN_BUTTON)
        self.wait_until_clickable(self.Locators.MENU_BTN)

    def logout(self):
        self.click(self.Locators.MENU_BTN)
        self.click(self.Locators.LOGOUT_BTN)
