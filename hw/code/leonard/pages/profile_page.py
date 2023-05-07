import time
from leonard.utils.locators import ProfilePageLocators
from leonard.utils.base_page import BasePage


class ProfilePage(BasePage):
    url = 'https://vdonate.ml/profile?id='
    locators = ProfilePageLocators()

    def __init__(self, driver, aID: int):
        self.url += str(aID)
        super().__init__(driver)

    def GetAbout(self):
        return self.Find(self.locators.ABOUT_CONTENT)

    def ClickAboutEditBtn(self):
        self.Click(self.locators.ABOUT_EDIT_BTN)

    def ClickAboutCancelBtn(self):
        self.Click(self.locators.ABOUT_CANCEL_BTN)

    def ClickAboutSubmitBtn(self, timeout=1):
        self.Click(self.locators.ABOUT_SUBMIT_BTN)
        # Оттяжка на обработку текста при нажатии submit
        started = time.time()
        while time.time() - started < timeout:
            if self.GetAbout().get_attribute('contenteditable') == 'false':
                return
