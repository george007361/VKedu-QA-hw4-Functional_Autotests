import string
from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import Keys

class SearchPage(BasePage):
    url = 'https://vdonate.ml/search'

    class Locators:
        SEARCH_LINE = (
            By.XPATH, '//input[starts-with(@class, "input-field__input") and (@name="searchField")]')
        SEARCH_BTN = (
            By.XPATH, '//button[contains(@class, "search-page__search-btn")]')
        RESULTS_LIST = (
            By.XPATH, '//div[contains(@class, "search-page__list-area")]')

        def RESULT_ITEM(name):
            return (By.XPATH, f'//div[contains(@class, "search-page__list-area")]//div[contains(text(), {name})]')

        def RESULTS_INFO(text):
            return (By.XPATH, f'//div[contains(@class, "search-page__list-area") and contains(text(), "{text}")]')

    def search(self, query: string):
        self.render(self.url)

        self.find(self.Locators.SEARCH_LINE).send_keys(query)
        self.find(self.Locators.SEARCH_BTN).click()

        self.wait().until(EC.element_to_be_clickable(self.Locators.SEARCH_BTN))

    def search_by_enter(self, query: string):
        self.render(self.url)

        elem = self.find(self.Locators.SEARCH_LINE)
        elem.send_keys(query)
        elem.send_keys(Keys.ENTER)

        self.wait().until(EC.element_to_be_clickable(self.Locators.SEARCH_BTN))

    def is_users_in_list(self, names):
        for name in names:
            self.find(self.Locators.RESULT_ITEM(name))

    def is_no_results(self):
        self.find(self.Locators.RESULTS_INFO('ничего не найдено'))

    # def signin(self, user, passwd):
    #     self.render(self.url)

    #     self.find(self.Locators.LOGIN_INPUT).send_keys(user)
    #     self.find(self.Locators.PASSWORD_INPUT).send_keys(passwd)

    #     self.find(self.Locators.LOGIN_BUTTON).click()
