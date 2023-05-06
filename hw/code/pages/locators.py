from selenium.webdriver.common.by import By


class BasePageLocators:
    QUERY_LOCATOR = (By.NAME, 'q')
    QUERY_LOCATOR_ID = (By.ID, 'id-search-field')
    GO_BUTTON_LOCATOR = (By.XPATH, '//*[@id="submit"]')
    START_SHELL = (By.ID, 'start-shell')
    PYTHON_CONSOLE = (By.ID, 'hterm:row-nodes')


class LoginPageLocators:
    USERNAME = (By.NAME, 'username')
    PASSWORD = (By.NAME, 'password')
    SUBMIT_BTN = (By.XPATH, '//form//button[@type="submit"]')
