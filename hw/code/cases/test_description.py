import pytest
from cases.base_case import BaseCase
from pages.profile_page import ProfilePage


class TestProfileDescription(BaseCase):
    authorize = True

    @pytest.fixture(autouse=True)
    def profile(self, setup):
        self.driver.get('https://vdonate.ml/profile?id=9')
        self.currentPage = ProfilePage(self.driver, 9)

    def test_init(self):
        assert self.driver.current_url == 'https://vdonate.ml/profile?id=9'
