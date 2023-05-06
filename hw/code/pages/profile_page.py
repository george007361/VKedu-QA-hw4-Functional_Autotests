from pages.base_page import BasePage


class ProfilePage(BasePage):
    url = 'https://vdonate.ml/profile?id='

    def __init__(self, driver, aID: int):
        self.url += str(aID)
        super().__init__(driver)
