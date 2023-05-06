from cases.base_case import BaseCase


class TestProfileDescription(BaseCase):
    def test_init(self):
        assert self.driver.current_url == 'https://vdonate.ml/feed'
