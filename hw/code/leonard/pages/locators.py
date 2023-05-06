from selenium.webdriver.common.by import By


class LoginPageLocators:
    USERNAME = (By.NAME, 'username')
    PASSWORD = (By.NAME, 'password')
    SUBMIT_BTN = (By.XPATH, '//form//button[@type="submit"]')
