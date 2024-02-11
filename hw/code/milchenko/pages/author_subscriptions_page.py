from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from milchenko.pages.base_page import BasePage

class AuthorSubscriptionsPage(BasePage):
    base_url = 'https://vdonate.ml/feed'
    url: str

    class Locators:
        PROFILE_BUTTON = (
            By.XPATH, '//img[contains(@class, "profile-mini__avatar_size_big")]/parent::a[starts-with(@href, '
                      '"/profile")]'
        )
        ADD_SUBSCRIPTION_BUTTON = (
            By.XPATH,
            '//div[@class="subscription-cards-container__title-area font_big"]/button[@class="button button__back bg_button_icon"]'
        )
        SUBSCRIPTION_TITLE = (
            By.XPATH,
            '//span[text()="Создание подписки"]'
        )
        SUBSCRIPTION_CLOSE_CROSS = (
            By.XPATH,
            '//button[@class="button button__back bg_button_icon editor__close-btn"]'
        )
        SUBSCRIPTION_CLOSE_CANCEL = (
            By.XPATH,
            '//button[@class="button button__back bg_button_outline btn-area__btn"]'
        )
        SUBSCRIPTIONS_LEVEL = (
            By.XPATH,
            '//div[@class="subscription-cards-container__title-area font_big"]'
        )
        TITLE_INPUT = (
            By.XPATH,
            '//input[@placeholder="Придумайте заголовок для подписки"]'
        )
        PRICE_INPUT = (
            By.XPATH,
            '//input[@placeholder="Введите стоимость подписки"]'
        )
        TEXT_INPUT = (
            By.XPATH,
            '//textarea[@placeholder="Замотивируйте своих донатеров"]'
        )
        CREATE_BUTTON = (
            By.XPATH,
            '//button[@class="button button__back bg_button_primary btn-area__btn"]'
        )
        FIRST_POPUP = (
            By.XPATH, '(//span[contains(@class, "notice__msg")])[1]'
        )
        EDIT_BUTTON = (
            By.XPATH,
            '//button[@class="button button__back bg_button_sub-2 subscription-card__button"]'
        )
        UPDATE_BUTTON = (
            By.XPATH,
            '//button[@class="button button__back bg_button_primary btn-area__btn"]'
        )
        DELETE_BUTTON = (
            By.XPATH,
            '//button[@class="button button__back bg_button_error btn-area__btn"]'
        )
        EMPTY_SUBSCRIPTIONS = (
            By.XPATH,
            '//div[@class="subscription-cards-container__empty font_regular bg_main"]'
        )
        FIELD_TITLE = (
            By.XPATH,
            '//span[@class="subscription-card__title font_regular"]'
        )
        FIELD_PRICE = (
            By.XPATH,
            '//span[@class="price__count font_regular"]'
        )
        FIELD_TEXT = (
            By.XPATH,
            '//div[@class="subscription-card__motivation font_small"]'
        )

    def open(self):
        self.render(self.base_url)

        self.click(self.Locators.PROFILE_BUTTON)

        self.wait(self.default_timeout).until(EC.presence_of_element_located(self.Locators.ADD_SUBSCRIPTION_BUTTON))
        self.url = self.driver.current_url

    def open_subs(self):
        self.click(self.Locators.ADD_SUBSCRIPTION_BUTTON)
        self.wait().until(EC.presence_of_element_located(self.Locators.SUBSCRIPTION_TITLE))

    def open_update(self):
        self.click(self.Locators.EDIT_BUTTON)
        self.wait().until(EC.presence_of_element_located(self.Locators.DELETE_BUTTON))

    def close_subs(self, is_cross=True):
        self.click(self.Locators.SUBSCRIPTION_CLOSE_CROSS if is_cross else self.Locators.SUBSCRIPTION_CLOSE_CANCEL)
        self.wait().until(EC.presence_of_element_located(self.Locators.ADD_SUBSCRIPTION_BUTTON))

    def create_subscription(self, title, price, text, update=False):
        t = self.find(self.Locators.TITLE_INPUT)
        if update:
            t.clear()
        t.send_keys(title)

        p = self.find(self.Locators.PRICE_INPUT)
        if update:
            p.clear()
        p.send_keys(price)

        txt = self.find(self.Locators.TEXT_INPUT)
        if update:
            txt.clear()
        txt.send_keys(text)
        
        self.click(self.Locators.CREATE_BUTTON if not update else self.Locators.UPDATE_BUTTON)
        self.wait().until(
            EC.any_of(
                EC.presence_of_element_located(self.Locators.ADD_SUBSCRIPTION_BUTTON),
                EC.presence_of_element_located(self.Locators.FIRST_POPUP)
            )
        )            

    def delete_subscription(self):
        self.click(self.Locators.EDIT_BUTTON)
        self.click(self.Locators.DELETE_BUTTON)
        self.wait(5).until(EC.presence_of_element_located(self.Locators.EMPTY_SUBSCRIPTIONS))
