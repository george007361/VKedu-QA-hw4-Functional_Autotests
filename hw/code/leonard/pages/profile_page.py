import time
from leonard.utils.locators import ProfilePageLocators
from leonard.utils.base_page import BasePage


class ProfilePage(BasePage):
    url = 'https://vdonate.ml/profile?id='
    locators = ProfilePageLocators()

    def __init__(self, driver, aID: int):
        self.url += str(aID)
        super().__init__(driver)

    def GetAboutContent(self):
        return self.Find(self.locators.ABOUT_CONTENT)

    def GetCreatePostContent(self):
        return self.Find(self.locators.POST_CREATE_CONTENT)

    def GetLastPostContent(self):
        return self.Find(self.locators.POST_LAST)

    def ClickAboutEditBtn(self):
        self.Click(self.locators.ABOUT_EDIT_BTN)

    def ClickAboutCancelBtn(self):
        self.Click(self.locators.ABOUT_CANCEL_BTN)

    def ClickAboutSubmitBtn(self, timeout=1):
        self.Click(self.locators.ABOUT_SUBMIT_BTN)
        # Wait на обработку текста при нажатии submit
        started = time.time()
        while time.time() - started < timeout:
            if self.GetAboutContent().get_attribute('contenteditable') == 'false':
                return

    def ClickPostCreateBtn(self):
        self.Click(self.locators.POST_CREATE_BTN)

    def ClickPostCreaterSubmitBtn(self, timeout=1):
        self.Click(self.locators.POST_CREATER_SUBMIT_BTN)
        # Wait на обработку текста при нажатии submit
        started = time.time()
        while time.time() - started < timeout:
            if len(self.driver.find_elements(*self.locators.POST_CREATE_CONTENT)) == 0:
                return

    def ClickPostCreaterCanselBtn(self):
        self.Click(self.locators.POST_CREATER_CANCEL_BTN)
