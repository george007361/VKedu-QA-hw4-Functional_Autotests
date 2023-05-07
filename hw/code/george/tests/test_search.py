
import os
import re

import pytest
from base_case import BaseCase
from helpers.random_data import RandomData
from pages.search_page import SearchPage

@pytest.mark.skip()
class TestSearch(BaseCase):
    authorize = True

    def test_no_results(self):
        search_page = SearchPage(self.browser)
        search_page.search(RandomData.string(15, RandomData.latin))
        search_page.is_no_results()

    def test_user_exists(self):
        search_page = SearchPage(self.browser)
        search_page.search(os.getenv("LOGIN"))
        search_page.is_users_in_list(os.getenv("LOGIN"))

    def test_search_by_enter(self):
        search_page = SearchPage(self.browser)
        search_page.search_by_enter(os.getenv("LOGIN"))
        search_page.is_users_in_list(os.getenv("LOGIN"))

    def test_user_part_name(self):
        search_page = SearchPage(self.browser)
        name = os.getenv("LOGIN")
        word = re.split('_|\s', name)[0]
        key = word[:int(-1 * len(word) / 2)]
        search_page.search(key)
        search_page.is_users_in_list(name)

    def test_user_two_words(self):
            search_page = SearchPage(self.browser)

            name = os.getenv("LOGIN")
            
            words = re.split('_|\s', name)
            
            key = ' '.join(words[:-1])

            search_page.search(key)
            search_page.is_users_in_list(name)