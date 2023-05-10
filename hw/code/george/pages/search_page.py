import string
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import Keys

from pages.base_page import BasePage

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
        self.type_to(self.Locators.SEARCH_LINE, query)
        self.click(self.Locators.SEARCH_BTN)
        self.wait().until(EC.element_to_be_clickable(self.Locators.SEARCH_BTN))

    def search_by_enter(self, query: string):
        self.type_to(self.Locators.SEARCH_LINE, query)
        self.type_to(self.Locators.SEARCH_LINE,Keys.ENTER)
        self.wait().until(EC.element_to_be_clickable(self.Locators.SEARCH_BTN))

    def is_users_in_list(self, names):
        for name in names:
            self.find(self.Locators.RESULT_ITEM(name))
    
    def get_link_to_user(self, name):
        link = self.find(self.Locators.RESULT_ITEM(name)).get_attribute('href')
        return link

    def is_no_results(self):
        self.find(self.Locators.RESULTS_INFO('ничего не найдено'))

