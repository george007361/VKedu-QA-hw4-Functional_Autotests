from selenium.webdriver.common.by import By


class BasePageLocators:
    NOTICE = (
        By.CSS_SELECTOR,
        'div.notice-container div.notice:nth-of-type(1) span[class~="notice__msg"]'
    )


class LoginPageLocators:
    USERNAME = (By.NAME, 'username')
    PASSWORD = (By.NAME, 'password')
    SUBMIT_BTN = (By.CSS_SELECTOR, 'form button[type="submit"]')


class ProfilePageLocators:
    ABOUT_EDIT_BTN = (
        By.CSS_SELECTOR, 'div.about__header > button'
    )
    ABOUT_CONTENT = (By.CSS_SELECTOR, 'div.about__text')
    ABOUT_CANCEL_BTN = (
        By.CSS_SELECTOR, 'form.about__form button[type="button"]'
    )
    ABOUT_SUBMIT_BTN = (
        By.CSS_SELECTOR, 'form.about__form button[type="submit"]'
    )
