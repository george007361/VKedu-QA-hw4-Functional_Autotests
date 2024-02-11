import os

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from zenehu.pages.base_page import BasePage


class ProfilePage(BasePage):
    base_url = 'https://vdonate.ml/feed'
    url: str

    class Locators:
        PROFILE_BUTTON = (
            By.XPATH, '//img[contains(@class, "profile-mini__avatar_size_big")]/parent::a[starts-with(@href, '
                      '"/profile")]'
        )
        PROFILE_EDIT_BUTTON = (
            By.XPATH, '//button[contains(@class, "profile-info__edit-btn")]'
        )
        PROFILE_EDIT_CROSS_BUTTON = (
            By.XPATH, '//button[contains(@class, "editor__close-btn")]'
        )
        PROFILE_EDIT_SAVE_BUTTON = (
            By.XPATH, '//span[text()="Изменить"]/parent::button'
        )
        PROFILE_EDIT_CANCEL_BUTTON = (
            By.XPATH, '//span[text()="Отменить"]/parent::button'
        )
        PROFILE_EMAIL = (
            By.XPATH, '//input[@placeholder="Введите почту"]'
        )
        PROFILE_NICKNAME = (
            By.XPATH, '//input[@placeholder="Введите псевдоним"]'
        )
        PROFILE_PASSWORD = (
            By.XPATH, '//input[@placeholder="Введите пароль"]'
        )
        PROFILE_PASSWORD_SECOND = (
            By.XPATH, '//input[@placeholder="Точно также"]'
        )
        PROFILE_AVATAR_UPLOAD = (
            By.XPATH, '//input[@title="Загрузите аватарку"]'
        )
        FIRST_POPUP = (
            By.XPATH, '(//span[contains(@class, "notice__msg")])[1]'
        )
        CLOSE_POPUP = (
            By.XPATH,
            '//div[@class="notice notice__back bg_notice-error"]/button[@class="button button__back bg_button_icon"]'
        )

    def open(self):
        self.render(self.base_url)

        self.click(self.Locators.PROFILE_BUTTON)

        self.wait(self.default_timeout).until(EC.presence_of_element_located(self.Locators.PROFILE_EDIT_BUTTON))
        self.url = self.driver.current_url

    def open_edit_page(self):
        self.open()

        self.click(self.Locators.PROFILE_EDIT_BUTTON)

        self.wait(self.default_timeout).until(EC.presence_of_element_located(self.Locators.PROFILE_EDIT_CROSS_BUTTON))

    def close_edit_page_cross(self):
        self.open_edit_page()

        self.click(self.Locators.PROFILE_EDIT_CROSS_BUTTON)

        self.wait(self.default_timeout).until(EC.element_to_be_clickable(self.Locators.PROFILE_EDIT_BUTTON))

    def close_edit_page_cancel(self):
        self.open_edit_page()

        self.click(self.Locators.PROFILE_EDIT_CANCEL_BUTTON)

        self.wait(self.default_timeout).until(EC.element_to_be_clickable(self.Locators.PROFILE_EDIT_BUTTON))

    def close_popups(self):
        buttons = self.find(self.Locators.CLOSE_POPUP)
        self.click(buttons)

    def edit_avatar(self, avatar_path):
        avatar_path = os.path.abspath(avatar_path)
        self.find(self.Locators.PROFILE_AVATAR_UPLOAD).send_keys(avatar_path)

        self.click(self.Locators.PROFILE_EDIT_SAVE_BUTTON)

        self.wait(self.default_timeout).until(EC.element_to_be_clickable(self.Locators.PROFILE_EDIT_BUTTON))

    def edit_profile(self, email, nickname, password, password_second):
        if email:
            self.clear_and_send_keys(self.Locators.PROFILE_EMAIL, email)
        if nickname:
            self.clear_and_send_keys(self.Locators.PROFILE_NICKNAME, nickname)

        self.clear_and_send_keys(self.Locators.PROFILE_PASSWORD, password)
        self.clear_and_send_keys(self.Locators.PROFILE_PASSWORD_SECOND, password_second)

        self.click(self.Locators.PROFILE_EDIT_SAVE_BUTTON)

        self.wait(self.default_timeout).until(EC.element_to_be_clickable(self.Locators.PROFILE_EDIT_BUTTON))

    def input_email(self, email):
        self.clear_and_send_keys(self.Locators.PROFILE_EMAIL, email)

    def input_nickname(self, nickname):
        self.clear_and_send_keys(self.Locators.PROFILE_NICKNAME, nickname)

    def input_password(self, password):
        self.find(self.Locators.PROFILE_PASSWORD).send_keys(password)

    def input_password_second(self, password_second):
        self.find(self.Locators.PROFILE_PASSWORD_SECOND).send_keys(password_second)

    def get_popup_text(self):
        return self.find(self.Locators.FIRST_POPUP).text
